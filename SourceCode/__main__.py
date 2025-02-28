from lox.lexer import Lexer
from lox.parser import Parser
from lox.interpreter import Interpreter


def main(file):
    with open(file, "r") as f:
        lines = f.readlines()

    # remove comments and empty lines, then join lines
    processed_lines = []
    for line in lines:
        line = line.split("#", 1)[0].strip()
        if line:
            processed_lines.append(line)
    source = "\n".join(processed_lines)

    # initialise the interpreter.
    interpreter = Interpreter()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
    except Exception as e:
        print(f"Lexer Error: {e}")
        return

    try:
        parser = Parser(tokens)
        statements = parser.parse()
    except Exception as e:
        print(f"Parser Error: {e}")
        return

    try:
        interpreter.interpret(statements)
    except Exception as e:
        print(f"Runtime Error: {e}")


if __name__ == "__main__":
    file = "test.txt"
    main(file)
