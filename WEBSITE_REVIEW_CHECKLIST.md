# Website review checklist

Snapshot: 2026-09-13

Purpose: inventory every HTML file currently present across the eight REDOGIT repositories, distinguish public pages from templates/test fixtures/legacy copies, link the raw source, and keep unfinished review work explicit.

## Counting rule

- 23 HTML files are present across the eight repositories.
- 22 unique HTML blobs are present because `Dream-To-Action/index.html` and `Dream-To-Action/prototype/dream-to-action.html` are intentionally byte-identical.
- `Other-Projects-`, `orbit`, `MauiBrickBreak`, `FirstNeuralNetwork`, and the private `DnD` repository currently contain no `.html` file in their repository trees.
- An HTML file is not automatically a public website. Templates, test fixtures, and preserved legacy prototypes stay classified separately.

## Checklist

| State | Repository | Path | Role | Raw HTML | Review / action |
|---|---|---|---|---|---|
| [ ] review | redogit/redogit | `index.html` | public profile/homepage | https://raw.githubusercontent.com/redogit/redogit/main/index.html | Current public surface. Review link integrity, content freshness, keyboard/focus behavior, narrow viewport, and claims against repository evidence. |
| [ ] review | redogit/conscience64 | `index.html` | public research homepage | https://raw.githubusercontent.com/redogit/conscience64/main/index.html | Current public surface. Existing API/data verifier is not a visual-browser audit. |
| [ ] review | redogit/conscience64 | `about/index.html` | public About page | https://raw.githubusercontent.com/redogit/conscience64/main/about/index.html | Existing page-check record covers update navigation; broader visual/accessibility review remains separate. |
| [ ] review | redogit/conscience64 | `coordinate-space/index.html` | public Coordinate Space | https://raw.githubusercontent.com/redogit/conscience64/main/coordinate-space/index.html | Functional/browser checks exist; full visual/WCAG audit remains open. |
| [x] repaired-in-PR | redogit/conscience64 | `history/index.html` | public History/Restore | https://raw.githubusercontent.com/redogit/conscience64/main/history/index.html | Missing explicit REDOGIT update navigation found and repaired on `site-review-small-batches-2026-09-13`; page-check manifest updated. |
| [ ] review | redogit/conscience64 | `play/index.html` | public Play directory | https://raw.githubusercontent.com/redogit/conscience64/main/play/index.html | Six public tools listed. Review card/link consistency and localized labels. |
| [ ] review | redogit/conscience64 | `play/compare/index.html` | public Source Compare | https://raw.githubusercontent.com/redogit/conscience64/main/play/compare/index.html | Review keyboard workflow, diff announcements, long-text bounds, export behavior. |
| [ ] review | redogit/conscience64 | `play/computational-chorus/index.html` | public Computational Chorus | https://raw.githubusercontent.com/redogit/conscience64/main/play/computational-chorus/index.html | Review animation/audio-independent usability, reduced-motion behavior, and text alternatives. |
| [ ] review | redogit/conscience64 | `play/garden/index.html` | public Pattern Garden | https://raw.githubusercontent.com/redogit/conscience64/main/play/garden/index.html | Review non-drag interaction path, SVG/canvas alternatives, mobile sizing. |
| [ ] review | redogit/conscience64 | `play/musilanguage/index.html` | public Musilanguage entry | https://raw.githubusercontent.com/redogit/conscience64/main/play/musilanguage/index.html | Review navigation and whether every audio/music function has a non-audio path. |
| [ ] review | redogit/conscience64 | `play/musilanguage/radio.html` | public Musilanguage Radio | https://raw.githubusercontent.com/redogit/conscience64/main/play/musilanguage/radio.html | Review media state announcements, autoplay assumptions, keyboard controls. |
| [ ] review | redogit/conscience64 | `play/musilanguage/single.html` | public self-contained Musilanguage build | https://raw.githubusercontent.com/redogit/conscience64/main/play/musilanguage/single.html | Large self-contained copy. Check drift against modular source and duplicate logic. |
| [ ] review | redogit/conscience64 | `play/musilanguage/word-forge.html` | public Word Forge | https://raw.githubusercontent.com/redogit/conscience64/main/play/musilanguage/word-forge.html | Review generated-word labeling, input bounds, keyboard path, and export/clear behavior. |
| [ ] review | redogit/conscience64 | `play/orbit/index.html` | public Orbit Shelf | https://raw.githubusercontent.com/redogit/conscience64/main/play/orbit/index.html | Review local persistence, source-link safety, import/export limits, and mobile layout. |
| [ ] review | redogit/conscience64 | `play/steps/index.html` | public Small Steps | https://raw.githubusercontent.com/redogit/conscience64/main/play/steps/index.html | Review form validation, status announcements, history/import boundaries. |
| [ ] review | redogit/conscience64 | `play/weave/index.html` | public Word Weave | https://raw.githubusercontent.com/redogit/conscience64/main/play/weave/index.html | Review source/original preservation, keyboard reordering alternative, and export semantics. |
| [ ] review | redogit/conscience64 | `research/projects/index.html` | public research-project index | https://raw.githubusercontent.com/redogit/conscience64/main/research/projects/index.html | Review project-link completeness and whether unresolved states remain visible. |
| [ ] review | redogit/conscience64 | `research/cross-carrier/2026-09-13/internal-update/global_search/index.html` | generated internal/public search workbench | https://raw.githubusercontent.com/redogit/conscience64/main/research/cross-carrier/2026-09-13/internal-update/global_search/index.html | Generated interface. Existing notes already retain network/proxy limits. Verify external-link policy and local-storage disclosure. |
| [x] classify | redogit/conscience64 | `research/cross-carrier/2026-09-13/internal-update/global_search/interface.html` | build template, not a deployable site | https://raw.githubusercontent.com/redogit/conscience64/main/research/cross-carrier/2026-09-13/internal-update/global_search/interface.html | Contains the `__CATALOG__` placeholder by design. Do not treat direct opening as a finished website; `build_interface.py` materializes the generated `index.html`. |
| [x] classify | redogit/conscience64 | `research/cross-carrier/2026-09-13/internal-update/global_search/shadow.html` | isolated interaction test fixture | https://raw.githubusercontent.com/redogit/conscience64/main/research/cross-carrier/2026-09-13/internal-update/global_search/shadow.html | Fixed absolute coordinates and minimal structure are intentional for XY/pointer receipts. Do not publish as a general user page. |
| [x] classify | redogit/conscience64 | `research/cross-carrier/2026-09-13/internal-update/global_search/legacy/black_hole_ai_conscience_ecs/index.html` | preserved legacy game prototype | https://raw.githubusercontent.com/redogit/conscience64/main/research/cross-carrier/2026-09-13/internal-update/global_search/legacy/black_hole_ai_conscience_ecs/index.html | Preserved predecessor. Improvements should be successors, not silent rewrites. |
| [ ] review | redogit/Dream-To-Action | `index.html` | public/local-first planning prototype | https://raw.githubusercontent.com/redogit/Dream-To-Action/main/index.html | 43 included browser checks pass. Real screen-reader session, full WCAG audit, real-person/service-provider pilot, and direct `file://` launch remain explicitly unverified. |
| [x] duplicate | redogit/Dream-To-Action | `prototype/dream-to-action.html` | preserved release copy | https://raw.githubusercontent.com/redogit/Dream-To-Action/main/prototype/dream-to-action.html | Byte-identical to root `index.html`; preserve intentionally unless the release model changes. |

