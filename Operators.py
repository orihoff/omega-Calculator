from abc import ABC, abstractmethod

class Operator(ABC):
    def __init__(self, symbol, precedence, associativity):
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity

    @abstractmethod
    def execute(self, operand1, operand2=None):
        """
        Execute the operator's operation on operands.
        operand1: The first operand.
        operand2: The second operand (optional for some operators).
        :return: The result of the operation.
        """
        pass


class AdditionOperator(Operator):
    def __init__(self):
        super().__init__('+', 2, 'left')

    def execute(self, operand1, operand2):
        return operand1 + operand2


class SubtractionOperator(Operator):
    def __init__(self):
        super().__init__('-', 2, 'left')

    def execute(self, operand1, operand2):
        return operand1 - operand2


class MultiplicationOperator(Operator):
    def __init__(self):
        super().__init__('*', 3, 'left')

    def execute(self, operand1, operand2):
        return operand1 * operand2


class DivisionOperator(Operator):
    def __init__(self):
        super().__init__('/', 3, 'left')

    def execute(self, operand1, operand2):
        if operand2 == 0:
            raise ValueError("Division by zero is undefined.")
        return operand1 / operand2


class PowerOperator(Operator):
    def __init__(self):
        super().__init__('^', 4, 'right')

    def execute(self, operand1, operand2):
        return operand1 ** operand2


class FactorialOperator(Operator):
    def __init__(self):
        super().__init__('!', 5, 'left')

    def execute(self, operand1, operand2=None):
        # מימוש חישוב עצרת ידני
        if operand1 < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        result = 1
        for i in range(1, int(operand1) + 1):
            result *= i
        return result


class MaxOperator(Operator):
    def __init__(self):
        super().__init__('$', 1, 'left')

    def execute(self, operand1, operand2):
        return operand1 if operand1 > operand2 else operand2


class MinOperator(Operator):
    def __init__(self):
        super().__init__('&', 1, 'left')

    def execute(self, operand1, operand2):
        return operand1 if operand1 < operand2 else operand2
