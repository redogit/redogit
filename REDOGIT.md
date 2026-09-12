# REDOGIT

`redogit` is the working rule for these repositories:

> **Do it. Inspect what happened. Preserve the history. Redo the smallest thing that matters better. Verify the successor. Repeat.**

A redo is not a clean-room claim that the earlier work never existed. Git already gives us the right machinery: history, diffs, branches, commits, and successors.

## The loop

1. **Input** — load the actual code, artifact, failure, or idea that exists.
2. **Boundary** — identify what the project is responsible for and what it is not.
3. **Difference** — find the consequential defect, dependency, ambiguity, or missing behavior.
4. **Redo** — build the smallest coherent successor that addresses that difference.
5. **Check** — make the important behavior observable and executable where possible.
6. **Promote** — call a successor `current` only after its declared check passes. An unverified successor is a candidate, not the current answer.
7. **Retain** — keep predecessor, failure, and provenance in history.
8. **Continue** — extend only when the next difference earns the extra complexity.

## Repository contract

A repository may expose its current state in `redogit.json`, governed by `REDOGIT.schema.json`.

The contract states:

- which successor is current;
- where it lives;
- how to build and verify it, when applicable;
- which predecessors remain retained;
- what the repository owns and explicitly does not own;
- whether an external blocker prevents normal verification.

For executable repositories, the shared reusable workflow `.github/workflows/verify-redogit.yml` validates the contract and executes the declared build and verification commands. Callers should pin a tested commit of that workflow rather than follow a moving branch implicitly.

A repository with an external runner or service blocker must record the blocker rather than manufacture a green status. A provenance-only fork may declare `provenance-boundary` and verify attribution/boundary without pretending inherited code has been rebuilt.

## Promotion invariant

The current pointer moves forward only after evidence exists:

`predecessor -> bounded difference -> candidate successor -> declared check -> PASS -> current successor`

If the check fails:

`candidate successor -> failure evidence -> next bounded redo`

The predecessor is not rewritten to hide the failure, and a failed candidate is not promoted by documentation alone.

## What REDOGIT rejects

- pretending old mistakes never happened;
- copying accidental architecture forward because it is already there;
- mixing unrelated projects because their names overlap;
- opaque generated dumps when a smaller reconstructible source exists;
- calling something complete without an observable completion condition;
- declaring a successor current before its own declared verification passes;
- hiding external blockers behind false or unrelated green checks.

## What REDOGIT keeps

- useful ideas;
- authorship and upstream attribution;
- failures as evidence;
- small testable cores;
- explicit successors;
- machine-readable current-state contracts;
- freedom to redo the successor again.

Git is not only where the finished answer goes. It is the lineage of learning how to make the answer better.
