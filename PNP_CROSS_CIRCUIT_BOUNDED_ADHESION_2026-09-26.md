# Cross-Circuit Bounded-Adhesion Terminal — 2026-09-26

**Program:** P vs NP / qualitative-centrality + positive-balance route  
**Predecessor:** `PNP_POSITIVE_CIRCUIT_LOCAL_DECISION_2026-09-26.md`  
**Status:** scoped exact polynomial terminal  
**Claim ceiling:** not universal P=NP

## 1. Setup

Let C_1,...,C_t be the selected positive balance-circuit clause supports covering the normalized residual F.

Duplicate clause membership across circuits is harmless because conjunction is idempotent.

For each circuit C_i let V_i be the variables occurring in its clauses.

Assume there is a tree T on the circuit Objects satisfying the running-intersection condition:

    for every variable x,
    { i : x in V_i } induces a connected subtree of T.

For circuit i define its boundary

    B_i = { x in V_i : x also occurs in V_j for some j adjacent to i in T }.

Assume

    |B_i| <= b

for all i.

This is a signed-incidence condition, not raw circuit-support overlap.

## 2. Local maximum-deficiency bound

Because C_i is a row-matroid circuit, every proper clause subset H subset C_i has linearly independent signed rows.

Hence

    |H| = rank(M_H) <= |Var(H)|

for every proper H.

For H=C_i,

    |C_i|-1 = rank(M_Ci) <= |V_i|.

Therefore the maximum deficiency of F_{C_i} is at most one:

    delta*(F_{C_i}) <= 1.

Now fix any assignment alpha to at most s variables.

Restriction can remove satisfied clauses and delete at most s variables from the remaining clause subsets. Therefore

    delta*(F_{C_i}|alpha) <= 1+s.

Szeider's maximum-deficiency SAT algorithm decides a CNF with maximum deficiency k in O(2^k n^3) time and returns either a satisfying assignment or a regular-resolution refutation.

Thus for s<=b, every boundary-conditioned local circuit is decidable in

    O(2^(b+1) poly(n)).

## 3. Tree compatibility algorithm

Root T arbitrarily.

For every circuit i and every assignment alpha to B_i:

1. decide whether the local circuit formula F_{C_i}|alpha is satisfiable;
2. combine alpha with already-computed child boundary tables;
3. retain alpha exactly when there exists a local satisfying extension compatible with every child message.

Because the running-intersection property makes every cross-subtree variable pass through the relevant boundary, standard tree/junction consistency is exact: no hidden variable relation crosses a cut outside the separator.

The root table is nonempty iff the conjunction of all circuit formulas is satisfiable, which is exactly F because the circuit supports cover every clause.

## 4. Cost

Each boundary table has at most 2^b rows.

There are at most t<=delta(F)<=m circuit Objects.

For each table row, local conditioned SAT is bounded by the maximum-deficiency algorithm with parameter at most b+1.

Hence total work is

    t * 2^b * O(2^(b+1) poly(n))
    =
    O(t * 4^b * poly(n)).

Therefore if

    b = O(log n)

with an explicit constant bound charged into the polynomial exponent, and a valid running-intersection tree is supplied or found in polynomial work, the residual is exactly decidable in polynomial total work.

Homeward reconstruction follows retained table witnesses plus the existing normalization trace.

## 5. What this terminal means

The surviving difficulty is not merely:

    CIRCUITS OVERLAP.

It is the inability to organize the **signed variable incidence among locally tractable circuits** through polynomial-size compatibility boundaries.

This terminal consumes a real portion of the synchronized remainder:

    LOCALLY SAT CIRCUITS
    +
    RUNNING-INTERSECTION CIRCUIT TREE
    +
    LOGARITHMIC SIGNED BOUNDARY
    ->
    POLYNOMIAL EXACT SAT/UNSAT.

## 6. Required recognizer

This is not admitted as a universal algorithm merely because a good tree may exist.

A terminal invocation must include a polynomially verifiable receipt for:

- the circuit list and source clause IDs;
- the tree T;
- the running-intersection condition for every variable;
- each boundary B_i;
- the declared logarithmic cap;
- all local maximum-deficiency calculations;
- message tables / witness or refutation receipts;
- Homeward reconstruction.

Discovery of an adequate tree is a separate charged obligation.

    EXISTENCE OF SMALL ADHESION
    !=
    POLYNOMIAL DISCOVERY

## 7. Remainder after this terminal

The active hard cell is now:

    all positive circuits locally SAT
    AND
    no admitted logarithmic-boundary running-intersection decomposition
    AND
    global sign-centrality still unresolved.

The next one-degree question is whether the signed circuit-variable incidence admits a stronger polynomially recognizable decomposition/dominance rule, or whether a counterfamily forces large compatibility boundary despite the balance structure.

## 8. Claim ceiling

    SCOPED POLYNOMIAL TERMINAL = YES
    UNIVERSAL SMALL-ADHESION THEOREM = NOT ESTABLISHED
    UNIVERSAL P=NP = NOT ESTABLISHED

    LOCAL SAT != GLOBAL SAT
    SMALL SEPARATOR EXISTENCE != CHEAP DISCOVERY
    SPAN != WORK
