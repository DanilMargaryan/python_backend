import math


def factorial(n: int):
    return math.factorial(n)


def fibonacci(n: int):
    a, b = 0, 1
    for __ in range(n):
        a, b = b, a + b
    return a


def mean(numbers: list):
    return sum(numbers) / len(numbers)
