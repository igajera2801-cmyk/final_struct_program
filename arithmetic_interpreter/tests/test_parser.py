"""
Test Cases for Parser Module
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tokenizer import tokenize
from src.parser import (
    parse, parse_expression, parse_term, parse_primary, parse_unary,
    peek_token, consume_token, expect_token
)
from src.node import (
    get_node_tag, get_node_value, get_node_left, get_node_right,
    is_leaf_node, is_binary_node, is_unary_node
)


class TestParserBasic(unittest.TestCase):
    """Basic parser tests."""
    
    def test_parse_single_number(self):
        """Test parsing a single number."""
        tokens = tokenize("42")
        ast = parse(tokens)
        self.assertEqual(get_node_tag(ast), 'number')
        self.assertEqual(get_node_value(ast), '42')
        self.assertTrue(is_leaf_node(ast))
    
    def test_parse_simple_addition(self):
        """Test parsing simple addition."""
        tokens = tokenize("2 + 3")
        ast = parse(tokens)
        self.assertEqual(get_node_tag(ast), '+')
        self.assertTrue(is_binary_node(ast))
        self.assertEqual(get_node_value(get_node_left(ast)), '2')
        self.assertEqual(get_node_value(get_node_right(ast)), '3')
    
    def test_parse_simple_subtraction(self):
        """Test parsing simple subtraction."""
        tokens = tokenize("5 - 3")
        ast = parse(tokens)
        self.assertEqual(get_node_tag(ast), '-')
    
    def test_parse_simple_multiplication(self):
        """Test parsing simple multiplication."""
        tokens = tokenize("4 * 3")
        ast = parse(tokens)
        self.assertEqual(get_node_tag(ast), '*')
    
    def test_parse_simple_division(self):
        """Test parsing simple division."""
        tokens = tokenize("8 / 2")
        ast = parse(tokens)
        self.assertEqual(get_node_tag(ast), '/')


class TestParserPrecedence(unittest.TestCase):
    """Operator precedence tests."""
    
    def test_multiplication_before_addition(self):
        """Test that multiplication has higher precedence than addition."""
        # 2 + 3 * 4 should parse as 2 + (3 * 4)
        tokens = tokenize("2 + 3 * 4")
        ast = parse(tokens)
        
        # Root should be +
        self.assertEqual(get_node_tag(ast), '+')
        # Left should be 2
        self.assertEqual(get_node_value(get_node_left(ast)), '2')
        # Right should be * node
        right = get_node_right(ast)
        self.assertEqual(get_node_tag(right), '*')
    
    def test_division_before_subtraction(self):
        """Test that division has higher precedence than subtraction."""
        # 10 - 6 / 2 should parse as 10 - (6 / 2)
        tokens = tokenize("10 - 6 / 2")
        ast = parse(tokens)
        
        self.assertEqual(get_node_tag(ast), '-')
        right = get_node_right(ast)
        self.assertEqual(get_node_tag(right), '/')
    
    def test_left_associativity_addition(self):
        """Test left associativity for addition."""
        # 1 + 2 + 3 should parse as (1 + 2) + 3
        tokens = tokenize("1 + 2 + 3")
        ast = parse(tokens)
        
        # Root should be +
        self.assertEqual(get_node_tag(ast), '+')
        # Right should be 3
        self.assertEqual(get_node_value(get_node_right(ast)), '3')
        # Left should be another + node
        left = get_node_left(ast)
        self.assertEqual(get_node_tag(left), '+')
    
    def test_left_associativity_multiplication(self):
        """Test left associativity for multiplication."""
        # 2 * 3 * 4 should parse as (2 * 3) * 4
        tokens = tokenize("2 * 3 * 4")
        ast = parse(tokens)
        
        self.assertEqual(get_node_tag(ast), '*')
        self.assertEqual(get_node_value(get_node_right(ast)), '4')
        left = get_node_left(ast)
        self.assertEqual(get_node_tag(left), '*')
    
    def test_power_right_associativity(self):
        """Test right associativity for power operator."""
        # 2 ^ 3 ^ 2 should parse as 2 ^ (3 ^ 2)
        tokens = tokenize("2 ^ 3 ^ 2")
        ast = parse(tokens)
        
        self.assertEqual(get_node_tag(ast), '^')
        self.assertEqual(get_node_value(get_node_left(ast)), '2')
        right = get_node_right(ast)
        self.assertEqual(get_node_tag(right), '^')


class TestParserParentheses(unittest.TestCase):
    """Parentheses handling tests."""
    
    def test_parentheses_override_precedence(self):
        """Test that parentheses override operator precedence."""
        # (2 + 3) * 4 should parse with + at the left
        tokens = tokenize("(2 + 3) * 4")
        ast = parse(tokens)
        
        self.assertEqual(get_node_tag(ast), '*')
        left = get_node_left(ast)
        self.assertEqual(get_node_tag(left), '+')
    
    def test_nested_parentheses(self):
        """Test nested parentheses."""
        tokens = tokenize("((2 + 3))")
        ast = parse(tokens)
        
        self.assertEqual(get_node_tag(ast), '+')
    
    def test_complex_parentheses(self):
        """Test complex parenthesized expression."""
        tokens = tokenize("(1 + 2) * (3 + 4)")
        ast = parse(tokens)
        
        self.assertEqual(get_node_tag(ast), '*')
        self.assertEqual(get_node_tag(get_node_left(ast)), '+')
        self.assertEqual(get_node_tag(get_node_right(ast)), '+')


class TestParserUnary(unittest.TestCase):
    """Unary operator tests."""
    
    def test_unary_minus(self):
        """Test unary minus (negation)."""
        tokens = tokenize("-5")
        ast = parse(tokens)
        
        self.assertEqual(get_node_tag(ast), 'negate')
        self.assertTrue(is_unary_node(ast))
        self.assertEqual(get_node_value(get_node_left(ast)), '5')
    
    def test_double_negation(self):
        """Test double negation."""
        tokens = tokenize("--5")
        ast = parse(tokens)
        
        self.assertEqual(get_node_tag(ast), 'negate')
        inner = get_node_left(ast)
        self.assertEqual(get_node_tag(inner), 'negate')
    
    def test_negation_in_expression(self):
        """Test negation within expression."""
        tokens = tokenize("-5 + 3")
        ast = parse(tokens)
        
        self.assertEqual(get_node_tag(ast), '+')
        left = get_node_left(ast)
        self.assertEqual(get_node_tag(left), 'negate')


class TestParserErrors(unittest.TestCase):
    """Parser error handling tests."""
    
    def test_empty_tokens(self):
        """Test parsing empty token list."""
        with self.assertRaises(ValueError):
            parse([])
    
    def test_unmatched_left_paren(self):
        """Test unmatched left parenthesis."""
        tokens = tokenize("(2 + 3")
        with self.assertRaises(ValueError):
            parse(tokens)
    
    def test_unmatched_right_paren(self):
        """Test unmatched right parenthesis."""
        tokens = tokenize("2 + 3)")
        with self.assertRaises(ValueError):
            parse(tokens)
    
    def test_missing_operand(self):
        """Test missing operand."""
        tokens = tokenize("2 +")
        with self.assertRaises(ValueError):
            parse(tokens)
    
    def test_consecutive_operators(self):
        """Test consecutive binary operators."""
        tokens = tokenize("2 + * 3")
        with self.assertRaises(ValueError):
            parse(tokens)


class TestHelperFunctions(unittest.TestCase):
    """Tests for parser helper functions."""
    
    def test_peek_token(self):
        """Test peek_token function."""
        tokens = tokenize("2 + 3")
        token = peek_token(tokens)
        self.assertEqual(get_node_value(token) if token else None, '2')
        # Token list should be unchanged
        self.assertEqual(len(tokens), 3)
    
    def test_peek_empty(self):
        """Test peek_token with empty list."""
        result = peek_token([])
        self.assertIsNone(result)
    
    def test_consume_token(self):
        """Test consume_token function."""
        tokens = tokenize("2 + 3")
        token, remaining = consume_token(tokens)
        self.assertEqual(get_node_value(token), '2')
        self.assertEqual(len(remaining), 2)
    
    def test_consume_empty(self):
        """Test consume_token with empty list."""
        with self.assertRaises(ValueError):
            consume_token([])
    
    def test_expect_token_success(self):
        """Test expect_token with correct token."""
        tokens = tokenize("(2)")
        token, remaining = expect_token(tokens, '(')
        self.assertEqual(get_node_tag(token), '(')
    
    def test_expect_token_failure(self):
        """Test expect_token with wrong token."""
        tokens = tokenize("2 + 3")
        with self.assertRaises(ValueError):
            expect_token(tokens, '(')


if __name__ == '__main__':
    unittest.main(verbosity=2)
