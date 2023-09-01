# UltraCOLOR library v0.1.0
## Table of Contents
- [1. Description](#1-description)
- [2. Features](#2-features)
  - [2.1 Does not require dependencies](#21-does-not-require-dependencies)
  - [2.2 Lightweight](#22-lightweight)
  - [2.3 Easy to use](#23-easy-to-use)
  - [2.4 Accurate color conversion](#24-accurate-color-conversion)
- [3. Installation](#3-installation)
  - [3.1 Install prebuilt package](#31-install-prebuilt-package)
  - [3.2 From source code](#32-from-source-code)
- [4. Supported Color Spaces](#4-supported-color-spaces)

## 1. Description
UltraCOLOR is a Python library that provides functionality for working with different color spaces. It supports RGBA, Hex and HSLA color spaces, allowing for accurate color conversion. The library does not require any third-party dependencies and only utilizes the Python standard library. With UltraCOLOR, you can easily convert colors between different color spaces and perform various operations on them.

## 2. Features
### 2.1 Does not require dependencies
This library **does not require** third party dependencies: *only* the Python >= 3.8 is required
### 2.2 Lightweight
UltraCOLOR is a lightweight library, making it a perfect choice for projects where performance is a key factor.
### 2.3 Easy to use
The library provides a simple and intuitive API, making it easy to perform complex color operations with just a few lines of code.
### 2.4 Accurate color conversion
This is achieved by using the built-in type `Decimal`
```python
from ucolor import ColorRGBA, convert
foo = ColorRGBA(33, 33, 33)
bar = convert.rgba_to_hsla(foo)
baz = convert.hsla_to_rgba(bar)
print(foo == baz) # True
```

## 3. Installation
### 3.1 Install prebuilt package

```console
$ pip3 install ucolor
```
### 3.2 From source code
*NOTE: when installing this way you get the latest version of the library, it may contain bugs or not work at all.*
```console
$ pip3 install git+https://notabug.org/Aserogl/ucolor.git@main
```

## 4. Supported Color Spaces
- [x] RGBA
- [x] Hex
- [x] HSLA
- [ ] HSVA
