from Operators import PowerOperator, AdditionOperator, SubtractionOperator, FactorialOperator

def test_operators():
    """
    Test various operators and demonstrate their functionality.
    """
    # Power Operator
    power = PowerOperator()
    print(f"2 ^ 3 = {power.execute(2, 3)}")  # Output: 8

    # Addition Operator
    addition = AdditionOperator()
    print(f"5 + 7 = {addition.execute(5, 7)}")  # Output: 12

    # Subtraction Operator
    subtraction = SubtractionOperator()
    print(f"10 - 4 = {subtraction.execute(10, 4)}")  # Output: 6

    # Factorial Operator
    factorial = FactorialOperator()
    print(f"5! = {factorial.execute(5)}")  # Output: 120


if __name__ == "__main__":
    print("Testing Operators:")
    test_operators()
