# Dean's fixed list — from overlap totals to exact boundary states

**Checkpoint:** Steps 19–25, continued under the user's instruction “Yes, but just go hard through the steps.” Base: `redogit/redogit@cd6d3329109cf114a3466332487dc69a7aff2104`, following [Step 18](PNP_DEAN_OVERLAPPING_WHEEL_ROUNDING_2026-09-29.md). This supersedes the earlier pause after every single step for this continuation. The objective remains a complete, exact, uniformly polynomial Dean procedure; the results here are partial and do not settle P versus NP.

**Bound:** fixed graphs and exact input IDs; no added seven-/nine-vertex rank carrier. One composition repair retains binary assignments on a supplied overlap of at most three vertices, with regions of at most six vertices. Its tree extension is admitted only after explicit structural checks. The proofs below are self-reviewed; the exact computations provide finite corroboration, not an independent external audit.

## Step 19 — the overlap penalty is sound but can discard decisive information

Let W(r;h) denote the six-vertex wheel whose five rim vertices, in order r, form a cycle and whose hub h is adjacent to every rim vertex. Use

\[
G=W((0,1,2,3,4);5)\ \cup\ W((0,1,2,6,7);8).
\]

The supports A={0,1,2,3,4,5} and B={0,1,2,6,7,8} share S={0,1,2}, which induces path 0-1-2. There are n=9 vertices and m=18 edges; no edge joins A\S to B\S. Fix k=4 and b=n-k=5.

Each verified wheel requires four omissions. The existing penalty gives 4+4-3=5, tying b and leaving this selected certificate inconclusive. This is the **best bound from just these two rounded rows**: the omission vector with ones at {0,1,2,3,6} and zeros elsewhere satisfies both local totals at four and has total five. It violates actual graph edges, but is feasible in that two-row relaxation; therefore no weighting of those two rows with the box bounds can prove a larger lower bound.

In the actual graph, omitting all of S leaves a triangle on {3,4,5} and another on {6,7,8}, each permitting only one selection. Selecting exactly one shared vertex permits at most one extra selection per side, for total three. Selecting {0,2} excludes every nonshared vertex, for total two. No other shared selection is independent. Thus alpha(G)=3, attained by {0,3,6}, and tau(G)=6. The input is NO at k=4 even though the two rounded totals stall at five. What was lost was the conditional meaning of the local totals when the *same* shared assignment is fixed.

### Control: older uncompressed rows already prove this NO

This is not a failure of the complete previous clique/cycle machinery. The following **existing** rows have exact nonnegative rational weights and load every vertex exactly once:

| Existing row, using listed cyclic order for C5 | Omission requirement | Weight |
| --- | ---: | ---: |
| C5 (0,1,2,3,4) | 3 | 1/5 |
| C5 (0,1,2,6,7) | 3 | 2/5 |
| Triangle {0,1,5} | 2 | 1/5 |
| Triangle {0,7,8} | 2 | 1/5 |
| Triangle {1,2,8} | 2 | 1/5 |
| Triangle {2,6,8} | 2 | 1/5 |
| Triangle {3,4,5} | 2 | 4/5 |
| Triangle {6,7,8} | 2 | 2/5 |

Their penalty is zero and B=29/5>5, already proving NO. This is the smallest repair needed for the decision on this fixture: retain and reweight the source rows instead of retaining only the two rounded totals.

The full frozen LP optimum is exactly 29/5. A matching feasible omission point sets y=4/5 at hubs 5 and 8, and y=3/5 at the seven rim IDs. Equivalently, x=1/5 at hubs and x=2/5 elsewhere. Every triangle contains one hub and two rim vertices, so its selection sum is one; there is no larger clique. For any odd cycle of length ell>=5, its selection sum is at most 2ell/5 <= (ell-1)/2. The seven-/nine-vertex positive-edge carriers cannot occur: only the three shared vertices and two hubs have degree at least four, fewer than seven distinct IDs. The feasible point and displayed dual therefore agree exactly. A numerical LP was used only to find the displayed weights; all admitted arithmetic is checked with exact fractions.

