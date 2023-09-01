"""
This module provides the ColorRGBA class for representing colors in RGBA format.

The ColorRGBA class includes methods for color manipulation such as linear
interpolation (lerp) and mixing.

It also includes properties for accessing and modifying individual color
components (red, green, blue, alpha).

Additionally, the module provides predefined colors as class properties
(white, black, red, etc.).
"""

__all__ = ["ColorRGBA"]

from typing import Self
from .utils import _in_range, _lerp


class ColorRGBA:
    """
    A class to represent RGBA color.

    Attributes:
    r: float
        Red component of the color, in the range 0-255.
    g: float
        Green component of the color, in the range 0-255.
    b: float
        Blue component of the color, in the range 0-255.
    a: float = 1
        Alpha (transparency) component of the color, in the range 0-1.

    Methods:
    __str__(self) -> str

    __repr__(self) -> str

    __eq__(self, other: ColorRGBA) -> bool

    lerp(cls, a: ColorRGBA, b: ColorRGBA, t: float) -> ColorRGBA

    mix(cls, a: ColorRGBA, b: ColorRGBA) -> ColorRGBA
    """

    def __init__(self, r: float, g: float, b: float, a: float = 1) -> None:
        self.__r = r
        self.__g = g
        self.__b = b
        self.__a = a
        if not self.__isValid():
            raise ValueError("RGB components must be in 0..255 "
                             "and Alpha in 0..1")

    # magic methods
    def __str__(self) -> str:
        """ Returns a string representation of the color """
        return f"r={self.__r}, g={self.__g}, b={self.__b}, a={self.__a}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the color, suitable for debugging 
        """
        return (f"<ColorRGBA(r={self.__r}, g={self.__g}, b={self.__b}, "
                f"a={self.__a}) at {hex(id(self))}>")

    def __eq__(self, other: Self) -> bool:
        """ Checks if this color is equal to another color """
        return self.__r == other.r and self.__g == other.g \
               and self.__b == other.b

    # private methods
    def __isValid(self) -> bool:
        return _in_range(self.__r, 0, 255) \
               and _in_range(self.__g, 0, 255) \
               and _in_range(self.__b, 0, 255) \
               and _in_range(self.__a, 0, 1)

    # colors
    @classmethod
    @property
    def white(cls) -> Self:
        return ColorRGBA(255, 255, 255)

    @classmethod
    @property
    def black(cls) -> Self:
        return ColorRGBA(0, 0, 0)

    @classmethod
    @property
    def red(cls) -> Self:
        return ColorRGBA(255, 0, 0)

    @classmethod
    @property
    def orange(cls) -> Self:
        return ColorRGBA(255, 133, 0)

    @classmethod
    @property
    def yellow(cls) -> Self:
        return ColorRGBA(255, 255, 0)

    @classmethod
    @property
    def green(cls) -> Self:
        return ColorRGBA(0, 255, 0)

    @classmethod
    @property
    def blue(cls) -> Self:
        return ColorRGBA(0, 180, 255)

    @classmethod
    @property
    def darkBlue(cls) -> Self:
        return ColorRGBA(0, 50, 255)

    @classmethod
    @property
    def purple(cls) -> Self:
        return ColorRGBA(100, 0, 200)

    # rgba components
    @property
    def r(self) -> float:
        """ Red RGBA component """
        return self.__r

    @r.setter
    def r(self, new_value: int) -> None:
        if not _in_range(new_value, 0, 255):
            raise ValueError("RGB components must be in 0..255!")
        self.__r = new_value

    @property
    def g(self) -> float:
        """ Green RGBA component """
        return self.__g

    @g.setter
    def g(self, new_value: int) -> None:
        if not _in_range(new_value, 0, 255):
            raise ValueError("RGB components must be in 0..255!")
        self.__g = new_value

    @property
    def b(self) -> float:
        """ Blue RGBA component """
        return self.__b

    @b.setter
    def b(self, new_value: int) -> None:
        if not _in_range(new_value, 0, 255):
            raise ValueError("RGB components must be in 0..255!")
        self.__b = new_value

    @property
    def a(self) -> float:
        """ RGBA Alpha component """
        return self.__a

    @a.setter
    def a(self, new_value: int) -> None:
        if not _in_range(new_value, 0, 1):
            raise ValueError("Alpha must be in 0..255!")
        self.__a = new_value

    # lerp
    @classmethod
    def lerp(cls, a: Self, b: Self, t: float) -> Self:
        """ Mixes two colors with a certain factor and returns the result """
        return ColorRGBA(
            _lerp(a.r, b.r, t),
            _lerp(a.g, b.g, t),
            _lerp(a.b, b.b, t),
            _lerp(a.a, b.a, t),
        )

    @classmethod
    def mix(cls, a: Self, b: Self) -> Self:
        """ Mixes two colors with a factor of 0.5 and returns the result """
        return ColorRGBA.lerp(a, b, 0.5)
