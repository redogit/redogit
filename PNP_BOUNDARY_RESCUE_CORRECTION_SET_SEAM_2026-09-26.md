# Boundary Rescue / Correction-Set Seam — 2026-09-26

**Program:** synchronized P vs NP proof program  
**Predecessors:**  
- `PNP_MINIMAL_LINEAR_BOOLEAN_SEAM_PAIR_2026-09-26.md`  
- `PNP_BOOLEAN_SHEAR_FIBER_THEOREM_2026-09-26.md`  
**Status:** exact Boolean seam theorem  
**Claim ceiling:** not universal P=NP

## 1. Parent/tight decomposition

Let (V) be a tight internal variable block and let (R) be the parent clauses touching (V).

For every (iin R), write

[
C_i=D_iee E_i,
]

where:

- (D_i) contains the literals on internal variables (V);
- (E_i) contains the literals on boundary/outside variables (B).

The tight restriction is

[
G=igwedge_{iin R}D_i.
]

The exact parent interface is

[
I_V(B)
=
exists V,
igwedge_{iin R}(D_iee E_i).
]

## 2. Boundary rescue set

Fix a boundary assignment (alphain{0,1}^B).

Define the rescued clause set

[
mathcal R(alpha)
=
{,iin R:alphamodels E_i,}.
]

These are exactly the touched parent clauses already satisfied by the outside assignment.

Every clause (i
otinmathcal R(alpha)) has all its outside literals falsified by (alpha), and therefore reduces to (D_i).

Hence

[
left.
igwedge_{iin R}(D_iee E_i)
ight|_{alpha}
=
igwedge_{i
otinmathcal R(alpha)}D_i.
]

Therefore:

[
oxed{
I_V(alpha)=1
iff
Gsetminusmathcal R(alpha)in SAT.
}
]

This is exact.

## 3. Correction-set formulation

Assume (G) is UNSAT.

A set (Csubseteq R) is a correction set iff

[
Gsetminus Cin SAT.
]

Thus:

[
oxed{
I_V(alpha)=1
iff
mathcal R(alpha)
	ext{ is a correction set of }G.
}
]

If (G) is SAT, then every deletion (Gsetminus C) is SAT, so

[
I_Vequiv	op.
]

That is exactly the autarky door from the minimum-surplus fork.

## 4. MUS-transversal formulation

For UNSAT (G), a clause-removal set (C) makes (G) satisfiable iff it intersects every unsatisfiable subset, equivalently every MUS.

Therefore:

[
oxed{
I_V(alpha)=1
iff
orall Hin MUS(G):
mathcal R(alpha)cap H
eqarnothing.
}
]

So the exact Boolean parent interface is a hitting-set predicate:

[
oxed{
	ext{BOUNDARY ASSIGNMENT}
	o
	ext{RESCUE SET}
	o
	ext{MUS TRANSVERSAL}.
}
]

This is the precise Object that lies between the linear residual seam and the parent Boolean decision.

## 5. Minimal seam pair revisited

For the minimal witness, the common tight block is

[
G=
{C_1=x,;
C_2=y,;
C_3=
eg xee
eg y}.
]

It is minimally UNSAT.

Hence its correction sets are exactly the nonempty clause-removal sets.

### Parent A

Boundary attachment:

[
a	ext{ true}:
mathcal R_A(1)={C_1},
]

[
a	ext{ false}:
mathcal R_A(0)=arnothing.
]

Therefore:

[
I_A(1)=1,
qquad
I_A(0)=0,
]

so:

[
I_A=a.
]

### Parent B

Boundary attachment:

[
a	ext{ true}:
mathcal R_B(1)={C_1,C_2},
]

[
a	ext{ false}:
mathcal R_B(0)={C_3}.
]

Both are correction sets.

Therefore:

[
I_Bequiv	op.
]

The two parents have the same exact (ho_B), but different rescue maps into the correction family.

That is the smallest separating mechanism.

## 6. What the linear seam erased

The residual map preserves weighted cancellation:

[
E^T|_{ker(A_V^T)}.
]

It does **not** preserve:

