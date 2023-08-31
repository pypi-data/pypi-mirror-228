from __future__ import annotations

from abc         import ABC
from collections import defaultdict
from decimal     import Decimal
from operator    import add
from typing      import cast, Literal, Generator, Union   # ATTN: check collections.abc.Generator ok for 3.9

from frplib.numeric import Numeric, ScalarQ, as_real, as_numeric, show_numeric


#
# Helpers
#

def merge_with(a, b, merge_fn=lambda x, y: y):
    merged = {k: a.get(k, b.get(k)) for k in a.keys() ^ b.keys()}
    merged.update({k: merge_fn(a[k], b[k]) for k in a.keys() & b.keys()})
    return merged

def is_zero(x: Numeric):  # Move to Numeric, should it take ScalarQ?
    return x == 0  # Temp

def show_coef(x: ScalarQ) -> str:
    return show_numeric(as_numeric(x), max_denom=1)


#
# Unique Symbols
#

def symbol_name_generator(base='#x_') -> Generator[str, None, None]:
    script = 0
    while True:
        yield f'{base}{{{script}}}'
        script += 1

gensym = symbol_name_generator()


#
# Generic Symbolic Quantities
#

class Symbolic(ABC):
    def is_pure(self):
        ...

    def pure_value(self):
        ...

    def key_of(self):
        ...


#
# Multinomial Terms
#

class SymbolicMulti(Symbolic):
    "A symbolic multinomial term c a_1^k_1 a_2^k_2 ... a_n^k_n."
    def __init__(self, vars: list[str], powers: list[int], coef: Numeric = 1):
        # if powers too short, those count as 0, so ok; extra powers ignored
        # coef, [''], [1]  acts as a scalar and a *multiplicative* identity
        multi: dict[str, int] = defaultdict(int)
        for var, pow in zip(vars, powers):
            multi[var] += pow
        self.term = multi
        self.coef = coef
        self.key: Union[str, None] = None

    @staticmethod
    def key_str(sym_m: SymbolicMulti) -> str:
        out = [show_coef(sym_m.coef),]
        for var, pow in sorted(sym_m.term.items()):
            if var:
                out.append(f'{var}^{pow}')
        return " ".join(out)

    @property
    def term_order(self) -> str:
        if self.key is None:
            out = []
            for var, pow in sorted(self.term.items()):
                out.append(f'{var}^{pow}')
            self.key = " ".join(out)
        return self.key

    @classmethod
    def symbol(cls, var: str) -> SymbolicMulti:
        return SymbolicMulti([var], [1])

    @classmethod
    def pure(cls, x: ScalarQ = 0):
        return cls([''], [1], as_numeric(x))  # ATTN: Including constants a good idea?

    def is_pure(self) -> bool:
        return len(self.term) == 1 and '' in self.term.keys()

    def pure_value(self):
        if self.is_pure():
            return self.coef
        return None

    def key_of(self):
        return self.key_str(self)

    @classmethod
    def from_terms(cls, multi: dict[str, int], coef: Numeric = 1):
        if is_zero(coef):
            return cls.pure(0)
        x = object.__new__(cls)
        x.term = multi.copy()
        x.coef = coef
        x.key = None
        return x

    def clone(self) -> SymbolicMulti:
        return self.from_terms(self.term, self.coef)

    def __bool__(self) -> bool:
        return False if self.is_pure() and is_zero(self.coef) else True

    def __str__(self) -> str:
        return self.key_str(self)

    def __frplib_repr__(self) -> str:
        return str(self)

    def __mul__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            return self.from_terms(self.term, self.coef * as_real(other))
        if isinstance(other, SymbolicMulti):
            term = merge_with(self.term, other.term, add)
            coef = self.coef * other.coef
            return SymbolicMulti.from_terms(term, coef)
        # Handle other symbolics here
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            return self.from_terms(self.term, as_real(other) * self.coef)
        # Cannot be SymbolicMulti in rul
        # Handle other symbolics here
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if self.is_pure():
                return self.from_terms(self.term, self.coef + as_real(other))
            return SymbolicMultiSum([self, SymbolicMulti.pure(as_numeric(other))])
        if isinstance(other, SymbolicMulti):
            return SymbolicMultiSum([self, other])
        # Handle other symbolics here
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if self.is_pure():
                return self.from_terms(self.term, as_real(other) + self.coef)
            return SymbolicMultiSum([self, SymbolicMulti.pure(as_numeric(other))])
        # Handle other symbolics here
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if self.is_pure():
                return self.from_terms(self.term, self.coef - as_real(other))
            return SymbolicMultiSum([self, SymbolicMulti.pure(as_numeric(-other))])
        if isinstance(other, SymbolicMulti):
            return SymbolicMultiSum([self, -1 * other])
        # Handle other symbolics here
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if self.is_pure():
                return self.from_terms(self.term, as_real(other) - self.coef)
            return SymbolicMultiSum([SymbolicMulti.pure(as_numeric(other)), -1 * self])
        # Handle other symbolics here
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            return self.from_terms(self.term, self.coef / as_real(other))

        if isinstance(other, (SymbolicMulti, SymbolicMultiSum)):
            return symbolic(self, other)

        if isinstance(other, SymbolicMultiRatio):
            return symbolic(self * other.denominator, other.numerator)

        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            return symbolic(SymbolicMulti.pure(other), self)

        if isinstance(other, (SymbolicMulti, SymbolicMultiSum)):
            return symbolic(other, self)

        if isinstance(other, SymbolicMultiRatio):
            return symbolic(other.numerator, self * other.denominator)

        return NotImplemented

    def __pow__(self, n):
        if isinstance(n, int):
            if n == 0:
                return self.pure(1)
            term = self.term.copy()
            for var, pow in term.items():
                term[var] = pow * n if var else pow   # Constant always has power 1
            return self.from_terms(term, self.coef ** n)
        return NotImplemented

