import re
from variables import *

def is_literal(value: str) -> bool:
    """
    Check if a given value is a literal.

    Args:
    - value (str): The value to be checked.

    Returns:
    - bool: True if the value is a literal, False otherwise.
    """
    if value == 'true' or value == 'false':
        return True

    if value[0].isdigit():
        return True

    if value[0] == '"':
        return True

def is_condition_operator(value: str) -> bool:
    """
    Check if a given value is a condition operator.

    Args:
    - value (str): The value to be checked.

    Returns:
    - bool: True if the value is a condition operator, False otherwise.
    """
    return value in condition_operators

def typeof(value: any):
    """
    Get the type of a variable or literal value.

    Args:
    - value (any): The variable or literal value.

    Returns:
    - str: The type of the variable or literal value.

    Raises:
    - ValueError: If the value is not a literal or a valid variable.
    """
    var = get_variable(value)
    if var:
        return var.__class__.__name__
    if isinstance(value, str):
        if integer_validator(value):
            return 'Integer'
        if double_validator(value):
            return 'Double'
        if string_validator(value):
            return 'String'
        if boolean_validator(value):
            return 'Boolean'

    if value.__class__.__name__.lower() in type_names:
        return value.__class__.__name__

    raise ValueError(f'{value} is not a literal or valid variable.')

def get_variable(var: str):
    """
    Get the variable with the given name from the current or outer scopes.

    Args:
    - var (str): The name of the variable.

    Returns:
    - any: The variable value, or None if not found.
    """
    for i in range(len(scopes) - 1, -1, -1):
        if var in scopes[i]:
            return scopes[i][var]

    return None

def get_variable_scope(var: str):
    """
    Get the scope index of the variable with the given name.

    Args:
    - var (str): The name of the variable.

    Returns:
    - int: The scope index, or None if not found.
    """
    for i in range(len(scopes) - 1, -1, -1):
        if var in scopes[i]:
            return i

    return None


def identifier_name_validator(identifier: str) -> bool:
    """
    Validate if a given string is a valid identifier name.

    Args:
    - identifier (str): The identifier name.

    Returns:
    - bool: True if the identifier name is valid, False otherwise.
    """
    # Define the regex pattern for a valid Python identifier
    if identifier in keywords:
        return False

    pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    match = pattern.match(identifier)
    return bool(match)


def literal_validator(value: str) -> bool:
    """
    Validate if a given string is a valid literal.

    Args:
    - value (str): The literal value.

    Returns:
    - bool: True if the literal value is valid, False otherwise.
    """
    if integer_validator(value) or double_validator(value) or boolean_validator(value) or string_validator(value):
        return True
    return False

def integer_validator(input_string):
    """
    Validate if a given string is a valid integer.

    Args:
    - input_string (str): The input string.

    Returns:
    - bool: True if the string is a valid integer, False otherwise.
    """
    # Define the regex pattern for integer validation
    pattern = re.compile(r'^[+-]?\d+$')

    # Match the pattern against the input string
    match = pattern.match(input_string)

    # Check if the string is a valid integer
    if match:
        return True
    else:
        return False


def double_validator(input_string):
    """
    Validate if a given string is a valid double.

    Args:
    - input_string (str): The input string.

    Returns:
    - bool: True if the string is a valid double, False otherwise.
    """
    # Define the regex pattern for double validation
    pattern = re.compile(r'^[+-]?\d+(\.\d+)?$')

    # Match the pattern against the input string
    match = pattern.match(input_string)

    # Check if the string is a valid double
    if match:
        return True
    else:
        return False


def boolean_validator(input_string):
    """
    Validate if a given string is a valid boolean.

    Args:
    - input_string (str): The input string.

    Returns:
    - bool: True if the string is a valid boolean, False otherwise.
    """
    if input_string in ('true', 'false'):
        return True
    return False


def string_validator(input_string):
    """
    Validate if a given string is a valid string.

    Args:
    - input_string (str): The input string.

    Returns:
    - bool: True if the string is valid, False otherwise.
    """
    # Define the regex pattern for a string enclosed in single quotes
    pattern = re.compile(r'^[\'\"](.*?)[\'\"]$')

    # Match the pattern against the input string
    match = pattern.match(input_string)

    # Check if the string is valid
    if match:
        return True
    else:
        return False


def expression_validator(expression) -> bool:
    """
    Validate if a given expression is syntactically correct.

    Args:
    - expression: The expression to be validated.

    Returns:
    - bool: True if the expression is valid, False otherwise.
    """
    # TODO: Implement expression validation
    pass

def condition_validator(code: str) -> bool:
    """
    Validate if a given condition expression is syntactically correct.

    Args:
    - code (str): The condition expression to be validated.

    Returns:
    - bool: True if the expression is valid, False otherwise.
    """
    # TODO: Implement condition validation
    pass
