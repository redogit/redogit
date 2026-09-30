# Dean's fixed list — discovered articulation composition

**Checkpoint:** Steps 35–39, September 30, 2026 UTC / September 29 evening New York. Base: `redogit/redogit@3a6607a005d3376b2949b1e4ab3a43f37bf52a32`. Read the [current problem map](PNP_CURRENT_PROBLEM_MAP_2026-09-30.md) for the deeper GitHub/Work reconciliation and the still-open universal SAT obligations.

**Result:** an exact deterministic polynomial procedure for graphs whose articulation atoms become bipartite after deleting at most one vertex per atom. It discovers the articulation structure, recognizes the local class, solves the conditional problems and returns original-ID witnesses and checkable certificates. The original graph is unchanged. This is a separate declared composition route; the earlier whole-graph cap-one procedure is unchanged. No global repair-set enumeration is used.

**Original goal:** a uniform polynomial algorithm for arbitrary Dean/Independent-Set inputs, contributing to the pursued P = NP goal. That goal remains open. A local cap-one terminal and its closure under articulation composition do not prove universal coverage. No novelty claim is made for articulation decomposition or dynamic programming.

## Step 35 — the actual shared-vertex interface

Let G be the union of induced pieces G_A and G_B whose vertex intersection is exactly {v}, with no edge between their private vertices. Define M_A(s), for s in {0,1}, as the largest number of selected PRIVATE vertices in piece A conditional on v having state s. Thus

\[
M_A(0)=\alpha(G_A-v),\qquad
M_A(1)=\alpha(G_A-N_{G_A}[v]),
\]

and similarly for B. Then

\[
\alpha(G)=\max\{M_A(0)+M_B(0),\ 1+M_A(1)+M_B(1)\}.
\]

Restriction proves the upper bounds. In either branch the private witnesses unite without a cross-edge conflict; add v only in the selected branch. This proves attainment and counts v exactly once. Neither one unconditional score per piece nor two independently chosen boundary states is a valid replacement.

For two edges {v,a} and {v,b}, both tables are (1,0). The union has optimum two, witnessed by {a,b}; subtracting one from the sum of the two unconditional optima would incorrectly give one.

## Step 36 — induced weights do not require a general weighted solver here

For any child piece or subtree attached through a single v, its private feasible sets when v is selected are a subset of those allowed when v is omitted. Therefore

\[
M(1)\le M(0).
\]

All scores are integers. Incorporating child j contributes baseline M_j(0) and correction M_j(1)-M_j(0) if v is selected. At a vertex counted in the current bag, its effective weight is

\[
w(v)=1+\sum_{j\text{ attached at }v}(M_j(1)-M_j(0))\le1.
\]

Consequently every positive weight is EXACTLY ONE. For an unforced vertex of nonpositive weight, omitting it cannot decrease the weighted objective and cannot violate independence. Remove those vertices from the local optimization. What remains is an unweighted induced-subgraph independent-set problem.

This corrects the earlier concern precisely: negative weights really occur, but for this cardinality/singleton-interface model a general weighted matching or flow algorithm is unnecessary. At the center of a two-leaf star, w(v)=1-1-1=-1. The computation retains that negative value and chooses the two leaves. A forced boundary vertex is handled separately; it is never silently discarded because of its weight.

The argument depends on integer unit rewards, downward-closed independent sets, and one shared vertex per interface. It is not a theorem for arbitrary rewards, quotas or higher-order interface interactions.

## Step 37 — exact messages on a verified tree of pieces

Supply a tree of bags B_i covering every vertex and edge of G. Require that the bags containing each original vertex form a connected subtree (running intersection), and that adjacent bags intersect in at most one vertex. Empty intersections allow disconnected components. Bags themselves may be large.

Root the tree. Let p_i be the parent separator vertex when present. Let U_i be the union of bags in the subtree at i. Define M_i(s) to count a maximum independent set in U_i excluding p_i from the count, conditional on its state s. If the parent separator is empty, use a single free state and count all vertices of U_i.

The local vertices owned at i are B_i minus {p_i}. For a child c, write a_c for its separator, if present. Set

\[
C_i=\sum_{c:a_c\text{ present}}M_c(0)
 +\sum_{c:a_c\text{ absent}}M_c(\mathrm{free}),
\]

\[
w_i(v)=\mathbf1[v\ne p_i]
 +\sum_{c:a_c=v}(M_c(1)-M_c(0)).
\]

The parent separator's initial weight is zero because its own selection is counted above this bag. Its descendants may still contribute a negative correction. For any independent local choice J consistent with the parent state, the best subtree score is

\[
C_i+\sum_{v\in J}w_i(v).
\]

**Why composition is valid:** running intersection implies that private interiors of distinct child subtrees are disjoint. Any edge joining such interiors would require a covering bag and force its endpoints through the separators, contradicting privacy. The same condition ensures that every repeated original ID receives the same state. Thus, conditional on J, child witnesses can be united and all owned vertices are counted once.

