# Highest-view plan authority: executable local slice

Implements the authority-map / Knowledge Decay obligation from the highest-view plan
in `redogit/redogit` PR #42, with its directly dependent local lineage view.
This is an offline navigation and assessment tool, not a replacement for RMAL,
SOII, a native project runtime, a file-parity verifier, or a command center.

## Start here

Python 3.10 or newer, standard library only. Run from the repository/package root:

```sh
python3 -m unittest discover -s tests -v
python3 tools/plan_authority.py graph plan-authority/example-overlay.json > graph.json
python3 tools/plan_authority.py validate graph.json
python3 tools/plan_authority.py next graph.json --actions plan-authority/example-actions.json
python3 tools/plan_authority.py restore graph.json > restored.json
```

The example is entirely synthetic. The real local authority overlay is deliberately
not in this repository. To use it, supply its exact local filename to `graph`.
The command reads only the named file, writes only to standard output, defaults
to a private source label, and never scans a Library, repository, or home directory.
Shell redirection in these examples is the caller's explicit file-write operation.
Do not redirect output over an input or an existing evidence record.

## Graph and reconstruction

Accepted input schema: `rmal/plan-authority-overlay/v1`.
Output schema: `redogit/plan-lineage/v1`.

The graph retains the exact original UTF-8 source, including whitespace and line
endings, plus its byte digest. Each derived node has an exact JSON source pointer;
relations are typed navigation links, not claims of support, proof or authority.
Reconstruction recomputes the projection and rejects altered source, nodes,
relations, flags or unexpected envelope fields. The original source is unchanged.
Unknown source annotations are retained verbatim and marked uninterpreted.

The states deliberately have different scopes:

- `current`: current *planning* obligations or explicit overlay, not completed code;
- `historical`: predecessor/reference or retained base-plan snapshot;
- `superseded`: only the **base-only priority** when `override_applied` is explicit;
- `coexisting`: independent native-workstream or shared-method references;
- `retained`: parked/retained lineage, never silently reactivated.

Superseding a base-only priority does not retire its entire route. Base obligations,
reported failures, unresolved statements, source-native labels, and claim ceilings
remain in the unchanged input. A declared predecessor digest does not authenticate
missing predecessor bytes; the remainder reports that distinction explicitly.

Graph node IDs identify positions within this projection. The portfolio's original
native IDs and other source-native identities remain recoverable through pointers.
Do not interpret reordering of address-like node IDs as a change of native identity.

## Action assessment

`next` reads an explicit array of `redogit/action-proposal/v1` records. The complete
synthetic proposal illustrates the fields. A result carries a deep copy of the
proposal and the exact input-source digest so expectation, observation,
usefulness, counterprobe and Way Back are not detached from the decision.

The assessor rejects declared permission denial, rejected target decisions,
unbounded or unreconstructible actions, and a public privacy downgrade from a
nonpublic graph. It defers missing/moved revisions, missing native state, unknown
permissions/privacy/delta, unmet dependencies and conflicting active writers.
A repair needs a target-local acceptance reference. Current, revision-consistent
zero-delta and already-merged repair observations yield `no_change`.
**Stale observations cannot establish even a no-change decision.**

Merge, release and publication require separate operation gates and are never
executed here. Even `candidate` grants no authority and performs no operation.
All inputs about permissions, acceptance, evidence and identity remain caller
statements; this tool does not authenticate people, GitHub receipts or source
content. `declared != authenticated` is part of every result.

Priority indexes refer to the source's explicit priority list. Their association
with a native workstream must be reviewed by the caller; the tool does not guess
that association from natural-language names. Selection follows supplied indexes,
then stable action IDs, and reports `priority_binding_authenticated: false`.
It is a deterministic candidate ordering, not a claim of optimality or authority.

## Privacy and export

The graph contains the **whole source**. Treat it as at least as private as that
source. A nonpublic graph cannot be exported by `public`, even with the approval
flag. A graph declared public additionally requires an explicit local projection
approval flag:

```sh
python3 tools/plan_authority.py public reviewed-public-graph.json --public-projection-approved
```

This only emits JSON; it does not publish. Privacy labels and the flag are caller
declarations, not a privacy scan, authenticated consent, or declassification.
Do not label private, private-derived or unreviewed material public. No real user
input, private retrieval locator, private source hash or derived local graph is
included in this source distribution.

## Verification and limits

The new slice has synthetic unit, malformed-input, tamper, stale-revision,
no-overwrite, privacy, concurrency, exact-roundtrip and CLI controls. CI runs
against the exact PR head with zero configured repository permissions, without
third-party Actions. All direct inputs and the workflow itself trigger its gate.

The execution container's direct Git networking failed DNS resolution. Local
verification therefore covers this additive package, not a complete repository
checkout or the pre-existing profile workflow. CI and independent review remain
separate admission evidence. Hostile concurrent filesystem mutation, cross-platform
screen-reader/device behavior, native compiler conformance, and mathematical
claims are not established by these tests. Input size and nesting are bounded.

No predecessor plan, existing interface, current-authority pointer, publication
projection, research evidence or native implementation is edited by this slice.
Removal of these additive files is its rollback; retain private inputs and receipts.

`PLAN != SOLUTION`
`GENERATE != VERIFY != ADMIT`
`BYTE_IDENTITY != SEMANTIC_TRUTH`
`RELATED != AUTHORIZED_TO_EDIT`
`DELTA_ZERO -> NO_CHANGE`
