# test_calculator.py
import pytest
from Calculator import Calculator

calculator = Calculator()

# Test invalid syntax
@pytest.mark.parametrize("expression", [
    "2*^3",  # Invalid operator
    "5//2",  # Double slash
    "3+*",   # Operator without operand
    "(3+5",  # Unmatched parenthesis
    "4+5)",  # Unmatched parenthesis
])
def test_invalid_syntax(expression):
    assert calculator.calculate(expression) is None

# Test gibberish
@pytest.mark.parametrize("expression", [
    "abc123",  # Random characters
    "!@#$%^&*",  # Special characters
    "ג'יבריש",   # Non-Latin gibberish
])
def test_gibberish(expression):
    assert calculator.calculate(expression) is None

# Test empty and whitespace strings
@pytest.mark.parametrize("expression", [
    "",      # Empty string
    "   ",   # Whitespaces
    "\t\t",  # Tabs
])
def test_empty_and_whitespace(expression):
    assert calculator.calculate(expression) is None

# Test simple expressions
@pytest.mark.parametrize("expression, expected", [
    ("2+3", 5),
    ("10-4", 6),
    ("3*4", 12),
    ("8/2", 4),
    ("2^3", 8),
    ("!5", 120),
    ("~3", -3),
    ("10%3", 1),
    ("10$3", 10),
    ("10&3", 3),
    ("10@20", 15),
    ("(2+3)*4", 20),
    ("3+4*2", 11),
    ("(10-2)^2", 64),
])
def test_simple_expressions(expression, expected):
    result = calculator.calculate(expression)
    assert result == pytest.approx(expected, rel=1e-5), f"Failed for expression: {expression}"

# Test complex expressions
@pytest.mark.parametrize("expression, expected", [
    ("(2+3)*4-5", 15),
    ("10/(2+3)*4", 8),
    ("(!3+2)^2", 64),
    ("~(5*2)+10", 0),
    ("(10%3)^2+4", 5),
    ("2^(3+1)+1", 17),
    ("(3+4)*(5-2)", 21),
    ("10/(2+3) + (5-1)", 6),
    ("((3+4)^2)/7", 7),
    ("!(2*5)/(10)", 362880),
    ("(!(3+2)/(5-1))*2", 60),
    ("(10-3$4)*2", 14),
    ("(3+5)*(2+3)", 40),
    ("((3+5)@(2+3))^2", 42.25),
    ("(3+4)*(2+3)^2", 175),
    ("(10/(2+3)+4)*3", 18),
])
def test_complex_expressions(expression, expected):
    result = calculator.calculate(expression)
    assert result == pytest.approx(expected, rel=1e-5), f"Failed for expression: {expression}"
