"""
Test Cases for Tokenizer Module
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tokenizer import tokenize, get_patterns, match_single_token
from src.token import get_token_tag, get_token_value


class TestTokenizerBasic(unittest.TestCase):
    """Basic tokenizer tests."""
    
    def test_single_digit(self):
        """Test tokenizing a single digit."""
        tokens = tokenize("5")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(get_token_tag(tokens[0]), 'number')
        self.assertEqual(get_token_value(tokens[0]), '5')
    
    def test_multi_digit(self):
        """Test tokenizing multi-digit numbers."""
        tokens = tokenize("123")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(get_token_tag(tokens[0]), 'number')
        self.assertEqual(get_token_value(tokens[0]), '123')
    
    def test_decimal_number(self):
        """Test tokenizing decimal numbers."""
        tokens = tokenize("3.14")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(get_token_tag(tokens[0]), 'number')
        self.assertEqual(get_token_value(tokens[0]), '3.14')
    
    def test_simple_addition(self):
        """Test tokenizing simple addition."""
        tokens = tokenize("2 + 3")
        self.assertEqual(len(tokens), 3)
        self.assertEqual(get_token_tag(tokens[0]), 'number')
        self.assertEqual(get_token_tag(tokens[1]), '+')
        self.assertEqual(get_token_tag(tokens[2]), 'number')
    
    def test_all_operators(self):
        """Test tokenizing all supported operators."""
        tokens = tokenize("1 + 2 - 3 * 4 / 5 % 6 ^ 7")
        operators = [get_token_tag(t) for t in tokens if get_token_tag(t) != 'number']
        self.assertEqual(operators, ['+', '-', '*', '/', '%', '^'])


class TestTokenizerWhitespace(unittest.TestCase):
    """Whitespace handling tests."""
    
    def test_no_whitespace(self):
        """Test expression without whitespace."""
        tokens = tokenize("2+3")
        self.assertEqual(len(tokens), 3)
    
    def test_extra_whitespace(self):
        """Test expression with extra whitespace."""
        tokens = tokenize("  2   +   3  ")
        self.assertEqual(len(tokens), 3)
    
    def test_tabs_and_spaces(self):
        """Test expression with tabs and spaces."""
        tokens = tokenize("2\t+\t3")
        self.assertEqual(len(tokens), 3)


class TestTokenizerParentheses(unittest.TestCase):
    """Parentheses tokenization tests."""
    
    def test_simple_parentheses(self):
        """Test simple parenthesized expression."""
        tokens = tokenize("(2 + 3)")
        self.assertEqual(len(tokens), 5)
        self.assertEqual(get_token_tag(tokens[0]), '(')
        self.assertEqual(get_token_tag(tokens[4]), ')')
    
    def test_nested_parentheses(self):
        """Test nested parentheses."""
        tokens = tokenize("((1 + 2) * 3)")
        paren_count = sum(1 for t in tokens if get_token_tag(t) in ('(', ')'))
        self.assertEqual(paren_count, 4)


class TestTokenizerEdgeCases(unittest.TestCase):
    """Edge cases and error handling tests."""
    
    def test_empty_string(self):
        """Test that empty string raises error."""
        with self.assertRaises(ValueError):
            tokenize("")
    
    def test_whitespace_only(self):
        """Test that whitespace-only string raises error."""
        with self.assertRaises(ValueError):
            tokenize("   ")
    
    def test_invalid_character(self):
        """Test that invalid characters raise error."""
        with self.assertRaises(ValueError):
            tokenize("2 + x")
    
    def test_non_string_input(self):
        """Test that non-string input raises error."""
        with self.assertRaises(TypeError):
            tokenize(123)
        with self.assertRaises(TypeError):
            tokenize(None)
    
    def test_special_characters(self):
        """Test that special characters raise error."""
        with self.assertRaises(ValueError):
            tokenize("2 @ 3")
        with self.assertRaises(ValueError):
            tokenize("2 # 3")


class TestTokenizerComplex(unittest.TestCase):
    """Complex expression tests."""
    
    def test_complex_expression(self):
        """Test complex expression tokenization."""
        tokens = tokenize("(12 * 2) + 3 + 4")
        self.assertEqual(len(tokens), 9)
    
    def test_negative_start(self):
        """Test expression starting with minus."""
        tokens = tokenize("-5 + 3")
        self.assertEqual(len(tokens), 4)
        self.assertEqual(get_token_tag(tokens[0]), '-')
    
    def test_large_numbers(self):
        """Test large numbers."""
        tokens = tokenize("999999999 + 1")
        self.assertEqual(get_token_value(tokens[0]), '999999999')


class TestMatchSingleToken(unittest.TestCase):
    """Tests for match_single_token function."""
    
    def test_match_number(self):
        """Test matching a number."""
        patterns = get_patterns()
        result = match_single_token("123", 0, patterns)
        self.assertIsNotNone(result)
        token, pos = result
        self.assertEqual(get_token_tag(token), 'number')
        self.assertEqual(get_token_value(token), '123')
        self.assertEqual(pos, 3)
    
    def test_match_operator(self):
        """Test matching an operator."""
        patterns = get_patterns()
        result = match_single_token("+", 0, patterns)
        self.assertIsNotNone(result)
        token, pos = result
        self.assertEqual(get_token_tag(token), '+')
    
    def test_no_match(self):
        """Test when no pattern matches."""
        patterns = get_patterns()
        result = match_single_token("@", 0, patterns)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
