#!/usr/bin/env python3
"""Exact finite checks for Dean Steps 30-34. Standard library only.

The default recognition/optimization route allows at most one vertex outside
a bipartite induced graph. General supplied-set enumeration is separately
gated by an explicit cap. Failure of admission returns UNKNOWN for MIS.
"""
from __future__ import annotations

from collections import deque
from itertools import combinations
import copy
import json
from pathlib import Path
import sys


class Graph:
    def __init__(self, vertices, edges):
        self.V = tuple(sorted(vertices))
        assert len(set(self.V)) == len(self.V)
        assert all(type(v) is int and v >= 0 for v in self.V)
        self.E = tuple(sorted(tuple(sorted(e)) for e in edges))
        assert len(set(self.E)) == len(self.E)
        assert all(len(e) == 2 and e[0] != e[1] and set(e) <= set(self.V) for e in self.E)
        self.adj = {v: set() for v in self.V}
        for u, v in self.E:
            self.adj[u].add(v)
            self.adj[v].add(u)

    def induced(self, vertices):
        keep = set(vertices)
        assert keep <= set(self.V)
        return Graph(keep, [(u, v) for u, v in self.E if u in keep and v in keep])

    def identity(self):
        return {"vertices": list(self.V), "edges": [list(e) for e in self.E]}


def independent(g, selected):
    s = set(selected)
    return len(s) == len(selected) and s <= set(g.V) and all(u not in s or v not in s for u, v in g.E)


def powerset(ids):
    ids = tuple(ids)
    for mask in range(1 << len(ids)):
        yield tuple(v for i, v in enumerate(ids) if mask & (1 << i))


def truth(g):
    assert len(g.V) <= 18, "independent exhaustive oracle cap"
    best = ()
    for s in powerset(g.V):
        if len(s) > len(best) and independent(g, s):
            best = s
    return len(best), list(best)


def valid_odd_cycle(g, cycle):
    return len(cycle) >= 3 and len(cycle) % 2 == 1 and len(set(cycle)) == len(cycle) and all(v in g.adj for v in cycle) and all(cycle[(i+1) % len(cycle)] in g.adj[v] for i, v in enumerate(cycle))


def bipartition(g):
    color, parent, depth = {}, {}, {}
    for root in g.V:
        if root in color:
            continue
        color[root], parent[root], depth[root] = 0, None, 0
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in sorted(g.adj[u]):
                if v not in color:
                    color[v], parent[v], depth[v] = 1-color[u], u, depth[u]+1
                    queue.append(v)
                elif color[v] == color[u]:
                    a, b, left, right = u, v, [], []
                    while depth[a] > depth[b]:
                        left.append(a); a = parent[a]
                    while depth[b] > depth[a]:
                        right.append(b); b = parent[b]
                    while a != b:
                        left.append(a); right.append(b)
                        a, b = parent[a], parent[b]
                    cycle = left + [a] + list(reversed(right))
                    assert valid_odd_cycle(g, cycle)
                    return {"bipartite": False, "odd_cycle": cycle}
    return {"bipartite": True, "left": [v for v in g.V if color[v] == 0], "right": [v for v in g.V if color[v] == 1]}


def matching_certificate(g):
    coloring = bipartition(g)
    assert coloring["bipartite"]
    left, right = coloring["left"], coloring["right"]
    ml, mr = {}, {}
    for start in left:
        queue, visited_left, predecessor = deque([start]), {start}, {}
        free = None
        while queue and free is None:
            u = queue.popleft()
            for v in sorted(g.adj[u]):
                if v in predecessor or ml.get(u) == v:
                    continue
                predecessor[v] = u
                if v not in mr:
                    free = v
                    break
                next_left = mr[v]
                if next_left not in visited_left:
                    visited_left.add(next_left); queue.append(next_left)
        while free is not None:
            u = predecessor[free]
            old = ml.get(u)
            ml[u], mr[free] = free, u
            free = old
    zl, zr = set(left)-set(ml), set()
    queue = deque(sorted(zl))
    while queue:
        u = queue.popleft()
        for v in sorted(g.adj[u]):
            if ml.get(u) == v or v in zr:
                continue
            zr.add(v)
            assert v in mr, "augmenting path remained"
            if mr[v] not in zl:
                zl.add(mr[v]); queue.append(mr[v])
    cover = sorted((set(left)-zl) | zr)
    witness = sorted(set(g.V)-set(cover))
    result = {"matching": [[u, ml[u]] for u in sorted(ml)], "cover": cover, "witness": witness, "alpha": len(witness)}
    verify_matching(g, result)
    return result


