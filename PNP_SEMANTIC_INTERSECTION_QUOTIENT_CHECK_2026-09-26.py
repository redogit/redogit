#!/usr/bin/env python3
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import comb
import json
import random

SEED = 20260926
RANDOM_TRIALS = 5000


def canonical_clause(lits):
    signs = {}
    for lit in lits:
        v = abs(lit) - 1
        s = 1 if lit > 0 else -1
        if v in signs and signs[v] != s:
            return None
        signs[v] = s
    return tuple(sorted(signs.items()))


def cleanup_cnf(clauses):
    unique = sorted({c for c in clauses if c is not None}, key=lambda c: (len(c), c))
    kept, kept_sets = [], []
    for c in unique:
        sc = frozenset(c)
        if any(k.issubset(sc) for k in kept_sets):
            continue
        kept.append(c)
        kept_sets.append(sc)
    return kept


def falsifying_signature(clause):
    return tuple((v, 0 if sign == 1 else 1) for v, sign in clause)


def compatible_join(a, b):
    out = dict(a)
    for v, value in b:
        prev = out.get(v)
        if prev is not None and prev != value:
            return None
        out[v] = value
    return tuple(sorted(out.items()))


def intersection_semilattice(signatures, cap=None):
    states = {()}
    for sig in signatures:
        additions = []
        for state in tuple(states):
            joined = compatible_join(state, sig)
            if joined is not None:
                additions.append(joined)
        states.update(additions)
        if cap is not None and len(states) > cap:
            return states, False
    return states, True


def mobius_values(states):
    ordered = sorted(states, key=lambda s: (len(s), s))
    as_sets = {s: frozenset(s) for s in ordered}
    mu = {}
    for state in ordered:
        if not state:
            mu[state] = 1
            continue
        fs = as_sets[state]
        subtotal = 0
        for lower in ordered:
            if len(lower) >= len(state):
                break
            if as_sets[lower].issubset(fs):
                subtotal += mu[lower]
        mu[state] = -subtotal
    return mu


def quotient_model_count(n, cnf):
    states, completed = intersection_semilattice([falsifying_signature(c) for c in cnf])
    assert completed
    mu = mobius_values(states)
    return sum(mu[s] * (1 << (n - len(s))) for s in states)


def brute_model_count(n, cnf):
    count = 0
    for assignment in product((0, 1), repeat=n):
        ok = True
        for clause in cnf:
            if not any(
                (sign == 1 and assignment[v] == 1)
                or (sign == -1 and assignment[v] == 0)
                for v, sign in clause
            ):
                ok = False
                break
        count += int(ok)
    return count


def compatible_subset_count(cnf):
    signatures = [falsifying_signature(c) for c in cnf]
    m = len(signatures)
    total = 0
    for mask in range(1, 1 << m):
        state = ()
        valid = True
        for i, sig in enumerate(signatures):
            if (mask >> i) & 1:
                state = compatible_join(state, sig)
                if state is None:
                    valid = False
                    break
        total += int(valid)
    return total


def threshold_family(p):
    r = (p + 1) // 2
    out = []
    for subset in combinations(range(p), r):
        out.append(tuple((v, 1) for v in subset))
    for subset in combinations(range(p), r):
        out.append(tuple((v, -1) for v in subset))
    return out


def exact_rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c] != 0), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        pv = a[r][c]
        a[r] = [x / pv for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [a[i][j] - f * a[r][j] for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def nae_pair_cnf(edges):
    cnf = []
    for edge in edges:
        cnf.append(tuple((v, 1) for v in edge))
        cnf.append(tuple((v, -1) for v in edge))
    return cnf


def random_panel():
    random.seed(SEED)
    tested = 0
    mismatches = 0
    quotient_failures = 0
    max_ratio = 0.0
    max_case = None
    for _ in range(RANDOM_TRIALS):
        n = random.randint(2, 8)
        raw = []
        for _ in range(random.randint(1, 10)):
            width = random.randint(1, min(4, n))
            vars_ = random.sample(range(n), width)
            lits = [(v + 1) * (1 if random.random() < 0.5 else -1) for v in vars_]
            raw.append(canonical_clause(lits))
        cnf = cleanup_cnf(raw)
        if not cnf:
            continue
        if quotient_model_count(n, cnf) != brute_model_count(n, cnf):
            mismatches += 1
            break
        raw_events = compatible_subset_count(cnf)
        states, _ = intersection_semilattice([falsifying_signature(c) for c in cnf])
        semantic_events = len(states) - 1
        if semantic_events > raw_events:
            quotient_failures += 1
            break
        ratio = raw_events / max(1, semantic_events)
        if ratio > max_ratio:
            max_ratio = ratio
            max_case = {
                "variables": n,
                "clauses": len(cnf),
                "raw_events": raw_events,
                "semantic_events": semantic_events,
            }
        tested += 1
    return {
        "seed": SEED,
        "requested_trials": RANDOM_TRIALS,
        "tested": tested,
        "model_count_mismatches": mismatches,
        "semantic_event_gt_raw_event_failures": quotient_failures,
        "largest_observed_raw_to_semantic_ratio": max_ratio,
        "largest_ratio_case": max_case,
    }


def separation_panel():
    rows = []
    for p in (3, 5, 7, 9):
        r = (p + 1) // 2
        M = comb(p, r)
        cnf = threshold_family(p)
        states, _ = intersection_semilattice([falsifying_signature(c) for c in cnf])
        rows.append({
            "p": p,
            "r": r,
            "clauses": len(cnf),
            "same_sign_clique_size_M": M,
            "raw_nonempty_conformal_cliques": 2 * ((1 << M) - 1),
            "semantic_intersection_states_including_universe": len(states),
            "closed_form_semantic_states": (1 << p) + 1,
            "model_count": quotient_model_count(p, cnf),
        })
    return rows


def overlap_counterexample():
    fano = [
        (0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)
    ]
    sat = [
        (0,3,6),(0,1,4),(0,2,5),(1,4,6),(1,2,3),(1,5,6),(3,4,6)
    ]
    rows = []
    for name, edges in (("FANO_UNSAT", fano), ("FULL_RANK_SAT", sat)):
        cnf = nae_pair_cnf(edges)
        states, _ = intersection_semilattice([falsifying_signature(c) for c in cnf])
        incidence = [[1 if v in e else 0 for v in range(7)] for e in edges]
        rows.append({
            "name": name,
            "vertices": 7,
            "hyperedges": 7,
            "cnf_clauses": 14,
            "incidence_rank_over_Q": exact_rank(incidence),
            "positive_balance_cover": "7 pairwise-disjoint (+edge,-edge) 2-circuits with unit coefficients",
            "balance_circuit_overlap_graph": "7 isolated circuit vertices",
            "semantic_intersection_states_including_universe": len(states),
            "model_count": brute_model_count(7, cnf),
            "edges": edges,
        })
    return {
        "statement": "same balance-circuit overlap object and same n/m/rank counts, opposite SAT status",
        "instances": rows,
    }


def main():
    print(json.dumps({
        "schema": "pnp-semantic-intersection-quotient-evidence/v1",
        "date": "2026-09-26",
        "claim_ceiling": "BOUNDED_VALIDATION_ONLY; theorem requires separate proof",
        "random_panel": random_panel(),
        "strict_separation_family": separation_panel(),
        "overlap_only_counterexample": overlap_counterexample(),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
