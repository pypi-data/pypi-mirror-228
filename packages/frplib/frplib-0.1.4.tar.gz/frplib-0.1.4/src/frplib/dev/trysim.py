from itertools import product

from frplib.kinds      import *
from frplib.symbolic   import *
from frplib.vec_tuples import *
from frplib.numeric    import *
from frplib.utils      import *

def arbitrary(*xs):
    values = sequence_of_values(*xs, flatten=Flatten.NON_TUPLES, transform=as_numeric_vec)
    if len(values) == 0:
        return Kind.empty
    return Kind([KindBranch.make(vs=x, p=gen_symbol()) for x in values])

def combine_product(branchA, branchB):
    return KindBranch.make(vs=list(branchA.vs) + list(branchB.vs), p=branchA.p * branchB.p)

def prod(kA, kB):
    return Kind([combine_product(brA, brB) for brA, brB in product(kA._canonical, kB._canonical)])

def prod_str(kA, kB):
    return lmap(str, [combine_product(brA, brB).p for brA, brB in product(kA._canonical, kB._canonical)])

def prod_sum(kA, kB):
    return sum([combine_product(brA, brB).p for brA, brB in product(kA._canonical, kB._canonical)])


u = uniform(1, 2, 3)
a = arbitrary(1, 2, 3)
