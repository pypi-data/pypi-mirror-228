from __future__ import annotations

from frplib.symbolic  import symbol, gen_symbol

#
# Helpers
#

def test_symbol_arithmetic():
    "Simple sequence patterns."
    a = symbol('a')
    b = symbol('b')

    assert str(a) == '1 a^1'
    assert str(b) == '1 b^1'
    assert str(a - a) == '0'
    assert str(1 + a) == '1 + 1 a^1'
    assert str((1 + a) * (1 - a)) == '1 + -1 a^2'
    assert str(1 + b + b**2 + b**3) == '1 + 1 b^1 + 1 b^2 + 1 b^3'
    assert str((a - a) * (1 + b + b**2 + b**3)) == '0'

    assert str(1.2 * a) == '1.2 a^1'
    assert str((1.2 * a) ** 2) == '1.44 a^2'

    assert str(gen_symbol()) != str(gen_symbol())

    assert str(1 / (1 + a)) == '(1)/(1 + 1 a^1)'
