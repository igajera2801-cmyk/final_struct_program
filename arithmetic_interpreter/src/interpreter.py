"""
Interpreter Module
Main interpreter that combines tokenizer, parser, and evaluator.
"""

from src.tokenizer import tokenize, print_tokens
from src.parser import parse
from src.evaluator import evaluate, format_result
from src.node import print_ast, ast_to_expression


def interpret(expr_str, verbose=False):
    """
    Interpret an arithmetic expression string.
    
    Args:
        expr_str: The expression to interpret
        verbose: If True, print intermediate steps
    
    Returns:
        The numeric result of the expression
    
    Raises:
        ValueError: If the expression is invalid
        TypeError: If the input is not a string
    """
    # Tokenize
    tokens = tokenize(expr_str)
    
    if verbose:
        print(f"\nInput: {expr_str}")
        print_tokens(tokens)
    
    # Parse
    ast = parse(tokens)
    
    if verbose:
        print_ast(ast)
    
    # Evaluate
    result = evaluate(ast)
    
    if verbose:
        print(f"Result: {expr_str} = {format_result(result)}")
    
    return result


def interpret_with_details(expr_str):
    """
    Interpret an expression and return detailed information.
    
    Args:
        expr_str: The expression to interpret
    
    Returns:
        Dictionary containing tokens, ast, result, and formatted_result
    """
    tokens = tokenize(expr_str)
    ast = parse(tokens)
    result = evaluate(ast)
    
    return {
        "input": expr_str,
        "tokens": tokens,
        "ast": ast,
        "result": result,
        "formatted_result": format_result(result),
        "reconstructed": ast_to_expression(ast)
    }


def validate_expression(expr_str):
    """
    Validate an expression without evaluating it.
    
    Args:
        expr_str: The expression to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        tokens = tokenize(expr_str)
        parse(tokens)
        return (True, None)
    except (ValueError, TypeError) as e:
        return (False, str(e))


def repl():
    """
    Run a Read-Eval-Print Loop for interactive use.
    Type 'quit' or 'exit' to stop.
    """
    print("=" * 50)
    print("  Arithmetic Expression Interpreter")
    print("=" * 50)
    print("Enter expressions to evaluate.")
    print("Commands: 'quit' or 'exit' to stop")
    print("          'verbose' to toggle verbose mode")
    print("=" * 50)
    print()
    
    verbose = False
    
    while True:
        try:
            expr_str = input("> ").strip()
            
            if not expr_str:
                continue
            
            if expr_str.lower() in ('quit', 'exit'):
                print("Goodbye!")
                break
            
            if expr_str.lower() == 'verbose':
                verbose = not verbose
                status = "ON" if verbose else "OFF"
                print(f"Verbose mode: {status}")
                continue
            
            result = interpret(expr_str, verbose=verbose)
            print(f"= {format_result(result)}")
            
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
