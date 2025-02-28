from lox.expressions import ExprVisitor, Variable, Assignment, Binary, Unary, Literal, Grouping
from lox.statements import StmtVisitor, Print, Expression
from lox.tokens import TokenType, Token


class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name: str, value):
        self.values[name] = value

    def assign(self, name: Token, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.globals.define("input", lambda prompt: input(prompt))

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
        try:
            # assign the variable if it exists
            self.environment.assign(expr.name, value)
        except RuntimeError:
            # if not define it
            self.environment.define(expr.name.lexeme, value)
        return value

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

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
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(arg) for arg in expr.arguments]
        if callable(callee):
            return callee(*arguments)
        else:
            raise RuntimeError("Can only call functions")

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

    def visit_if_stmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_block_stmt(self, stmt):
        previous = self.environment
        self.environment = Environment(previous)
        try:
            for statement in stmt.statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def execute(self, stmt):
        stmt.accept(self)