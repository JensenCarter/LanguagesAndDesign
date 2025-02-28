from lox.lexer import Lexer
from lox.parser import Parser
from lox.interpreter import Interpreter

# file
file = "test.txt"

def main(file):
    lines = open(file, "r").readlines()

    # initialise interpreter
    interpreter = Interpreter()

    for line_number, line in enumerate(lines, start=1):
        # remove whitespace and comments
        line = line.strip().split("#", 1)[0].strip()
        # skip empty lines
        if not line:
            continue

        # tokenize current line
        try:
            lexer = Lexer(line)
            tokens = lexer.tokenize()
        except Exception as e:
            print(f"Line {line_number} Lexer Error: {e}")
            continue

        # parse tokens into statements
        try:
            parser = Parser(tokens)
            statements = parser.parse()
            interpreter.interpret(statements)
        except Exception as e:
            print(f"Line {line_number} Error: {e}")

if __name__ == "__main__":
    main(file)
