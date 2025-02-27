from lox.lexer import Lexer
from lox.parser import Parser
from lox.interpreter import Interpreter

def main():
    try:
        with open("test.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: 'test.txt' file not found.")
        return

    interpreter = Interpreter()

    for line_number, line in enumerate(lines, start=1):
        # removes whitespace, comments and, skips empty lines
        line = line.strip().split("#", 1)[0].strip()
        if not line:
            continue

        try:
            lexer = Lexer(line)
            tokens = lexer.tokenize()
        except Exception as e:
            print(f"Line {line_number} Lexer Error: {e}")
            continue

        parser = Parser(tokens)
        expr = parser.parse()

        if expr:
            try:
                result = interpreter.interpret(expr)
                print(f"{line} = {result}\n")
            except Exception as e:
                print(f"Line {line_number} Interpreter Error: {e}\n")

if __name__ == "__main__":
    main()
