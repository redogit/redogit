# Signed Binary-Cluster Augmentation Carrier — 2026-09-25

**Target research program:** P vs NP through the DEAN / Independent-Set obligation  
**Claim ceiling:** scoped exact theorem; **not** a universal P=NP proof  
**Status:** theorem proved below; bounded exhaustive implementation check also recorded

## 1. Context

Let S be the current independent cohort and R = V(G) \ S the outside candidates.

Build the bipartite support graph from candidates R to current members S: a candidate b is adjacent to s in S exactly when selecting b would force s out.

The support graph induces a transversal matroid M_S on ground set R:

    X is independent in M_S
    iff
    X can be matched injectively into S.

A +1 Dean augmentation exists exactly when M_S has a circuit that is independent in the candidate-candidate conflict graph.

This file proves an exact signed carrier for the case where:

1. the relevant support matroid is binary and supplied with an exact GF(2) representation; and
2. the candidate-conflict graph is a disjoint union of cliques.

The clique components are treated as colors. A conflict-free set then contains at most one element of each color.

## 2. Support-Transversal Circuit Augmentation Lemma

Let B be a candidate-conflict-independent subset of R and write W = N(B) intersect S.

If B is a circuit of the support transversal matroid M_S, then

    |B| = |W| + 1.

Reason: a transversal-matroid circuit is minimally unmatchable. Every proper subset of B is matchable into W, while B itself is not. Hall's theorem therefore gives deficiency exactly one.

Hence

    S' = (S \ W) union B

is independent and |S'| = |S| + 1.

Conversely, every +1 augmentation contains an inclusion-minimal support-deficient subset, and that subset is a support-matroid circuit that remains candidate-conflict independent.

Therefore:

    +1 Dean augmentation
    iff
    candidate-conflict-free circuit of M_S.

## 3. Binary-cluster theorem

Let M be a binary matroid of rank r, represented by an r x n matrix over GF(2).

Assume its ground set is partitioned into exactly r nonempty conflict cliques / color classes C_1, ..., C_r.

A set is candidate-conflict independent exactly when it is rainbow: it contains at most one element of each color.

### Theorem

There is a deterministic polynomial procedure that returns exactly one of:

    POSITIVE:
        a rainbow circuit of M

    NEGATIVE:
        a certificate that M has no rainbow circuit.

When M = M_S, the positive result gives an exact |S| -> |S|+1 Dean augmentation. The negative result proves that no +1 augmentation exists; by the minimal-augmentation theorem, S is maximum.

## 4. Construction

Choose one arbitrary element b_i in C_i from every color.

### Case A — the initial transversal is dependent

If B = {b_1, ..., b_r} is dependent, extract any circuit contained in B.

It is automatically rainbow. Return POSITIVE.

### Case B — the initial transversal is a basis

Otherwise B is a basis because it contains r independent elements in a rank-r matroid.

Express every element in basis coordinates, so b_i = e_i.

For an element v in C_i, let v_j denote its j-th GF(2) coordinate.

#### B1 — immediate one-degree positive move

If some v in C_i has v_i = 0, replace b_i by v.

The determinant of the resulting transversal equals the replacement coordinate v_i = 0, hence the transversal is dependent. Extract its rainbow circuit and return POSITIVE.

So from here onward every v in C_i satisfies v_i = 1.

#### B2 — dependency digraph

Create a directed graph D on color indices 1,...,r.

Add j -> i for j != i exactly when some element v in C_i has v_j = 1.

Retain one exact witness element for every directed edge.

### Case B2-NEGATIVE — D is acyclic

Take a topological ordering of D.

For any rainbow transversal, its chosen column from color i has:

- diagonal coordinate i equal to 1;
- nonzero off-diagonal coordinates only at predecessor vertices of i.

Thus every rainbow-transversal matrix is triangular in the topological order with all diagonal entries equal to 1.

Therefore every full rainbow transversal is a basis.

Any rainbow circuit could be extended by arbitrary representatives from unused colors to a dependent full rainbow transversal, contradiction.

Hence no rainbow circuit exists. Return NEGATIVE with the topological order and coordinate-support receipts.

### Case B2-POSITIVE — D contains a directed cycle

Choose a shortest directed cycle

    i_1 -> i_2 -> ... -> i_k -> i_1.

For every cycle edge i_t -> i_(t+1), choose its retained witness column from color i_(t+1).

Use basis columns for all colors outside the cycle.

Because the directed cycle is shortest, no selected cycle column has a nonzero coordinate at another cycle vertex except:

- its own diagonal coordinate; and
- its predecessor on the cycle.

Any additional cycle-to-cycle nonzero coordinate would be a directed chord and, together with the appropriate directed portion of the cycle, would create a shorter directed cycle.

Therefore the cycle block of the selected transversal is I + P, where P is the permutation matrix of the directed cycle.

Over GF(2),

    (I + P) * 1 = 0

because P * 1 = 1.

So the cycle block is singular, and therefore the full rainbow transversal is singular.

Extract a circuit from it. Return POSITIVE.

## 5. Cost

With a supplied exact binary matrix representation:

- basis test / Gaussian elimination: polynomial;
- conversion to basis coordinates: polynomial;
- scanning coordinates to build D: polynomial;
- topological sort or directed-cycle detection: linear in D;
- shortest directed cycle: polynomial;
- circuit extraction from a singular transversal: polynomial;
- certificate verification: polynomial.

No subset-valued state and no exponential search is introduced by this carrier.

## 6. Relationship to published matroid theory

Bérczi and Schwarcz proved that a rank-r binary matroid colored with exactly r colors either has a rainbow circuit or a monochromatic cocircuit, and characterized rainbow-circuit-free colorings through rank-preserving reductions to partition matroids / standard colorings.

The dependency-digraph construction above is a direct executable specialization in GF(2) basis coordinates. The external theorem supports the structural boundary; the proof in this file supplies the concrete constructive route used by this research program.

## 7. Bounded verification

A separate exhaustive checker enumerated all canonical color families containing the identity basis for:

    r = 2 : 16 configurations
    r = 3 : 262,144 configurations

For all 262,160 checked configurations there were zero mismatches between:

    a singular rainbow transversal exists

and

    some same-color column has zero diagonal coordinate
    OR
    the dependency digraph contains a directed cycle.

This finite panel is validation evidence only; the proof above is the theorem argument.

## 8. Scope boundary

This theorem does not establish a universal Independent-Set algorithm.

The live remainder includes at least:

- arbitrary candidate-conflict graphs rather than disjoint conflict cliques;
- nonbinary support transversal matroids;
- states where the number of conflict cliques does not match the relevant binary rank;
- preservation of this carrier's preconditions after an augmentation.

Those residuals remain explicit.

## 9. Signed one-degree interpretation

The carrier gives the exact desired two-way behavior inside its scope:

    directed dependency cycle
        -> POSITIVE
        -> exact +1 augmentation

    acyclic dependency graph
        -> NEGATIVE
        -> no +1 augmentation
        -> current S is maximum

No second independent degree is silently changed.

GENERATE != VERIFY != ADMIT

SCOPED THEOREM != UNIVERSAL P=NP PROOF


## 10. Log-cluster-defect extension

The cluster-graph requirement can be relaxed by one bounded defect family without changing the original Dean constraints.

Let H be the candidate-conflict graph and let Z be a **carrier exception set** such that H-Z is a disjoint union of cliques.

Z is not deleted from the mathematical problem. It is separated into an explicit exception carrier so that every choice involving Z remains reconstructible.

Assume:

1. the support matroid M is binary and supplied with an exact GF(2) representation;
2. |Z| = k;
3. for every stable independent exception choice A subseteq Z that is reached below, the residual cluster color count c_A is at least the residual matroid rank r_A whenever that branch is needed for complete closure.

### Exact branch construction

Enumerate every conflict-stable subset A of Z.

#### A is already dependent in M

Then A contains a conflict-free circuit. Return POSITIVE.

#### A is independent in M

Remove from the outside carrier every candidate conflicting with A and set

    R_A = (E(M) \ Z) \ N_H(A).

Contract A in the support matroid and restrict to R_A:

    M_A = (M / A) | R_A.

Because binary matroids are closed under minors, M_A remains binary.

Because H-Z is a cluster graph, H[R_A] is also a cluster graph.

Let:

    c_A = number of nonempty conflict cliques in H[R_A]
    r_A = rank(M_A).

##### c_A > r_A

Choose one element from any r_A + 1 distinct cliques.

The chosen set is conflict-free but has cardinality larger than rank(M_A), so it is dependent. Extract a circuit and return POSITIVE.

##### c_A = r_A

Run the signed binary-cluster carrier proved above.

It either returns a conflict-free circuit (POSITIVE) or certifies that no such circuit exists in this branch.

##### c_A < r_A

This carrier does not claim completeness for the branch. Return branch status UNRESOLVED rather than laundering the gap into NO.

### Completeness inside the guard

Suppose the original instance has a conflict-free support-matroid circuit C.

Let

    A = C intersect Z
    Y = C \ A.

A is conflict-stable.

If A is dependent, its branch returns POSITIVE.

