"""Steps 19-25: exact finite probes for fixed-size boundary composition.

The tree evaluator accepts only supplied bags <=6 and intersections <=3.
It does not find decompositions or decide inputs rejected by that contract.
"""
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path
import sys


def edge(a, b):
    return tuple(sorted((a, b)))


def wheel(rim, hub):
    return {edge(hub, v) for v in rim} | {
        edge(rim[i], rim[(i + 1) % 5]) for i in range(5)
    }


def subsets(vertices):
    vertices = sorted(vertices)
    for mask in range(1 << len(vertices)):
        yield frozenset(v for i, v in enumerate(vertices) if mask >> i & 1)


def independent(selected, edges):
    return all(not (u in selected and v in selected) for u, v in edges)


def exhaustive(vertices, edges):
    valid = [s for s in subsets(vertices) if independent(s, edges)]
    witness = max(valid, key=lambda s: (len(s), tuple(sorted(s))))
    return len(witness), witness, len(valid)


def boundary_rows(vertices, edges, a, b):
    assert a | b == vertices
    assert all({u, v} <= a or {u, v} <= b for u, v in edges)
    shared = a & b
    assert len(a) <= 6 and len(b) <= 6 and len(shared) <= 3
    rows = []
    for state in subsets(shared):
        if not independent(state, edges):
            rows.append({'selected': sorted(state), 'a': None, 'b': None, 'total': None})
            continue
        scores = []
        for bag in (a, b):
            scores.append(max(len(s) for s in subsets(bag - shared)
                              if independent(s | state, edges)))
        rows.append({'selected': sorted(state), 'a': scores[0], 'b': scores[1],
                     'total': len(state) + sum(scores)})
    return rows


def validate_tree(vertices, edges, bags, links):
    if not bags or any(len(b) > 6 or not b <= vertices for b in bags):
        raise ValueError('bag contract')
    if frozenset().union(*bags) != vertices:
        raise ValueError('vertex coverage')
    if len(links) != len(bags) - 1 or len(set(links)) != len(links):
        raise ValueError('tree edge count')
    adjacent = [set() for _ in bags]
    for u, v in links:
        if not (0 <= u < v < len(bags)):
            raise ValueError('tree endpoints')
        adjacent[u].add(v)
        adjacent[v].add(u)
        if len(bags[u] & bags[v]) > 3:
            raise ValueError('separator contract')
    reached, todo = set(), [0]
    while todo:
        u = todo.pop()
        if u not in reached:
            reached.add(u)
            todo.extend(adjacent[u] - reached)
    if len(reached) != len(bags):
        raise ValueError('disconnected tree')
    covered = {edge(u, v) for bag in bags for u, v in combinations(bag, 2)}
    if not edges <= covered:
        raise ValueError('edge coverage')
    occurrence = {v: 0 for v in vertices}
    connecting = {v: 0 for v in vertices}
    for bag in bags:
        for v in bag:
            occurrence[v] += 1
    for u, v in links:
        for x in bags[u] & bags[v]:
            connecting[x] += 1
    if any(connecting[v] != occurrence[v] - 1 for v in vertices):
        raise ValueError('running intersection')
    return adjacent


def tree_alpha(vertices, edges, bags, links, root=0):
    adjacent = validate_tree(vertices, edges, bags, links)
    if not 0 <= root < len(bags):
        raise ValueError('root')
    parent, order = {root: None}, [root]
    for u in order:
        for v in sorted(adjacent[u]):
            if v != parent[u]:
                parent[v] = u
                order.append(v)
    separator = {u: bags[u] & bags[parent[u]] if parent[u] is not None
                 else frozenset() for u in order}
    messages, choices = {}, {}
    candidate_count = 0
    for u in reversed(order):
        messages[u], choices[u] = {}, {}
        local_edges = {edge(v, w) for v, w in combinations(bags[u], 2)
                       if edge(v, w) in edges}
        children = sorted(adjacent[u] - ({parent[u]} if parent[u] is not None else set()))
        for selected in subsets(bags[u]):
            candidate_count += 1
            if not independent(selected, local_edges):
                continue
            score = len(selected - separator[u])
            possible = True
            for child in children:
                value = messages[child].get(selected & separator[child])
                if value is None:
                    possible = False
                    break
                score += value
            state = selected & separator[u]
            if possible and score > messages[u].get(state, -1):
                messages[u][state], choices[u][state] = score, selected
    witness = set()
    todo = [(root, frozenset())]
    while todo:
        u, state = todo.pop()
        selected = choices[u][state]
        witness.update(selected - separator[u])
        for child in adjacent[u]:
            if parent.get(child) == u:
                todo.append((child, selected & separator[child]))
    answer = messages[root][frozenset()]
    assert len(witness) == answer and independent(witness, edges)
    return answer, sorted(witness), candidate_count, max(map(len, messages.values()))


