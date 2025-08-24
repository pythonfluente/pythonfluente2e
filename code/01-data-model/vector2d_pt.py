"""
vector2d.py: classe simples usando métodos especiais

Classe simplificada por motivos didáticos.
Falta tratamento de erro nos métodos `__add__` e `__mul__`.

Em outras partes do livro faremos esse código ficar
mais robusto e flexível.

Soma::

    >>> v1 = Vector(2, 4)
    >>> v2 = Vector(2, 1)
    >>> v1 + v2
    Vector(4, 5)

Valor absoluto ou módulo::

    >>> v = Vector(3, 4)
    >>> abs(v)
    5.0

Multiplicação escalar::

    >>> v * 3
    Vector(9, 12)
    >>> abs(v * 3)
    15.0

"""

import math

class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x!r}, {self.y!r})'

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
