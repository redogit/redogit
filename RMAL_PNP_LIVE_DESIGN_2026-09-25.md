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
    incidence-component factorization
    polynomial conformal-event-count / output-sensitive clique terminal

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

## POLYNOMIAL CONFORMAL-EVENT-COUNT TERMINAL

The log-degeneracy guard is only a sufficient proxy.

The exact inclusion-exclusion carrier needs one event for each nonempty clique of the clause nonclash / column-conformality graph Q_F. Use an output-sensitive all-clique enumerator with a fixed polynomial cap P(N)=N^c.

    enumeration completes <= P(N)
        -> retain every conformal event
        -> exact inclusion-exclusion #SAT / SAT / UNSAT

    more than P(N) events emitted
        -> stop
        -> UNRESOLVED under this carrier.

This is polynomial because clique listing has polynomial work per emitted clique.

Thus the admitted resource is the actual number of jointly falsifiable clause-event intersections, not merely a structural width proxy.

Current qualitative residual:

    SUPER-CAP CONFORMAL EVENT MULTIPLICITY.

This is representation-growth evidence, not a hardness certificate.

## BALANCE-CIRCUIT / CONFORMAL-EVENT BRIDGE

For every positive balance circuit B:

    z>0 on B
    M^T z=0

every variable used in B occurs in both polarities inside B.

Therefore every clause in B clashes with at least one other clause in B, and B can never be a clique of the clause nonclash / column-conformality graph.

So for every conformal event T:

    B_i not-subseteq T
    for every balance circuit B_i.

Equivalently:

    F \ T

hits every circuit in the positive balance-circuit cover.

This is the first direct exact seam between the balance carrier and the conformal-event carrier.

It does not yet bound the number of conformal events. The next useful theorem must exploit the overlap structure of the balance-circuit hypergraph strongly enough to force polynomial event count, decomposition, dominance, projection, or a negative sign-central certificate.

## INCIDENCE-COMPONENT FACTORIZATION

Before treating global conformal-event multiplicity as a live obstruction, split the CNF by connected components of the clause-variable incidence graph.

For disjoint components F_i:

    SAT(F) iff every SAT(F_i)

and

    #SAT(F)
      =
    2^(free variables)
      * product_i #SAT(F_i).

The clause nonclash graph is the graph join of the component nonclash graphs, so:

    K(F)+1
      =
    product_i (K(F_i)+1).

Thus global clique/event count may be exponential solely because independent components multiply. That is not intrinsic hard-core growth.

Run conformal-event enumeration and every other exact terminal componentwise.

Positive balance circuits also localize componentwise because the signed incidence matrix is block diagonal and a support-minimal positive dependency cannot span two blocks.

Current event-side remainder:

    INCIDENCE-CONNECTED
    +
    SUPER-CAP CONFORMAL EVENT MULTIPLICITY.

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


## 2026-09-26 successor — semantic intersection-state quotient

Successor artifact: [Semantic Intersection-State Quotient](PNP_SEMANTIC_INTERSECTION_QUOTIENT_2026-09-26.md).

The conformal-clique carrier was exact but still counted descriptions rather than semantic event identities. The successor quotients all compatible clause subsets by their exact joined falsifying partial assignment, producing an intersection semilattice L(F). Möbius inversion over L(F) gives exact #SAT, SAT/UNSAT, and Homeward reconstruction whenever the number of distinct semantic states is polynomially bounded.

A strict separation family has exponentially many raw conformal cliques but only polynomially many semantic intersection states, so the live qualitative remainder is now:

    SUPER-CAP DISTINCT SEMANTIC INTERSECTION-STATE MULTIPLICITY

not raw clique multiplicity.

The balance-side counterprobe also burned an overly weak next target: pairwise support overlap among selected positive balance circuits is not enough. Two full-rank 7-variable instances have the same seven disjoint positive 2-circuit overlap object but opposite SAT status. The next relation must preserve variable/sign incidence together with canonical semantic intersection states.

    DESCRIPTION MULTIPLICITY != EVENT MULTIPLICITY
    CIRCUIT OVERLAP ALONE != UNIVERSAL NAVIGATION


## 2026-09-26 successor — cubic 3-uniform residual calibration

Successor: [PNP_CUBIC_3UNIFORM_RESIDUAL_2026-09-26.md](PNP_CUBIC_3UNIFORM_RESIDUAL_2026-09-26.md).

The paired positive-balance family was pushed one degree further. Under 3-uniformity, maximum degree <=3, connectedness, and the current full-rank paired residual, the surviving boundary has m=n and every variable degree exactly 3: a cubic 3-uniform hypergraph.

The external Henning-Yeo boundary makes every non-2-colorable cubic component edge-critical: deleting any hyperedge yields a 2-colorable remainder. This does not by itself reduce complexity. Flip/recolor coordinates relative to such a near-solution are a bijective XOR change of variables and therefore fail the degree-removal gate.

Incidence girth was also counterprobed and rejected as a decision invariant: a 10-vertex cubic 3-uniform girth-6 instance with 48 valid 2-colorings was found.

A quasi-matching theorem supplies a conditional positive certificate through perfect-matching count modulo 3, but generic permanent-mod-3 computation is not admitted as polynomial. Use it only inside independently tractable matching-count carriers.

Current cubic remainder:

    EDGE-CRITICAL CUBIC 3-UNIFORM INCIDENCE CARRIER
    x
    SEMANTIC INTERSECTION-STATE CARRIER
    x
    PAIRED BALANCE CIRCUITS

