# Positive-Circuit Cover Is Too Coarse — Higher-Order Circuit Compatibility Counterprobe

**Program:** synchronized P vs NP proof program  
**Predecessor:** `PNP_BOUNDARY_RESCUE_CORRECTION_SET_SEAM_2026-09-26.md`  
**Status:** exact bounded counterexample + exact higher-order circuit witnesses  
**Claim ceiling:** selected circuit-cover incidence is insufficient; full circuit structure may be stronger but is not proved sufficient

## 1. Target

The boundary-rescue theorem reduced the Boolean interface to:

[
alpha
mapsto
mathcal R(alpha)
mapsto
	ext{correction-set / MUS-transversal status}.
]

The positive-balance line supplied a selected cover of the clause set by support-minimal positive circuits.

Question:

> Is it enough to know which selected cover circuits a rescue set hits?

Answer:

[
oxed{	ext{NO}.}
]

## 2. Paired-NAE test block

Use seven Boolean variables (x_0,dots,x_6).

Let the 3-uniform hyperedges be:

[
egin{aligned}
e_0&=(1,2,6),\
e_1&=(0,1,3),\
e_2&=(0,1,5),\
e_3&=(2,3,6),\
e_4&=(0,2,4),\
e_5&=(1,2,3),\
e_6&=(0,2,5),\
e_7&=(0,3,6),\
e_8&=(1,4,6),\
e_9&=(1,2,5),\
e_{10}&=(3,4,5).
end{aligned}
]

For every hyperedge (e_j), include the opposite clause pair:

[
P_j=igvee_{vin e_j}x_v,
qquad
N_j=igvee_{vin e_j}
eg x_v.
]

Each pair ({P_j,N_j}) is a support-minimal positive 2-circuit of the signed clause matrix.

The eleven disjoint pairs give an explicit positive-circuit cover of all 22 clauses.

The full paired formula is UNSAT.

## 3. Same selected-cover signature, different correction status

Use two rescue sets:

[
R_{m SAT}={P_0,P_9},
]

[
R_{m UNSAT}={P_0,N_9}.
]

Both rescue sets:

- hit exactly the same selected cover circuits: (e_0) and (e_9);
- hit exactly one clause of each selected pair;
- leave every other selected pair untouched.

So the selected-cover hit signature is identical.

Yet exact truth-table evaluation over all (2^7=128) assignments gives:

[
Gsetminus R_{m SAT}in SAT,
]

with witness in ({pm1}^7):

[
(1,-1,-1,1,1,-1,-1),
]

while

[
Gsetminus R_{m UNSAT}in UNSAT.
]

Therefore:

[
oxed{
	ext{SELECTED POSITIVE-CIRCUIT COVER HIT PATTERN}

otRightarrow
	ext{CORRECTION-SET STATUS}.
}
]

## 4. Higher-order positive circuits see the lost polarity

The failure is not invisible to the **full** positive-circuit structure.

Using zero-based clause-row indices (P_0,N_0,P_1,N_1,dots), the following exact support is a positive row circuit:

[
Q_+
=
{1,5,8,11,13,14,18,21},
]

with positive dependence coefficients proportional to:

[
(2,1,1,1,2,2,4,1).
]

It contains row (18=P_9), but not row (19=N_9), and does not contain row (0=P_0).

Hence:

[
R_{m SAT}cap Q_+
eqarnothing,
qquad
R_{m UNSAT}cap Q_+=arnothing.
]

A second exact positive circuit is:

[
Q_-
=
{9,10,12,15,16,19},
]

with positive dependence coefficients proportional to:

[
(1,1,2,1,1,2).
]

It contains (19=N_9), but not (18=P_9), and not (0=P_0).

Thus:

[
R_{m UNSAT}cap Q_-
eqarnothing,
qquad
R_{m SAT}cap Q_-=arnothing.
]

So the larger positive circuits detect precisely the sign/polarity choice that the trivial pair-cover forgot.

## 5. What this bends open

The hierarchy is now:

[
	ext{CIRCUIT COVER MEMBERSHIP}
quad	ext{too coarse}
]

[
Downarrow
]

[
	ext{FULL POSITIVE-CIRCUIT ARRANGEMENT}
quad	ext{strictly richer}
]

[
Downarrow
]

[
	ext{MUS / MINIMAL SIGN-CENTRAL COMPATIBILITY}
quad	ext{exact correction obstruction}.
]

The hidden relation is not merely:

[
	ext{which circuits are touched}.
]

It includes:

[
oxed{
	ext{which signed clauses participate together
in higher-order positive dependencies}.
}
]

## 6. Connection to MUSes

The rescue theorem says a rescue set is a correction set iff it hits every MUS.

Within the qualitative-matrix dictionary, MUSes correspond to minimal sign-central column sets of the transpose signed matrix.

Therefore the exact remaining signature lies above ordinary row-matroid circuit incidence:

[
oxed{
	ext{POSITIVE LINEAR CIRCUITS}

eq
	ext{MINIMAL SIGN-CENTRAL OBSTRUCTIONS}.
}
]

For deficiency one these notions coincide.

For higher deficiency, a MUS contains a network of locally satisfiable positive circuits whose combined signed compatibility makes the whole support sign-central / UNSAT.

## 7. New nearest edge

Do not ask whether the selected circuit cover determines the Boolean interface. It does not.

Ask:

> Can the minimal sign-central / MUS obstruction structure be reconstructed in polynomial work from the **full positive-circuit arrangement plus normalization data**, without enumerating all MUSes?

Cheapest next falsification:

Find two rescue sets that have the same hit signature against **all** positive circuits but different correction status.

- If such a pair exists, even the full positive-circuit arrangement is too coarse.
- If no such pair exists and a theorem can be proved, correction status reduces to a positive-circuit signature problem.

No conclusion from the bounded search is promoted without that theorem.

## 8. Evidence boundary

[
oxed{	ext{SELECTED COVER INSUFFICIENT = EXACT COUNTEREXAMPLE}}
]

[
oxed{	ext{HIGHER-ORDER POSITIVE CIRCUITS DETECT THIS EXAMPLE = EXACT}}
]

[
oxed{	ext{FULL CIRCUIT SIGNATURE SUFFICIENT = OPEN}}
]

[
oxed{	ext{POLYNOMIAL MUS / MINIMAL SIGN-CENTRAL SIGNATURE = OPEN}}
]

[
oxed{P=NP	ext{ remains unproved}.}
]
