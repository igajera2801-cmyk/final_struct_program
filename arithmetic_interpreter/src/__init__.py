"""
Arithmetic Interpreter Package
A simple interpreter for arithmetic expressions.
"""

from src.interpreter import interpret, interpret_with_details, validate_expression, repl
from src.tokenizer import tokenize
from src.parser import parse
from src.evaluator import evaluate

__all__ = [
    'interpret',
    'interpret_with_details',
    'validate_expression',
    'repl',
    'tokenize',
    'parse',
    'evaluate'
]

__version__ = '1.0.0'
