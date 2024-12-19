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
    ("5!", 120),
    ("~3", -3),
    ("10%3", 1),
    ("10$3", 10),
    ("10&3", 3),
    ("10@20", 15),
    ("(2+3)*4", 20),
    ("3+4*2", 11),
    ("(10-2)^2", 64),
    ("(10#-2)^2", 1),
])
def test_simple_expressions(expression, expected):
    result = calculator.calculate(expression)
    assert result == pytest.approx(expected, rel=1e-5), f"Failed for expression: {expression}"


# Test complex expressions
@pytest.mark.parametrize("expression, expected", [

    ("(2+3)*4-5", 15),
    ("10/(2+3)*4", 8),
    ("(3!+2)^2", 64),
    ("~(5*2)+10", 0),
    ("(10%3)^2+4", 5),
    ("2^(3+1)+1", 17),
    ("(3+4)*(5-2)", 21),
    ("10/(2+3) + (5-1)", 6),
    ("((3+4)^2)/7", 7),
    ("(2*5)!/(10)", 362880),
    ("((3+2)!/(5-1))*2", 60),
    ("(10-3$4)*2", 12),
    ("(3+5)*(2+3)", 40),
    ("((3+5)@(2+3))^2", 42.25),
    ("(3+4)*(2+3)^2", 175),
    ("(10/(2+3)+4)*3", 18),
    ("((2+3)*4-5+6+10+1)", 32),
    ("10/(2+3)*4+(5-3+8+1)", 19),
    ("((3!+2)^2+(4-2)+12+1)", 79),
    ("~(5*2)+(10/(5-3)+20+1)", 16),
    ("((10%3)^2+4)*2+15+1", 26),
    ("2^(3+1)+1+(5-3+12+1)", 32),
    ("((3+4)*(5-2))+10+15+1", 47),
    ("10/(2+3)+(5-1)^2+10+1", 29),
    ("(((3+4)^2)/7)+(2^2+12+1)", 24),
    ("(2*5)!/(10-5)+14+1+2", 725777),
    ("((3!+2)/(5-1))*2+11+3+1", 19),
    ("(10-3$4)*2+(5^2)+12+1", 50),
    ("(3+5)*(2+3)+(10/2+13+1)", 59),
    ("((3+5)@(2+3))^2+(10-3+9+1)", 59.25),
    ("((3+4)*(2+3)^2)+2+13+1", 191),
    ("(10/(2+3)+4)*3+11+3+1", 33),
    ("~5!", None),
    ("~--3", -3),
    ("2--5!", None),

])
def test_complex_expressions(expression, expected):
    result = calculator.calculate(expression)
    assert result == pytest.approx(expected, rel=1e-5), f"Failed for expression: {expression}"
