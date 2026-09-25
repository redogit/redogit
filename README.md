# redogit

> **Public projection status — 2026-09-18:** Conscience64 GitHub Pages is intentionally held at a minimal privacy surface pending explicit owner approval of an exact reviewed revision. Project/research state is independent of public availability. Public URLs are projections, not canonical authority.


## About me

I’m a data specialist, reverse engineer, and generalist builder. I take complicated systems apart, look for the distinction that actually changes the result, and try to turn what survives into something people can inspect, reuse, and improve.

The central idea behind my work is simple to state and large in consequence:

**higher organization = differentiation + relation + coordination**

I am interested in how this pattern scales outward: from bounded self-maintaining cells, to multicellular organisms, to animals acting in environments, to social coordination, language and culture, technical extension, distributed human-machine cognition, civilization, planetary coupling, meta-coordination, and collective self-modeling.

I do **not** treat those levels as literally identical. A civilization is not simply a giant animal, and a machine is not made equivalent to a person by participating in a feedback loop. The structural question is more careful: how can heterogeneous components retain their distinctions while coordinating well enough to sense, distinguish, remember, model, value, act, repair, learn, and reorganize together?

That is the technical **we** I want my work to help: humans, animals and other living systems, tools and machines, institutions, durable information, networks, and environments working together without erasing agency, boundaries, provenance, or evidence. The higher-level whole should not require its parts to become the same.

A recurring working motif is:

`SENSE → DISTINGUISH → REMEMBER → MODEL → VALUE → COORDINATE → ACT → REPAIR → LEARN → REORGANIZE`

At the highest level I currently use, **adaptive organization** means the ability of a system to modify its own organization while preserving enough continuity to remain meaningfully the same system. That turns a decision field into something stronger: a field capable of changing its own decision operators.

My work crosses software, language, knowledge organization, accessibility, games, mathematics, and experimental research. The common thread is human-directed problem solving: preserve context, make assumptions visible, keep provenance, test bounded changes, and do not confuse a useful representation with proof.

I expect my working model to change. Better evidence can change my mind; negative results can change the design; an interpretation error becomes part of the record rather than something to hide.


## September 25, 2026 — P vs NP proof-program checkpoint

The current P-versus-NP research line is being carried forward as an **exact obligation-preserving proof program**, not as a solved claim. The working Dean/Independent-Set obligation is used as the concrete NP-complete carrier.

Current proof architecture:

```text
ORIGINAL OBLIGATION
→ four-ID semantic catalog
→ bounded-arity exact facts
→ one signed degree of change
→ minimal dynamic repair
→ Homeward reconstruction
→ verified residual
```

Each semantic object/relation is tracked through four distinct ID roles:

```text
OccurrenceID
SemanticObjectID
SemanticContextSupportsIDs
SemanticClarityIDs
```

The active anti-decay rule is:

```text
OBJECT / OBLIGATION STAYS
CARRIER MAY MOVE
MOVE AWAY FROM IRREVERSIBLE KNOWLEDGE LOSS
```

The current one-degree progress carrier maintains a certified interval

```text
L <= alpha(G) <= U
```

for the graph independence number. A positive move is an exact augmentation `L -> L+1`; a negative move is a certified upper-bound improvement `U -> U-1`. Inclusion-minimal augmentation gives an exact +1 move whenever a larger independent set is available, but finding such a move is not yet proved polynomial on arbitrary graphs. Existing exact scoped negative carriers include LP/dual and odd-cycle support-frame bounds.

The semantic-event/storage side has been narrowed substantially: under a fixed finite bounded-arity vocabulary, the number of possible authoritative semantic facts is polynomial in the catalog domain size. This controls storage/fixed-point event growth, but **does not by itself prove obligation completeness**.

Current universal proof obligation:

```text
For every unresolved Dean / Independent-Set state with L < q <= U,
produce in polynomial total cost either:

  (+) a certified exact augmentation L -> L+1

or

  (-) a certified exact upper-bound improvement U -> U-1

while preserving the original obligation, provenance, exactness,
Knowledge-Decay protections, and Homeward witness reconstruction.
```

If that signed-progress theorem is proved uniformly, the gap `U-L` can shrink at most `n` times, yielding a polynomial exact Independent-Set solver and therefore `P = NP`.



