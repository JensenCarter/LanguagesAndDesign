from lox.tokens import TokenType
from lox.expressions import Binary, Grouping, Literal, Unary, Variable, Assignment
from lox.statements import Print, Expression

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        # store parsed statements
        statements = []
        while not self._is_at_end():
            statements.append(self.statement())
        return statements

    def statement(self):
        # check if token is print statement or an expression
        if self.match(TokenType.PRINT):
            return self.print_statement()
        return self.expression_statement()

    def print_statement(self):
        expr = self.expression()
        return Print(expr)

    def expression_statement(self):
        expr = self.expression()
        return Expression(expr)

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.logic_or()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                return Assignment(expr.name, value)
            raise RuntimeError("Invalid assignment target.")
        return expr

    def logic_or(self):
        expr = self.logic_and()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.logic_and()
            expr = Binary(expr, operator, right)
        return expr

    def logic_and(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Binary(expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.LESS, TokenType.LESS_EQUAL,
                         TokenType.GREATER, TokenType.GREATER_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.MUL, TokenType.DIV):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        # handle not or negative operations
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.NUMBER):
            return Literal(self.previous().literal)
        if self.match(TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous().literal)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise Exception("Expected expression.")

    def match(self, *types):
        # check if token matched one of given types
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type):
        # check if current token matches expected type
        return not self._is_at_end() and self.peek().type == token_type

    def advance(self):
        # move to next token
        if not self._is_at_end():
            self.current += 1
        return self.previous()

    def _is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise Exception(message)