## Confirmed defects / repairs so far

- `conscience64/BUILD_AUDIT.json` had stale Browser API and project-registry metadata. The review branch updates API `1.2.0 -> 1.3.0`, registry `1.0.0 -> 1.1.0`, learned invariants `13 -> 20`, adds `lessonCount: 14`, and includes `projects.lessons` in the API inventory.
- `conscience64/history/index.html` lacked the explicit REDOGIT update-navigation marker used by the other reviewed public pages. The review branch adds it and updates `about/page-checks.json` from 16 to 17 checked pages.
- `global_search/interface.html` is not a broken website; it is a source template containing `__CATALOG__` until materialized by the build step.
- `global_search/shadow.html` is not a responsive public page; it is an intentionally fixed-coordinate test fixture.

## Explicitly unfinished, not to be falsely closed

- Conscience64 `BUILD_AUDIT.json` still correctly says `visualBrowserRenderingChecked: false`; API/data verification does not prove visual rendering or WCAG conformance.
- The original structured solver/operator-lab source and the original Fuzzball carrier remain recorded recovery gaps.
- Dream to Action still needs a real assistive-technology session, a full WCAG conformance audit, and real-world participant/service-provider validation before those claims can be made.
- A repository-wide live-link and deployed-GitHub-Pages pass is still needed after the review branches are merged.

## Small-batch order

1. Correct stale audit metadata and missing History update navigation. **Done on review branch.**
2. Review public profile + top-level Conscience64 pages.
3. Review Play tools in groups of three.
4. Review research/search HTML and keep templates/test fixtures/legacy files correctly classified.
5. Review Dream to Action without overwriting its explicitly documented validation limits.
6. Run/record live deployment and accessibility checks after merge; do not convert unavailable evidence into a PASS.
