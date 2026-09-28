"""Finalize verified live links without rewriting biography or historical evidence."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import publish_dream_pages as original

ROOT = Path(__file__).resolve().parents[1]
OLD = 'https://redogit.github.io/redogit/'
LIVE = 'https://redogit.github.io/conscience64/'
RUN = 'https://github.com/redogit/conscience64/actions/runs/36459096995'
NOTICE = original.README_NOTICE.replace(OLD, LIVE)


def prepare():
    path = ROOT / 'README.md'
    raw = path.read_bytes()
    original.require(original.blob_sha(raw) == '64e88a932d13b00ea0c60b7d83283162d56b6a96', 'Read the changed profile before applying this correction')
    text = raw.decode('utf-8')
    head, marker, biography = text.partition('## About me\n')
    original.require(marker and original.README_NOTICE in head, 'Expected profile announcement missing')
    for suffix in ['dream-to-action/', 'about.html', 'recent-work.html']:
        head = head.replace(OLD + suffix, LIVE + suffix)
    corrected = head + marker + biography
    original.require(corrected.partition('## About me\n')[2] == biography, 'Biography changed')
    path.write_bytes(corrected.encode('utf-8'))
    source = ROOT / 'docs/dream-to-action/SOURCE.json'
    data = json.loads(source.read_text(encoding='utf-8'))
    data.update(public_url=LIVE + 'dream-to-action/', publication_host='Enabled redogit/conscience64 GitHub Pages host', profile_public_url=LIVE + 'about.html#announcements', prior_attempt={'url': OLD + 'dream-to-action/', 'status': 'NOT DEPLOYED: Pages site Not Found', 'run_id': 36457772017}, live_verification={'url': RUN, 'http': 200, 'anonymous_https': True, 'checked_utc': '2026-09-28T17:35:22Z'}, profile_pages_enabled=False)
    source.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    publishing = '''# Dream to Action — verified public Pages route

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
'''
    (ROOT / 'docs/dream-to-action/PUBLISHING.md').write_text(publishing, encoding='utf-8')
    check()


def check():
    original.BASE_URL = LIVE
    original.README_NOTICE = NOTICE
    original.check()
    data = json.loads((ROOT / 'docs/dream-to-action/SOURCE.json').read_text(encoding='utf-8'))
    original.require(data['public_url'] == LIVE + 'dream-to-action/', 'Incorrect live source link')
    original.require(data['live_verification']['url'] == RUN, 'Missing deployment evidence')
    print('PASS: corrected live profile/application links; previous biography is unchanged.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--prepare', action='store_true')
    g.add_argument('--check', action='store_true')
    g.add_argument('--live', action='store_true')
    a = p.parse_args()
    try:
        if a.prepare: prepare()
        elif a.check: check()
        else:
            original.BASE_URL = LIVE
            original.live()
    except (OSError, ValueError) as e:
        raise SystemExit('Publication finalization failed: ' + str(e))
