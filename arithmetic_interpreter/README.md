# Arithmetic Expression Interpreter

A Python implementation of an arithmetic expression interpreter using only functions (no classes). This project implements the classic compiler pipeline: **Tokenizer → Parser → Evaluator**.

## Features

- **Lexical Analysis (Tokenizer)**: Converts input string into tokens
- **Parsing (Recursive Descent)**: Builds an Abstract Syntax Tree (AST)
- **Evaluation (Tree-Walking)**: Evaluates the AST to produce a result
- **Operator Precedence**: Correctly handles mathematical operator precedence
- **Parentheses Support**: Override precedence with grouping
- **Unary Negation**: Support for negative numbers
- **Decimal Numbers**: Support for floating-point arithmetic

## Supported Operators

| Operator | Description | Precedence | Associativity |
|----------|-------------|------------|---------------|
| `^` | Power | Highest | Right |
| `*` | Multiplication | High | Left |
| `/` | Division | High | Left |
| `%` | Modulo | High | Left |
| `+` | Addition | Low | Left |
| `-` | Subtraction | Low | Left |
| `-` (unary) | Negation | Highest | Right |
| `()` | Grouping | - | - |

## Project Structure

```
arithmetic_interpreter/
├── main.py              # Entry point
├── run_tests.py         # Test runner
├── README.md            # This file
├── src/
│   ├── __init__.py      # Package exports
│   ├── token.py         # Token functions
│   ├── tokenizer.py     # Lexical analysis
│   ├── node.py          # AST node functions
│   ├── parser.py        # Recursive descent parser
│   ├── evaluator.py     # AST evaluation
│   └── interpreter.py   # Main interpreter logic
└── tests/
    ├── __init__.py
    ├── test_tokenizer.py
    ├── test_parser.py
    ├── test_evaluator.py
    └── test_interpreter.py
```

## Installation

No external dependencies required. Uses only Python standard library.

```bash
# Clone or download the project
cd arithmetic_interpreter
```

## Usage

### Interactive REPL Mode

```bash
python main.py
```

```
==================================================
  Arithmetic Expression Interpreter
==================================================
Enter expressions to evaluate.
Commands: 'quit' or 'exit' to stop
          'verbose' to toggle verbose mode
==================================================

> 2 + 3 * 4
= 14
> (2 + 3) * 4
= 20
> 2 ^ 3 ^ 2
= 512
> quit
Goodbye!
```

### Command Line Mode

```bash
# Evaluate a single expression
python main.py "2 + 3 * 4"

# Verbose mode (shows tokens and AST)
python main.py -v "(12 * 2) + 3 + 4"
```

### Programmatic Usage

```python
from src import interpret, tokenize, parse, evaluate

# Simple interpretation
result = interpret("2 + 3 * 4")
print(result)  # 14

# Step by step
tokens = tokenize("2 + 3")
ast = parse(tokens)
result = evaluate(ast)

# With details
from src import interpret_with_details
details = interpret_with_details("2 + 3 * 4")
print(details['tokens'])
print(details['ast'])
print(details['result'])

# Validation only
from src import validate_expression
is_valid, error = validate_expression("2 + + 3")
```

## Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test module
python run_tests.py tokenizer
python run_tests.py parser
python run_tests.py evaluator
python run_tests.py interpreter
```

## Grammar

The parser implements the following grammar:

```
expression  → term (('+' | '-') term)*
term        → power (('*' | '/' | '%') power)*
power       → unary ('^' unary)*
unary       → '-' unary | primary
primary     → NUMBER | '(' expression ')'
```

## Examples

| Expression | Result | Notes |
|------------|--------|-------|
| `2 + 3` | `5` | Addition |
| `10 - 4` | `6` | Subtraction |
| `6 * 7` | `42` | Multiplication |
| `20 / 4` | `5` | Division |
| `17 % 5` | `2` | Modulo |
| `2 ^ 10` | `1024` | Power |
| `2 + 3 * 4` | `14` | Precedence (* before +) |
| `(2 + 3) * 4` | `20` | Parentheses override |
| `2 ^ 3 ^ 2` | `512` | Right-associative (2^9) |
| `-5 + 10` | `5` | Unary negation |
| `--5` | `5` | Double negation |
| `3.14 * 2` | `6.28` | Decimal numbers |

## Architecture

### Token
A token is a dictionary with `tag` and `value`:
```python
{"tag": "number", "value": "42"}
{"tag": "+", "value": "+"}
```

### AST Node
An AST node is a dictionary with `tag`, `value`, `left`, and `right`:
```python
{"tag": "number", "value": "42", "left": None, "right": None}
{"tag": "+", "value": "+", "left": {...}, "right": {...}}
```

### Pipeline
1. **Input**: `"2 + 3 * 4"`
2. **Tokenize**: `[{number, "2"}, {+, "+"}, {number, "3"}, {*, "*"}, {number, "4"}]`
3. **Parse**: AST with `+` at root, `2` as left, `*` node as right
4. **Evaluate**: `14`

## Error Handling

The interpreter handles various errors:
- Invalid characters in input
- Unmatched parentheses
- Missing operands
- Division by zero
- Empty input

## License

MIT License
