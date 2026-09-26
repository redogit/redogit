#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product
import json
import random

SEED = 20260926
RANDOM_TRIALS = 1000


def discrete_partition(n):
    return tuple((i,) for i in range(n))


def join_edge(partition, edge):
    edge = set(edge)
    merged = set()
    keep = []
    for block in partition:
        s = set(block)
        if s & edge:
            merged |= s
        else:
            keep.append(tuple(block))
    keep.append(tuple(sorted(merged)))
    keep.sort(key=lambda b: (b[0], len(b), b))
    return tuple(keep)


def full_partition_states(n, edges):
    states = {discrete_partition(n)}
    widths = [1]
    for edge in edges:
        states |= {join_edge(p, edge) for p in tuple(states)}
        widths.append(len(states))
    return states, widths


def signed_coefficients(n, edges):
    coeff = {discrete_partition(n): 1}
    widths = [1]
    for edge in edges:
        new = defaultdict(int)
        for partition, value in coeff.items():
            new[partition] += value
            new[join_edge(partition, edge)] -= value
        coeff = {p: v for p, v in new.items() if v != 0}
        widths.append(len(coeff))
    return coeff, widths


def count_from_coefficients(coeff):
    return sum(value * (1 << len(partition)) for partition, value in coeff.items())


def brute_count(n, edges):
    total = 0
    for coloring in product((0, 1), repeat=n):
        if all(len({coloring[v] for v in edge}) > 1 for edge in edges):
            total += 1
    return total


def random_cubic_3uniform(n, rng, retries=2000):
    stubs = [v for v in range(n) for _ in range(3)]
    for _ in range(retries):
        rng.shuffle(stubs)
        edges = []
        seen = set()
        valid = True
        for i in range(0, len(stubs), 3):
            edge = tuple(sorted(stubs[i:i + 3]))
            if len(set(edge)) != 3 or edge in seen:
                valid = False
                break
            seen.add(edge)
            edges.append(edge)
        if not valid:
            continue

        adj = [set() for _ in range(n)]
        for edge in edges:
            for a, b in combinations(edge, 2):
                adj[a].add(b)
                adj[b].add(a)
        seen_vertices = {0}
        stack = [0]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen_vertices:
                    seen_vertices.add(v)
                    stack.append(v)
        if len(seen_vertices) == n:
            return edges
    return None


def known_witnesses():
    return {
        "FANO": (
            7,
            [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)],
        ),
        "FULL_RANK_SAT7": (
            7,
            [(0,3,6),(0,1,4),(0,2,5),(1,4,6),(1,2,3),(1,5,6),(3,4,6)],
        ),
        "SAT_GIRTH6_N10": (
            10,
            [(3,6,9),(2,4,6),(7,8,9),(2,5,9),(1,5,7),
             (0,3,8),(0,4,7),(1,3,4),(0,5,6),(1,2,8)],
        ),
    }


def witness_panel():
    rows = {}
    for name, (n, edges) in known_witnesses().items():
        states, full_widths = full_partition_states(n, edges)
        coeff, coeff_widths = signed_coefficients(n, edges)
        rows[name] = {
            "vertices": n,
            "edges": edges,
            "full_equality_partition_states": len(states),
            "final_nonzero_coefficient_states": len(coeff),
            "maximum_full_prefix_width": max(full_widths),
            "maximum_active_coefficient_width": max(coeff_widths),
            "coefficient_count": count_from_coefficients(coeff),
            "brute_count": brute_count(n, edges),
        }
    return rows


def random_panel():
    rng = random.Random(SEED)
    tested = 0
    mismatches = 0
    best = None

    for _ in range(RANDOM_TRIALS):
        n = rng.choice((6, 7, 8, 9))
        edges = random_cubic_3uniform(n, rng)
        if edges is None:
            continue

        states, full_widths = full_partition_states(n, edges)
        coeff, coeff_widths = signed_coefficients(n, edges)

        exact = count_from_coefficients(coeff)
        brute = brute_count(n, edges)
        if exact != brute:
            mismatches += 1
            return {
                "tested": tested,
                "mismatches": mismatches,
                "failure": {"n": n, "edges": edges, "coefficient_count": exact, "brute_count": brute},
            }

        tested += 1
        reduction = len(states) - len(coeff)
        ratio = len(states) / max(1, len(coeff))
        candidate = (
            ratio,
            reduction,
            {
                "vertices": n,
                "edges": edges,
                "full_equality_partition_states": len(states),
                "final_nonzero_coefficient_states": len(coeff),
                "maximum_full_prefix_width": max(full_widths),
                "maximum_active_coefficient_width": max(coeff_widths),
                "model_count": exact,
            },
        )
        if best is None or candidate[:2] > best[:2]:
            best = candidate

    return {
        "seed": SEED,
        "requested_trials": RANDOM_TRIALS,
        "tested": tested,
        "mismatches": mismatches,
        "strongest_observed_state_reduction": best[2] if best else None,
    }


def main():
    print(json.dumps({
        "schema": "pnp-cubic-bond-coefficient-transfer-evidence/v1",
        "date": "2026-09-26",
        "claim_ceiling": "BOUNDED_VALIDATION_ONLY; theorem requires separate proof",
        "witness_panel": witness_panel(),
        "random_panel": random_panel(),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
