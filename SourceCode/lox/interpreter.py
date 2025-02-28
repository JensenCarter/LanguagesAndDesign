from lox.expressions import ExprVisitor, Variable, Assignment, Binary, Unary, Literal, Grouping
from lox.statements import StmtVisitor, Print, Expression
from lox.tokens import TokenType


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals = {}  # global dictionary for variable values
        self.environment = self.globals

    def interpret(self, statements):
        for stmt in statements:
            stmt.accept(self)

    def visit_print_stmt(self, stmt):
        # handle print statements
        value = self.evaluate(stmt.expression)
        print(value)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)

    def visit_assignment_expr(self, expr):
        value = self.evaluate(expr.value)
        self.globals[expr.name] = value  # store in global dictionary
        return value

    def visit_variable_expr(self, expr):
        # look up variables value
        if expr.name in self.globals:
            return self.globals[expr.name]
        raise RuntimeError(f"Undefined variable '{expr.name}'.")

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        operator_type = expr.operator.type

        if operator_type == TokenType.PLUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            elif isinstance(left, str) and isinstance(right, str):
                return left + right
            else:
                raise RuntimeError("Operands must be two numbers or two strings")
        elif operator_type == TokenType.MINUS:
            return left - right
        elif operator_type == TokenType.MUL:
            return left * right
        elif operator_type == TokenType.DIV:
            return left / right
        elif operator_type == TokenType.EQUAL_EQUAL:
            return left == right
        elif operator_type == TokenType.BANG_EQUAL:
            return left != right
        elif operator_type == TokenType.LESS:
            return left < right
        elif operator_type == TokenType.LESS_EQUAL:
            return left <= right
        elif operator_type == TokenType.GREATER:
            return left > right
        elif operator_type == TokenType.GREATER_EQUAL:
            return left >= right
        elif operator_type == TokenType.AND:
            return left and right
        elif operator_type == TokenType.OR:
            return left or right
        else:
            raise Exception("Unknown binary operator")

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -right
        elif expr.operator.type == TokenType.BANG:
            return not right
        else:
            raise Exception("Unknown unary operator")

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_call_expr(self, expr):
        raise NotImplementedError("not implemented")

    def visit_get_expr(self, expr):
        raise NotImplementedError("not implemented")

    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left): return left
        else:
            if not self.is_truthy(left): return left
        return self.evaluate(expr.right)

    def is_truthy(self, value):
        if value is None: return False
        if isinstance(value, bool): return value
        return True

    def visit_set_expr(self, expr):
        raise NotImplementedError("not implemented")

    def visit_super_expr(self, expr):
        raise NotImplementedError("not implemented")

    def visit_this_expr(self, expr):
        raise NotImplementedError("not implemented")

    def evaluate(self, expr):
        return expr.accept(self)
