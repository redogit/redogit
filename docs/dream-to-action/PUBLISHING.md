# Dream to Action — verified public Pages route

**Live application:** https://redogit.github.io/conscience64/dream-to-action/

**About Me announcement:** https://redogit.github.io/conscience64/about.html#announcements

**Why it exists:** https://redogit.github.io/conscience64/about.html#dream-to-action

**Recent Work:** https://redogit.github.io/conscience64/recent-work.html#dream-to-action

The canonical application and its development history remain in `redogit/Dream-To-Action`. The canonical public profile pages remain in this repository under `docs/`. Conscience64's existing Pages service publishes only exact pinned copies of the three explicitly selected public files, plus a provenance manifest. This is a hosting projection, not a project migration or a new license.

## Deployment evidence

Native Pages deployment succeeded in run https://github.com/redogit/conscience64/actions/runs/36459090437 . The separate live verifier https://github.com/redogit/conscience64/actions/runs/36459096995 requested each route anonymously over HTTPS and verified the delivered app and profile source bytes at 2026-09-28T17:35:22Z. The app SHA-256 is `231fdadb14093df1028abe015f3c4d583b1031da5ae03048abff5244c3eac807`, matching the tested Operations 0.2 release.

## Corrected hosting assumption

The first profile-host attempt, run 36457772017, failed at Configure Pages: site Not Found. The earlier `/redogit/dream-to-action/` URL was not successfully deployed and is superseded by the live route above. Neither a repository's public visibility nor an existing workflow file proves Pages is enabled. The dedicated `/Dream-To-Action/` route was also not activated. This history remains in Git; it is not relabeled as a success.

## Preserved boundaries

No participant journals, browser backups, private-origin About page, source-repository internals, or unrelated private content are published. Demo data is fictional and separate. Browser records and optional exports/backups remain unencrypted. Existing testbed/Musilanguage publication scope and private-route counterprobes remain intact, with the new routes authorized separately.

The profile workflow now verifies source integrity and the selected public host; it does not pretend to deploy a disabled profile Pages service. Actual publishing is the narrowly scoped Conscience64 Pages pipeline. To update the public copy, explicitly advance its pinned source revisions and hashes after review; changing an unrelated source file is not automatic publication permission.

Current checks: `python tools/finalize_dream_publication.py --check` and `python tools/finalize_dream_publication.py --live`. `tools/publish_dream_pages.py` remains the historical first-attempt preparer; the current wrapper supplies the corrected live host and notice.

The broad Conscience64 REDOGIT check retains an unrelated Cooperative Field v3/v2 mismatch already present before this publication. The publication, exact-byte, private-route, and live HTTP checks passed; no all-repository-green or real-world-benefit claim is made.
