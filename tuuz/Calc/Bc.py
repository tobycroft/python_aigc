from decimal import Decimal, ROUND_HALF_UP


def to_decimal(number):
    if isinstance(number, int):
        return Decimal(number)
    elif isinstance(number, float):
        return Decimal(str(number))
    elif isinstance(number, str):
        try:
            return Decimal(number)
        except:
            return Decimal(0)
    elif isinstance(number, Decimal):
        return number
    else:
        try:
            return Decimal(str(number))
        except:
            return Decimal(0)


def add(num1, num2):
    return to_decimal(num1) + to_decimal(num2)


def sum(num1, num2):
    return add(num1, num2)


def min(num1, num2):
    return to_decimal(num1) - to_decimal(num2)


def mul(num1, num2):
    return to_decimal(num1) * to_decimal(num2)


def div(num1, num2):
    try:
        return to_decimal(num1) / to_decimal(num2)
    except ZeroDivisionError:
        return Decimal(0)


def pow(num1, num2):
    return to_decimal(num1) ** to_decimal(num2)


def round(num1, round_to):
    return to_decimal(num1).quantize(Decimal(str(10 ** -round_to)), rounding=ROUND_HALF_UP)


def div_round(num1, num2, round_to):
    return (to_decimal(num1) / to_decimal(num2)).quantize(Decimal(str(10 ** -round_to)), rounding=ROUND_HALF_UP)


def abs(num1):
    return abs(to_decimal(num1))


def neg(num1):
    return -to_decimal(num1)


def mod(num1, num2):
    return to_decimal(num1) % to_decimal(num2)
