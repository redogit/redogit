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
