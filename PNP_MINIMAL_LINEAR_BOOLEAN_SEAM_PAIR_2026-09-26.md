# Minimal Linear-Seam / Boolean-Seam Separation Pair — 2026-09-26

**Program:** synchronized P vs NP proof program  
**Method:** BEND — pressure the same Object from linear, Boolean, surplus, balance, and parent-lift directions  
**Predecessor:** `PNP_BOUNDARY_RESIDUAL_ORTHANTS_2026-09-26.md`  
**Status:** exact finite counterexample + minimality below this parent size  
**Claim ceiling:** identifies the missing seam degree; does not prove P=NP

## 1. Target

Find the smallest pair for which the current linear seam declares the boundary behavior identical while the exact Boolean interface differs.

Use the strongest current linear equivalence:

- same internal tight matrix (A_V);
- same boundary variable set;
- same exact boundary residual map
  [
  ho_B = A_B^T|_{ker(A_V^T)};
  ]
- same global full-column-rank / positive-balance setting.

Then compare:

[
I_V=exists V,F_{mathrm{touch}}.
]

## 2. The pair

Variables:

[
V={x,y},qquad B={a}.
]

### Parent A

[
F_A=
(xee a)
wedge
(y)
wedge
(
eg xee
eg y)
wedge
(
eg a).
]

### Parent B

[
F_B=
(xee a)
wedge
(yee a)
wedge
(
eg xee
eg yee
eg a)
wedge
(
eg a).
]

The first three clauses are the clauses touching (V).  
The fourth clause is the same outside clause in both parents.

## 3. Same tight block

Restrict both parents to (V):

[
G=F_A[V]=F_B[V]
=
(x)wedge(y)wedge(
eg xee
eg y).
]

The signed internal matrix is

[
A_V=
egin{pmatrix}
1&0\
0&1\
-1&-1
end{pmatrix}.
]

It has

[
operatorname{rank}(A_V)=2
]

and

[
K_V=ker(A_V^T)=operatorname{span}{(1,1,1)^T}.
]

So the tight block has thickness/nullity (k=1).

## 4. Same exact linear seam

The boundary-attachment columns are

[
e_A=
egin{pmatrix}
1\0\0
end{pmatrix},
qquad
e_B=
egin{pmatrix}
1\1\-1
end{pmatrix}.
]

Their difference is exactly the internal (y)-column:

[
e_B-e_A=
egin{pmatrix}
0\1\-1
end{pmatrix}
=
A_V[:,y].
]

For every (zin K_V),

[
A_V[:,y]^Tz=0.
]

Therefore

[
e_A^Tz=e_B^Tz
qquad
orall zin K_V.
]

Hence the two instances have **the same exact boundary residual map**:

[
oxed{ho_B^A=ho_B^B}.
]

For the positive basis vector (z=(1,1,1)^T),

[
ho_B^A(z)=ho_B^B(z)=1.
]

Thus they also have the same:

- residual rank (eta=1);
- residual sign arrangement;
- inherited internal positive-balance direction.

## 5. Same global linear balance

With variable order ((x,y,a)), the full parent matrices are

[
M_A=
egin{pmatrix}
1&0&1\
0&1&0\
-1&-1&0\
0&0&-1
end{pmatrix},
]

[
M_B=
egin{pmatrix}
1&0&1\
0&1&1\
-1&-1&-1\
0&0&-1
end{pmatrix}.
]

Both have full column rank:

[
operatorname{rank}(M_A)
=
operatorname{rank}(M_B)
=
3.
]

And the same strictly positive balance vector:

[
(1,1,1,1)^T
]

satisfies

[
M_A^Tmathbf 1=0,
qquad
M_B^Tmathbf 1=0.
]

Both parents have surplus (1), and (V={x,y}) is a minimum-surplus set in both.

So the separation is not caused by losing the current normalized rank/balance/surplus conditions.

## 6. Boolean interfaces differ

For Parent A:

[
I_A(a)
=
exists x,y,
[(xee a)wedge ywedge(
eg xee
eg y)].
]

Since (y=1), the third clause forces (x=0).  
Then the first clause requires (a=1).

Therefore

[
oxed{I_A(a)=a}.
]

For Parent B:

[
I_B(a)
=
exists x,y,
[(xee a)wedge(yee a)wedge
(
eg xee
eg yee
eg a)].
]

If (a=0), choose (x=y=1).  
If (a=1), choose for example (x=0).

Therefore

[
oxed{I_B(a)=	op}.
]

So:

[
oxed{
ho_B^A=ho_B^B
quad	ext{but}quad
I_A
eq I_B.
}
]

## 7. The difference reaches the parent decision

Both parents contain the same outside clause (
eg a).

Thus:

[
F_A
equiv
awedge
eg a
]

at the interface level, hence

[
oxed{F_Ain UNSAT}.
]

