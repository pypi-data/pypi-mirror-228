"""
This module provides various color conversion utilities.
It includes functions to convert:
- HSLA to RGBA
- Hex to RGBA
- RGBA to HSLA
- Hex to HSLA
- RGBA to Hex
- HSLA to Hex
- RGBA to ANSI
- HSLA to ANSI
- Hex to ANSI

Each function takes in a color in one format and returns it in another.
The color formats supported are HSLA, RGBA and HEX.
"""

__all__ = ["hsla_to_rgba", "hex_to_rgba", "rgba_to_hsla", "hex_to_hsla",
           "rgba_to_hex", "hsla_to_hex", "rgba_to_ansi", "hsla_to_ansi",
           "hex_to_ansi"]

from .color_rgba import ColorRGBA
from .color_hsla import ColorHSLA
from .utils import _to_decimal


# toRgba
def hsla_to_rgba(hsla: ColorHSLA) -> ColorRGBA:
    h, s, l = (_to_decimal(hsla.h), _to_decimal(hsla.s) / 100,
               _to_decimal(hsla.l) / 100)
    c = (1 - abs(l * 2 - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    r = g = b = 0
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x
    return ColorRGBA(
        float((m + r) * 255),
        float((m + g) * 255),
        float((m + b) * 255),
        hsla.a
    )


def hex_to_rgba(hex_value: str) -> ColorRGBA:
    if len(hex_value) != 6:
        raise ValueError("Invalid hex number")
    try:
        r = int(hex_value[:2], 16)
        g = int(hex_value[2:4], 16)
        b = int(hex_value[4:], 16)
    except ValueError as e:
        raise ValueError("Invalid hex number") from e
    return ColorRGBA(r, g, b)


# toHsla
def rgba_to_hsla(rgba: ColorRGBA) -> ColorHSLA:
    r = _to_decimal(rgba.r) / 255
    g = _to_decimal(rgba.g) / 255
    b = _to_decimal(rgba.b) / 255

    max_value = max(r, g, b)
    min_value = min(r, g, b)
    delta = max_value - min_value

    # Calculate hue
    if delta == 0:
        h = 0
    elif max_value == r:
        h = ((g - b) / delta) % 6
    elif max_value == g:
        h = (b - r) / delta + 2
    else:
        h = (r - g) / delta + 4
    h *= 60

    # Calculate lightness
    l = (max_value + min_value) / 2

    # Calculate saturation
    if delta == 0:
        s = 0
    else:
        s = delta / (1 - abs(l * 2 - 1))

    return ColorHSLA(float(h), float(s * 100), float(l * 100), rgba.a)


def hex_to_hsla(hex_value: str) -> ColorHSLA:
    return rgba_to_hsla(hex_to_rgba(hex_value))


# toHex
def rgba_to_hex(rgba: ColorRGBA) -> str:
    return f"{int(rgba.r):02x}{int(rgba.g):02x}{int(rgba.b):02x}"


def hsla_to_hex(hsla: ColorHSLA) -> str:
    return rgba_to_hex(hsla_to_rgba(hsla))


# toAnsi
def rgba_to_ansi(color: ColorRGBA) -> str:
    r = int(color.r)
    g = int(color.g)
    b = int(color.b)
    return f"\033[38;2;{r};{g};{b}m"


def hsla_to_ansi(hsla: ColorHSLA) -> str:
    return rgba_to_ansi(hsla_to_rgba(hsla))


def hex_to_ansi(hex_value: str) -> str:
    return rgba_to_ansi(hex_to_rgba(hex_value))
