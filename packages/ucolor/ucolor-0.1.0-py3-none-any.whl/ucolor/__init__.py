"""
UltraCOLOR is a Python library that provides functionality for working with
different color spaces. It supports RGBA, Hex and HSLA color spaces, allowing
for accurate color conversion. The library does not require any third-party
dependencies and only utilizes the Python standard library. With UltraCOLOR,
you can easily convert colors between different color spaces and perform various
operations on them.
"""

__all__ = ["convert", "ColorRGBA", "ColorHSLA", "default_term_color"]

from . import convert
from .color_rgba import ColorRGBA
from .color_hsla import ColorHSLA


default_term_color = "\033[0m"