def reject(vertices, edges, bags, links, expected):
    try:
        tree_alpha(vertices, edges, bags, links)
    except ValueError as exc:
        assert str(exc) == expected, (str(exc), expected)
        return expected
    raise AssertionError('Invalid decomposition admitted')


def main(output):
    vertices = frozenset(range(9))
    a, b = frozenset(range(6)), frozenset((0, 1, 2, 6, 7, 8))
    a_edges = wheel((0, 1, 2, 3, 4), 5)
    b_edges = wheel((0, 1, 2, 6, 7), 8)
    intact = a_edges | b_edges
    altered = intact - {(3, 4)}
    identity = (a_edges - {(3, 4)}) | (wheel((0, 2, 1, 6, 7), 8) - {(6, 7)})
    assert len(intact) == 18 and len(altered) == len(identity) == 17
    fixtures = {}
    for name, edges, expected in [('intact', intact, 3), ('one_edge_yes', altered, 4),
                                   ('count_only_false_yes', identity, 4)]:
        optimum, witness, count = exhaustive(vertices, edges)
        rows = boundary_rows(vertices, edges, a, b)
        assert optimum == expected == max(r['total'] for r in rows if r['total'] is not None)
        roots = [tree_alpha(vertices, edges, [a, b], [(0, 1)], root) for root in (0, 1)]
        assert all(r[0] == optimum and r[2] == 128 for r in roots)
        fixtures[name] = {'edges': [list(e) for e in sorted(edges)], 'n': 9, 'm': len(edges),
                          'alpha': optimum, 'tau': 9 - optimum, 'witness': sorted(witness),
                          'enumerated_subsets': 512, 'independent_sets': count, 'states': rows}

    # Exact old-row certificate: every row is checked against the input graph.
    raw_rows = [((0, 1, 2, 3, 4), 3, Q(1, 5), 'cycle'),
                ((0, 1, 2, 6, 7), 3, Q(2, 5), 'cycle'),
                ((0, 1, 5), 2, Q(1, 5), 'clique'),
                ((0, 7, 8), 2, Q(1, 5), 'clique'),
                ((1, 2, 8), 2, Q(1, 5), 'clique'),
                ((2, 6, 8), 2, Q(1, 5), 'clique'),
                ((3, 4, 5), 2, Q(4, 5), 'clique'),
                ((6, 7, 8), 2, Q(2, 5), 'clique')]
    for labels, d, weight, kind in raw_rows:
        required = ({edge(labels[i], labels[(i + 1) % len(labels)]) for i in range(len(labels))}
                    if kind == 'cycle' else {edge(u, v) for u, v in combinations(labels, 2)})
        assert required <= intact and weight >= 0
        assert d == ((len(labels) + 1) // 2 if kind == 'cycle' else len(labels) - 1)
    loads = {v: sum(w for s, _, w, _ in raw_rows if v in s) for v in vertices}
    dual = sum(d * w for _, d, w, _ in raw_rows) - sum(max(Q(0), l - 1) for l in loads.values())
    assert set(loads.values()) == {Q(1)} and dual == Q(29, 5)
    # Point satisfying just the two rounded scalar rows, at objective five.
    omitted = {0, 1, 2, 3, 6}
    assert len(omitted & a) == len(omitted & b) == 4 and len(omitted) == 5
    assert not independent(vertices - omitted, intact)
    fixtures['intact']['old_row_dual'] = str(dual)

    rows = [r for r in fixtures['count_only_false_yes']['states'] if r['total'] is not None]
    quotiented = max(q + max(r['a'] for r in rows if len(r['selected']) == q)
                     + max(r['b'] for r in rows if len(r['selected']) == q)
                     for q in {len(r['selected']) for r in rows})
    assert quotiented == 5 > fixtures['count_only_false_yes']['alpha']
    fixtures['count_only_false_yes']['unsafe_count_summary'] = quotiented

    # Safe quotient for one fixed, already computed future table B.
    # Retain the maximizing boundary ID assignment and reconstruct its witness.
    for name, edges in [('intact', intact), ('one_edge_yes', altered),
                        ('count_only_false_yes', identity)]:
        rows = [r for r in fixtures[name]['states'] if r['total'] is not None]
        classes = []
        for future_score in sorted({r['b'] for r in rows}):
            members = [r for r in rows if r['b'] == future_score]
            chosen = max(members, key=lambda r: len(r['selected']) + r['a'])
            classes.append({'future_score': future_score,
                            'members': [r['selected'] for r in members],
                            'chosen': chosen['selected'], 'total': chosen['total']})
        best = max(classes, key=lambda row: row['total'])
        sigma = frozenset(best['chosen'])
        pieces = [max((s for s in subsets(bag - (a & b)) if independent(s | sigma, edges)),
                      key=len) for bag in (a, b)]
        witness = sigma | pieces[0] | pieces[1]
        assert len(witness) == best['total'] == fixtures[name]['alpha']
        assert independent(witness, edges) and len(classes) == 2
        fixtures[name]['fixed_context_classes'] = classes
        fixtures[name]['fixed_context_witness'] = sorted(witness)

    # Zero boundary: one table entry still contains the entire local optimum.
    zero_vertices = frozenset(range(5))
    zero_edges = {edge(i, (i + 1) % 5) for i in range(5)}
    zero_rows = boundary_rows(zero_vertices, zero_edges, frozenset(), zero_vertices)
    assert len(zero_rows) == 1 and zero_rows[0]['total'] == exhaustive(zero_vertices, zero_edges)[0] == 2

    # A real three-bag fork exercises the tree composition and every root.
    c = frozenset((3, 4, 9, 10, 11, 12))
    fork_edges = intact | wheel((3, 4, 9, 10, 11), 12)
    fork_vertices = vertices | c
    truth, _, _ = exhaustive(fork_vertices, fork_edges)
    fork_runs = [tree_alpha(fork_vertices, fork_edges, [a, b, c], [(0, 1), (0, 2)], r)
                 for r in range(3)]
    assert all(r[0] == truth and r[2] == 192 for r in fork_runs)

    invalid = [reject(vertices, intact | {(3, 6)}, [a, b], [(0, 1)], 'edge coverage'),
               reject(frozenset((0, 1, 2)), {(0, 1), (1, 2), (0, 2)},
                      [frozenset((0, 1)), frozenset((1, 2)), frozenset((0, 2))],
                      [(0, 1), (1, 2)], 'running intersection'),
               reject(frozenset(range(7)), set(), [frozenset(range(7))], [], 'bag contract'),
               reject(frozenset(range(5)), set(), [frozenset(range(4)), frozenset(range(5))],
                      [(0, 1)], 'separator contract')]
    assert tree_alpha(frozenset(), set(), [frozenset()], [])[0] == 0
    assert tree_alpha(frozenset((0,)), set(), [frozenset((0,))], [])[0] == 1

    # Large explicit family: t wheels sharing the same three-vertex rim path.
    t = 100
    bags, family_edges = [], set()
    for i in range(t):
        u, v, h = 3 + 3*i, 4 + 3*i, 5 + 3*i
        bags.append(frozenset((0, 1, 2, u, v, h)))
        family_edges |= wheel((0, 1, 2, u, v), h)
    family_vertices = frozenset().union(*bags)
    run = tree_alpha(family_vertices, family_edges, bags, [(0, i) for i in range(1, t)])
    assert len(family_vertices) == 303 and run[0] == 101 and run[2] == 6400 and run[3] <= 8

    # Any two distinct boundary states admit a one-vertex distinguishing context.
    # Exhaustive ordered pairs at boundary sizes 0..6; not a universal theorem.
    pairs_checked = 0
    for size in range(7):
        states = list(subsets(range(size)))
        for left in states:
            for right in states:
                if left == right:
                    continue
                v = min(left ^ right)
                z = size
                test_edge = {(v, z)}
                assert independent(left | {z}, test_edge) != independent(right | {z}, test_edge)
                pairs_checked += 1
    assert pairs_checked == 5334

    result = {'schema': 'redogit/dean-boundary-probe/v1', 'source_base':
              'cd6d3329109cf114a3466332487dc69a7aff2104', 'result': 'PASS',
              'fixtures': fixtures, 'fork_alpha': truth, 'fork_roots_checked': 3,
              'fork_subsets_checked': 8192, 'rejected_contracts': invalid,
              'family': {'wheels': t, 'vertices': 303, 'alpha': run[0],
                         'local_candidates': run[2], 'max_message_states': run[3]},
              'boundary_distinguishing_pairs_checked': pairs_checked}
    result['zero_boundary'] = {'states': len(zero_rows), 'alpha': zero_rows[0]['total']}
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print('PASS Steps 19-25: pair, old-row control, identity counterexample, tree gate, context separation, safe fixed-context quotient, one-entry boundary')
    print(json.dumps({'fixture_alphas': {k: v['alpha'] for k, v in fixtures.items()},
                      'old_row_dual': str(dual), 'count_summary_false_value': quotiented,
                      'family': result['family'], 'context_pairs': pairs_checked}, sort_keys=True))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
