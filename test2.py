import ast
import operator

from langchain.tools import tool

# 允许使用的数学运算符
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def safe_calculate(expression: str):
    """仅计算简单的数学表达式。"""

    # 限制表达式长度，防止过大输入
    if len(expression) > 100:
        raise ValueError("表达式过长")

    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        # 数字常量
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                if abs(node.value) > 1_000_000_000:
                    raise ValueError("数字过大")
                return node.value

        # 二元运算
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)

            if op_type not in OPERATORS:
                raise ValueError("不支持的运算符")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if op_type is ast.Div and right == 0:
                raise ValueError("除数不能为零")

            result = OPERATORS[op_type](left, right)

            if abs(result) > 1_000_000_000:
                raise ValueError("计算结果过大")

            return result

        # 一元正负号
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)

            if op_type not in (ast.UAdd, ast.USub):
                raise ValueError("不支持的运算符")

            return OPERATORS[op_type](
                evaluate(node.operand)
            )

        raise ValueError("不支持的表达式")

    return evaluate(tree.body)


@tool
def calculate(expression: str) -> str:
    """计算简单数学表达式，支持加减乘除和括号。

    Args:
        expression: 例如 "3 * 7 + 2" 或 "(25 - 18)"。
    """
    try:
        result = safe_calculate(expression)

        return f"计算结果：{expression} = {result}"

    except (
        ValueError,
        SyntaxError,
        ZeroDivisionError,
        OverflowError
    ) as error:
        return f"计算失败：{error}"