def verify_matching(g, cert):
    matching = cert["matching"]
    endpoints = [v for e in matching for v in e]
    assert all(len(e) == 2 and tuple(sorted(e)) in g.E for e in matching)
    assert len(set(endpoints)) == len(endpoints)
    cover = cert["cover"]
    assert len(set(cover)) == len(cover) and set(cover) <= set(g.V)
    assert all(u in cover or v in cover for u, v in g.E)
    assert len(cover) == len(matching)
    assert cert["witness"] == sorted(set(g.V)-set(cover))
    assert cert["alpha"] == len(g.V)-len(matching)
    assert independent(g, cert["witness"])


def solve_given_transversal(g, X, cap):
    X = tuple(sorted(X))
    assert len(X) == len(set(X)) and set(X) <= set(g.V)
    if len(X) > cap:
        return {"status": "UNKNOWN", "reason": "declared transversal cap exceeded"}
    base = g.induced(set(g.V)-set(X))
    if not bipartition(base)["bipartite"]:
        return {"status": "UNKNOWN", "reason": "deletion does not leave a bipartite graph"}
    branches = []
    for selected in powerset(X):
        if not independent(g, selected):
            continue
        forbidden = set(X)
        for v in selected:
            forbidden |= g.adj[v]
        residual = g.induced(set(g.V)-forbidden)
        cert = matching_certificate(residual)
        branches.append({"selected": list(selected), "remaining": list(residual.V), "certificate": cert, "score": len(selected)+cert["alpha"]})
    best = max(branches, key=lambda b: b["score"])
    answer = {"status": "EXACT", "context": g.identity(), "X": list(X), "branches": branches, "alpha": best["score"], "witness": sorted(best["selected"]+best["certificate"]["witness"])}
    verify_answer(g, answer, cap)
    return answer


def verify_answer(g, answer, cap):
    assert answer["status"] == "EXACT" and answer["context"] == g.identity()
    X = answer["X"]
    assert len(X) == len(set(X)) and set(X) <= set(g.V) and len(X) <= cap
    assert bipartition(g.induced(set(g.V)-set(X)))["bipartite"]
    expected = {s for s in powerset(X) if independent(g, s)}
    observed = [tuple(b["selected"]) for b in answer["branches"]]
    assert len(observed) == len(set(observed)) and set(observed) == expected
    for branch in answer["branches"]:
        blocked = set(X)
        for v in branch["selected"]:
            blocked |= g.adj[v]
        residual = g.induced(set(g.V)-blocked)
        assert branch["remaining"] == list(residual.V)
        verify_matching(residual, branch["certificate"])
        assert branch["score"] == len(branch["selected"])+branch["certificate"]["alpha"]
    assert answer["alpha"] == max(b["score"] for b in answer["branches"])
    assert len(answer["witness"]) == answer["alpha"] and independent(g, answer["witness"])


def discover_one(g):
    first = bipartition(g)
    if first["bipartite"]:
        return {"status": "ADMITTED", "X": [], "candidate_tests": 0}
    cycle, rejected = first["odd_cycle"], []
    for v in sorted(cycle):
        rest = bipartition(g.induced(set(g.V)-{v}))
        if rest["bipartite"]:
            return {"status": "ADMITTED", "X": [v], "odd_cycle": cycle, "rejected_candidates": rejected, "candidate_tests": len(rejected)+1}
        rejected.append({"vertex": v, "surviving_odd_cycle": rest["odd_cycle"]})
    answer = {"status": "UNKNOWN", "scope_fact": "no transversal of size at most one", "odd_cycle": cycle, "rejected_candidates": rejected, "candidate_tests": len(rejected)}
    verify_rejection(g, answer)
    return answer


def verify_rejection(g, result):
    cycle = result["odd_cycle"]
    assert valid_odd_cycle(g, cycle)
    rejections = result["rejected_candidates"]
    assert sorted(r["vertex"] for r in rejections) == sorted(cycle)
    for r in rejections:
        assert r["vertex"] not in r["surviving_odd_cycle"]
        assert valid_odd_cycle(g, r["surviving_odd_cycle"])


