# Cubic Paired-NAE Future-Frontier Projection Carrier — 2026-09-26

**Predecessor:** PNP_CUBIC_BOND_LATTICE_CARRIER_2026-09-26.md  
**Program:** RMAL / P vs NP  
**Status:** scoped exact decision + Homeward theorem + bounded differential validation  
**Claim ceiling:** not a universal P=NP proof

## 1. One-degree repair

The signed partition-coefficient carrier still keeps equality coordinates for vertices after their last possible interaction with an unprocessed hyperedge.

That is unnecessary carrier mass.

Fix a stable hyperedge order

    e_1,...,e_m.

After processing the first i hyperedges define the future-active vertex set

    A_i = union_{j>i} e_j.

A vertex outside A_i cannot occur in any later hyperedge.

Therefore no future inclusion-exclusion transition can merge a connected/equality block that contains no A_i vertex with any later block.

Such a block is permanently closed.

The lawful one-degree repair is:

    coordinate becomes future-inactive
        ->
    remove it from the active partition
        ->
    if its whole block closes, charge its final color multiplicity exactly.

This moves the carrier, not the Object.

## 2. Decision-state invariant

For a processed-edge subset X subseteq {e_1,...,e_i}, let Pi_X be the full equality partition of all incident vertices induced by the selected hyperedges X.

Project Pi_X onto A_i:

- delete every inactive vertex from its block;
- discard blocks that become empty.

Call the projected partition

    frontier_i(X).

Let

    closed_i(X)

be the number of full blocks of Pi_X having no future-active vertex.

For q=2 define the signed frontier weight of active partition pi:

    w_i(pi)
      =
    sum_{X : frontier_i(X)=pi}
      (-1)^|X| 2^(closed_i(X)).

Thus each state already pays exactly for equality components that can never interact again.

## 3. Exact transition

Before processing e_i, every vertex of e_i is still active because e_i itself is unprocessed.

For every current state (pi,w), form the two exact Whitney directions:

    ABSENT:
        (pi, +w)

    PRESENT:
        (join(pi,e_i), -w).

Then project each resulting partition from A_(i-1) to A_i.

For every block that disappears completely, multiply its coefficient by 2.

Aggregate equal projected partitions and delete exact zero weights.

## 4. Correctness theorem

Induct on i.

At i=0 the only history is the empty selected-edge set with coefficient 1 and no closed nontrivial work.

Assume the state invariant holds for prefix i-1.

Every selected subset of the first i edges is uniquely either:

    X

or

    X union {e_i}

for one prefix subset X.

Their signs differ by exactly a factor -1.

The present branch merges precisely the equality blocks touched by e_i.

Projection removes only vertices that no future edge can touch.

A block projected to empty is a final connected component of the selected-edge subhypergraph, so it independently contributes exactly 2 binary colors.

Therefore the recurrence produces exactly the stated w_i.

After i=m:

    A_m = empty.

Every equality component is closed.

The unique empty frontier state has weight

    sum_{X subseteq E}
      (-1)^|X| 2^(components(V,X))
      =
    P_H(2),

the exact number of proper 2-colorings of H.

If the empty state's coefficient cancels to zero, H is not 2-colorable.

## 5. Zero-state deletion

All future operations are linear in the current weight.

Therefore:

    w_i(pi)=0
        ->
    no net contribution from that history class
    to either future signed direction.

The state may be removed.

A state with the same projected partition may later be regenerated from another nonzero predecessor and is retained normally.

## 6. Actual execution width

Define

    W_front(H,order)
      =
    max_i number of nonzero projected partition states after step i.

Do not replace this by frontier vertex count alone.

A frontier with b vertices can admit Bell(b) equality partitions, so small-looking coordinate count does not automatically imply polynomial state count.

Fix a polynomial admission cap

    P(N_input)=N_input^c.

Run with stable hyperedge order.

If the active nonzero state count exceeds P(N_input), stop and return UNRESOLVED.

If it never exceeds the cap, there are only m polynomial rounds, two transitions per state, polynomial partition operations, and O(n+m)-bit signed coefficients.

Hence:

    POLYNOMIAL ACTUAL FRONTIER-STATE WIDTH
        ->
    EXACT POLYNOMIAL 2-COLOR DECISION.

No optimal order is assumed.

## 7. Homeward cannot be inferred from the unlabeled projection

A closed block was paid by factor 2.

For later witness reconstruction, a partial coloring may already force that component to color 0 or 1.

So an unlabeled decision carrier alone does not satisfy the Homeward contract.

    DECISION COUNT
    !=
    WITNESS RECONSTRUCTION.

The repair is to carry one minimal color-status degree per active equality block during conditional-count queries.

## 8. Labeled frontier for a partial coloring

Fix a partial coloring alpha.

Each active partition block carries one status:

    UNFIXED
    COLOR_0
    COLOR_1.

The status records the color forced by every alpha-assigned vertex already known to lie in that full equality component, including assigned vertices that were later forgotten from the active frontier.