with no NP-hardness claim attached to the exact cubic restriction.


## 2026-09-26 successor — cubic paired-NAE bond lattice

Successor: [PNP_CUBIC_BOND_LATTICE_CARRIER_2026-09-26.md](PNP_CUBIC_BOND_LATTICE_CARRIER_2026-09-26.md).

The paired cubic NAE carrier now preserves the original hyperedge obligation instead of splitting it into two signed clause-falsification descriptions.

For each hyperedge e:

    Mono(e)
      := all vertices of e have the same color.

For any selected edge set A, the intersection of Mono(e), e in A, depends only on the equality partition pi_A induced by connected components of the selected-edge subhypergraph.

Therefore:

    EDGE-SUBSET HISTORY
    !=
    EVENT IDENTITY

    EVENT IDENTITY
    =
    EQUALITY PARTITION.

The distinct equality partitions form the hypergraph bond/intersection lattice L_H. Möbius inversion gives the exact 2-color count:

    P_H(2)
      =
    sum_{pi in L_H}
      mu(hat0,pi) 2^(|pi|).

If the distinct partition-state count is within a declared polynomial cap, the carrier yields exact SAT/UNSAT/#2-color plus Homeward witness reconstruction in polynomial total work.

The retained cubic witnesses compress further in this carrier:

    Fano:
        73 signed semantic states
        -> 37 equality-partition states
        -> 0 colorings

    full-rank SAT-7:
        69
        -> 35
        -> 14 colorings

    SAT girth-6 n=10:
        495
        -> 227
        -> 48 colorings.

A 1,000-instance bounded cubic differential panel returned zero total-count mismatches and zero partial-extension mismatches.

Current cubic remainder:

    EDGE-CRITICAL CUBIC 3-UNIFORM
    +
    SUPER-CAP EQUALITY-PARTITION MULTIPLICITY.

Do not return to generic recoloring coordinates.

    PAIRED OBLIGATION PRESERVED
    !=
    UNIVERSAL P=NP CLOSURE.


## 2026-09-26 successor — signed partition-coefficient transfer

Inside the cubic paired-NAE bond lattice, edge-subset histories can be aggregated during execution rather than only after the full lattice is built.

For every active equality partition pi carry one signed coefficient c(pi).

Processing one hyperedge e performs exactly:

    absent:
        new[pi] += c(pi)

    present:
        new[join(pi,e)] -= c(pi).

After aggregation, a state with coefficient zero is deleted exactly: both of its future linear contributions are zero.

The final exact count is:

    #2-colorings
      =
    sum_pi c(pi) 2^(blocks(pi)).

Coefficient magnitude has only O(m) bits.

The admitted execution measure is now:

    W_coeff
      =
    maximum number of active nonzero coefficient partitions
    under the fixed stable hyperedge order.

If W_coeff is polynomially capped, exact solve and Homeward reconstruction are polynomial even when the full generated bond lattice is larger.

Bounded cubic validation:

    1,000 instances
    count mismatches: 0

strongest observed reduction:

    139 full equality states
    ->
    100 active coefficient states.

Current cubic remainder:

    EDGE-CRITICAL CUBIC 3-UNIFORM
    +
    SUPER-CAP ACTIVE PARTITION-COEFFICIENT WIDTH.

Successor/source:

- [Cubic Paired-NAE Bond-Lattice Carrier](PNP_CUBIC_BOND_LATTICE_CARRIER_2026-09-26.md)
- [checker](PNP_CUBIC_BOND_COEFFICIENT_CHECK_2026-09-26.py)
- [bounded evidence](PNP_CUBIC_BOND_COEFFICIENT_EVIDENCE_2026-09-26.json)


## 2026-09-26 successor — future-frontier projection carrier

Successor: [Cubic Paired-NAE Future-Frontier Projection Carrier](PNP_CUBIC_FRONTIER_PROJECTION_CARRIER_2026-09-26.md).

The signed bond-lattice execution now projects an equality coordinate as soon as no unprocessed hyperedge can touch it again.

When an entire equality block closes:

    unfixed block -> multiply by 2
    fixed-color block -> multiply by 1.

Decision uses nonzero signed equality-partition states on the future-active frontier.

Homeward is separately guarded: partial-color queries attach only one minimal status per active block:

    UNFIXED / 0 / 1.

A 0/1 conflict inside a joined block is an empty event and drops.

The complete terminal is admitted only when both actual widths stay inside the fixed polynomial cap:

    W_front  = projected decision-state width
    W_home   = maximum labeled state width during self-reduction.

Bounded validation:

    decision panel: 1,000 cubic instances, 0 mismatches
    Homeward panel: 1,000 cubic instances, 0 failures
    strongest observed global->frontier width reduction: 118 -> 12
    maximum labeled Homeward width observed: 66.

Current cubic remainder:

    EDGE-CRITICAL CUBIC 3-UNIFORM
    +
    SUPER-CAP PROJECTED FRONTIER WIDTH
    OR
    SUPER-CAP LABELED HOMEWARD WIDTH.

The next lawful degree may alter/factor incidence ordering only through a polynomially discoverable certificate.

- [checker](PNP_CUBIC_FRONTIER_PROJECTION_CHECK_2026-09-26.py)
- [bounded evidence](PNP_CUBIC_FRONTIER_PROJECTION_EVIDENCE_2026-09-26.json)
