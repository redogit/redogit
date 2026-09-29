# Cubic 3-Uniform Residual Calibration — 2026-09-26

**Predecessor:** PNP_SEMANTIC_INTERSECTION_QUOTIENT_2026-09-26.md  
**Program:** RMAL / P vs NP  
**Status:** derived scoped residual + external theorem bindings + bounded counterprobes  
**Claim ceiling:** no universal P=NP proof; no NP-hardness claim for the cubic Property-B boundary

## 1. Paired-balance family

For a 3-uniform hypergraph H=(V,E), define the paired CNF

    F_H = AND_{e={a,b,c} in E}
          [(x_a OR x_b OR x_c)
           AND
           (not x_a OR not x_b OR not x_c)].

F_H is satisfiable exactly when H has Property B / a proper 2-coloring.

Each hyperedge contributes two opposite signed clause rows. Those two rows form a positive balance 2-circuit with unit coefficients.

This family is retained as a calibration carrier because its balance-circuit support overlap can be trivial while its Boolean obligation remains nontrivial.

## 2. Exact cubic boundary inside the bounded-degree paired carrier

Assume:

- H is connected;
- H is 3-uniform;
- maximum vertex degree Delta(H) <= 3;
- the paired signed clause matrix is in the current full-column-rank linearly-lean residual.

Let n=|V| and m=|E|.

Full column rank gives

    rank <= number of positive-edge rows = m

for the unsigned incidence submatrix, so in the full-rank paired construction the retained incidence rank requirement forces m >= n in the calibrated full-rank cases.

The degree bound gives

    3m = sum_v degree(v) <= 3n,

hence m <= n.

Therefore the exact surviving full-rank boundary is

    m=n

and equality in the degree sum forces

    degree(v)=3 for every v.

Thus the bounded-degree paired residual collapses to a connected cubic 3-uniform hypergraph.

This is a derived residual condition. It is not a proof that deciding Property B on that exact class is NP-complete.

## 3. External edge-deletion theorem

Henning and Yeo's theorem, as quoted in later peer-reviewed sources, gives:

    every connected 3-uniform hypergraph
    with maximum degree <=3 that is not 3-regular
    is 2-colorable.

Consequently every connected cubic 3-uniform hypergraph is either already 2-colorable or becomes 2-colorable after deleting any one hyperedge.

So a non-2-colorable cubic residual is edge-critical.

This is a genuine structural restriction.

## 4. FIRE — near-solution recoloring is not degree removal

Take any edge e and any valid 2-coloring c of H-e.

Introduce flip coordinates f_v and write the proposed final coloring as

    c'_v = c_v XOR f_v.

Every NAE constraint becomes

    NAE(c_a XOR f_a,
        c_b XOR f_b,
        c_c XOR f_c).

The map f -> c' is a bijection on Boolean assignments.

Therefore solving the flip system is exactly the original coloring obligation in translated coordinates.

    NEAR SOLUTION != REDUCED BOOLEAN DEGREE
    RECOLORING COORDINATES != POLYNOMIAL REPAIR THEOREM.

Bounded experiments also found valid H-e colorings whose nearest full valid coloring requires three coordinated flips.

Retain the edge-deletion theorem as geometry, but do not promote generic recoloring search.

## 5. FIRE — incidence girth is not the obstruction

The Fano paired residual has cubic bipartite incidence graph equal to the Heawood graph and incidence girth 6.

A bounded configuration-model search found a connected cubic 3-uniform 10-vertex instance with incidence girth 6 and 48 proper 2-colorings:

    (3,6,9)
    (2,4,6)
    (7,8,9)
    (2,5,9)
    (1,5,7)
    (0,3,8)
    (0,4,7)
    (1,3,4)
    (0,5,6)
    (1,2,8)

Therefore:

    NO INCIDENCE 4-CYCLE
    !=
    NON-2-COLORABLE.

Girth remains a structural coordinate, not a decision certificate.

## 6. Quasi-matching / perfect-matching modulo-3 certificate

A published sufficient condition states that a k-uniform hypergraph is 2-colorable when the number of quasi-matchings in its incidence graph is nonzero modulo k.

For the cubic 3-uniform case n=m, quasi-matchings are perfect matchings of the cubic bipartite incidence graph.

Hence the implication is

    #PM(G_I) mod 3 != 0
        ->
    H is 2-colorable
        ->
    F_H is SAT.

Finite calibration:

    Fano:
        #PM = 24 = 0 mod 3
        #2-colorings = 0

    full-rank SAT 7-vertex witness:
        #PM = 20 = 2 mod 3
        #2-colorings = 14

    SAT girth-6 10-vertex witness:
        #PM = 60 = 0 mod 3
        #2-colorings = 48.

So the condition is one-way and incomplete, as expected.

### Admission barrier

Do not treat #PM mod 3 as a generic polynomial recognizer.

Permanent modulo 2 collapses to determinant parity, but permanent modulo odd primes such as 3 does not receive that determinant shortcut and is computationally hard in general.

Therefore this certificate is admitted only when the incidence graph is already in a class where the required matching count is independently polynomial-time computable, such as appropriate planar/Pfaffian, bounded-genus, or bounded-treewidth carriers.

    THEOREM WITH EXPENSIVE PREMISE
    !=
    FREE POLYNOMIAL TERMINAL.

## 7. Updated incidence Object

The lawful cubic residual is now represented simultaneously as:

    cubic 3-uniform hypergraph H
    +
    cubic bipartite incidence graph G_I
    +
    paired positive balance 2-circuits
    +
    semantic intersection-state semilattice L(F_H)
    +
    edge-critical deletion witnesses when non-2-colorable.

The next move must exploit a relation among these carriers that is polynomially recognizable and actually removes information/search, rather than merely renaming a coloring.

## 8. Current remainder

Do not claim:

    CUBIC PROPERTY B = NP-COMPLETE

without an exact source establishing that restriction.

Do retain:

    GENERAL RANK-3 PROPERTY B IS NP-COMPLETE
    CUBIC RESIDUAL IS A DERIVED SUBCLASS
    NON-2-COLORABLE CUBIC RESIDUALS ARE EDGE-CRITICAL
    RECOLORING IS A BIJECTIVE COORDINATE CHANGE
    GIRTH>=6 DOES NOT DECIDE
    PM-MOD-3 IS ONLY A CONDITIONAL ONE-WAY TERMINAL.

The next exact target is:

    find a polynomially recognizable incidence/semantic relation
    that collapses one degree in the edge-critical cubic residual,

or produce a counterexample and preserve it as ASH.

GENERATE != VERIFY != ADMIT.
