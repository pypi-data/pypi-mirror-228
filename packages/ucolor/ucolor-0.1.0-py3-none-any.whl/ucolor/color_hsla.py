"""
This module provides the ColorHSLA class for representing colors in HSLA format.

The ColorHSLA class includes methods for color manipulation such as linear
interpolation (lerp) and mixing.

It also includes properties for accessing and modifying individual color
components (hue, saturation, lightness, alpha).

Additionally, the module provides predefined colors as class properties
(white, black, red, etc.).
"""

__all__ = ["ColorHSLA"]

from typing import Self
from .utils import _in_range, _lerp


class ColorHSLA:
    """
    A class to represent HSLA color.

    Attributes:
    h: float
        Hue component of the color, in the range 0-360.
    s: float
        Saturation component of the color, in the range 0-100.
    l: float
        Ligthness component of the color, in the range 0-100.
    a: float = 1
        Alpha (transparency) component of the color, in the range 0-1.

    Methods:
    __str__(self) -> str

    __repr__(self) -> str

    __eq__(self, other: ColorHSLA) -> bool

    lerp(cls, a: ColorHSLA, b: ColorHSLA, t: float) -> ColorHSLA

    mix(cls, a: ColorHSLA, b: ColorHSLA) -> ColorHSLA
    """

    def __init__(self, h: float, s: float, l: float, a: float = 1) -> None:
        self.__h = h
        self.__s = s
        self.__l = l
        self.__a = a
        if not self.__isValid():
            raise ValueError("Hue must be in 0..360, "
                             "Saturation and Lightness must be in 0..100 and "
                             "Alpha in 0..1")

    # magic methods
    def __str__(self) -> str:
        """ Returns a string representation of the color """
        return f"h={self.__h}, s={self.__s}, l={self.__l}, a={self.__a}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the color, suitable for debugging
        """
        return (f"<ColorHSLA(h={self.__h}, s={self.__s}, l={self.__l}, "
                f"a={self.__a}) at {hex(id(self))}>")

    def __eq__(self, other: Self) -> bool:
        """ Checks if this color is equal to another color """
        return self.__h == other.__h and self.__s == other.s \
               and self.__l == other.l

    # private methods
    def __isValid(self) -> bool:
        return _in_range(self.__h, 0, 360) \
               and _in_range(self.__s, 0, 100) \
               and _in_range(self.__l, 0, 100) \
               and _in_range(self.__a, 0, 1)

    # colors
    @classmethod
    @property
    def white(cls) -> Self:
        return ColorHSLA(0, 0, 100)

    @classmethod
    @property
    def black(cls) -> Self:
        return ColorHSLA(0, 0, 0)

    @classmethod
    @property
    def red(cls) -> Self:
        return ColorHSLA(0, 100, 50)

    @classmethod
    @property
    def orange(cls) -> Self:
        return ColorHSLA(31, 100, 50)

    @classmethod
    @property
    def yellow(cls) -> Self:
        return ColorHSLA(60, 100, 50)

    @classmethod
    @property
    def green(cls) -> Self:
        return ColorHSLA(120, 100, 50)

    @classmethod
    @property
    def blue(cls) -> Self:
        return ColorHSLA(198, 100, 50)

    @classmethod
    @property
    def darkBlue(cls) -> Self:
        return ColorHSLA(228, 100, 50)

    @classmethod
    @property
    def purple(cls) -> Self:
        return ColorHSLA(270, 100, 39)

    # hsla components
    @property
    def h(self) -> float:
        """ Hue HSLA component """
        return self.__h

    @h.setter
    def h(self, new_value: int) -> None:
        if not _in_range(new_value, 0, 360):
            raise ValueError("Hue must be in 0..360")
        self.__h = new_value

    @property
    def s(self) -> float:
        """ Saturation HSLA component """
        return self.__s

    @s.setter
    def s(self, new_value: int) -> None:
        if not _in_range(new_value, 0, 100):
            raise ValueError("Saturation must be in 0..100")
        self.__s = new_value

    @property
    def l(self) -> float:
        """ Lightness HSLA component """
        return self.__l

    @l.setter
    def l(self, new_value: int) -> None:
        if not _in_range(new_value, 0, 100):
            raise ValueError("Lightness must be in 0..100")
        self.__l = new_value

    @property
    def a(self) -> float:
        """ HSLA Alpha component """
        return self.__a

    @a.setter
    def a(self, new_value: int) -> None:
        if not _in_range(new_value, 0, 1):
            raise ValueError("Alpha must be in 0..1!")
        self.__a = new_value

    # lerp
    @classmethod
    def lerp(cls, a: Self, b: Self, t: float) -> Self:
        """ Mixes two colors with a certain factor and returns the result """
        return ColorHSLA(
            _lerp(a.h, b.h, t),
            _lerp(a.s, b.s, t),
            _lerp(a.l, b.l, t),
            _lerp(a.a, b.a, t)
        )

    @classmethod
    def mix(cls, a: Self, b: Self) -> Self:
        """ Mixes two colors with a factor of 0.5 and returns the result """
        return ColorHSLA.lerp(a, b, 0.5)
