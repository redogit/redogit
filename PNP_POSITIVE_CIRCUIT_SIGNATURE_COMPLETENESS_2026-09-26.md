# Positive-Circuit Signature Completeness for Correction Status

**Program:** synchronized P vs NP proof program  
**Predecessors:**  
- `PNP_BOUNDARY_RESCUE_CORRECTION_SET_SEAM_2026-09-26.md`  
- `PNP_HIGHER_ORDER_CIRCUIT_COMPATIBILITY_2026-09-26.md`  
**Status:** exact theorem + polynomial signature-equivalence queries  
**Claim ceiling:** does not yet give a polynomial algorithm for evaluating the signature class itself

## 1. Definitions

Let (G) be any Boolean CNF with signed clause-variable matrix (M(G)).

Let

[
mathcal P(G)
]

be the family of all support-minimal positive row dependencies of (M(G)):

[
Qsubseteq G
]

is in (mathcal P(G)) iff there exists (y_Q>0) on (Q) such that

[
M_Q^Ty_Q=0,
]

and no proper nonempty subset of (Q) supports a nonnegative dependence.

These are the positive row circuits.

For a clause rescue/deletion set (Csubseteq G), define its positive-circuit hit signature:

[
s_C:mathcal P(G)	o{0,1},
]

[
s_C(Q)=1
iff
Ccap Q
eqarnothing.
]

Equivalently, (s_C(Q)=0) iff (Q) survives completely in (Gsetminus C).

## 2. Theorem — signature completeness

For any two deletion sets (C,Dsubseteq G),

[
oxed{
s_C=s_D
Longrightarrow
igl(Gsetminus Cin SAT
iff
Gsetminus Din SATigr).
}
]

So correction-set status is constant on positive-circuit signature classes.

### Proof

Assume:

[
s_C=s_D.
]

Suppose for contradiction that

[
Gsetminus Cin SAT
]

but

[
Gsetminus Din UNSAT.
]

Choose a minimally unsatisfiable subformula

[
Hsubseteq Gsetminus D.
]

Because (H) is minimally UNSAT, it is lean and therefore has no nontrivial linear autarky.

By the signed theorem of alternatives used in the normalization program:

[
operatorname{rank}M_H=n(H)
]

and there exists a strictly positive vector

[
y>0
]

with

[
M_H^Ty=0.
]

Decompose (y) into support-minimal nonnegative kernel rays / positive circuits:

[
y=sum_j lambda_j y^{(j)},
qquad
lambda_j>0.
]

Because (y) is strictly positive on every clause of (H), the supports

[
Q_j=operatorname{supp}(y^{(j)})
]

cover every clause of (H).

Each (Q_j) is a positive row circuit of (M_H), and therefore also a positive row circuit of (M(G)): adding other rows does not create a smaller dependence inside the fixed support (Q_j).

Since:

[
Hsubseteq Gsetminus D,
]

we have:

[
Dcap Q_j=arnothing
]

for every (j).

Thus:

[
s_D(Q_j)=0.
]

By (s_C=s_D),

[
s_C(Q_j)=0,
]

so:

[
Ccap Q_j=arnothing
]

for every (j).

The (Q_j) cover (H). Hence:

[
Ccap H=arnothing.
]

Therefore:

[
Hsubseteq Gsetminus C.
]

But (H) is UNSAT, contradicting:

[
Gsetminus Cin SAT.
]

The reverse direction follows symmetrically.

QED.

## 3. Exact consequence for the boundary interface

For a tight block (G=F[V]) and boundary assignment (alpha), let:

[
R(alpha)
]

be its rescued clause set.

The boundary-rescue theorem gave:

[
I_V(alpha)=1
iff
Gsetminus R(alpha)in SAT.
]

Therefore the exact interface factors through the full positive-circuit signature:

[
oxed{
alpha
	o
R(alpha)
	o
s_{R(alpha)}
	o
I_V(alpha).
}
]

So:

[
oxed{
	ext{FULL POSITIVE-CIRCUIT HIT SIGNATURE
IS A COMPLETE BOOLEAN QUOTIENT
FOR CORRECTION STATUS.}
}
]

This is stronger than the selected-circuit-cover carrier.

## 4. Why the selected cover failed

A chosen positive-circuit cover stores only a subset of (mathcal P(G)).

The paired-NAE counterprobe produced rescue sets with identical hit patterns on the selected disjoint 2-circuit cover but different correction status.

Larger positive circuits (Q_+,Q_-) distinguish the two rescue sets.

That is exactly what the theorem predicts:

[
	ext{SELECTED COVER}

eq
	ext{FULL POSITIVE-CIRCUIT SIGNATURE}.
]

## 5. The exponential-family problem is not ignored

