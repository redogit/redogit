# Tight-Block Cofactor Deficiency Theorem — 2026-09-26

**Program:** synchronized P vs NP proof program
**Predecessor:** `PNP_TIGHT_BLOCK_BALANCE_INHERITANCE_2026-09-26.md`
**Status:** exact structural theorem + improved FPT fork algorithm
**Claim ceiling:** not universal P=NP

## 1. Tight block

Let G be a minimum-surplus tight block with:

    n=n(G)
    m=m(G)
    sigma(G)=delta(G)=k>0.

Thus:

    m=n+k.

Let v be any variable.

Let H_v be the sub-clause-set consisting of all clauses not containing v in either polarity.

## 2. Matching-satisfiable complement theorem

Claim:

    delta*(H_v) <= 0.

### Proof

Assume for contradiction there exists H' subseteq H_v with positive deficiency:

    |H'|-|var(H')| = r > 0.

Let:

    U=var(H')
    S=var(G) \ U.

Because every clause of H' avoids v, we have v notin U, hence v in S and S is nonempty.

No clause of H' touches S.

Therefore every clause touching S lies outside H', so:

    |Gamma_G(S)|
      <=
    m-|H'|.

Hence:

    |Gamma_G(S)|-|S|
      <=
    (n+k-|H'|) - (n-|U|)
      =
    k-(|H'|-|U|)
      =
    k-r
      <
    k.

But sigma(G)=k says every nonempty S has expansion at least k.

Contradiction.

Thus every H' subseteq H_v has deficiency <=0 and:

    delta*(H_v)<=0.

QED.

By matching theory, H_v is matching-satisfiable and admits polynomial exact handling.

## 3. Cofactor maximum-deficiency bounds

Let:

    p = number of clauses containing v
    q = number of clauses containing -v.

Set v=true.

The p positive-parent clauses are satisfied and disappear.

At most q negative-parent clauses survive with -v deleted.

The remainder is H_v plus at most q additional clauses.

For every sub-clause-set J of the cofactor, separate:

    J = J_H union J_q

where J_H subseteq H_v and |J_q|<=q.

Since delta(J_H)<=0, adding |J_q| clauses can raise deficiency by at most |J_q|.

Therefore:

    delta*(G|v=true) <= q.

Similarly:

    delta*(G|v=false) <= p.

These are exact upper bounds independent of clause width.

## 4. One-sided fork algorithm

Assume the obstruction/UNSAT-side non-Mersenne theorem has selected an internal variable v with:

    p+q = vd(v) <= nM(k)

and:

    p<=k
    q<=k.

Choose the truth value b that leaves the smaller opposite-polarity side:

    s=min(p,q).

Then:

    delta*(G|v=b) <= s.

Run exact maximum-deficiency SAT only on this one cofactor.

### If the tested cofactor is SAT

The returned assignment plus v=b satisfies G.

Therefore the tight block is SAT.

In the parent minimum-surplus fork, this supplies the autarky/removal door.

### If the tested cofactor is UNSAT

Then no satisfying assignment of G can have v=b.

Therefore:

    G entails v=1-b.

Fix v to the opposite value as an exact forced-literal / cofactor-dominance move.

No second SAT call is needed to justify the fixing.

Thus one parameterized cofactor query always yields either:

    SAT TIGHT BLOCK
or
    EXACT DEGREE REMOVAL.

## 5. Cost

The maximum-deficiency SAT algorithm costs:

    O(2^s poly(N)).

And:

    s
      <=
    floor(vd(v)/2)
      <=
    floor(nM(k)/2)
      <=
    (k+1+log2(k))/2.

Therefore the fork cost is:

    2^(k/2) * poly(k,N)

up to the logarithmic non-Mersenne factor.

More explicitly:

    2^s
    <=
    2^((k+1+log2 k)/2)
    =
    O(sqrt(k) * 2^(k/2)).

This improves the earlier direct O(2^k) tight-block fork.

## 6. Expanded logarithmic core

If:

    k <= c log2 N

then cost is:

    O(sqrt(log N) * N^(c/2) * poly(N)).

Thus every fixed constant multiple of logarithmic surplus remains polynomial, with half the exponent contribution compared with direct tight-block SAT.

Equivalently, for a fixed allowed polynomial exponent budget, the admissible logarithmic-surplus thickness approximately doubles.

This is a quantitative improvement, not a superlogarithmic closure.

## 7. Why this is structurally useful

The hard block decomposes around every variable into:

    MATCHING-SATISFIABLE COMPLEMENT
    +
    p positive attachments
    +
    q negative attachments.

So the Boolean difficulty at v is carried entirely by the signed attachment clauses.

The smaller attachment side is enough to test one value.

This is much closer to the user's core/edge geometry:

    CORE = matching-solvable complement
    EDGE = signed attachments through v.

Bend only the smaller edge first.

## 8. Interaction with positive balance

The tight block also inherits:

    full column rank
    strict positive balance
    k-dimensional left nullspace
    <=k positive balance circuits covering all clauses.

The cofactor theorem does not yet use these facts.

Therefore positive balance remains available as an independent degree for improving the one-sided cofactor cost below 2^(k/2), or for proving that the smaller attachment side has additional structure.

Do not count that improvement before proving it.

## 9. Next one-degree target

For the selected low-excess v, inspect the smaller polarity attachment family A_v of size s.

Question:

> Does strict positive balance plus tight expansion force the maximum deficiency of the tested cofactor to be substantially smaller than s, or force A_v to decompose into independently testable pieces?

Candidate target bounds:

    delta*(G|v=b) <= O(log k)

or

    attachment interaction width <= O(log k).

Either would turn the superlogarithmic k region into a polynomially selectable edge.

## 10. Claim ceiling

    H_v MAX DEFICIENCY <=0 = EXACT
    COFACTOR delta* <= OPPOSITE POLARITY COUNT = EXACT
    ONE-SIDED FORK = EXACT
    COST O(sqrt(k) 2^(k/2) poly(N)) = EXACT
    SUPERLOGARITHMIC POLYNOMIAL CLOSURE = OPEN
    UNIVERSAL P=NP = OPEN

    ONE SIDE TESTED != BOOLEAN BRANCH TREE
    FPT IMPROVEMENT != POLYNOMIAL FOR UNBOUNDED k
    CORE EXPANSION != DESTINATION