Current refinement: relative to a present independent cohort `S`, the candidate-to-`S` support graph defines a **transversal matroid**: a candidate subset is matroid-independent exactly when it can be matched into `S`. A +1 augmentation exists exactly when this matroid has a circuit that is also independent in the candidate-candidate conflict graph. Every such circuit has support deficiency exactly one and replaces its supported members of `S` with one additional candidate. The uniform-transversal special case recovers ordinary size-`k` Stable Set, so this positive augmentation subproblem is itself a genuine hardness locus rather than a hidden matching shortcut.

A new scoped exact carrier is now recorded in [Signed Binary-Cluster Augmentation Carrier](PNP_SIGNED_BINARY_CLUSTER_CARRIER_2026-09-25.md). When the support matroid has an exact binary GF(2) representation of rank r and the candidate conflicts form exactly r disjoint cliques, one arbitrary rainbow transversal either is already dependent or becomes a basis. In basis coordinates, a zero same-color diagonal coordinate gives an immediate positive circuit; otherwise an off-diagonal color-dependency digraph controls the result. A shortest directed cycle constructs a singular rainbow transversal and therefore an exact +1 augmentation, while an acyclic dependency digraph makes every rainbow transversal unit-triangular and certifies that no +1 augmentation exists. This is polynomial inside its stated scope. A separate exhaustive canonical check covered 262,160 rank-2/rank-3 configurations with zero mismatches; that finite check supports the implementation logic but is not the proof.

The same carrier now has an exact **log-cluster-defect extension**. Candidate-conflict vertices that obstruct cluster structure are retained as an explicit exception carrier Z rather than semantically deleted. Stable choices A⊆Z are enumerated, chosen exceptions are contracted in the binary support matroid, and the remaining cluster carrier is solved exactly when its nonempty clique count is at least its residual matroid rank. With |Z|=O(log n), Cluster Vertex Deletion plus the 2^|Z| exact exception branches remains polynomial. Branches with fewer residual cliques than residual rank remain explicitly UNRESOLVED.

A further support-side admission theorem removes another hidden representation cost: when the candidate→current-cohort support graph is a bipartite forest, its ordinary 0/1 adjacency matrix is an exact GF(2) representation of the support transversal matroid. Matching a candidate subset into the current cohort is equivalent to linear independence of its adjacency columns; uniqueness of perfect matchings in a forest prevents determinant cancellation. This lets the binary signed carrier operate directly on original Dean relations for that family.


A 2026 external result also aligns two previously separate repair families: vertex-packing LP structure and critical-independent-set structure are equivalent views of the same independence machinery. Accordingly, LP persistency / crown / critical-set extraction are treated as one saturated degree family before moving to independent carriers such as odd-cycle frames, matching/min-cut structure, rank, and signed residual repairs.

**Current mathematical status remains open.** Scoped carrier theorems, finite computations, codecs, semantic compression, and successful special cases are not promoted into a universal P=NP claim.


## September 18, 2026 convergence

The current forward-only convergence pass is governed by [GITHUB_CONVERGENCE_PLAN_2026-09-18.md](GITHUB_CONVERGENCE_PLAN_2026-09-18.md). Its exact-head verification and closure evidence are recorded in [GITHUB_CONVERGENCE_RESULT_2026-09-18.md](GITHUB_CONVERGENCE_RESULT_2026-09-18.md).

Current successor state includes:

- **RMAO** as the active game/world target;
- **RMALKDVMLLL** as the broader VM/link-layer framework;
- **RMAPL / Ω** as the domain-first repair/fitting design surface, with implementation still evidence-gated;
- **Dynamic RMAL** as a bounded dynamic game/state contract surface for the RMAO character system;
- **Super Seraphine** as a fictional magic trickster character whose presentation may vary broadly without gaining server/admin or real-world identity authority;
- **Sproutling** as a fictional game growth-form with no real-age or real-family mapping.

Privacy remains a hard publication gate:

```text
PUBLIC_REPOSITORY != PRIVATE_FAMILY_CONTEXT
GAME_CHARACTER != PRIVATE_PERSON
SPROUTLING != REAL_CHILD
PSEUDONYM != IDENTITY_DISCLOSURE
```