But:

[
F_B
equiv
	opwedge
eg a,
]

and for example

[
(x,y,a)=(1,1,0)
]

satisfies (F_B).

Therefore

[
oxed{F_Bin SAT}.
]

This is stronger than merely producing different interface clauses: the hidden seam coordinate flips the final parent decision.

## 8. What separates the pair

The linear seam sees boundary columns only modulo the internal column space.

In general:

[
ho_B(A_B)=ho_B(A_B')
]

iff, column by column,

[
A_B'-A_Binoperatorname{col}(A_V).
]

Thus (ho_B) identifies an entire fiber:

[
A_B+operatorname{col}(A_V).
]

But Boolean CNF semantics is not invariant inside that fiber.

In the witness,

[
e_B=e_A+A_V[:,y].
]

This is a **column shear** invisible to every internal balance.

Booleanly, however, it changes the clausewise attachments:

[
y
	o
yee a,
]

and

[

eg y
	o

eg yee
eg a.
]

That lets (a) act as an alternative/gating coordinate across the (y)-clauses and changes the existential interface from (a) to (	op).

## 9. The missing Object

The thing hidden between the linear and Boolean seams is therefore:

[
oxed{	ext{the discrete representative inside the }ho_B	ext{-fiber}}
]

or, operationally:

[
oxed{	ext{CLAUSEWISE BOUNDARY-ATTACHMENT SHEAR}}.
]

The immediate separating data is the rowwise signed support:

[
(P_a,N_a),
]

where

[
P_a={C:ain C},
qquad
N_a={C:
eg ain C}.
]

For the two touched blocks:

### Parent A

[
P_a={C_1},
qquad
N_a=arnothing.
]

### Parent B

[
P_a={C_1,C_2},
qquad
N_a={C_3}.
]

The outside-sign conflict graph changes from no conflict to conflicts
(C_1-C_3) and (C_2-C_3).

So the first-mixed Boolean carrier was detecting a distinction that the residual linear quotient had deliberately erased.

## 10. Minimality

Under the current parent-valid seam contract, no smaller parent can separate the two views.

A boundary requires at least two parent variables.

### Two parent variables, three clauses

A proper tight block has one internal variable (x) and one boundary variable (a).

The tight internal positive-balanced block can contain only the two opposite (x)-sign rows.

Existentially eliminating (x) gives their single resolvent.

For fixed active boundary (a), the exact residual map records the sum of the two signed (a)-attachments:

- positive sum gives interface (a);
- negative sum gives (
eg a);
- zero with active (a) means complementary attachments and gives (	op).

Thus identical (ho_B) implies identical Boolean interface.

No separation exists.

### Two parent variables, four clauses

The only new tight case has three clauses touching (x).

Tightness forces the boundary variable (a) to occur in at least two of those touched clauses.

Up to internal sign reversal/permutation, the internal sign column is

[
(-1,-1,+1)^T.
]

For the 20 possible boundary-attachment vectors with at least two nonzero entries, exhaustive exact enumeration groups them by the exact residual-map coordinates

[
(e_1+e_3,;e_2+e_3).
]

Within every group the existential Boolean interface is identical.

So no two-variable/four-clause parent separation exists.

Therefore the displayed

[
oxed{3	ext{ variables}, 4	ext{ clauses}}
]

pair is minimal in total parent size under the declared seam conditions.

## 11. Consequence for the research direction

Residual rank and residual orthants are now definitively too coarse.

Do not ask whether (eta) alone controls the Boolean interface.

The next quotient must preserve enough of the **fiber representative** to distinguish Booleanly active shears while still discarding irrelevant attachment detail.

New target:

> Classify which transformations
> [
> A_Bmapsto A_B+A_VT
> ]
> preserve the exact existential interface, and which change it.

Equivalently:

[
oxed{
	ext{find the Boolean stabilizer of the linear-seam fiber action}.
}
]

If that stabilizer is polynomially recognizable and the remaining orbit space is polynomially bounded, we obtain a stronger joint seam carrier.

If the orbit space can encode arbitrary Boolean functions, this entire linear-seam compression route is Ash.

## 12. Claim ceiling

[
oxed{ho	ext{-IDENTICAL / BOOLEAN-DIFFERENT PAIR FOUND}}
]

[
oxed{	ext{PAIR IS MINIMAL UNDER THE DECLARED PARENT-SIZE CONTRACT}}
]

[
oxed{	ext{HIDDEN DEGREE = DISCRETE ATTACHMENT SHEAR}}
]

[
oxed{	ext{LINEAR RESIDUAL QUOTIENT ALONE = INSUFFICIENT}}
]

[
oxed{	ext{BOOLEAN STABILIZER OF SHEARS = NEXT OPEN EDGE}}
]

[
oxed{P=NP	ext{ remains unproved}.}
]
