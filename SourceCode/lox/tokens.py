from enum import Enum, auto


class TokenType(Enum):
    # single characters
    LPAREN = auto()
    RPAREN = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    BANG = auto()

    # one or two characters
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    # booleans and logical operators
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()

    NUMBER = auto()
    EOF = auto()


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: float):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal

    def __repr__(self):
        return f"Token({self.type}, '{self.lexeme}', {self.literal})"