from dataclasses import dataclass
from enum        import Enum, auto
from itertools   import accumulate
from typing      import Any, TypeAlias

from frplib.kinds      import Kind
from frplib.kind_trees import unfold_tree
from frplib.numeric    import show_values, show_tuples


# alias BranchIndex = Int
# alias Level = Int
# alias Width = Int
# Pos = Pos { x : Int, y : Int }
# Edge = First | Other | Middle | Last
# Branch = Branch Pos Width Edge Labels
# Segment = Segment Pos
# Item = Branch | Segment
# Index = (BranchIndex, Size, Level)
# Subtree = (Weight, (Node, List[Subtree]))

# unfold_scan : {env} -> Index -> Subtree -> (Maybe Pos) -> (List Item) -> (Branch, List Item)
# Env contains widths by level, dim

# Branch(x, y, First,  level labels) =>    ,----- w ---- <...>   -  [last - missing on leaves]
# Branch(x, y, Middle, level labels) =>    +----- w ---- <...>   -
# Branch(x, y, Last,   level labels) =>    `----- w ---- <...>   -
# Branch(x, y, Other,  level labels) =>    |----- w ---- <...>   -
# Segment(x, y)                      =>    |

class Edge(Enum):
    FIRST = auto()
    MIDDLE = auto()
    OTHER = auto()
    LAST = auto()
    ROOT = auto()

@dataclass(frozen=True)
class Branch:
    x: int
    y: int
    edge: Edge
    level: int
    labels: tuple[str, str]

@dataclass(frozen=True)
class Segment:
    x: int
    y: int
    z: Any

Items: TypeAlias = list[Branch | Segment]
STree: TypeAlias = 'list[str | STree]'

# from frplib.kind_trees import unfold_tree
# from frplib.uscan import *
# from rich.pretty import pprint
# uu = uniform(1, 2, 3) * uniform(7, 8, 9)
# x = unfold_tree(uu._canonical)
# wd = [(0,3)]
# sep = [4, 2, 0]
# xl = unfolded_labels(x['unfolded'][1:], str(x['unfolded'][0]), 1, wd)
# s, _ = unfold_scan(xl, wd, sep)
# unfolded_str(s, wd)
#
# bit = choice(0, 1)
# bbb = bit ** 3
# z = unfold_tree(bbb._canonical)
# wd2 = [(0,3)]
# sep2 = [0, 4, 2, 0]
# zl = unfolded_labels(z['unfolded'][1:], str(z['unfolded'][0]), 1, wd2)
# s2, _ = unfold_scan(zl, wd2, sep2)
# unfolded_str(s2, wd2)


def unfolded_labels(unfolded_branches, root_str, level, widths) -> STree:
    w_strs = show_values(subtree[0] for subtree in unfolded_branches)
    v_strs = show_tuples([subtree[1] if isinstance(subtree[1], tuple) else subtree[1][0]
                          for subtree in unfolded_branches], scalarize=False)
    w_max = max(len(w) for w in w_strs) + 2  # for spaces
    v_max = max(len(v) for v in v_strs) + 2  # for spaces
    w_strs = ['{0:-<{wd}}'.format(' ' + w + ' ', wd=w_max) for w in w_strs]
    v_strs = ['{0:<{wd}}'.format(' ' + v + ' ', wd=v_max)  for v in v_strs]

    if len(widths) <= level:
        widths.append((w_max, v_max))
        assert len(widths) >= level  # must be length >= level - 1 to get to append
    else:
        widths[level] = tuple(map(max, zip(widths[level], (w_max, v_max))))

    out: STree = []
    for index, branch in enumerate(unfolded_branches):
        if isinstance(branch[1], tuple):
            out.append([w_strs[index], v_strs[index]])
        else:
            out.append([w_strs[index], unfolded_labels(branch[1][1:], v_strs[index], level + 1, widths)])
    return [root_str, *out]

def after_dashes(weight_width: int) -> int:
    if weight_width < 6:
        return 4
    elif weight_width < 10:
        return 6
    else:
        return 8

