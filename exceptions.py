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


