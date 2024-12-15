import re
from Operators import (
    AdditionOperator,
    SubtractionOperator,
    MultiplicationOperator,
    DivisionOperator,
    PowerOperator,
    FactorialOperator,
    UnaryMinusOperator,
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
    InvalidCharacterException,
    FactorialFloatException
)


class ExpressionParser:
    def __init__(self):
        """
        Initialize the expression parser with supported operators.
        """
        self.operators = {
            '+': AdditionOperator(),
            '-': SubtractionOperator(),
            'u-': UnaryMinusOperator(),
            '~': TildeOperator(),
            'u~': TildeOperator(),
            '*': MultiplicationOperator(),
            '/': DivisionOperator(),
            '^': PowerOperator(),
            '!': FactorialOperator(),
            '%': ModuloOperator(),
            '$': MaxOperator(),
            '&': MinOperator(),
            '@': AverageOperator(),
            '#': DigitSumOperator(),
        }
        self.operator_symbols = set(self.operators.keys())
        self.postfix_operators = {'!'}
        self.left_parenthesis = '('
        self.right_parenthesis = ')'

    def tokenize(self, expression):
        """
        Tokenize a mathematical expression into numbers, operators, and parentheses.
        """
        expression = expression.replace(' ', '')
        token_pattern = (
            r'\d+\.?\d*'
            r'|[' + re.escape(''.join(self.operator_symbols)) + r'\(\)]'
            r'|.'
        )
        tokens = re.findall(token_pattern, expression)

        # Check for consecutive tildes
        for i in range(len(tokens) - 1):
            if tokens[i] == '~' and tokens[i + 1] == '~':
                raise ConsecutiveTildesException(expression, expression.find('~~') + 1)

        return tokens

    def is_operator(self, token):
        return token in self.operator_symbols

    def is_number(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def wrap_negatives(self, tokens):
        """
        Identifies and processes unary minus signs in the tokenized expression.
        """
        new_tokens = []
        i = 0

        # Handle leading sequence of unary minuses
        while i < len(tokens) and tokens[i] == '-':
            new_tokens.append('u-')
            i += 1

        # Process the rest of the tokens
        while i < len(tokens):
            token = tokens[i]
            if token == '-':
                is_unary = tokens[i - 1] in self.operator_symbols or tokens[i - 1] == self.left_parenthesis
                if is_unary:
                    new_tokens.append(self.left_parenthesis)
                    while i < len(tokens) and tokens[i] == '-':
                        new_tokens.append('u-')
                        i += 1
                    if i < len(tokens) and (self.is_number(tokens[i]) or tokens[i] == self.left_parenthesis):
                        new_tokens.append(tokens[i])
                        new_tokens.append(self.right_parenthesis)
                        i += 1
                    else:
                        raise InvalidExpressionException(
                            f"Invalid token sequence after unary minus: '{tokens[i]}'",
                            ''.join(tokens), i
                        )
                else:
                    new_tokens.append(token)
                    i += 1
            else:
                new_tokens.append(token)
                i += 1

        return new_tokens

    def parse_expression(self, expression):
        if not expression.strip():
            raise InvalidExpressionException("Expression cannot be empty or whitespace only.", expression, 0)

        tokens = self.tokenize(expression)
        tokens = self.wrap_negatives(tokens)

        output_queue = []
        operator_stack = []
        previous_token_type = None
        current_position = 0

        for i, token in enumerate(tokens):
            token_str = str(token)
            token_position = expression.find(token_str, current_position)
            current_position = token_position + len(token_str)

            if self.is_number(token):
                output_queue.append(float(token))
                previous_token_type = 'number'
            elif token == '~':
                if i + 1 >= len(tokens) or not (self.is_number(tokens[i + 1]) or tokens[i + 1] in ('-', '(')):
                    raise InvalidExpressionException(
                        f"Tilde ('~') must be followed by a number, a minus sign, or an opening parenthesis.",
                        expression,
                        token_position
                    )
                operator_stack.append(token)
                previous_token_type = 'operator'
            elif token in self.postfix_operators:
                if previous_token_type not in ('number', 'right_parenthesis', 'postfix_operator'):
                    raise InvalidExpressionException(
                        f"Postfix operator '{token}' must follow a number, another postfix operator, or a closing parenthesis.",
                        expression,
                        token_position
                    )

                while operator_stack:
                    top = operator_stack[-1]
                    if top == self.left_parenthesis:
                        break
                    o2 = self.operators.get(top)
                    if not o2:
                        break
                    if (o2.associativity == 'left' and o2.precedence >= self.operators[token].precedence) or \
                       (o2.associativity == 'right' and o2.precedence > self.operators[token].precedence):
                        popped = operator_stack.pop()
                        output_queue.append(popped)
                    else:
                        break

                output_queue.append(token)
                previous_token_type = 'postfix_operator'
            elif self.is_operator(token):
                o1 = self.operators.get(token)
                if not o1:
                    raise InvalidTokenException(token, expression, token_position)

                while operator_stack:
                    top = operator_stack[-1]
                    if top == self.left_parenthesis:
                        break
                    o2 = self.operators.get(top)
                    if not o2:
                        break
                    if (o1.associativity == 'left' and o1.precedence <= o2.precedence) or \
                       (o1.associativity == 'right' and o1.precedence < o2.precedence):
                        popped = operator_stack.pop()
                        output_queue.append(popped)
                    else:
                        break

                operator_stack.append(token)
                previous_token_type = 'operator'

            elif token == self.left_parenthesis:
                operator_stack.append(token)
                previous_token_type = 'left_parenthesis'
            elif token == self.right_parenthesis:
                while operator_stack and operator_stack[-1] != self.left_parenthesis:
                    popped = operator_stack.pop()
                    output_queue.append(popped)
                if not operator_stack:
                    raise MismatchedParenthesesException(expression, token_position)
                operator_stack.pop()
                previous_token_type = 'right_parenthesis'
            else:
                raise InvalidTokenException(token, expression, token_position)

        while operator_stack:
            top = operator_stack.pop()
            if top in (self.left_parenthesis, self.right_parenthesis):
                raise MismatchedParenthesesException(expression, current_position)
            output_queue.append(top)

        return output_queue

    def evaluate_postfix(self, postfix_tokens):
        stack = []
        for token in postfix_tokens:
            if isinstance(token, float):
                stack.append(token)

            elif token in self.operators:
                operator = self.operators[token]
                if operator.arity == 1:
                    a = stack.pop()
                    result = operator.evaluate(a)
                    stack.append(result)

                elif operator.arity == 2:
                    b = stack.pop()
                    a = stack.pop()
                    result = operator.evaluate(a, b)
                    stack.append(result)

            elif token in self.postfix_operators:
                operator = self.operators[token]
                a = stack.pop()
                result = operator.evaluate(a)
                stack.append(result)

        if len(stack) != 1:
            raise InvalidExpressionException("The user input has too many values.", '', 0)
        return stack[0]
