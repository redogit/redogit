# Logarithmic-Surplus Tight-Edge Closure — 2026-09-26

**Program:** synchronized P vs NP proof program
**Predecessor:** `PNP_MINIMUM_SURPLUS_FORK_2026-09-26.md`
**Status:** scoped exact polynomial terminal
**Claim ceiling:** not universal P=NP

## 1. Tight block

Let V be a nonempty minimum-surplus variable set of F and let:

    G = F[V]
    k = sigma(F).

Then:

    delta(G)=k
    sigma(G)=k.

Since k>0, G is matching-lean.

For matching-lean clause-sets:

    delta*(G)=delta(G).

Therefore:

    delta*(G)=k.

## 2. Exact fork decision by maximum deficiency

SAT parameterized by maximum deficiency k is fixed-parameter tractable.

Using the Szeider maximum-deficiency algorithm:

    SAT(G)
    can be decided in
    O(2^k * poly(|G|))

with a satisfying assignment or a regular-resolution refutation in the corresponding outcome.

Thus the minimum-surplus fork is algorithmically selectable with parameter exactly equal to the surplus thickness of the tight block.

## 3. Door A

If G is SAT, return a satisfying assignment alpha of G.

As proved in the minimum-surplus fork theorem, alpha is an autarky of F on V and removes every clause touching V satisfiability-equivalently.

## 4. Door B

If G is UNSAT, use the returned negative certificate plus the minimum-surplus/non-Mersenne theorem to select a controlled low-degree variable inside V.

Then apply the currently admitted normalization/projection rules if one is applicable.

The fork decision itself does not justify an unbounded materialized DP step.

## 5. Logarithmic closure

Let N be the encoded input scale for the current polynomially bounded normalization carrier.

If:

    k = sigma(F) <= c log_2 N

for a fixed constant c, then:

    2^k <= N^c.

Therefore the tight-edge fork is selectable in polynomial total work.

So the verified core now includes:

    ALL RESIDUALS WHOSE CURRENT SURPLUS
    IS O(log N)

for the fork-selection obligation.

This strictly strengthens:

    every fixed surplus K is tractable.

## 6. Uniformity boundary

The first unresolved surplus regime is now:

    sigma(F) = omega(log N).

The remaining universal problem is not low/fixed/logarithmic surplus.

It is the high-expansion regime.

This is conceptually important:

    SMALL EDGE THICKNESS
    -> EXACT FPT DOOR SELECTION

    SUPERLOGARITHMIC EDGE THICKNESS
    -> CURRENT OPEN CORE-CLIMB REGION.

## 7. Interaction with R5+B

For logarithmic k:

    nM(k)=O(k+log k)=O(log N).

A minimum-degree internal variable under Door B therefore has logarithmic occurrence degree.

Materialized DP can generate at most:

    O(log^2 N)

raw resolvents for that variable.

This is polynomially small per selected projection.

If the fork/projection is repeated, cumulative representation still requires the existing global lifecycle accounting; do not infer universal closure solely from one local logarithmic step.

However if each successful step remains inside a fixed polynomial envelope and the fork is recomputed, the per-step discovery cost is polynomial.

## 8. New nearest edge

The core has climbed to:

    sigma <= O(log N).

The nearest edge is:

    SUPERLOGARITHMIC SURPLUS
    +
    minimum-surplus tight block
    +
    matching-lean / maximum-deficiency k
    +
    strict positive balance on the normalized parent.

Question:

> What additional structure becomes stronger, not weaker, as the tight block's expansion k grows?

Candidates:

- Hall/DM irreducibility;
- positive-balance circuit density;
- signed incidence expansion;
- qualitative-matrix rigidity;
- forced redundancy among low-degree projections.

The high-surplus regime should be attacked as a high-expansion object, not merely as a larger parameter value.

## 9. Claim ceiling

    TIGHT BLOCK delta*=sigma = EXACT
    FORK FPT IN sigma = EXACT
    sigma=O(log N) FORK SELECTION = POLYNOMIAL
    SUPERLOGARITHMIC SURPLUS CLOSURE = OPEN
    UNIVERSAL P=NP = OPEN

    FPT PARAMETERIZATION != UNIVERSAL POLYNOMIALITY
    LOGARITHMIC PARAMETER != UNBOUNDED PARAMETER
    CORE EXPANSION != DESTINATION