For parent state zero, forbid p_i. For state one, select p_i explicitly, add w_i(p_i), and forbid its neighbors in B_i. Among all other allowed local vertices retain only those with positive weight. Let the resulting induced graph be H_i,s. The recurrence is exactly

\[
M_i(s)=C_i+s\,w_i(p_i)+\alpha(H_{i,s}).
\]

For a free state omit the parent term. This equation follows from Step 36's safe deletion of unforced nonpositive weights. It preserves the best VALUE; the retained traceback supplies an actual cohort, not a claim that all possible maximum cohorts are retained.

If G[B_i]-X_i is bipartite with |X_i|<=1, then H_i,s-(X_i intersection V(H_i,s)) is also bipartite. The Step 31 include/exclude formula and Step 28 matching/cover certificates therefore solve every local query. No bag-subset enumeration is needed. At most two message states and at most two bipartite branches per state occur at each bag.

Induct from leaves to root. The recurrence gives the exact conditional values; unions of the chosen local and child witnesses attain them. The root's free value is alpha(G). For target k, a witness of size at least k supplies a valid k-subset; a certified optimum below k supplies NO. Malformed decomposition and admission failure are distinct from that NO.

## Step 38 — discover the interface and charge the work

The implementation does not assume that a helpful tree is supplied.

1. Separate connected components; join their decomposition trees through an empty root bag if needed.
2. For a connected current induced graph H, test vertices in stable-ID order. For each v, compute components of H-v by graph traversal.
3. If H-v has at least two components C_j, create a singleton bag {v} and recursively decompose each induced H[C_j union {v}]. Attach each child tree at a bag containing v.
4. If no such v exists, retain H as an atom. An isolated vertex and the empty graph are base cases.
5. Verify vertex/edge coverage, tree structure, singleton separators and running intersection. Run the complete Step 32 cap-one recognition on each atom. If any atom fails, this route returns UNKNOWN, retaining its local odd-cycle rejection record.

**Correctness of discovery:** every edge of a split graph lies in one C_j union {v}; distinct branches meet only at v. Connecting their trees through {v} preserves running intersection and edge coverage. Each recursive child is strictly smaller. Induction proves all decomposition obligations.

For a connected graph with n>=2, the leaf sizes obey sum(|B_leaf|-1)=n-1. Each leaf has at least two vertices, so there are at most n-1 leaves; every internal split has at least two children. There are O(n) bags, with total bag-vertex incidence O(n). Disconnected components and an empty root preserve this linear bound, including n=0 separately.

The elementary discovery makes O(n) recursive calls. Each may test at most n vertices with O(n+m) traversals/construction in an indexed implementation, giving the conservative bound O(n^2(n+m)). Validation, local cap-one discovery and at most four elementary matching computations per bag are polynomial under the same coarse bound, with normal indexing/sorting and ID-bit overhead charged separately. The research code favors simple checks over optimized constants.

Messages have values between zero and n; signed weights and offsets have O(log(n+1)) bits. The probe retains full subtree witnesses, using at most O(n^2) vertex occurrences, rather than claiming a minimal-memory implementation. Input IDs retain their encoded bit costs. No factor 2^(number of atoms) occurs.

The admitted class can be stated intrinsically as graphs whose articulation atoms each have odd-cycle-transversal number at most one. The cap-one property is hereditary under induced subgraphs. A connected atom with no cut vertex cannot straddle the private sides of an edge of any singleton-separator decomposition: an empty separator would disconnect it, and a one-vertex separator would be a cut. Thus it must lie in one bag. This explains why a different valid singleton-separator tree cannot hide an inadmissible atom inside otherwise admitted bags.

## Step 39 — a larger exact class and the two-vertex obstruction

For t disjoint pieces K_(p,p) plus a universal local apex, add bridge edges between consecutive apices. For p>=1 the graph has

\[
n=t(2p+1),\quad m=t(p^2+2p)+(t-1),\quad\alpha=tp.
\]

Each piece contributes at most p vertices to an independent set, and choosing one bipartition side in every piece attains tp. There are t vertex-disjoint triangles, one inside each piece, so every global bipartizing deletion set has size at least t; deleting all apices attains t. The new procedure nevertheless discovers and solves the composition using local cap one.

The retained t=10, p=12 run has 250 vertices, 1,689 edges, 29 bags, 527 tested cut candidates and optimum 120. The earlier whole-graph cap-one recognizer returns UNKNOWN on it. The 12-triangle chain similarly has global transversal number 12 and optimum 12, now solved by the discovered decomposition.

**Why not silently raise separator size to two:** a private vertex adjacent to boundary vertices u and v contributes one exactly when neither boundary vertex is selected. Its table is (1,0,0,0) on states (00,10,01,11), with nonzero mixed difference. It cannot be represented by an offset plus two unary weights.

The earlier Step 27 supplies a stronger exact obstruction to the proposed extension. For arbitrary H=(S,F), replace each edge uv by u-a_e-b_e-v. Take a central edgeless bag S and one path bag {u,a_e,b_e,v} for each source edge, arranged as a star. Every bag is bipartite, each separator has only TWO vertices, and running intersection holds. Yet

