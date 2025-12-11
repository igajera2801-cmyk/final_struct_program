"""
Node Module
Functions for creating and manipulating AST (Abstract Syntax Tree) nodes.
A node is represented as a dictionary with 'tag', 'value', 'left', and 'right' keys.
"""


def create_node(tag, value, left=None, right=None):
    """
    Create a new AST node.
    
    Args:
        tag: The type of node (e.g., 'number', '+', '-', etc.)
        value: The value associated with the node
        left: Left child node (default None)
        right: Right child node (default None)
    
    Returns:
        A dictionary representing the AST node
    """
    return {
        "tag": tag,
        "value": value,
        "left": left,
        "right": right
    }


def get_node_tag(node):
    """
    Get the tag (type) of a node.
    
    Args:
        node: An AST node dictionary
    
    Returns:
        The tag string
    """
    return node["tag"]


def get_node_value(node):
    """
    Get the value of a node.
    
    Args:
        node: An AST node dictionary
    
    Returns:
        The value
    """
    return node["value"]


def get_node_left(node):
    """
    Get the left child of a node.
    
    Args:
        node: An AST node dictionary
    
    Returns:
        The left child node or None
    """
    return node["left"]


def get_node_right(node):
    """
    Get the right child of a node.
    
    Args:
        node: An AST node dictionary
    
    Returns:
        The right child node or None
    """
    return node["right"]


def is_leaf_node(node):
    """
    Check if a node is a leaf (has no children).
    
    Args:
        node: An AST node dictionary
    
    Returns:
        True if the node has no children, False otherwise
    """
    return get_node_left(node) is None and get_node_right(node) is None


def is_unary_node(node):
    """
    Check if a node is a unary operation (has only left child).
    
    Args:
        node: An AST node dictionary
    
    Returns:
        True if the node has only a left child, False otherwise
    """
    return get_node_left(node) is not None and get_node_right(node) is None


def is_binary_node(node):
    """
    Check if a node is a binary operation (has both children).
    
    Args:
        node: An AST node dictionary
    
    Returns:
        True if the node has both children, False otherwise
    """
    return get_node_left(node) is not None and get_node_right(node) is not None


def node_to_string(node, indent=0):
    """
    Convert an AST node to a readable string format (recursive).
    
    Args:
        node: An AST node dictionary
        indent: Current indentation level
    
    Returns:
        A formatted string representation of the AST
    """
    if node is None:
        return " " * indent + "None"
    
    prefix = " " * indent
    tag = get_node_tag(node)
    value = get_node_value(node)
    
    lines = [f"{prefix}Node(tag='{tag}', value='{value}')"]
    
    left = get_node_left(node)
    right = get_node_right(node)
    
    if left is not None or right is not None:
        lines.append(f"{prefix}  left:")
        lines.append(node_to_string(left, indent + 4))
        lines.append(f"{prefix}  right:")
        lines.append(node_to_string(right, indent + 4))
    
    return "\n".join(lines)


def print_ast(node):
    """
    Print the AST in a readable format.
    
    Args:
        node: The root AST node
    """
    print("Abstract Syntax Tree:")
    print("-" * 40)
    print(node_to_string(node))
    print("-" * 40)


def ast_to_expression(node):
    """
    Convert an AST back to an expression string.
    
    Args:
        node: An AST node dictionary
    
    Returns:
        String representation of the expression
    """
    if node is None:
        return ""
    
    tag = get_node_tag(node)
    value = get_node_value(node)
    left = get_node_left(node)
    right = get_node_right(node)
    
    if tag == "number":
        return value
    
    if tag == "negate":
        return f"(-{ast_to_expression(left)})"
    
    # Binary operators
    left_expr = ast_to_expression(left)
    right_expr = ast_to_expression(right)
    return f"({left_expr} {value} {right_expr})"
