# R5+1 Additive Bounded Variable Elimination — 2026-09-26

**Program:** synchronized P vs NP proof program  
**Predecessor:** `PNP_R5_R6_SURPLUS_FLOOR_2X3_CROWN_2026-09-26.md`  
**Status:** admitted polynomial normalization strengthening  
**Claim ceiling:** not universal P=NP

## 1. Observation

The previous R5 guard admitted exact Davis-Putnam elimination only when the cleaned clause count did not increase.

That guard is stronger than polynomial lifecycle preservation requires.

A successful DP elimination always removes one variable. Therefore at most n_0 such eliminations can occur.

Allowing a constant additive clause increase per eliminated variable still keeps the entire representation polynomial.

This is standard bounded-variable-elimination semantics; practical SAT preprocessing also permits positive clause-growth limits. The proof here is the explicit lifecycle bound, not solver practice.

## 2. New rule

Replace the zero-growth-only R5 by:

    R5+1 ADDITIVE BOUNDED DP

For a candidate variable v:

1. construct all exact non-tautological v-resolvents;
2. remove the v-parent clauses;
3. canonical-clean, deduplicate, and subsume;
4. let c be predecessor clause count and c' successor clause count;
5. admit elimination when

       c' <= c + 1.

Store the usual DP Homeward reconstruction receipt.

After success restart normalization at R0.

## 3. Polynomial lifecycle proof

Let n_0,c_0 be the original input counts.

Every R5+1 success removes exactly one variable, so there are at most n_0 successful R5+1 steps.

Each increases the clause count by at most one.

Other admitted normalization rules either remove variables/clauses or obey their existing polynomial-size guards.

Therefore throughout the lifecycle:

    n(F) <= n_0
    c(F) <= c_0 + n_0

under the R5+1 contribution.

Every clause has length at most n_0, so literal storage remains polynomial.

Candidate DP construction is polynomial in the current polynomial-size representation: at most c(F)^2 parent pairs per candidate variable.

The number of successful variable eliminations is at most n_0; clause-removal operations remain bounded by the polynomial clause envelope. Hence total discovery/execution and trace storage remain polynomial.

## 4. Homeward

Exact DP elimination is equisatisfiable and supports ordinary model reconstruction by retaining the eliminated parent clauses / reconstruction stack.

Thus R5+1 preserves the same decision and Homeward obligations as the previous R5, with one additional clause of permitted local representation debt.

    +1 REPRESENTATION DEBT
    !=
    BOOLEAN BRANCH.

## 5. Consequence for the tight 2x3 crown

The predecessor theorem showed that an R5-zero-growth + R6 fixed point with surplus 3 contains a degree-5 variable with polarity profile 2+3 and exact cleaned DP growth +1.

R5+1 eliminates exactly that variable.

Therefore no unresolved R5+1 + R6 fixed point can have surplus 3.

Together with the previous surplus floor:

    sigma(F) >= 4

for every nonterminal residual after R5+1 and R6 saturation.

Hence:

    SURPLUS 1 = CLOSED
    SURPLUS 2 = CLOSED
    SURPLUS 3 = CLOSED.

No positive-balance amortization theorem is needed for the unique +1 crown debt.

## 6. New R5+1 degree floor

At an R5+1 fixed point, any variable with raw DP growth at most +1 is eliminable even before tautology/subsumption savings.

For polarity counts p,q>=1, raw clause-growth bound is:

    g(p,q) = p*q - p - q.

Profiles eliminated automatically include:

    1 + q   for every q
    2 + 2   growth 0
    2 + 3   growth 1
    3 + 2   growth 1.

Thus every surviving variable has:

    vd(v) >= 6.

For degree 6 the only potentially surviving profiles are:

    2+4  raw growth 2
    3+3  raw growth 3
    4+2  raw growth 2.

## 7. New first unresolved surplus

R6 saturation gives:

    muvd(F) <= nM(sigma(F)).

At an R5+1 fixed point:

    muvd(F) >= 6.

Since:

    nM(3)=5
    nM(4)=6,

the first possible unresolved surplus is now exactly:

    sigma(F)=4.

If sigma=4 then some variable has degree exactly 6 and polarity profile in:

    {2+4, 3+3, 4+2}.

This is the next local Object.

## 8. Why not silently increase the growth bound forever

Any fixed additive constant B remains polynomial because at most n_0 variables are eliminated, and it can consume additional finite surplus cells.

But:

    FIXED B FOR EACH DESIRED CELL
    !=
    ONE UNIVERSAL POLYNOMIAL RULE.

Increasing B without a global representation-growth proof can reproduce ordinary DP explosion.

Any future relaxation must carry an explicit global potential/budget proving that cumulative representation size remains polynomial.

## 9. Next one-degree obligation

At sigma=4, test the degree-6 profiles separately:

    2+4
    3+3
    4+2.

Ask whether existing R2-R4 or positive-balance circuit structure forces enough tautology, duplication, subsumption, decomposition, or simultaneous removal to reduce cleaned DP growth to <=1.

Equivalently:

    CAN THE CURRENT STRUCTURE PAY
    THE REMAINING +2 / +3 LOCAL DP DEBT?

If not, the next candidate is a globally charged additive-growth budget, not an unbounded local relaxation.

## 10. Claim ceiling

    R5+1 POLYNOMIAL LIFECYCLE = EXACT
    SURPLUS <=3 CLOSED = EXACT
    SIGMA=4 DEGREE-6 PROFILE = EXACT
    UNIVERSAL ADDITIVE BVE CLOSURE = OPEN
    UNIVERSAL P=NP = OPEN

    SMALL POSITIVE GROWTH != EXPONENTIAL BLOWUP
    UNCHARGED REPEATED GROWTH != ADMISSIBLE
    GENERATE != VERIFY != ADMIT
