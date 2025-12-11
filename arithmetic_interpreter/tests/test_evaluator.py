"""
Test Cases for Evaluator Module
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tokenizer import tokenize
from src.parser import parse
from src.evaluator import (
    evaluate, format_result, convert_to_number,
    add, subtract, multiply, divide, modulo, power, negate
)


class TestEvaluatorBasicOperations(unittest.TestCase):
    """Basic arithmetic operation tests."""
    
    def test_single_number(self):
        """Test evaluating a single number."""
        tokens = tokenize("42")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 42)
    
    def test_addition(self):
        """Test simple addition."""
        tokens = tokenize("2 + 3")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 5)
    
    def test_subtraction(self):
        """Test simple subtraction."""
        tokens = tokenize("10 - 4")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 6)
    
    def test_multiplication(self):
        """Test simple multiplication."""
        tokens = tokenize("6 * 7")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 42)
    
    def test_division(self):
        """Test simple division."""
        tokens = tokenize("20 / 4")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 5)
    
    def test_modulo(self):
        """Test modulo operation."""
        tokens = tokenize("17 % 5")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 2)
    
    def test_power(self):
        """Test power operation."""
        tokens = tokenize("2 ^ 3")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 8)


class TestEvaluatorPrecedence(unittest.TestCase):
    """Test operator precedence in evaluation."""
    
    def test_add_then_multiply(self):
        """Test that 2 + 3 * 4 = 14, not 20."""
        tokens = tokenize("2 + 3 * 4")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 14)
    
    def test_subtract_then_divide(self):
        """Test that 10 - 6 / 2 = 7, not 2."""
        tokens = tokenize("10 - 6 / 2")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 7)
    
    def test_power_precedence(self):
        """Test that power has correct precedence."""
        tokens = tokenize("2 * 3 ^ 2")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 18)  # 2 * (3^2) = 2 * 9 = 18
    
    def test_power_right_associative(self):
        """Test that 2 ^ 3 ^ 2 = 512, not 64."""
        tokens = tokenize("2 ^ 3 ^ 2")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 512)  # 2 ^ (3^2) = 2^9 = 512


class TestEvaluatorParentheses(unittest.TestCase):
    """Test parentheses in evaluation."""
    
    def test_parentheses_override(self):
        """Test that (2 + 3) * 4 = 20."""
        tokens = tokenize("(2 + 3) * 4")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 20)
    
    def test_nested_parentheses(self):
        """Test nested parentheses."""
        tokens = tokenize("((2 + 3) * 2)")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 10)
    
    def test_complex_parentheses(self):
        """Test complex parenthesized expression."""
        tokens = tokenize("(1 + 2) * (3 + 4)")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 21)


class TestEvaluatorNegation(unittest.TestCase):
    """Test unary negation in evaluation."""
    
    def test_simple_negation(self):
        """Test simple negation."""
        tokens = tokenize("-5")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, -5)
    
    def test_double_negation(self):
        """Test double negation."""
        tokens = tokenize("--5")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 5)
    
    def test_negation_in_expression(self):
        """Test negation in expression."""
        tokens = tokenize("-5 + 10")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 5)
    
    def test_negation_with_parentheses(self):
        """Test negation with parentheses."""
        tokens = tokenize("-(3 + 2)")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, -5)


class TestEvaluatorDecimalNumbers(unittest.TestCase):
    """Test decimal number handling."""
    
    def test_decimal_addition(self):
        """Test adding decimal numbers."""
        tokens = tokenize("1.5 + 2.5")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 4.0)
    
    def test_decimal_multiplication(self):
        """Test multiplying decimal numbers."""
        tokens = tokenize("2.5 * 4")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 10.0)
    
    def test_decimal_division(self):
        """Test dividing with decimals."""
        tokens = tokenize("7 / 2")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 3.5)


class TestEvaluatorErrors(unittest.TestCase):
    """Test error handling in evaluation."""
    
    def test_division_by_zero(self):
        """Test that division by zero raises error."""
        tokens = tokenize("5 / 0")
        ast = parse(tokens)
        with self.assertRaises(ValueError) as context:
            evaluate(ast)
        self.assertIn("zero", str(context.exception).lower())
    
    def test_modulo_by_zero(self):
        """Test that modulo by zero raises error."""
        tokens = tokenize("5 % 0")
        ast = parse(tokens)
        with self.assertRaises(ValueError) as context:
            evaluate(ast)
        self.assertIn("zero", str(context.exception).lower())
    
    def test_evaluate_none(self):
        """Test that evaluating None raises error."""
        with self.assertRaises(ValueError):
            evaluate(None)


class TestEvaluatorComplexExpressions(unittest.TestCase):
    """Test complex expression evaluation."""
    
    def test_from_scheme_original(self):
        """Test expression from original Scheme code."""
        tokens = tokenize("(12 * 2) + 3 + 4")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 31)
    
    def test_many_operations(self):
        """Test expression with many operations."""
        tokens = tokenize("1 + 2 * 3 - 4 / 2")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 5)  # 1 + 6 - 2 = 5
    
    def test_deeply_nested(self):
        """Test deeply nested expression."""
        tokens = tokenize("((((1 + 2))))")
        ast = parse(tokens)
        result = evaluate(ast)
        self.assertEqual(result, 3)
    
    def test_all_operators_combined(self):
        """Test expression with all operators."""
        tokens = tokenize("2 ^ 3 + 4 * 5 - 6 / 2 % 2")
        ast = parse(tokens)
        result = evaluate(ast)
        # 2^3 + 4*5 - (6/2)%2 = 8 + 20 - 1 = 27
        self.assertEqual(result, 27)


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions."""
    
    def test_convert_to_number_int(self):
        """Test converting integer string."""
        result = convert_to_number("42")
        self.assertEqual(result, 42)
        self.assertIsInstance(result, int)
    
    def test_convert_to_number_float(self):
        """Test converting float string."""
        result = convert_to_number("3.14")
        self.assertAlmostEqual(result, 3.14)
        self.assertIsInstance(result, float)
    
    def test_format_result_int(self):
        """Test formatting integer result."""
        result = format_result(42)
        self.assertEqual(result, "42")
    
    def test_format_result_whole_float(self):
        """Test formatting whole number float."""
        result = format_result(42.0)
        self.assertEqual(result, "42")
    
    def test_format_result_decimal(self):
        """Test formatting decimal result."""
        result = format_result(3.14)
        self.assertEqual(result, "3.14")
    
    def test_add_function(self):
        """Test add helper function."""
        self.assertEqual(add(2, 3), 5)
    
    def test_subtract_function(self):
        """Test subtract helper function."""
        self.assertEqual(subtract(5, 3), 2)
    
    def test_multiply_function(self):
        """Test multiply helper function."""
        self.assertEqual(multiply(4, 5), 20)
    
    def test_divide_function(self):
        """Test divide helper function."""
        self.assertEqual(divide(20, 4), 5)
    
    def test_modulo_function(self):
        """Test modulo helper function."""
        self.assertEqual(modulo(17, 5), 2)
    
    def test_power_function(self):
        """Test power helper function."""
        self.assertEqual(power(2, 3), 8)
    
    def test_negate_function(self):
        """Test negate helper function."""
        self.assertEqual(negate(5), -5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
