# Boolean Shear Fiber Theorem and Normalization Partition — 2026-09-26

**Program:** synchronized P vs NP proof program  
**Predecessor:** `PNP_MINIMAL_LINEAR_BOOLEAN_SEAM_PAIR_2026-09-26.md`  
**Status:** exact fiber theorem + normalization refinement  
**Claim ceiling:** not universal P=NP

## 1. Exact fiber theorem

Fix a tight internal matrix (A_V) with full column rank.

For two boundary attachment matrices (E,E') on the same touched clause rows, define:

[
ho_E = E^T|_{ker(A_V^T)}.
]

Then:

[
oxed{ho_E=ho_{E'}}
]

iff every column of (E'-E) lies in (operatorname{col}(A_V)).

Equivalently, there exists a matrix (T) such that

[
oxed{E'=E+A_VT}.
]

Because (A_V) has full column rank, (T) is unique once (E,E') are fixed.

### Proof

[
ho_E=ho_{E'}
]

iff

[
(E'-E)^Tz=0
quadorall zinker(A_V^T).
]

Thus each column (d) of (E'-E) lies in

[
(ker(A_V^T))^perp.
]

By the fundamental theorem of linear algebra,

[
(ker(A_V^T))^perp=operatorname{col}(A_V).
]

Hence (d=A_Vt) columnwise, giving (E'-E=A_VT).

QED.

## 2. What the linear seam actually quotients

The current residual map does not see the exact discrete attachment matrix (E).

It sees only its coset modulo the internal column space:

[
oxed{
[E]_{m lin}
=
E+operatorname{col}(A_V).
}
]

The coordinate (T) inside that fiber is therefore the exact degree discarded by the linear seam.

Call (T) the:

[
oxed{	ext{BOUNDARY ATTACHMENT SHEAR COORDINATE}}.
]

## 3. Boolean semantics is not invariant on the fiber

The minimal witness proves:

[
E_B=E_A+A_V[:,y]
]

while

[
ho_{E_A}=ho_{E_B}.
]

Yet:

[
I_A(a)=a,
qquad
I_B(a)=	op.
]

With the same outside clause (
eg a), the parent decisions differ:

[
F_Ain UNSAT,
qquad
F_Bin SAT.
]

Therefore:

[
oxed{
	ext{LINEAR FIBER EQUALITY}

otRightarrow
	ext{BOOLEAN INTERFACE EQUALITY}.
}
]

## 4. Why the minimal witness does not survive the current normalizer

In the witness, the shear copies the complete signed occurrence column of internal variable (y) onto boundary variable (a) on the rows where (a) was absent.

Thus every positive-(y) clause acquires (a), and every negative-(y) clause acquires (
eg a).

Take any positive-(y) parent clause and negative-(y) parent clause.

Their resolvent on (y) contains:

[
aee
eg a.
]

Hence every (y)-resolvent is tautological.

So (y) becomes an exact blocked / zero-resolvent variable.

The current BCE / bounded-DP lifecycle removes it.

Thus:

[
oxed{
	ext{MINIMAL BOOLEAN-CHANGING SHEAR}
=
	ext{NORMALIZER-VISIBLE}.
}
]

This does not erase the counterexample. It classifies it.

## 5. Three species inside one linear fiber

For admissible shears (T) such that (E+A_VT) remains a legal signed clause-incidence attachment, classify:

### A. BOOLEAN STABILIZER

[
exists V,F(E+A_VT)
equiv
exists V,F(E).
]

The shear is invisible both linearly and Booleanly.

### B. NORMALIZER-VISIBLE SHEAR

The Boolean interface changes, but the transformed parent exposes an already-admitted polynomial reduction:

- blocked clause / blocked variable;
- non-increasing or charged bounded DP;
- dominance;
- functional elimination;
- autarky reduction;
- another current normalization terminal.

This shear never belongs to the final hard core.

### C. HARD SHEAR

The Boolean interface changes **and** both sides survive the current normalization lifecycle.

This is the only species that can remain hidden in the current P-vs-NP remainder.

## 6. New exact research target

The old question:

> Does (ho_B) determine the Boolean interface?

is answered:

[
oxed{	ext{NO}}.
]

The repaired question is:

> After quotienting out the Boolean stabilizer and every normalizer-visible shear, does any hard shear remain?

Formally:

[
oxed{
mathcal H(A_V,E)
=
{T:
E+A_VT	ext{ legal},
 I_T
otequiv I_0,
 	ext{both states normalization-irreducible}
}.
}
]

The decisive target is:

[
oxed{
mathcal H(A_V,E)=arnothing
quad	ext{for every fully normalized tight block?}
}
]

If true, the linear seam becomes sufficient **after normalization**, even though it is insufficient in general.

If false, the smallest member of (mathcal H) identifies the next missing Boolean distinction.

## 7. Pressure directions

BEND the hard-shear set with:

1. exact Boolean projection;
2. R0-R6 normalization;
3. first-mixed resolution structure;
4. boundary conflict graph;
5. residual rank / orthants;
6. positive balance;
7. surplus expansion;
8. parent liftability.

The first surviving hard shear is the next seam Object.

## 8. Claim ceiling

[
oxed{ho	ext{-FIBER THEOREM = EXACT}}
]

[
oxed{	ext{MINIMAL GENERAL SEPARATION = FOUND}}
]

[
oxed{	ext{MINIMAL WITNESS IS NORMALIZER-VISIBLE}}
]

[
oxed{	ext{HARD-SHEAR EMPTINESS = OPEN}}
]

[
oxed{P=NP	ext{ remains unproved}.}
]
