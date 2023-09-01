__all__ = ["_clamp", "_lerp", "_in_range", "_to_decimal"]

from decimal import Decimal


def _clamp(value: float, min_value: float, max_value: float) -> float:
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def _lerp(a: float, b: float, t: float) -> float:
    t = _clamp(t, 0, 1)
    _a = _to_decimal(a)
    _b = _to_decimal(b)
    return float(_a + (_b - _a) * _to_decimal(t))


def _in_range(num: float, start: float, end: float) -> bool:
    return num >= start and num <= end


def _to_decimal(number: float) -> Decimal:
    return Decimal(str(number))