The family (mathcal P(G)) may be exponentially large.

The theorem therefore does **not** license explicit circuit enumeration.

Instead use the positive-kernel cone:

[
K_+(G)
=
{yinmathbb R_{ge0}^{m}:
M(G)^Ty=0}.
]

Its extreme rays are exactly the support-minimal positive dependencies up to scaling.

This cone has a polynomial-size H-representation:

[
M(G)^Ty=0,
qquad
yge0.
]

Thus the full circuit family is represented implicitly by the original signed matrix plus nonnegativity.

## 6. Polynomial separator query between two rescue signatures

Given two rescue sets (C,D), their signatures differ iff there exists a positive circuit hit by one and not the other.

For example, a circuit hit by (C) but disjoint from (D) exists iff the following LP is feasible for some clause (ein Csetminus D):

[
M^Ty=0,
]

[
yge0,
]

[
y_i=0quad(iin D),
]

[
y_ege1.
]

If feasible, decompose an extreme feasible ray / choose an extreme point of the normalized section to obtain a positive circuit disjoint from (D) containing a member of (C).

Conversely any such circuit gives a feasible solution.

Therefore equality of full positive-circuit hit signatures is decidable with polynomially many linear programs.

One may also combine the (e)-tests through a normalization such as

[
sum_{ein Csetminus D}y_ege1.
]

Do the symmetric test for (Dsetminus C).

Hence:

[
oxed{
s_C=s_D
	ext{ is polynomially decidable without enumerating }mathcal P(G).
}
]

## 7. Signature-preserving rescue moves

Let (Csubseteq G) and (e
otin C).

Adding (e) to the rescue set changes the signature iff there exists a positive circuit:

[
Q
i e
]

with:

[
Qcap C=arnothing.
]

This is exactly the LP feasibility test:

[
M^Ty=0,quad
yge0,quad
y_i=0 (iin C),quad
y_ege1.
]

If infeasible, then:

[
s_C=s_{Ccup{e}}.
]

By the signature-completeness theorem:

[
oxed{
Gsetminus Cin SAT
iff
Gsetminus(Ccup{e})in SAT.
}
]

Thus we obtain a new exact polynomial rescue reduction:

> Add a clause to the rescue/deletion set whenever no surviving positive circuit uses that clause.

This changes the formula while preserving correction status, with an LP receipt.

Repeated application reaches a canonical/maximal signature-preserving rescue closure under a fixed stable clause order.

## 8. What still remains

The theorem gives:

- a complete quotient;
- polynomial equivalence testing between two quotient representatives;
- polynomial tests for some signature-preserving moves.

It does **not** yet give the Boolean value attached to an arbitrary signature class.

In particular:

[
	ext{signature equality is easy}
]

does not imply:

[
	ext{correction status of a signature is easy}.
]

The remaining problem is therefore sharper:

[
oxed{
	ext{EVALUATE THE BOOLEAN CORRECTION VALUE
ON POSITIVE-CIRCUIT SIGNATURE CLASSES
IN POLYNOMIAL WORK.}
}
]

## 9. Connection to minimal sign-central structure

MUSes correspond, under the signed-matrix dictionary, to column-minimal sign-central submatrices of (M(G)^T).

The signature-completeness proof shows why MUS enumeration can be replaced conceptually by the full positive-circuit arrangement:

every MUS has a strictly positive balance whose positive circuits cover every MUS clause.

So the exact remaining distinction is not missing positive circuits.

It is:

[
oxed{
	ext{WHICH SURVIVING POSITIVE-CIRCUIT ARRANGEMENTS
ARE JOINTLY SIGN-CENTRAL / UNSAT?}
}
]

That is the higher-order compatibility function.

## 10. Next BEND target

Pressure the signature class from:

1. oriented-matroid / positive-cone structure;
2. minimal sign-central structure;
3. surplus / maximum deficiency;
4. normalization R0-R6;
5. correction/MUS duality;
6. boundary rescue realizability.

Find either:

A. a polynomial invariant of the surviving positive-circuit arrangement that evaluates correction status; or

B. a smallest pair of **signature classes** that all current polynomial invariants identify but correction status separates.

## 11. Claim ceiling

[
oxed{	ext{FULL POSITIVE-CIRCUIT SIGNATURE COMPLETENESS = EXACT}}
]

[
oxed{	ext{SIGNATURE EQUIVALENCE TEST = POLYNOMIAL LP}}
]

[
oxed{	ext{SIGNATURE-PRESERVING RESCUE MOVE = POLYNOMIAL LP}}
]

[
oxed{	ext{SIGNATURE VALUE EVALUATION = OPEN}}
]

[
oxed{	ext{UNIVERSAL P=NP = OPEN}}
]
