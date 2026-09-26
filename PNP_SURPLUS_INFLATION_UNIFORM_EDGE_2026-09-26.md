# Core-Climb Correction — Surplus Inflation Is the Uniform Edge — 2026-09-26

**Program:** synchronized P vs NP proof program
**Predecessor:** `PNP_FIXED_B_BVE_UNIFORMITY_EDGE_2026-09-26.md`
**Status:** correction / sharper remainder
**Claim ceiling:** not universal P=NP

## 1. Correction

The predecessor said, too loosely:

    FOR EACH FIXED K, POLYNOMIAL
    !=
    ONE POLYNOMIAL FOR ALL K.

That statement is true as a general warning about non-uniform families, but it is not the sharp obstruction here.

For an input formula of encoded size N, the initial surplus K satisfies K<=O(N).

The finite-ring BVE allowance

    B(K)=G(nM(K))=O(K^2)

is therefore itself polynomial in the original input size.

If the surplus bound stayed at its original scale throughout elimination, choosing B from the original K would yield a uniform polynomial representation bound.

So:

    UNBOUNDED INITIAL K
    IS NOT BY ITSELF THE OBSTRUCTION.

## 2. Actual feedback edge

Exact DP elimination changes both clause count and deficiency.

If eliminating v has cleaned clause growth g:

    n' = n-1
    c' = c+g

so:

    delta' = c'-n'
           = delta + g + 1.

Surplus satisfies:

    sigma' <= delta',

but need not remain bounded by the predecessor surplus.

Thus the dangerous feedback is:

    DP GROWTH
    -> DEFICIENCY / POSSIBLE SURPLUS INFLATION
    -> LARGER R6 DEGREE BOUND
    -> LARGER NEXT DP GROWTH.

The universal edge is therefore:

    SURPLUS INFLATION UNDER PROJECTION.

## 3. What would close the edge

Any one uniform theorem of the following form is sufficient to prevent exponent escalation:

A. Surplus monotonicity:
       sigma(DP_v(F)) <= poly(original sigma, original N)
   with one fixed polynomial over the whole trace.

B. Amortized inflation:
       sum positive Delta-sigma <= poly(N_0).

C. Balance-charged inflation:
       every unit of DP/deficiency growth consumes a nonrenewable amount of
       positive-balance circuit dimension/incidence resource whose initial mass is polynomial.

D. Nonmaterialized projection:
       eliminate v while preserving exact SAT semantics in a carrier whose stored size
       grows only polynomially and whose next recognizers operate directly on that carrier.

E. Recompression:
       any temporary DP growth is followed by a polynomially discoverable canonical
       reduction returning the representation to a fixed polynomial envelope before
       the next degree is selected.

## 4. Why deficiency alone does not pay

For ordinary materialized DP:

    delta' = delta + g + 1.

So deficiency is not a decreasing potential; it is exactly one place where projection debt accumulates.

The positive-balance nullity of the current signed matrix is tied to deficiency only at the full-column-rank normalized CNF state. Generated resolvents can change that matrix and require re-normalization.

Therefore:

    CURRENT NULLITY
    !=
    AUTOMATIC NONRENEWABLE BUDGET.

A valid balance potential must be proved across the transformation, not inferred from the predecessor.

## 5. Core / edge geometry

Verified core:

    exact normalization R0-R6
    charged fixed-additive BVE
    positive-circuit local closure
    every fixed current surplus ring has polynomial local DP allowance.

Nearest edge:

    projection can inflate the parameter that controls the next guaranteed degree.

Goal:

    bend SURPLUS INFLATION inward
    by proving monotonicity, amortization, recompression, or a new exact carrier.

## 6. Next one-degree experiment

Measure one exact DP transformation together with:

    Delta n
    Delta c
    Delta delta
    Delta sigma
    Delta rank
    Delta positive-kernel dimension
    Delta selected circuit-cover size
    Delta signed cross-circuit incidence.

Search for a quantity Psi formed from these terms such that:

    Psi(successor) < Psi(predecessor)

or at least:

    cumulative positive representation debt
    <= initial polynomial Psi mass.

Do not infer Psi from empirical correlation; finite experiments only nominate candidates.

## 7. Corrected claim ceiling

    FIXED CURRENT-SURPLUS RING LOCALLY CLOSABLE = EXACT
    INITIAL UNBOUNDED SURPLUS BY ITSELF = NOT THE OBSTRUCTION
    SURPLUS INFLATION FEEDBACK = CURRENT UNIFORM EDGE
    AMORTIZED / RECOMPRESSED PROJECTION = OPEN
    UNIVERSAL P=NP = OPEN
