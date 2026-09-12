# redogit

## Do it. Inspect it. Redo it better.

`redogit` is my public working rule: preserve what actually happened, keep the useful part, rebuild the smallest thing that matters, verify the successor, and keep going.

Git history stays history. A redo is a successor, not a rewritten past.

See **[REDOGIT.md](REDOGIT.md)** for the rule. Repositories can expose their current successor through a machine-readable **`redogit.json`** contract defined by **[REDOGIT.schema.json](REDOGIT.schema.json)**.

## Use it locally

From a clone of this profile repository, the small Python CLI can inspect any local REDOGIT repository:

```bash
python tools/redogit.py status /path/to/repository
python tools/redogit.py check /path/to/repository
python tools/redogit.py run /path/to/repository
```

- `status` reads the current successor, retained predecessors, boundary, and any recorded blocker.
- `check` validates the REDOGIT invariants without executing project code.
- `run` validates the contract and then executes its declared build and verification commands.

GitHub repositories can use the shared reusable workflow `.github/workflows/verify-redogit.yml`. Current callers pin a tested commit rather than following a moving branch implicitly.

## Current public projects

- **[Conscience64](https://github.com/redogit/conscience64)** — Privacy-safe static research space and Cross-Carrier / Float64 work. Its current contract favors compact source, provenance, manifests, regeneration, and runner-independent integrity checks. A fresh reusable-workflow caller reproduced the repository's zero-job `startup_failure`, so that external scheduling blocker remains recorded instead of being hidden behind a false green check.
- **[MauiBrickBreak](https://github.com/redogit/MauiBrickBreak)** — The .NET 6 MAUI/Orbit game remains as history. Current v2 is a reusable .NET 10 game core plus a separate verifier for wall, paddle, block, and ball-loss consequences. Its root solution and pinned shared REDOGIT gate are green.
- **[FirstNeuralNetwork](https://github.com/redogit/FirstNeuralNetwork)** — The original C# experiment remains as history. Current v2 is a reusable deterministic .NET 10 logistic-neuron library plus a separate OR-classification verifier. Its root solution and pinned shared REDOGIT gate are green; earlier ACDN successor work remains preserved too.
- **[Orbit Engine](https://github.com/redogit/orbit)** — My upstream-derived fork of [bijington/orbit](https://github.com/bijington/orbit). Its REDOGIT provenance contract is green and keeps upstream authorship separate. The inherited .NET 6 engine build is being treated independently as predecessor evidence and repaired only through explicit local deltas.

## The current pattern

`actual predecessor → bounded difference → candidate successor → declared check → PASS → current successor → retained lineage → next bounded difference`

The declaration of “what is current” is part of verification too. For current C# successors, a small caller invokes the pinned shared workflow; that workflow reads `redogit.json`, validates the invariant, builds the declared root solution, and executes the declared verifier.

## Free Use!

The original text and code of this homepage are free to use, copy, modify, and share, including for commercial purposes. Attribution is welcome, but not required. Linked projects and third-party material keep their own licensing terms.

---

[Standalone homepage](index.html) · [REDOGIT contract](redogit.json) · [REDOGIT schema](REDOGIT.schema.json) · [Publishing instructions](PUBLISHING.md) · [Browse repositories](https://github.com/redogit?tab=repositories)
