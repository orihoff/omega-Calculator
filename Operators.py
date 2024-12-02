# operators.py

from abc import ABC, abstractmethod
from exceptions import DivisionByZeroException


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
    def execute(self, operand1, operand2=None):
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

    def execute(self, operand1, operand2):
        return operand1 + operand2


class SubtractionOperator(Operator):
    def __init__(self):
        super().__init__('-', 1, 'left', 2)

    def execute(self, operand1, operand2):
        return operand1 - operand2


class MultiplicationOperator(Operator):
    def __init__(self):
        super().__init__('*', 2, 'left', 2)

    def execute(self, operand1, operand2):
        return operand1 * operand2


class DivisionOperator(Operator):
    def __init__(self):
        super().__init__('/', 2, 'left', 2)

    def execute(self, operand1, operand2):
        if operand2 == 0:
            raise DivisionByZeroException()
        return operand1 / operand2


class PowerOperator(Operator):
    def __init__(self):
        super().__init__('^', 4, 'right', 2)

    def execute(self, operand1, operand2):
        return pow(operand1, operand2)


class FactorialOperator(Operator):
    def __init__(self):
        super().__init__('!', 5, 'left', 1)

    def execute(self, operand1, operand2=None):
        if operand1 < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        result = 1
        for i in range(1, int(operand1) + 1):
            result *= i
        return result


class NegationOperator(Operator):
    def __init__(self):
        super().__init__('u-', 6, 'right', 1)  # Unary minus operator

    def execute(self, operand1, operand2=None):
        return -operand1


class TildeOperator(Operator):
    def __init__(self):
        super().__init__('~', 6, 'right', 1)  # Tilde operator for negation

    def execute(self, operand1, operand2=None):
        return -operand1


class ModuloOperator(Operator):
    def __init__(self):
        super().__init__('%', 3, 'left', 2)

    def execute(self, operand1, operand2):
        if operand2 == 0:
            raise DivisionByZeroException()
        return operand1 % operand2


class MaxOperator(Operator):
    def __init__(self):
        super().__init__('$', 1, 'left', 2)

    def execute(self, operand1, operand2):
        return max(operand1, operand2)


class MinOperator(Operator):
    def __init__(self):
        super().__init__('&', 1, 'left', 2)

    def execute(self, operand1, operand2):
        return min(operand1, operand2)


class AverageOperator(Operator):
    def __init__(self):
        super().__init__('@', 1, 'left', 2)

    def execute(self, operand1, operand2):
        return (operand1 + operand2) / 2
