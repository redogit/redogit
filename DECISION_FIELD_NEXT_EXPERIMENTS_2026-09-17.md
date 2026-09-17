# Decision Field Next Experiments — 2026-09-17

The framework is now parameterized and federated. Next work should test whether it earns anything beyond reorganizing terminology.

## E1 — Cross-domain reconstruction

Take one frozen task from each of:

- SAT / DEAN;
- GSFL;
- Orbit recovery;
- Dream to Action;
- one software behavior contract.

Encode each only through `DF=(X,O,D,R,F,E,G,U)` plus registered operators. Verify that the encoded run reconstructs the original result and claim boundary without hidden project-specific state.

Failure condition: the shared core must be expanded with ad-hoc project semantics until it simply restates each project.

## E2 — Operator portability

For each operator proposed for transfer between domains, record:

```text
source preconditions
target preconditions
preserved invariants
relation-type equivalence or mismatch
new verifier
failure witness
```

Do not count shared names as portability.

## E3 — Decision-field compression

Compare:

```text
original project-specific state carrier
vs
Decision Field encoded carrier
```

Measure:

- reconstruction correctness;
- hidden context required;
- number of consequential distinctions preserved;
- planning/verification cost;
- representation size.

No compression claim without matched output correctness.

## E4 — Gyroscopic scheduler

On GYRO-DEAN bounded panels, compare:

- fixed carrier order;
- gain/cost scheduler;
- exact-rank nullspace scheduler;
- branch-only baseline.

Track total planning + transform + verification + materialized-carrier cost, not solver core time alone.

## E5 — Quantum structural counterprobe

Use a small standard quantum measurement example solely to test the abstraction boundary:

- represent state/context/outcome update through Decision Field;
- ensure Born probabilities and quantum state update remain supplied by the quantum-domain operator;
- construct a classical stochastic model with the same outer field topology;
- verify the core does not confuse the two mechanisms.

Success means the abstraction preserves the difference. It does not constitute new quantum physics.

## E6 — Backward reconstruction

Select older pre-Decision-Field artifacts and ask whether a fresh reader can reconstruct the modern parameterization from their actual consequence/distinction/operator structure without using current terminology as an answer key.

This is the strongest test against retrospective vocabulary contamination.
