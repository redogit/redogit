# Fixed-B Additive BVE and the Exponent-Escalation Obstruction — 2026-09-26

**Program:** synchronized P vs NP proof program
**Predecessor:** `PNP_R5_PLUS1_ADDITIVE_BVE_2026-09-26.md`
**Status:** exact finite-ring closure + exact obstruction to naive universalization
**Claim ceiling:** not universal P=NP

## 1. Fixed additive BVE

For any fixed constant B>=0 define R5+B:

    exact DP eliminate v
    if cleaned successor clause count c' <= c+B.

Every successful step removes one variable.

There are at most n_0 such steps, so cumulative clause growth caused by R5+B is at most:

    B*n_0.

Therefore for every fixed B:

    c(F) <= c_0 + B*n_0

from this rule, and the normalization lifecycle remains polynomial.

Homeward is ordinary exact DP reconstruction.

Thus:

    EVERY FIXED ADDITIVE B
    IS A LEGITIMATE POLYNOMIAL NORMALIZATION RULE.

## 2. Immediate sigma=4 closure

At the R5+1+R6 fixed point with sigma=4, a minimum-degree variable has degree 6 and polarity profile:

    2+4
    3+3
    4+2.

Raw DP clause-growth bounds are:

    g(2,4)=8-6=2
    g(3,3)=9-6=3
    g(4,2)=2.

Therefore R5+3 eliminates every such degree-6 variable without needing any extra positive-balance redundancy.

Hence no R5+3 + R6 fixed point has sigma=4.

Together with earlier rings:

    sigma <=4 is closed by the polynomial normalization lifecycle using fixed B=3.

## 3. General finite-ring formula

For a variable with total degree d=p+q and p,q>=1, the maximum raw DP growth is

    g(p,q)=pq-p-q.

For fixed d, this is maximized at the most balanced polarity split:

    G(d)=floor(d^2/4)-d.

If R6 gives a variable of degree

    d <= nM(sigma),

then choosing a fixed constant

    B_sigma = G(nM(sigma))

is sufficient to eliminate some minimum-degree variable for every residual with that fixed surplus value sigma.

Therefore for every fixed K there exists a fixed constant

    B(K)=max_{1<=s<=K} G(nM(s))

such that R5+B(K) plus R6 closes every residual with

    sigma(F)<=K.

This is an exact finite-ring theorem.

## 4. Why this is not P=NP

The constants B(K) depend on the surplus ring K.

To obtain one universal polynomial algorithm we cannot choose a new algorithmic constant after seeing an unbounded K unless the resulting cumulative representation has one fixed polynomial exponent independent of the input.

A tempting rule is to let B grow polynomially with the current representation.

That is where the circularity appears.

Suppose the current clause envelope is C.

A low-degree variable may have

    d=O(sigma)<=O(C).

Exact DP on such a variable may create

    O(d^2)=O(C^2)

resolvents.

If we enlarge the permitted envelope from C to C^2, the next R6 degree guarantee is only bounded in the new surplus / clause scale, now potentially O(C^2).

The next unrestricted DP step may then require

    O(C^4),

then

    O(C^8),

and so on.

After t such exponent-doubling stages the naive envelope can become

    C^(2^t).

With t allowed to grow with n, this is not a fixed polynomial bound.

Thus:

    EACH LOCAL STEP IS POLYNOMIAL IN CURRENT SIZE
    !=
    TOTAL ALGORITHM POLYNOMIAL IN ORIGINAL INPUT SIZE.

This is the exact exponent-escalation obstruction.

## 5. What the universal climbing law must do

A universal proof cannot merely say:

    allow enough DP growth for the current ring.

It needs a global potential or amortization theorem that prevents the degree/growth scale from feeding back into itself.

Sufficient forms would include any theorem proving one of:

1. surplus never rises faster than a fixed function of the original input under the chosen projections;
2. cumulative DP growth is charged to a resource that decreases and has polynomial original mass;
3. generated resolvents collapse under positive-balance/circuit structure so actual growth is subquadratic enough to close a fixed recurrence;
4. one can project the low-degree variable into a shared carrier without materializing all pairwise resolvents;
5. the exponent of the representation bound does not increase with successive eliminations.

This is now the central edge.

## 6. Core / edge interpretation

The verified core contains:

    for every fixed K,
    surplus <=K is polynomially closable
    by a fixed additive BVE budget B(K).

The edge is:

    UNBOUNDED SURPLUS.

The missing bridge is not another finite surplus calculation.

It is:

    UNIFORMITY IN K.

In complexity language:

    FOR EACH FIXED K, POLYNOMIAL
    !=
    ONE POLYNOMIAL FOR ALL K.

This distinction must remain explicit.

## 7. Next one-degree obligation

Do not spend the next step proving sigma=5,6,... separately.

Attack the feedback relation:

    DP GROWTH
    -> DEFICIENCY/SURPLUS CHANGE
    -> NEXT GUARANTEED DEGREE
    -> NEXT DP GROWTH.

Find a potential Psi whose initial value is polynomially bounded and whose decrease pays for generated projection structure.

Candidate resources to test:

- eliminated variable count;
- original clause-occurrence mass;
- positive-balance nullity / deficiency;
- circuit-cover dimension;
- signed cross-circuit incidence rank;
- reusable resolvent DAG size rather than materialized clause count.

The theorem needed is a uniform amortization theorem.

## 8. Claim ceiling

    EVERY FIXED SURPLUS RING K POLYNOMIALLY CLOSABLE = EXACT
    SIGMA<=4 CLOSED WITH B=3 = EXACT
    NAIVE DYNAMIC-B UNIVERSALIZATION = ASH
    UNIFORM AMORTIZED PROJECTION = OPEN
    UNIVERSAL P=NP = OPEN

    POINTWISE POLYNOMIAL != UNIFORM POLYNOMIAL
    LOCAL POLYTIME != GLOBAL POLYTIME
    EDGE-BY-EDGE FINITE CLOSURE != UNIVERSAL CLIMB
