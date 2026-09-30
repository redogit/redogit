# Dean's fixed list — compact expressions and the cost of choosing

**Checkpoint:** Steps 26–29, September 30, 2026 UTC. Continues [Steps 19–25](PNP_DEAN_BOUNDARY_STATE_PROGRESSION_2026-09-29.md) from public source commit `67f7f98c46f6d1b85553d70f11b8268e79d0f884`, under the user's instruction to proceed through the steps and resume from checkpoint. The objective remains an exact uniformly polynomial procedure for the unrestricted Dean/Independent-Set decision. This checkpoint does not supply that procedure or settle P versus NP.

The previous checkpoint separated the number of contextual classes from the cost of constructing and optimizing them. This continuation supplies a representation that avoids enumerating boundary assignments, proves its construction and evaluation costs, and then exposes its optimization obligation by an explicit reduction. The private component cap is three. No larger rank carrier is added. Proofs are self-reviewed; finite checks are corroboration, not an independent audit.

## Step 26 — construct a compact exact expression directly from edges

Let G=(V,E) be a finite simple undirected graph, S a supplied boundary, and U=V\S. Admit this route only if every connected component C of G[U] contains at most three vertices. S need not be small or edgeless. Its IDs and its induced edges are retained exactly.

For each component C and each independent I subset of C, store the actual set I, its size, and its boundary neighborhood

\[
N_S(I)=\{s\in S:\text{some }v\in I\text{ has }\{s,v\}\in E\}.
\]

There are at most eight candidate subsets per component. Define, for any independent boundary assignment sigma subset of S,

\[
g_C(\sigma)=
\max_{\substack{I\subseteq C\text{ independent}\\
N_S(I)\cap\sigma=\varnothing}} |I|,
\qquad
f_U(\sigma)=\sum_C g_C(\sigma).
\]

Invalid boundary assignments are rejected. The empty local option is always feasible.

**Exactness proof:** fixing sigma removes from each C precisely those vertices adjacent to sigma. There are no edges between distinct components of G[U]. Therefore every valid extension restricts to one feasible option per component, giving the upper bound; conversely, the union of maximizing local options is independent and realizes that sum. Retaining the actual maximizing I in each factor reconstructs a witness against the original edges. Hence

\[
\alpha(G)=
\max_{\sigma\subseteq S\text{ independent}}
\left(|\sigma|+\sum_C g_C(\sigma)\right).
\]

This last maximum is an obligation, not a free operation.

**Costs, separately charged:** connected components and the cap check take O(n+m) with adjacency lists. At most eight subsets per component require constant-size internal checks. Each cross edge occurs in at most eight stored neighborhood unions. Indexed arrays and per-option marking therefore allow O(8(n+m)) elementary work and O(8(n+m)) retained IDs/edges/options; bit storage includes the O(log(n+1)) cost of IDs and scores. One supplied assignment can be checked and evaluated in the same polynomial bound, and its actual extension recovered in O(n) output work after the choices are made. A simple implementation that sorts or repeatedly scans IDs remains polynomial, though it need not attain this tighter indexed bound.

No table of all 2^|S| boundary assignments is constructed for these operations. The representation succeeds where Step 24 first materialized all states. If a private component exceeds the cap, the route returns UNKNOWN/outside scope; this is not a Dean NO.

The finite probe stores the full canonical source graph and boundary with the expression. Evaluation against a different graph is rejected as stale. This exact source comparison also costs polynomial work; it is not hidden behind a hash-only authority claim.

## Step 27 — small factors can still contain the original optimization problem

For an arbitrary simple graph H=(S,F), let m=|F|. Construct G by removing the original edges and replacing each edge e={u,v} with the three-edge path

\[
u-a_e-b_e-v,
\]

where every a_e and b_e is a fresh private ID. The original vertices S are now edgeless; G has |S|+2m vertices and 3m edges. G[U] consists of disjoint two-vertex components, so it passes even the stronger private cap of two.

