# Surplus / Non-Mersenne Autarky-Reduction Terminal — 2026-09-26

**Program:** synchronized P vs NP proof program  
**Predecessor:** `PNP_SYNCHRONIZATION_HANDOFF_002_2026-09-26.md`  
**Status:** admitted polynomial SAT-decision reduction; Homeward witness assignment remains separately bounded  
**Claim ceiling:** not a universal P=NP proof

## 1. Why this is new relative to the current normalization

The 2026-09-25 normalization already includes:

- maximal matching-autarky reduction / matching-lean kernel;
- maximal linear-autarky reduction;
- later cofactor/BCE/functional/DP rules.

Kullmann-Zhao Theorem 10.2 gives a further polynomial clause-removal reduction that can still fire **after matching-autarky reduction**.

Let:

    sigma(F) = surplus(F)
    muvd(F)  = minimum variable degree
    nM(k)    = kth non-Mersenne number.

For matching-lean F with sigma(F)>=1, if

    muvd(F) > nM(sigma(F)),

one can compute in polynomial time a nonempty variable set V attaining minimum surplus and remove all clauses touching V. The resulting sub-clause-set is satisfiability-equivalent to F because there exists an autarky whose variable set is V.

Crucially:

    REDUCED CLAUSE OBJECT IS POLYTIME COMPUTABLE
    WITNESS AUTARKY ASSIGNMENT IS NOT KNOWN POLYTIME IN GENERAL.

This is exactly an Object-removal / coordinate-separation result.

## 2. External theorem

Kullmann-Zhao, *Bounds for variables with few occurrences in conjunctive normal forms*, Theorem 10.2:

For every multi-clause-set F, a sub-clause-set F' subseteq F can be found in polynomial time such that:

1. there exists an autarky phi for F with F'=phi*F;
2. if F' has variables, then sigma(F')>=1 and

       muvd(F') <= nM(sigma(F')).

The algorithm loops:

1. compute the matching-lean kernel;
2. compute surplus sigma(F) and a minimum-surplus variable set V;
3. if muvd(F)>nM(sigma(F)), remove every clause containing a variable of V;
4. repeat.

The paper explicitly separates this reduction from Conjecture 10.3, which asks for polynomial computation of the witnessing autarky assignment itself.

## 3. New normalization rule

Add:

    R6_SURPLUS_AUTARKY_OBJECT_REDUCTION

Precondition:

    n(F)>0
    matching-autarky normalization already saturated
    sigma(F)>=1
    muvd(F)>nM(sigma(F)).

Action:

    compute a minimum-surplus nonempty variable set V
    remove every clause touching V
    canonical-clean
    restart normalization.

Receipt:

    source clause IDs
    V
    sigma(F)
    delta(F[V]) = sigma(F)
    muvd(F)
    nM(sigma(F))
    exact removed clause IDs
    predecessor/successor UOIDs.

Decision semantics:

    SAT(F) iff SAT(F').

Progress:

    at least one variable and at least one touched clause leave the active residual;
    hence repeated R6 applications terminate in at most the original variable/clause count.

## 4. Interaction with R1 and R2

R6 is not R1.

R1 handles matching autarkies and reaches the matching-lean kernel. Theorem 10.2 explicitly applies its second reduction after matching-autarky elimination, so R6 can strictly refine an R1 fixed point.

R6 is not automatically R2.

R2 handles linear autarkies with an explicit polynomial LP witness. The external theorem guarantees a general autarky behind R6 but does not guarantee that it is linear. No evidence currently shows that R2 subsumes R6.

Therefore:

    R1 FIXED POINT != R6 FIXED POINT
    R2 FIXED POINT != PROVED R6 FIXED POINT.

## 5. Homeward boundary

For SAT/UNSAT **decision**, R6 is exact immediately:

    F SAT iff F' SAT.

For an UNSAT result, no removed-clause witness assignment is needed; the UNSAT certificate of F' also establishes UNSAT of F because F and F' are equisatisfiable and F' subseteq F.

For a SAT result, reconstructing a full satisfying assignment for F from a satisfying assignment of F' requires a satisfying assignment for the removed autarky block.

Theorem 10.2 guarantees existence but does not provide that assignment in polynomial time. The paper isolates this as the MLCR / Conjecture 10.3 problem.

Therefore:

    R6 = ADMITTED FOR SAT/UNSAT DECISION
    R6 = NOT YET ADMITTED FOR POLYNOMIAL HOMEWARD SAT-WITNESS RECONSTRUCTION.

Do not silently restore the removed variables.

## 6. Repaired normalization lifecycle

For the decision program:

    R1 matching-autarky kernel
    -> R2 linear-autarky kernel
    -> R3 cofactor dominance
    -> R4 BCE
    -> R5 functional / non-increasing DP family
    -> R6 surplus/non-Mersenne autarky-object reduction
    -> restart to fixed point.

Because R6 may expose new R1-R5 opportunities, restart the full schedule after every R6 change.

The exact ordering may later be optimized, but the fixed-point semantics must include R6.

## 7. New residual invariant

At a fully saturated R6 fixed point with variables:

    sigma(F)>=1
    and
    muvd(F) <= nM(sigma(F))
             <= sigma(F)+1+log2(sigma(F)).

Thus every remaining matching-lean residual has a provably bounded-degree variable relative to its surplus.

This does not by itself give a polynomial branching algorithm when sigma(F) grows with input size.

But it removes the high-minimum-degree cell from the active residual without constructing a Boolean selector.

## 8. New exact missing seam

The Homeward SAT-witness problem created by R6 is not vague.

Kullmann-Zhao identify the critical class MLCR. For the minimum-surplus sets used by R6, the induced restricted clause-set F[V] lies in MLCR and is satisfiable.

The missing assignment seam is:

    FIND A SATISFYING ASSIGNMENT FOR MLCR IN POLYNOMIAL TIME.

This is equivalent in their framework to polynomial construction of the relevant nontrivial autarky.

For the P-vs-NP **decision** obligation, R6 itself is already usable without solving this seam.

For a constructive SAT witness obligation, MLCR becomes an explicit Homeward Remainder.

## 9. Current P-vs-NP remainder after R6

After saturation:

    matching-lean
    linearly lean
    R3-R5 irreducible
    R6 irreducible
    positive balance circuits locally tractable
    muvd(F) <= nM(sigma(F))
    large signed cross-circuit compatibility may remain
    qualitative centrality unresolved.

The next one-degree attack should ask whether the guaranteed low-degree variable at the R6 fixed point is:

- functionally determined;
- dominance-removable;
- cheaply DP-projectable;
- decomposing in the positive-circuit incidence;
- or a source of a bounded reusable projection.

Do not branch merely because its degree is bounded by nM(sigma).

## 10. Claim ceiling

    NEW POLYNOMIAL SAT-DECISION REDUCTION = ADMITTED
    STRICT NOVELTY OVER R1 = ESTABLISHED BY THEOREM'S POST-MATCHING STEP
    STRICT NOVELTY OVER R2 = NOT PROVED UNIVERSALLY, BUT NO SUBSUMPTION EVIDENCE
    POLYNOMIAL SAT-WITNESS HOMEWARD = OPEN (MLCR seam)
    UNIVERSAL P=NP = OPEN

    OBJECT REMOVAL != WITNESS ASSIGNMENT
    DECISION EQUIVALENCE != HOMEWARD COMPLETION
    SPAN != WORK
