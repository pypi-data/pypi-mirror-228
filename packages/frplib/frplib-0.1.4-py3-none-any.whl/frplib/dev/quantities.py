from __future__  import annotations

import re

from abc         import abstractmethod
from dataclasses import dataclass
from decimal     import Decimal, Context, ROUND_HALF_UP
from enum        import Enum, auto
from fractions   import Fraction
from typing      import Literal, TypeAlias

from frplib.exceptions import EvaluationError

class Quantity:
    ""
#    @abstractmethod
#    def apply(self, f):
#        "Applies a statistic/function to this quantity."
#        ...

    # Consider arithmetic registry here but for now
    def __add__(self, other):
        symbol_a = isinstance(self, SymbolicQuantity)
        symbol_b = isinstance(other, SymbolicQuantity)

        if symbol_a or symbol_b:
            return symbolic_add(self, other)
        return numeric_add(self, other)

    def __radd__(self, other):
        symbol_a = isinstance(self, SymbolicQuantity)
        symbol_b = isinstance(other, SymbolicQuantity)

        if symbol_a or symbol_b:
            return symbolic_add(other, self)
        return numeric_add(other, self)

# 
#    @abstractmethod
#    def __sub__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rsub__(self, other):
#        ...
# 
#    @abstractmethod
#    def __mul__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rmul__(self, other):
#        ...
# 
#    @abstractmethod
#    def __matmul__(self, other):
#        ...
# 
#    @abstractmethod
#    def __truediv__(self, other):
#        ...
# 
#    @abstractmethod
#    def __floordiv__(self, other):
#        ...
# 
#    @abstractmethod
#    def __mod__(self, other):
#        ...
# 
#    @abstractmethod
#    def __divmod__(self, other):
#        ...
# 
#    @abstractmethod
#    def __pow__(self, other):
#        ...
# 
#    @abstractmethod
#    def __lshift__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rshift__(self, other):
#        ...
# 
#    @abstractmethod
#    def __and__(self, other):
#        ...
# 
#    @abstractmethod
#    def __xor__(self, other):
#        ...
# 
#    @abstractmethod
#    def __or__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rmatmul__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rtruediv__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rfloordiv__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rmod__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rdivmod__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rpow__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rlshift__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rrshift__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rand__(self, other):
#        ...
# 
#    @abstractmethod
#    def __rxor__(self, other):
#        ...
# 
#    @abstractmethod
#    def __ror__(self, other):
#        ...


#
# Numeric Quantities
#

DEFAULT_RATIONAL_DENOM_LIMIT = 1000000000   # Default Decimal -> Fraction conversion

class NumType(Enum):
    INTEGER = auto()
    RATIONAL = auto()
    REAL = auto()

class NumericQuantity(Quantity):
    @abstractmethod
    def __float__(self) -> float:
        ...

@dataclass(frozen=True)
class IntegerQuantity(NumericQuantity):
    type: Literal[NumType.INTEGER] = NumType.INTEGER
    value: int = 0

    def __int__(self):
        return self.value

    def __index__(self):
        return self.value

    def __float__(self) -> float:
        return float(self.value)

@dataclass(frozen=True)
class RationalQuantity(NumericQuantity):
    type: Literal[NumType.RATIONAL] = NumType.RATIONAL
    value: Fraction = Fraction(0)

    def __float__(self) -> float:
        return float(self.value)

    def real(self) -> 'RealQuantity':
        return RealQuantity(value=Decimal(self.value.numerator) / Decimal(self.value.denominator))

@dataclass(frozen=True)
class RealQuantity(NumericQuantity):
    type: Literal[NumType.REAL] = NumType.REAL
    value: Decimal = Decimal('0')

    def __float__(self) -> float:
        return float(self.value)

    def rational(self, limit_denominator=False) -> RationalQuantity:
        x = Fraction(self.value)
        if limit_denominator:
            x = x.limit_denominator(limit_denominator)
        return RationalQuantity(value=x)

Numeric: TypeAlias = IntegerQuantity | RationalQuantity | RealQuantity
Scalar: TypeAlias = int | float | Fraction | Decimal | Numeric | str

#
# Numeric Conversion
#

integer_re = r'(?:0|[1-9][0-9]{0,2}(?:_[0-9]{3})+|[1-9][0-9]*)'  # _ separators allowed
rat_denom = r'/(?:[1-9][0-9]{0,2}(?:_[0-9]{3})+|[1-9][0-9]*)'
decimal = r'\.[0-9]*'
sci_exp = r'[eE][-+]?(?:0|[1-9][0-9]*)'
opt_sign = r'-?'
numeric_re = rf'({opt_sign})({integer_re})(?:({rat_denom})|({decimal}(?:{sci_exp})?)|({sci_exp}))?'

def numeric_from_str(s: str) -> Numeric:
    m = re.match(numeric_re, s.strip())
    if not m:
        raise EvaluationError(f'Could not parse string as a numeric quantity: "{s}"')

    sign, integer, denom, dec_exp, exp = m.groups('')

    if not denom and not dec_exp and not exp:
        return IntegerQuantity(value=int(sign + integer))

    if denom:
        return RationalQuantity(value=Fraction(int(sign + integer), int(denom[1:])))

    if dec_exp:
        return RealQuantity(value=Decimal(sign + integer + dec_exp))

    return RealQuantity(value=Decimal(sign + integer + exp))

def numeric(x: Scalar, no_rationals=False) -> Numeric:
    if isinstance(x, (IntegerQuantity, RationalQuantity, RealQuantity)):
        return x

    if isinstance(x, str):
        return numeric_from_str(x)

    if isinstance(x, int):
        return IntegerQuantity(value=x)

    if isinstance(x, Fraction):           # Check complexity to decide if real?
        value = RationalQuantity(value=x)
        if no_rationals:
            return value.real()
        return value

    return RealQuantity(value=Decimal(x))


#
# Symbolic Quantities
#

@dataclass(frozen=True)
class SymbolicQuantity(Quantity):
    pass

@dataclass(frozen=True)
class SymbolicPolynomial(SymbolicQuantity):
    pass

@dataclass(frozen=True)
class SymbolicRational(SymbolicQuantity):
    pass

@dataclass(frozen=True)
class SymbolicApplication(SymbolicQuantity):
    pass


#
# Quantity Operations
#

def numeric_add(a: Numeric, b: Scalar) -> Numeric:
    if isinstance(b, int):
        return a.__class__(value=a.value + b)
    raise ValueError('temp')

def symbolic_add(a: SymbolicQuantity, b) -> SymbolicQuantity:
    return NotImplemented
