from decimal import Decimal, ROUND_HALF_UP


def add(num1, num2):
    return Decimal(num1) + Decimal(num2)


def sum(num1, num2):
    return add(num1, num2)


def min(num1, num2):
    return Decimal(num1) - Decimal(num2)


def mul(num1, num2):
    return Decimal(num1) * Decimal(num2)


def div(num1, num2):
    return Decimal(num1) / Decimal(num2)


def pow(num1, num2):
    return Decimal(num1) ** Decimal(num2)


def round(num1, round_to):
    return Decimal(num1).quantize(Decimal(str(10 ** -round_to)), rounding=ROUND_HALF_UP)


def div_round(num1, num2, round_to):
    return (Decimal(num1) / Decimal(num2)).quantize(Decimal(str(10 ** -round_to)), rounding=ROUND_HALF_UP)


def neg(num1):
    return -abs(num1)


def mod(num1, num2):
    return Decimal(num1) % Decimal(num2)
