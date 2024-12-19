# main.py

from Calculator import *


def main():
    calculator = Calculator()
    print("Advanced Calculator - Omega Class 2024")
    print("Enter a mathematical expression to calculate or type 'exit' to quit.")
    print("Supported operators: +, -, *, /, ^, !, ~, %, &, $, @, #, (, )")
    print("Examples: 2 + 3 * 4, (2 + 3) * 4, 5!, 2 ^ 3, 10 / 2, 5 $ 3, 5 & 3, 5 @ 3, ~3 + 5, 123#")

    while True:
        expression = input("Enter expression: ").strip()
        if expression.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break
        if not expression:
            continue  # Ignore empty input
        result = calculator.calculate(expression)
        if result is not None:
            print(f"Result: {result}")
        else:
            print("Invalid expression. Please try again.")


if __name__ == "__main__":
    main()
