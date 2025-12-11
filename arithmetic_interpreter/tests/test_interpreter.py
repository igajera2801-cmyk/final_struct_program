"""
Integration Tests for Arithmetic Interpreter
Tests the complete pipeline: tokenize -> parse -> evaluate
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.interpreter import interpret, interpret_with_details, validate_expression


class TestInterpreterBasic(unittest.TestCase):
    """Basic interpreter integration tests."""
    
    def test_single_number(self):
        """Test interpreting a single number."""
        self.assertEqual(interpret("42"), 42)
    
    def test_addition(self):
        """Test simple addition."""
        self.assertEqual(interpret("2 + 3"), 5)
    
    def test_subtraction(self):
        """Test simple subtraction."""
        self.assertEqual(interpret("10 - 4"), 6)
    
    def test_multiplication(self):
        """Test simple multiplication."""
        self.assertEqual(interpret("6 * 7"), 42)
    
    def test_division(self):
        """Test simple division."""
        self.assertEqual(interpret("20 / 4"), 5)
    
    def test_modulo(self):
        """Test modulo operation."""
        self.assertEqual(interpret("17 % 5"), 2)
    
    def test_power(self):
        """Test power operation."""
        self.assertEqual(interpret("2 ^ 10"), 1024)


class TestInterpreterOperatorPrecedence(unittest.TestCase):
    """Test operator precedence in full pipeline."""
    
    def test_multiplication_before_addition(self):
        """Test correct precedence: 2 + 3 * 4 = 14."""
        self.assertEqual(interpret("2 + 3 * 4"), 14)
    
    def test_division_before_subtraction(self):
        """Test correct precedence: 10 - 6 / 2 = 7."""
        self.assertEqual(interpret("10 - 6 / 2"), 7)
    
    def test_power_before_multiplication(self):
        """Test correct precedence: 2 * 3 ^ 2 = 18."""
        self.assertEqual(interpret("2 * 3 ^ 2"), 18)
    
    def test_power_right_associativity(self):
        """Test right associativity: 2 ^ 3 ^ 2 = 512."""
        self.assertEqual(interpret("2 ^ 3 ^ 2"), 512)
    
    def test_modulo_same_as_multiplication(self):
        """Test modulo has same precedence as multiplication."""
        # 10 + 8 % 3 should be 10 + 2 = 12
        self.assertEqual(interpret("10 + 8 % 3"), 12)


class TestInterpreterParentheses(unittest.TestCase):
    """Test parentheses handling in full pipeline."""
    
    def test_parentheses_basic(self):
        """Test basic parentheses: (2 + 3) * 4 = 20."""
        self.assertEqual(interpret("(2 + 3) * 4"), 20)
    
    def test_parentheses_nested(self):
        """Test nested parentheses."""
        self.assertEqual(interpret("((2 + 3) * 2)"), 10)
    
    def test_parentheses_multiple(self):
        """Test multiple parenthesized groups."""
        self.assertEqual(interpret("(1 + 2) * (3 + 4)"), 21)
    
    def test_parentheses_complex(self):
        """Test complex expression with parentheses."""
        self.assertEqual(interpret("((10 + 2) * 3) / 6"), 6)


class TestInterpreterNegation(unittest.TestCase):
    """Test negation in full pipeline."""
    
    def test_simple_negation(self):
        """Test simple negation: -5 = -5."""
        self.assertEqual(interpret("-5"), -5)
    
    def test_double_negation(self):
        """Test double negation: --5 = 5."""
        self.assertEqual(interpret("--5"), 5)
    
    def test_triple_negation(self):
        """Test triple negation: ---5 = -5."""
        self.assertEqual(interpret("---5"), -5)
    
    def test_negation_in_expression(self):
        """Test negation in expression: -5 + 10 = 5."""
        self.assertEqual(interpret("-5 + 10"), 5)
    
    def test_negation_with_multiplication(self):
        """Test negation with multiplication."""
        self.assertEqual(interpret("-3 * 4"), -12)
    
    def test_negation_with_parentheses(self):
        """Test negation with parentheses: -(3 + 2) = -5."""
        self.assertEqual(interpret("-(3 + 2)"), -5)


class TestInterpreterDecimalNumbers(unittest.TestCase):
    """Test decimal number handling in full pipeline."""
    
    def test_decimal_input(self):
        """Test decimal input."""
        self.assertAlmostEqual(interpret("3.14"), 3.14)
    
    def test_decimal_addition(self):
        """Test decimal addition."""
        self.assertAlmostEqual(interpret("1.5 + 2.5"), 4.0)
    
    def test_decimal_multiplication(self):
        """Test decimal multiplication."""
        self.assertAlmostEqual(interpret("2.5 * 4"), 10.0)
    
    def test_mixed_integer_decimal(self):
        """Test mixed integer and decimal."""
        self.assertAlmostEqual(interpret("5 + 2.5"), 7.5)


class TestInterpreterComplexExpressions(unittest.TestCase):
    """Test complex expression evaluation."""
    
    def test_original_scheme_expression(self):
        """Test expression from original Scheme code: (12 * 2) + 3 + 4 = 31."""
        self.assertEqual(interpret("(12 * 2) + 3 + 4"), 31)
    
    def test_many_operations(self):
        """Test many operations: 1 + 2 * 3 - 4 / 2 = 5."""
        self.assertEqual(interpret("1 + 2 * 3 - 4 / 2"), 5)
    
    def test_all_operators(self):
        """Test all operators together."""
        # 2^3 + 4*5 - 6/2 + 7%3 = 8 + 20 - 3 + 1 = 26
        self.assertEqual(interpret("2 ^ 3 + 4 * 5 - 6 / 2 + 7 % 3"), 26)
    
    def test_deeply_nested(self):
        """Test deeply nested expression."""
        self.assertEqual(interpret("(((1 + 2) * 3) - 4) / 5"), 1)
    
    def test_large_numbers(self):
        """Test large numbers."""
        self.assertEqual(interpret("1000000 * 1000000"), 1000000000000)
    
    def test_chained_additions(self):
        """Test chained additions."""
        self.assertEqual(interpret("1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10"), 55)
    
    def test_chained_multiplications(self):
        """Test chained multiplications (factorial-like)."""
        self.assertEqual(interpret("1 * 2 * 3 * 4 * 5"), 120)


class TestInterpreterEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_zero(self):
        """Test zero."""
        self.assertEqual(interpret("0"), 0)
    
    def test_add_zero(self):
        """Test adding zero."""
        self.assertEqual(interpret("5 + 0"), 5)
    
    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        self.assertEqual(interpret("100 * 0"), 0)
    
    def test_zero_power(self):
        """Test zero as exponent."""
        self.assertEqual(interpret("5 ^ 0"), 1)
    
    def test_power_of_one(self):
        """Test power of one."""
        self.assertEqual(interpret("5 ^ 1"), 5)
    
    def test_whitespace_handling(self):
        """Test extra whitespace."""
        self.assertEqual(interpret("  2   +   3  "), 5)
    
    def test_no_whitespace(self):
        """Test no whitespace."""
        self.assertEqual(interpret("2+3*4"), 14)


class TestInterpreterErrors(unittest.TestCase):
    """Test error handling."""
    
    def test_division_by_zero(self):
        """Test division by zero error."""
        with self.assertRaises(ValueError):
            interpret("5 / 0")
    
    def test_invalid_character(self):
        """Test invalid character error."""
        with self.assertRaises(ValueError):
            interpret("2 + x")
    
    def test_empty_input(self):
        """Test empty input error."""
        with self.assertRaises(ValueError):
            interpret("")
    
    def test_unmatched_parenthesis(self):
        """Test unmatched parenthesis error."""
        with self.assertRaises(ValueError):
            interpret("(2 + 3")
    
    def test_missing_operand(self):
        """Test missing operand error."""
        with self.assertRaises(ValueError):
            interpret("2 +")


class TestInterpretWithDetails(unittest.TestCase):
    """Test interpret_with_details function."""
    
    def test_returns_all_fields(self):
        """Test that all fields are returned."""
        result = interpret_with_details("2 + 3")
        
        self.assertIn('input', result)
        self.assertIn('tokens', result)
        self.assertIn('ast', result)
        self.assertIn('result', result)
        self.assertIn('formatted_result', result)
        self.assertIn('reconstructed', result)
    
    def test_correct_result(self):
        """Test correct result in details."""
        result = interpret_with_details("2 + 3 * 4")
        
        self.assertEqual(result['input'], "2 + 3 * 4")
        self.assertEqual(result['result'], 14)
        self.assertEqual(result['formatted_result'], "14")


class TestValidateExpression(unittest.TestCase):
    """Test validate_expression function."""
    
    def test_valid_expression(self):
        """Test validation of valid expression."""
        is_valid, error = validate_expression("2 + 3")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_invalid_expression(self):
        """Test validation of invalid expression."""
        is_valid, error = validate_expression("2 + + 3")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_empty_expression(self):
        """Test validation of empty expression."""
        is_valid, error = validate_expression("")
        self.assertFalse(is_valid)


# Mathematical identity tests
class TestMathematicalIdentities(unittest.TestCase):
    """Test mathematical identities and properties."""
    
    def test_commutative_addition(self):
        """Test commutativity of addition: a + b = b + a."""
        self.assertEqual(interpret("3 + 5"), interpret("5 + 3"))
    
    def test_commutative_multiplication(self):
        """Test commutativity of multiplication: a * b = b * a."""
        self.assertEqual(interpret("3 * 5"), interpret("5 * 3"))
    
    def test_associative_addition(self):
        """Test associativity of addition: (a + b) + c = a + (b + c)."""
        self.assertEqual(interpret("(1 + 2) + 3"), interpret("1 + (2 + 3)"))
    
    def test_associative_multiplication(self):
        """Test associativity of multiplication: (a * b) * c = a * (b * c)."""
        self.assertEqual(interpret("(2 * 3) * 4"), interpret("2 * (3 * 4)"))
    
    def test_distributive(self):
        """Test distributive property: a * (b + c) = a*b + a*c."""
        self.assertEqual(interpret("2 * (3 + 4)"), interpret("2 * 3 + 2 * 4"))
    
    def test_additive_identity(self):
        """Test additive identity: a + 0 = a."""
        self.assertEqual(interpret("5 + 0"), 5)
    
    def test_multiplicative_identity(self):
        """Test multiplicative identity: a * 1 = a."""
        self.assertEqual(interpret("5 * 1"), 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
