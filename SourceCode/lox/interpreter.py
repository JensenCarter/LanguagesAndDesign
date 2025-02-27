from lox.expressions import ExprVisitor
from lox.tokens import TokenType

class Interpreter(ExprVisitor):
    def interpret(self, expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr):
        left = self.interpret(expr.left)
        right = self.interpret(expr.right)
        operator_type = expr.operator.type

        if operator_type == TokenType.PLUS:
            return left + right
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
        right = self.interpret(expr.right)
        operator_type = expr.operator.type
        if operator_type == TokenType.MINUS:
            return -right
        elif operator_type == TokenType.BANG:
            return not right
        else:
            raise Exception("Unknown unary operator")

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_grouping_expr(self, expr):
        return self.interpret(expr.expression)

    # Stub implementations for additional abstract methods (not used in Stage 2)
    def visit_assign_expr(self, expr):
        raise NotImplementedError("Assignment expressions are not implemented in Stage 2.")

    def visit_call_expr(self, expr):
        raise NotImplementedError("Call expressions are not implemented in Stage 2.")

    def visit_get_expr(self, expr):
        raise NotImplementedError("Property access expressions are not implemented in Stage 2.")

    def visit_logical_expr(self, expr):
        raise NotImplementedError("Logical expressions are not implemented in Stage 2.")

    def visit_set_expr(self, expr):
        raise NotImplementedError("Property setting expressions are not implemented in Stage 2.")

    def visit_super_expr(self, expr):
        raise NotImplementedError("Super expressions are not implemented in Stage 2.")

    def visit_this_expr(self, expr):
        raise NotImplementedError("'this' expressions are not implemented in Stage 2.")

    def visit_variable_expr(self, expr):
        raise NotImplementedError("Variable expressions are not implemented in Stage 2.")