def graphs(n):
    pairs = tuple(combinations(range(n), 2))
    for edges in powerset(pairs):
        yield Graph(range(n), edges)


def energy(g, selected):
    s = set(selected)
    return -len(s) + sum(u in s and v in s for u, v in g.E)


def switched_pair_delta(g, flipped, u, v):
    def at(a, b):
        y = ({u} if a else set()) | ({v} if b else set())
        return energy(g, y ^ set(flipped))
    return at(0, 0)+at(1, 1)-at(1, 0)-at(0, 1)


def triangle_chain(t):
    edges = []
    for i in range(t):
        edges += list(combinations(range(3*i, 3*i+3), 2))
        if i:
            edges.append((3*i-3, 3*i))
    return Graph(range(3*t), edges)


def expect_rejection(action):
    try:
        action()
    except AssertionError:
        return
    raise AssertionError("corrupted certificate accepted")


def main(output):
    total = admitted = bipartite = rejected = flips = pair_deltas = branches = 0
    by_n = []
    for n in range(6):
        row = {"n": n, "graphs": 0, "bipartite": 0, "one_vertex": 0, "outside_cap": 0}
        for g in graphs(n):
            total += 1; row["graphs"] += 1
            coloring = bipartition(g)
            if coloring["bipartite"]:
                bipartite += 1; row["bipartite"] += 1
            else:
                assert valid_odd_cycle(g, coloring["odd_cycle"])
            valid_flips = 0
            for flipped in powerset(g.V):
                flips += 1
                ok = True
                for u, v in g.E:
                    delta = switched_pair_delta(g, flipped, u, v)
                    assert delta == (-1 if ((u in flipped) != (v in flipped)) else 1)
                    ok &= delta <= 0
                    pair_deltas += 1
                valid_flips += ok
            assert bool(valid_flips) == coloring["bipartite"]
            gate = discover_one(g)
            independently_admitted = coloring["bipartite"] or any(bipartition(g.induced(set(g.V)-{v}))["bipartite"] for v in g.V)
            assert (gate["status"] == "ADMITTED") == independently_admitted
            if gate["status"] == "ADMITTED":
                answer = solve_given_transversal(g, gate["X"], 1)
                assert answer["alpha"] == truth(g)[0]
                branches += len(answer["branches"]); admitted += 1
                if gate["X"]:
                    row["one_vertex"] += 1
                roundtrip = json.loads(json.dumps(answer))
                verify_answer(g, roundtrip, 1)
                for k in range(n+2):
                    assert (answer["alpha"] >= k) == (truth(g)[0] >= k)
            else:
                verify_rejection(g, gate)
                rejected += 1; row["outside_cap"] += 1
        by_n.append(row)
    bowtie = Graph(range(5), [(0,1),(1,4),(0,4),(2,3),(3,4),(2,4)])
    bowgate = discover_one(bowtie)
    assert bowgate["X"] == [4] and [r["vertex"] for r in bowgate["rejected_candidates"]] == [0,1]
    bowanswer = solve_given_transversal(bowtie, [4], 1)
    assert bowanswer["alpha"] == 2 and [b["score"] for b in bowanswer["branches"]] == [2,1]
    c9 = Graph(range(9), [(i,(i+1)%9) for i in range(9)])
    c9answer = solve_given_transversal(c9, [0], 1)
    assert c9answer["alpha"] == 4 and [b["score"] for b in c9answer["branches"]] == [4,4]
    disconnected_obstructions = triangle_chain(2)
    assert discover_one(disconnected_obstructions)["status"] == "UNKNOWN"
    cap2 = solve_given_transversal(disconnected_obstructions, [1,4], 2)
    assert cap2["alpha"] == 2 and len(cap2["branches"]) == 4
    assert solve_given_transversal(disconnected_obstructions, [1,4], 1)["status"] == "UNKNOWN"
    assert solve_given_transversal(disconnected_obstructions, [1], 1)["status"] == "UNKNOWN"
    k4 = Graph(range(4), list(combinations(range(4),2)))
    adjacent_X = solve_given_transversal(k4, [0,1], 2)
    assert adjacent_X["alpha"] == 1 and len(adjacent_X["branches"]) == 3
    # A supplied two-vertex set is not assumed independent; invalid branches reject.
    corrupted = copy.deepcopy(adjacent_X)
    corrupted["branches"].append(copy.deepcopy(corrupted["branches"][0]))
    expect_rejection(lambda: verify_answer(k4, corrupted, 2))
    missing = copy.deepcopy(c9answer); missing["branches"].pop()
    expect_rejection(lambda: verify_answer(c9, missing, 1))
    inflated = copy.deepcopy(c9answer); inflated["branches"][0]["score"] += 1
    expect_rejection(lambda: verify_answer(c9, inflated, 1))
    invalid_match = copy.deepcopy(c9answer); invalid_match["branches"][0]["certificate"]["matching"] = [[1,3]]
    expect_rejection(lambda: verify_answer(c9, invalid_match, 1))
    missing_cover = copy.deepcopy(c9answer); missing_cover["branches"][0]["certificate"]["cover"] = []
    expect_rejection(lambda: verify_answer(c9, missing_cover, 1))
    p9 = Graph(c9.V, [e for e in c9.E if e != (0,1)])
    expect_rejection(lambda: verify_answer(p9, c9answer, 1))
    # Original IDs survive residuals, including nonconsecutive labels.
    renamed = Graph([10,20,30], [(10,20),(20,30),(10,30)])
    renameanswer = solve_given_transversal(renamed, [20], 1)
    assert renameanswer["alpha"] == 1 and independent(renamed, renameanswer["witness"])
    # Large block, bounded repair: K_20,20 plus a vertex joined to all forty.
    p, q, apex = range(20), range(20,40), 40
    large = Graph(range(41), [(u,v) for u in p for v in q]+[(u,apex) for u in range(40)])
    largegate = discover_one(large)
    assert largegate["X"] == [40]
    largeanswer = solve_given_transversal(large, [40], 1)
    assert largeanswer["alpha"] == 20 and [b["score"] for b in largeanswer["branches"]] == [20,1]
    # Linear local composition, despite arbitrarily large global OCT.
    chain = triangle_chain(100)
    witness = [3*i+1 for i in range(100)]
    assert independent(chain, witness) and len(witness) == 100
    assert all(all(v in chain.adj[u] for u,v in combinations(range(3*i,3*i+3),2)) for i in range(100))
    assert bipartition(chain.induced(set(chain.V)-set(witness)))["bipartite"]
    result = {
        "schema": "dean-parity-repair-result-v1", "status": "PASS",
        "exact_integer_arithmetic": True, "random_sampling": False,
        "exhaustive": {"max_vertices": 5, "graphs": total, "bipartite": bipartite, "admitted_at_cap_one": admitted, "outside_cap_one": rejected, "coordinate_flips": flips, "pair_mixed_differences": pair_deltas, "certified_branches": branches, "by_n": by_n},
        "bowtie": {"gate": bowgate, "branch_scores": [2,1], "alpha": 2},
        "C9": c9answer,
        "two_triangle_chain": {"cap_one": "UNKNOWN", "cap_two_alpha": cap2["alpha"], "cap_two_branches": 4},
        "adjacent_transversal": {"graph": "K4", "X": [0,1], "feasible_branches": 3, "alpha": 1},
        "counterprobes": {"duplicate_branch": "rejected", "missing_branch": "rejected", "inflated_score": "rejected", "invalid_matching": "rejected", "missing_cover": "rejected", "stale_graph": "rejected", "over_cap": "UNKNOWN", "invalid_transversal": "UNKNOWN", "nonconsecutive_ids": "passed"},
        "large_one_vertex_case": {"vertices": 41, "edges": len(large.E), "X": [40], "alpha": 20, "branch_scores": [20,1], "certificate": largeanswer},
        "triangle_chain": {"blocks": 100, "vertices": 300, "edges": len(chain.E), "alpha": 100, "minimum_odd_cycle_transversal": 100, "uniform_proof_in_receipt": True, "no_global_subset_enumeration": True},
        "claim_ceiling": "Exact admitted special case and finite corroboration; no unrestricted polynomial solver or P-versus-NP resolution."
    }
    Path(output).write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k: v for k,v in result.items() if k in ("status", "exhaustive", "counterprobes", "triangle_chain")}))


if __name__ == "__main__":
    main(sys.argv[1])
