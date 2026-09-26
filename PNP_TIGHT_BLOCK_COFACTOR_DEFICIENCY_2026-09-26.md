# Tight-Block Cofactor Deficiency — Corrected Scope — 2026-09-26

**Program:** synchronized P vs NP proof program  
**Predecessor:** `PNP_TIGHT_BLOCK_BALANCE_INHERITANCE_2026-09-26.md`  
**Status:** exact internal theorem + preserved failed parent-lift  
**Claim ceiling:** not universal P=NP

## 1. Critical scope distinction

Let F be the parent formula and V a minimum-surplus variable set.

    G = F[V]

is obtained from every clause touching V by deleting literals whose variables lie outside V.

Therefore G is generally a **strengthening/projection carrier**, not an equisatisfiable subformula of F.

Exact directions:

    SAT(G)
    -> satisfying assignment on V is an autarky of F
    -> touched clauses can be removed from F.

But:

    UNSAT(G)
    !=
    UNSAT(F).

Outside-V literals deleted in G may satisfy the corresponding parent clauses.

Likewise:

    UNSAT(G|v=b)
    !=
    F entails v=1-b.

Any parent-level forced-literal claim based only on a cofactor of G is invalid.

This correction supersedes the parent-lift language in the first version of this artifact.

## 2. Internal complement theorem

Inside the tight block G assume:

    sigma(G)=delta(G)=k>0.

For any variable v in var(G), let H_v contain all clauses of G not touching v.

Then:

    delta*(H_v)<=0.

### Proof

Assume H' subseteq H_v has positive deficiency r.

Let U=var(H') and S=var(G)\U.

Since H' avoids v, v in S and S is nonempty.

No clause of H' touches S, so:

    |Gamma_G(S)| <= c(G)-|H'|.

Using c(G)=n(G)+k:

    |Gamma_G(S)|-|S|
      <=
    (n+k-|H'|)-(n-|U|)
      =
    k-r
      <
    k,

contradicting sigma(G)=k.

QED.

Thus H_v is matching-satisfiable.

## 3. Internal cofactor bounds

Let v occur p times positively and q times negatively in G.

Within G:

    delta*(G|v=true)<=q
    delta*(G|v=false)<=p.

Reason: each cofactor consists of H_v plus at most the opposite-polarity attachment clauses, and every sub-clause-set of H_v has deficiency <=0.

This is an exact structural statement about the tight carrier G.

## 4. What the internal cofactor solver can do

If an exact solver for one cofactor G|v=b returns SAT, then G is SAT.

That result lifts to the parent:

    SAT(G)
    -> AUTARKY(F,V).

If the cofactor returns UNSAT, then only the internal statement follows:

    G entails v=1-b.

This may guide the next structural analysis of G, but it does not authorize fixing v in F.

Therefore the previous claimed one-sided parent degree-removal algorithm is rejected.

## 5. Preserved Ash

The following inference is invalid:

    UNSAT(G|v=b)
    -> F entails v=1-b.

And therefore the proposed recurrence that repeatedly forced parent variables from tight-block cofactor UNSAT certificates is invalid.

Disposition:

    PARENT-LIFT OF INTERNAL FORCING = ASH
    QUASI-POLYNOMIAL RECURRENCE BASED ON THAT LIFT = ASH.

This is a representation-boundary failure:

    FAILED REPRESENTATION LIFT
    !=
    FAILED INTERNAL THEOREM.

## 6. What survives

Exact survivors:

1. H_v has maximum deficiency <=0 inside G.
2. G cofactors have maximum deficiency bounded by the opposite polarity count.
3. SAT of any G cofactor proves SAT(G).
4. SAT(G) gives a parent autarky.
5. UNSAT of a G cofactor supplies internal structural information only.
6. G inherits full rank and strict positive balance from F.

## 7. Correct nearest edge

We need a **liftable** internal certificate.

The next question is not merely:

    can we force v inside G?

It is:

> What property/certificate of the tight restriction G survives restoration of the deleted outside-V literals strongly enough to justify a parent-level removal, dominance, decomposition, or projection?

Possible liftable outputs include:

- a satisfying assignment of G (already lifts as autarky);
- a clause relation whose proof remains valid after restoring outside literals;
- a parent-matrix/qualitative relation proved using original clause rows rather than only restricted rows;
- an exact decomposition separating touched clauses from outside-variable support;
- a certificate explicitly quantifying the deleted literals.

## 8. Claim ceiling

    INTERNAL COMPLEMENT delta*<=0 = EXACT
    INTERNAL COFACTOR DEFICIENCY BOUNDS = EXACT
    SAT(G) -> PARENT AUTARKY = EXACT
    INTERNAL UNSAT -> PARENT FORCING = REJECTED
    QUASI-POLYNOMIAL PARENT ALGORITHM = REJECTED
    UNIVERSAL P=NP = OPEN

    RESTRICTION != EQUIVALENCE
    INTERNAL FORCING != PARENT FORCING
    HOMEWARD / LIFTABILITY IS REQUIRED
