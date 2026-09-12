# redogit

## Do it. Inspect it. Redo it better.

`redogit` is my public working rule: preserve what actually happened, keep the useful part, rebuild the smallest thing that matters, verify the successor, and keep going.

Git history stays history. A redo is a successor, not a rewritten past.

See **[REDOGIT.md](REDOGIT.md)** for the rule. Repositories can expose their current successor through a machine-readable **`redogit.json`** contract defined by **[REDOGIT.schema.json](REDOGIT.schema.json)**.

## Current public projects

- **[Conscience64](https://github.com/redogit/conscience64)** — Privacy-safe static research space and Cross-Carrier / Float64 work. Its current contract favors compact source, provenance, manifests, regeneration, and runner-independent integrity checks. GitHub Actions job scheduling remains an external blocker for this repository, so that blocker is recorded rather than hidden.
- **[MauiBrickBreak](https://github.com/redogit/MauiBrickBreak)** — The .NET 6 MAUI/Orbit game remains as history. Current v2 is a reusable .NET 10 game core plus a separate verifier for wall, paddle, block, and ball-loss consequences. Its root solution and CI are green.
- **[FirstNeuralNetwork](https://github.com/redogit/FirstNeuralNetwork)** — The original C# experiment remains as history. Current v2 is a reusable deterministic .NET 10 logistic-neuron library plus a separate OR-classification verifier. Its root solution and CI are green; earlier ACDN successor work remains preserved too.
- **[Orbit Engine](https://github.com/redogit/orbit)** — My upstream-derived fork of [bijington/orbit](https://github.com/bijington/orbit). Its REDOGIT contract is intentionally a provenance boundary: upstream authorship remains upstream, and this fork remains separate from the unrelated Orbit Lab research lineage.

## The current pattern

`actual predecessor → bounded difference → successor → reusable core → separate verifier → observable result → retained lineage → next successor`

The declaration of “what is current” is part of verification too. For code repositories, CI parses `redogit.json`, builds the root `REDOGIT.slnx`, then executes the successor contract.

## Free Use!

The original text and code of this homepage are free to use, copy, modify, and share, including for commercial purposes. Attribution is welcome, but not required. Linked projects and third-party material keep their own licensing terms.

---

[Standalone homepage](index.html) · [REDOGIT contract](redogit.json) · [Publishing instructions](PUBLISHING.md) · [Browse repositories](https://github.com/redogit?tab=repositories)
