#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product
import json
import random

SEED_DECISION = 20260926
SEED_HOMEWARD = 20260927
TRIALS = 1000
NONE = -1


def normalize_partition(blocks):
    out = [tuple(sorted(b)) for b in blocks if b]
    out.sort(key=lambda b: (b[0], len(b), b))
    return tuple(out)


def discrete_partition(vertices):
    return tuple((v,) for v in sorted(vertices))


def join_edge(partition, edge):
    e = set(edge)
    merged = set()
    keep = []
    for block in partition:
        s = set(block)
        if s & e:
            merged |= s
        else:
            keep.append(block)
    if merged:
        keep.append(tuple(sorted(merged)))
    return normalize_partition(keep)


def project_partition(partition, active, q=2):
    active = set(active)
    keep = []
    factor = 1
    for block in partition:
        remaining = tuple(v for v in block if v in active)
        if remaining:
            keep.append(remaining)
        else:
            factor *= q
    return normalize_partition(keep), factor


def future_sets(edges):
    future = [set() for _ in range(len(edges) + 1)]
    acc = set()
    for i in range(len(edges) - 1, -1, -1):
        acc |= set(edges[i])
        future[i] = set(acc)
    return future


def decision_frontier_count(n, edges):
    future = future_sets(edges)
    incident = future[0]
    free = n - len(incident)

    coeff = {discrete_partition(incident): 1}
    widths = [1]

    for i, edge in enumerate(edges):
        tmp = defaultdict(int)
        for partition, value in coeff.items():
            tmp[partition] += value
            tmp[join_edge(partition, edge)] -= value

        new = defaultdict(int)
        for partition, value in tmp.items():
            if value == 0:
                continue
            projected, factor = project_partition(partition, future[i + 1])
            new[projected] += value * factor

        coeff = {p: v for p, v in new.items() if v != 0}
        widths.append(len(coeff))

    return sum(coeff.values()) * (1 << free), widths


def normalize_labeled(items):
    out = [(tuple(sorted(block)), label) for block, label in items if block]
    out.sort(key=lambda x: (x[0][0], len(x[0]), x[0], x[1]))
    return tuple(out)


def merge_labels(labels):
    fixed = {x for x in labels if x != NONE}
    if len(fixed) > 1:
        return None
    return next(iter(fixed)) if fixed else NONE


def join_labeled(state, edge):
    e = set(edge)
    merged = set()
    labels = []
    keep = []
    for block, label in state:
        s = set(block)
        if s & e:
            merged |= s
            labels.append(label)
        else:
            keep.append((block, label))

    label = merge_labels(labels)
    if label is None:
        return None

    if merged:
        keep.append((tuple(sorted(merged)), label))
    return normalize_labeled(keep)


def project_labeled(state, active, q=2):
    active = set(active)
    keep = []
    factor = 1
    for block, label in state:
        remaining = tuple(v for v in block if v in active)
        if remaining:
            keep.append((remaining, label))
        else:
            factor *= 1 if label != NONE else q
    return normalize_labeled(keep), factor


def conditional_frontier_count(n, edges, alpha, cap=None):
    future = future_sets(edges)
    incident = future[0]
    free_vertices = set(range(n)) - incident
    free_factor = 1 << sum(1 for v in free_vertices if v not in alpha)

    initial = tuple(((v,), alpha.get(v, NONE)) for v in sorted(incident))
    coeff = {initial: 1}
    widths = [1]

    for i, edge in enumerate(edges):
        tmp = defaultdict(int)
        for state, value in coeff.items():
            tmp[state] += value
            joined = join_labeled(state, edge)
            if joined is not None:
                tmp[joined] -= value

        new = defaultdict(int)
        for state, value in tmp.items():
            if value == 0:
                continue
            projected, factor = project_labeled(state, future[i + 1])
            new[projected] += value * factor

        coeff = {s: v for s, v in new.items() if v != 0}
        widths.append(len(coeff))

        if cap is not None and len(coeff) > cap:
            return None, widths, False

    return sum(coeff.values()) * free_factor, widths, True


def brute_count(n, edges, alpha=None):
    alpha = {} if alpha is None else dict(alpha)
    free = [v for v in range(n) if v not in alpha]
    total = 0
    for values in product((0, 1), repeat=len(free)):
        coloring = dict(alpha)
        coloring.update(dict(zip(free, values)))
        if all(len({coloring[v] for v in edge}) > 1 for edge in edges):
            total += 1
    return total


def reconstruct(n, edges, cap=None):
    total, widths, ok = conditional_frontier_count(n, edges, {}, cap)
    max_width = max(widths)
    if not ok:
        return None, max_width, False, "CAP"
    if total == 0:
        return None, max_width, True, "UNSAT"

    alpha = {}
    for v in range(n):
        trial = dict(alpha)
        trial[v] = 0
        count0, w0, ok0 = conditional_frontier_count(n, edges, trial, cap)
        max_width = max(max_width, max(w0))
        if not ok0:
            return None, max_width, False, "CAP"

        if count0 > 0:
            alpha[v] = 0
        else:
            alpha[v] = 1
            count1, w1, ok1 = conditional_frontier_count(n, edges, alpha, cap)
            max_width = max(max_width, max(w1))
            if not ok1 or count1 <= 0:
                return None, max_width, False, "RECONSTRUCTION"

    return alpha, max_width, True, "SAT"


def random_cubic(n, rng, retries=2000):
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

        reached = {0}
        stack = [0]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in reached:
                    reached.add(v)
                    stack.append(v)

        if len(reached) == n:
            return edges
    return None


def decision_panel():
    rng = random.Random(SEED_DECISION)
    tested = mismatches = 0
    max_width = 0

    for _ in range(TRIALS):
        n = rng.choice((6, 7, 8, 9))
        edges = random_cubic(n, rng)
        if edges is None:
            continue

        exact, widths = decision_frontier_count(n, edges)
        brute = brute_count(n, edges)
        if exact != brute:
            mismatches += 1
            break

        tested += 1
        max_width = max(max_width, max(widths))

    return {
        "seed": SEED_DECISION,
        "requested_trials": TRIALS,
        "tested": tested,
        "mismatches": mismatches,
        "maximum_projected_decision_width_observed": max_width,
    }


def homeward_panel():
    rng = random.Random(SEED_HOMEWARD)
    tested = failures = invalid = 0
    max_width = 0

    for _ in range(TRIALS):
        n = rng.choice((6, 7, 8, 9))
        edges = random_cubic(n, rng)
        if edges is None:
            continue

        brute = brute_count(n, edges)
        coloring, width, ok, status = reconstruct(n, edges)
        max_width = max(max_width, width)

        if not ok or ((brute > 0) != (coloring is not None)):
            failures += 1
            break

        if coloring is not None:
            if not all(len({coloring[v] for v in edge}) > 1 for edge in edges):
                invalid += 1
                break

        tested += 1

    return {
        "seed": SEED_HOMEWARD,
        "requested_trials": TRIALS,
        "tested": tested,
        "failures": failures,
        "invalid_returned_colorings": invalid,
        "maximum_labeled_homeward_width_observed": max_width,
    }


def main():
    print(json.dumps({
        "schema": "pnp-cubic-frontier-projection-evidence/v1",
        "date": "2026-09-26",
        "claim_ceiling": "BOUNDED_VALIDATION_ONLY; theorem requires separate proof",
        "decision_panel": decision_panel(),
        "homeward_panel": homeward_panel(),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
