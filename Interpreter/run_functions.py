import interpret_functions
from validators import *
from variables import *
from my_types import *
from evaluate_expression import *


def decl_function(code: list, line: int) -> int:
    """
    For variable declaration.

    Parameters:
    - code (list): List representing the code.

    Returns:
    - int: Always returns 0.
    """
    scopes[-1][code[line][2]] = eval(f'{code[line][1].capitalize()}')(code[line][4])
    return 0


def read_function(code: list, line: int) -> int:
    """
    Input function.

    Parameters:
    - code (list): List representing the code.

    Returns:
    - int: Always returns 0.
    """
    var = get_variable(code[line][1])
    T = eval(var.__class__.__name__)
    value = input('Input value: ')

    if var.__class__.__name__ == 'String':
        value = '"' + value + '"'

    if not eval(f'{var.__class__.__name__.lower()}_validator')(value):
        raise ValueError(f'Invalid literal {value} for type {code[line][1]}')

    value = T(value)
    scope_index = get_variable_scope(code[line][1])
    scopes[scope_index][code[line][1]] = value
    return 0


def display_function(code: list, line: int) -> int:
    """
    Print function.

    Parameters:
    - code (list): List representing the code.

    Returns:
    - int: Always returns 0.
    """
    with open('output.txt', 'a') as out_stream:
        if len(code[line]) > 2:
            expression = infix_to_postfix(' '.join(code[line][1:]))
            out_stream.write(str(evaluate_postfix(expression)) + '\n')

        elif is_literal(code[line][1]):
            out_stream.write(code[line][1] + '\n')

        else:
            out_stream.write(str(get_variable(code[line][1])) + '\n')

    return 0


def assignment_function(code: list, line: int) -> int:
    """
    For expressions.

    Parameters:
    - code (list): List representing the code.

    Returns:
    - int: Always returns 0.
    """
    # print(len(code))
    return assign_helper(code[line])


def check_function(code: list, line: int) -> int:
    """
    If statement.

    Parameters:
    - code (list): List representing the code.

    Returns:
    - int: Returns 1 if the condition is true, 2 otherwise.
    """
    return check_helper(code[line])



def other_function(code: list, line: int, a: int) -> int:  # TODO
    """Else statement"""
    if a == 4:
        return 1
    else:
        return 3



def step_function(code: list, line: int, first_loop: bool) -> int:
    """
    For statement.

    Parameters:
    - code (list): List representing the code.

    Returns:
    - int: Returns 3 if the condition is true, 2 otherwise.
    """
    index1 = code[line].index(':')
    index2 = code[line].index(':', index1 + 1)

    if first_loop:
        assign_helper(code[line][2:index1])
    else:
        assign_helper(code[line][index2 + 1:-2])

    check = check_helper(['check'] + code[line][index1 + 1: index2])

    if check == 1:
        return 2
    else:
        return 3


def till_function(code: list, line: int) -> int:
    """
    While statement.

    Parameters:
    - code (list): List representing the code.

    Returns:
    - int: Returns 4 if the condition is true, 2 otherwise.
    """
    check = check_helper(['check'] + code[line][2:-2])

    if check == 1:
        return 2
    else:
        return 3


def assign_helper(code: list):
    postfix = infix_to_postfix(' '.join(code[2:]))
    T = eval(get_variable(code[0]).__class__.__name__)

    scope_index = get_variable_scope(code[0])
    value = T(evaluate_postfix(postfix))
    op = code[1]

    if op != '=':
        value = calculate(scopes[scope_index][code[0]], value, op[:-1])

    scopes[scope_index][code[0]] = value

    return 0


def check_helper(code: list):
    condition = False
    for i in range(len(code)):
        if is_condition_operator(code[i]):
            expression_validator(' '.join(code[1:i]))
            expression_validator(' '.join(code[i + 1:-1]))

            postfix = infix_to_postfix(' '.join(code[1:i]))
            left_value = evaluate_postfix(postfix)

            postfix = infix_to_postfix(' '.join(code[i + 1:]))
            right_value = evaluate_postfix(postfix)

            condition = f'{left_value} {code[i]} {right_value}'
            condition = eval(condition)
            break

    if condition:
        return 1
    else:
        return 4