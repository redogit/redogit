# Dean's fixed list — local rounding with one shared identity

**Status:** approved Step 18, following the [Step 17 wheel counterprobe](PNP_DEAN_FROZEN_CATALOG_WHEEL_GAP_2026-09-29.md). Test exactly one overlapping-wheel pair, with one deleted edge and the same target in both graphs. The existing clique/cycle evidence, seven-/nine-vertex carriers, and overlap formula remain the authority. This step verifies their composition; it introduces no graph-pattern catalog or discovery procedure.

## 1. Claim and proof dependencies

**Claim:** a verified lower bound on integral omissions *within a named vertex support* can be rounded there, then combined with other verified local bounds using the existing weighted overlap penalty. **Verdict: proved as written**, under that local-support hypothesis. This is a self-review with an exact finite counterprobe, not an independent external audit.

Write the supplied graph as G=(V,E), with selection target k and omission budget b=|V|-k. A valid omission vector y lies in {0,1}^V and covers every supplied edge. Let y(S) denote the sum of y_v over the distinct input IDs in S.

For each supplied support S_i, suppose its retained local proof establishes y(S_i) >= q_i, for an exact rational q_i. Integrality gives d_i=ceil(q_i) and y(S_i) >= d_i. For any supplied nonnegative rational weights lambda_i, put

\[
L_v=\sum_{i:v\in S_i}\lambda_i,\qquad
B=\sum_i\lambda_i d_i-\sum_{v\in V}\max(0,L_v-1).
\]

The [Step 14 proof](PNP_DEAN_MIXED_FRAME_DISCOVERY_2026-09-29.md) used only validity of the local inequalities, so it applies directly:

\[
\sum_i\lambda_i d_i\le\sum_v L_vy_v
\le\sum_v y_v+\sum_v\max(0,L_v-1),
\quad\text{hence}\quad y(V)\ge B.
\]

The last inequality uses 0<=y_v<=1. Thus B>b proves NO. A checked independent k-set proves YES; failure to cross the budget alone leaves UNKNOWN. The empty list gives zero, a single row gives its local conclusion, and repeated copies of one support are charged by their repeated IDs. For the displayed clique/cycle arithmetic receipts, verification is polynomial in their supplied length, the input, and rational bit lengths; this does not bound discovery cost or the length of proofs needed for arbitrary inputs.

**Support condition:** q_i must bound y(S_i), rather than a whole-graph quantity relabeled as local. If obtained from Step 14 rows, those rows must be contained in S_i and their internal load penalty must be computed there. After rounding, the parent formula recomputes loads from the named supports S_i. Every required input edge is rechecked before its evidence is used.

Dependency chain: supplied vertex IDs and edges -> checked clique/cycle rows -> Step 14 local rational sum -> integrality on that same support -> Step 13/14 overlap accounting -> comparison with the fixed budget. Every implication used here is proved in this receipt or its retained internal predecessors; no new external theorem is needed.

## 2. Exact NO graph and its one-edge YES opposite

Use vertex IDs 0,...,10. The shared hub is h=0. Rim A is the cyclic order (1,2,3,4,5), and rim B is (6,7,8,9,10). Each rim has its five consecutive cycle edges; h is adjacent to every rim vertex. There are no other edges. Supports S_A={0,1,2,3,4,5} and S_B={0,6,7,8,9,10} meet only at the same h. Thus n=11 and m=20. Fix **k=5, b=6** throughout the pair.

Inside each wheel, the existing rim-C5 row requires three omissions and each of its five hub triangles requires two. Weights 3/5 on the rim and 1/5 on each triangle load each of the six support vertices exactly once, giving q=19/5 and d=4. Unit weights on the two rounded conclusions give

\[
B=4+4-1=7>6.
\]

The single penalty is the shared hub's load two. This proves **NO**. Directly, selecting the hub permits no other vertex; omitting it allows at most two selections on each C5. The independent set {1,3,6,8} attains four, so alpha=4 and tau=7.

Now delete **only edge {5,1}**, preserving all IDs, the other 19 edges, k=5, and b=6. Rim A becomes path 1-2-3-4-5. Its local maximum is three, attained by {1,3,5}; rim B still has maximum two. The independent five-set

\[
\{1,3,5,7,9\}
\]

avoids h and all remaining edges. Hence alpha=5, tau=6, and this graph is **YES**.