For one component {a_e,b_e}, its maximum contribution is one unless both endpoints u and v belong to sigma; in that case both private vertices are excluded and the contribution is zero. Thus

\[
|\sigma|+f_U(\sigma)
=m+|\sigma|-|F[\sigma]|.
\]

For every sigma, delete one endpoint of each still-present edge in H[sigma], processing the original induced edges in any fixed order. At most |F[sigma]| deletions leave an independent set. Consequently

\[
|\sigma|-|F[\sigma]|\le \alpha(H).
\]

Taking sigma to be a maximum independent set of H attains equality. Therefore

\[
\boxed{\alpha(G)=m+\alpha(H).}
\]

This is a polynomial construction and a two-way exact decision reduction: H has an independent set of size at least k iff G has one of size at least m+k. The source witness can also be recovered: any G witness restricts to sigma and has size at most m+|sigma|-|F[sigma]|; the deletion procedure then obtains at least k source vertices whenever the G witness has at least m+k.

The construction is the familiar operation of subdividing every edge twice; no novelty or priority claim is made for it. Its explicit proof here needs no unverified external reduction theorem. It shows that unrestricted optimization of Step 26's compact expressions already includes the original Independent-Set obligation, even with an edgeless boundary, pair-sized private components, three local independent options per component, and degree-two private vertices. It does not prove an unconditional superpolynomial lower bound or P != NP.

In binary coordinates x_v indicating boundary selection, the objective is

\[
m+\sum_{v\in S}x_v-\sum_{\{u,v\}\in F}x_ux_v.
\]

Every evaluation is easy; the pair interactions retain the original conflict graph. Small factor arity and compact description alone do not make choosing all x_v easy. The scalar |F[sigma]| is fully determined by the retained source IDs and edges; it is not an estimated penalty.

## Step 28 — a complete tractable branch with matching and witnesses

Now require both G[S] and G[U] to be edgeless. This is exactly a supplied bipartition; every private component is a singleton. Then

\[
f_U(\sigma)=|U|-|N(\sigma)|,
\]

and the global optimum can be obtained in polynomial time without enumerating sigma.

Build a bipartite matching M by processing the left vertices one at a time. From each newly processed vertex, search for an alternating path to an unmatched right vertex and augment if one exists. One search visits each edge at most a constant number of times with standard visited marks. After each left-vertex prefix the matching is maximum: adding one left vertex can increase the optimum by at most one; if it does, the symmetric difference with a larger matching contains an augmenting path beginning at that new vertex. A path wholly in the older prefix would contradict its already maximal cardinality. Failure to find a path therefore preserves a maximum matching for the enlarged prefix. Total work is O(n(n+m)), with O(n+m) storage.

Starting from all unmatched vertices in S, follow unmatched edges from S to U and matched edges from U to S. Write the reached sets as Z_S,Z_U. No unmatched right vertex is reached, since that would give an augmenting path. Set

\[
C=(S\setminus Z_S)\cup Z_U.
\]

**Certificate proof:** every edge is covered. An uncovered edge would run from reached left u to unreached right v. If it is unmatched, the traversal reaches v; if matched, a reached matched left vertex was entered through its matched right partner, so v was already reached. Both cases contradict the alleged uncovered edge.

Each matched pair has either both endpoints reached or both unreached, so C contains exactly one endpoint of each matched edge. C contains no unmatched left vertex (all are starting points) and no unmatched right vertex (none is reached). Hence |C|=|M|. Any vertex cover must meet every disjoint matched edge and therefore has size at least |M|. C is minimum, and its complement is a maximum independent set:

\[
\alpha(G)=|V|-|M|.
\]

A supplied matching and equal-sized cover can be checked directly against the original E, yielding both a witnessed YES at k<=|V|-|M| and a certified NO at k>|V|-|M|. The original graph remains the authority for both certificates. Failure of the bipartition admission is UNKNOWN for this branch.