Otherwise A is independent. Since C is conflict-free, Y is contained in R_A. Moreover

    A union Y

is dependent in M, so Y is dependent in M/A.

Therefore the exact A-branch contains a conflict-free dependent set in the residual binary cluster carrier. If c_A > r_A it is detected by rank. If c_A = r_A it is detected by the binary-cluster theorem.

Consequently, if every stable branch satisfies the stated rank/color guard and every branch returns NEGATIVE, then no original conflict-free circuit exists.

### Cost

Cluster Vertex Deletion is fixed-parameter tractable; published algorithms include O*(1.811^k).

After a suitable Z is obtained, this carrier uses at most

    2^k

exception subsets, with polynomial work per branch.

Hence for

    k = O(log n)

the full guarded carrier has polynomial total cost.

The fixed-parameter search is used only to locate the carrier exception set. The original conflict graph remains authoritative and unchanged.

### Bounded differential validation

A separate random exact checker generated binary matrix matroids, conflict graphs whose deletion of at most two designated exception vertices leaves a cluster graph, and compared the guarded carrier result against brute-force conflict-free dependence.

Results:

    generated cases: 5,000
    cases decided by the theorem guard: 4,195
    mismatches: 0

This is bounded implementation evidence only. The proof above supplies the scoped mathematical claim.

## 11. New remainder after the extension

The conflict-side residual is now narrower:

- binary support with large cluster-deletion distance;
- guarded branches where c_A < r_A;
- nonbinary support;
- preservation/rotation between these carriers after repeated +1 augmentations.

The next one-degree repair should target one of these residuals directly rather than modifying already-closed binary/cluster cases.


## 12. Forest-support admission theorem

The binary-support precondition has a direct Dean-level sufficient condition that avoids abstract binary-matroid recognition.

Let B=(R,S;E_B) be the bipartite support graph between outside candidates R and the current cohort S.

Assume B is a forest.

Form the |S| x |R| zero-one adjacency matrix A over GF(2):

    A[s,b] = 1 iff candidate b conflicts with current member s.

### Theorem

A candidate subset X subseteq R is matchable injectively into S if and only if the columns A[X] are linearly independent over GF(2).

Therefore A is an exact binary representation of the support transversal matroid.

### Proof

If X is matchable, choose |X| support vertices used by a matching covering X and inspect the corresponding |X| x |X| square submatrix.

A bipartite forest cannot contain two distinct perfect matchings on the same square subgraph: the symmetric difference of two distinct perfect matchings would contain an alternating cycle.

Hence the determinant expansion contains exactly one nonzero matching permutation. Its determinant is 1 over GF(2), so A[X] has full column rank.

Conversely, if A[X] has full column rank, some |X| x |X| minor has nonzero determinant. The determinant expansion therefore contains at least one nonzero permutation, which is a matching covering X.

Thus matchability and GF(2) column independence coincide.

### Consequence

When:

1. the support graph B is a forest;
2. the candidate-conflict graph is a cluster graph;
3. the cluster/color count satisfies the binary-cluster carrier's rank guard;

the signed binary-cluster theorem can run directly on the original Dean relations using A as its exact binary matrix.

No separate matroid-representation discovery step is required.

### Bounded implementation validation

A separate checker generated random bipartite forests with up to seven vertices on each side and compared matching feasibility against GF(2) column rank on random candidate subsets.

Results:

    subset comparisons: 25,000
    mismatches: 0

This is bounded implementation evidence; the determinant/matching argument above is the theorem.

## 13. Support-side remainder

A cyclic support graph is now an explicit next-degree residual.

The forest theorem does not justify deleting support edges from the original obligation. Any future repair must preserve all support edges semantically and move only the carrier representation.

A promising bounded direction is to treat a small support-cycle defect as an explicit exception carrier, analogous to the log-cluster-defect treatment on the candidate-conflict side, but no universal theorem for that extension is claimed here.


## 14. One-cycle support obstruction

The first support-cycle degree is not harmless.

Consider two current support vertices s0,s1 and four outside candidates:

    x0 -> {s0,s1}
    x1 -> {s0,s1}
    p  -> {s0}
    q  -> {s1}

The support presentation contains exactly one K2,2 cycle on x0,x1,s0,s1, with p and q attached as one-sided candidates.

### Exact support matroid

Every pair of candidates is matchable into {s0,s1}:

- x0,x1 use opposite supports;
- xi,p assigns p->s0 and xi->s1;
- xi,q assigns q->s1 and xi->s0;
- p,q use s0,s1.

No set of three candidates can be matched into two supports.

Therefore the support transversal matroid is exactly

    U_{2,4}.

U_{2,4} is the canonical excluded minor for binary representability, so this one-cycle support presentation is genuinely nonbinary.

### No lossless one-edge deletion

Deleting any one of the four cycle edges changes the matchability relation.

Example:

    delete x0--s0.

Then x0 and q are both restricted to s1 and the pair {x0,q}, previously matchable, is no longer matchable.

The other cycle edges are symmetric.

Hence:

    forest -> one support cycle

cannot be implemented as

    delete one cycle edge -> reuse forest carrier.

That would change the Dean obligation rather than merely change its carrier.

### Bounded validation

A separate exhaustive enumeration checked connected simple bipartite unicyclic presentations for side sizes up to 4 x 4 until the first counterexample was reached.

    connected unicyclic presentations examined before witness: 729

The witness above is the first retained obstruction from that enumeration under its generation order. The mathematical U_{2,4} argument, not enumeration order, is the evidence for the boundary.

### Next degree

The correct next support-side degree is therefore:

    BINARY SUPPORT
        ->
    EXPLICIT NONBINARY OBSTRUCTION

rather than destructive cycle removal.

For transversal/gammoid matroids, published structure identifies U_{2,4} and M(K4) as excluded-minor obstructions to the binary-gammoid class. Future repair should preserve such an obstruction as a first-class residual and move to a carrier capable of representing it exactly.


## 15. Support-component direct-sum and bounded-rank closure

The U(2,4) obstruction does not require an immediate global field change.

Let B=(R,S;E_B) be the candidate-to-current-cohort support presentation. Decompose B into connected bipartite components

    B_1, ..., B_t.

Let R_i be the candidate side and S_i the current-cohort side of component B_i.

### Direct-sum theorem

The support transversal matroid decomposes as

    M_S = M_1 direct-sum ... direct-sum M_t,

where M_i is the transversal matroid presented by B_i.

Reason: every support matching is the disjoint union of its component matchings, and no candidate in R_i can use a support vertex outside S_i.

Therefore every matroid circuit is contained entirely in one R_i.

This has an important Dean consequence:

    +1 augmentation exists globally
    iff
    some support component contains a candidate-conflict-free circuit.

Candidate-conflict edges joining different support components do not affect this existential circuit test because a circuit never uses candidates from two distinct direct-sum components.

### Bounded-rank circuit closure

Let a support component M_i have rank at most d.

Every circuit C of M_i satisfies

    |C| = rank(C) + 1 <= d + 1.

Therefore, for fixed constant d, enumerate all candidate subsets

    C subseteq R_i
    with
    1 <= |C| <= d+1.

For each C:

1. verify candidate-conflict independence in the original Dean graph;
2. verify C is dependent in the support transversal matroid by maximum matching;
3. verify every proper one-element deletion C-{x} is support-matchable.

If all three hold, C is a stable support-matroid circuit and yields an exact +1 Dean augmentation.

If no component contains such a circuit, and every support component has rank at most d, then no +1 augmentation exists and the current cohort S is maximum.

### Complexity

For fixed d, circuit enumeration costs at most

    sum_i O(|R_i|^(d+1) * poly(n))

and matching/candidate-conflict verification is polynomial.

Hence:

    fixed maximum support-component rank
    -> exact polynomial augmentation-or-certify.

### U(2,4) closure

The first one-cycle obstruction retained in Section 14 has rank 2.

All circuits of U(2,4) are 3-element subsets.

Thus the obstruction is completely handled by the d=2 bounded-rank carrier:

    stable 3-circuit exists
        -> exact +1 augmentation

    no stable 3-circuit
        -> no augmentation through that support component.

No GF(3) representation is required for this local closure.

### Bounded differential validation

A separate random checker compared:

- brute-force search for any candidate-conflict-free support circuit; and
- componentwise enumeration of all circuits of size at most 3

on random support/conflict instances for which every support component had rank at most 2.

Results:

    generated cases: 10,000
    eligible cases: 7,978
    mismatches: 0

This finite panel is implementation evidence only. The direct-sum and circuit-size arguments above are the scoped theorem.

## 16. New support-side remainder

The support-side obstruction has moved from “first nonbinary cycle” to:

    support components of unbounded rank
    that are not already covered by the binary/cluster carriers.

The next one-degree support question is therefore not whether U(2,4) is representable over a larger field, but whether one can expose a polynomially bounded separator / decomposition / rank defect inside an unbounded-rank connected support component while preserving the exact matching semantics.


## 17. Exact support-signature entropy carrier

The cluster-conflict family admits another exact carrier that does not require binary support.

