from Calculator import Calculator

def main():
    calculator = Calculator()
    expressions = [
        "2 + 3 * 4",       # אמור להחזיר 14
        "(2 + 3) * 4",     # אמור להחזיר 20
        "5!",              # אמור להחזיר 120
        "2 ^ 3",           # אמור להחזיר 8
        "10 / 2",          # אמור להחזיר 5
        "5 $ 3",           # אופרטור מקסימום, אמור להחזיר 5
        "5 & 3",           # אופרטור מינימום, אמור להחזיר 3
    ]

    for expr in expressions:
        result = calculator.calculate(expr)
        print(f"{expr} = {result}")

if __name__ == "__main__":
    print("בדיקת מחשבון:")
    main()
