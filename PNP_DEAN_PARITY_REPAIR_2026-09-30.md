# Dean's fixed list — parity, one-vertex repair, and exact discovery

**Checkpoint:** Steps 30–34, September 30, 2026 UTC (September 29 evening in America/New_York). Research base: `redogit/redogit@e76004c44d4fc470f3d82a3c6ad795d92b4fecbc`, continuing [Steps 26–29](PNP_DEAN_COMPONENT_EXPRESSION_2026-09-30.md). The user's sustained-progression and public-profile instructions remain in force.

**Original goal:** an exact deterministic uniformly polynomial procedure for arbitrary finite Dean/Independent-Set inputs. That goal remains open. This checkpoint proves and implements a complete special case with polynomial recognition as well as optimization. The repair cap is **one vertex**. The original applicant list and exclusions remain fixed: both choices for that vertex are considered, rather than editing the supplied problem.

**What changed:** compact factors did not settle optimization in Step 27. Here, a precise parity test identifies the reach of one coordinate change; a small deletion set identifies a stronger exact route. A large connected example and a many-block counterexample distinguish these mechanisms from merely requiring every region to be small.

## Step 30 — exactly when bit flips repair the pairwise signs

Use the source conflict graph H=(V,F) from Step 27. Its relevant objective, omitting the constant |F|, is

\[
Q_H(x)=\sum_v x_v-\sum_{\{u,v\}\in F}x_ux_v,
\quad x_v\in\{0,1\}.
\]

Step 27 proved max Q_H=alpha(H), including witness recovery. Write E_H=-Q_H for the minimization form.

Allow only the declared reversible coordinate changes

\[
x_v=b_v+(1-2b_v)y_v=y_v\mathbin{\mathrm{xor}}b_v,
\quad b_v\in\{0,1\}.
\]

The coefficient of y_u*y_v in E_H after substitution is

\[
c_{uv}=(1-2b_u)(1-2b_v).
\]

Unary terms and constants change, but no pair interaction is lost. For any fixed other coordinates, the mixed difference on a pair is

\[
\Delta_{uv}=E(0,0)+E(1,1)-E(1,0)-E(0,1)=c_{uv}.
\]

For a nonedge it is zero. A binary pair is submodular precisely when this mixed difference is nonpositive. In this quadratic sum, all pairs have that property iff every edge has b_u != b_v. Thus:

> All pair interactions in this particular energy can be made submodular by individual bit flips **iff H is bipartite**.

**Proof of the graph equivalence:** a successful b assignment is exactly a two-coloring. Around an odd cycle, alternating the required bit returns the wrong value at the starting vertex, so no such assignment exists. Conversely, if a breadth-first coloring first meets an edge whose endpoints have the same color, the two parent paths to their lowest common ancestor and that edge form an odd cycle. If no such edge occurs, the coloring satisfies every edge. Disconnected components and isolated vertices are handled separately; the empty graph has the empty successful assignment.

This is an exact obstruction to this restricted coordinate move. It is not an obstruction to all representations, auxiliary variables, nonlinear changes, or general algorithms. We do not infer a graph-cut solver from a sign check or import a graph-cut representation theorem. When H is bipartite, the already proved matching/cover route supplies an exact solver directly. When H contains an odd cycle, a new name or a bit flip does not remove that cycle's incompatible parity requirements.

The finite check evaluates mixed differences from the complete transformed energy values, and compares them with the symbolic coefficient. It covers all 33,867 bit-flip assignments on all 1,100 labeled simple graphs with zero through five vertices, checking 167,012 edge-pair differences. The existence of a successful flip assignment agrees with the independent coloring result on every graph.

## Step 31 — one exceptional vertex, two exact branches

Let G=(V,E) be the fixed input graph. Suppose a vertex v is supplied and G-v is bipartite. Partition the independent sets into those omitting v and those containing v. In the latter class, every neighbor of v must be omitted. With N[v]={v} union N(v),

\[
\boxed{\alpha(G)=
\max\bigl(\alpha(G-v),\ 1+\alpha(G-N[v])\bigr).}
\]

