import re
from Operators import AdditionOperator, SubtractionOperator, MultiplicationOperator, DivisionOperator, PowerOperator, FactorialOperator, MaxOperator, MinOperator
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
            '$': MaxOperator(),
            '&': MinOperator(),
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
        token_pattern = r'\d+\.?\d*|[' + re.escape(''.join(self.operator_symbols)) + r'\(\)]'
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
        tokens = self.tokenize(expression)
        output_queue = []
        operator_stack = []

        for token in tokens:
            if self.is_number(token):
                # Numbers go directly to the output queue
                output_queue.append(float(token))
            elif self.is_operator(token):
                # Handle operators
                o1 = self.operators[token]
                while operator_stack and operator_stack[-1] != self.left_parenthesis:
                    o2 = self.operators[operator_stack[-1]]
                    if (o1.associativity == 'left' and o1.precedence <= o2.precedence) or \
                       (o1.associativity == 'right' and o1.precedence < o2.precedence):
                        output_queue.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(token)
            elif token == self.left_parenthesis:
                operator_stack.append(token)
            elif token == self.right_parenthesis:
                while operator_stack and operator_stack[-1] != self.left_parenthesis:
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise InvalidExpressionException("Mismatched parentheses.")
                operator_stack.pop()
            else:
                raise InvalidTokenException(token)

        # Pop all remaining operators
        while operator_stack:
            if operator_stack[-1] in (self.left_parenthesis, self.right_parenthesis):
                raise InvalidExpressionException("Mismatched parentheses.")
            output_queue.append(operator_stack.pop())

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