The old rim-A C5 proof is rejected because {5,1} is absent. Three disjoint existing K2 rows on {0,1}, {2,3}, and {4,5} instead prove y(S_A)>=3. The intact wheel still gives y(S_B)>=4. Their correct composition is

\[
B=3+4-1=6=b.
\]

This bound is tight and does not reject the YES; the displayed witness establishes the YES verdict. Its omitted set is {0,2,4,6,8,10}, and h=0 is the *same omission* serving both local requirements.

| Same target k=5, b=6 | Edges | Local integer bounds | Shared-ID penalty | Correct B | Exact answer |
| --- | ---: | --- | ---: | ---: | --- |
| Two intact wheels | 20 | 4 + 4 | 1 | 7 | NO: alpha=4, tau=7 |
| Delete only {5,1} | 19 | 3 + 4 | 1 | 6 | YES: alpha=5, tau=6 |

## 3. Two false rules exposed by the same YES

1. **Forget the overlap:** even the freshly valid local conclusions 3+4 sum to 7>6. This falsely rejects the five-set because the omitted hub is counted twice. Subtracting the existing one-unit penalty repairs the error.
2. **Retain stale local evidence:** reusing 4 for the altered first wheel gives 4+4-1=7>6 even after correct overlap accounting. The missing required edge must invalidate that old local proof; an overlap penalty cannot repair an invalid premise.

This pair establishes sound composition, **not an extra rounding gain** over the older unrounded bound: for two intact wheels, (19/5)+(19/5)-1=33/5>6 already proves NO, and its global ceiling is also seven. Step 17 remains the separate disjoint five-wheel example where the order of local rounding retains an additional unit.

No exact seven- or nine-vertex rank occurrence is introduced or available here. Their positive-edge patterns require every mapped vertex to have at least four or six neighbors, respectively. In either graph every rim vertex has degree at most three, leaving only the hub as a possible high-degree ID. That is insufficient for seven or nine distinct mapped vertices.

## 4. Reproducible finite check and audit

Run the retained standard-library [exact probe](PNP_DEAN_OVERLAPPING_WHEEL_ROUNDING_2026-09-29.py):

```sh
python3 PNP_DEAN_OVERLAPPING_WHEEL_ROUNDING_2026-09-29.py
```

Python 3.12.14 enumerated all 2^11=2,048 selection subsets separately in each graph. It found 122 independent sets in the NO graph and 144 in the YES graph, with maxima four and five. Exact Fraction arithmetic checked local loads, the two composed bounds, every valid omission set against 16 supplied rational-weight pairs, rejection of the missing-edge wheel receipt, the three-edge replacement proof, both false-rule counterexamples, and the degree obstruction. It printed `PASS exact Step 18 overlap and stale-evidence counterprobes`. Probe SHA-256: `540597867082750d0a29c5122f8da06459f457473f4e6433714cb17cb23e465a`.

| Audit obligation | Status and evidence |
| --- | --- |
| Local support and rounding | Passed: both intact local sums are 19/5 on six named IDs; omissions there are integral. |
| Weighted overlap after rounding | Passed: displayed inequality applies to any supplied valid local integer rows. |
| Same input comparison | Passed: only {5,1} changes; both use n=11, k=5, b=6. |
| YES safety | Passed: explicit five-set; both unsafe rules reject it and the correct bound does not. |
| Exhaustive finite scope | Passed: 2,048 subsets per graph; the finite weight grid supports only that grid. The symbolic proof handles arbitrary nonnegative rational weights. |
| Complete discovery or polynomial universal solver | Out of scope; no such conclusion. |

## 5. World relation and remainder

For a fixed pairwise conflict roster, two groups can share one applicant, task, or transmission. Its stable identity matters: omitting it can satisfy obligations in both groups, while consuming only one unit of the global omission budget. If one supplied conflict edge changes, local evidence depending on that edge must be rechecked. This is a transfer of the counting mechanism within the declared graph model, not empirical evidence for a changing real-world schedule.

**Admitted:** local integer conclusions compose soundly under the existing overlap formula; this exact 11-vertex NO/YES pair; the two explicit failure modes and their repairs. **Remainder:** useful support discovery, sufficient proof size on arbitrary graphs, and a complete uniformly polynomial Dean procedure remain unresolved. The carrier catalog stays fixed, and `P ?= NP` remains open. Further research requires the next approved bounded step.
