"""
Parser Module
Functions for parsing tokens into an Abstract Syntax Tree (AST).
Implements recursive descent parsing with proper operator precedence.

Grammar:
    expression     -> term (('+' | '-') term)*
    term           -> power (('*' | '/' | '%') power)*
    power          -> unary ('^' unary)*
    unary          -> '-' unary | primary
    primary        -> NUMBER | '(' expression ')'
"""

from src.token import get_token_tag, get_token_value
from src.node import create_node


def peek_token(tokens):
    """
    Look at the next token without consuming it.
    
    Args:
        tokens: List of remaining tokens
    
    Returns:
        The next token or None if no tokens remain
    """
    if tokens:
        return tokens[0]
    return None


def consume_token(tokens):
    """
    Consume and return the next token.
    
    Args:
        tokens: List of remaining tokens
    
    Returns:
        Tuple of (consumed_token, remaining_tokens)
    
    Raises:
        ValueError: If no tokens remain
    """
    if not tokens:
        raise ValueError("Unexpected end of expression")
    return (tokens[0], tokens[1:])


def expect_token(tokens, expected_tag):
    """
    Consume a token and verify it has the expected tag.
    
    Args:
        tokens: List of remaining tokens
        expected_tag: The expected token tag
    
    Returns:
        Tuple of (consumed_token, remaining_tokens)
    
    Raises:
        ValueError: If the token doesn't match expected tag
    """
    token, remaining = consume_token(tokens)
    if get_token_tag(token) != expected_tag:
        actual = get_token_tag(token)
        raise ValueError(f"Expected '{expected_tag}' but got '{actual}'")
    return (token, remaining)


def parse_primary(tokens):
    """
    Parse a primary expression: number or parenthesized expression.
    
    Grammar: primary -> NUMBER | '(' expression ')'
    
    Args:
        tokens: List of remaining tokens
    
    Returns:
        Tuple of (ast_node, remaining_tokens)
    """
    token = peek_token(tokens)
    
    if token is None:
        raise ValueError("Unexpected end of expression, expected number or '('")
    
    tag = get_token_tag(token)
    value = get_token_value(token)
    
    # Number literal
    if tag == 'number':
        _, remaining = consume_token(tokens)
        node = create_node('number', value)
        return (node, remaining)
    
    # Parenthesized expression
    if tag == '(':
        _, remaining = consume_token(tokens)  # consume '('
        node, remaining = parse_expression(remaining)
        _, remaining = expect_token(remaining, ')')  # expect and consume ')'
        return (node, remaining)
    
    raise ValueError(f"Unexpected token: '{value}'")


def parse_unary(tokens):
    """
    Parse a unary expression: negation or primary.
    
    Grammar: unary -> '-' unary | primary
    
    Args:
        tokens: List of remaining tokens
    
    Returns:
        Tuple of (ast_node, remaining_tokens)
    """
    token = peek_token(tokens)
    
    if token and get_token_tag(token) == '-':
        _, remaining = consume_token(tokens)  # consume '-'
        operand, remaining = parse_unary(remaining)  # recursive for --5
        node = create_node('negate', '-', operand)
        return (node, remaining)
    
    return parse_primary(tokens)


def parse_power(tokens):
    """
    Parse a power expression (right-associative).
    
    Grammar: power -> unary ('^' unary)*
    Note: Power is right-associative, so 2^3^2 = 2^(3^2) = 512
    
    Args:
        tokens: List of remaining tokens
    
    Returns:
        Tuple of (ast_node, remaining_tokens)
    """
    node, remaining = parse_unary(tokens)
    
    token = peek_token(remaining)
    if token and get_token_tag(token) == '^':
        _, remaining = consume_token(remaining)  # consume '^'
        right_node, remaining = parse_power(remaining)  # right-associative
        node = create_node('^', '^', node, right_node)
    
    return (node, remaining)


def parse_term(tokens):
    """
    Parse a term: handles *, /, % (higher precedence than +, -).
    
    Grammar: term -> power (('*' | '/' | '%') power)*
    
    Args:
        tokens: List of remaining tokens
    
    Returns:
        Tuple of (ast_node, remaining_tokens)
    """
    node, remaining = parse_power(tokens)
    
    while True:
        token = peek_token(remaining)
        if token is None:
            break
        
        tag = get_token_tag(token)
        if tag not in ('*', '/', '%'):
            break
        
        _, remaining = consume_token(remaining)  # consume operator
        right_node, remaining = parse_power(remaining)
        node = create_node(tag, tag, node, right_node)
    
    return (node, remaining)


def parse_expression(tokens):
    """
    Parse an expression: handles +, - (lowest precedence).
    
    Grammar: expression -> term (('+' | '-') term)*
    
    Args:
        tokens: List of remaining tokens
    
    Returns:
        Tuple of (ast_node, remaining_tokens)
    """
    node, remaining = parse_term(tokens)
    
    while True:
        token = peek_token(remaining)
        if token is None:
            break
        
        tag = get_token_tag(token)
        if tag not in ('+', '-'):
            break
        
        _, remaining = consume_token(remaining)  # consume operator
        right_node, remaining = parse_term(remaining)
        node = create_node(tag, tag, node, right_node)
    
    return (node, remaining)


def parse(tokens):
    """
    Main parse function. Converts tokens into an AST.
    
    Args:
        tokens: List of token dictionaries
    
    Returns:
        The root AST node
    
    Raises:
        ValueError: If parsing fails or tokens remain after parsing
    """
    if not tokens:
        raise ValueError("Cannot parse empty token list")
    
    ast, remaining = parse_expression(tokens)
    
    if remaining:
        token = peek_token(remaining)
        value = get_token_value(token)
        raise ValueError(f"Unexpected token after expression: '{value}'")
    
    return ast
