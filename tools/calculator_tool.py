"""
Enterprise Calculator Tool
Safe mathematical expression evaluator for quantitative analysis tasks.
"""

import math
import ast
import operator
from crewai.tools import BaseTool
from utils.logger import get_logger

logger = get_logger(__name__)

# Allowed operators and math functions for safe evaluation
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

SAFE_FUNCTIONS = {
    "abs": abs, "round": round, "min": min, "max": max,
    "sum": sum, "pow": pow, "sqrt": math.sqrt, "log": math.log,
    "log10": math.log10, "log2": math.log2, "exp": math.exp,
    "ceil": math.ceil, "floor": math.floor, "factorial": math.factorial,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "pi": math.pi, "e": math.e,
}


def _safe_eval(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Name):
        if node.id in SAFE_FUNCTIONS:
            return SAFE_FUNCTIONS[node.id]
        raise ValueError(f"Unknown name: {node.id}")
    elif isinstance(node, ast.BinOp):
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op)}")
        return op(_safe_eval(node.left), _safe_eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op)}")
        return op(_safe_eval(node.operand))
    elif isinstance(node, ast.Call):
        func = _safe_eval(node.func)
        args = [_safe_eval(a) for a in node.args]
        return func(*args)
    else:
        raise ValueError(f"Unsupported node type: {type(node)}")


class CalculatorTool(BaseTool):
    """
    Safe mathematical expression evaluator.

    Supports arithmetic, exponentiation, modulo, and common math functions
    (sqrt, log, sin, cos, etc.). Does NOT execute arbitrary code.

    Example inputs:
        "sqrt(144) + 2^10"
        "log10(1000000)"
        "factorial(10) / factorial(5)"
    """

    name: str = "Calculator"
    description: str = (
        "Evaluate mathematical expressions safely. Use for computing statistics, "
        "growth rates, percentages, financial metrics, or any numerical analysis. "
        "Supports arithmetic, exponents, sqrt, log, sin, cos, factorial, and more. "
        "Input should be a valid math expression as a string."
    )

    def _run(self, expression: str) -> str:
        expression = expression.strip()
        logger.info(f"[CalculatorTool] Evaluating: '{expression}'")
        try:
            tree = ast.parse(expression, mode="eval")
            result = _safe_eval(tree.body)
            formatted = f"{result:,.6g}" if isinstance(result, float) else str(result)
            logger.info(f"[CalculatorTool] Result: {formatted}")
            return f"Expression: {expression}\nResult: {formatted}"
        except ZeroDivisionError:
            return "Error: Division by zero."
        except Exception as exc:
            logger.warning(f"[CalculatorTool] Failed: {exc}")
            return (
                f"Could not evaluate '{expression}': {exc}. "
                "Ensure the expression uses supported syntax and functions."
            )