Let the candidate-conflict graph on one support component be a disjoint union of nonempty cliques / color classes

    C_1, ..., C_c.

Let M be the support transversal matroid presented directly by the candidate-to-current-cohort bipartite support graph.

### Full-rainbow reduction

A candidate-conflict-free circuit exists if and only if there is a **full rainbow transversal**

    X = {x_1, ..., x_c},  x_i in C_i,

that is dependent in M.

Proof:

- if a full rainbow transversal is dependent, it contains a matroid circuit, and that circuit remains rainbow/conflict-free;
- if a rainbow circuit uses only some colors, extend it by choosing one arbitrary candidate from every unused color. Matroid dependence is monotone under supersets, so the resulting full rainbow transversal is still dependent.

Thus the search need not enumerate arbitrary subsets.

### Exact semantic quotient within one color

For candidates x,y in the same color C_i, define

    x ~_S y
    iff
    N_S(x) = N_S(y),

where N_S(x) is the exact set of current-cohort support vertices adjacent to x.

Candidates equivalent under ~_S are interchangeable for support matchability because every matching query sees the same candidate-to-support neighborhood.

The quotient does **not** merge authoritative occurrences:

- every candidate keeps its OccurrenceID / original student ID;
- the quotient key is a derived SemanticObjectID for the current support-neighborhood signature;
- Homeward retains the occurrence list for each signature.

Let

    t_i = number of distinct support-neighborhood signatures in C_i.

Choose one representative for each signature.

### Theorem

Enumerate all

    product_i t_i

full tuples of support-signature representatives, one from each color.

For each tuple X:

1. compute maximum bipartite matching from X into the current cohort S;
2. if the matching size is |X|, continue;
3. if the matching size is smaller, X is support-dependent;
4. repeatedly delete elements while dependence persists to extract an inclusion-minimal dependent rainbow subset C;
5. C is a conflict-free support-matroid circuit and therefore gives an exact +1 Dean augmentation.

If every signature tuple is matchable, then every raw full rainbow transversal is matchable, hence no rainbow circuit exists and the current cohort is maximum.

### Polynomial envelope

Define exact support-signature choice entropy

    H_sig = sum_i log2(t_i).

Then

    product_i t_i = 2^(H_sig).

Hence if

    H_sig = O(log n)

with a fixed constant in the O(log n) bound, total enumeration and matching cost are polynomial.

Equivalently, the carrier is polynomial whenever

    product_i t_i <= n^c

for a fixed constant c.

This condition is checked directly; no claim is made when the product is superpolynomial.

### Why this is anti-decay rather than lossy compression

The quotient removes only a coordinate that is provably irrelevant to the current support-matching obligation: which same-color occurrence realizes an identical current support neighborhood.

It does not identify different original students globally, transfer evidence, or erase provenance.

If the support context changes later, signatures are recomputed from the new context and the old occurrence/signature relation remains in history.

### Bounded differential validation

A separate random checker generated arbitrary transversal support presentations and cluster-conflict color classes, then compared:

- brute-force raw one-per-color rainbow-transversal dependence; and
- enumeration after exact same-color support-neighborhood quotienting.

Results:

    generated instances: 10,000
    mismatches: 0

This finite panel is implementation evidence only. The full-rainbow extension and matching-equivalence arguments above are the scoped theorem.

## 18. Updated cluster-conflict remainder

For arbitrary transversal support plus cluster conflicts, the unresolved instances can now be required to have simultaneously:

- an unbounded-rank connected support component;
- support-signature choice product larger than every admitted fixed polynomial bound;
- no immediate rank-vs-color positive certificate;
- and no applicability of the binary / bounded-rank / log-cluster-defect carriers.

This is a narrower representation-selection obstruction than the original raw candidate search.


## 19. Minimal support-signature antichain repair

The support-signature entropy carrier admits an exact one-degree reduction before any Cartesian enumeration.

Fix one candidate-conflict clique / color C_i.

For candidates a,b in C_i, write

    a <=_S b

when

    N_S(a) subseteq N_S(b).

If the inclusion is strict, b is support-dominated by a for the purpose of finding a +1 augmentation.

### Dominance theorem

Suppose a full rainbow selection X contains b and is support-dependent.

Replace b by a, where a and b are in the same conflict clique and

    N_S(a) subseteq N_S(b).

Call the new full rainbow selection X'.

Any matching covering X' would also cover X after replacing the edge incident with a by the same support assignment for b only if that assignment lies in N_S(b); more directly, shrinking one left vertex's allowed support neighborhood cannot increase maximum matching size.

