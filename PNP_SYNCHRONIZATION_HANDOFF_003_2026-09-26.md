# P vs NP Synchronization Handoff 003 — Minimal Seam Pair / Correction-Set Object

**Status:** CURRENT BOUNDED OUTWARD SYNCHRONIZATION  
**Mathematical authority:** `redogit/redogit`  
**Method/routing authority:** `redogit/conscience64/research/cooperative-field/`  
**Tooling authority:** `redogit/DnD`

## Consequential mathematical delta

New target-local successors:

- `PNP_MINIMAL_LINEAR_BOOLEAN_SEAM_PAIR_2026-09-26.md`
- `PNP_MINIMAL_LINEAR_BOOLEAN_SEAM_PAIR_CHECK_2026-09-26.py`
- `PNP_BOOLEAN_SHEAR_FIBER_THEOREM_2026-09-26.md`
- `PNP_BOUNDARY_RESCUE_CORRECTION_SET_SEAM_2026-09-26.md`

## Exact separation

Smallest fully parent-valid witness under the declared seam contract:

- 3 variables;
- 4 clauses;
- same minimum-surplus tight block;
- same exact boundary residual map rho;
- same residual rank;
- same full column rank;
- same strictly positive global balance;
- same outside balancing clause;
- different exact Boolean interface;
- opposite parent SAT status.

Therefore:

    LINEAR-SEAM EQUALITY
    !=
    BOOLEAN-INTERFACE EQUALITY.

## Hidden degree

For fixed full-column-rank A_V:

    rho_E = rho_E'
    iff
    E' - E = A_V T

for a unique shear coordinate T.

The linear seam sees the attachment matrix only modulo col(A_V).

The Boolean seam also needs the discrete clausewise representative.

Operational meaning:

    LINEAR CANCELLATION
    !=
    BOOLEAN VARIABLE OWNERSHIP / COMPLEMENT COUPLING.

## Minimal witness is normalizer-visible

The first separating shear copies an internal variable sign-column onto the boundary.

That makes all resolvents on that variable tautological.

Therefore BCE / bounded DP consumes the witness.

So the current hard-core question is not whether rho fails in general—it does.

It is:

    DOES A BOOLEAN-CHANGING,
    NORMALIZATION-IRREDUCIBLE
    HARD SHEAR EXIST?

## Correction-set seam

For tight restriction G and boundary assignment alpha, let R(alpha) be the touched clauses externally satisfied/rescued by alpha.

Then:

    interface(alpha)=SAT
    iff
    G \ R(alpha) is SAT.

If G is UNSAT:

    interface(alpha)=SAT
    iff
    R(alpha) is a correction set
    iff
    R(alpha) hits every MUS of G.

So the exact Boolean seam is:

    BOUNDARY ASSIGNMENT
    -> CLAUSE-RESCUE OWNERSHIP
    -> CORRECTION SET
    -> MUS TRANSVERSAL.

## Positive-circuit convergence

Within the signed-matrix setting:

    MU(1)
    =
    UNSAT POSITIVE-BALANCE CIRCUIT.

For higher-deficiency MUSes, every proper positive circuit is SAT by minimality, so the obstruction is:

    GLOBAL INCOMPATIBILITY
    AMONG LOCALLY SAT POSITIVE CIRCUITS.

Thus the interface and positive-circuit research lines now meet on the MUS/correction-set object.

## Current nearest edge

> Can the MUS-transversal predicate of a fully normalized tight block be represented and queried in polynomial work from its positive-circuit compatibility structure without enumerating all MUSes or correction sets?

Parallel sub-obligation:

> Is the hard-shear set empty after full normalization?

## Claim ceiling

    MINIMAL rho-IDENTICAL / BOOLEAN-DIFFERENT PAIR = EXACT
    LINEAR FIBER THEOREM = EXACT
    CORRECTION-SET INTERFACE THEOREM = EXACT
    FIRST WITNESS NORMALIZER-VISIBLE = EXACT
    HARD-SHEAR EMPTINESS = OPEN
    POLYNOMIAL MUS SIGNATURE = OPEN
    UNIVERSAL P=NP = OPEN

    GENERATE != VERIFY != ADMIT
    METHOD TRANSFER != EVIDENCE TRANSFER