def unfold_scan(unfolded, widths_by_level: list[tuple[int, int]], sep: list[int]) -> tuple[Items, list[int]]:
    "Converts an unfolded tree into scan ordered branches for display."

    def level_width(level, leaf=False):
        if level == 0:
            return 4
        weight_width, value_width = widths_by_level[level]
        extra = 1 + (1 - leaf)  # 1 for segment line, 1 for next node connection
        dashes = after_dashes(weight_width)  # number dashes after weight
        return extra + (2 * dashes + 1) + weight_width + value_width

    num_levels = len(widths_by_level)
    level_widths = [level_width(level, level == num_levels - 1)
                    for level in range(num_levels)]
    x_by_level = list(accumulate(level_widths, initial=0))

    def scan(index: tuple[int, int, int], tree: STree, acc: Items) -> tuple[Branch, int, int]:
        # index = (m, ell) the mth branch at level ell
        # tree = [w, leaf | subtree]:  tree contains *labels* as data, computed together by subtree!!
        # acc = list of Items

        m, size, level = index
        x = x_by_level[level]
        weight, more = tree
        assert isinstance(weight, str)

        if level == 0:
            edge = Edge.ROOT
        elif m == 0 and size > 1:
            edge = Edge.FIRST
        elif size % 2 != 0 and m == size // 2:
            edge = Edge.MIDDLE
        elif m == size - 1:
            edge = Edge.LAST
        else:
            edge = Edge.OTHER

        # Leaf
        if isinstance(more, str):  # <=> level == env.dim
            if len(acc) == 0:  # First/top leaf node
                return (Branch(x, 0, Edge.FIRST, level, (weight, more)), 0, 0)
            base = acc[-1]
            yb = base.y
            return (Branch(x, yb + 1, edge, level, (weight, more)), yb + 1, yb + 1)

        # Non-Leaf
        node, *subtree = more
        assert isinstance(node, str)
        assert len(subtree) > 0

        size_prime = len(subtree)
        no_middle = size_prime % 2 == 0
        half_height = size_prime // 2
        x_prime = x_by_level[level + 1]
        y_min = int(10 ** 10)  # Sentinels
        y_max = -1

        for k in range(half_height):
            b = subtree[k]
            assert not isinstance(b, str)
            b_prime, y_max, y_min_k = scan((k, size_prime, level + 1), b, acc)
            y_min = min(y_min, y_min_k)
            acc.append(b_prime)
            # k always < size_prime - 1 here
            if no_middle and k == half_height - 1:
                yb = y_max
                for i in range(sep[level + 1] // 2):
                    yb += 1
                    acc.append(Segment(x_prime, yb, 'D'))
            else:
                yb = y_max
                for i in range(sep[level + 1]):
                    yb += 1
                    acc.append(Segment(x_prime, yb, 'D'))

        # k == half_height
        if no_middle:
            yb += 1
            me = Branch(x, yb, edge, level, (weight, node))
            y_seg = me.y + 1
            if m > 0:
                for y in range(y_min, me.y):
                    acc.append(Segment(x, y, 'B'))
            acc.append(Segment(x_prime, yb, 'A'))  # --| split
            for i in range(sep[level + 1] // 2, sep[level + 1]):
                yb += 1
                acc.append(Segment(x_prime, yb, 'D'))

        for k in range(half_height, size_prime):
            b = subtree[k]
            assert not isinstance(b, str)
            b_prime, y_max, y_min_k = scan((k, size_prime, level + 1), b, acc)
            yb = b_prime.y
            y_min = min(y_min, y_min_k)

            if k == half_height and not no_middle:
                me = Branch(x, yb, edge, level, (weight, node))
                if m > 0:
                    for y in range(y_min, me.y):
                        acc.append(Segment(x, y, 'B'))
                y_seg = me.y + 1

            if m < size - 1:
                # ATTN! Overlap here as y_max grows
                for y in range(y_seg, y_max + 1):
                    acc.append(Segment(x, y, 'C'))
                y_seg = y_max + 1
            acc.append(b_prime)

            if k < size_prime - 1:
                yb = y_max
                for i in range(sep[level + 1]):
                    yb += 1
                    acc.append(Segment(x_prime, yb, 'D'))

        # for k, b in enumerate(subtree):
        #     assert not isinstance(b, str)
        #     if k == half_height and no_middle:
        #         # yb is height of last branch above the middle
        #         # ATTN: yb + 1 ?  yb for the first helps some things and hurts others
        #         me = Branch(x, yb + 1, edge, level, (weight, node))
        #         acc.append(Segment(x_prime, yb + 1, 'A'))  # --| split
        #
        #     b_prime, y_max, y_min_k = scan((k, size_prime, level + 1), b, acc)
        #     yb = b_prime.y
        #     y_min = min(y_min, y_min_k)
        #
        #     if k < half_height:
        #         # if m > 0:
        #         #     acc.append(Segment(x, yb, 'B'))
        #         acc.append(b_prime)
        #     if k == half_height and not no_middle:
        #         me = Branch(x, yb, edge, level, (weight, node))
        #     if k == half_height:
        #         if m > 0:
        #             for y in range(y_min, me.y):
        #                 acc.append(Segment(x, y, 'B'))
        #     if k >= half_height:
        #         if m < size - 1:
        #             # ATTN! Overlap here as y_max grows
        #             for y in range(me.y + 1, y_max + 1):
        #                 acc.append(Segment(x, y, 'C'))
        #             # acc.append(Segment(x, yb, 'C'))
        #         acc.append(b_prime)
        #
        #     if k < size_prime - 1:
        #         yb = y_max
        #         for i in range(sep[level + 1]):
        #             yb += 1
        #             acc.append(Segment(x_prime, yb, 'D'))
        return (me, max(yb, y_max), y_min)

    if len(unfolded) == 1:
        return ([Branch(4, 0, Edge.ROOT, 0, ('', unfolded[0]))], level_widths)

    items: Items = []
    root, _, _ = scan((0, 1, 0), ['', unfolded], items)
    items.append(root)
    items.sort(key=lambda v: (v.y, v.x))

    return (items, level_widths)

def unfolded_str(scanned: Items, widths_by_level: list[tuple[int, int]]) -> str:
    # Temporarily interpret items here; move to another function
    y_last = 0
    x_last = 0
    num_levels = len(widths_by_level)

    out: list[str] = []
    for item in scanned:
        x, y = (item.x, item.y)
        # Fill in missing spaces
        if y_last == y:
            out.append(' ' * (x - x_last))
        else:
            out.append('\n' * (y - y_last))
            out.append(' ' * x)

        # Print appropriate piece for this item:
        #   Branch(x, y, First,  level labels) =>    ,----- w ---- <...>   -
        #   Branch(x, y, Middle, level labels) =>    +----- w ---- <...>   -
        #   Branch(x, y, Last,   level labels) =>    `----- w ---- <...>   -
        #   Branch(x, y, Other,  level labels) =>    |----- w ---- <...>   -
        #   Segment(x, y)                      =>    |
        # Skip the final joining piece for a lief

        if isinstance(item, Segment):
            token = '|'
        else:
            edge = item.edge
            level = item.level
            connect = '-' if level < num_levels - 1 else ''
            wlabel, vlabel = item.labels
            after_dash_s = '-' * after_dashes(len(wlabel))
            before_dash_s = after_dash_s + '-'
            joins = {Edge.FIRST: ',', Edge.MIDDLE: '+', Edge.LAST: '`', Edge.OTHER: '|'}

            if edge == Edge.ROOT:
                token = '<> {0}'.format(connect)
            else:
                token = '{seg}{before}{weight:-<{wwd}}{after}{value:<{vwd}}{con}'.format(
                    seg=joins[edge],
                    before=before_dash_s, weight=wlabel, after=after_dash_s,
                    value=vlabel, con=connect,
                    wwd=widths_by_level[level][0],
                    vwd=widths_by_level[level][1]
                )
        out.append(token)
        x_last = x + len(token)
        y_last = y
    return "".join(out)

def unfold(k: Kind) -> str:  # ATTN: Return an object that prints this string, later
    dim = k.dim
    unfolded = unfold_tree(k._canonical)
    if unfolded is None:
        return k.show_full()
    # ATTN: Remove other components from this, no longer needed
    unfolded = unfolded['unfolded']
    assert unfolded is not None

    wd = [(0, 3)]
    labelled = unfolded_labels(unfolded[1:], str(unfolded[0]), 1, wd)

    sep = [2 * (dim - level) for level in range(dim + 1)]
    scan, _ = unfold_scan(labelled, wd, sep)

    # from rich.pretty import pprint  # ATTN:TEMP
    # pprint(scan)

    return unfolded_str(scan, wd)
