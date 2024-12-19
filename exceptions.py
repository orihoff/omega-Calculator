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
    def __init__(self, token, expression=None, index=None):
        if expression and index is not None:
            error_message = self.generate_error_message(expression, index, f"Invalid token '{token}'")
        else:
            error_message = f"Invalid token encountered: {token}"
        super().__init__(error_message)

    @staticmethod
    def generate_error_message(expression, index, message):
        marker = ' ' * index + '^'
        return f"{message}:\n{expression}\n{marker}"


class InvalidExpressionException(CalculatorException):
    """
    Raised when the expression is invalid or improperly formatted.
    """
    def __init__(self, message="Invalid expression.", expression=None, index=None):
        if expression and index is not None:
            error_message = self.generate_error_message(expression, index, message)
        else:
            error_message = message
        super().__init__(error_message)

    @staticmethod
    def generate_error_message(expression, index, message):
        marker = ' ' * index + '^'
        return f"{message}:\n{expression}\n{marker}"


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
    def __init__(self, expression=None, index=None):
        if expression and index is not None:
            error_message = self.generate_error_message(expression, index, "Consecutive tildes are not allowed")
        else:
            error_message = "Consecutive tildes are not allowed in the expression."
        super().__init__(error_message)

    @staticmethod
    def generate_error_message(expression, index, message):
        marker = ' ' * index + '^'
        return f"{message}:\n{expression}\n{marker}"


class MissingOperandException(CalculatorException):
    """
    Raised when an operator is missing a required operand.
    """
    def __init__(self, operator, expression=None, index=None):
        if expression and index is not None:
            error_message = self.generate_error_message(expression, index, f"Missing operand for operator '{operator}'")
        else:
            error_message = f"Missing operand for operator: {operator}"
        super().__init__(error_message)

    @staticmethod
    def generate_error_message(expression, index, message):
        marker = ' ' * index + '^'
        return f"{message}:\n{expression}\n{marker}"


class MismatchedParenthesesException(CalculatorException):
    """
    Raised when there are mismatched parentheses in the expression.
    """
    def __init__(self, expression=None, index=None):
        if expression and index is not None:
            error_message = self.generate_error_message(expression, index, "Mismatched parentheses")
        else:
            error_message = "Mismatched parentheses in the expression."
        super().__init__(error_message)

    @staticmethod
    def generate_error_message(expression, index, message):
        marker = ' ' * index + '^'
        return f"{message}:\n{expression}\n{marker}"


class InvalidCharacterException(CalculatorException):
    """
    Raised when an invalid character is encountered in the expression.
    """
    def __init__(self, char, expression=None, index=None):
        if expression and index is not None:
            error_message = self.generate_error_message(expression, index, f"Invalid character '{char}'")
        else:
            error_message = f"Invalid character encountered: {char}"
        super().__init__(error_message)

    @staticmethod
    def generate_error_message(expression, index, message):
        marker = ' ' * index + '^'
        return f"{message}:\n{expression}\n{marker}"


class FactorialNegativeNumberException(CalculatorException):
    """
    Raised when attempting to calculate the factorial of a negative number.
    """
    def __init__(self, operand=None):
        if operand is not None:
            message = f"Factorial is not defined for negative numbers: {operand}"
        else:
            message = "Factorial is not defined for negative numbers."
        super().__init__(message)


class FactorialFloatException(CalculatorException):
    """
    Raised when attempting to calculate the factorial of a float number.
    """
    def __init__(self, operand=None):
        if operand is not None:
            message = f"Factorial is not defined for non-integer numbers: {operand}"
        else:
            message = "Factorial is not defined for non-integer numbers."
        super().__init__(message)


class ResultTooLargeException(CalculatorException):
    """
    Raised when the result of a calculation exceeds the allowable range.
    """
    def __init__(self, result):
        message = f"The result {result} is too large to handle."
        super().__init__(message)
