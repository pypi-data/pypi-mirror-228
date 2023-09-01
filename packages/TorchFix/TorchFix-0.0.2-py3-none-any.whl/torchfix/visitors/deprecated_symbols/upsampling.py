import libcst as cst
import libcst.matchers as m
from typing import Optional, Tuple


def call_replacement_upsampling(node: cst.Call) -> cst.Call:
    """Replace `nn.UpsamplingNearest2d` and `nn.UpsamplingNearest2d` with
    appropriately parametrized `torch.nn.functional.interpolate`.
    """

    end_arg, step_arg = _get_range_args(node)
    step = 1
    if step_arg is not None:
        # `step` is a literal integer
        if isinstance(step_arg.value, cst.Integer):
            step = int(step_arg.value.value)

        # `step` is unary minus and an integer (i.e. negative integer)
        elif m.matches(
            step_arg,
            m.Arg(value=m.UnaryOperation(operator=m.Minus(), expression=m.Integer())),
        ):
            step = -int(step_arg.value.expression.value)

        # Bail out, don't know how to update with non-integer `step`.
        else:
            return None

    updated_end_arg = None

    # `end` is a literal (positive) integer
    if isinstance(end_arg.value, cst.Integer):
        end = int(end_arg.value.value) + step
        if end >= 0:
            updated_end_arg = end_arg.with_deep_changes(
                old_node=end_arg.value, value=str(end)
            )
        else:
            # `end` became negative
            updated_end_arg = end_arg.with_changes(
                value=cst.UnaryOperation(
                    operator=cst.Minus(),
                    expression=cst.Integer(value=str(-end)),
                )
            )

    # `end` is a unary minus and an integer (i.e. negative integer)
    elif m.matches(
        end_arg,
        m.Arg(value=m.UnaryOperation(operator=m.Minus(), expression=m.Integer())),
    ):
        end = -int(end_arg.value.expression.value) + step
        if end < 0:
            updated_end_arg = end_arg.with_deep_changes(
                old_node=end_arg.value.expression, value=str(-end)
            )
        else:
            # `end` became non-negative
            updated_end_arg = end_arg.with_changes(value=cst.Integer(value=str(end)))

    # `end` is an expression with `- 1` at the end: remove the `- 1`.
    # This is a common occurrence, thus special handling.
    elif m.matches(
        end_arg,
        m.Arg(
            value=m.BinaryOperation(operator=m.Subtract(), right=m.Integer(value="1"))
        ),
    ):
        updated_end_arg = end_arg.with_changes(value=end_arg.value.left)

    # `end` something else: add `+ 1` at the end
    else:
        updated_end_arg = end_arg.with_changes(
            value=cst.BinaryOperation(
                left=end_arg.value,
                operator=cst.Add(),
                right=cst.Integer(value="1"),
            )
        )

    replacement = node
    if updated_end_arg is not None:
        replacement = replacement.deep_replace(end_arg, updated_end_arg)
    replacement = replacement.with_deep_changes(
        old_node=replacement.func.attr, value="arange"
    )

    return replacement