symbolic_zero = SymbolicMulti.pure(0)
symbolic_one = SymbolicMulti.pure(1)


#
# Sums of Multinomial Terms
#

class SymbolicMultiSum(Symbolic):
    "A sum of symbolic multinomial terms sum_i c_i a_i1^k_1 a_i2^k_2 ... a_in^k_n."
    def __init__(self, multis: list[SymbolicMulti]) -> None:
        terms = self.combine_terms(multis)
        if not terms:
            self.terms = [symbolic_zero]
        else:
            self.terms = sorted(terms, key=lambda t: t.term_order)

    @staticmethod
    def key_str(multi_sum: SymbolicMultiSum) -> str:
        return " + ".join(SymbolicMulti.key_str(m) for m in multi_sum.terms)

    def __str__(self) -> str:
        return self.key_str(self)

    def __frplib_repr__(self) -> str:
        return str(self)

    def is_pure(self) -> bool:
        return len(self.terms) == 1 and self.terms[0].is_pure()

    def pure_value(self):
        if len(self.terms) == 1:
            return self.terms[0].pure_value()
        return None

    def key_of(self):
        return self.key_str(self)

    @classmethod
    def singleton(cls, sym: SymbolicMulti):
        return SymbolicMultiSum([sym])

    @staticmethod
    def combine_terms(terms: list[SymbolicMulti]) -> list[SymbolicMulti]:
        combined: dict[str, SymbolicMulti] = {}
        for term in terms:
            k = term.term_order
            if k in combined:
                combined[k] = SymbolicMulti.from_terms(term.term, combined[k].coef + term.coef)
            else:
                combined[k] = term
        return [v for v in combined.values() if not is_zero(v.coef)]

    def __add__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            return SymbolicMultiSum([*self.terms, SymbolicMulti.pure(other)])

        if isinstance(other, SymbolicMulti):
            return SymbolicMultiSum([*self.terms, other])

        if isinstance(other, SymbolicMultiSum):
            return SymbolicMultiSum([*self.terms, *other.terms])

        # Handle other symbolics here
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            return SymbolicMultiSum([*self.terms, SymbolicMulti.pure(-other)])

        if isinstance(other, SymbolicMulti):
            return SymbolicMultiSum([*self.terms, -1 * other])

        if isinstance(other, SymbolicMultiSum):
            terms = [*self.terms]
            terms.extend(-1 * term for term in other.terms)
            return SymbolicMultiSum(terms)

        # Handle other symbolics here
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            return SymbolicMultiSum([*self.terms, SymbolicMulti.pure(other)])

        if isinstance(other, SymbolicMulti):
            return SymbolicMultiSum([*self.terms, other])

        # Handle other symbolics here
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            terms = [SymbolicMulti.pure(-other)]
            terms.extend(-1 * term for term in self.terms)
            return SymbolicMultiSum(terms)

        if isinstance(other, SymbolicMulti):
            terms = [other]
            terms.extend(-1 * term for term in self.terms)
            return SymbolicMultiSum(terms)

        # Handle other symbolics here
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            return SymbolicMultiSum([x * as_real(other) for x in self.terms])

        if isinstance(other, SymbolicMulti):
            return SymbolicMultiSum([x * other for x in self.terms])

        if isinstance(other, SymbolicMultiSum):
            # Combine like terms
            combined: dict[str, SymbolicMulti] = {}
            for term1 in self.terms:
                for term2 in other.terms:
                    prod = term1 * term2
                    k = prod.term_order
                    if k in combined:
                        combined[k].coef += prod.coef
                    else:
                        combined[k] = prod
            terms = [v for v in combined.values() if not is_zero(v.coef)]
            return SymbolicMultiSum(terms)
        # Handle other symbolics here
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            return SymbolicMultiSum([as_real(other) * x for x in self.terms])

        if isinstance(other, SymbolicMulti):
            return SymbolicMultiSum([other * x for x in self.terms])

        # Handle other symbolics here
        return NotImplemented

    def __pow__(self, n):
        if isinstance(n, int):
            if n == 0:
                return symbolic_one
            if n == 1:
                return self
            if n % 2 == 0:
                return (self * self) ** (n // 2)
            return self * (self * self) ** (n // 2)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if other == 1:
                return self
            d = as_real(other)
            return SymbolicMultiSum([term / d for term in self.terms])

        if isinstance(other, (SymbolicMulti)):
            if other.is_pure() and other.coef == 1:
                return self
            return SymbolicMultiSum([term / other for term in self.terms])

        if isinstance(other, (SymbolicMultiSum, SymbolicMultiRatio)):
            return symbolic(self, other)

        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if other == 1:
                return symbolic(symbolic_one, self)
            d = as_real(other)
            return symbolic(SymbolicMulti.pure(d), self)

        if isinstance(other, (SymbolicMulti)):
            if other.is_pure() and other.coef == 1:
                return symbolic(symbolic_one, self)
            return symbolic(other, self)

        if isinstance(other, SymbolicMultiRatio):
            return symbolic(self, other)

        return NotImplemented


#
# Ratios of Sums of Multinomial Terms
#

class SymbolicMultiRatio(Symbolic):
    def __init__(self, numerator: SymbolicMultiSum, denominator: SymbolicMultiSum):
        terms = [numerator, denominator]
        # ATTN: ADD simplify here, or preferably earlier
        self.terms = terms

    @property
    def numerator(self):
        return self.terms[0]

    @property
    def denominator(self):
        return self.terms[1]

    @staticmethod
    def key_str(ratio):
        return f'({str(ratio.numerator)})/({str(ratio.denominator)})'

    def __str__(self) -> str:
        return self.key_str(self)

    def __frplib_repr__(self) -> str:
        return str(self)

    def is_pure(self) -> bool:
        return self.numerator.is_pure() and self.denominator.is_pure()

    def pure_value(self):
        npv = self.numerator.pure_value()
        dpv = self.denominator.pure_value()

        if npv is not None and dpv is not None:
            return npv / dpv
        return None

    def key_of(self):
        return self.key_str(self)

    def __add__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if is_zero(as_numeric(other)):
                self
            numer = self.numerator + other
            denom = self.denominator
            return simplify(SymbolicMultiRatio(numer, denom))

        if isinstance(other, SymbolicMultiRatio):
            if self.denominator.key_of() == other.denominator.key_of():
                return SymbolicMultiRatio(self.numerator + other.numerator, self.denominator)

            numer = self.numerator * other.denominator + self.denominator * other.numerator
            denom = self.denominator * other.denominator
            return simplify(SymbolicMultiRatio(numer, denom))

        if isinstance(other, SymbolicMultiSum):
            numer = self.numerator + other
            denom = self.denominator
            return simplify(SymbolicMultiRatio(numer, denom))

        if isinstance(other, SymbolicMulti):
            if not other:
                return self
            numer = self.numerator + SymbolicMultiSum([other])
            denom = self.denominator
            return simplify(SymbolicMultiRatio(numer, denom))

        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if is_zero(as_numeric(other)):
                self
            numer = other + self.numerator
            denom = self.denominator
            return simplify(SymbolicMultiRatio(numer, denom))

        if isinstance(other, SymbolicMultiSum):
            numer = other + self.numerator
            denom = self.denominator
            return simplify(SymbolicMultiRatio(numer, denom))

        if isinstance(other, SymbolicMulti):
            if not other:
                return self
            numer = SymbolicMultiSum([other]) + self.numerator
            denom = self.denominator
            return simplify(SymbolicMultiRatio(numer, denom))

        return NotImplemented

    def __sub__(self, other):
        return self + (-1 * other)

    def __rsub__(self, other):
        return other + (-1 * self)

    def __mul__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if is_zero(as_numeric(other)):
                return symbolic_zero
            numer = self.numerator * other
            denom = self.denominator
            return SymbolicMultiRatio(numer, denom)

        if isinstance(other, SymbolicMultiRatio):
            if self.numerator.key_of() == other.denominator.key_of():
                return simplify(symbolic(other.numerator, self.denominator))

            if self.denominator.key_of() == other.numerator.key_of():
                return simplify(symbolic(self.numerator, other.denominator))

            numer = self.numerator * other.numerator
            denom = self.denominator * other.denominator
            return SymbolicMultiRatio(numer, denom)

        if isinstance(other, SymbolicMultiSum):
            numer = self.numerator * other
            denom = self.denominator
            return SymbolicMultiRatio(numer, denom)

        if isinstance(other, SymbolicMulti):
            numer = self.numerator * SymbolicMultiSum([other])
            denom = self.denominator
            return SymbolicMultiRatio(numer, denom)

        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if is_zero(as_numeric(other)):
                return symbolic_zero
            numer = other * self.numerator
            denom = self.denominator
            return SymbolicMultiRatio(numer, denom)

        if isinstance(other, SymbolicMultiSum):
            numer = other * self.numerator
            denom = self.denominator
            return SymbolicMultiRatio(numer, denom)

        if isinstance(other, SymbolicMulti):
            numer = SymbolicMultiSum([other]) * self.numerator
            denom = self.denominator
            return SymbolicMultiRatio(numer, denom)

        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            if other == 1:
                return self
            numer = self.numerator / other
            denom = self.denominator
            return SymbolicMultiRatio(numer, denom)

        if isinstance(other, SymbolicMultiRatio):
            numer = self.numerator * other.numerator
            denom = self.denominator * other.denominator
            return SymbolicMultiRatio(numer, denom)

        if isinstance(other, SymbolicMultiSum):
            numer = self.numerator * other
            denom = self.denominator
            return SymbolicMultiRatio(numer, denom)

        if isinstance(other, SymbolicMulti):
            numer = self.numerator * SymbolicMultiSum([other])
            denom = self.denominator
            return SymbolicMultiRatio(numer, denom)

        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float, Decimal)):   # is_scalar_q(other):
            numer = SymbolicMultiSum([SymbolicMulti.pure(other)])
            denom = self.denominator
            return SymbolicMultiRatio(numer * denom, self.numerator)

        if isinstance(other, SymbolicMultiSum):
            numer = self.denominator * other
            denom = self.numerator
            return SymbolicMultiRatio(numer, denom)

        if isinstance(other, SymbolicMulti):
            numer = self.denominator * SymbolicMultiSum([other])
            denom = self.numerator
            return SymbolicMultiRatio(numer, denom)

        return NotImplemented

    def __pow__(self, n):
        if isinstance(n, int):
            if n == 0:
                return symbolic_one
            if n == 1:
                return self
            return symbolic(self.numerator ** n, self.denominator ** n)
        return NotImplemented


