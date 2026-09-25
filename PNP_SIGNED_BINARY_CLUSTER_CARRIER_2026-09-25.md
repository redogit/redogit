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
