# Project Page Source Verification — 2026-10-02

**Result:** PASS after source repairs.

This receipt verifies the project-page inventory against the repository sources that actually own the claims. It is not merely a link check.

## Acceptance evidence

- **Structural page/source audit:** [run 37095881692](https://github.com/redogit/redogit/actions/runs/37095881692) — SUCCESS
- **Semantic source contract:** [run 37095881688](https://github.com/redogit/redogit/actions/runs/37095881688) — SUCCESS
- **Repository-level live Pages graph:** [run 37095243715](https://github.com/redogit/redogit/actions/runs/37095243715) — SUCCESS
- **Main / Dream route verification:** [run 37095243708](https://github.com/redogit/redogit/actions/runs/37095243708) — SUCCESS
- Registry under test: `PROJECT_PAGES.json@302d84d486fbf04155fdb612014f6c525222255e`

## Scope

39 declared project pages:

- 6 current live projections
- 23 current source-only surfaces
- 5 historical or bounded snapshots
- 2 current source-preserved predecessors
- 1 current reference surface
- 2 redirects

## Authority used

1. Current repository root README / current manifest controls present publication and status.
2. Project README / contract / `CURRENT` file controls project-specific claims.
3. Executable implementation controls concrete implementation facts when prose is stale.
4. Source-native HTML may be runnable without being a current Pages route.
5. Dated snapshots remain preserved but must point forward to current authority.
6. Standalone export copies do not override source-native authority.

## Material corrections made

### Conscience64 About
The old “eight repositories” page was a September 13–14 snapshot. It is now explicitly labeled historical and points to `redogit/redogit` for the current account-level project inventory.

### Current Pages versus repository source
The current Conscience64 Pages contract is the generated curated projection, not the whole repository. The Play hub, Musilanguage, and NEON//VEIL are curated base routes; Dream is a separately approved overlay. Source/local projects such as Analytics, Coordinate Space, Explorer World, MMO World predecessors, advanced MMO, and research-update interfaces no longer claim current Pages publication.

### Dated research/UI checkpoints
S′1 Experiment 0, the September 14 PNP discriminator, September 25 PNP Live Design, and September 29 Recent Work retain their bodies but are explicitly scoped as historical/bounded/reference snapshots.

### History repository count
The current History & Restore repository catalog now contains the 16 public repositories visible on October 2, 2026. Older smaller counts remain untouched inside dated historical records.

### MMO activity-count repair
`play/mmo/simple/core.mjs` contains **12** concrete activities. The old `CURRENT.md` prose still described a 10→12 gap. It now distinguishes:
- the richer advanced surface: 4 built-in + 6 optional Starter Pack slots;
- the current primary Simple Core: full 12-activity direct mix, including **Sidewalk Slalom** and **Parcel Relay**.

### Portfolio source map
The current navigation authorities are `PUBLIC_PAGES.json` and `PROJECT_PAGES.json`. The older organization tree survives inside the Portfolio export and is labeled exported history rather than canonical current redogit source.

## Claim ceilings confirmed

- **P vs NP:** open.
- **Hodge conjecture:** open.
- **W114 Perturbation Lab:** game/visual carrier; score and robustness are not algebraic-cycle evidence.
- **Dream to Action:** repository source, project landing, and operational public app are distinct roles.
- **RMAL:** canonical Git home is `redogit/DnD`; current language implementation contract is ISO C23.
- **Fuzzball Hidden Game:** intentionally unlisted; distinct from the unresolved historical Fuzzball carrier.
- **Conscience64 Pages:** public projection != repository authority.

## Exact source heads

```text
redogit/conscience64@main ea546a415261ca21ae3be39dbe070e8ecade19f6
redogit/Other-Projects-@main 547c6001b628ab47472dee2c8d8b47cb241646f8
redogit/redogit@main 302d84d486fbf04155fdb612014f6c525222255e
redogit/Dream-To-Action@main f31e80176029e0922c1394d8d4d77f9e837fd83a
redogit/DnD@master f4aef51833103cc182faf893b70786fef4f91bb6
redogit/pnp-dean@main 2134a06657f5195b8209cd6874e27c6dffea4d0e
redogit/hodge@main f9e6ab78cbfbd309f9f014c20a88565ce00905c2
redogit/conscience64-platform@main 3433a2719d6261a0f470f9551a2de61610f0d92e
redogit/games@main d5b4c3c690e69381ff31db2f98e124298b6d02d1
redogit/language-carriers@main d8e9f2c0ec680f893d307b5636a3a5450a47cef9
redogit/archives-knowledge@main 69ad42991b9debaf8a0bc415e8baf2cdb11f8542
redogit/portfolio@main c1370265cb002e5a405468fce7f0296fc76e193e
redogit/orbit@main dc8e0c5f23745a5e12693e7cd122bc646c934a11
redogit/MauiBrickBreak@master ce162bb1a0e51d5608cfcdbf2b0391b61ef74061
redogit/FirstNeuralNetwork@master bd80601d641ddaa00c492c93894e2afec33f5558
redogit/RMAL@main 235e2a29b09e757e14aa253fca417a2142f1f3d4
```

## Remainder

No semantic mismatches remain from this verification pass.

This does **not** claim that every historical file in every repository has been modernized. Historical snapshots, reference implementations, visual samples, generated/export copies, and provenance copies intentionally remain historical where their identity matters.
