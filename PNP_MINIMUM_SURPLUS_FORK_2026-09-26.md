# Minimum-Surplus Fork — Autarky or Internal Projection — 2026-09-26

**Program:** synchronized P vs NP proof program
**Predecessor:** `PNP_SURPLUS_INFLATION_COUNTERPROBE_2026-09-26.md`
**Status:** exact structural fork; constructive separator open
**Claim ceiling:** not universal P=NP

## 1. Object

For a current clause-set F with variables, choose a nonempty variable set V realizing surplus:

    delta(F[V]) = sigma(F).

Here F[V] is the standard restriction to clauses touching V, with literals outside V removed and multiplicity preserved where required.

Call V a minimum-surplus / tight variable Object.

Because V realizes the global minimum, restriction preserves the surplus value:

    sigma(F[V]) = delta(F[V]) = sigma(F).

## 2. Exact fork

Exactly one of the ordinary truth cases holds.

### Door A — F[V] is satisfiable

Let alpha be any satisfying assignment of F[V].

Every original clause touching V restricts to a clause in F[V], and alpha satisfies that restricted clause using a literal whose variable lies in V.

Therefore alpha satisfies every original clause it touches.

Hence alpha is an autarky of F with variable domain contained in V, and all clauses touched by V may be removed satisfiability-equivalently.

Thus:

    SAT TIGHT OBJECT
    -> AUTARKY REMOVAL.

### Door B — F[V] is unsatisfiable

Since:

    sigma(F[V]) = delta(F[V]),

take a minimally unsatisfiable sub-clause-set H subseteq F[V].

The standard minimum-surplus lemma implies:

    var(H)=V.

Let:

    k = delta(F[V]) = sigma(F).

The non-Mersenne minimally-unsatisfiable degree theorem applied to H yields some v in V with:

    vd_H(v) <= nM(delta(H))
    and each literal degree <= delta(H).

Degree transfer from H through F[V] back to F gives the standard bound:

    vd_F(v) <= nM(k)

with the corresponding literal-degree control from the Kullmann-Zhao proof.

Therefore:

    UNSAT TIGHT OBJECT
    -> CONTROLLED LOW-DEGREE VARIABLE INSIDE V.

## 3. Why this matters for surplus inflation

The earlier surplus-inflation counterexamples eliminated variables outside the minimum-surplus witness that was destroyed.

The fork gives a principled alternative:

    SELECT INSIDE THE TIGHT OBJECT.

If Door A holds, remove the tight block by autarky.

If Door B holds, project a controlled-degree variable from inside the tight block.

This aligns the projection coordinate with the edge being preserved.

## 4. Constructive gap

The theorem is structural, not yet an algorithm for the fork.

We still need a polynomial procedure that, given F and a polynomially found minimum-surplus V, returns one of:

    AUTARKY(V)
or
    INTERNAL_LOW_DEGREE_PROJECTION(v in V)

with enough evidence to justify the selected move.

Merely deciding SAT(F[V]) by a general SAT solver is circular for the P-vs-NP obligation.

Likewise, invoking a general autarky oracle is circular.

The known MLCR/autarky literature is related but not identical to this R6-fixed-point fork; do not conflate them.

## 5. Candidate total-search formulation

Define:

    TIGHT_EDGE(F,V)

Input:
    clause-set F
    minimum-surplus witness V.

Required output:

A.
    satisfying assignment alpha of F[V],
    which verifies as an autarky of F;

or B.
    a certified internal variable v in V,
    together with a polynomially admissible exact projection/removal receipt.

The structural theorem guarantees Door A or the existence of a low-degree v under Door B.

The missing issue is obtaining the correct useful output without first solving the same hidden Boolean obligation.

## 6. Surplus-atlas carrier

For each variable r define rooted surplus:

    sigma_r(F)
      =
    min_{S contains r} |Gamma(S)|-|S|.

Then:

    sigma(F)=min_r sigma_r(F).

For fixed r, the objective is submodular under the anchored domain; minimizers have lattice closure.

Candidate compact carrier:

    ROOTED_SURPLUS_ATLAS {
        r,
        sigma_r,
        canonical minimal anchored minimizer,
        canonical maximal anchored minimizer
    }.

This is intended to preserve where the current low-expansion edges live rather than retaining only scalar sigma.

The ordinary Dulmage-Mendelsohn theory confirms the underlying submodular/lattice geometry for f(S)=|Gamma(S)|-|S| in bipartite graphs. The anchored adaptation still requires target-local verification for the exact carrier operations we use.

## 7. Counterprobe status

Rooted surplus values are not monotone under arbitrary DP.

Finite exact search found surviving-variable rooted values that both increase and decrease after elimination.

Therefore:

    ROOTED SURPLUS SCALAR != MONOTONE POTENTIAL.

The atlas is a navigation carrier, not yet a progress proof.

## 8. New nearest edge

The core no longer asks:

    WHICH ARBITRARY LOW-DEGREE VARIABLE DO WE ELIMINATE?

It asks:

    CAN WE SOLVE TIGHT_EDGE(F,V)
    IN POLYNOMIAL WORK?

Equivalent operational wording:

> For a minimum-expansion variable block, can we either expose its removable satisfying side or expose an internally projectable obstruction side without Boolean branching?

## 9. Next one-degree probes

Attack the fork using independent carriers:

1. qualitative/sign-central matrix of F[V];
2. positive-balance circuits restricted to clauses touching V;
3. matching / DM-style decomposition of the incidence subgraph;
4. exact low-degree structure inside V;
5. counterexamples where all four carriers agree but Door A/B differs.

The cheapest defeating counterpair has priority.

## 10. Claim ceiling

    MINIMUM-SURPLUS FORK = EXACT
    SAT DOOR -> AUTARKY = EXACT
    UNSAT DOOR -> INTERNAL LOW-DEGREE EXISTENCE = EXACT
    POLYNOMIAL FORK SEPARATOR = OPEN
    ROOTED SURPLUS ATLAS = CANDIDATE CARRIER
    UNIVERSAL P=NP = OPEN

    EXISTENCE OF TWO DOORS != CHEAP DOOR SELECTION
    NAVIGATION CARRIER != PROGRESS POTENTIAL
    GENERATE != VERIFY != ADMIT
