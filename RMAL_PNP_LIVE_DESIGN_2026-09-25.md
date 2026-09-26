# RMAL P vs NP — Live Design — 2026-09-25

> Start with [TERMS FIRST](RMAL_RESEARCH_ORIENTATION_2026-09-25.md). This page is the current design, not the dictionary.

## TERMS I AM USING HERE

```text
OBJECT        := the thing I am preserving / reasoning about
OBLIGATION    := what the result actually has to satisfy
RESULT        := what came out
METHOD        := repeatable lawful path + checks + cost
CARRIER       := what currently holds / moves what matters
TRACE         := ordered record of what changed and what was checked
REMAINDER     := exact unresolved part after admitted work
HOMEWARD      := way back to original obligation / witness / source
CLAIM CEILING := strongest claim current evidence supports
```

```text
RESULT != METHOD != PROOF != EXPLANATION
MAKING THE DOUGHNUTS != KNOWING HOW TO MAKE THE DOUGHNUTS
```

The design below is mainly the second Object: preserving enough method, receipts, cost, and reconstruction that the result can be earned again.

## THE THING I AM TRYING TO PROVE

I am not trying to prove that a particular SAT solver is fast on a pile of cases.

I am trying to build an exact uniform process where every admissible unresolved state does one of three lawful things:

    CLOSE POSITIVE
    CLOSE NEGATIVE
    OR
    MOVE TO A STRICTLY SMALLER / CHEAPER EXACT REMAINDER

and where the **entire lifecycle cost** is polynomial:

    recognize
    select
    transform
    verify
    store
    reconstruct

The proof obligation is not allowed to hide exponential work in the carrier.

## THE DOUGHNUT SPLIT

    MAKING THE DOUGHNUTS
    !=
    KNOWING HOW TO MAKE THE DOUGHNUTS

For this project:

    RESULT
    !=
    ALGORITHM
    !=
    PROOF OF THE ALGORITHM
    !=
    EXPLANATION OF WHY THE ALGORITHM EXISTS

The current normalization theorem is specifically the **knowing how it was made** layer.

## CURRENT EXECUTION SHAPE

    ORIGINAL OBLIGATION
    -> FOUR-ID SEMANTIC BINDING
    -> EXACT NORMALIZATION
    -> CERTIFIED TRACTABLE TERMINAL, if one applies
    -> OTHERWISE: EXPLICIT RESIDUAL
    -> ONE NEW CONSEQUENTIAL DEGREE
    -> VERIFY
    -> HOMEWARD
    -> CONTINUE

## EXACT NORMALIZATION — CURRENT ORDER

Use stable IDs. Apply the first exact rule that is admitted. After any change, restart.

    R0  exact cleanup / unit consequences
    R1  maximal linear-autarky reduction
    R2  signed cofactor dominance
    R3  blocked-clause elimination
    R4  certified functional-variable / gate elimination
    R5  non-increasing Davis-Putnam merge

Then test existing certified terminals:

    2-SAT
    Horn
    dual-Horn
    affine / GF(2), when recognized
    beta-acyclic Choice-CNF
    hierarchical forbidden-pair path
    logarithmic crossing-defect path
    skew-symmetric forbidden-pair path
    logarithmic maximal deficiency
    binary-cluster / log-cluster-defect carriers
    other explicitly admitted scoped terminals
    log conformal-defect hitting / exact model-count terminal
    log nonclash-degeneracy / conformal-clique inclusion-exclusion terminal

## NORMALIZATION CLOSURE THEOREM

Let

    mu(F) = variables(F) + clauses(F).

Every successful normalization step strictly decreases mu.

All admitted rules have polynomial discovery / verification cost under their stated guards.

The guarded representation never leaves a polynomial size envelope.

Therefore:

    number of successful steps <= n_0 + c_0

and the complete normalization lifecycle is polynomial.

Each step stores a polynomial-size proof / reconstruction receipt.

Reverse replay of those receipts reconstructs the original witness or validates the negative direction.

### What that closes

    P5/P6 LOCAL NORMALIZATION LIFECYCLE: CLOSED FOR THE DECLARED RULE SET.

### What that does not close

    NORMALIZATION != SAT SOLVER
    LOCAL POLYNOMIAL WORK != GLOBAL POLYNOMIAL COVER
    P5/P6 != P7

## CURRENT HARD CORE AFTER NORMALIZATION

A residual that survives the present exact suite can be required to have:

    NO LINEAR AUTARKY
    NO CERTIFIED COFACTOR DOMINANCE
    NO BLOCKED CLAUSE
    NO ADMISSIBLE FUNCTIONAL VARIABLE
    NO NON-INCREASING DP VARIABLE
    NO ALREADY-CERTIFIED TRACTABLE TERMINAL

and, in the linearly-lean matrix carrier:

    full column rank
    strictly positive clause-balance vector y
    M^T y = 0
    deficiency = dimension of left-nullspace

