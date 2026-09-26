# Boundary Residual Orthant Arrangement — 2026-09-26

**Program:** synchronized P vs NP proof program  
**Predecessor:** `PNP_BOUNDARY_RESIDUAL_MAP_2026-09-26.md`  
**Status:** exact geometric bound; Boolean-interface implication open  
**Claim ceiling:** not universal P=NP

## 1. Residual subspace

For tight block V with boundary B:

    rho_B : K_V -> R^B
    R_V = image(rho_B)
    beta = dim R_V.

R_V is the linear space of boundary residual pressures produced by internal balance directions.

## 2. Sign regimes

Two nonzero residual vectors r,r' in R_V are in the same open sign regime when every boundary coordinate has the same sign:

    sign(r_b)=sign(r'_b)
    for all b in B

with zero coordinates treated as lying on arrangement boundaries.

The coordinate hyperplanes:

    H_b = { r in R_V : r_b=0 }

form a central hyperplane arrangement in a beta-dimensional vector space.

## 3. Exact region bound

A central arrangement of m hyperplanes in R^beta has at most:

    2 * sum_{i=0}^{beta-1} binomial(m-1,i)

open regions.

Here m<=|B| after discarding identically-zero/repeated coordinate restrictions.

Therefore the number of strict sign regimes of boundary residual pressure is at most:

    2 * sum_{i=0}^{beta-1} binomial(|B|-1,i)
    =
    O(|B|^(beta-1))

for fixed beta.

Including lower-dimensional zero-sign faces still gives a polynomial number of sign cells for every fixed beta, with exponent depending on beta.

Thus:

    FIXED BOUNDARY-RESIDUAL RANK
    ->
    POLYNOMIALLY MANY LINEAR SIGN REGIMES.

## 4. What this does not prove

The exact Boolean existential interface:

    exists V . touched-parent-CNF

need not be determined solely by the sign regime of a real balance residual.

Therefore:

    POLYNOMIALLY MANY LINEAR SIGN CELLS
    !=
    POLYNOMIAL BOOLEAN INTERFACE

without a comparison theorem.

This is a scoped geometric compression only.

## 5. Joint seam carrier

The candidate seam carrier now has two parts:

    LINEAR:
      residual subspace R_V
      beta=dim R_V
      coordinate-hyperplane sign arrangement

    BOOLEAN:
      first mixed resolution layer
      outside-literal conflict graph
      lifted non-tautological interface clauses.

The bridge obligation is:

> Within one residual sign cell, are all relevant Boolean first-mixed conflicts equivalent for the parent decision obligation, or can exponentially many Boolean distinctions survive inside a single linear cell?

This is the cheapest falsification target.

## 6. Scoped polynomial terminal candidate

If one can prove for a class C of normalized tight blocks that:

1. beta(V)<=b for fixed b;
2. every Boolean interface distinction is determined by the residual sign cell plus polynomial local metadata;
3. the arrangement and metadata are polynomially constructible;

then the interface has a polynomial exact carrier.

Only item 1 is supplied by small beta itself.

Items 2-3 remain proof obligations.

## 7. Pressure interpretation

BEND pressures now disagree usefully:

    LINEAR PRESSURE:
      small beta can mean few residual directions.

    BOOLEAN PRESSURE:
      forgetting/interpolation can still be exponentially complex.

The seam is whatever Boolean information remains after quotienting by the residual sign arrangement.

That remainder is the next Object.

## 8. Next counterprobe

Search finite normalized tight blocks for pairs of boundary assignments / proof supports that:

    occupy the same residual sign cell

but:

    differ in liftability,
    differ in interface truth,
    or require distinct prime interface clauses.

If found, identify the smallest extra distinction.

Repeat until either:

    a polynomial joint carrier survives,

or:

    the residual quotient collapses back to the full Boolean interface.

## 9. Claim ceiling

    ORTHANT ARRANGEMENT REGION BOUND = EXACT
    FIXED beta -> POLY LINEAR SIGN REGIMES = EXACT
    LINEAR SIGN REGIME DETERMINES BOOLEAN INTERFACE = OPEN
    JOINT LINEAR/BOOLEAN CARRIER = ACTIVE
    UNIVERSAL P=NP = OPEN

    LOW DIMENSION != LOW BOOLEAN COMPLEXITY
    PRESSURE DISAGREEMENT REVEALS THE SEAM