This section succeeds the September 14 snapshot below; it does not rewrite that historical checkpoint.


## September 19, 2026 — Libraries of Libraries successor

The current knowledge/reconstruction successor is **Libraries of Libraries**. This is not an identity claim that I, the repositories, or the projects are a federation. The older files and commits that used federation terminology remain preserved as historical provenance rather than being rewritten.

Current canonical successor surfaces:

- [Libraries of Libraries — RMAL Build](LIBRARIES_OF_LIBRARIES_RMAL_BUILD_2026-09-19.md)
- [Libraries of Libraries — Git Lineage](LIBRARIES_OF_LIBRARIES_GIT_LINEAGE_2026-09-19.md)
- [Compact RMAL form](libraries-of-libraries.rmal)

The active compression is:

`Library-of-Babel problem → identity → Library → Orbit → Libraries of Libraries → fighting point → consequential distinction → Decision Field → RMAL → Master Librarian → human surface → action → observation → learned delta → recovery seed → way back`

The **fighting point** is current successor terminology for the preserve-the-difference boundary: if collapsing two states changes a protected consequence for the current obligation, that distinction must survive. The phrase is not retroactively attributed to older Git history.

`CONNECTION != OWNERSHIP` · `RELATION != AUTHORITY_TRANSFER` · `RECONSTRUCTION != SOURCE`


## September 19, 2026 — Cooperative implementation protocol

Current cooperation/provenance authority is recorded in [COOPERATIVE_IMPLEMENTATION_PROTOCOL_2026-09-19.md](COOPERATIVE_IMPLEMENTATION_PROTOCOL_2026-09-19.md) with a [machine-readable provenance record](COOPERATIVE_IMPLEMENTATION_PROVENANCE_2026-09-19.json).

The governing attribution is:

```text
DESIGN_AUTHORITY = RYAN_MCMILLAN
IMPLEMENTATION_RELATION = HUMAN_AI_COIMPLEMENTATION
CROSS_WRITE_DEFAULT = DENY
```

The governing coordination path is:

```text
REFERENCE -> PROPOSAL -> HANDOFF -> TARGET_DECISION -> TARGET_LOCAL_SUCCESSOR
```

This makes the collaboration explicit without collapsing ownership or authority: Ryan McMillan designed the goals, principles, named frameworks, and cooperation model; implementation and refinement are carried out collaboratively with ChatGPT/OpenAI tooling under Ryan's direction, constraints, corrections, and acceptance gates.

The executable RMAL carrier is maintained additively in `redogit/Other-Projects-` at `docs/RMAL_COOPERATIVE_IMPLEMENTATION_PROTOCOL.rmal`. Compilation validates the carrier syntax and structure; it does not grant scientific truth authority.


## September 19, 2026 — current cooperation/language/evidence continuation

The current synthesis now includes:

- **USDAY-first cooperation** and **Pairity-before-parity** as design-state operating rules;
- the corrected **Interlingua Linguistics Agreement System** successor;
- a fail-closed **private-history method-learning boundary**;
- the compiled/audited RMAL cooperative carrier in `redogit/Other-Projects-`;
- bounded Conscience64 public-source dependency measurements under the continuing publication hold.

The additive RMAL cooperative carrier passed RMALC 2.1.1 `check`, `compile`, and `audit`, with claim ceiling `PARSER_COMPILE_AUDIT_VALIDATION_ONLY`.

```text
REFERENCE -> PROPOSAL -> HANDOFF -> TARGET_DECISION -> TARGET_LOCAL_SUCCESSOR
```

```text
DESIGN != IMPLEMENTATION
AGREEMENT != EVIDENCE
PRIVATE_HISTORY != PUBLIC_EVIDENCE
SOURCE_GRAPH_MEASURED != PUBLICATION_APPROVED
AUDIT_PASS != SEMANTIC_TRUTH
```


## September 20, 2026 — Bidirectional Handoff Pairity

The cross-project cooperation path is now explicitly **two-way** at the coordination layer:

```text
A -> REQUEST -> B -> TARGET DECISION -> RESPONSE -> A
B -> REQUEST -> A -> TARGET DECISION -> RESPONSE -> B
```

See [Bidirectional Handoff Pairity](BIDIRECTIONAL_HANDOFF_PROTOCOL_2026-09-20.md) and its [machine-readable contract](BIDIRECTIONAL_HANDOFF_PROTOCOL_2026-09-20.json).

