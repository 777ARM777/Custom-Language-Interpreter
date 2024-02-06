from interpret_functions import *

if __name__ == '__main__':
    # Reading file
    with open('code.my') as code:
        code = code.readlines()

    # Syntax analyze and run code
    line = 0

    while line < len(code):
        line = interpret_scope(code, line)

    # Output the result to 'output.txt'
    with open('output.txt', 'r') as out:
        print(out.read())

    # Clear the content of 'output.txt'
    with open('output.txt', 'w') as out:
        out.write('')
