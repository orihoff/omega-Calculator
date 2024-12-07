# calculator.py

from ExpressionParser import ExpressionParser
from exceptions import CalculatorException, InvalidTokenException, MissingOperandException
from Operators import Operator


class Calculator:
    def __init__(self):
        """
        Initialize the calculator with an expression parser.
        """
        self.parser = ExpressionParser()

    def calculate(self, expression):
        """
        Evaluate the given mathematical expression.

        :param expression: str
            The mathematical expression to evaluate.
        :return: float
            The result of the calculation.
        """
        try:
            # Step 1: Parse the expression into postfix notation
            postfix = self.parser.parse_expression(expression)

            # Step 2: Evaluate the postfix expression
            result = self.evaluate_postfix(postfix)

            return result
        except CalculatorException as e:
            print(e)  # Exception already includes the error message and marker
            return None  # Return None in case of an error
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def evaluate_postfix(self, postfix):
        """
        Evaluate a mathematical expression in postfix notation.

        :param postfix: list
            The postfix tokenized expression.
        :return: float
            The result of the calculation.
        """
        stack = []
        operators = self.parser.operators

        for token in postfix:
            if isinstance(token, float):
                # Operand: Push it onto the stack
                stack.append(token)
            elif isinstance(token, str) and token in operators:
                operator = operators[token]

                if operator.arity == 1:
                    if not stack:
                        raise MissingOperandException(operator.symbol)
                    operand = stack.pop()
                    result = operator.execute(operand)
                elif operator.arity == 2:
                    if len(stack) < 2:
                        raise MissingOperandException(operator.symbol)
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    result = operator.execute(operand1, operand2)
                else:
                    raise CalculatorException(f"Unsupported operator arity: {operator.arity}")

                # Push the result back onto the stack
                stack.append(result)
            else:
                raise InvalidTokenException(token)

        # The result should be the only item left in the stack
        if len(stack) != 1:
            raise CalculatorException("Invalid expression structure.")

        return stack.pop()
