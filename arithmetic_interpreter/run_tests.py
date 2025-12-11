#!/usr/bin/env python3
"""
Test Runner Script
Runs all tests for the Arithmetic Interpreter project.
"""

import unittest
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def run_all_tests():
    """Discover and run all tests."""
    print("=" * 60)
    print("  Arithmetic Interpreter - Test Suite")
    print("=" * 60)
    print()
    
    # Discover tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Skipped: {len(result.skipped)}")
    print()
    
    if result.wasSuccessful():
        print("  ✓ ALL TESTS PASSED!")
        print("=" * 60)
        return 0
    else:
        print("  ✗ SOME TESTS FAILED")
        print("=" * 60)
        return 1


def run_specific_test(test_name):
    """Run a specific test module."""
    print(f"Running tests from: {test_name}")
    print()
    
    loader = unittest.TestLoader()
    
    if test_name == 'tokenizer':
        from tests import test_tokenizer
        suite = loader.loadTestsFromModule(test_tokenizer)
    elif test_name == 'parser':
        from tests import test_parser
        suite = loader.loadTestsFromModule(test_parser)
    elif test_name == 'evaluator':
        from tests import test_evaluator
        suite = loader.loadTestsFromModule(test_evaluator)
    elif test_name == 'interpreter':
        from tests import test_interpreter
        suite = loader.loadTestsFromModule(test_interpreter)
    else:
        print(f"Unknown test module: {test_name}")
        print("Available: tokenizer, parser, evaluator, interpreter")
        return 1
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        if test_name in ('-h', '--help'):
            print("Usage:")
            print("  python run_tests.py           # Run all tests")
            print("  python run_tests.py tokenizer # Run tokenizer tests")
            print("  python run_tests.py parser    # Run parser tests")
            print("  python run_tests.py evaluator # Run evaluator tests")
            print("  python run_tests.py interpreter # Run interpreter tests")
            return 0
        return run_specific_test(test_name)
    else:
        return run_all_tests()


if __name__ == '__main__':
    sys.exit(main())
