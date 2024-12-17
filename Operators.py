# Operators.py

from abc import ABC, abstractmethod
from exceptions import DivisionByZeroException, FactorialNegativeNumberException, FactorialFloatException, \
    ResultTooLargeException, InvalidExpressionException


class Operator(ABC):
    def __init__(self, symbol, precedence, associativity, arity):
        """
        Initialize the operator.

        :param symbol: str, the operator symbol.
        :param precedence: int, the precedence level.
        :param associativity: str, 'left' or 'right'.
        :param arity: int, number of operands (1 for unary, 2 for binary).
        """
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity
        self.arity = arity

    @abstractmethod
    def evaluate(self, operand1, operand2=None):
        """
        Execute the operator's operation on operands.

        :param operand1: float
        :param operand2: float, optional
        :return: float
        """
        pass


class AdditionOperator(Operator):
    def __init__(self):
        super().__init__('+', 1, 'left', 2)

    def evaluate(self, operand1, operand2):
        return operand1 + operand2


class SubtractionOperator(Operator):
    def __init__(self):
        super().__init__('-', 1, 'left', 2)

    def evaluate(self, operand1, operand2):
        return operand1 - operand2


class MultiplicationOperator(Operator):
    def __init__(self):
        super().__init__('*', 2, 'left', 2)

    def evaluate(self, operand1, operand2):
        try:
            # חישוב הכפלה עם טיפול ב-OverflowError
            result = operand1 * operand2
        except OverflowError:
            raise ResultTooLargeException(f"Result too large: {operand1} * {operand2}")

        # בדיקה סופית שהתוצאה בגבולות המותרים
        if abs(result) > MAX_RESULT:
            raise ResultTooLargeException(f"Result too large: {result}")

        return result


class DivisionOperator(Operator):
    def __init__(self):
        super().__init__('/', 2, 'left', 2)

    def evaluate(self, operand1, operand2):
        if operand2 == 0:
            raise DivisionByZeroException()
        # בדיקה אם התוצאה תחרוג מ-MAX_RESULT
        if abs(operand1 / operand2) > MAX_RESULT:
            raise ResultTooLargeException(f"Result too large: {operand1} / {operand2}")
        return operand1 / operand2


class PowerOperator(Operator):
    def __init__(self):
        super().__init__('^', 3, 'right', 2)

    def evaluate(self, operand1, operand2):
        try:

            result = pow(operand1, operand2)
        except OverflowError:

            raise ResultTooLargeException(f"Result too large: {operand1}^{operand2}")

        if abs(result) > MAX_RESULT:
            raise ResultTooLargeException(f"Result too large: {result}")

        return result


MAX_RESULT = 1e308

class FactorialOperator(Operator):
    def __init__(self):
        super().__init__('!', 6, 'right', 1)  # right associativity, unary operator

    def evaluate(self, operand1, operand2=None):
        # Allow numbers very close to integers by rounding them
        if abs(operand1 - round(operand1)) < 0.0001:
            operand1 = round(operand1)  # Round to the nearest integer

        # Validate the input after rounding
        if operand1 < 0:
            raise FactorialNegativeNumberException(operand1)
        if operand1 != int(operand1):  # Check for non-integer values without using is_integer()
            raise FactorialFloatException(operand1)

        # Handle factorial for large numbers
        operand1 = int(operand1)  # Ensure operand is an integer
        if operand1 > 170:
            raise ResultTooLargeException(f"Factorial input too large: {operand1}")

        # Calculate factorial iteratively
        result = 1
        for i in range(1, operand1 + 1):
            result *= i
        return result


class UnaryMinusOperator(Operator):
    def __init__(self):
        super().__init__('u-', 3, 'right', 1)  # Unary minus operator

    def evaluate(self, operand1, operand2=None):
        return -operand1


class TildeOperator(Operator):
    def __init__(self):

        super().__init__('~', 6, 'right', 1)

    def evaluate(self, operand1, operand2=None):
        return -operand1


class ModuloOperator(Operator):
    def __init__(self):
        super().__init__('%', 4, 'left', 2)

    def evaluate(self, operand1, operand2):
        if operand2 == 0:
            raise DivisionByZeroException()
        return operand1 % operand2


class MaxOperator(Operator):
    def __init__(self):
        super().__init__('$', 5, 'left', 2)

    def evaluate(self, operand1, operand2):
        return max(operand1, operand2)


class MinOperator(Operator):
    def __init__(self):
        super().__init__('&', 5, 'left', 2)

    def evaluate(self, operand1, operand2):
        return min(operand1, operand2)


class AverageOperator(Operator):
    def __init__(self):
        super().__init__('@', 5, 'left', 2)

    def evaluate(self, operand1, operand2):
        return (operand1 + operand2) / 2


class DigitSumOperator(Operator):
    def __init__(self):
        super().__init__('#', 6, 'right', 1)  # Precedence 6, unary operator, right associativity

    def evaluate(self, operand1, operand2=None):
        operand_str = str(operand1)  # המרת הקלט למחרוזת

        # בדיקה אם המספר בפורמט מדעי (מכיל 'e' או 'E')
        if 'e' in operand_str.lower():
            raise InvalidExpressionException(f"Number is too large: {operand1}")

        # בדיקה אם המספר שלילי
        if float(operand1) < 0:
            raise InvalidExpressionException(f"DigitSumOperator is not defined for negative numbers: {operand1}")

        # חישוב סכום הספרות
        digit_sum = sum(int(digit) for digit in operand_str if digit.isdigit())
        return digit_sum