## Step 20 — keep the shared assignment, then combine exact local tables

For any supplied two-region graph with A union B=V and no edge between A\S and B\S, S=A intersection B, define

\[
f_A(\sigma)=\max\{|I|:I\subseteq A\setminus S,\ I\cup\sigma\text{ is independent in }G[A]\},
\]

and define f_B similarly, for each independent sigma subset of S. Invalid boundary states are rejected, not assigned zero. Then

\[
\alpha(G)=\max_{\sigma\subseteq S\text{ independent}}
\bigl(|\sigma|+f_A(\sigma)+f_B(\sigma)\bigr).
\]

**Proof:** every global independent set restricts to the same sigma on both sides, so its size is at most the displayed expression. Conversely, maximizing local witnesses with that same sigma can be united: each side checks its own edges, and the required absence of cross-interior edges rules out an unchecked conflict. The shared selection is counted once. Both inequalities give equality. This is an exact composition theorem for a supplied valid separation, not a bound on finding one.

For Step 19 and its opposite, delete only edge {3,4} to obtain G-minus, keeping n=9, k=4, b=5. The following table lists all five feasible boundary states; the other three of the eight binary states contain edge {0,1} or {1,2} and are rejected.

| Shared selected IDs sigma | Intact f_A | f_B | Intact total | Altered f_A | Altered total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Empty | 1 | 1 | 2 | 2 | 3 |
| {0} | 1 | 1 | 3 | 1 | 3 |
| {1} | 1 | 1 | 3 | 2 | 4 |
| {2} | 1 | 1 | 3 | 1 | 3 |
| {0,2} | 0 | 0 | 2 | 0 | 2 |

The intact graph has alpha=3, tau=6: NO. The changed graph has alpha=4, tau=5: YES, witnessed by {1,3,4,6}. The first local table is recomputed from the changed edges. In particular, the old triangle {3,4,5} is no longer an admissible clique row. The exact table is useful for reusable composition; it is not claimed necessary to prove the intact NO, which the preceding 29/5 receipt already resolves.

With the declared caps |A|,|B|<=6 and |S|<=3, at most 64 subsets per region build all at most eight boundary entries. Both endpoints of every input edge must be covered by one region. If these checks fail, this composition is unadmitted; it supplies no NO or YES verdict for the input.

## Step 21 — a count-only summary invents a false YES

Use the same nine IDs and two supports, but take

\[
H=\bigl(W((0,1,2,3,4);5)-\{\{3,4\}\}\bigr)
\cup\bigl(W((0,2,1,6,7);8)-\{\{6,7\}\}\bigr).
\]

There are 17 edges. The full supplied edge set makes S={0,1,2} a triangle; both local tables include every edge induced by their support, including shared edges contributed by the other region. Only the empty state and three singleton states are feasible.

| Shared selected IDs | f_A | f_B | Exact total |
| --- | ---: | ---: | ---: |
| Empty | 2 | 2 | 4 |
| {0} | 1 | 1 | 3 |
| {1} | 2 | 1 | 4 |
| {2} | 1 | 2 | 4 |

Hence alpha(H)=4, attained by {3,4,6,7}. At k=5, b=4 the answer is NO. However, if each side retains only its maximum at each *count* q=|sigma|, both report two extra selections at q=1. Adding 1+2+2 yields five, a false YES: A's two requires sigma={1}, while B's two requires sigma={2}. Those are different applicants.

For a fixed feasible count q and fixed finite tables, equality between “maximum of the sum” and “sum of the maxima” holds exactly when the sides have a common maximizing boundary assignment at q. To prove necessity, any state reaching the sum of individual maxima must reach each maximum; sufficiency follows by using that common state. Thus count compression needs a checked compatibility condition. Equal counts alone do not supply it. This counterexample rejects that particular quotient, not every possible compression.

## Step 22 — exact composition on a verified tree of small regions

The same mechanism extends to a supplied tree T of bags B_i, with these admission conditions:

1. The bags cover all input vertex IDs, and every input edge has both endpoints in at least one bag.
2. The nodes containing any one vertex form a connected subtree of T (the running-intersection condition).
3. Each bag contains at most six vertices; each tree-edge intersection contains at most three.

Root T. Let S_i be the intersection with the parent bag, with S_root empty. Let V_i be all IDs in the subtree rooted at i. The message F_i(sigma) is the maximum number of selected vertices in V_i\S_i conditional on choosing exactly sigma on S_i. Infeasible states have no entry. The recurrence is

\[
F_i(\sigma)=\max_{\substack{X\subseteq B_i\text{ independent}\\X\cap S_i=\sigma}}
\left(|X\setminus S_i|+\sum_{j\text{ child of }i}F_j(X\cap S_j)\right).
\]

**Proof by subtree induction:** a vertex appearing inside a child subtree and outside it must occur in the connecting separator, by running intersection. Edge coverage then prevents an edge between two child interiors or between a child interior and a parent-only vertex: a bag covering that edge would force the supposed interior endpoint through the separator. Consequently, the child interiors are disjoint, interact with the parent only through their stated separators, and may be optimized independently once X is fixed. The displayed counts charge every selected ID exactly once. Restriction gives the upper bound, and union of consistent local witnesses gives its attainment. Leaves are the same formula with an empty sum. Thus F_root(empty)=alpha(G). Retaining a maximizing local assignment per table entry permits a final witness traceback, which is checked against the original E.

There are at most 64 local assignments per bag and eight separator states per message. For t supplied bags, the arithmetic loop uses O(64t) score additions/comparisons after indexed edge lookup and structural validation: each child contributes one table lookup for each candidate assignment of its parent. Scores have O(log(n+1)) bits. Vertex/edge coverage, tree structure, and running intersection are explicitly validated; ordinary indexed graph operations add polynomial preprocessing, with expected O(n+m+t) dictionary work under the fixed caps. Stored scores and local traceback choices occupy O(8t) entries, each with an O(log(n+1))-bit score and at most six IDs, plus the output witness. The code does not copy a growing witness into every intermediate table.

The gate is load-bearing. Three edge bags {0,1}, {1,2}, {0,2} arranged as a path cover the triangle's edges but violate running intersection for ID 0. The verifier rejects them. Adding cross-interior edge {3,6} to the Step 19 pair also rejects its two-bag decomposition because no bag covers that edge. Neither rejection is a graph NO verdict. Empty and singleton graph cases are admitted and checked.

An explicit family supplies a larger control: t wheels share the same rim path 0-1-2, with each wheel having three private vertices. A star of their six-vertex supports passes the gate. No shared selection permits t private selections; any singleton permits t+1 overall; selecting {0,2} permits only two. Thus alpha=t+1 for t>=1, on n=3+3t vertices. At t=100, the exact run obtained alpha=101 on 303 vertices, using 6,400 local candidates and at most five feasible message states. This constructed family is not the user's arbitrary 400-applicant instance.