Each target keeps local authority. A request is not a command, a response is not authority transfer, and a counterproposal creates a new handoff rather than rewriting the prior response.

Current implementations remain asymmetric, but Conscience64 now has one verified structured return runtime for `PRIVATE_METHOD_HANDOFF`: PR #176 links the admitted request packet UOID to a restricted target-local response and append-only response ledger. Generic response classes remain unimplemented. Other-Projects has implemented RMAL handoff/target-acceptance syntax but not the complete structured return packet.


## September 20, 2026 — isolated public testbed

Conscience64 publication authority has narrowed to a generated **public-testbed-only** projection under issue #166. The projection is built solely from `public-testbed/`, carries the exact source revision and deterministic projection identity, rejects private-origin carriers, and is verified against both the `gh-pages` tree and the network edge.

This does **not** publish the Conscience64 repository as a whole and does not grant commercial rights.

`PUBLIC_TESTBED != WHOLE_REPOSITORY` · `PUBLIC_EXPERIMENT != VERIFIED_TRUTH` · `PUBLIC_PROJECTION != COMMERCIAL_LICENSE`
Current verified live source: `redogit/conscience64@9a17f941808993049466e9b75ee8ec99253b5add`.
Current projection commit: `0888f45cb99bd16e225e20bd30005c9de8582551`; projection identity: `e54b69dff1964e218d1f99d7d28f5ace05649723ff677f25840ebe502f10e4a3`.

The public surface now retains six explicit path states (`active`, `tested`, `failed`, `blocked`, `deferred`, `return`) and six method labels (`USDAY`, `Interlingua`, `Pairity`, `Visible paths`, `Wonderment`, `One-degree experiment`). These are navigation/method carriers, not authority or scientific validation.

## Explore the history — 10 doors

The history is intentionally **distributed, independently authoritative, and reconstructible rather than centralized**. The [10-step History Playground](history-playground.html) gives people ten optional doors into the theories, formal results, experiments, tools, games, apps, education, accessibility, philosophy, ethics, coding, failures, and recovered history.

Each door follows:

`FIND → TRY → LEARN → TEACH → LEAVE A TRAIL`

Finishing all ten is not a mastery badge or a completeness claim. It means you explored ten slices and can explain what you found. Start with the [full check-in guide](HISTORY_PLAYGROUND_10_STEP_CHECKIN.md), the [Work Index](WORK_INDEX.md), or the [machine-readable quest manifest](history-playground.json).

## Research + production

The [Research + Production switchboard](research-production.html) separates the work into independently traceable lanes:

`RESEARCH · PRODUCTION · PLAY · TEACH · HISTORY`

The two main loops are deliberately different:

`QUESTION → CLAIM → TEST → EVIDENCE → REMAINDER`

`NEED → BUILD → VERIFY → RELEASE/USE → FEEDBACK → REPAIR`

A research result may inspire a product without becoming a product claim. A successful app, game, or public release does not scientifically validate the theory that inspired it. The current [Research + Production guide](RESEARCH_PRODUCTION.md) and [machine-readable coordination map](research-production-map.json) carry the adaptive-organization, technical-we, meta-coordination, self-modeling, and no-center ideas alongside the existing projects. Their predecessors `RESEARCH_PRODUCTION_FEDERATION.md` and `research-production.json` remain preserved as historical provenance.

The current conversation has also been restructured into an explicit [goal topology](GOAL_TOPOLOGY_2026-09-15.md) with a [machine-readable companion](goal-topology-2026-09-15.json). Each goal keeps its own owner, state, dependency, next action, and evidence boundary so independent lines can move without silently merging authority.

## Active project slice

The current [Active Projects surface](active-projects.html) is the narrower **current/runnable/deployed** projection. It routes status back to the owning repositories instead of making this profile the authority. The predecessor `active-federation.*` files remain preserved as historical provenance.

`ACTIVE != UNIVERSALLY_VALID` · `CONNECTED != MERGED` · `OPEN_PR != ACTIVE_MAIN`

