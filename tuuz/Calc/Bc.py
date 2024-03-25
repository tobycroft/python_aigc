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


def bc_add(num1, num2):
    return to_decimal(num1) + to_decimal(num2)


def bc_sum(num1, num2):
    return bc_add(num1, num2)


def bc_min(num1, num2):
    return to_decimal(num1) - to_decimal(num2)


def bc_mul(num1, num2):
    return to_decimal(num1) * to_decimal(num2)


def bc_div(num1, num2):
    try:
        return to_decimal(num1) / to_decimal(num2)
    except ZeroDivisionError:
        return Decimal(0)


def bc_pow(num1, num2):
    return to_decimal(num1) ** to_decimal(num2)


def bc_round(num1, round_to):
    return to_decimal(num1).quantize(Decimal(str(10 ** -round_to)), rounding=ROUND_HALF_UP)


def bc_div_round(num1, num2, round_to):
    return (to_decimal(num1) / to_decimal(num2)).quantize(Decimal(str(10 ** -round_to)), rounding=ROUND_HALF_UP)


def bc_abs(num1):
    return abs(to_decimal(num1))


def bc_neg(num1):
    return -to_decimal(num1)


def bc_mod(num1, num2):
    return to_decimal(num1) % to_decimal(num2)