**Literature relation:** these are tree-decomposition conditions and dynamic programming, not a new general algorithm. The checked primary source is van Rooij, Bodlaender, van Leeuwen, Rossmanith and Vatshelle, *Fast Dynamic Programming on Graph Decompositions*, arXiv:1806.01667v1, 5 June 2018, [versioned PDF](https://arxiv.org/pdf/1806.01667v1), Definition 2.3 (PDF page 7), and the introduction's distinction between finding a decomposition and solving on one. Translation: their X_x is our B_i; their width is max |B_i|-1, at most five here. Our additional intersection cap is three. The recurrence and its fixed-cap cost are proved above rather than imported from a different problem's theorem. Classification: known framework after notation translation; no novelty claim. Source checked September 29, 2026; the exact PDF version was read through web retrieval, with no local source cache claimed. No SETH or other complexity hypothesis is used.

## Step 23 — why arbitrary future contexts prevent universal state merging

Take an edgeless boundary S of size s, so all 2^s subsets are valid selected states. For two different states sigma and rho, choose v in their symmetric difference. Attach just one external vertex z with the single edge {v,z}. The best number of *additional* selected vertices is zero if v is selected, and one if v is not selected. Therefore this external context distinguishes sigma from rho.

It follows that an equivalence relation preserving exact extension behavior under **every possible such future context** has 2^s distinct classes on this boundary. This is a proved obstruction to merging those states as universally interchangeable. It is not an exponential-time lower bound for all algorithms: all states have short bit-string descriptions, and an algorithm might manipulate a succinct function, exploit the fixed actual context, use a different decomposition, or use other mathematics without materializing a table of all states. Even the empty-edge graph itself is easy. No P-versus-NP conclusion follows.

This identifies the useful obligation: any proposed compression must state which future contexts are allowed and prove that its merged states remain interchangeable for those contexts. Object identity alone does not bound the number of consequentially different assignments; preserving identity and finding a small exact representation are separate requirements.

## Step 24 — a safe quotient for the actual fixed context

Return to the supplied two-region graph and its complete, verified boundary tables. Restrict to boundary states feasible on both sides. For this specific fixed future B, place states in the same class when f_B(sigma) has the same value c. In each class retain

\[
M_c=\max_{\sigma:f_B(\sigma)=c}\bigl(|\sigma|+f_A(\sigma)\bigr)
\]

and a maximizing *actual* assignment sigma_c, together with local witness provenance. The exact answer is max_c(M_c+c). This follows by partitioning the maximum in Step 20 into disjoint classes; f_B is constant within each class. The retained sigma_c selects mutually compatible local witnesses. The rule does not independently combine incompatible A and B maxima as the count-only quotient did.

All three nine-vertex fixtures compress to two classes. In the intact and one-edge pair, the B-score-one class contains the empty state and all three singletons; the B-score-zero class contains {0,2}. The intact best class gives three selections. After the edge deletion, its retained maximizing state changes to {1}, yielding the witnessed four-set {1,3,4,6}. In the Step 21 counterexample, B-score-one groups {0},{1}, while B-score-two groups the empty state and {2}; both class totals are four. Witness reconstruction against the full input edges passed in every case.

This is a proved fixed-context quotient of already computed tables. It does not preserve behavior if the future B changes, and the context's edge/provenance identity must accompany it. In particular, this check constructed the full tables before compressing them; it does not show that the quotient can be discovered more cheaply, or that maximizing within its classes is polynomial for arbitrary large regions.

## Step 25 — one class can still contain the original computational obligation

Consider a proposed unrestricted extension of the table method. Let S be empty, A empty, and B be an arbitrary input graph H. There is exactly one boundary state, but

\[
f_B(\varnothing)=\alpha(H).
\]

Thus a uniformly polynomial routine computing this single table value on arbitrary H would already solve the original Dean decision by comparing it with k. Conversely, an exact independent-set optimizer computes that value. The statement is an identity reduction, not an assumption about P versus NP and not an implementation outside the six-vertex cap. The finite zero-boundary control uses a five-cycle, has one entry, and correctly returns two.

Together, Steps 23–25 distinguish three costs: how many states remain consequentially distinct under the declared context, how their classes are represented and discovered, and how their optimum values and witnesses are computed. A polynomial class count by itself does not establish polynomial total work. Fixed-cap local enumeration supplies all three costs for Step 22's admitted class; no such bound has been established here for unrestricted H.

## Evidence, audit, and relation to the world

Retained artifacts: [probe](PNP_DEAN_BOUNDARY_STATE_PROBE_2026-09-29.py), [contract](PNP_DEAN_BOUNDARY_STATE_CONTRACT_2026-09-29.json), [exact result](PNP_DEAN_BOUNDARY_STATE_RUN_2026-09-29_r2/result.json), [manifest](PNP_DEAN_BOUNDARY_STATE_RUN_2026-09-29_r2/manifest.json), and [run output](PNP_DEAN_BOUNDARY_STATE_RUN_2026-09-29_r2/stdout.txt).

To reproduce the mathematical checks from the repository root:

```sh
python3 PNP_DEAN_BOUNDARY_STATE_PROBE_2026-09-29.py /tmp/dean-boundary-result.json
```

The recorded CPython 3.12.14 run used exact integer/Fraction arithmetic, no random sampling, a 30-second wall limit, 20-second per-process CPU limit, 1 GiB address-space limit, one core and one cooperative thread cap. It completed in about 0.116 seconds. The installed Mathbox version-2 manifest validator passed with input/result hashes checked. The scratch execution had no local Git commit; the manifest records that limitation, declares the remote base explicitly, and pins the actual executed script before and after the run. The later GitHub commit retains those same bytes. The initial numerical LP exploration is not part of the proof-supporting run; its extracted rational certificate is.

| Obligation | Evidence and scope |
| --- | --- |
| Scalar-overlap failure and old-row control | Two-row feasible point at five; exact 29/5 primal/dual proof; source rows checked against E. |
| Exact pair and identity counterexample | All 512 subsets of each of three nine-vertex graphs; maxima 3,4,4; respectively 34,41,45 independent sets. |
| Conditional composition | Complete boundary tables plus the restriction/union proof. |
| Branching and root choice | A 13-vertex three-bag fork: all 8,192 subsets give alpha=4, matched from all three roots. Both roots checked on every two-region fixture. |
| Admission failures | Uncovered cross edge, disconnected occurrence of an ID, bag over six, separator over three all rejected. Empty and singleton cases passed. |
| Larger bounded structure | The proved t-wheel family; t=100 check gives n=303, alpha=101, 6,400 candidates. |
| Context separation | Direct symbolic distinguisher for every s; finite edge-membership checks on all 5,334 ordered distinct state pairs at s=0,...,6. |
| Fixed-context quotient | Two classes on each of three fixtures; exact scores and reconstructed witnesses checked against the full graph. |
| One-entry cost boundary | Identity reduction proved for arbitrary H; finite empty-boundary C5 control returns alpha=2. |
| Universal polynomial procedure | Unresolved; not inferred from fixed-cap cases, timings, or source attribution. |

Probe SHA-256: `c4c51a43248dc01b205e06ae43c8f0169ca920b0196bad92adba850c3558a59e`. Result SHA-256: `904137cb1108c52faeb4e4934c8c7014ab5e92c3611d17b861ff1de5191a9f3e`.

For a fixed conflict roster, two departments can each say “one shared worker selected” while referring to different workers. Combining their best counts can promise an impossible global roster. The interface must retain the assignments that make the local plans jointly executable. This is the exact graph-model mechanism; no claim about a live scheduling deployment, changing conflicts, or higher-order resource constraints is made.

## Current research state and executable remainder

The overlap-only scalar route is refuted as a complete exact summary by Step 19, while its soundness from Step 18 survives. Reweighting its retained source rows resolves that fixed NO. Count-only boundary joining is refuted by Step 21. Identity-conditioned composition is proved on the supplied two-region separation and verified bounded tree class. Universal merging across arbitrary future contexts is refuted for the stated extension-behavior equivalence by Step 23.

The fixed-context route was then executed: Step 24's quotient preserves optimum values and reconstructible witnesses in the declared context. Step 25 exposes its remaining cost obligation. The main goal remains open: there is no established uniformly polynomial way here to find a sufficient decomposition, construct the necessary contextual classes, and compute their values for arbitrary Dean graphs. The next route stays **open**, not exhausted: seek a succinct fixed-context representation whose construction, class-restricted maximization, and witness recovery all have separately proved cost bounds. The current quotient is available as a truth oracle within the three-ID cap; its full-table construction must be charged rather than hidden. Resuming this route requires a specific representation and operation bound, not another repetition of the existing finite cases. This checkpoint closes the overlap-composition phase while preserving its failed summaries, counterexamples, working repair, and unresolved universal obligation. `P ?= NP` remains open.