\[
\alpha(G)=|F|+\alpha(H).
\]

Thus arbitrary many two-vertex interfaces around a large central bag already encode the original arbitrary independent-set optimization. The local pieces being easy and each separator having constant size do not suffice. This reuses the previously proved reduction; no new execution of its old probe is claimed. It is not a proof that a polynomial algorithm cannot exist. It identifies exactly where the unary monotonicity argument stops and why the total coupling must be controlled.

## Proof audit and reproducible evidence

**Primary verdict: proved as written, by self-review**, for the displayed composition theorem, elementary discovery bound, declared graph class and explicit control families. Dependencies are the previous matching/cover and cap-one theorems, plus the restriction/union, monotonicity and cut arguments above. No external source leaf from the recovered SAT or meta-theory records is imported as a new solver assumption.

| Obligation | Audit outcome |
| --- | --- |
| Fixed input, repeated IDs, cross edges | Passed: full context binding and decomposition validation; stale graph, changed shared ID, missing cross edge and broken running intersection rejected. |
| Forced boundary and signed weights | Passed: parent counted once; negative forced contribution retained; nonpositive deletion applies only to unforced vertices. |
| Completeness of conditional scores | Passed: restriction/union induction, two states retained, missing state rejected; direct exhaustive checks of 67,023 message values. |
| Optimality and traceback | Passed: local matching/cover certificates, exact recurrence and original-ID union witnesses; inflated score/weight and duplicate records rejected. |
| Discovery and total work | Passed within stated indexed bound; no free tree, ordering oracle or global repair enumeration. |
| Scope | Passed: K4 returns UNKNOWN for this route, wider separators rejected; arbitrary weighted objectives excluded. |
| Universal P = NP target | Incomplete: U_COVER/U_LOCAL/U_MASS and normalized-core evaluation remain open. |

| Finite test | Result |
| --- | --- |
| All labeled simple graphs on 0–5 vertices | 1,100 total; 1,033 admitted with exact optimum; 67 UNKNOWN |
| Ordered shared-vertex pairs, each piece on 1–4 vertices | 75 x 75 = 5,625 pairs; 5,476 admitted with exact optimum; 149 UNKNOWN |
| Alternative roots on admitted pairs | 5,476 exact optimum agreements |
| Conditional message values against exhaustive induced-subgraph oracle | 67,023 checks |
| Corrupt/interface/scope controls | 10 expected rejections or UNKNOWN outcomes |
| Larger controls | 36-vertex triangle chain and 250-vertex large-piece bridge chain; explicit certificates |

Evidence: [probe](PNP_DEAN_ARTICULATION_PROBE_2026-09-30.py), [contract](PNP_DEAN_ARTICULATION_CONTRACT_2026-09-30.json), [result](PNP_DEAN_ARTICULATION_RUN_2026-09-30/result.json), [manifest](PNP_DEAN_ARTICULATION_RUN_2026-09-30/manifest.json), [stdout](PNP_DEAN_ARTICULATION_RUN_2026-09-30/stdout.txt), [stderr](PNP_DEAN_ARTICULATION_RUN_2026-09-30/stderr.txt). The new probe imports the unchanged [Step 30 probe](PNP_DEAN_PARITY_REPAIR_PROBE_2026-09-30.py), whose SHA-256 is `709c2f6933e414ebc9a1034dc53f565bc1b57211544f8da6a8c4b212aa6905d5`.

CPython 3.12.14; exact integers; no randomness. Run began 2026-09-30T03:47:41.462545Z and completed in 11.399185 seconds. Enforced bounds: 120 seconds wall, 90 seconds per-process CPU, 1 GiB address space, one core and one cooperative thread. The Mathbox version-2 validator checked input/output hashes successfully. The workspace was not a Git checkout; the manifest honestly records commit unavailable/dirty true while the contract and result pin the remote base. Assertions were enabled. This is research code, not a hardened input service.

New probe SHA-256: `fea7dcb37cdeb575e8aba747fd32645989eaf4ddc5ebdf9e38d71baa5d177c53`.
Result SHA-256: `f7acf72dd42172b1004e0e2a1c28f65adb6d600cd71f98979a927d778166fbad`.

Reproduce the scientific checks from the repository root:

```sh
python3 PNP_DEAN_ARTICULATION_PROBE_2026-09-30.py /tmp/dean-articulation-result.json
```

## Live handoff

The three executed mechanisms are: exact singleton-interface composition, charged articulation discovery, and the two-interface coupling counterexample. The first two succeed for the stated class; the third closes the naive extension based only on small individual separators. The general interface route remains open where a new property actually controls the joint interaction and is polynomially discoverable.

A next useful discriminator must therefore target a declared coupling restriction or a genuinely different way to evaluate the surviving core. It must not repeat unconditioned local scores, selected-circuit-cover signatures, a free optimal order, arbitrary widening to two interfaces, or a quotient defined by already knowing all answers. The original universal goal remains open.
