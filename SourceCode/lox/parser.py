from lox.tokens import TokenType
from lox.expressions import Binary, Grouping, Literal, Unary, Variable, Assignment, Call
from lox.statements import Print, Expression, IfStmt, WhileStmt, BlockStmt


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
        if self.match(TokenType.PRINT):
            return self.print_statement()
        elif self.match(TokenType.IF):
            return self.if_statement()
        elif self.match(TokenType.WHILE):
            return self.while_statement()
        elif self.match(TokenType.LBRACE):
            return self.block_statement()
        else:
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
        if self.match(TokenType.NUMBER, TokenType.STRING):
            expr = Literal(self.previous().literal)
        elif self.match(TokenType.TRUE):
            expr = Literal(True)
        elif self.match(TokenType.FALSE):
            expr = Literal(False)
        elif self.match(TokenType.IDENTIFIER, TokenType.INPUT):
            expr = Variable(self.previous())
        elif self.match(TokenType.LPAREN):
            expr = Grouping(self.expression())
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
        else:
            raise RuntimeError("Expected expression.")
        return self.finish_call(expr)

    def finish_call(self, callee):
        while self.check(TokenType.LPAREN):
            paren = self.advance()
            arguments = []
            if not self.check(TokenType.RPAREN):
                arguments.append(self.expression())
            self.consume(TokenType.RPAREN, "Expect ')' after arguments.")
            callee = Call(callee, paren, arguments)
        return callee

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

    def block_statement(self):
        self.consume(TokenType.LBRACE, "Expect '{' to start block.")
        statements = []
        while not self.check(TokenType.RBRACE) and not self._is_at_end():
            statements.append(self.statement())
        self.consume(TokenType.RBRACE, "Expect '}' after block.")
        return BlockStmt(statements)

    def if_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after condition.")
        then_branch = self.block_statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.block_statement()
        return IfStmt(condition, then_branch, else_branch)

    def while_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after condition.")
        body = self.block_statement()
        return WhileStmt(condition, body)