#
# Simple Simplification Rules
#

def simplify(a: Symbolic | Numeric) -> Union[Symbolic, Numeric]:
    if isinstance(a, (int, Decimal)):
        return a

    apv = a.pure_value()
    if isinstance(a, SymbolicMultiSum) and apv is not None:
        return apv
    elif isinstance(a, SymbolicMultiRatio):
        npv = a.numerator.pure_value()
        dpv = a.denominator.pure_value()

        if npv is not None and (dpv is not None or is_zero(npv)):
            return (npv / dpv) if dpv is not None else 0
        elif npv is not None:
            return SymbolicMultiRatio(SymbolicMultiSum.singleton(symbolic_one), a.denominator * npv)
        if dpv is not None:
            return a.numerator / dpv

        # ATTN: Get other constants too!  Normalize Multisum to have a coef and leading 1 term
        if a.numerator.key_of() == a.denominator.key_of():
            return 1
    return a


#
# Symbolic Constructors (use these not the class constructors)
#

def symbolic(numerator: Union[Symbolic, str], denominator: Union[Symbolic, Literal[1]] = 1) -> Union[Symbolic, Numeric]:
    if isinstance(numerator, str):
        numerator = symbol(numerator)

    npv = numerator.pure_value()
    dpv = denominator.pure_value() if denominator != 1 else 1
    if npv is not None and dpv is not None:
        return npv / dpv
    elif npv is not None and denominator == 1:
        return npv
    elif npv is not None:
        numerator = symbolic_one
        denominator = denominator / npv
    elif denominator == 1:
        return simplify(numerator)

    assert isinstance(numerator, Symbolic)
    assert isinstance(denominator, Symbolic)

    if isinstance(numerator, SymbolicMulti):
        numerator = SymbolicMultiSum([numerator])

    if isinstance(denominator, SymbolicMulti):
        denominator = SymbolicMultiSum([denominator])

    num_rat = isinstance(numerator, SymbolicMultiRatio)
    den_rat = isinstance(denominator, SymbolicMultiRatio)

    if num_rat and den_rat and numerator.key_of() == denominator.key_of():
        return symbolic_one
    if num_rat:
        numerator = cast(SymbolicMultiSum, numerator)
        return simplify(numerator.__truediv__(denominator))
    elif den_rat:
        denominator = cast(SymbolicMultiSum, denominator)
        return simplify(denominator.__rtruediv__(numerator))

    numerator = cast(SymbolicMultiSum, numerator)
    denominator = cast(SymbolicMultiSum, denominator)

    if numerator.key_of() == denominator.key_of():
        return symbolic_one

    return simplify(SymbolicMultiRatio(numerator, denominator))
#
# Symbol constructors
#

def gen_symbol() -> SymbolicMulti:
    "Generates a unique symbol as a symbolic quantity."
    var = next(gensym)
    return SymbolicMulti([var], [1])

def symbol(var: str) -> SymbolicMulti:
    "Generates a symbol with given variable name."
    return SymbolicMulti([var], [1])

def is_symbolic(obj) -> bool:
    return isinstance(obj, (SymbolicMulti, SymbolicMultiSum, SymbolicMultiRatio))

# def arbitrary(*xs):
#     values = sequence_of_values(*xs, flatten=Flatten.NON_TUPLES, transform=as_numeric_vec)
#     if len(values) == 0:
#         return Kind.empty
#     return Kind([KindBranch.make(vs=x, p=gen_symbol()) for x in values])
