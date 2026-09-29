# Surplus Inflation Counterprobe and Expansion-Witness Edge — 2026-09-26

**Program:** synchronized P vs NP proof program
**Predecessor:** `PNP_SURPLUS_INFLATION_UNIFORM_EDGE_2026-09-26.md`
**Status:** exact counterexamples + repaired carrier hypothesis
**Claim ceiling:** not universal P=NP

## 1. Question

Can DP-induced surplus inflation be paid for by ordinary clause-count growth?

Answer: no.

Surplus is the minimum Hall-style expansion

    sigma(F)=min_{nonempty V subseteq var(F)} |Gamma_F(V)|-|V|.

DP changes this incidence geometry even when the number of clauses does not grow.

## 2. Exact zero-growth counterexample: surplus 1 -> 2

Let

    F = {
      { x1, -x3 },
      { x1,  x3 },
      {-x1,  x2 },
      {-x1, -x2 }
    }.

Then:

    n(F)=3
    c(F)=4
    sigma(F)=1.

Minimum-surplus witnesses include:

    {x2}
    {x3}

each touching exactly two clauses.

Eliminate x1 by exact DP.

All four opposite-polarity parent pairs yield:

    { x2,  x3 }
    { x2, -x3 }
    {-x2,  x3 }
    {-x2, -x3 }.

Thus:

    n(F')=2
    c(F')=4
    clause growth = 0
    sigma(F')=2.

So:

    Delta c = 0
    Delta sigma = +1.

## 3. Stronger bounded counterexample: surplus 1 -> 3 with zero clause growth

A finite exact search on four variables found:

    F = {
      { x1,  x4 },
      {-x4, -x3 },
      {-x2,  x4 },
      {-x1,  x2 },
      {-x4,  x3 },
      {-x4, -x2, x1 }
    }.

For elimination of x4:

    positive x4 parents = 2
    negative x4 parents = 3
    cleaned predecessor clauses = 6
    cleaned successor clauses = 6.

Exact surplus:

    sigma(F)=1
    sigma(DP_x4(F))=3.

Hence:

    Delta c = 0
    Delta sigma = +2.

The successor is:

    {
      {-x3,  x1},
      {-x2,  x1},
      {-x2,  x3},
      {-x1,  x2},
      { x1,  x3},
      {-x3, -x2}
    }.

This is a finite counterexample to any proposed bound of the form:

    positive surplus inflation
    <=
    positive clause-count growth.

## 4. Interpretation

The eliminated variable acts as an incidence mediator.

Before elimination, small variable sets may have low expansion because several constraints meet through the eliminated variable.

Resolution composes those constraints directly among the surviving variables.

After elimination, the same surviving variables can touch a denser family of clauses even with unchanged total clause count.

Thus:

    DP FILL
    HAS A HALL-EXPANSION COMPONENT
    DISTINCT FROM CLAUSE-COUNT FILL.

Surplus inflation is therefore not merely representation growth.

It is a change in the minimum-expansion witness geometry.

## 5. Required carrier

For each current formula retain at least one canonical minimum-surplus witness:

    W subseteq var(F)
    |Gamma(W)|-|W| = sigma(F).

Better, when polynomially representable, retain the family/lattice of minimum-surplus witnesses or a canonical certificate sufficient to reconstruct them.

For candidate elimination v, measure:

    whether v in W;
    clauses touching W and v;
    which new resolvents enter Gamma'(W\{v});
    whether W survives as a low-expansion witness;
    whether multiple minimum witnesses merge/disappear.

The next potential candidate must account for:

    representation debt
    +
    destruction of low-expansion witnesses.

## 6. What is burned

    CLAUSE GROWTH PAYS SURPLUS GROWTH = ASH.

Also unsupported:

    ZERO-GROWTH DP PRESERVES SURPLUS.

It does not.

## 7. Literature alignment

The clause-set literature defines surplus exactly as minimum variable-to-clause expansion and uses it to characterize matching leanness and low-degree bounds.

The singular-DP literature proves deficiency preservation for singular DP on minimally unsatisfiable formulas, but that special theorem does not extend to arbitrary DP surplus preservation.

No external theorem has been admitted that bounds general DP surplus inflation tightly enough for the universal proof obligation.

## 8. New edge

The nearest edge is now:

    MINIMUM-SURPLUS WITNESS DESTRUCTION UNDER PROJECTION.

Question:

> Can we choose/project a low-degree variable so that either a minimum-surplus witness survives with controlled inflation, or the destruction of that witness releases another polynomially bounded resource that pays for the projection?

This is more precise than tracking sigma as a scalar.

## 9. Finite computation boundary

The examples above were checked by exact enumeration of nonempty variable subsets for surplus and exact canonical DP construction.

They falsify the stated monotonicity/payment hypotheses.

They do not prove a universal alternative potential.

## 10. Claim ceiling

    CLAUSE-GROWTH-ONLY POTENTIAL = REJECTED
    SURPLUS-SCALAR-ONLY POTENTIAL = INSUFFICIENTLY JUSTIFIED
    EXPANSION-WITNESS CARRIER = CANDIDATE
    UNIVERSAL AMORTIZATION = OPEN
    UNIVERSAL P=NP = OPEN