See the [activation notes](ACTIVE_PROJECTS.md) and [machine-readable active registry](active-projects.json). The predecessor `ACTIVE_FEDERATION.md` and `active-federation.json` remain preserved for provenance. Conscience64 and Other-Projects keep their own local active registries.

## Current work — September 14, 2026

### Conscience64 spatial interface

Conscience64 is being unified around a **2.5D / 3D visual grammar**. The main Space Lens now has a capability-adaptive graphics path that prefers **WebGPU**, falls back through **WebGL2 / WebGL**, and retains the existing Canvas2D/evidence surface when GPU APIs are unavailable. The Compass brings the major public and operational surfaces into one spatial navigation layer.

The same depth hierarchy is being carried through Play, Research Analytics, Coordinate Space, and Research Records. Reduced-motion and forced-colors fallbacks remain part of the interface contract. Visual depth is navigation and presentation—not scientific evidence.

[Conscience64](https://github.com/redogit/conscience64) · [Research site](https://redogit.github.io/conscience64/)

### Fuzzball Hidden Game — Alpha 0.1

The new **Fuzzball Hidden Game** is now a verified merged alpha inside Conscience64. The alpha has a deterministic floating-world seed, a triangular explorer, 22 ambient Fuzzballs, and 16 humanoid creatures across four families: Mosswalker, Glasskin, Emberkin, and Duskseer. Humanoids have bounded deterministic wandering and proximity reactions.

The game remains intentionally **unlisted** from the public Play catalog and declares `noindex,nofollow`. Unlisted is a distribution choice, not a security boundary.

Most importantly:

`HISTORICAL_FUZZBALL_CARRIER != NEW_FUZZBALL_HIDDEN_GAME`

The older Fuzzball research carrier is still an unresolved historical recovery problem. Similarity, naming, or new implementation does not establish historical identity.

### Research Analytics

Research Analytics now has a live-ingestion architecture rather than only a demonstration stream: append-only event handling, SSE delivery, explicit event classes, an LLVM event bridge, and CI checks around the event contract.

The analytics model keeps these states distinct:

`OBSERVATION → TESTED → VERIFIED → CONTRADICTION → REVISED → PROMOTED / REOPENED`

Promotion is never automatic. An analytics event can record evidence; the dashboard itself does not validate the scientific claim represented by that event.

### Research method

The working method has become deliberately cyclical:

`working model → outward exploration → independent evidence/testing → return → reconcile → second-pass verification → revised working model`

I try to preserve at least these distinctions:

```text
USER_INPUT != ASSISTANT_SYNTHESIS
REQUESTED != IMPLEMENTED
IMPLEMENTED != VERIFIED
OBSERVATION != INTERPRETATION
REPETITION != VERIFICATION
RETRIEVED != INDEPENDENT_EVIDENCE
BYTE_IDENTITY != SEMANTIC_TRUTH
SOFTWARE_VERIFICATION != SCIENTIFIC_VALIDATION
```

Negative results, interpretation mistakes, changed boundaries, contradictions, and unresolved questions remain first-class records. I also use a two-pass update habit: make the change, then come back through it looking specifically for omissions, confounds, stale links, provenance errors, and overclaims.

## What I am exploring

Current work includes Cross-Carrier reconstruction, Coordinate Space / Float64 transport, Tiny Babel / TBCL, Orbit-style knowledge organization, SPrime finite searches, Hodge-conjecture research aids, P-versus-NP-related computational experiments, human–knowledge working-set models, accessibility-oriented tooling, cooperative systems, games, and research infrastructure.

The Hodge conjecture and P versus NP remain open. A successful program run, transport round trip, visual analogy, finite search, or deployed web application does not change those mathematical claim ceilings.

## REDOGIT

**Do it. Inspect it. Redo it better.**

REDOGIT is my public working rule:

1. start from the actual artifact, code, idea, or failure;
2. preserve the predecessor and provenance;
3. bound the change;
4. build the smallest useful successor;
5. verify what can actually be verified;
6. retain failures and unresolved state;
7. continue from the successor without rewriting history.

See [REDOGIT.md](REDOGIT.md) and the machine-readable [redogit.json](redogit.json).

## All eight repositories

The account-level count remains **eight repositories: seven public and one private placeholder**. New Conscience64 games, research records, analytics surfaces, and browser tools are subprojects inside an existing repository; they do not silently become new repositories.

### 1. [Conscience64](https://github.com/redogit/conscience64)

Research environment and browser interface containing Space Lens / Compass4D, Coordinate Space, Research Analytics, research records, history/restore surfaces, public Play applications, Explorer/MMO work, Computational Chorus, Musilanguage, and the unlisted Fuzzball Hidden Alpha.

The repository preserves explicit boundaries between source integrity, software behavior, interpretation, and independent evidence.

### 2. [Dream to Action](https://github.com/redogit/Dream-To-Action)

A local-first human-directed planning prototype built around a chosen goal, a real barrier, a next action, and an honest review. Human benefit and assistive-technology validation remain separate from software checks.

### 3. [Other Projects](https://github.com/redogit/Other-Projects-)

Multi-project home for ChatGPT/Conscience cooperation, the Human Expression Archive, S1024 Compression Lab, Context Discovery, SPrime Search, Hodge research aids, and other bounded experiments. Subprojects are not counted as additional repositories.

### 4. [MauiBrickBreak](https://github.com/redogit/MauiBrickBreak)

Preserved .NET/MAUI game lineage with reusable game-state, geometry, collision, and behavior-verification successors.

### 5. [FirstNeuralNetwork](https://github.com/redogit/FirstNeuralNetwork)

Preserved neural-network experiments and bounded deterministic successors. Passing finite truth-table tests are software results, not claims of general intelligence.

### 6. [Orbit Engine](https://github.com/redogit/orbit)

An upstream-derived .NET MAUI Graphics engine fork with retained attribution and local REDOGIT repair history. This is distinct from the Orbit Library / knowledge-organization research line.

### 7. [redogit](https://github.com/redogit/redogit)

This profile, the REDOGIT rule and schema, repository accounting, verification helpers, and dated forward-only profile updates.

### 8. Private repository

One repository remains private. It is counted without publishing its identity, URL, code, documents, or internal verification details.

## Current Conscience64 research records

The preserved browser/API registry remains historically bounded while newer records are added forward-only. Current human-readable records include Cross-Carrier Wave, Orbit Library, Tiny Babel / TBCL, Operator Moonshot, Model Experiments, Geometry / 4D / Codecs, Historical Recovery, Hodge Conjecture Research Spine, and Research Analytics.

[Research records](https://github.com/redogit/conscience64/tree/main/research/projects) · [Research Analytics](https://redogit.github.io/conscience64/) · [Coordinate Space](https://redogit.github.io/conscience64/) · [Play](https://redogit.github.io/conscience64/) · [History](https://redogit.github.io/conscience64/)

## Rights and commercial access

Current owner policy: **no third-party commercial access is authorized at this time** for original material controlled by the owner unless a separate written grant explicitly says otherwise.

Public visibility does not itself grant commercial rights. Consumer access to RMAOS MINGX, including the declared Mini ($0.99) and Full / Pro Advanced ($1.00) tiers, is separate from business licensing or commercial exploitation rights.

Earlier versions of this profile used broader “Free Use” wording. The current policy does not pretend to retroactively cancel rights already validly granted under an existing license or permission. MIT-, GPL-, upstream-, third-party-, and other already-applicable terms continue to control the material they cover.

See [COMMERCIAL_ACCESS_POLICY.md](COMMERCIAL_ACCESS_POLICY.md).

`PUBLIC_PROJECTION != COMMERCIAL_ACCESS` · `BUSINESS_ACCESS = DENY_UNLESS_EXPLICITLY_GRANTED`

---

Current navigation: [Libraries of Libraries](LIBRARIES_OF_LIBRARIES_RMAL_BUILD_2026-09-19.md) · [RMAL](libraries-of-libraries.rmal) · [Git lineage](LIBRARIES_OF_LIBRARIES_GIT_LINEAGE_2026-09-19.md) · [Goal Topology](GOAL_TOPOLOGY_2026-09-15.md) · [Active project slice](active-projects.html) · [Research + Production](research-production.html) · [Work Index](WORK_INDEX.md) · [10-Step History Playground](history-playground.html) · [Detailed check-in guide](HISTORY_PLAYGROUND_10_STEP_CHECKIN.md) · [Body-of-work recovery snapshot](BODY_OF_WORK.md) · [Standalone homepage](index.html)