### Join

When PRESENT(e) merges blocks:

- UNFIXED + x -> x;
- COLOR_0 + COLOR_0 -> COLOR_0;
- COLOR_1 + COLOR_1 -> COLOR_1;
- COLOR_0 + COLOR_1 -> incompatible event, contribution 0.

### Close

When an equality block leaves the frontier:

    UNFIXED -> multiply by 2
    COLOR_0 -> multiply by 1
    COLOR_1 -> multiply by 1.

The same absent/present signed coefficient transition applies.

Therefore the final empty-state weight is exactly:

    number of proper 2-colorings extending alpha.

## 9. Homeward self-reduction

First run alpha=empty.

If the exact count is zero, return UNSAT.

Otherwise process vertices in stable-ID order.

For next vertex v:

1. set alpha(v)=0 temporarily;
2. run the labeled frontier conditional count;
3. if the count is positive, retain 0;
4. otherwise set alpha(v)=1 and verify positive extension count.

After at most n decisions, alpha is a proper 2-coloring.

### Fail-closed Homeward guard

Define

    W_home(H)
      =
    maximum labeled frontier-state count
    encountered across the actual self-reduction queries.

Use the same declared polynomial cap.

If any conditional query exceeds the cap:

    return UNRESOLVED under this full carrier.

Do not claim witness reconstruction merely because the unlabeled decision run was small.

Therefore the complete scoped terminal requires:

    W_front <= P(N)
    AND
    W_home <= P(N).

Under these guards:

- decision work is polynomial;
- witness reconstruction uses at most n+1 polynomial runs;
- trace size is polynomial;
- every original vertex color is Homeward-recoverable.

## 10. Knowledge-Decay interpretation

When a vertex disappears from the active frontier, its source identity is not deleted from history.

Only its no-longer-needed equality coordinate is removed from the hot carrier.

If its block remains open, any partial-color obligation is retained as the one-bit block status.

If its block closes, all future obligations are already discharged and its remaining color multiplicity is charged exactly.

Thus:

    NO FUTURE RELATION
        ->
    PROJECT COORDINATE

but:

    CONSEQUENCE STILL OPEN
        ->
    RETAIN MINIMAL STATUS.

This is active motion away from carrier decay, not lossy forgetting.

## 11. Alignment with established transfer-matrix methods

Connectivity-partition frontier states are standard in Fortuin-Kasteleyn / Potts-model transfer-matrix computation of chromatic and partition functions.

The present theorem specializes that idea to the paired-NAE hypergraph carrier and makes the proof-program obligations explicit:

- exact absent/present signed transitions;
- semantic equality-partition state identity;
- zero-state cancellation;
- one-coordinate future-inactive projection;
- actual state-count admission rather than width folklore;
- explicit Homeward reconstruction guard.

External examples include Salas-Sokal and Chang-Shrock transfer-matrix treatments of chromatic polynomials; no priority is claimed for the general frontier-connectivity principle.

## 12. Retained witnesses

Using the fixed edge orders in the current cubic artifacts:

| instance | global active coefficient width | projected decision width | labeled Homeward width observed | #2-colorings |
|---|---:|---:|---:|---:|
| Fano | 37 | 19 | 19 | 0 |
| full-rank SAT-7 | 32 | 14 | 17 | 14 |
| SAT girth-6 n=10 | 226 | 73 | 73 | 48 |

Projection is exact and materially smaller on these retained examples.

## 13. Bounded validation

### Decision panel

1,000 random connected simple cubic 3-uniform hypergraphs, 6-9 vertices:

    decision/count mismatches: 0.

Strongest observed reduction versus the global signed coefficient carrier:

    global max active width: 118
    projected frontier max width: 12
    exact #2-colorings: 58.

Witness hyperedges:

    (0,1,5)
    (0,1,6)
    (2,3,7)
    (1,4,6)
    (0,5,7)
    (4,5,8)
    (2,4,8)
    (3,7,8)
    (2,3,6).

### Homeward panel

A separate 1,000 random cubic-instance panel ran complete self-reduction through labeled frontier conditional counts.

Results:

    reconstruction failures: 0
    SAT/UNSAT mismatches: 0
    invalid returned colorings: 0
    maximum labeled frontier width observed: 66.

Finite panels are implementation evidence only.

## 14. Updated remainder

The cubic paired residual is now closed whenever the actual decision and Homeward frontier state counts stay within the admitted polynomial cap under the fixed charged order.

The surviving object is:

    EDGE-CRITICAL CUBIC 3-UNIFORM
    +
    SUPER-CAP PROJECTED FRONTIER STATE WIDTH
    OR
    SUPER-CAP LABELED HOMEWARD WIDTH.

This is still a scoped representation-growth remainder.

It is not an NP-hardness certificate and not a universal P=NP proof.

The next lawful degree should change the edge order or factor the incidence carrier only through a polynomially discoverable certificate; do not assume an optimal frontier order for free.

GENERATE != VERIFY != ADMIT.
