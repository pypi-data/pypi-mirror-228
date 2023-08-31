# Dev examples for other parts of the package
import random


from collections.abc   import Iterable, Iterator
from typing            import ( Callable
                              , Generator
                              , Generic
                              , Mapping
                              , Optional
                              , TypeAlias
                              , TypeVar
                              )

from frplib.exceptions import KindError
from frplib.kinds      import Kind, uniform, constant, permutations_of
from frplib.frps       import FRP, FrpExpression, frp
from frplib.statistics import Statistic, MonoidalStatistic, scalar_statistic
from frplib.vec_tuples import VecTuple

# ATTN: convert dict to an appropriate Mixture supertype,  Mixture | Callable
# ATTN:UPDATE have supertypes ConditionalKind and ConditionalFrp
# with Conditional*Dict and Conditional*Callable subtypes
# factories conditional_kind and conditional_frp also can take some notion
# of domain for the callable case to make it easy to check compatiability

### .examples.MontyHall

def arbitrary(*values) -> Kind:
    "Returns a symbolic kind with arbitrary positive weight on each value"
    ...
    return Kind.empty #ATTN:TEMP

door_with_prize = uniform(1, 2, 3)     # Kind with equal weights on all doors
chosen_door = arbitrary(1, 2, 3)       # Kind with any weights on the doors
@scalar_statistic(name='Chose Prize Initially')
def chose_prize_door_initially(prize, chosen):
    return prize == chosen


### .examples.Labyrinth

from itertools import islice

# TEMP Labyrinth
labyrinth = {1: [2, 3, 4], 2: [1, 3, 5], 3: [2, 6, 7], 4: [2], 5: [2, 7], 6: [3], 7: [3, 5]}
steps = { juncture: uniform(labyrinth[juncture]) for juncture in labyrinth }
#from_latest = lambda steps: conditional_kind( lambda path: steps[path[-1]] )

# ATTN: replace with above
def from_latest(steps: dict) -> Callable:
    # Convert this to a CallableMixture
    def mixture(path):
        latest = path[-1]
        return steps[latest]
    return mixture

start = constant(1)
moves = from_latest(steps)

def theseus_latest(initial: Kind, step: dict) -> Generator:
    current = initial
    while True:
        current = (current >> step) @ 2
        yield current

T = TypeVar('T')

def nth(seq: Iterator[T], n: int) -> T:
    return next(islice(seq, n, n+1))

def after_move_n(n: int, start: Kind, steps: dict) -> Kind:
    return nth(theseus_latest(start, steps), n)

def ever_visited(n: int):
    # Assume rooms labeled 1..n
    # convert to current room and binary array 1..n
    def visits(path: tuple[int,...]) -> tuple[int, ...]:
        rooms = [0] * (n + 1)
        rooms[0] = path[-1]  # current room
        for room in path:
            rooms[room] = 1
        return tuple(rooms)
    return visits

    


# Method for power and monoidal statistic combination
#
# Computes  (kind ** n) ^ stat using monoidal properties of stat

def pow_stat(kind: Kind, n: int, stat: MonoidalStatistic) -> Kind:
    # something like exponentiation by squaring where we apply
    # the statistic at various intermediate points
    # ATTN:INCOMPLETE
    return Kind.empty


# Functions that can be factories or decorators
# The new_ prefix is temporary
#
# NOTE: General issue: dim=0 means an *arbitrary length* tuple expected

def new_statistic(
        maybe_fn : Optional[Callable] = None, # If supplied, return Statistic, else a decorator
        *,
        name: Optional[str] = None,         # A user-facing name for the statistic
        dim: Optional[int] = None,          # Number of arguments the function takes; 0 means tuple expected
        codim: Optional[int] = None,        # Dimension of the codomain; None means don't know
        description: Optional[str] = None,  # A description used as a __doc__ string for the Statistic
        monoidal: bool = False              # Is this a Monoidal statistic?
) -> Statistic | Callable[[Callable], Statistic]:
    if maybe_fn:
        return Statistic(maybe_fn, dim, codim, name, description)
    def decorator(fn: Callable) -> Statistic:     # Function to be converted to a statistic
        return Statistic(fn, dim, codim, name, description)
    return decorator

def new_scalar_statistic(
        name: Optional[str] = None,         # A user-facing name for the statistic
        dim: Optional[int] = None,          # Number of arguments the function takes; 0 means tuple expected
        description: Optional[str] = None,  # A description used as a __doc__ string for the Statistic
        monoidal: bool = False              # Is this a Monoidal statistic?
) -> Statistic | Callable[[Callable], Statistic]:
    def decorator(fn: Callable) -> Statistic:     # Function to be converted to a statistic
        return Statistic(fn, dim, 1, name, description)
    return decorator



# Examples. Sec 8

class FisherYates(FrpExpression):
    def __init__(self, items: Iterable):
        super().__init__()
        self.items = tuple(items)
        self.n = len(self.items)

    def sample1(self):
        permuted = list(self.items)
        for i in range(self.n - 1):
            j = random.randrange(i, self.n)
            permuted[j], permuted[i] = permuted[i], permuted[j]  # swap
        return VecTuple(permuted)

    def value(self):
        if self._cached_value is None:
            self._cached_value = self.sample1()
        return self._cached_value

    def kind(self) -> Kind:
        if self.n <= 10:
            return permutations_of(self.items)
        raise KindError(f'The kind of a large ({self.n} > 10) permutation is too costly to compute.')

    def clone(self) -> 'FisherYates':
        self._cached_value = None
        self.value()
        return self

def shuffle(items: Iterable) -> FRP:
    return frp(FisherYates(items))
