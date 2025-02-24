from parser import Mparser
from scanner import Scanner
from sly.lex import LexError
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
import os
from Interpreter import Interpreter


if __name__ == "__main__":
    folder_path = 'examples'
    file_list = os.listdir(folder_path)
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents = file.read()
                print(f'Testing {filename}:')
            try:
                TreePrinter()
                parser = Mparser()
                typeChecker = TypeChecker()
                interpreter = Interpreter()
                cos = parser.parse(Scanner().tokenize(file_contents))

                if cos is not None:
                    cos.printTree(0)
                    typeChecker.visit(cos)
                    interpreter.visit(cos)
            except LexError as e:
                print(f"Lexer error: {e}")
