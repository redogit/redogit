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
6. **Retain** — keep predecessor, failure, and provenance in history.
7. **Continue** — extend only when the next difference earns the extra complexity.

## What REDOGIT rejects

- pretending old mistakes never happened;
- copying accidental architecture forward because it is already there;
- mixing unrelated projects because their names overlap;
- opaque generated dumps when a smaller reconstructible source exists;
- calling something complete without an observable completion condition.

## What REDOGIT keeps

- useful ideas;
- authorship and upstream attribution;
- failures as evidence;
- small testable cores;
- explicit successors;
- freedom to redo the successor again.

Git is not only where the finished answer goes. It is the lineage of learning how to make the answer better.
