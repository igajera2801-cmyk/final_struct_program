"""
Evaluator Module
Functions for evaluating the Abstract Syntax Tree (AST).
"""

from src.node import (
    get_node_tag,
    get_node_value,
    get_node_left,
    get_node_right
)


def evaluate(ast):
    """
    Evaluate an AST node and return the numeric result.
    
    Args:
        ast: An AST node dictionary
    
    Returns:
        The numeric result of evaluation
    
    Raises:
        ValueError: If the AST contains invalid nodes or operations
    """
    if ast is None:
        raise ValueError("Cannot evaluate None node")
    
    tag = get_node_tag(ast)
    value = get_node_value(ast)
    left = get_node_left(ast)
    right = get_node_right(ast)
    
    # Number literal
    if tag == 'number':
        return convert_to_number(value)
    
    # Unary negation
    if tag == 'negate':
        operand = evaluate(left)
        return negate(operand)
    
    # Binary operations
    if tag == '+':
        return add(evaluate(left), evaluate(right))
    
    if tag == '-':
        return subtract(evaluate(left), evaluate(right))
    
    if tag == '*':
        return multiply(evaluate(left), evaluate(right))
    
    if tag == '/':
        return divide(evaluate(left), evaluate(right))
    
    if tag == '%':
        return modulo(evaluate(left), evaluate(right))
    
    if tag == '^':
        return power(evaluate(left), evaluate(right))
    
    raise ValueError(f"Unknown operator in AST: '{tag}'")


def convert_to_number(value):
    """
    Convert a string value to a number.
    
    Args:
        value: String representation of a number
    
    Returns:
        Integer or float depending on the value
    """
    num = float(value)
    # Return int if it's a whole number
    if num == int(num):
        return int(num)
    return num


def negate(operand):
    """
    Negate a number.
    
    Args:
        operand: The number to negate
    
    Returns:
        The negated number
    """
    return -operand


def add(left, right):
    """
    Add two numbers.
    
    Args:
        left: Left operand
        right: Right operand
    
    Returns:
        Sum of left and right
    """
    return left + right


def subtract(left, right):
    """
    Subtract two numbers.
    
    Args:
        left: Left operand
        right: Right operand
    
    Returns:
        Difference of left and right
    """
    return left - right


def multiply(left, right):
    """
    Multiply two numbers.
    
    Args:
        left: Left operand
        right: Right operand
    
    Returns:
        Product of left and right
    """
    return left * right


def divide(left, right):
    """
    Divide two numbers.
    
    Args:
        left: Left operand (dividend)
        right: Right operand (divisor)
    
    Returns:
        Quotient of left divided by right
    
    Raises:
        ValueError: If attempting to divide by zero
    """
    if right == 0:
        raise ValueError("Division by zero")
    return left / right


def modulo(left, right):
    """
    Calculate modulo of two numbers.
    
    Args:
        left: Left operand
        right: Right operand
    
    Returns:
        Remainder of left divided by right
    
    Raises:
        ValueError: If attempting modulo by zero
    """
    if right == 0:
        raise ValueError("Modulo by zero")
    return left % right


def power(base, exponent):
    """
    Calculate power of a number.
    
    Args:
        base: The base number
        exponent: The exponent
    
    Returns:
        base raised to the power of exponent
    """
    return base ** exponent


def format_result(result):
    """
    Format the result for display.
    Shows as integer if whole number, otherwise as float.
    
    Args:
        result: The numeric result
    
    Returns:
        Formatted string representation
    """
    if isinstance(result, float) and result == int(result):
        return str(int(result))
    return str(result)
