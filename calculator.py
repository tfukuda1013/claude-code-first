"""シンプルな電卓CLI。Claude Code入門用のサンプルコード。"""

import sys


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("0で割ることはできません")
    return a / b


def power(a: float, b: float) -> float:
    return a ** b


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "^": power,
}


def main() -> None:
    if len(sys.argv) != 4:
        print("使い方: python calculator.py <数値1> <演算子> <数値2>")
        print("例: python calculator.py 3 + 5")
        sys.exit(1)

    a, op, b = sys.argv[1], sys.argv[2], sys.argv[3]

    if op not in OPERATIONS:
        print(f"未対応の演算子です: {op}（使えるのは + - * / ）")
        sys.exit(1)

    result = OPERATIONS[op](float(a), float(b))
    print(f"{a} {op} {b} = {result}")


if __name__ == "__main__":
    main()
