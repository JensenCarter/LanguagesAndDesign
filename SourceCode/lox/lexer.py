from lox.tokens import Token, TokenType


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.current = 0

    def tokenize(self):
        # loop through code and generate tokens
        while not self._is_at_end():
            char = self._peek()

            if char.isspace():
                self._advance()
            elif char == "(":
                self._add_token(TokenType.LPAREN)
                self._advance()
            elif char == ")":
                self._add_token(TokenType.RPAREN)
                self._advance()
            elif char == "{":
                self._add_token(TokenType.LBRACE)
                self._advance()
            elif char == "}":
                self._add_token(TokenType.RBRACE)
                self._advance()
            elif char == '"':
                self._string()
            elif char in "+-–*/":
                # converts weird dash to normal one
                if char == "–":
                    char = "-"
                self._handle_operator(char)
            elif char == "!":
                self._advance()
                if self._peek() == "=":
                    self._advance()
                    self._add_token(TokenType.BANG_EQUAL)
                else:
                    self._add_token(TokenType.BANG)
            elif char == "=":
                self._advance()
                if self._peek() == "=":
                    self._advance()
                    self._add_token(TokenType.EQUAL_EQUAL)
                else:
                    self._add_token(TokenType.EQUAL)
            elif char in "<>":
                self._advance()
                if self._peek() == "=":
                    ch = char
                    self._advance()
                    if ch == "<":
                        self._add_token(TokenType.LESS_EQUAL)
                    else:
                        self._add_token(TokenType.GREATER_EQUAL)
                else:
                    if char == "<":
                        self._add_token(TokenType.LESS)
                    else:
                        self._add_token(TokenType.GREATER)
            elif char.isdigit() or char == ".":  # for decimals
                self._number()
            elif char.isalpha() or char == "_":  # for variables
                self._identifier()
            else:
                raise RuntimeError(f"Unexpected character: {char}")

        self._add_token(TokenType.EOF)  # end of file token
        return self.tokens

    def _string(self):
        # skip opening quotation mark
        self._advance()
        start = self.current
        while self._peek() != '"' and not self._is_at_end():
            self._advance()
        if self._is_at_end():
            raise RuntimeError("Unterminated string literal")
        # extract content
        value = self.source[start:self.current]
        # advance past closing quotation mark
        self._advance()
        self._add_token(TokenType.STRING, value, start)

    def _handle_operator(self, char):
        operator_map = {
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.MUL,
            "/": TokenType.DIV
        }
        self._add_token(operator_map[char])
        self._advance()

    def _number(self):
        start = self.current
        is_float = False

        while self._is_digit(self._peek()):
            self._advance()

        if self._peek() == ".":  # handle decimals for floats
            is_float = True
            self._advance()
            if not self._is_digit(self._peek()):
                raise RuntimeError(f"Invalid number: '{self.source[start:self.current]}'")
            while self._is_digit(self._peek()):
                self._advance()

        number_str = self.source[start:self.current]
        value = float(number_str) if is_float else int(number_str)
        self._add_token(TokenType.NUMBER, value, start)

    def _identifier(self):
        start = self.current
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()
        text = self.source[start:self.current]
        keywords = {
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "print": TokenType.PRINT,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "input": TokenType.INPUT,
            "and": TokenType.AND,
            "or": TokenType.OR,
        }
        token_type = keywords.get(text, TokenType.IDENTIFIER)
        self._add_token(token_type, text, start)

    def _advance(self):
        self.current += 1

    def _peek(self):
        return self.source[self.current] if self.current < len(self.source) else "\0"

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _is_digit(self, c):
        return c.isdigit()

    def _add_token(self, type: TokenType, literal=None, start: int = None):
        if type == TokenType.NUMBER:
            lexeme = self.source[start:self.current]
        elif type == TokenType.STRING:
            lexeme = self.source[start - 1:self.current]
        elif start is not None:
            lexeme = self.source[start:self.current]
        else:
            lexeme = self.source[self.current:self.current + 1] if self.current < len(self.source) else ""
        self.tokens.append(Token(type, lexeme, literal))

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
