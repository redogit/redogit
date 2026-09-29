# Tight-Block Resolution Lift to Parent Interface — 2026-09-26

**Program:** synchronized P vs NP proof program
**Predecessor:** corrected `PNP_TIGHT_BLOCK_COFACTOR_DEFICIENCY_2026-09-26.md`
**Status:** exact conditional lift theorem + explicit tautology obstruction
**Claim ceiling:** not universal P=NP

## 1. Parent / tight restriction

Let F be the parent CNF and V a tight variable block.

For every parent clause C touching V write:

    C = D_C union E_C

where:

    D_C = literals whose variables lie in V
    E_C = literals whose variables lie outside V.

The restricted tight formula is:

    G=F[V]={D_C}.

Deleting E_C strengthens the touched clauses.

Therefore an UNSAT proof of G is not automatically an UNSAT proof of F.

## 2. Annotated resolution lift

Take a resolution derivation inside G using pivots only from V.

Annotate every leaf D_C with its parent outside remainder E_C.

Replay a resolution step:

    (A union {x}), (B union {-x})
    -> A union B

using the corresponding parent/lifted clauses.

The lifted step resolves the same internal pivot x while carrying every outside literal inherited from its ancestors.

At the end, if the restricted derivation reaches the empty clause, the lifted derivation reaches a clause L whose variables all lie outside V.

By soundness of resolution:

    touched parent clauses entail L.

Thus L is a parent-valid interface consequence.

## 3. Tautology gate

L may be tautological.

Example:

    parent:
      {x,a}
      {-x,-a}

    restriction to V={x}:
      {x}
      {-x}

The restriction is UNSAT.

The lifted resolution result is:

    {a,-a},

a tautology.

So:

    INTERNAL REFUTATION
    !=
    USEFUL PARENT INTERFACE CLAUSE.

A useful lift requires:

    L non-tautological.

## 4. Sufficient compatibility condition

For one chosen restricted resolution proof P, let:

    E(P)=union of all outside remainders E_C
         over source clauses used by P.

If E(P) contains no complementary literal pair, then every lifted intermediate outside annotation is non-tautological and the final interface clause L is non-tautological.

Therefore:

    RESTRICTED REFUTATION
    +
    SIGN-COMPATIBLE OUTSIDE SUPPORT
    ->
    NONTRIVIAL PARENT INTERFACE CLAUSE.

This condition is polynomially checkable once P is known.

It is sufficient, not necessary; cancellations/subsumptions may permit useful lifts even when the raw union has clashes.

## 5. Parent-level use

A non-tautological lifted interface clause L is a logical consequence of the touched parent clauses.

It may be:

- added as a learned/projection clause;
- tested for subsumption/dominance;
- used to expose a functional relation;
- used in a bounded parent-level projection;
- or used to reduce the outside-interface search space.

Its addition alone is not guaranteed to reduce representation size.

Any admission into normalization needs the same global size/potential accounting as other generated clauses.

## 6. Exact projection interpretation

The complete parent-safe Object at the boundary is:

    exists V . conjunction(touched parent clauses).

This is a Boolean relation on the outside-interface variables.

Resolution elimination on variables V can represent that relation as interface clauses.

The restricted formula G corresponds to strengthening the interface by deleting all outside literals, not to the exact existential projection.

Therefore:

    TIGHT RESTRICTION = STRUCTURAL PROBE
    EXISTENTIAL INTERFACE RELATION = LIFTABLE PARENT OBJECT.

This repairs the Surface boundary.

## 7. New edge

Given a tight block V:

Door A:
    G SAT
    -> autarky
    -> parent clause removal.

Door B:
    G UNSAT
    -> seek a compact non-tautological interface consequence/projection.

The obstruction inside Door B is:

    OUTSIDE-SIGN CANCELLATION / INTERFACE COMPLEXITY.

This is now the parent-safe continuation of the core climb.

## 8. Counterprobe obligation

Search for families where:

- G is UNSAT;
- every short/selected restricted refutation lifts only to tautological or redundant interface clauses;
- yet the exact existential interface relation requires large representation.

Such a family would burn naive proof lifting and force a different carrier.

Conversely, a theorem guaranteeing polynomially many useful lifted clauses for normalized tight blocks would be a genuine parent-level advance.

## 9. Claim ceiling

    ANNOTATED RESOLUTION LIFT = EXACT
    NONTAUTOLOGICAL LIFT -> PARENT CONSEQUENCE = EXACT
    SIGN-COMPATIBLE OUTSIDE SUPPORT SUFFICIENT = EXACT
    EVERY TIGHT REFUTATION HAS USEFUL LIFT = NOT ESTABLISHED
    POLYNOMIAL INTERFACE PROJECTION = OPEN
    UNIVERSAL P=NP = OPEN

    INTERNAL PROOF != PARENT PROOF
    RESTRICTION != EXISTENTIAL PROJECTION
    LIFTABILITY IS A FIRST-CLASS OBLIGATION
