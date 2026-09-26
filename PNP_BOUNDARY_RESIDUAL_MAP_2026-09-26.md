# Boundary Residual Map — What Lives Between Internal Balance and Parent Lift — 2026-09-26

**Program:** synchronized P vs NP proof program  
**Predecessor:** `PNP_BEND_FIRST_MIXED_LAYER_2026-09-26.md`  
**Status:** exact linear seam definition + counterprobe  
**Claim ceiling:** not universal P=NP

## 1. Counterprobe

Internal positive-balance circuit minimality does not prevent outside-sign conflict.

Small exact examples exist with two opposite internal signed rows:

    r1 = -r2

forming a support-minimal positive circuit, while their parent outside remainders contain opposite literals of the same boundary variable.

Therefore:

    INTERNAL POSITIVE CIRCUIT
    !=
    CLEAN PARENT LIFT.

The lost information is precisely in the deleted outside coordinates.

## 2. Put back only the seam coordinates

For a tight variable block V, let R be its touched clauses.

Partition the variables occurring in those parent clauses into:

    V = internal variables
    B = boundary variables outside V that occur in R.

Let the parent signed clause matrix restricted to touched clauses be:

    A = [ A_V | A_B ].

The tight restriction uses only:

    A_V.

The parent interface is controlled by both blocks.

## 3. Internal balance space

Define:

    K_V = ker(A_V^T).

Because the tight block inherits strict positive balance and has thickness k:

    dim K_V = k

and K_V contains a strictly positive vector.

Every z in K_V is an internal cancellation among touched clause rows.

But z need not cancel boundary coordinates.

## 4. Boundary residual map

Define the linear map:

    rho_B : K_V -> R^B

by:

    rho_B(z) = A_B^T z.

Interpretation:

    A_V^T z = 0
    says the weighted clause combination cancels every internal coordinate.

    A_B^T z
    is exactly the residual signed pressure left on the parent boundary.

Thus rho_B records what an internal balance becomes when lifted back toward the parent.

This is a precise linear Object living between:

    INTERNAL BALANCE
and
    FULL PARENT BALANCE.

## 5. Parent balance kernel

The balances that cancel both internal and boundary coordinates are:

    ker(rho_B)
      =
    ker(A^T) intersect K_V.

So:

    dim image(rho_B)
      =
    dim K_V - dim ker(rho_B).

Call:

    beta(V) = rank(rho_B).

This is the number of independent boundary residual directions carried by internal balance dependencies.

Bounds:

    0 <= beta(V) <= min(k, |B|).

## 6. Exact meanings

### beta(V)=0

Every internal balance also cancels the boundary matrix linearly.

This does not by itself prove SAT/UNSAT or a compact Boolean projection, but it means the internal balance carrier loses no linear cancellation when restored to the touched parent matrix.

### beta(V)>0

There are internal balance directions whose cancellation fails exactly on boundary coordinates.

These are linear seams: directions invisible in the tight restriction but visible in the parent.

Outside-sign conflict can occur here.

## 7. Relation to first mixed layer

The first mixed layer is Boolean/proof-theoretic.

rho_B is linear/algebraic.

They are independent pressures on the same seam.

Candidate bridge question:

> Does small beta(V) imply a resolution/interpolation/interface carrier of complexity polynomial in beta(V), k, and input size?

Counterquestion:

> Can beta(V)=1 while the exact Boolean interface requires exponential representation?

The second is the cheapest serious falsification route.

## 8. Relation to the global parent balance

The fully normalized parent has y>0 with:

    M(F)^T y=0.

Restrict y to touched clauses R.

For internal columns V:

    A_V^T y_R=0.

For boundary columns B, clauses outside R may also contain those variables, so generally:

    A_B^T y_R
    =
    - M[outside R,B]^T y_outside.

Thus the boundary residual of the inherited positive vector is exactly balanced by the rest of the parent.

This gives a conservation law across the seam:

    TIGHT-BLOCK BOUNDARY PRESSURE
    +
    OUTSIDE-PARENT BOUNDARY PRESSURE
    =
    0.

That is a genuine cross-coordinate relation absent from the restricted block alone.

## 9. New BEND pressures

Apply simultaneously:

1. Boolean proof pressure:
       first mixed resolution layer.

2. Linear pressure:
       beta(V)=rank(rho_B).

3. Sign pressure:
       complementary outside literals.

4. Hall pressure:
       k=sigma(F)=dim K_V.

5. Global conservation:
       parent positive balance cancels block residual against outside residual.

6. Forgetting/interpolation pressure:
       exact Boolean interface representation size.

The seam is understood only where these agree or their conflict is explained.

## 10. Next counterprobe

Search for normalized/tight parent instances with:

    small beta(V)
    but
    large Boolean interface complexity,

and conversely:

    large beta(V)
    but
    simple interface.

If either separation is strong, beta alone is not the missing carrier.

If Boolean interface complexity is controlled by beta together with sign-conflict structure, formulate the joint theorem.

## 11. Claim ceiling

    INTERNAL CIRCUIT DOES NOT CONTROL OUTSIDE SIGNS = EXACT COUNTERPROBE
    BOUNDARY RESIDUAL MAP = EXACT DEFINITION
    beta(V) <= min(k,|B|) = EXACT
    GLOBAL POSITIVE-BALANCE CONSERVATION ACROSS SEAM = EXACT
    beta CONTROLS BOOLEAN INTERFACE = OPEN
    UNIVERSAL P=NP = OPEN

    LOST COORDINATE != LOST OBJECT
    PUT BACK THE SEAM, NOT THE WHOLE WORLD
    LINEAR RESIDUAL != BOOLEAN PROJECTION