Restriction proves each branch is an upper bound for its class. Conversely, a maximum independent set of G-v is valid in G, and adjoining v to a maximum independent set of G-N[v] is valid in G. This proves equality and reconstructs original-ID witnesses.

Both residuals are induced subgraphs of the bipartite graph G-v. By Step 28, each has a matching M and a vertex cover C of equal size. Their equality certifies the residual optimum |R|-|M|; the complement of C supplies a witness. The original answer is the maximum of the two certified scores. A YES needs a branch witness of size at least k. A NO needs both branch upper bounds below k. A failed search, missing branch, or stale certificate supplies neither.

For a supplied v, the two matching computations cost O(n(n+m)) using the elementary augmenting-path algorithm. Building residuals, checking covers/matchings, and reconstructing the final witness are polynomial. The stored two certificates require O(n+m) IDs/edges apart from bit lengths. A sorted-list implementation and the deliberately simple checker can add polynomial lookup/sorting overhead; the asymptotic indexed construction is not claimed as a microbenchmark of the probe.

The cap limits the exceptional set, not the total graph size. Take a complete bipartite K_(p,q) and add one new vertex adjacent to every old vertex, with p,q>=1. It is connected and nonbipartite. Removing the new vertex leaves K_(p,q). Its two branch scores are max(p,q) and one, so alpha=max(p,q). The run checks p=q=20: 41 vertices, 440 edges, branch scores 20 and one, and a 20-person witness with a matching/cover certificate. This example imposes no six-vertex bag cap and uses no exhaustive search over 41 vertices.

### Explicit negative certificate on the C9 control

Use C9 in the new fixture order 0-1-2-3-4-5-6-7-8-0; this is an explicitly relabeled cycle, not a silent change to Step 29's IDs. Choose v=0 and retain k=5.

| Branch | Residual vertices | Matching | Residual alpha | Total |
| --- | --- | --- | ---: | ---: |
| Omit 0 | {1,...,8} | {1,2}, {3,4}, {5,6}, {7,8} | 4 | 4 |
| Select 0 | {2,...,7} | {2,3}, {4,5}, {6,7} | 3 | 4 |

Covers {1,3,5,7} and {2,4,6} meet every respective residual edge and match those cardinalities. Both scores are four, proving NO at k=5. A maximum witness is {2,4,6,8}. The existing odd-cycle certificate also proves this NO; the branch method is not claimed necessary for that fixture.

## Step 32 — discover the repair instead of assuming it

The supplied-vertex requirement can be removed for the fixed cap of one.

1. Run a two-coloring check on G. If it succeeds, use the bipartite solver with no exceptional vertex.
2. Otherwise recover one explicit odd cycle C from the failed coloring.
3. For each vertex v of C, test whether G-v is bipartite.
4. If one succeeds, apply Step 31. If all fail, return UNKNOWN for the Dean optimization route and the precise structural fact that no deletion set of size at most one makes G bipartite.

**Completeness of discovery:** any vertex whose deletion makes G bipartite must lie on C. If it were outside C, that unchanged odd cycle would survive. Therefore testing only vertices of the recovered cycle loses no valid one-vertex repair. At most n coloring checks cost O(n(n+m)). Together with Step 31's two matching runs, the whole admitted procedure remains polynomial; there is no hidden assumption that a helpful decomposition or repair vertex is supplied for free.

There is also a checkable rejection record. Retain C and, for every v in C, an odd cycle C_v avoiding v. A candidate outside C fails because C survives; a candidate inside C fails because its C_v survives. At most n cycles of at most n IDs suffice. This proves nonmembership in the admitted one-vertex class. It does **not** prove that G lacks a k-person independent set.

### Why “pick any vertex of the cycle” fails

The bowtie graph has triangles {0,1,4} and {2,3,4}, meeting at vertex 4. From the first recovered triangle {0,1,4}, deleting 0 or 1 leaves the other triangle. Deleting 4 leaves two disjoint edges and is the valid repair. The retained run rejects candidates 0 and 1 with an explicit surviving cycle and then accepts 4. The branch scores are two when omitting 4 and one when selecting 4. Hence alpha=2.

