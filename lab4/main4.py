import sys
import os
from scanner import Scanner
from parser import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker

if __name__ == '__main__':
    directory = 'examples'
    for filename in os.listdir(directory):
        if filename.endswith(".m"):
            path = os.path.join(directory, filename)
            try:
                file = open(path, "r")
            except IOError:
                print("Cannot open {0} file".format(path))
                continue
            print(filename)
            text = file.read()
            file.close()

            parser = Mparser()
            lexer = Scanner()
            ast = parser.parse(lexer.tokenize(text))

            if ast is not None:
                ast.printTree()
                typeChecker = TypeChecker()
                typeChecker.visit(ast)
