import ast
from typing import Any, cast

import sympy

from QHyper.util import QUBO, VARIABLES


# TODO slack_coefficients is dict[str, Any] and num_slack is int
# def calc_slack_coefficients(constant: int) -> dict[str, int]:
#     num_slack = int(np.floor(np.log2(constant)))
#     slack_coefficients = {f's{j}': 2 ** j for j in range(num_slack)}
#     if constant - 2 ** num_slack >= 0:
#         slack_coefficients[num_slack] = constant - 2 ** num_slack + 1
#     return slack_coefficients


class Parser(ast.NodeVisitor):
    def __init__(self) -> None:
        self.polynomial_as_dict: QUBO = {}

    # todo make sure it is a single expression
    def visit_Expr(self, node: ast.Expr) -> Any:
        visit_value = self.visit(node.value)

        if isinstance(visit_value, list):
            for i in cast(list[tuple[VARIABLES, float]], visit_value):
                self.polynomial_as_dict[tuple(i[0])] = i[1]
        elif isinstance(visit_value, str):
            # expression consisting of a single variable name
            self.polynomial_as_dict[(visit_value,)] = 1
        elif isinstance(visit_value, (int, float)):
            # expression consisting of a single numerical value
            self.polynomial_as_dict[()] = visit_value
        else:
            raise Exception

    def visit_BinOp(self, node: ast.BinOp) -> Any:

        left = self.visit(node.left)
        right = self.visit(node.right)

        if isinstance(node.op, ast.Add):
            return self.tmp(left, right)

        if isinstance(node.op, ast.Sub):
            return self.tmp(left, right, multiplier=-1)

        if isinstance(node.op, ast.Mult):
            if isinstance(left, list):
                variable, constant = left[0]
            else:
                variable, constant = [], 1
                if isinstance(left, str):
                    variable.append(left)
                elif isinstance(left, (int, float)):
                    constant *= left

            if isinstance(right, str):
                variable.append(right)
            elif isinstance(right, (int, float)):
                constant *= right
            elif isinstance(right, list):
                # todo - check that!!! only in the case of powers:
                variable += right[0][0]
            return [[variable, constant]]

        if isinstance(node.op, ast.Pow):
            node.left = cast(ast.Name, node.left)
            node.right = cast(ast.Constant, node.right)
            return [[[node.left.id for _ in range(node.right.value)], 1]]

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            if isinstance(operand, (int, float)):
                return [[[], -operand]]
            elif isinstance(operand, list):
                operand[0][1] = -1 * operand[0][1]
                return operand
            else:  # is there any exception case?
                return [[[operand], -1]]

        if isinstance(node.op, ast.UAdd):
            return operand

    def visit_Constant(self, node: ast.Constant) -> Any:
        return node.value

    def visit_Name(self, node: ast.Name) -> Any:
        return node.id

    @staticmethod
    def tmp(left: Any, right: Any, multiplier: int = 1) -> list[Any]:

        if isinstance(left, list):
            if isinstance(right, list):
                # todo not sure if right should be modifed if it is static
                right[0][1] = multiplier * right[0][1]
                return left + right
            elif isinstance(right, (int, float)):
                return left + [[[], multiplier * right]]
            elif isinstance(right, str):
                return left + [[[right], multiplier]]
        elif isinstance(right, list):
            right[0][1] = multiplier * right[0][1]
            if isinstance(left, str):
                return [[[left], 1]] + right
            if isinstance(left, (int, float)):
                return [[[], left]] + right
        elif isinstance(right, (int, float)):
            right *= multiplier
            if isinstance(left, str):
                return [[[left], 1]] + [[[], right]]
            if isinstance(left, (int, float)):
                return [[[], left]] + [[[], right]]
        elif isinstance(right, str):
            if isinstance(left, str):
                return [[[left], 1]] + [[[right], multiplier]]
            if isinstance(left, (int, float)):
                return [[[], left]] + [[[right], multiplier]]
        raise Exception


class Expression:
    def __init__(self, equation: sympy.core.Expr | dict) -> None:
        if isinstance(equation, sympy.core.Expr):
            self.polynomial: sympy.core.Expr | None = equation
            self.dictionary: dict = self.as_dict()
        elif isinstance(equation, dict):
            self.polynomial: sympy.core.Expr | None = None
            self.dictionary: dict = equation
        else:
            raise Exception(
                "Expression equation must be an instance of "
                "sympy.core.Expr or dict, got of type: "
                f"{type(equation)} instead"
            )

    def as_dict(self) -> QUBO:
        if self.polynomial is not None:
            parser = Parser()
            ast_tree = ast.parse(
                str(sympy.expand(self.polynomial))
            )  # type: ignore[no-untyped-call]
            parser.visit(ast_tree)
            self.dictionary = parser.polynomial_as_dict
        return self.dictionary

    def __repr__(self) -> str:
        return str(self.dictionary)

    # def as_dict_with_slacks(self):
    #     parser = Parser()
    #     objective_function = sympy.expand(self.polynomial)
    #     ast_tree = ast.parse(str(objective_function))
    #     parser.visit(ast_tree)

    #     result = parser.polynomial_as_dict
    #     if self.op == '==':
    #         return result

    #     if self.op == '<=':
    #         if tuple() in result:
    #             value = result[tuple()]
    #             return result | calc_slack_coefficients(value)
    #         return result
    #     else:
    #         raise Exception("Unimplemented")

    def as_polynomial(self) -> str:
        if self.polynomial is not None:
            return str(self.polynomial)
        else:
            polynomial = str()
            for k in self.dictionary:
                if self.dictionary[k] < 0:
                    polynomial += "- "
                polynomial += str(abs(self.dictionary[k])) + "*"
                polynomial += "*".join(k)
                polynomial += " "
            return polynomial.rstrip()