The repair vertex is not necessarily part of a maximum independent set. “It repairs the structure” does not imply “select it”; both branches remain necessary.

## Step 33 — state the parameter cost before allowing more repairs

For a supplied set X such that G-X is bipartite, let r=|X|. For each independent T subset of X, define

\[
R_T=V\setminus\bigl(X\cup N(T)\bigr).
\]

Fixing I intersection X=T gives the exact identity

\[
\alpha(G)=
\max_{\substack{T\subseteq X\\T\text{ independent}}}
\bigl(|T|+\alpha(G[R_T])\bigr).
\]

**Proof:** every global independent set restricts to an independent T and avoids all its neighbors. Its remaining vertices lie in R_T. Conversely, T can be joined to any independent set of G[R_T]. Each residual is induced in G-X and therefore bipartite. Apply the matching/cover certificate separately to every feasible T.

There are at most 2^r branch states. Straight enumeration with matching costs O(2^r*n(n+m)), plus input validation and polynomial bookkeeping. If all branch certificates are retained, their size also includes that 2^r factor. The default implementation still caps r at one. Two supplied r=2 fixtures are explicit controls, not automatic scope expansion:

- Two triangles joined by a bridge need two deletions. With one designated nonbridge vertex from each triangle as X, all four subsets are feasible; the cap-two control returns alpha=2. The cap-one call returns UNKNOWN.
- K4 with X={0,1} leaves an edge, but X itself is not independent. Exactly three branch states are feasible, not four. The control returns alpha=1 and rejects a duplicated branch.

For any fixed constant r, trying all at-most-r subsets to discover X adds O(n^r(n+m)) straightforward work. That is a family of fixed-cap polynomial bounds, whose exponent depends on the cap. It is not one uniformly polynomial unrestricted discovery bound when r grows.

If a suitable X is supplied with r<=c*log2(max(2,n)) for a fixed constant c, then 2^r is polynomial in n and the stated optimization bound is polynomial. Naively discovering such an X by n^r enumeration does not supply the same polynomial bound. This distinction concerns the elementary discovery method here, not a claim that stronger parameterized algorithms do not exist. No unchecked external discovery bound is imported.

The usual name for X is an **odd-cycle transversal**: deleting it meets every odd cycle and leaves a bipartite graph. This is a structural condition on the original graph; it does not authorize removing applicants from the decision obligation.

## Step 34 — global repair count and actual difficulty can diverge

For t>=1, take disjoint triangles B_i={3i,3i+1,3i+2}, i=0,...,t-1, and add bridge edges {3i,3(i+1)} between consecutive triangles.

**Exact properties:**

- The graph is connected, with n=3t and m=4t-1.
- Every odd-cycle transversal must meet each of the t vertex-disjoint triangles, so its size is at least t.
- Deleting X={3i+1:0<=i<t} leaves a path on the bridge vertices, with one leaf attached at each, hence a forest. The minimum odd-cycle transversal size is therefore exactly t.
- Every independent set uses at most one vertex per triangle. X itself is independent, so alpha=t.
- Since X is independent, blindly enumerating all T subset of this particular X really does create 2^t feasible branches, although this graph's optimum is immediate from the disjoint clique upper bound and X as a witness.

At t=100, the run checks the 300-vertex graph, its 399 edges, the 100-set witness, every triangle, and the bipartite residual after deleting X. The general t statement is proved above; the run does not enumerate 2^100 subsets.

This is a counterexample to “many global repairs imply the graph is hard” and to using the size of one global branch table as an algorithm-independent runtime lower bound. It is also a scope counterexample for the cap-one route once t>=2, regardless of whether a particular target k is YES or NO.

The prior Step 22 composition applies too: arrange triangle bags and two-vertex bridge bags in alternating path order. Bags have size at most three and adjacent intersections size one, with all edge coverage and running-intersection conditions satisfied. This is a reuse of the earlier theorem, not a new decomposition algorithm or a new run of that earlier probe.

