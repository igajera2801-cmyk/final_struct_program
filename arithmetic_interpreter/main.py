#!/usr/bin/env python3
"""
Main Entry Point
Arithmetic Expression Interpreter

Usage:
    python main.py                  # Interactive REPL mode
    python main.py "2 + 3 * 4"      # Evaluate single expression
    python main.py -v "2 + 3 * 4"   # Verbose mode (show tokens and AST)
"""

import sys
from src.interpreter import interpret, repl
from src.evaluator import format_result


def print_usage():
    """Print usage information."""
    print("Arithmetic Expression Interpreter")
    print()
    print("Usage:")
    print("  python main.py                  # Interactive REPL mode")
    print("  python main.py \"<expression>\"   # Evaluate single expression")
    print("  python main.py -v \"<expression>\" # Verbose mode")
    print()
    print("Examples:")
    print("  python main.py \"2 + 3 * 4\"")
    print("  python main.py \"(10 + 5) / 3\"")
    print("  python main.py -v \"2 ^ 3 ^ 2\"")
    print()
    print("Supported operators:")
    print("  +  Addition")
    print("  -  Subtraction (also unary negation)")
    print("  *  Multiplication")
    print("  /  Division")
    print("  %  Modulo")
    print("  ^  Power (right-associative)")
    print("  () Parentheses for grouping")


def main():
    """Main function."""
    args = sys.argv[1:]
    
    # No arguments - run REPL
    if not args:
        repl()
        return 0
    
    # Help flag
    if args[0] in ('-h', '--help'):
        print_usage()
        return 0
    
    # Verbose flag
    verbose = False
    if args[0] in ('-v', '--verbose'):
        verbose = True
        args = args[1:]
    
    # No expression provided after flags
    if not args:
        print("Error: No expression provided")
        print_usage()
        return 1
    
    # Join all remaining arguments as the expression
    expr_str = ' '.join(args)
    
    try:
        result = interpret(expr_str, verbose=verbose)
        if not verbose:
            print(f"{expr_str} = {format_result(result)}")
        return 0
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