This matching/cover relation is classical, not a new unrestricted Dean algorithm. The primary bibliographic check is Hopcroft and Karp, *An n^(5/2) Algorithm for Maximum Matchings in Bipartite Graphs*, SIAM Journal on Computing 2(4), 225–231, December 1973, [DOI 10.1137/0202019](https://epubs.siam.org/doi/10.1137/0202019). The publisher's abstract and metadata were read on September 30, 2026; the full PDF fetch was unavailable. The abstract gives their faster O((m+n)sqrt(n)) matching bound. The retained probe implements the simpler O(n(n+m)) augmenting search proved above and claims no Hopcroft–Karp implementation or bound.

The comparison is exact: singleton private components with an edgeless boundary give the tractable bipartite branch. Allowing disjoint private edges already admits Step 27's arbitrary source reduction. Merely changing the private cap from two to one is useful only together with the edgeless-boundary condition; arbitrary edges inside S would still contain the original problem.

## Step 29 — one edge repairs one factor, not every consequence for free

Use H=K3 on original IDs {0,1,2}. Step 27 produces nine IDs, nine edges, and three private pairs:

| Source pair | Private IDs | Replacing path |
| --- | --- | --- |
| {0,1} | {3,4} | 0-3-4-1 |
| {0,2} | {5,6} | 0-5-6-2 |
| {1,2} | {7,8} | 1-7-8-2 |

The whole graph is C9 in order (0,3,4,1,7,8,2,6,5). Thus alpha=4, tau=5. At the fixed target k=5 and omission budget b=9-5=4, it is NO. This is also an older odd-cycle certificate control, not a new rank carrier.

Delete only the boundary-to-private edge {0,3}; retain all nine IDs, all three private pairs, k=5, and b=4. In the first factor the option {3} now has empty boundary neighborhood, so that factor always contributes one. Its former value was 1-x_0*x_1. The other two factors have exactly the same serialized contents as before.

The altered graph is P9, with alpha=5 and tau=4. The boundary state sigma={0,1} extends to the explicit valid five-set {0,1,3,6,8}. It is YES at the same target. Equivalently, the expression now gives

\[
3+\max_{\sigma\subseteq\{0,1,2\}}
\bigl(|\sigma|-|E_{K3-\{0,1\}}[\sigma]|\bigr)=3+2=5.
\]

The implemented counterprobe rebuilds the three factors from the changed E and verifies that exactly one factor differs; it is not presented as an implemented incremental update engine. For this particular cross-edge deletion the component partition is unchanged, so a future incremental implementation can recompute just that component's at most eight local options, while updating the source identity and rechecking the resulting global witness. Its work depends on that component's boundary incidences and the chosen provenance representation. It is not constant time in arbitrary boundary degree.

A graph change invalidates the old expression's context identity. Reusing the old optimum would falsely reject this YES; the probe explicitly rejects an old expression evaluated against the changed graph. Even a local formula edit can require a global reoptimization. No general dynamic optimum-maintenance bound follows. An arbitrary internal edge edit can split or merge private components and requires fresh admission, so the one-factor repair is confined to the declared cross-edge deletion.

## Evidence and reproducibility

- [Retained JavaScript probe](PNP_DEAN_COMPONENT_EXPRESSION_PROBE_2026-09-30.mjs).
- [Exact finite result](PNP_DEAN_COMPONENT_EXPRESSION_RESULT_2026-09-30.json).
- [Execution and provenance record](PNP_DEAN_COMPONENT_EXPRESSION_EXECUTION_2026-09-30.json).

Reproduction command, with Node available:

```sh
node PNP_DEAN_COMPONENT_EXPRESSION_PROBE_2026-09-30.mjs > /tmp/dean-component-result.json
```

All 16,645 assertions passed with exact small integers and no random sampling.

| Check | Exact finite coverage |
| --- | --- |
| Build and evaluate the expression | All 76 labeled simple graphs with 0–4 vertices; all 1,099 boundary partitions. 1,061 admitted, 38 over-cap cases rejected; 4,073 feasible boundary states compared to a separate brute-force extension oracle. Invalid states rejected. |
| Full three-vertex private components | Additional nine-vertex fixture with two three-vertex components; all six feasible states checked. |
| Arbitrary-source reduction | All 76 source graphs with 0–4 vertices. Up to 16 transformed vertices; 251,023 transformed subsets checked by the independent brute-force oracle; 1,099 boundary scores and recovered source witnesses checked. |
| Bipartite solver | 533 graphs: all 3-by-3 bipartite graphs plus empty-side, 1-by-1, and 2-by-2 controls. 33,049 subsets checked; matching, cover, and complement witness validated. |
| Admission | Oversized private component and a nonbipartite partition return UNKNOWN; invalid boundary assignments reject. |
| One-edge repair | C9 -> P9 on the same IDs and target. Exact maxima 4 -> 5; one changed factor, two identical factors, explicit five-set, stale-context rejection. |

Probe Git blob: `61cd2e133e42799ab05f21c8ca661c419ae55153`. Result Git blob: `1879920a0d6d206d4aceeb17309ccc798afd81c9`.

**Execution boundary:** the local exec-server connection was unavailable. The exact retained probe function was executed directly in the available JavaScript/V8 tool runtime, finishing in 618 milliseconds on this one finite run. Its host version was not exposed. The published module retains that function's actual source plus a Node output wrapper. The wrapper was not run in Node here. No new Python run, process-level resource limit, Mathbox version-2 manifest validation, or local Git checkout is claimed. The custom execution record identifies this limitation and pins the source/result Git blobs. These modest finite timings do not establish an asymptotic theorem.

The brute-force oracle is deliberately capped at 18 vertices and uses small bit masks; the largest actual exhaustive case has 16. The mathematical constructions and cost proofs are separate from that finite implementation. The original Steps 19–25 Python/manifest evidence remains historical and unchanged.

## Connection to the user's research and practical systems

This continues the identity-preserving composition in Steps 20–24 and the reconstruction-cost obligation made explicit in Step 25. It also matches the profile's Libraries of Libraries requirement to count construction, verification, storage, and recovery separately. Keeping an exact small expression is a successful representation repair; claiming its global maximum is therefore cheap would omit a different obligation.

For a conflict roster, a private component describes a small group of tasks whose choices interact locally, while S contains choices shared across groups. The factor says exactly which private tasks remain possible for a supplied shared plan. An incremental build or planning system can retain that dependency information and invalidate the affected factor when an exclusion changes. The one-edge example shows why it must also invalidate conclusions that depended on the factor. These are graph-model correspondences, not a measured deployment or a claim that every scheduling constraint is pairwise.

Step 27's binary objective also provides an exact mathematical bridge to pairwise energy formulations: minimizing its negative is the same optimization after a constant/sign change. Representing it as an energy, a compact circuit, or a learned evaluator supplies no exact global-optimization guarantee by itself. A heuristic may propose a witness; the original graph checks that witness. A negative answer still needs its own valid bound or exact optimization evidence.

## Current state and next discriminating obligation

Step 26 closes the representation/build/evaluation/witness questions for the declared small-private-component class without enumerating S. Step 27 refutes the inference that those properties alone settle global optimization. Step 28 supplies a complete polynomial special case with two-sided certificates. Step 29 bounds the repair to one changed input edge and one affected factor while exposing the remaining global consequence.

The general compact-expression optimization route remains open as a research target, but “every factor is small” has been exhausted as a sufficient tractability argument. A next proposal must identify a checkable restriction on the interactions among boundary variables, then prove both its admission cost and its optimization/witness cost. Reusing Step 22's already proved bounded-decomposition recurrence is available when its gate holds; it would be a composition of existing results, not an unrestricted advance. No such small-interaction guarantee is established for arbitrary H, and the original fixed-list polynomial obligation remains unresolved. `P ?= NP` remains open.
