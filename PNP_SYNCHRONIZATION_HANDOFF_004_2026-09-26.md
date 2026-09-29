# P vs NP Synchronization Handoff 004 — Positive-Circuit Signature Quotient

**Status:** CURRENT BOUNDED OUTWARD SYNCHRONIZATION  
**Mathematical authority:** `redogit/redogit`  
**Tooling authority:** `redogit/DnD`  
**Method/routing authority:** `redogit/conscience64/research/cooperative-field/`

## Consequential delta

New/updated target-local successors:

- `PNP_HIGHER_ORDER_CIRCUIT_COMPATIBILITY_2026-09-26.md`
- `PNP_POSITIVE_CIRCUIT_SIGNATURE_COMPLETENESS_2026-09-26.md`
- live design commit `437f0b873bdca8ddc7736cac96a8070b79f00460`

## Exact theorem

For any CNF G and rescue/deletion sets C,D, let s_C record which support-minimal positive row circuits of M(G) are hit by C.

Then:

~~~text
s_C = s_D
->
SAT(G\C) = SAT(G\D).
~~~

Thus correction status is constant on full positive-circuit hit-signature classes.

## Polynomial implicit representation

The positive-circuit family is represented implicitly by:

~~~text
M^T y = 0
y >= 0.
~~~

LP queries can decide whether two rescue sets have different positive-circuit signatures without enumerating circuits.

For rescue C define U(C) as the union of all positive circuits disjoint from C.

Clause membership in U(C) is polynomially testable by LP, and:

~~~text
SAT(G\C)
iff
SAT(U(C)).
~~~

So boundary rescue can be followed by a polynomial positive-circuit/linear-autarky closure.

## Counterprobe preserved

A selected circuit cover is too coarse. A paired-NAE example has two rescue sets that hit the same selected pair-cover circuits but have opposite correction status. Larger positive circuits distinguish them.

Disposition:

~~~text
SELECTED COVER = ASH AS COMPLETE SIGNATURE
FULL POSITIVE-CIRCUIT SIGNATURE = EXACT COMPLETE QUOTIENT
~~~

## Current remainder

The unresolved Boolean work is now:

~~~text
EVALUATE SAT ON THE
NORMALIZED SURVIVING POSITIVE-CIRCUIT CORE U(C)
IN POLYNOMIAL WORK.
~~~

Equivalently:

~~~text
WHICH SURVIVING POSITIVE-CIRCUIT ARRANGEMENTS
ARE JOINTLY SIGN-CENTRAL / UNSAT?
~~~

No claim that this value evaluation is polynomial has been admitted.

## Claim ceiling

~~~text
MINIMAL LINEAR/BOOLEAN SEAM PAIR = EXACT
BOUNDARY RESCUE / MUS TRANSVERSAL = EXACT
FULL POSITIVE-CIRCUIT SIGNATURE COMPLETENESS = EXACT
SIGNATURE EQUIVALENCE QUERIES = POLYNOMIAL LP
POSITIVE-CIRCUIT RESCUE CLOSURE = POLYNOMIAL LP
SIGNATURE VALUE EVALUATION = OPEN
UNIVERSAL P=NP = OPEN
~~~

## Tooling

No new DnD/RMAL compiler obligation was created.

Current RMAL tooling authority remains:

`redogit/DnD@c5d819b8ccda3ffe63e024d8ef02514fedcf896e`

~~~text
METHOD_TRANSFER != EVIDENCE_TRANSFER
NEWEST TOOLING != MATHEMATICAL EVIDENCE
~~~
