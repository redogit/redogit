# Dream to Action — public Pages route

Public application: https://redogit.github.io/redogit/dream-to-action/

Canonical source: https://github.com/redogit/Dream-To-Action

This directory is an explicitly selected, byte-identical publication of the tested standalone Operations 0.2 application. It is not a migration of the project. Its immutable source commit, file digest, and publication scope are in `SOURCE.json`.

The existing `redogit/redogit` Pages host is used because the available connector does not expose the administration action needed to activate a new Pages site for `Dream-To-Action`. The separate `https://redogit.github.io/Dream-To-Action/` route has not been activated by this publication. Source development and history stay in their original repository. Public visibility does not grant new reuse rights or override `COMMERCIAL_ACCESS_POLICY.md` in the source project.

Only the application and these public provenance notes are added here. Browser journals, optional browser backups, private files, and source repository internals are not part of this projection. Personal mode starts empty; the demo is fictional. Application records stay in the browser unless the visitor chooses an export; optional local backup and exports are unencrypted. GitHub still hosts and serves the website itself.

The About Me announcement is at `../about.html#announcements`; the brief explanation of purpose is at `../about.html#dream-to-action`. The existing Recent Work / Current Surfaces section and the GitHub profile notice also link to the application. Earlier biography and project content were retained unchanged outside the additive blocks.

Deployment is handled by the existing Pages workflow. Before upload it verifies the application SHA-256 and announcement content. After deployment it requests the application and announcement pages anonymously over HTTPS, checks status/content, and compares the delivered application bytes to the tested release. A manifest alone is not evidence of a successful public deployment; inspect the workflow's completed post-deployment check.

To verify locally: `python tools/publish_dream_pages.py --check` from the repository root. To check published content: `python tools/publish_dream_pages.py --live`. For a future release, update the explicit source commit/digest and projection together; do not silently follow a moving external branch.
