# ExpressionParser.py

import re
from Operators import (
    AdditionOperator,
    SubtractionOperator,
    MultiplicationOperator,
    DivisionOperator,
    PowerOperator,
    FactorialOperator,
    NegationOperator,
    TildeOperator,
    ModuloOperator,
    MaxOperator,
    MinOperator,
    AverageOperator
)
from exceptions import (
    InvalidTokenException,
    InvalidExpressionException,
    ConsecutiveTildesException,
    MismatchedParenthesesException
)


class ExpressionParser:
    def __init__(self):
        """
        Initialize the expression parser with supported operators.
        """
        self.operators = {
            '+': AdditionOperator(),
            '-': SubtractionOperator(),
            'u-': NegationOperator(),  # Unary minus operator
            '~': TildeOperator(),      # Tilde operator
            '*': MultiplicationOperator(),
            '/': DivisionOperator(),
            '^': PowerOperator(),
            '!': FactorialOperator(),
            '%': ModuloOperator(),
            '$': MaxOperator(),
            '&': MinOperator(),
            '@': AverageOperator(),
        }
        self.operator_symbols = set(self.operators.keys())
        self.left_parenthesis = '('
        self.right_parenthesis = ')'

    def tokenize(self, expression):
        """
        Tokenize a mathematical expression into numbers, operators, and parentheses.
        :param expression: str, the mathematical expression.
        :return: list, the tokens.
        """
        # Remove spaces
        expression = expression.replace(' ', '')

        # Regular expression to match numbers and operators
        token_pattern = (
            r'\d+\.?\d*'  # Match numbers (including decimals)
            r'|[' + re.escape(''.join(self.operator_symbols)) + r'\(\)]'  # Operators and parentheses
        )
        tokens = re.findall(token_pattern, expression)
        return tokens

    def is_operator(self, token):
        """
        Check if a token is an operator.
        :param token: str
        :return: bool
        """
        return token in self.operator_symbols

    def parse_expression(self, expression):
        """
        Parse an infix mathematical expression into postfix notation.
        :param expression: str, the infix expression.
        :return: list, the postfix notation tokens.
        """
        # Check for empty or whitespace-only expressions
        if not expression.strip():
            raise InvalidExpressionException("Expression cannot be empty or whitespace only.", expression, 0)

        tokens = self.tokenize(expression)
        output_queue = []
        operator_stack = []
        previous_token_type = None
        consecutive_tilde = False  # Track consecutive tilde operators

        for token in tokens:
            if self.is_number(token):
                # Reset tilde tracker
                consecutive_tilde = False
                # Numbers go directly to the output queue
                output_queue.append(float(token))
                previous_token_type = 'number'
            elif token in self.operator_symbols:
                # Check for invalid placement of tilde
                if token == '~':
                    if previous_token_type == 'number':
                        error_index = expression.find(token)
                        raise InvalidExpressionException(
                            "Invalid placement of '~' operator after a number.", expression, error_index
                        )
                    if consecutive_tilde:
                        error_index = expression.find(token)
                        raise ConsecutiveTildesException(expression, error_index)
                    consecutive_tilde = True

                else:
                    consecutive_tilde = False  # Reset for other operators

                # Handle unary operators
                if token in ('-', '~') and previous_token_type in (None, 'operator', 'left_parenthesis'):
                    if token == '-':
                        token = 'u-'  # Unary minus
                o1 = self.operators.get(token)
                if not o1:
                    error_index = expression.find(token)
                    raise InvalidTokenException(token, expression, error_index)

                while operator_stack:
                    top = operator_stack[-1]
                    if top == self.left_parenthesis:
                        break
                    o2 = self.operators.get(top)
                    if not o2:
                        break
                    if (o1.associativity == 'left' and o1.precedence <= o2.precedence) or \
                       (o1.associativity == 'right' and o1.precedence < o2.precedence):
                        output_queue.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(token)
                previous_token_type = 'operator'
            elif token == self.left_parenthesis:
                consecutive_tilde = False  # Reset tilde tracker
                operator_stack.append(token)
                previous_token_type = 'left_parenthesis'
            elif token == self.right_parenthesis:
                consecutive_tilde = False  # Reset tilde tracker
                while operator_stack and operator_stack[-1] != self.left_parenthesis:
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    error_index = expression.rfind(token)
                    raise MismatchedParenthesesException(expression, error_index)
                operator_stack.pop()  # Pop the left parenthesis
                previous_token_type = 'right_parenthesis'
            else:
                error_index = expression.find(token)
                raise InvalidTokenException(token, expression, error_index)

        # Pop all remaining operators
        while operator_stack:
            top = operator_stack.pop()
            if top in (self.left_parenthesis, self.right_parenthesis):
                error_index = expression.rfind(top)
                raise MismatchedParenthesesException(expression, error_index)
            output_queue.append(top)

        return output_queue

    def is_number(self, token):
        """
        Check if a token is a number.
        :param token: str
        :return: bool
        """
        try:
            float(token)
            return True
        except ValueError:
            return False

    def mark_error(self, expression, index):
        """
        Highlight the position of an error in the expression.
        :param expression: str, the original mathematical expression.
        :param index: int, the index of the error in the expression.
        :return: str, the expression with an error marker.
        """
        if index < 0 or index >= len(expression):
            raise ValueError("Error index is out of bounds.")

        marker = ' ' * index + '^'
        return f"{expression}\n{marker}"
