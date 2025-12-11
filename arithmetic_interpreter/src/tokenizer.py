"""
Tokenizer Module
Functions for lexical analysis - converting input string to tokens.
"""

import re
from src.token import create_token, get_token_tag, token_to_string


def get_patterns():
    """
    Get the list of token patterns.
    Each pattern is a tuple of (regex_pattern, token_tag).
    Order matters - patterns are matched in order.
    
    Returns:
        List of (pattern, tag) tuples
    """
    return [
        (r'\d+\.?\d*', 'number'),    # Integer and decimal numbers
        (r'\+', '+'),                 # Addition
        (r'\-', '-'),                 # Subtraction
        (r'\*', '*'),                 # Multiplication
        (r'\/', '/'),                 # Division
        (r'\%', '%'),                 # Modulo
        (r'\^', '^'),                 # Power
        (r'\(', '('),                 # Left parenthesis
        (r'\)', ')'),                 # Right parenthesis
        (r'\s+', 'whitespace'),       # Whitespace (will be filtered)
    ]


def match_single_token(text, position, patterns):
    """
    Try to match a single token at the given position in text.
    
    Args:
        text: The input string
        position: Current position in the string
        patterns: List of (pattern, tag) tuples
    
    Returns:
        Tuple of (token, new_position) if match found, None otherwise
    """
    for pattern, tag in patterns:
        regex = re.compile(pattern)
        match = regex.match(text, position)
        if match:
            value = match.group()
            token = create_token(tag, value)
            new_position = match.end()
            return (token, new_position)
    return None


def tokenize(expr_str):
    """
    Convert an expression string into a list of tokens.
    Whitespace tokens are automatically filtered out.
    
    Args:
        expr_str: The input expression string
    
    Returns:
        List of token dictionaries
    
    Raises:
        ValueError: If an invalid character is encountered
    """
    if not isinstance(expr_str, str):
        raise TypeError("Input must be a string")
    
    if not expr_str.strip():
        raise ValueError("Input cannot be empty")
    
    tokens = []
    patterns = get_patterns()
    position = 0
    
    while position < len(expr_str):
        result = match_single_token(expr_str, position, patterns)
        
        if result is None:
            raise ValueError(
                f"Invalid character at position {position}: '{expr_str[position]}'"
            )
        
        token, new_position = result
        
        # Filter out whitespace tokens
        if get_token_tag(token) != 'whitespace':
            tokens.append(token)
        
        position = new_position
    
    return tokens


def print_tokens(tokens):
    """
    Print all tokens in a readable format.
    
    Args:
        tokens: List of token dictionaries
    """
    print("Tokens:")
    print("-" * 40)
    for i, token in enumerate(tokens):
        print(f"  [{i}] {token_to_string(token)}")
    print("-" * 40)


def tokens_to_string(tokens):
    """
    Convert token list to a string representation.
    
    Args:
        tokens: List of token dictionaries
    
    Returns:
        String representation of all tokens
    """
    lines = [token_to_string(token) for token in tokens]
    return "\n".join(lines)
