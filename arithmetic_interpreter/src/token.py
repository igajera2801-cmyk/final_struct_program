"""
Token Module
Functions for creating and manipulating tokens.
A token is represented as a dictionary with 'tag' and 'value' keys.
"""


def create_token(tag, value):
    """
    Create a new token.
    
    Args:
        tag: The type of token (e.g., 'number', '+', '-', etc.)
        value: The actual string value from the input
    
    Returns:
        A dictionary representing the token
    """
    return {"tag": tag, "value": value}


def get_token_tag(token):
    """
    Get the tag (type) of a token.
    
    Args:
        token: A token dictionary
    
    Returns:
        The tag string
    """
    return token["tag"]


def get_token_value(token):
    """
    Get the value of a token.
    
    Args:
        token: A token dictionary
    
    Returns:
        The value string
    """
    return token["value"]


def is_token_type(token, tag):
    """
    Check if a token is of a specific type.
    
    Args:
        token: A token dictionary
        tag: The tag to check against
    
    Returns:
        True if the token's tag matches, False otherwise
    """
    return get_token_tag(token) == tag


def token_to_string(token):
    """
    Convert a token to a readable string format.
    
    Args:
        token: A token dictionary
    
    Returns:
        A formatted string representation
    """
    return f"Token(tag='{get_token_tag(token)}', value='{get_token_value(token)}')"