Therefore

    rank_support(X') <= rank_support(X) < |X| = |X'|,

so X' remains dependent.

Consequently every dependent raw rainbow transversal can be transformed, color by color, into a dependent transversal using only inclusion-minimal support neighborhoods in each color.

### Exact carrier

Within each color:

1. quotient identical support neighborhoods as in Section 17;
2. remove every quotient signature that strictly contains another signature of the same color;
3. retain the removed occurrences and dominance edge for Homeward/provenance;
4. enumerate only the remaining inclusion-minimal signatures.

Let

    a_i = number of inclusion-minimal distinct support signatures in color C_i.

The exact enumeration count becomes

    product_i a_i

rather than

    product_i t_i.

Define minimal-antichain entropy

    H_min = sum_i log2(a_i).

If

    H_min = O(log n)

under a fixed admitted bound, exact augmentation-or-certify remains polynomial for arbitrary transversal support.

### Anti-decay boundary

A dominated candidate is not declared semantically equal to its dominator.

Only its role in the current support-deficiency search is dominated.

The authoritative occurrence, original student ID, full conflict relations, and historical support neighborhood remain preserved. If S changes, the order is recomputed.

### Bounded differential validation

A separate random checker compared raw full-rainbow dependence against enumeration restricted to inclusion-minimal same-color support signatures.

Results:

    generated instances: 10,000
    mismatches: 0

The proof above is the theorem; this panel is bounded implementation evidence.

## 20. Updated entropy remainder

Any cluster-conflict residual outside the current exact carrier must now have a superpolynomial product of inclusion-minimal support-neighborhood antichains, not merely many raw candidates or duplicate support signatures.

That is the next exact representation-selection obstruction on the cluster side.


## 12. Binary gammoid -> series-parallel support carrier

The binary support-transversal hypothesis has a stronger structural consequence than an arbitrary GF(2) representation.

The support matroid M_S is transversal by construction from the candidate-to-current-cohort bipartite support graph.

Every transversal matroid is a gammoid. A classical characterization of binary gammoids states that the following are equivalent:

    binary gammoid
    graphic gammoid
    regular gammoid
    no U_{2,4} or M(K_4) minor.

Since binary matroids already exclude U_{2,4}, a binary gammoid has no M(K_4) minor and has a graphic realization.

Therefore a binary support transversal matroid M_S has a graph H_S such that

    M_S ~= M(H_S)

and H_S may be chosen K_4-minor-free, i.e. series-parallel in the standard graphic-matroid sense.

An independent source theorem of de Sousa and Welsh states that every binary transversal matroid is graphic. Ingleton-Piff duality also identifies strict gammoids as precisely the duals of transversal matroids.

### Consequence for Dean augmentation

Circuits of M(H_S) are exactly graph cycles of H_S.

Hence:

    +1 Dean augmentation
    iff
    H_S contains a cycle C whose candidate edges are pairwise compatible
    in the original candidate-conflict graph.

The binary support side is therefore frozen as a series-parallel cycle carrier. Remaining hardness may live entirely in the coupling to candidate conflicts.

This is a carrier translation, not evidence that arbitrary conflict constraints are easy.

## 13. Log-conflict-cover extension

Let:

    H = series-parallel support graph whose cycle matroid is M_S
    Q = candidate-conflict graph on E(H)

A cycle of H is a valid +1 augmentation circuit exactly when its edge set is an independent set of Q.

Let Z be a vertex cover of Q of size k. Here vertices of Q are candidate edges of H.

Because Z covers every conflict edge,

    Q - Z

has no edges.

So all nontrivial conflict choices are concentrated in Z.

### Exact algorithm

Enumerate every independent subset A of Q[Z].

Interpret:

    A     = conflict-cover candidates included in the desired cycle
    Z-A   = conflict-cover candidates excluded from the desired cycle.

For each A:

1. Delete from H every edge represented by Z-A.
2. Delete from H every edge outside Z that conflicts in Q with some edge of A.
3. Retain all edges in A as required edges.
4. Decide whether the resulting series-parallel graph contains a simple cycle containing every edge of A.
5. If yes, return that cycle and map it Homeward through the support-transversal circuit to the exact +1 Dean augmentation.

Correctness:

- A is independent inside Q[Z].
- Q-Z has no edges.
- every outside neighbor conflicting with A was removed.
- no edge of Z-A may enter the cycle.

Therefore every returned cycle is Q-independent.

Conversely, let C be any Q-independent cycle and set

    A = C intersect Z.

The enumeration reaches A. No edge of C is deleted in that branch, and the marked-cycle test accepts C.

Thus the procedure finds a compatible support cycle iff one exists.

### Marked-cycle subproblem

The support graph H is series-parallel and therefore has treewidth at most two (after the standard simple/partial-2-tree interpretation of its biconnected blocks).

The property

    there exists a simple cycle containing every marked edge

has a constant-boundary dynamic program on a series-parallel decomposition. Equivalently, it is a fixed finite-state connectivity problem on treewidth two.

Hence each marked-cycle query is polynomial-time (indeed linear-time with a fixed SP decomposition and finite state table).

### Cost

There are at most

    2^k

branches and polynomial work in each branch.

Therefore:

    k = O(log n)

implies polynomial total work.

This gives another exact one-degree carrier:

    conflict vertex-cover size k
        -> enumerate signed hub choices
        -> series-parallel marked-cycle DP
        -> +1 augmentation or exact no-compatible-cycle certificate.

The original candidate-conflict graph remains authoritative. Z is a carrier/interface set, not semantic deletion.

### Relation to known forbidden-pair complexity

Arbitrary forbidden-pair constraints can make path/cycle routing hard even when the host graph is structurally simple. The structural parameter must therefore control the coupling relation Q, not only H.

Published PAFP work likewise finds fixed-parameter tractability when parameterizing the forbidden-pair graph by structural measures such as its vertex-cover number, while host-graph width alone need not remove hardness.

## 14. One-degree interpretation of the conflict-cover carrier

Choose one z in Z.

The two signed moves are:

    +z : require z in the candidate cycle
    -z : forbid z from the candidate cycle.

The repair is local:

    +z removes only conflict neighbors of z
    -z removes only z.

No support relation is rewritten.

After k signed decisions, the remaining conflict graph is empty and the residual problem is a pure series-parallel cycle query.

For k=O(log n), carrying both signs exactly remains polynomial.

This is a literal implementation of:

    one degree of change
    -> positive / negative family
    -> smallest exact repair
    -> Homeward reconstruction.


## 15. Operational support-carrier recognition from Dean data

The earlier binary-support carrier does not need to assume that an exact GF(2) representation is supplied externally.

Let P_S be the original Dean candidate-to-current-cohort bipartite support graph and let M_S be its transversal matroid on the candidate side.

### Polynomial independence oracle

For any candidate subset X,

    X is independent in M_S

iff P_S has a matching that covers X.

Therefore an independence/rank query to M_S is computable in polynomial time by bipartite matching.

### Seymour graphic-recognition step

Paul Seymour proved that an arbitrary matroid presented by an independence oracle can be tested for graphicness with polynomially many oracle calls, even though binary representability itself cannot be tested with polynomially many independence-oracle queries.

The constructive graphic-recognition procedure also yields a realizing graph H whenever the input matroid is graphic.

Hence, using only the original Dean support relation:

    support bipartite graph
        -> matching independence oracle
        -> Seymour graphic recognition
        -> either GRAPHIC(H) or NOT_GRAPHIC.

No generic transversal-matroid linear representation needs to be constructed.

### Why an accepted support carrier is series-parallel

M_S is transversal by construction, hence it is a gammoid.

If Seymour's recognizer accepts M_S as graphic, then M_S is binary because every graphic matroid is binary.

Thus M_S is a binary gammoid.

A standard binary-gammoid characterization gives the equivalences:

    binary gammoid
    <=> graphic gammoid
    <=> regular gammoid
    <=> no U_{2,4} or M(K_4) minor.

Therefore an accepted graphic M_S has no M(K_4) minor.

Its realizing graph H may consequently be taken as a K_4-minor-free / series-parallel support graph (componentwise, with the usual matroid series/parallel interpretation).

So the exact executable route is:

    Dean support relation
        -> matching oracle
        -> graphic recognizer
        -> series-parallel graph carrier
        -> compatible-cycle search.

### Rejection semantics

If graphic recognition rejects M_S, do not infer a false NO for the Dean obligation.

Because M_S remains a transversal matroid / gammoid, rejection only means that this particular series-parallel support carrier is not admissible.

Moreover, a non-graphic gammoid cannot be binary under the binary-gammoid characterization. Therefore the rejected support matroid is nonbinary and, by Tutte's theorem, contains a U_{2,4} minor.

This U_{2,4} statement is a structural remainder, not yet a polynomially located repair coordinate: binary recognition / U_{2,4}-minor detection is not polynomial in the general independence-oracle model.

Accordingly:

    GRAPHIC
        -> admit series-parallel support carrier

    NOT_GRAPHIC
        -> preserve NONBINARY_SUPPORT remainder
        -> do not fabricate a U_{2,4} witness unless independently constructed.

This closes representation-selection cost on the accepted branch while preserving the exact unresolved negative branch.

### Cost contract

If the Dean instance has polynomial encoding length N:

- each independence query is a polynomial bipartite-matching computation;
- Seymour graphic recognition uses polynomially many oracle queries and polynomial auxiliary work;
- the realizing support graph is polynomial-size;
- subsequent series-parallel recognition/decomposition is polynomial;
- no uncharged generic transversal representation is invoked.

Therefore the support-carrier recognition/construction lifecycle is polynomial on the admitted branch.


## 16. General log-conflict-cover theorem — binary/graphic support no longer required

The earlier log-conflict-cover carrier can be strengthened substantially.

Let:

    M = arbitrary support transversal matroid on candidate ground set R
    Q = candidate-conflict graph on R
    Z = a vertex cover of Q, |Z| = k.

No binary, graphic, gammoid-representation, or series-parallel hypothesis is required beyond the fact that M is the transversal matroid already defined by the Dean support bipartite graph.

Because Z is a vertex cover,

    Q - Z

has no edges.

Thus every pair of candidates outside Z is mutually compatible.

### Exact algorithm

Enumerate every Q-independent subset A of Z.

#### Case 1 — A is dependent in M

A contains a matroid circuit.

Since A is Q-independent, that circuit is conflict-free.

Return POSITIVE and reconstruct the exact +1 Dean augmentation.

#### Case 2 — A is independent in M

Delete from R-Z every candidate that conflicts in Q with any member of A.

Call the surviving outside set Y_A.

Because Q-Z has no edges, Y_A is internally conflict-free, and by construction there are no Q-edges between A and Y_A.

Now consider the contraction M/A restricted to Y_A.

Compute

    r_A = rank_M(A)
    r_full = rank_M(A union Y_A).

Then:

    rank_{M/A}(Y_A) = r_full - r_A.

If

    r_full - r_A < |Y_A|,

then Y_A is dependent in M/A.

Extract any circuit C' of (M/A)|Y_A.

The set A union C' is dependent in M and is conflict-free in Q, so it contains a conflict-free circuit C of M.

Return POSITIVE.

If instead

    r_full - r_A = |Y_A|,

then Y_A is independent in M/A, so no subset of Y_A can complete A to a dependent set.

Mark this A-branch NEGATIVE.

### Completeness proof

Suppose there exists a conflict-free circuit C of M.

Let

    A = C intersect Z
    Y = C - Z.

The enumeration reaches A because C is conflict-free.

If Y is empty, then A=C is dependent and Case 1 returns POSITIVE.

Otherwise A is a proper subset of the circuit C, hence A is independent.

Since C is conflict-free:

- Y is contained in R-Z;
- no element of Y conflicts with any member of A;
- therefore Y subseteq Y_A.

Because C is a circuit,

    rank_M(C) = |C|-1.

Since A is independent,

    rank_M(A) = |A|.

Hence in the contraction:

    rank_{M/A}(Y)
      = rank_M(A union Y) - rank_M(A)
      = (|A|+|Y|-1) - |A|
      = |Y|-1.

So Y is dependent in M/A.

Therefore Y_A is dependent in M/A as well, and Case 2 returns POSITIVE.

Conversely, every POSITIVE branch explicitly produces a Q-independent dependent set and therefore a Q-independent circuit of M.

Thus:

    conflict-free support-matroid circuit exists
    iff
    the algorithm returns POSITIVE.

By the support-transversal augmentation lemma, this is equivalent to existence of an exact +1 Dean augmentation.

### Dean implementation cost

M is a transversal matroid represented by the original candidate-to-current-cohort support bipartite graph.

For any X subseteq R:

    rank_M(X)

is the size of a maximum matching from X into S.

So every rank/independence query is polynomial-time.

Contraction rank is computed without constructing a separate representation:

    rank_{M/A}(Y)
      = rank_M(A union Y) - rank_M(A).

Circuit extraction from a dependent set uses polynomially many matching/rank queries by deleting elements while dependence remains.

The algorithm has at most:

    2^k

branches, each with polynomial matching work.

Therefore:

    k = O(log n)

implies polynomial total time.

This theorem strictly strengthens the earlier series-parallel log-conflict-cover carrier: graphicness is unnecessary for correctness in this parameter regime.

The series-parallel realization remains useful as an alternate exact carrier, visualization, and decomposition surface when Seymour graphic recognition accepts.

### One-degree interpretation

Each z in Z is one signed conflict degree:

    +z : include z and delete only its conflict neighbors
    -z : exclude z.

After all k degrees are resolved, the remaining candidate family is conflict-free.

The support side is never approximated: dependence is decided exactly by matching rank.

### Bounded differential validation

A separate exact checker generated 20,000 random small instances with:

- up to 8 candidates;
- up to 5 current-support vertices;
- designated conflict vertex cover size at most 3;
- arbitrary support bipartite edges;
- arbitrary conflict edges incident to the designated cover.

The theorem carrier was compared to exhaustive enumeration of every conflict-free candidate subset and exact matching-rank dependence.

Results:

    tested instances: 20,000
    mismatches: 0

This bounded panel supports the implementation logic only; the proof above is the mathematical basis.

### Updated remainder

The conflict-cover theorem removes support-representation complexity entirely when the coupling graph has logarithmic vertex cover.

The live universal residual is therefore concentrated in conflict graphs whose minimum useful coupling interface is superlogarithmic, together with other independently certified carrier families that may reduce that residual before enumeration.


## 17. One-degree U2,4 obstruction extraction on the non-graphic support branch

The NONBINARY_SUPPORT remainder from Section 15 can be made constructive without invoking a generic binary-matroid oracle.

Let M be the Dean support transversal matroid.

M is a gammoid. The class of gammoids is closed under minors.

For gammoids, the classical binary-gammoid theorem gives:

    binary
    iff
    graphic.

Therefore graphic recognition can be used as a binary test on every minor encountered below, even though binary recognition is not polynomial for arbitrary oracle-given matroids.

### Minor oracle from the original Dean support relation

Maintain two disjoint sets:

    C = elements contracted so far
    D = elements deleted so far.

The active minor is

    N = M / C \ D.

For any active set X,

    rank_N(X)
      = rank_M(X union C) - rank_M(C).

The ranks on the right are computed exactly by maximum matching in the original candidate-to-current-cohort support bipartite graph.

Thus every active minor has a polynomial-time rank/independence oracle without constructing a new transversal presentation.

### One-degree descent

Assume Seymour graphic recognition rejects N.

Because N is still a gammoid, N is nonbinary.

For each active element e, test the two one-degree minors:

    N \ e
    N / e.

Each is a gammoid and therefore:

    non-graphic
    iff
    nonbinary.

If either one is non-graphic, replace N by that one-element minor and append the exact operation to the Homeward trace:

    -e = delete e
    +e = contract e.

Only one element / one degree changes in a step.

Repeat.

### Termination and identification

The active ground set strictly decreases at every accepted step, so there are at most |E(M)| steps.

If no one-element deletion or contraction preserves non-graphicness, N is minor-minimal nonbinary.

Tutte's excluded-minor characterization of binary matroids states:

    matroid is binary
    iff
    it has no U_{2,4} minor.

Therefore the unique minor-minimal nonbinary matroid is U_{2,4}.

Hence the descent terminates with an explicit minor:

    N ~= U_{2,4}.

Its four surviving elements, together with the ordered contraction/deletion trace, form a recoverable NONBINARY_SUPPORT obstruction certificate.

### Cost

At most O(n) descent rounds are needed.

A straightforward implementation may test O(n) candidate one-element minors per round.

Each test runs Seymour's polynomial graphic-recognition procedure on a minor whose independence/rank oracle is implemented by polynomially many maximum-matching computations in the original support graph.

Therefore the complete obstruction extraction is polynomial-time.

### Why this does not contradict oracle lower bounds

Generic binary recognition from an independence oracle is not polynomially query-bounded.

This procedure uses additional certified structure:

    every active matroid is a gammoid.

Within gammoids:

    binary <=> graphic,

and graphicness *is* polynomially recognizable from an independence oracle.

The structure is doing the work.

### Signed one-degree interpretation

The support carrier now has an exact dichotomy:

    GRAPHIC
      -> construct series-parallel support carrier

    NOT_GRAPHIC
      -> one-element minor descent
      -> explicit U_{2,4} obstruction + Homeward trace.

No abstract NONBINARY_SUPPORT label needs to remain source-less.

The next repair obligation is not to erase U_{2,4}; it is to determine the smallest lawful carrier transformation that uses this four-element obstruction while preserving the original Dean augmentation obligation.


## 18. Coupling-graph calibration — exact but not a new carrier

The attempted "Dean coupling graph" construction collapses exactly back to the original graph and must not be counted as a new representation-level advance.

Let S be the current independent cohort and R=V(G)\S.

The proposed coupling graph J_S had:

1. candidate-candidate edges equal to E(G[R]);
2. candidate-support edges equal to the original G-edges between R and S;
3. no support-support edges.

But S is independent, so G[S] has no edges.

Therefore:

    J_S = G

as an ordinary graph on V(G).

There is an accompanying exact identity for the augmentation objective.

For conflict-stable B subseteq R define:

    delta_S(B) = |B| - |N_G(B) intersect S|.

Then:

    max_B delta_S(B) = alpha(G) - |S|.

Proof, first direction:

For any admissible B,

    I_B = (S \ N(B)) union B

is independent, with

    |I_B| = |S| + delta_S(B).

Therefore

    delta_S(B) <= alpha(G)-|S|.

Proof, reverse direction:

Let T be a maximum independent set and put B=T\S.

B is conflict-stable.

Every retained vertex T intersect S has no neighbor in B, hence

    T intersect S subseteq S \ N(B).

Therefore

    alpha(G)=|T|
            <= |B| + |S\N(B)|
            = |S| + delta_S(B).

Combining both inequalities gives equality.

### Consequence

Dynamic programming on treewidth(J_S) is simply dynamic programming on treewidth(G).

So the statement

    treewidth(J_S)=O(log n) gives a polynomial exact augmentation solver

is correct but is only the standard bounded-treewidth tractable island for Independent Set.

It must not be presented as a new universal coupling compression.

This is an anti-decay correction:

    RENAMED ORIGINAL PROBLEM != NEW PROGRESS.

### What survives

The earlier **log-conflict-cover theorem does survive** and is genuinely different.

There the parameter is the vertex-cover size of only the candidate-candidate conflict graph Q=G[R], while arbitrary support edges from R into S are handled by transversal-matroid rank / matching.

That carrier can therefore be small even when the full original graph G has large treewidth.

Likewise the binary/gammoid/series-parallel support carrier remains a genuine alternate representation of the support relation alone.

The universal remainder returns to the interaction between:

    structured support carrier
    +
    residual candidate-conflict relation,

without materializing their full union as a supposedly new object.

## 19. Updated remainder after coupling calibration

Do not pursue full-union width as a universal progress measure.

Continue one degree at a time on the separated carriers:

- support relation: matching / transversal / gammoid / graphic-series-parallel / U_{2,4} obstruction;
- candidate-conflict relation: exact structural interfaces such as logarithmic vertex cover or other certified decompositions;
- signed interaction: only through explicitly costed joins that do not recreate the whole original graph without compression.

The next valid move must reduce one of these separated carriers or provide an exact signed result; recombining them losslessly into G is a calibration identity, not a reduction.


## 12. Support-transversal to binary-gammoid series-parallel recognition

This section removes the earlier requirement that an exact GF(2) representation be supplied externally.

Let B=(R,S,E_B) be the current candidate-to-cohort support bipartite graph. Its transversal matroid M_S has ground set R and rank function

    r_M(X) = maximum matching size from X into S.

Hence every rank query is polynomial-time computable by bipartite matching.

Every transversal matroid is a gammoid. Classical work of Brylawski shows that binary gammoids are exactly the graphic matroids of series-parallel networks. Equivalently, for the support matroid:

    M_S is binary
    iff
    M_S is a series-parallel / quasi-series-parallel graphic matroid
    (componentwise, allowing loops/coloops/direct sums as appropriate).

This gives a direct recognition route from the original Dean support relation.

### Rank oracle for every residual minor

Maintain contracted and deleted sets C,D.

For any active subset X disjoint from C union D:

    r_(M/C\D)(X)
      = r_M(X union C) - r_M(C).

So even though transversal matroids are not closed under contraction, every rank query in every residual minor is still answered using the original support matching oracle.

### One-degree reductions

On the current active ground set A, repeatedly apply exactly one certified reduction:

#### Loop

    r({e}) = 0

Delete e.

In the Dean interpretation this means the candidate has no support capacity in the current residual matching carrier.

#### Coloop

    r(A) - r(A\{e}) = 1

Remove e as a direct rank-one bridge component and retain its reconstruction relation.

#### Parallel pair

For nonloops e,f:

    r({e,f}) = 1.

Delete one representative and record a parallel-extension edge.

#### Series pair

A pair e,f is a 2-element cocircuit exactly when

    r(A\{e,f}) = r(A)-1
    r(A\{e})   = r(A)
    r(A\{f})   = r(A).

Contract one representative and record a series-extension edge.

Each test uses only polynomially many matching-rank queries.

### Recognition theorem

A quasi-series-parallel matroid reduces completely by repeated loop/coloop/series/parallel reductions.

Conversely, reversing a successful reduction sequence constructs a series-parallel graphic realization:

- parallel reduction reverses to adding a parallel edge;
- series reduction reverses to subdividing an edge;
- coloop reverses to a bridge component;
- loop reverses to a graph loop;
- direct components remain direct components.

Therefore the above procedure is a polynomial exact recognizer for the support matroid's binary-gammoid island and simultaneously yields a constructive series-parallel graphic carrier.

### Consequence for augmentation

Inside this island:

    support-matroid circuits
    =
    simple cycles of the reconstructed series-parallel graph.

So the +1 Dean augmentation problem becomes:

    find a simple support-cycle whose ground elements
    are independent in the candidate-conflict graph.

The previously proved binary-cluster and log-cluster-defect carriers apply directly to this graphic realization.

### Exact residual when recognition fails

Because M_S is already a gammoid, failure to lie in the binary-gammoid class means the support matroid is nonbinary. The minimal representability obstruction is therefore a U_{2,4} minor.

Semantically, U_{2,4} is a rank-two four-candidate residual in which:

    every pair is support-matchable,
    every triple is support-dependent.

This becomes the next independent one-degree repair target.

The recognition failure is not promoted to a hardness claim and does not alter the original Dean graph. It creates one typed residual:

    NONBINARY_SUPPORT_U24

with the contraction/deletion provenance needed to reconstruct the four original candidate objects.

## 13. Immediate next degree

The smallest exact carrier change for U_{2,4} is field enlargement:

    GF(2) -> GF(3)

because U_{2,4} is not binary but is representable over GF(3), for example by the four projective columns

    (1,0), (0,1), (1,1), (1,-1).

This repairs the local representation obstruction only.

It does not yet establish that the binary rainbow-circuit algorithm extends to ternary support. That extension is the next proof obligation and must be treated as a new degree rather than silently inheriting the GF(2) theorem.


## 14. Field-lift and strong-base-orderability saturation

Two natural one-degree continuations were checked and are retained as bounded negative knowledge.

### 14.1 GF(2) -> GF(3) repairs representation, not signed progress

The nonbinary obstruction U_{2,4} is representable over GF(3), so the local representability defect can be repaired by changing one carrier degree:

    GF(2) -> GF(3).

However, the binary signed theorem does not transfer unchanged.

Bérczi-Schwarcz characterize binary matroids by the structure of their rank-preserving rainbow-circuit-free colorings. U_{2,4} is their canonical nonbinary example: it has rank 2, every circuit has size 3, and a two-coloring with two elements in each color is rainbow-circuit-free but has no monochromatic cocircuit.

Therefore:

    FIELD REPRESENTATION REPAIRED
    !=
    SIGNED RAINBOW PROGRESS REPAIRED.

The GF(3) carrier is retained as a valid representation option, but it is not admitted as a universal successor to the binary augmentation theorem.

### 14.2 Strong base orderability is already present everywhere on the support side

Every transversal matroid is strongly base orderable, and every gammoid is strongly base orderable.

Therefore the Dean support matroid M_S already has the strongest standard subset-wise base exchange property before any binary restriction is imposed.

This means the unresolved difficulty cannot be attributed to a lack of legal base exchanges.

The remaining obstruction is the coupling:

    support-matroid legal exchange
    AND
    candidate-conflict independence.

A one-exchange or strong-base-ordering map may be useful for navigation, but no monotone conflict-decrease theorem follows from strong base orderability alone.

Status:

    FIELD-LIFT-ONLY = SATURATED AS UNIVERSAL REPAIR
    STRONG-BASE-ORDERABILITY = SATURATED AS UNIVERSAL REPAIR

The live proof surface returns to:

    series-parallel graphic support
    x
    candidate-conflict overlay.

## 15. Graphic restatement of the live positive problem

When M_S is binary, the recognition theorem constructs a series-parallel graph H whose cycle matroid is M_S.

Then:

    +1 Dean augmentation
    iff
    H contains a simple cycle C
    such that C is an independent set of the candidate-conflict graph.

Equivalently, the binary support side is no longer abstract matroid search. It is a cycle-selection problem in a series-parallel graph with external forbidden/conflict pairs among the cycle edges.

General path/cycle selection with forbidden pairs is known to retain hardness under severe restrictions, while structured forbidden-pair families admit polynomial algorithms. Therefore the next admissible degree is the **structure of the conflict overlay relative to the series-parallel decomposition**, not further weakening of the already-solved support representation.


## 20. Hierarchical conflict-overlay carrier on series-parallel support

This section advances the live graphic remainder:

    series-parallel support cycle
    x
    candidate-conflict overlay.

The support graph H is the exact series-parallel graphic realization of the binary Dean support matroid. Its edges are candidate elements. A support-matroid circuit is therefore a simple cycle of H.

The candidate-conflict graph Q has the same edge-elements as vertices: a conflict pair {f,g} means a valid augmentation circuit may not contain both support edges f and g.

### 20.1 Cycle anchoring

Every simple cycle lies in one biconnected block of H.

Loops are handled earlier as one-element circuits. Parallel two-edge circuits can be checked directly. Consider a simple biconnected series-parallel block B with at least three edges.

Fix an edge

    e = st.

Eppstein's series-parallel decomposition theorem states that a biconnected series-parallel graph can be treated as a two-terminal series-parallel graph with the endpoints of any chosen edge as terminals.

Because e itself joins the two terminals directly, the TTSP decomposition can expose e as one parallel branch. Therefore

    B = P(e, N_e)

for a two-terminal series-parallel network N_e with terminals s,t.

Hence

    B - e = N_e.

Orient N_e recursively from s to t. The result is a DAG. By induction on the TTSP construction, every simple undirected s-t path in N_e is directed in this orientation.

Therefore:

    simple cycle C of B containing e
    iff
    directed simple s-t path P = C-e in N_e.

### 20.2 Carry conflicts exactly into the path instance

A conflict-free cycle containing e cannot contain any support edge f with

    {e,f} in E(Q).

Delete those f from N_e.

For every remaining support edge f, subdivide f once and call its new marker vertex x_f.

For every remaining candidate-conflict pair

    {f,g} in E(Q),

create the forbidden marker pair

    {x_f,x_g}.

A directed s-t path in the subdivided DAG is safe exactly when it contains at most one marker from every forbidden pair.

Thus:

    conflict-free support cycle containing e
    iff
    safe directed s-t path in the transformed branch D_e.

This is an exact carrier translation with a direct Homeward map from marker vertices to original candidate/support edges.

### 20.3 Remove semantically irrelevant forbidden pairs

Let a < b mean that marker b is reachable from marker a in D_e.

If the two markers of a forbidden pair are incomparable under reachability, they cannot both lie on one directed path.

Such a pair is irrelevant to the branch and can be removed without weakening the original cycle obligation.

Orient every remaining forbidden pair as

    (a,b) with a < b.

### 20.4 Hierarchical overlay theorem

For two oriented forbidden pairs

    p=(a,b)
    q=(c,d),

call them crossing / halving when their endpoints interlace:

    a < c < b < d

or symmetrically

    c < a < d < b.

The active forbidden-pair family is hierarchical exactly when no such crossing pair exists.

Kolman and Pangrac proved that Path Avoiding Forbidden Pairs on a DAG is polynomial-time solvable when the forbidden pairs have this hierarchical structure. Their reduction repeatedly:

1. contracts a vertex that is in no remaining forbidden pair while retaining a path label;
2. removes an edge joining the endpoints of a forbidden pair;
3. removes a forbidden pair whose endpoints are no longer reachable.

The reductions preserve a Homeward path witness.

Consequently, if the transformed branch D_e is hierarchical, the existence or nonexistence of a conflict-free support cycle through e is decidable in polynomial time.

### 20.5 Global exact binary-support carrier

Choose an arbitrary spanning forest T of H.

Every nonempty support cycle contains at least one non-tree edge.

Therefore it suffices to use as anchors

    A = E(H) \ E(T).

For each e in A, build and solve D_e.

If any branch returns a safe path, reconstruct its support cycle and the corresponding exact +1 Dean augmentation.

If every anchor branch is hierarchical and every one returns NO, then H contains no candidate-conflict-free circuit. Therefore the current Dean cohort is maximum.

This defines a new exact polynomial terminal island:

    BINARY_GAMMOID_SERIES_PARALLEL_SUPPORT
    +
    EDGEWISE_HIERARCHICAL_CONFLICT_OVERLAY.

This island is different from the earlier log-conflict-vertex-cover carrier: the candidate-conflict graph may contain many conflicts, provided their positions along every required anchor branch are hierarchically nested rather than crossing.

## 21. Log crossing-defect extension

The hierarchical theorem gives a natural one-degree defect measure.

For one anchor branch e, construct the crossing graph X_e:

- one vertex for every active comparable forbidden pair in D_e;
- two vertices are adjacent exactly when the corresponding forbidden pairs interlace.

Then:

    X_e has no edges
    iff
    the branch is hierarchical.

A set P of forbidden-pair vertices whose deletion makes X_e edgeless is exactly a vertex cover of X_e.

### 21.1 Preserve, do not discard, the removed pair obligations

A vertex cover P is only a carrier modulator. Its forbidden pairs remain authoritative.

For each selected forbidden pair

    p={x,y} in P,

the safe-path obligation says at least one of x,y must be absent.

Create exactly two signed repairs:

    -x : forbid x in this branch
    -y : forbid y in this branch.

Enumerate the 2^|P| signed endpoint choices.

After deleting the chosen marker vertices:

- every modulator pair in P is satisfied explicitly;
- the remaining forbidden pairs F-P were non-crossing before the deletions;
- deletion can remove reachability but cannot create a new interlacing reachability chain.

After pruning newly incomparable pairs, the residual instance is hierarchical and is solved by the polynomial PAFP carrier.

### 21.2 Completeness

Suppose a safe s-t path exists in the original anchor branch.

For every modulator pair p in P, the safe path omits at least one endpoint.

Choose an omitted endpoint as that pair's signed deletion.

The enumeration includes this choice, so one branch preserves the safe path.

Conversely, every branch deletes one endpoint of every modulator pair and then solves all remaining forbidden pairs exactly. Any returned path is therefore safe for the original branch.

Hence the signed modulator enumeration is exact.

### 21.3 Finding the modulator without hiding optimization

Do not assume a minimum crossing repair is available.

Run the standard parameterized Vertex Cover decision/search procedure on X_e with a declared cap

    k_e <= c log n

for fixed constant c.

If no such vertex cover is found, return this anchor branch as UNRESOLVED under this carrier.

If such P is found, total branch work is

    2^k_e poly(n).

The vertex-cover search itself is also 2^O(k_e) poly(n).

Thus for

    k_e = O(log n)

the complete anchor cost remains polynomial.

If every non-tree anchor e satisfies the declared logarithmic crossing-defect guard, the entire cycle/augmentation decision is polynomial.

### 21.4 One-degree semantics

Each crossing-modulator pair is one repair degree.

The two signs are not "truth values" for the pair; they are the two lawful ways to satisfy its at-most-one obligation:

    LEFT  -> exclude first endpoint
    RIGHT -> exclude second endpoint.

No other support or conflict degree changes.

### 21.5 Bounded differential validation

Two bounded checks were run separately from the proof.

1. The direct Kolman-Pangrac hierarchical reduction was compared against brute-force safe-path enumeration on 2,956 random small TTSP DAG instances whose active forbidden pairs were hierarchical.

       mismatches: 0
       stuck reductions: 0

2. The crossing-graph vertex-cover extension was compared against brute-force safe-path enumeration on 10,000 random small TTSP instances with arbitrary marker conflicts and a declared crossing-cover cap k<=2.

       instances decided by the guard: 9,995
       mismatches: 0
       stuck reductions: 0

These finite panels are implementation evidence only.

### 21.6 Updated live residual

Inside binary-gammoid / series-parallel support, arbitrary conflict count is no longer the correct obstruction.

The exact residual is now the **crossing structure** of the conflict pairs relative to the anchor TTSP order.

The carrier closes:

    crossing defect 0
    -> polynomial hierarchical solve

and

    crossing vertex-cover O(log n)
    -> polynomial signed repair + hierarchical solve.

The next one-degree conflict-side target is therefore a branch whose crossing graph has superlogarithmic vertex cover. It should be changed or summarized directly; already hierarchical/nested conflicts should not be touched.


## 22. Choice-CNF compilation of a TTSP conflict overlay

The hierarchical-path carrier is not the only exact way to use the series-parallel support decomposition.

For one anchored branch, let N be the oriented two-terminal series-parallel DAG after:

- removing the anchor edge e;
- deleting every support edge that conflicts with e.

Fix a binary TTSP decomposition tree for N.

### 22.1 Parallel nodes are Boolean decision fields

For every parallel-composition node p introduce one Boolean variable:

    x_p = 0  -> choose the left child
    x_p = 1  -> choose the right child.

Series nodes introduce no variable because an s-t path traverses both series children.

A total assignment to all parallel-node variables determines an s-t path recursively:

- at a leaf, use its support edge;
- at a series node, concatenate the two recursively chosen paths;
- at a parallel node, recurse only into the selected child.

Values assigned inside an unselected parallel subtree are semantically irrelevant to the resulting path but are harmless.

### 22.2 Exact edge signatures

For each support edge f, define its path signature sigma_f as the partial assignment containing, for every parallel ancestor p of f, the branch value that selects the child containing f.

Then:

    f lies on the path determined by assignment a
    iff
    a extends sigma_f.

This is proved directly by induction on the TTSP decomposition.

### 22.3 One candidate conflict becomes one CNF clause

Take a candidate-conflict pair {f,g}.

If sigma_f and sigma_g disagree on any common parallel ancestor, f and g can never occur on the same s-t path. The conflict is branch-irrelevant and creates no clause.

Otherwise merge the compatible signatures:

    sigma_fg = sigma_f union sigma_g.

The two support edges occur together exactly when every required decision in sigma_fg is satisfied.

Therefore the conflict is enforced by the single clause

    C_fg = OR over (p=b) in sigma_fg of [x_p != b].

Equivalently, C_fg is the negation of the conjunction specifying simultaneous reachability of f and g.

Let F_choice be the conjunction of all such clauses.

### 22.4 Exact equivalence theorem

For every full assignment a:

    a satisfies F_choice
    iff
    the TTSP path P(a) contains no candidate-conflict pair.

Proof:

If a violates C_fg, then it extends both edge signatures and the selected path contains f and g.

If the selected path contains a conflict pair f,g, then a extends both signatures and violates C_fg.

Hence:

    safe support path exists
    iff
    F_choice is satisfiable.

Combined with cycle anchoring:

    conflict-free support cycle through e
    iff
    ChoiceCNF(e) is satisfiable.

The compiler is polynomial in the decomposition size plus the number of conflict pairs.

The assignment-to-path and path-to-original-candidate maps provide Homeward reconstruction.

### 22.5 Existing exact SAT terminals transfer lawfully

This compiler does not make SAT easy by renaming it.

It does allow already certified tractable SAT structure to be reused without semantic loss.

Admit an anchor branch when ChoiceCNF(e) is recognized as any independently polynomial class, including:

- 2-CNF;
- Horn;
- dual-Horn;
- beta-acyclic CNF.

For beta-acyclic CNF, the clause hypergraph admits a polynomially computable weakly-simplicial variable elimination ordering. Davis-Putnam elimination along this ordering does not increase the number of clauses because each generated resolvent is contained in a parent clause.

This gives an exact one-degree execution law:

    choose one weakly-simplicial parallel variable
    -> eliminate it
    -> retain the reconstruction receipt
    -> continue.

At the end:

- SAT reconstructs the parallel choices and support path;
- UNSAT provides the corresponding resolution/elimination certificate.

### 22.6 Simple derived island: parallel depth one

If every support edge has at most one parallel ancestor in the TTSP decomposition, every edge signature contains at most one Boolean choice.

Every conflict clause then contains at most two choice variables.

Therefore:

    parallel-decision depth <= 1
    -> ChoiceCNF is 2-CNF
    -> exact polynomial branch.

This includes series compositions of independent binary parallel gadgets.

### 22.7 Bounded differential validation

A separate exact checker generated 3,481 random binary TTSP decomposition trees with random candidate-conflict pairs.

For each instance it compared:

    existence of a conflict-free recursively selected s-t path

against:

    satisfiability of the compiled ChoiceCNF.

Results:

    tested instances: 3,481
    mismatches: 0

This panel validates the compiler implementation only. The equivalence proof above is the mathematical basis.

### 22.8 Claim boundary

ChoiceCNF is an exact representation change, not a universal complexity collapse.

If the compiled formula falls outside all currently certified tractable SAT classes, the branch remains unresolved.

CHOICE_CNF_COMPILED != CHOICE_CNF_SOLVED.

## 23. Skew-symmetric forbidden-pair carrier

The hierarchical and ChoiceCNF carriers have an orthogonal exact neighbor from classical forbidden-pair path theory.

For an anchor branch D_e after edge-marker subdivision, suppose:

1. the active forbidden marker pairs are mutually disjoint;
2. each pair defines a mate involution v <-> v';
3. the branch satisfies Yinnone's skew-symmetry condition:

       arc (u,v) exists
       ->
       arc (v',u') exists

   for paired vertices u,u' and v,v'.

Yinnone proved that this Skew Forbidden Path problem is polynomially equivalent to finding an augmenting path with respect to a matching.

More importantly for the signed proof architecture, the same work defines a dual F-cut and proves:

    safe F-path exists
    iff
    no F-cut exists.

Therefore a recognized skew-symmetric anchor branch provides the exact two-direction contract:

    POSITIVE
      -> safe support path
      -> conflict-free support cycle
      -> +1 Dean augmentation

    NEGATIVE
      -> F-cut
      -> certificate that this anchor has no safe support path.

Recognition of the stated skew-symmetry and pair-disjointness conditions is polynomial by direct inspection.

This carrier may apply even when the forbidden pairs are not hierarchical.

### Updated conflict-overlay portfolio

For binary-gammoid / series-parallel support, an anchor branch is now certified by any of the following independent exact mechanisms:

    hierarchical forbidden-pair order
    log crossing-defect -> signed endpoint repair -> hierarchical order
    ChoiceCNF in a certified polynomial SAT class
    skew-symmetric disjoint forbidden pairs
    prior log conflict-vertex-cover transversal-matroid carrier

No evidence transfers between these domains merely because they solve the same branch.

A global NO is admitted only when every cycle anchor is closed by an exact negative certificate from some admitted carrier.


## 24. Forest-presentation circuit anatomy

The Dean support matroid is transversal. For the binary-transversal case there is a sharper structural theorem than the generic series-parallel realization.

Sali and Simonyi record the following theorem of Edmonds:

    A transversal matroid is binary
    iff
    it possesses a presentation by a bipartite forest.

They also record de Sousa-Welsh:

    A transversal matroid is binary
    iff
    it is graphic.

The de Sousa-Welsh result is published; the forest-presentation theorem is attributed by Sali-Simonyi to an unpublished result of Edmonds.

This section uses the forest presentation only as a mathematical carrier. The universal execution contract does not assume that an arbitrary such forest presentation is supplied for free.

### 24.1 Circuit theorem for a forest presentation

Let F=(L,R,E) be a bipartite forest presenting a transversal matroid M on left ground set L.

For nonempty C subseteq L, the following are equivalent:

1. C is a circuit of M.
2. The induced bipartite graph

       F[C union N(C)]

   is connected and every right/support vertex in N(C) has degree exactly 2 into C.

#### Proof: circuit -> forest shape

Because C is dependent, Hall gives

    |N(C)| <= |C|-1.

For any c in C, the proper subset C-c is independent, so Hall gives

    |N(C-c)| >= |C|-1.

But

    N(C-c) subseteq N(C).

Therefore

    |N(C)| = |C|-1

and, for every c,

    N(C-c) = N(C).

If F[C union N(C)] had more than one connected component, let C_i be the nonempty left vertices of a component. Every C_i would be a proper subset of C, hence Hall-independent:

    |N(C_i)| >= |C_i|.

Summing over components contradicts

    |N(C)| = |C|-1.

So the induced graph is connected. Since F is a forest, it is a tree.

The equality N(C-c)=N(C) for every c implies that no support vertex has degree one into C. Thus every support degree is at least 2.

A tree on |C|+|N(C)| vertices has

    |C|+|N(C)|-1
    = 2|N(C)|

edges, because |C|=|N(C)|+1.

The sum of support degrees is exactly this edge count. Since every support degree is at least 2, every support degree is exactly 2.

#### Proof: forest shape -> circuit

Assume F[C union N(C)] is connected and every support vertex has degree 2 into C.

It is a tree. Therefore

    2|N(C)|
    = |E|
    = |C|+|N(C)|-1,

so

    |C| = |N(C)|+1.

Hence C is dependent.

Now contract every support vertex r in N(C) to an ordinary edge joining its two C-neighbors. Because the bipartite graph is a tree, this produces an ordinary tree T on vertex set C.

For any nonempty proper X subset C, N_F(X) corresponds exactly to the edges of T incident with X.

If T[X] has k connected components, it has |X|-k internal edges; because X is proper and T is connected, every such component has at least one boundary edge. Hence T has at least

    (|X|-k)+k = |X|

edges incident with X.

Thus

    |N_F(X)| >= |X|

for every proper X. Hall's theorem makes every proper subset of C independent.

So C is a circuit.

### 24.2 Consequence

A circuit in a binary-transversal forest presentation is a closed support tree:

- selected candidates are the left vertices;
- each touched support is paired with exactly two selected candidates;
- contracting touched supports yields a tree on the candidate circuit.

This is substantially narrower than an arbitrary series-parallel cycle representation, although the two represent the same binary-transversal matroid at the matroid level.

## 25. Clause-star forest normal form for SAT

The forest circuit theorem reveals an exact hard-core calibration.

Let Phi be a CNF formula with nonempty clauses

    C_1, ..., C_m.

Create one left candidate rho, called the root.

For every literal occurrence l in clause C_j create one left occurrence candidate

    o_(j,l).

Create one right support vertex s_j for each clause.

Add support edges

    rho -- s_j

for every clause, and

    o_(j,l) -- s_j

for every literal occurrence.

The resulting presentation graph is a radius-two bipartite tree: root -> clause supports -> literal-occurrence leaves.

### 25.1 Candidate-conflict overlay

Keep rho conflict-free.

Add a candidate-conflict edge between:

1. every pair of distinct literal occurrences in the same clause; and
2. every pair of occurrences labelled by complementary literals x and not-x.

The same-clause conflicts are the minimal repair that prevents an unintended two-leaf circuit from being accepted as a satisfying witness.

### 25.2 Exact theorem

Phi is satisfiable if and only if the presented binary transversal matroid has a circuit that is independent in the candidate-conflict graph.

#### SAT -> conflict-free circuit

Take a satisfying truth assignment.

Choose exactly one true literal occurrence from every clause.

Let C contain rho and these m chosen occurrences.

Every support s_j has degree exactly two into C:

    rho
    +
    the chosen literal of C_j.

The induced support graph is connected. By the forest circuit theorem, C is a circuit.

It is conflict-free because:

- exactly one occurrence was chosen per clause;
- a single truth assignment cannot make both x and not-x true.

#### conflict-free circuit -> SAT

Let C be a conflict-free circuit.

C must contain rho.

Otherwise C lies wholly among literal leaves. By the forest circuit theorem, a connected circuit without rho can use only one clause support and exactly two of its occurrence leaves. Those two leaves conflict by construction.

Since rho belongs to C, every clause support s_j lies in N(C).

Every support has degree exactly two into C, so C contains exactly one literal occurrence from every clause.

Conflict-freedom guarantees that the selected occurrences never contain both polarities of the same variable.

Assign each selected positive literal's variable TRUE and each selected negative literal's variable FALSE; assign unused variables arbitrarily.

Every clause contains its selected true literal. Hence Phi is satisfiable.

### 25.3 Complexity consequence

Checking a proposed conflict-free circuit is polynomial.

Therefore conflict-free circuit existence is NP-complete even when the support transversal matroid is:

- binary;
- given directly by a forest presentation;
- presented by a radius-two tree with one central root.

This is a calibration of the coupling boundary, not evidence for P != NP.

It proves:

    BINARY_TRANSVERSAL_SUPPORT
    !=
    UNIVERSAL EASY AUGMENTATION.

The universal difficulty can survive entirely in consistency relations among candidate occurrences.

### 25.4 Bounded differential validation

A separate exhaustive/brute-force checker generated 1,500 random small CNF formulas over one to three variables and up to four clauses.

For each formula it compared:

    ordinary truth-table satisfiability

against

    existence of a conflict-free circuit in the clause-star forest construction.

Results:

    tested: 1,500
    mismatches: 0.

The finite panel validates the implementation of the reduction only. The proof above is the mathematical basis.

## 26. Four-ID compression of the clause-star hard core

The clause-star construction also shows why the four-ID catalog is useful even though it does not solve SAT by itself.

Each literal occurrence keeps its own OccurrenceID.

All occurrences of the same signed literal can share a SemanticObjectID, for example:

    LIT(x, TRUE)
    LIT(x, FALSE).

Clause membership is carried by SemanticContextSupportsIDs.

The complement relation

    COMPLEMENT(LIT(x,TRUE), LIT(x,FALSE))

is a SemanticClarity relation.

Thus the quadratic number of explicit occurrence-to-occurrence complement conflict edges need not be authoritative storage.

They can be reconstructed from:

    occurrence -> signed-literal object
    signed-literal -> complement object.

This compresses duplicated conflict representation while preserving exact semantics and Homeward provenance.

It does not reduce the logical problem:

    choose one supported literal object per clause
    without choosing both polarities of a variable.

That object is exactly CNF satisfiability in relational form.

REPRESENTATION COMPRESSION != COMPLEXITY COLLAPSE.

## 27. Independent-transversal and autarky directions

Dropping the artificial same-clause conflict clique and instead treating each clause's literal occurrences as one partition class gives the equivalent statement:

    Phi is satisfiable
    iff
    the complementary-literal conflict graph has
    an independent transversal choosing one occurrence per clause.

Graf-Haxell give polynomial algorithms under structural hypotheses that either find such an independent transversal or return a subset of classes with a small dominating set.

This is admitted as a one-degree structural carrier only under its stated hypotheses. A returned dominating set is structural information, not by itself an UNSAT certificate.

A second lawful reduction family is SAT autarky theory:

    partial assignment
    -> satisfies every clause it touches
    -> remove exactly those satisfied clauses
    -> untouched remainder is equisatisfiable.

Matching autarkies connect this reduction to Hall/matching structure and deficiency. Lean kernels preserve the exact unresolved remainder after all admitted autarky reductions.

The next proof obligation is not to rename arbitrary SAT as an autarky problem. It is to determine whether the clause-star hard core always yields, in polynomial total cost, one of:

    a satisfying independent transversal;
    an exact autarky reduction;
    an exact negative signed certificate;
    or a strictly smaller certified residual in another existing carrier.

No universal theorem is claimed yet.
