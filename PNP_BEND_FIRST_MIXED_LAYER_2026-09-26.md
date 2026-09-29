# BEND: Tight-Block Seam / First Mixed Layer — 2026-09-26

**Program:** synchronized P vs NP proof program  
**Method:** BEND = direct pressure from multiple angles to expose what the edge is made of  
**Predecessor:** `PNP_TIGHT_BLOCK_INTERFACE_LIFT_2026-09-26.md`  
**Status:** structural carrier + exact local statements; universal bound open  
**Claim ceiling:** not universal P=NP

## 1. Edge under pressure

Let V be a minimum-surplus variable block of parent CNF F.

For each touched parent clause C:

    C = D_C union E_C

where D_C uses variables in V and E_C uses variables outside V.

The tight restriction:

    G=F[V]={D_C}

is a structural probe.

The exact parent-safe projection is:

    I_V = exists V . conjunction_{C touches V} C.

General CNF forgetting can have exponential output and deciding polynomially bounded forgetting is hard in general. Therefore:

    MATERIALIZE I_V
    is not an admissible universal assumption.

The seam is what lies between G and I_V.

## 2. Outside-sign conflict graph

Define a graph X_V on the touched source clauses.

For source clauses C_i,C_j put an edge when their outside remainders contain a complementary pair:

    exists outside variable z:
      z in E_i
      and
      -z in E_j

or vice versa.

Interpretation:

    nonedge
    -> the two outside remainders are sign-compatible;

    edge
    -> combining both source supports may introduce an outside tautology.

This graph is not a SAT solver. It records where an internal proof can lose parent information when lifted.

## 3. Exact clean-support lift

Let P be any resolution derivation in G using only pivots in V.

Let Leaves(P) be its source clauses.

If Leaves(P) is an independent set of X_V, then the union of all outside remainders used by P contains no complementary literal pair.

Replay P on the corresponding parent clauses.

The final lifted interface clause is non-tautological.

Therefore:

    INTERNAL DERIVATION
    +
    OUTSIDE-CONFLICT-FREE SOURCE SUPPORT
    ->
    USEFUL PARENT-LIFTABLE CLAUSE.

This is exact.

The converse is not claimed: a proof may still lift usefully despite conflicts because some outside literals can disappear through subsumption or other proof structure.

## 4. What tautology means here

A tautological lift is not merely "resolution failed."

It says:

    the internal contradiction depended on strengthening
    clauses whose outside alternatives point in incompatible directions.

Example:

    {x,a}
    {-x,-a}

restricts to:

    {x}
    {-x}

but the lifted result is:

    {a,-a}.

The seam is the relation:

    INTERNAL CONTRADICTION
    x
    OUTSIDE ALTERNATIVES.

## 5. Relation to interpolation

Resolution interpolation studies exactly the broader phenomenon of eliminating local variables while retaining a relation on shared variables.

Known feasible-interpolation results show that a small resolution proof can yield a polynomial-size interpolation circuit in appropriate settings.

Known lower bounds and forgetting results show that:

    SMALL / EASY INTERNAL PROOF
    !=
    UNIVERSALLY SMALL INTERFACE REPRESENTATION.

So interpolation is a valid comparison carrier, not a free closure theorem.

## 6. First mixed layer

For a chosen internal resolution DAG P, propagate source-origin annotations upward.

A node is:

    CLEAN
    if its accumulated outside annotation is sign-compatible;

    MIXED
    when it is the first node on a derivation path whose accumulated outside support contains a complementary literal pair.

Define:

    M1(P) = set of first mixed nodes.

These are the exact seams where a clean parent lift first becomes obstructed.

Everything below M1(P) can be lifted as non-tautological interface clauses.

Everything above it has already crossed an outside-sign conflict and must be represented differently or repaired.

Thus instead of compiling the full existential projection, candidate carrier:

    FIRST_MIXED_LAYER {
      clean lifted clauses below seam,
      mixed-node source provenance,
      outside complementary pairs causing each mix,
      internal pivot relation,
      positive-balance / surplus coordinates of the involved source clauses
    }.

## 7. Why this is a BEND carrier

Pressure angles:

A. Internal SAT / resolution:
    what contradiction exists in G?

B. Parent lift:
    what remains valid when deleted literals are restored?

C. Outside sign pressure:
    exactly which outside alternatives make a lift tautological?

D. Forgetting complexity:
    does exact interface materialization explode?

E. Interpolation:
    can proof structure encode the interface more compactly than CNF clauses?

F. Positive balance:
    do source clauses at the first mixed layer satisfy extra signed dependencies?

G. Surplus / Hall expansion:
    does high tight-block expansion constrain the number or geometry of first mixes?

The seam is admitted only if it survives these pressures.

## 8. Immediate negative boundary

Do not assume:

    |M1(P)| is polynomially small

merely because:

    G has low maximum deficiency,
    or G has a short proof,
    or each positive circuit is locally tractable.

Proof/interpolant size can separate, and general forgetting can be exponential.

A bound on M1 must come from the special tight-block + positive-balance structure.

## 9. Cheapest counterprobe

Construct/search small normalized parent formulas with a minimum-surplus block V such that:

- G=F[V] is UNSAT;
- G is full-column-rank and strictly positively balanced;
- G has its positive-circuit cover;
- every short internal refutation encounters many distinct first mixed conflicts;
- the exact parent interface relation has many prime implicates / high representation complexity.

If such examples scale, first-mixed-layer compression is Ash.

If the number/structure of first mixed conflicts is bounded by k=surplus or another polynomial resource, extract the uniform theorem.

## 10. Next theorem target

Let k=sigma(F)=dim ker(M_G^T).

Test:

    DOES THERE EXIST AN INTERNAL REFUTATION P
    FOR WHICH
      complexity(M1(P))
    <=
      poly(k, input size)

AND whose clean lifted clauses plus a polynomial carrier for M1(P)
represent enough of the parent interface to make exact progress?

Stronger candidate:

    complexity(M1(P)) <= O(k)

or

    every first mixed conflict can be charged injectively
    to a positive-balance circuit / nullspace degree.

No such bound is currently admitted.

## 11. Claim ceiling

    OUTSIDE-CONFLICT GRAPH = EXACT DEFINITION
    CONFLICT-FREE SUPPORT -> NONTAUTOLOGICAL LIFT = EXACT
    FIRST MIXED LAYER = EXACT PROOF CARRIER
    POLYNOMIAL FIRST-MIXED BOUND = OPEN
    BALANCE-CHARGED MIXED LAYER = OPEN
    UNIVERSAL P=NP = OPEN

    BEND != FORCE
    PRESSURE REVEALS SEAM
    SEAM CARRIER != SOLUTION
    GENERATE != VERIFY != ADMIT
