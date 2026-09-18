# Publishing the homepage

> **Public projection status — 2026-09-18:** Conscience64 GitHub Pages is intentionally held at a minimal privacy surface pending explicit owner approval of an exact reviewed revision. Project/research state is independent of public availability. Public URLs are projections, not canonical authority.


`README.md` is the About me content shown on the GitHub profile at https://github.com/redogit.

`index.html` is a standalone version of the homepage. It works locally and needs no build step, JavaScript, third-party fonts, or external assets.

To publish the standalone page with GitHub Pages:

1. Open https://github.com/redogit/redogit/settings/pages.
2. Under **Build and deployment**, select **Deploy from a branch**.
3. Select the **main** branch and **/(root)**, then save.
4. Wait for GitHub Pages to finish publishing. GitHub will display the live address in these settings. With the default domain, it is https://redogit.github.io/redogit/.

The repository's GitHub Pages setting must be enabled separately; adding the HTML file alone does not enable hosting.

Both versions include the requested **Free Use!** permission for this homepage's original content and code. That permission does not change the licenses of linked projects or third-party material.

## Private-by-default publication rule

Public publication is opt-in rather than automatic:

`PRIVATE_BY_DEFAULT → REVIEW → EXPLICIT_OWNER_APPROVAL(EXACT_SHA) → PUBLIC_PROJECTION → DEPENDENCY_REVIEW`

A GitHub Pages URL is a revocable projection, not project identity or evidence authority. Repository visibility should also be private unless the owner separately determines the content is safe for public access. The current connector cannot administer repository visibility, so visibility changes require an account-level GitHub administration action outside this workflow.