If deficiency is logarithmic, the known exact deficiency algorithm closes it polynomially.

The live remainder is therefore the **high-deficiency, linearly-lean, projection-growth-positive fixed point**.

That is the next proof Object.

## CURRENT CONDENSED WISDOM

The long normalization proof compresses to:

    DON'T BRANCH ON A DEGREE
    UNTIL I HAVE FAILED TO PROVE THAT THE DEGREE IS:

        REDUNDANT,
        DOMINATED,
        FUNCTIONALLY DETERMINED,
        LOCALLY SATISFIED,
        OR CHEAPLY PROJECTABLE.

This rule is only useful because I can unfold it back into the exact mechanisms and receipts that earned it.

## NEXT DEGREE

The remaining exact structure that is present but not yet fully consumed is the positive clause-balance / left-nullspace carrier.

Do not call it UNSAT.

Do not call it proof of satisfiability.

It is structural evidence:

    POSITIVE BALANCE != UNSAT
    HIGH DEFICIENCY != HARDNESS CERTIFICATE

The next job is to determine whether that balance space yields an exact polynomial:

    reduction,
    decomposition,
    dominance relation,
    reusable projected consequence,
    or negative certificate

without recreating the removed Boolean degree under a new name.

## LOG CONFORMAL-DEFECT / HITTING TERMINAL

For the clause-column sign pattern A=M(F)^T, two columns are conformal exactly when the corresponding clauses do not clash.

Build the clause nonclash graph Q_F and find a vertex cover Z.

Then:

    F \ Z

is hitting.

If

    |Z| = O(log N_input),

retain Z as an exception carrier and evaluate the formula exactly by inclusion-exclusion over exceptional clauses. Every inclusion-exclusion term falsifies a subset of Z, producing a partial assignment; restricting the hitting core by that assignment leaves a hitting formula, whose exact model count is

    2^N - sum_C 2^(N-|C|).

This yields exact SAT / UNSAT and exact model count in polynomial total work under the logarithmic guard. A positive count reconstructs a witness by self-reduction; a zero count carries an exact arithmetic receipt.

This terminal is the qualitative-matrix translation of a tight-pattern neighborhood:

    TIGHT / HITTING
    +
    LOG CONFORMAL DEFECT
    ->
    EXACT POLYNOMIAL TERMINAL.

It does not close formulas whose minimum useful conformal-defect cover is superlogarithmic.

## NONCLASH-CLIQUE INCLUSION-EXCLUSION TERMINAL

The qualitative-matrix carrier is broader than the hitting / vertex-cover special case.

Let Q_F be the clause nonclash graph:

    C--D
    iff
    C and D contain no complementary literal pair.

Equivalently Q_F is the conformality graph of clause columns of A=M(F)^T.

For every nonempty set T of clauses:

    all clauses in T can be falsified simultaneously
    iff
    T is a clique of Q_F.

Therefore:

    #SAT(F)
      =
    2^n
      +
    sum_{nonempty clique T of Q_F}
        (-1)^|T| 2^(n-|V(T)|).

If Q_F has degeneracy d, a degeneracy ordering enumerates all cliques through at most

    m 2^d

candidate subsets.

Hence:

    d = O(log N_input)
    ->
    exact polynomial #SAT / SAT terminal.

Hitting is d=0.

For Homeward reconstruction, do not rebuild Q_F after partial assignments. Reuse the original clique list and intersect each original falsifying subcube with the partial assignment. This prevents the carrier guard from silently worsening during self-reduction.

The next qualitative residual therefore has superlogarithmic nonclash/conformality degeneracy.

## CLAIM CEILING

    ACTIVE PROOF PROGRAM
    SCOPED EXACT THEOREMS: YES
    POLYNOMIAL NORMALIZATION LIFECYCLE: YES
    UNIVERSAL P=NP PROOF: NOT ESTABLISHED

## SOURCE OBJECTS

- [Terms-first orientation](RMAL_RESEARCH_ORIENTATION_2026-09-25.md)
- [Live carrier/proof notebook](PNP_SIGNED_BINARY_CLUSTER_CARRIER_2026-09-25.md)
- [Profile checkpoint](README.md)


## POSITIVE BALANCE-CIRCUIT CARRIER

On the normalized linearly-lean residual:

    rank(M)=n
    y>0
    M^T y=0
    k = deficiency = dim ker(M^T)

the positive balance vector can be decomposed into at most k support-minimal positive row-dependency circuits.

Those circuit supports cover every clause.

So I can carry the continuous balance remainder as a finite typed relation set:

    <= k BalanceCircuit Objects
    + exact rational weights
    + source clause IDs
    + reconstruction receipts

This is structural compression only.

    POSITIVE BALANCE CIRCUIT != UNSAT CORE
    CIRCUIT COVER <= DEFICIENCY != SAT ALGORITHM

The new exact question is whether the **overlap relation among those positive circuits** can remove, dominate, decompose, or cheaply project one Boolean degree without recreating that degree as a fresh selector.
