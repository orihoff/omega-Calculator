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
    AverageOperator,
    DigitSumOperator
)
from exceptions import (
    InvalidTokenException,
    InvalidExpressionException,
    ConsecutiveTildesException,
    MismatchedParenthesesException,
    MissingOperandException,
    InvalidCharacterException
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
            'u~': TildeOperator(),     # Unary tilde operator
            '*': MultiplicationOperator(),
            '/': DivisionOperator(),
            '^': PowerOperator(),
            '!': FactorialOperator(),
            '%': ModuloOperator(),
            '$': MaxOperator(),
            '&': MinOperator(),
            '@': AverageOperator(),
            '#': DigitSumOperator(),  # Adding the DigitSumOperator
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
            r'|.'  # Match any single character (to catch invalid characters)
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
        if not expression.strip():
            raise InvalidExpressionException("Expression cannot be empty or whitespace only.", expression, 0)

        tokens = self.tokenize(expression)
        output_queue = []
        operator_stack = []
        previous_token_type = None

        current_position = 0  # Track position within the expression

        for i, token in enumerate(tokens):
            token_position = expression.find(token, current_position)
            current_position = token_position + len(token)

            if self.is_number(token):
                output_queue.append(float(token))
                previous_token_type = 'number'
            elif token in self.operator_symbols:
                if token == '~' and previous_token_type in ('operator', None):
                    # Check for consecutive tildes
                    if operator_stack and operator_stack[-1] in ('u~', '~'):
                        raise ConsecutiveTildesException(expression, token_position)

                    token = 'u~'
                    operator_stack.append(token)
                    previous_token_type = 'operator'
                    continue

                if token in ('-', '~') and previous_token_type in (None, 'operator', 'left_parenthesis'):
                    token = 'u-' if token == '-' else 'u~'
                    operator_stack.append(token)
                    previous_token_type = 'operator'
                    continue

                o1 = self.operators.get(token)
                if not o1:
                    raise InvalidTokenException(token, expression, token_position)

                # Handle factorial (`!`) and digit sum (`#`) separately
                if token in ('!', '#'):
                    if previous_token_type != 'number':
                        raise InvalidExpressionException(
                            f"Operator '{token}' must follow a number.",
                            expression,
                            token_position
                        )
                    while operator_stack and operator_stack[-1] not in ('(', ')'):
                        top = operator_stack[-1]
                        o2 = self.operators.get(top)
                        if o2 and o2.precedence > o1.precedence:
                            output_queue.append(operator_stack.pop())
                        else:
                            break
                    output_queue.append(token)
                    previous_token_type = 'operator'
                    continue

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
                if previous_token_type == 'left_parenthesis':
                    raise InvalidExpressionException(
                        "Empty parentheses are not allowed.", expression, token_position
                    )
                while operator_stack and operator_stack[-1] != self.left_parenthesis:
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise MismatchedParenthesesException(expression, token_position)
                operator_stack.pop()
                previous_token_type = 'right_parenthesis'
            elif token in ('u-', 'u~'):
                if previous_token_type in ('number', 'right_parenthesis'):
                    raise MissingOperandException("Missing operand for operator: {}".format(token), expression, token_position)
                operator_stack.append(token)
                previous_token_type = 'operator'
            else:
                raise InvalidTokenException(token, expression, token_position)

        while operator_stack:
            top = operator_stack.pop()
            if top in (self.left_parenthesis, self.right_parenthesis):
                raise MismatchedParenthesesException(expression, current_position)
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