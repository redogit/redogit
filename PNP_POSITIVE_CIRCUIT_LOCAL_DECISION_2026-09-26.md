# Positive Balance-Circuit Local Decision — 2026-09-26

**Program:** P vs NP / synchronized qualitative-centrality route  
**Predecessor:** `PNP_SYNCHRONIZATION_PACKET_2026-09-26.md`  
**Status:** scoped exact theorem + bounded exhaustive validation  
**Claim ceiling:** not a universal P=NP proof

## 1. Object

Let F be the fully normalized linearly-lean residual and M(F) its signed clause-variable matrix.

Let C be the support of one support-minimal positive balance vector z:

    z > 0 on C
    M_C^T z = 0

and no nonempty proper subset of C supports a nonzero nonnegative balance vector.

As established in the predecessor balance carrier, C is a circuit of the row matroid of M. Therefore

    rank(M_C) = |C|-1

and every proper subset of the rows in C is linearly independent.

Let F_C be exactly the clauses indexed by C.

## 2. Theorem

If F_C is UNSAT, then F_C is minimally UNSAT and has deficiency exactly one:

    |C| - |Var(F_C)| = 1.

### Proof

Assume F_C is UNSAT.

Choose an inclusion-minimal UNSAT subformula H subseteq F_C.

By Tarsi's lemma for minimally unsatisfiable CNFs,

    c(H) > n(H).

The signed clause-variable matrix M_H has c(H) rows and n(H) relevant variable columns, so

    rank(M_H) <= n(H) < c(H).

Thus the rows indexed by H are linearly dependent.

But C is a row-matroid circuit: every proper subset of C is linearly independent.

Therefore H cannot be a proper subset. Hence

    H = F_C.

So F_C itself is minimally UNSAT.

Again by Tarsi,

    |C| > |Var(F_C)|.

On the other hand,

    |C|-1
      = rank(M_C)
      <= |Var(F_C)|.

Combining the two inequalities gives

    |C| = |Var(F_C)| + 1.

QED.

## 3. Exact polynomial local terminal

The theorem gives a promise-specific local decision procedure for every extracted positive balance circuit.

Let c=|C| and v=|Var(F_C)|.

1. If c != v+1, return SAT for F_C.
   - Under the row-circuit promise, UNSAT would force c=v+1 by the theorem.

2. If c=v+1, run an exact polynomial recognizer for minimal unsatisfiability at deficiency one.
   - Davydov, Davydova, and Kleine Buning (1998) give a quadratic-time algorithm for the n+1-clause minimal-unsatisfiability problem.

3. If the recognizer returns minimally UNSAT, return LOCAL_UNSAT.
   Otherwise return SAT.
   - Under the row-circuit promise, every UNSAT F_C is minimally UNSAT, so rejection of MU(1) implies satisfiable.

Consequently:

    EVERY POSITIVE BALANCE CIRCUIT
    IS INDIVIDUALLY SAT/UNSAT DECIDABLE
    IN POLYNOMIAL TIME.

If any circuit support is LOCAL_UNSAT, the whole residual F is UNSAT.

If every circuit support is SAT, then no remaining obstruction is internal to one positive balance circuit.

## 4. Repaired remainder

After all circuit-local checks return SAT, the unresolved obligation is necessarily cross-circuit compatibility:

    LOCALLY SATISFIABLE POSITIVE CIRCUITS
    +
    SHARED SIGNED VARIABLE INCIDENCE
    ->
    GLOBAL QUALITATIVE CENTRALITY ?

This is stronger than the previous statement that circuit overlap alone is insufficient.

The next carrier must preserve enough of the signed cross-circuit incidence to distinguish compatible local satisfying orthants from globally incompatible ones.

## 5. Relation to qualitative centrality

For A=M(F)^T, sign-centrality is equivalent to:

    for every strict row signing D,
    DA contains a nonnegative column.

The positive-circuit local theorem does not enumerate row signings.

It removes one source of ambiguity:

    INTERNAL CIRCUIT HARDNESS

from the remaining problem.

After local closure, the only useful next quotient is one whose states describe compatibility of circuit-local orthant constraints across shared variables.

Do not replace that compatibility problem with an uncharged Boolean selector.

## 6. External source alignment

- Tarsi/Aharoni-Linial deficiency fact: every minimally unsatisfiable CNF has positive deficiency.
- G. Davydov, I. Davydova, H. Kleine Buning, *An Efficient Algorithm for the Minimal Unsatisfiability Problem for a Subclass of CNF*, Annals of Mathematics and Artificial Intelligence 23 (1998), 229-245, DOI 10.1023/A:1018924526592. The n+1-clause minimal-unsatisfiability problem is solvable in quadratic time.
- Broader fixed-parameter results for bounded deficiency are consistent with this local terminal but are not needed for the theorem above.

## 7. Bounded exhaustive validation

Canonical 3-variable signed clauses were exhaustively enumerated for clause-set sizes 2 through 4.

    candidate clause sets: 17,875
    support-minimal positive row circuits: 777
    UNSAT positive row circuits: 269
    violations of [minimal UNSAT and deficiency 1]: 0

The enumeration checked exact rational row rank, one-dimensional positive dependence, truth-table satisfiability, minimal unsatisfiability, and deficiency.

This finite panel validates the implementation/statement on the bounded domain only. It is not the proof.

## 8. Process disposition

    GENERATE: positive-circuit local theorem
    VERIFY: rank/circuit/Tarsi derivation
    EXTERNAL CHECK: MU(1) polynomial recognizer literature
    COMPUTATION: bounded exhaustive panel, zero violations
    ADMIT: scoped exact local terminal
    UNIVERSAL P=NP: OPEN

## 9. Next one-degree question

Assume every selected positive balance circuit is locally SAT.

Construct a polynomially discoverable compatibility carrier on shared signed variable incidences that either:

- glues circuit-local satisfying orthants;
- removes/dominates one global Boolean degree;
- decomposes the circuit system into independent obligations;
- yields a reusable polynomial projection; or
- certifies that no global orthant can satisfy all circuits.

The carrier must be strictly cheaper than explicit enumeration of all circuit-local satisfying assignments.

    LOCAL SAT != GLOBAL SAT
    CIRCUIT OVERLAP != SIGNED COMPATIBILITY
    SPAN != WORK
