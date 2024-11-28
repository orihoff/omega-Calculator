from ExpressionParser import ExpressionParser
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
        except Exception as e:
            print(f"Error: {e}")
            return None  # Return None in case of an error

    def evaluate_postfix(self, postfix):
        """
        Evaluate a mathematical expression in postfix notation.

        :param postfix: list
            The postfix tokenized expression.
        :return: float
            The result of the calculation.
        """
        stack = []

        for token in postfix:
            if isinstance(token, float):
                # Operand: Push it onto the stack
                stack.append(token)
            elif isinstance(token, str) and token in self.parser.operators:
                # Operator: Apply it to the top operands on the stack
                operator = self.parser.operators[token]

                if operator.symbol == '!':  # Unary operator (factorial)
                    operand = stack.pop()
                    result = operator.execute(operand)
                else:  # Binary operators (e.g., +, -, *, /)
                    operand2 = stack.pop()  # Correct order: operand2 comes first
                    operand1 = stack.pop()
                    result = operator.execute(operand1, operand2)

                # Push the result back onto the stack
                stack.append(result)
            else:
                raise ValueError(f"Invalid token: {token}")

        # The result should be the only item left in the stack
        if len(stack) != 1:
            raise ValueError("Invalid expression structure.")

        return stack.pop()
