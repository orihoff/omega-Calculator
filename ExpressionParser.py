import re
from Operators import (
    AdditionOperator,
    SubtractionOperator,
    MultiplicationOperator,
    DivisionOperator,
    PowerOperator,
    FactorialOperator,
    NegationOperator,
    ModuloOperator,
    MaxOperator,
    MinOperator,
    AverageOperator
)
from exceptions import InvalidTokenException, InvalidExpressionException

class ExpressionParser:
    def __init__(self):
        """
        Initialize the expression parser with supported operators.
        """
        self.operators = {
            '+': AdditionOperator(),
            '-': SubtractionOperator(),
            '*': MultiplicationOperator(),
            '/': DivisionOperator(),
            '^': PowerOperator(),
            '!': FactorialOperator(),
            '~': NegationOperator(),
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
        # Adjust the token pattern to handle the tilde operator
        token_pattern = (
            r'(?<![\w.])~\d+\.?\d*'       # Match tilde followed by a number
            r'|\d+\.?\d*'                 # Numbers
            r'|[' + re.escape(''.join(self.operator_symbols - {'~'})) + r'\(\)]'  # Other operators and parentheses
        )
        tokens = re.findall(token_pattern, expression.replace(' ', ''))
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
        tokens = self.tokenize(expression)
        output_queue = []
        operator_stack = []
        previous_token_type = None

        for token in tokens:
            if self.is_number(token):
                # Numbers go directly to the output queue
                output_queue.append(float(token))
                previous_token_type = 'number'
            elif token.startswith('~'):
                # Handle the tilde operator immediately before a number
                number_part = token[1:]
                if not self.is_number(number_part):
                    raise InvalidExpressionException(f"Invalid use of '~' operator with '{number_part}'.")
                # Apply the negation and push the result
                negated_number = -float(number_part)
                output_queue.append(negated_number)
                previous_token_type = 'number'
            elif self.is_operator(token):
                # Regular operators
                o1 = self.operators.get(token)
                if not o1:
                    raise InvalidTokenException(token)
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
                operator_stack.append(token)
                previous_token_type = 'left_parenthesis'
            elif token == self.right_parenthesis:
                while operator_stack and operator_stack[-1] != self.left_parenthesis:
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise InvalidExpressionException("Mismatched parentheses.")
                operator_stack.pop()  # Pop the left parenthesis
                previous_token_type = 'right_parenthesis'
            else:
                raise InvalidTokenException(token)

        # Pop all remaining operators
        while operator_stack:
            top = operator_stack.pop()
            if top in (self.left_parenthesis, self.right_parenthesis):
                raise InvalidExpressionException("Mismatched parentheses.")
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
