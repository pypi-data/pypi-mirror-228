from dataclasses                  import dataclass
from returns.interfaces           import bindable, equable, mappable, applicative
from returns.primitives.container import BaseContainer, container_equality
from returns.primitives.hkt       import Kind2, SupportsKind2, dekind
from typing                       import Callable, cast, Generator, Generic, Mapping, TypeAlias, TypeVar
from typing_extensions            import Self

from frplib.kind_trees import KindBranch, KindTree
from frplib.numeric    import NumericD, NumericF, NumericB, one


#
# Generic FRP Kind Monad.  Allow general value types and implement the functorial methods
#


#
# Internal Types and Type Variables
#

ValueType = TypeVar('ValueType')
ProbType = TypeVar('ProbType', NumericF, NumericD, NumericB)  # All support arithmetic, one(), and zero()
NewValueType = TypeVar('NewValueType')

ValueMap: TypeAlias = Callable[[ValueType], ProbType] | Mapping[ ValueType, ProbType ]

CanonicalKind: TypeAlias = list[KindBranch[ValueType, ProbType]]


#
# Helper functions ATTN: should probably become static methods
#

def unit_probability() -> ProbType:
    return cast(ProbType, one)        # ATTN: every ProbType must accept one (:int = 1) as a unit and zero (:int = 0) as a zero

def canonical_form(kind: KindTree[ValueType, ProbType]) -> CanonicalKind[ValueType, ProbType]:
    ...
    # normalize weights at each level
    # reduce to single level (eliminating trivial trees except as solitary root)
    # (if possible) sort leaves in order
    return [] # TEMP


#
# Main Class
#

class KindMonad(
    BaseContainer,
    SupportsKind2['KindMonad', ValueType, ProbType],
    # mappable.Mappable2[ValueType, ProbType],  supertype of applicative so not needed
    applicative.Applicative2[ValueType, ProbType],
    bindable.Bindable2[ValueType, ProbType],
    equable.Equable,
):
    """
    The base type for a generic Kind tree that can have 
    
    """

    def __init__( self: Self, spec: KindTree[ValueType,ProbType] | CanonicalKind[ValueType, ProbType]) -> None:
        inner_value: CanonicalKind[ValueType, ProbType]
        # mypy not picking up that this test distinguishes the union components, so cast
        if isinstance(spec[0], KindTree):
            inner_value = canonical_form(cast(KindTree[ValueType, ProbType], spec))
        else:  # CanonicalKind
            inner_value = cast(CanonicalKind[ValueType, ProbType], spec).copy()   # Copy the list; the rest is immutable
        super().__init__( inner_value )

        self._size = len(inner_value)

    @property
    def size(self):
        return self._size


    # Functorial Methods

    equals = container_equality

    def map( self, f: Callable[[ValueType], NewValueType] ) -> 'KindMonad[NewValueType, ProbType]':
        new_kind : CanonicalKind[NewValueType, ProbType] = list(map(lambda branch: KindBranch(values=f(branch.values), probability=branch.probability), self._inner_value))
        return KindMonad(new_kind)

    def apply( self: Self, fkind: Kind2['KindMonad', Callable[[ValueType], NewValueType], ProbType] ) -> 'KindMonad[NewValueType, ProbType]':
        def joinMap(
                f: CanonicalKind[Callable[[ValueType], NewValueType], ProbType],
                a: CanonicalKind[ValueType, ProbType]
        ) -> Generator[KindBranch[NewValueType, ProbType], None, None]:
            for a_branch in a:
                for f_branch in f:
                    yield a_branch.assoc(vs=f_branch.vs(a_branch.vs), p=f_branch.p * a_branch.p)
        # ATTN: Need to check and collapse common values
        return KindMonad(list(joinMap(fkind._inner_value, self._inner_value)))

    def bind(self: Self, f: Callable[[ValueType], Kind2['KindMonad', NewValueType, ProbType]]) -> 'KindMonad[NewValueType, ProbType]':
        def mix(branch: KindBranch[ValueType, ProbType]):
            subtree = dekind(f(branch.vs))._inner_value
            return KindBranch(values=subtree.vs, probability=branch.p * subtree.p)
            
        new_kind: CanonicalKind[NewValueType, ProbType] = [mix(branch) for branch in self._inner_value]
        # ATTN: Need to check and collapse common values
            
        return KindMonad(new_kind)
        
    @classmethod
    def from_value( cls, value: NewValueType ) -> 'KindMonad[NewValueType, ProbType]':
        return KindMonad( [KindBranch(vs=value, p=one)] )  # Uses 1 as the prob which will match all the allowed prob types


    # Overloads

    def __len__(self: Self) -> int:
        return self._size