[
alphamapstomathcal R(alpha).
]

A shear

[
Emapsto E+A_VT
]

can preserve every internal balance residual while changing which clauses are rescued by each boundary truth value.

Thus the missing Boolean information is:

[
oxed{	ext{CLAUSE-RESCUE OWNERSHIP}}
]

not another real-valued balance coordinate.

## 7. Connection to positive balance circuits

Every MUS (Hsubseteq G) is lean, hence linearly lean.

Therefore its signed clause-variable matrix has:

[
operatorname{rank}(M_H)=n(H)
]

and a strictly positive left-kernel vector.

Its balance nullity is:

[
dimker(M_H^T)
=
|H|-n(H)
=
delta(H).
]

### Deficiency 1

If

[
delta(H)=1,
]

then

[
operatorname{rank}(M_H)=|H|-1.
]

So the complete MUS support (H) is one row-matroid circuit, and its positive balance is support-minimal.

Thus:

[
oxed{
MU(1)
=
	ext{UNSAT POSITIVE-BALANCE CIRCUIT}
}
]

within this signed-matrix setting.

### Higher deficiency

If

[
delta(H)>1,
]

the positive balance decomposes into multiple support-minimal positive circuits covering (H).

No proper circuit support can itself be UNSAT, because (H) is minimally UNSAT.

Therefore the MUS obstruction is created by:

[
oxed{
	ext{GLOBAL INCOMPATIBILITY
AMONG LOCALLY SAT POSITIVE CIRCUITS}.
}
]

This is exactly the previously isolated cross-circuit remainder.

## 8. Convergence of the research lines

The current threads now meet:

[
	ext{LINEAR SEAM}
	o
	ext{ATTACHMENT SHEAR}
	o
	ext{BOUNDARY RESCUE SET}
	o
	ext{CORRECTION SET}
	o
	ext{MUS TRANSVERSAL}
	o
	ext{POSITIVE-CIRCUIT COMPATIBILITY}.
]

So the remaining Boolean seam is no longer vague.

It is:

> Can the correction-set/MUS-transversal predicate of a fully normalized tight block be represented and queried in polynomial work from its positive-circuit compatibility structure?

## 9. Why this does not already solve SAT

MUS/MCS duality is exact but can itself be exponentially large.

Enumerating all MUSes or all correction sets is not an admissible universal step.

Likewise:

[
	ext{MUS TRANSVERSAL FORMULATION}

eq
	ext{POLYNOMIAL ALGORITHM}.
]

The next carrier must avoid full MUS enumeration.

## 10. Next BEND pressures

Press this new Object from:

1. **positive circuits** — locally tractable components;
2. **MUS structure** — minimal global incompatibilities;
3. **correction sets** — minimum removals that restore satisfiability;
4. **boundary rescue map** — which removals boundary assignments can realize;
5. **surplus/maximum deficiency** — bounds every subformula's deficiency;
6. **matching structure** — correction/hitting formulations;
7. **normalization** — discard every rescue pattern already consumed by R0-R6.

Cheapest decisive question:

[
oxed{
	ext{DOES EVERY MUS OF A NORMALIZED TIGHT BLOCK
HAVE A POLYNOMIALLY DISCOVERABLE
CIRCUIT-COMPATIBILITY SIGNATURE?}
}
]

If yes, the Boolean interface can be reduced to hitting polynomially represented signatures.

If no, the smallest counterexample tells us the next hidden distinction.

## 11. Claim ceiling

[
oxed{	ext{BOUNDARY RESCUE THEOREM = EXACT}}
]

[
oxed{	ext{CORRECTION-SET / MUS TRANSVERSAL FORM = EXACT}}
]

[
oxed{	ext{MINIMAL PAIR EXPLAINED EXACTLY}}
]

[
oxed{	ext{HIGHER-DEFICIENCY MUS = CROSS-CIRCUIT COMPATIBILITY OBSTRUCTION}}
]

[
oxed{	ext{POLYNOMIAL MUS SIGNATURE = OPEN}}
]

[
oxed{P=NP	ext{ remains unproved}.}
]
