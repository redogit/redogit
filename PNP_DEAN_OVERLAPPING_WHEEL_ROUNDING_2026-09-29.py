"""Exact finite Step 18 probe; no search or runtime claim for arbitrary inputs."""
from fractions import Fraction as F
from itertools import product
from math import ceil


def edge(u, v):
    return tuple(sorted((u, v)))


HUB = 0
RIMS = (tuple(range(1, 6)), tuple(range(6, 11)))
SUPPORTS = tuple(frozenset((HUB, *rim)) for rim in RIMS)
VERTICES = frozenset(range(11))


def wheel_edges(rim):
    return {edge(HUB, v) for v in rim} | {
        edge(rim[i], rim[(i + 1) % 5]) for i in range(5)
    }


ORIGINAL = wheel_edges(RIMS[0]) | wheel_edges(RIMS[1])
DELETED = edge(5, 1)
ALTERED = ORIGINAL - {DELETED}


def independent(s, edges):
    return all(not {u, v} <= s for u, v in edges)


def subsets(vertices):
    ordered = sorted(vertices)
    for mask in range(1 << len(ordered)):
        yield frozenset(v for i, v in enumerate(ordered) if mask >> i & 1)


def wheel_receipt(rim, edges):
    # Supplied labels and all ten positive input edges are checked.
    assert len(set((HUB, *rim))) == 6
    assert wheel_edges(rim) <= edges
    rows = [(frozenset(rim), 3, F(3, 5))] + [
        (frozenset((HUB, rim[i], rim[(i + 1) % 5])), 2, F(1, 5))
        for i in range(5)
    ]
    support = frozenset((HUB, *rim))
    loads = {v: sum(w for s, _, w in rows if v in s) for v in support}
    assert set(loads.values()) == {F(1)}
    q = sum(d * w for _, d, w in rows)
    assert q == F(19, 5) and ceil(q) == 4
    return q


def composed(requirements, weights):
    loads = {v: sum(w for s, w in zip(SUPPORTS, weights) if v in s)
             for v in VERTICES}
    return sum(d * w for d, w in zip(requirements, weights)) - sum(
        max(F(0), load - 1) for load in loads.values()
    )


assert SUPPORTS[0] & SUPPORTS[1] == {HUB}
assert len(ORIGINAL) == 20 and len(ALTERED) == 19
assert ORIGINAL - ALTERED == {DELETED}
assert wheel_receipt(RIMS[0], ORIGINAL) == wheel_receipt(RIMS[1], ORIGINAL)
assert wheel_receipt(RIMS[1], ALTERED) == F(19, 5)
try:
    wheel_receipt(RIMS[0], ALTERED)
except AssertionError:
    pass
else:
    raise AssertionError('Stale first-wheel receipt was admitted')

# Three disjoint existing K2 rows prove the altered first support needs three.
matching = (edge(0, 1), edge(2, 3), edge(4, 5))
assert set(matching) <= ALTERED
assert len({v for e in matching for v in e}) == 6

for name, edges, requirements, witness in (
    ('NO', ORIGINAL, (4, 4), frozenset((1, 3, 6, 8))),
    ('YES', ALTERED, (3, 4), frozenset((1, 3, 5, 7, 9))),
):
    all_sets = list(subsets(VERTICES))
    assert len(all_sets) == 2048
    valid = [s for s in all_sets if independent(s, edges)]
    alpha = max(map(len, valid))
    tau = len(VERTICES) - alpha
    assert independent(witness, edges) and len(witness) == alpha
    assert (alpha, tau) == ((4, 7) if name == 'NO' else (5, 6))
    bound = composed(requirements, (F(1), F(1)))
    assert bound == tau
    assert (bound > 6) == (name == 'NO')  # Same k=5, b=6 in both graphs.
    # Finite arithmetic countercheck of the proved rational-weight formula.
    for selected in valid:
        omitted = VERTICES - selected
        assert all(len(omitted & s) >= d for s, d in zip(SUPPORTS, requirements))
        for weights in product((F(0), F(1, 2), F(1), F(3, 2)), repeat=2):
            assert composed(requirements, weights) <= len(omitted)
    # Neither fixed antihole carrier can occur: too few vertices have degree >=4.
    degrees = {v: sum(v in e for e in edges) for v in VERTICES}
    assert sum(d >= 4 for d in degrees.values()) == 1
    print(name, 'n=11', f'm={len(edges)}', 'k=5 b=6',
          f'alpha={alpha}', f'tau={tau}', f'corrected_bound={bound}',
          f'independent_sets={len(valid)}', f'witness={sorted(witness)}')

# Both false rules reject the explicit YES: one loses identity, one loses edges.
assert sum((3, 4)) == 7 > 6
assert composed((4, 4), (F(1), F(1))) == 7 > 6
assert composed((F(19, 5), F(19, 5)), (F(1), F(1))) == F(33, 5)
assert ceil(F(33, 5)) == 7  # This pair shows soundness, no new rounding gain.
print('PASS exact Step 18 overlap and stale-evidence counterprobes')
