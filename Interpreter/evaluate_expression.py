from stack import Stack
from validators import *
from my_types import *
import re

def is_operator(c: str) -> bool:
    """
    Check if the character is an operator.

    Args:
    - c (str): The character to be checked.

    Returns:
    - bool: True if the character is an operator, False otherwise.
    """

    return c in operators


def is_operand(c: str) -> bool:
    """
    Check if the character is an operand.

    Args:
    - c (str): The character to be checked.

    Returns:
    - bool: True if the character is an operand, False otherwise.
    """

    return not is_operator(c)


def infix_to_postfix(infix: str) -> str:
    """
    Converts an infix expression to postfix.

    Args:
    - infix (str): The infix expression to be converted.

    Returns:
    - str: The resulting postfix expression.
    """

    postfix = ""
    stack = Stack()

    def priority(c):
        """
        Assign priority to operators.

        Args:
        - c (str): The operator.

        Returns:
        - int: The priority of the operator.
        """

        if c in ['+', '-']:
            return 0
        elif c in ['*', '/']:
            return 1
        elif c == '^':
            return 2
        return -1

    for i in infix:
        if i == '(':
            stack.push('(')

        elif i == ')':
            while not stack.is_empty() and stack.top() != '(':
                postfix += ' ' + stack.top()
                stack.pop()
            if not stack.is_empty():
                stack.pop()
            else:
                return ""

        elif is_operand(i):
            postfix += i

        elif is_operator(i):
            while not stack.is_empty() and is_operator(stack.top()) and priority(stack.top()) >= priority(i):
                postfix += ' ' + stack.top()
                stack.pop()
            stack.push(i)

        else:
            return ""

    while not stack.is_empty():
        postfix += ' ' + stack.top()
        stack.pop()

    return postfix.strip()


def calculate(operand1: str, operand2: str, op: str) -> any:
    """
    Calculate the result of the given operation between two operands.

    Args:
    - operand1 (str): The first operand.
    - operand2 (str): The second operand.
    - op (str): The operator.

    Returns:
    - any: The result of the calculation.
    """

    expression = f"{operand1} {op} {operand2}"
    T = eval(typeof(operand1))
    return T(eval(expression))


def evaluate_postfix(postfix: str) -> any:
    """
    Evaluate a postfix expression and return the result.

    Args:
    - postfix (str): The postfix expression to be evaluated.

    Returns:
    - any: The result of the evaluation.
    """

    postfix = re.findall(r'"[^"]*"|\S+', postfix)
    stack = Stack()

    for i in range(len(postfix)):
        if is_operand(postfix[i]):
            if is_literal(postfix[i]):
                tmp = eval(typeof(postfix[i]))
                stack.push(tmp(postfix[i]))
            var = get_variable(postfix[i])
            if var:
                stack.push(var)
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.push(calculate(operand1, operand2, postfix[i]))

    return stack.top()
