from lox.tokens import Token, TokenType

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.current = 0

    def tokenize(self):
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
            elif char in "+-*/":
                if char == "-" and (self.current == 0 or self.source[self.current-1].isspace()):
                    # This simple heuristic distinguishes numeric negation from binary minus.
                    # (You might need a more robust solution in a full parser.)
                    self._add_token(TokenType.MINUS)
                    self._advance()
                else:
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
                    raise RuntimeError("Unexpected '='")
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
            elif char.isdigit() or char == ".":
                self._number()
            elif char.isalpha():
                self._identifier()
            else:
                raise RuntimeError(f"Unexpected character: {char}")

        self._add_token(TokenType.EOF)
        return self.tokens

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

        if self._peek() == ".":
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
        while self._peek().isalnum():
            self._advance()
        text = self.source[start:self.current]
        keywords = {
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "and": TokenType.AND,
            "or": TokenType.OR,
        }
        token_type = keywords.get(text)
        if token_type is None:
            raise RuntimeError(f"Unexpected identifier: {text}")
        self._add_token(token_type)

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
        else:
            lexeme = self.source[self.current:self.current+1] if self.current < len(self.source) else ""
        self.tokens.append(Token(type, lexeme, literal))