The two controls expose different advantages. K_(p,q) plus one universal vertex can have a large connected region but one structural exception. The triangle chain has arbitrarily many global exceptions but a small interface between easy regions. Neither parameter dominates every useful instance. Combining their mechanisms needs an explicit interface theorem and a charged admission procedure.

## Source relation and connection to earlier gammoid work

The verified primary source is Kratsch and Wahlström, *Compression via Matroids: A Randomized Polynomial Kernel for Odd Cycle Transversal*, [arXiv:1107.3068v2](https://arxiv.org/abs/1107.3068v2), revision October 6, 2011. The retrieved PDF identifies v2 on its margin but displays October 29, 2018 on its title page; both are recorded rather than conflated. Sections 2–3, Proposition 1 and Corollary 2 connect terminal linkage after deletions to gammoid independence and a randomized matrix representation. Their terminal set corresponds to a boundary with declared source, destination and deletion roles; their independent columns encode vertex-disjoint linkage, not a conflict-free Dean cohort. Their representation has one-sided error, unlike this checkpoint's exact certificates. This is an adjacent mechanism connecting to the user's earlier gammoid research, with no solver transfer admitted.

Source checked September 30, 2026 via retrieved PDF, without a local PDF cache. The 2004 Reed–Smith–Vetta paper was discovered, but its direct full text was unavailable; no theorem from it is a proof dependency here. The elementary arguments above are self-contained.

A polynomial-size representation for a different decision problem does not automatically preserve alpha(G), every conditional branch score, or a reconstructible Dean witness. A future transfer must specify those maps and prove the required preservation. No novelty claim is made for bipartization, parity switching, or conditioning on a small deletion set.

## Audit and finite evidence

**Scoped audit verdict: proved as written, by self-review.** This verdict applies to the displayed identities, parity criterion, cap-one discovery procedure, and explicit families. The unrestricted polynomial goal remains incomplete.

Dependencies are the exact Step 27 penalty identity, the Step 28 matching/cover theorem, and the internal restriction/union, coloring, and disjoint-triangle arguments. The source note is attribution and an adjacent route; no randomized-matrix theorem is a load-bearing leaf of the new solver.

| Audit obligation | Status and evidence |
| --- | --- |
| Fixed graph and original IDs | Passed: residuals preserve IDs; full source identity is checked; a nonconsecutive-ID fixture passes. |
| Bit-flip signs and quantifiers | Passed: algebra plus finite differences computed from full energy evaluations; odd-cycle parity obstruction explicit. |
| Both branches and completeness | Passed: independent-set partition proof, missing/duplicate branch rejection, both conditional bounds retained. |
| Matching optimality | Passed: actual input edges, disjoint endpoints, full cover, and equal matching/cover size checked. |
| Admission discovery cost | Passed: every valid one-vertex deletion lies on the recovered odd cycle; at most n coloring checks. |
| Admission failure versus graph NO | Passed: rejection proves only no size-at-most-one transversal; Dean status remains UNKNOWN. |
| Nullary/unary and disconnected cases | Passed: exhaustive graphs include n=0 and n=1; coloring starts at every component. |
| Stale and corrupt evidence | Passed: changed graph, false matching, empty cover, inflated score, missing branch and duplicate branch rejected. |
| Growing repair count | Passed within stated bounds: 2^r charged explicitly; no unrestricted polynomial conclusion. |
| Global lower-bound claim | Refuted for the proposed inference by the triangle-chain family. No claim about every algorithm. |
| External matrix transfer | Not admitted: linkage preservation is not yet preservation of all Dean conditional optima. |

Retained evidence: [probe](PNP_DEAN_PARITY_REPAIR_PROBE_2026-09-30.py), [contract](PNP_DEAN_PARITY_REPAIR_CONTRACT_2026-09-30.json), [result](PNP_DEAN_PARITY_REPAIR_RUN_2026-09-30/result.json), [version-2 manifest](PNP_DEAN_PARITY_REPAIR_RUN_2026-09-30/manifest.json), [stdout](PNP_DEAN_PARITY_REPAIR_RUN_2026-09-30/stdout.txt), [stderr](PNP_DEAN_PARITY_REPAIR_RUN_2026-09-30/stderr.txt).

| Finite coverage | Result |
| --- | --- |
| All labeled simple graphs with n=0,...,5 | 1,100 graphs |
| Bipartite graphs | 428 |
| Additional graphs admitted by one vertex | 605 |
| Total admitted by cap one | 1,033; exact optimum agrees with separate exhaustive independent-set enumeration |
| Outside cap one | 67; explicit surviving-cycle rejection records |
| Coordinate switches | 33,867; 167,012 mixed differences |
| Certified residual branches | 1,638; serialization round trips checked |
| Further discriminators | Bowtie, C9, bridged triangles, K4, nonconsecutive IDs, 41-vertex single-repair case, 300-vertex triangle chain |

The local execution connection recovered for this continuation. The recorded CPython 3.12.14 run completed in 1.118229 seconds using exact integers, no random sampling, a 45-second wall cap, 30-second per-process CPU cap, 1 GiB address-space cap, one core and one cooperative thread cap. The installed Mathbox manifest validator passed with input and output hashes checked. There was no local Git checkout; the manifest records commit unavailable/dirty true, names the remote base explicitly, and pins the executed script before and after. The later repository commit retains those exact bytes.

Probe SHA-256: `709c2f6933e414ebc9a1034dc53f565bc1b57211544f8da6a8c4b212aa6905d5`.
Result SHA-256: `28d4d2ce9c8474b9364018d9ec726d73d817a5937962ee766c6f1e59af51aabd`.

To reproduce the scientific checks from the repository root:

```sh
python3 PNP_DEAN_PARITY_REPAIR_PROBE_2026-09-30.py /tmp/dean-parity-result.json
```

The exhaustive oracle is capped at 18 vertices and actually enumerates only graphs through five vertices in this run. Large controls use explicit certificates and their separately stated proofs. The probe is research code, invoked without Python's assertion-disabling optimization flag; it is not a hardened public input service. Finite success and the recorded runtime do not replace the uniform proofs.

## Practical meaning and live research state

For a task-selection or conflict-roster model, the one exceptional person is a conditional interface: solve the case where they are absent and the case where they are selected with their incompatible neighbors absent. Each case returns both a concrete cohort and evidence bounding its best possible size. That makes a negative answer reviewable as well as a positive one. The supplied conflict list remains unchanged. This models pairwise incompatibilities only; no claim about a deployed admissions or scheduling system is made.

In the user's identity and carrier language, the applicant IDs are the Objects, the two branch states are distinct Surfaces for the same input, and the branch certificates retain the Homeward path to an actual cohort. A structural repair preserves the obligation only when all consequential branches and their costs survive. A coordinate flip preserves all assignments but may leave the parity obstruction. A decomposition can separate independent choices without pretending those choices are identical.

The executed routes have distinct outcomes:

- **Coordinate route:** complete characterization for individual bit flips; odd cycles obstruct that move. Closed only for the claim that this move handles arbitrary pairwise conflict graphs.
- **One-vertex route:** exact recognition, optimization, and witnesses established for the declared cap. Complete as a special-case procedure; no unrestricted extension claimed.
- **Growing-parameter route:** exact supplied-set formula established with its exponential branch factor. Global repair count alone is ruled out as a universal measure of actual difficulty.
- **Composition route:** the triangle chain is already handled by retained clique bounds or Step 22's decomposition. An interface combining large bipartite pieces with local exceptional vertices remains open.
- **Gammoid route:** relevant literature connection recovered; transfer to exact Dean conditional scores remains unproved and is deferred until that precise representation question is posed.

The next discriminating obligation is to supply and verify an interface between large solvable pieces, retain the conditional scores needed at that interface, and prove both construction and optimization cost without multiplying every local binary choice globally. A first executable case is a tree of large bipartite pieces with one exceptional vertex per piece and shared articulation IDs; the overlap accounting and witness rules must be proved before importing a weighted matching or cut routine. This is a proposed continuation, not an implemented result. The original unrestricted goal remains open: `P ?= NP`.

