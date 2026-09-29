# R5 + R6 Surplus Floor and Tight 2x3 DP Crown — 2026-09-26

**Program:** synchronized P vs NP proof program  
**Predecessor:** `PNP_SURPLUS_AUTARKY_OBJECT_REDUCTION_2026-09-26.md`  
**Status:** scoped exact theorem  
**Claim ceiling:** not universal P=NP

## 1. Setup

Let F be a nonterminal residual after the deterministic normalization lifecycle including:

- R0 cleanup/unit consequences;
- R1 linear-autarky reduction;
- R2 certified cofactor dominance;
- R3 blocked-clause elimination;
- R4 certified functional/gate elimination;
- R5 non-increasing Davis-Putnam elimination;
- R6 surplus/non-Mersenne autarky-object reduction.

Assume F still has variables.

Let for variable v:

    p(v) = positive literal degree
    q(v) = negative literal degree
    vd(v)=p(v)+q(v).

R6 saturation gives:

    muvd(F) <= nM(sigma(F)),

where nM is the non-Mersenne sequence

    2,4,5,6,8,...

for sigma=1,2,3,4,5,...

## 2. R5 degree floor

### Theorem

At an R5 fixed point every surviving variable satisfies

    p(v)>=2,
    q(v)>=2,

and not both p(v)=q(v)=2.

Hence

    vd(v)>=5

for every surviving variable.

### Proof

If p=0 or q=0, the variable is pure and earlier cleanup/autarky rules remove it.

If p=1 and q=q0>=1, exact DP elimination removes p+q0=q0+1 parent clauses and produces at most p*q0=q0 non-tautological resolvents. Before even accounting for duplicate resolvents, tautologies, existing clauses, or subsumption, clause count does not increase. Therefore R5 applies. Symmetrically for q=1.

If p=q=2, exact DP removes four parent clauses and produces at most four resolvents. Again the clause count cannot increase, so R5 applies.

Thus a surviving R5-fixed variable must have p,q>=2 and p+q>=5.

QED.

## 3. Surplus floor after R6

At the joint R5+R6 fixed point:

    5 <= muvd(F) <= nM(sigma(F)).

But

    nM(1)=2
    nM(2)=4.

Therefore:

    sigma(F) >= 3.

### Consequence

The entire matching-lean surplus-1 and surplus-2 cells are consumed by the current polynomial normalization lifecycle.

This is stronger than merely knowing that low-surplus formulas contain low-degree variables.

    R5 + R6
    ->
    NO UNRESOLVED RESIDUAL WITH SURPLUS <= 2.

## 4. Exact sigma=3 boundary

If sigma(F)=3, then

    nM(3)=5.

Together with the R5 degree floor:

    muvd(F)=5.

So some variable v has exactly five occurrences.

Since p,q>=2, its polarity profile is exactly:

    {p,q}={2,3}.

Call the two clauses on one sign P1,P2 and the three on the opposite sign N1,N2,N3.

## 5. Tight 2x3 DP crown theorem

Exact DP on v removes five parent clauses and has at most

    2*3=6

candidate resolvents.

R5 does not apply, so after tautology deletion, deduplication, canonical cleanup, and subsumption the resulting clause count must be strictly greater than the predecessor clause count.

The only possible raw increase is +1.

Therefore all six candidate resolvents must survive independently.

Thus at an R5 fixed point with sigma=3, the selected degree-5 variable satisfies:

1. every Pi/Nj pair has a non-tautological v-resolvent;
2. all six resolvents are distinct;
3. no generated resolvent is removed as a duplicate of an existing unaffected clause;
4. no generated resolvent is subsumed by an unaffected or generated clause under canonical cleanup;
5. no generated resolvent subsumes another in a way that lowers the cleaned count;
6. exact DP increases the cleaned clause count by exactly one.

Call this local Object:

    TIGHT_2x3_DP_CROWN.

## 6. Literal-compatibility consequence

A v-resolvent of Pi and Nj is tautological exactly when, after removing v and not-v, the two parent remainders contain some complementary literal pair.

Since all six resolvents must be non-tautological:

    for every i in {1,2}
    and j in {1,2,3},

    (Pi \ {v}) and (Nj \ {-v})
    contain no complementary literal pair.

So the two sign-sides of the crown are pairwise sign-compatible away from v.

This is a stronger local structural invariant than merely:

    vd(v)=5.

## 7. Positive-balance interaction

In the linearly-lean residual there is y>0 with

    M(F)^T y=0.

For the crown variable v this gives the exact weighted balance equation

    sum_{Pi side} y_C
    =
    sum_{Nj side} y_C.

Every positive balance circuit containing any v-parent clause must contain at least one parent from each polarity, because a nonnegative dependence cannot cancel the v-coordinate otherwise.

Therefore the next carrier for sigma=3 is not an arbitrary variable branch. It is:

    TIGHT_2x3_DP_CROWN
    +
    POSITIVE-CIRCUIT INCIDENCE THROUGH ITS FIVE PARENTS
    +
    EXACT WEIGHT BALANCE.

## 8. Burned target

The stronger conjecture

    R6-SATURATED + POSITIVE BALANCE
    -> SINGULAR VARIABLE

is not supported.

General matching-lean deficiency-1 literature already contains star-free examples with no singular variables, and finite balanced searches also produce nonsingular linearly-lean examples before later normalization rules fire.

What survives is the stronger fixed-point theorem above:

    R5 FIXED POINT -> DEGREE >=5.

## 9. Next one-degree obligation

For sigma=3 only, determine whether every TIGHT_2x3_DP_CROWN in a fully normalized strict-positive-balance residual must admit one of:

- R2 dominance;
- R3 blocked-clause consequence after a bounded derived step;
- R4 functional relation;
- a positive-circuit separator/decomposition through the five parent clauses;
- a reusable projection whose +1 DP growth is amortized/cancelled by a certified simultaneous removal;
- or an exact negative certificate.

The key local fact is that the raw DP excess is only one clause.

So the new quantitative question is:

    CAN STRICT POSITIVE BALANCE PAY FOR THE UNIQUE +1
    WITHOUT BRANCHING?

If yes, surplus=3 also closes.

## 10. Claim ceiling

    SURPLUS <=2 CLOSED BY R5+R6 = EXACT
    SIGMA=3 IMPLIES TIGHT 2x3 DP CROWN = EXACT
    POSITIVE BALANCE PAYS FOR +1 = OPEN
    UNIVERSAL P=NP = OPEN

    LOW DEGREE != FREE DEGREE
    +1 DP GROWTH != POLYNOMIAL CLOSURE BY ITSELF
    GENERATE != VERIFY != ADMIT
