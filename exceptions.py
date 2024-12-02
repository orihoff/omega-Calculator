# exceptions.py

class CalculatorException(Exception):
    """
    Base class for all calculator-related exceptions.
    """
    pass


class InvalidTokenException(CalculatorException):
    """
    Raised when an invalid token is encountered in the expression.
    """
    def __init__(self, token):
        super().__init__(f"Invalid token encountered: {token}")


class InvalidExpressionException(CalculatorException):
    """
    Raised when the expression is invalid or improperly formatted.
    """
    def __init__(self, message="Invalid expression."):
        super().__init__(message)


class DivisionByZeroException(CalculatorException):
    """
    Raised when a division by zero is attempted.
    """
    def __init__(self):
        super().__init__("Division by zero is not allowed.")


class ConsecutiveTildesException(CalculatorException):
    """
    Raised when consecutive tilde operators are encountered in the expression.
    """
    def __init__(self):
        super().__init__("Consecutive tildes are not allowed in the expression.")


class FactorialNegativeNumberException(CalculatorException):
    """
    Raised when attempting to calculate the factorial of a negative number.
    """
    def __init__(self):
        super().__init__("Factorial is not defined for negative numbers.")


class MissingOperandException(CalculatorException):
    """
    Raised when an operator is missing a required operand.
    """
    def __init__(self, operator):
        super().__init__(f"Missing operand for operator: {operator}")


class MismatchedParenthesesException(CalculatorException):
    """
    Raised when there are mismatched parentheses in the expression.
    """
    def __init__(self):
        super().__init__("Mismatched parentheses in the expression.")
