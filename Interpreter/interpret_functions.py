from analyze_functions import *
from run_functions import *
from variables import *
from my_types import *


def run_line(code: list, line: int, *args) -> int:
    """
    Execute a line of code.

    Args:
    - code (list): The code to be executed.

    Returns:
    - list: The result of the executed code.
    """
    if code[line] is None or code[line] == ['']:
        return line
    if code[line][0] == 'other':
        return other_function(code, line, args[0])
    if code[line][0] == 'step':
        return step_function(code, line, args[1])
    elif code[line][0] in keywords:
        func = eval(f'{code[line][0]}_function')
        return func(code, line)
    return assignment_function(code, line)


def analyze_code(code):
    """
    Analyze a code snippet and return the result.

    Args:
    - code: The code snippet to be analyzed.

    Returns:
    - None
    """
    if not code:
        return

    # Split code
    is_str = False
    res = ['']

    for i in code:
        if i == ' ' and not is_str:
            res.append('')
        elif i == "'" or i == '"':
            res[-1] += '"'
            is_str = not is_str
        elif i == '\n':
            break
        else:
            res[-1] += i

    if res == ['']:
        return

    if res[0] in keywords:
        func = eval(f'{res[0]}_analyze')
        res = func(res)
        return res
    return assignment_analyze(res)


def interpret_scope(code: list, line: int, *args) -> int:
    a = -1
    first_loop = True
    while line < len(code) and not ends_scope(code[line]):
        if isinstance(code[line], str):
            code[line] = analyze_code(code[line].strip())

        if code[line] is None:
            line += 1
            continue

        a = run_line(code, line, a, first_loop)

        if a == 1:
            line = interpret_scope(code, line + 1) + 1
        elif a == 2:
            interpret_scope(code, line + 1)
            first_loop = False
        elif a == 3:
            line = jump_scope(code, line + 1)
            first_loop = True
        elif a == 4:
            line = jump_scope(code, line + 1)
        else:
            line += 1

    if line >= len(code) or ends_scope(code[line]):
        return line + 1


def jump_scope(code, line) -> int:
    count = 1

    while count != 0 and line < len(code):
        if begins_scope(code[line]):
            count += 1
        elif ends_scope(code[line]):
            count -= 1
        line += 1

    if count == 0:
        return line
    raise SyntaxError('Scope never closed')


def begins_scope(line: (str, list)) -> bool:
    if isinstance(line, str) and line.rstrip().endswith('{'):
        return True
    if isinstance(line, list) and len(line) > 0 and line[-1] == '{':
        return True
    return False


def ends_scope(line: (str, list)) -> bool:
    if isinstance(line, str) and line.lstrip().startswith('}'):
        return True
    if isinstance(line, list) and len(line) > 0 and line[0] == '}':
        return True
    return False
