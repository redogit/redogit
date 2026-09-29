"""Publish/check the explicitly selected Dream to Action Pages projection.

Canonical application authority stays in redogit/Dream-To-Action. The existing
profile Pages host carries one pinned, byte-identical static application only.
No source tree, private history, browser backup, or participant journal is copied.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://redogit.github.io/redogit/'
SOURCE_COMMIT = '667e989dcad401829bb097726b3a14cc0aa90f2c'
SOURCE_URL = f'https://raw.githubusercontent.com/redogit/Dream-To-Action/{SOURCE_COMMIT}/index.html'
APP_HASH = '231fdadb14093df1028abe015f3c4d583b1031da5ae03048abff5244c3eac807'
APP_BYTES = 78619
EXPECTED = {
    'docs/about.html': 'cc8a1698433670058522d774060e50ae9140cd60',
    'docs/recent-work.html': 'd5e344e5823cdf263da89d7bb13edc6f8b34a4a4',
    'README.md': '920d96e3ef6c97452af579e87d0f2815162f91c6',
}
ANNOUNCEMENT = '''
<section id="announcements" aria-labelledby="announcements-title">
<h2 id="announcements-title">Announcements</h2>
<article class="card" id="dream-to-action-launch">
<p class="muted"><time datetime="2026-09-28">September 28, 2026</time> · PUBLIC BROWSER APP</p>
<h3>Dream to Action — make the next step possible</h3>
<p>Dream to Action now has a public browser home. Choose a goal, make the barrier visible, track the support and next actions, and keep an honest record of what changes. The dashboard, action board, evidence history, and resource library are there to make the work usable—not to rank people.</p>
<p><a href="dream-to-action/">Open Dream to Action →</a> · <a href="https://github.com/redogit/Dream-To-Action">Source and project history</a> · <a href="recent-work.html#dream-to-action">Recent-work announcement</a></p>
<p class="muted">No account required. Personal records stay in the browser unless you choose to export them; optional browser backup and exports are unencrypted. The demonstration workspace is fictional and separate from personal records.</p>
</article>
</section>
<section id="dream-to-action" aria-labelledby="dream-purpose-title">
<h2 id="dream-purpose-title">Dream to Action — why it exists</h2>
<p>I wanted to turn the idea of a fair chance to build a life you value into something practical. Start with what the person actually wants, name the real barrier, and find one usable next step. Keep what the person can do separate from what somebody else or an institution needs to provide or change.</p>
<p>This project exists because hardship is not a measure of a person's worth, and a plan is not an opportunity until the needed conditions are available. It helps preserve the goal, the responsibilities, the support that is still unconfirmed, and what actually happened. A completed task is not automatically an improvement; the point is somebody gaining a choice that was previously blocked.</p>
<p><a href="dream-to-action/">Try the workbench</a> · <a href="https://github.com/redogit/Dream-To-Action/blob/main/docs/OPERATIONS.md">Operating guide</a> · <a href="https://github.com/redogit/Dream-To-Action/blob/main/COMMERCIAL_ACCESS_POLICY.md">Project reuse policy</a></p>
<p class="muted">This is a planning and review tool, not a service provider, an eligibility decision, or a guarantee of housing, employment, funding, care, or another person's agreement.</p>
</section>
'''
RECENT_CARD = '''<div class="card" id="dream-to-action"><div class="status">PUBLIC BROWSER APP · SEPTEMBER 28, 2026</div><h3><a href="dream-to-action/">Dream to Action</a></h3><p>A chosen goal, a real barrier, and a usable next step. The public workbench adds a visual dashboard, dependency-aware action board, evidence history, and dated resource references. Individual effort stays separate from support or institutional change.</p><p>Personal records are local to the browser; the fictional demonstration is separate. Task completion is not proof of benefit, and source visibility does not change the project's reuse policy.</p><p><a href="dream-to-action/">Open app →</a> · <a href="about.html#dream-to-action">Why I built it</a> · <a href="https://github.com/redogit/Dream-To-Action">Canonical source</a></p></div>
'''
README_NOTICE = '> **New public app — September 28, 2026:** [Dream to Action](https://redogit.github.io/redogit/dream-to-action/) turns a chosen goal and a real barrier into a practical next step, with a dashboard, action board, and evidence history. No account required; personal and fictional demonstration records stay separate. [Why it exists](https://redogit.github.io/redogit/about.html#dream-to-action) · [Source](https://github.com/redogit/Dream-To-Action).\n\n'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={'User-Agent': 'Dream-To-Action-Publication-Check', 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(request, timeout=25) as response:
        require(response.status == 200, f'HTTP {response.status}: {url}')
        require(response.url.startswith('https://'), 'Unexpected insecure redirect')
        data = response.read(2_097_153)
        require(len(data) <= 2_097_152, 'Unexpected response size')
        return data


def transform(path: str, data: bytes) -> bytes:
    require(blob_sha(data) == EXPECTED[path], 'Source changed; re-read before editing ' + path)
    text = data.decode('utf-8')
    if path == 'docs/about.html':
        nav = '<a href="#announcements">Announcements</a><a href="#dream-to-action">Dream to Action</a>'
        require(text.count('<nav>') == 1 and text.count('</header>') == 1, 'Unexpected About Me structure')
        result = text.replace('<nav>', '<nav>' + nav, 1).replace('</header>', '</header>\n' + ANNOUNCEMENT, 1)
        recovered = result.replace('<nav>' + nav, '<nav>', 1).replace('</header>\n' + ANNOUNCEMENT, '</header>', 1)
    elif path == 'docs/recent-work.html':
        marker = '<h2>1 // Current surfaces</h2>\n<div class="grid">\n'
        require(text.count(marker) == 1, 'Recent-work insertion point changed')
        result = text.replace(marker, marker + RECENT_CARD, 1)
        recovered = result.replace(marker + RECENT_CARD, marker, 1)
    elif path == 'README.md':
        marker = '# redogit\n\n'
        require(text.startswith(marker), 'Profile introduction changed')
        result = marker + README_NOTICE + text[len(marker):]
        recovered = result.replace(marker + README_NOTICE, marker, 1)
    else:
        raise ValueError('Unapproved target path')
    require(recovered.encode('utf-8') == data, 'Change would alter unrelated content: ' + path)
    return result.encode('utf-8')


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids = []
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.ids.append(values['id'])
        if tag == 'a' and 'href' in values:
            self.hrefs.append(values['href'])


def check() -> None:
    app = ROOT / 'docs/dream-to-action/index.html'
    require(app.is_file() and not app.is_symlink(), 'Missing regular application file')
    raw = app.read_bytes()
    require(len(raw) == APP_BYTES and hashlib.sha256(raw).hexdigest() == APP_HASH, 'Application differs from tested canonical source')
    metadata = json.loads((ROOT / 'docs/dream-to-action/SOURCE.json').read_text(encoding='utf-8'))
    require(metadata['canonical_commit'] == SOURCE_COMMIT and metadata['sha256'] == APP_HASH, 'Publication provenance differs')
    about = (ROOT / 'docs/about.html').read_text(encoding='utf-8')
    recent = (ROOT / 'docs/recent-work.html').read_text(encoding='utf-8')
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    require(ANNOUNCEMENT in about, 'Missing About Me announcement or purpose section')
    require(RECENT_CARD in recent, 'Missing existing Recent Work announcement')
    require(README_NOTICE in readme, 'Missing profile announcement')
    for name, source in [('About Me', about), ('Recent Work', recent)]:
        parsed = Links(); parsed.feed(source)
        require(len(parsed.ids) == len(set(parsed.ids)), 'Duplicate page IDs in ' + name)
        require('dream-to-action/' in parsed.hrefs, 'Missing relative live-app link')
    require('#announcements' in about and '#dream-to-action' in about, 'Missing About Me navigation')
    print(json.dumps({'result': 'PASS', 'canonical_commit': SOURCE_COMMIT, 'application_sha256': APP_HASH, 'application_bytes': len(raw), 'public_path': BASE_URL + 'dream-to-action/', 'announcement_surfaces': ['About Me', 'Recent Work', 'GitHub profile'], 'privacy_scope': 'Static public application and already-public biography only; no participant records'}, indent=2))


def prepare() -> None:
    out = ROOT / 'docs/dream-to-action'
    require(not out.exists(), 'Publication folder already exists; use --check instead')
    changes = {path: transform(path, (ROOT / path).read_bytes()) for path in EXPECTED}
    raw = download(SOURCE_URL)
    require(len(raw) == APP_BYTES and hashlib.sha256(raw).hexdigest() == APP_HASH, 'Pinned download hash does not match tested release')
    metadata = {
        'schema': 'dream-to-action/public-projection/v1',
        'canonical_repository': 'redogit/Dream-To-Action',
        'canonical_commit': SOURCE_COMMIT,
        'source_file': 'index.html',
        'source_url': SOURCE_URL,
        'sha256': APP_HASH,
        'bytes': APP_BYTES,
        'public_url': BASE_URL + 'dream-to-action/',
        'publication_host': 'Existing redogit/redogit GitHub Pages site',
        'recorded_date': '2026-09-28',
        'boundary': 'Exact public application projection, not project migration. Original source/history/reuse policy remain in Dream-To-Action. No journals or private data are published.',
        'dedicated_project_pages': 'Not activated: the available connector lacks new-site administration. This route uses the already-enabled public Pages host.',
        'verification': 'Canonical byte identity is checked before upload; public HTTP and byte-identity checks run after deployment. This record alone is not a live-deployment claim.'
    }
    out.mkdir(parents=True)
    (out / 'index.html').write_bytes(raw)
    (out / 'SOURCE.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    for path, data in changes.items():
        (ROOT / path).write_bytes(data)
    check()


def live() -> None:
    # Public requests deliberately have no credentials and cannot read journal data.
    last = None
    for attempt in range(12):
        try:
            app = download(BASE_URL + 'dream-to-action/?publication=' + SOURCE_COMMIT)
            require(hashlib.sha256(app).hexdigest() == APP_HASH, 'Live application has not reached the pinned release')
            for page, marker in [('about.html', ANNOUNCEMENT), ('recent-work.html', RECENT_CARD)]:
                data = download(BASE_URL + page + '?publication=' + SOURCE_COMMIT).decode('utf-8')
                require(marker in data, 'Live announcement not yet present: ' + page)
            print(json.dumps({'result': 'PASS', 'public_application': BASE_URL + 'dream-to-action/', 'public_about_me': BASE_URL + 'about.html#announcements', 'public_recent_work': BASE_URL + 'recent-work.html#dream-to-action', 'http': 200, 'anonymous_requests': True, 'application_sha256': APP_HASH, 'checked_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}, indent=2))
            return
        except (OSError, ValueError) as exc:
            last = exc
            if attempt < 11:
                time.sleep(5)
    raise ValueError('Public deployment check did not pass: ' + str(last))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prepare', action='store_true')
    group.add_argument('--check', action='store_true')
    group.add_argument('--live', action='store_true')
    args = parser.parse_args()
    try:
        if args.prepare: prepare()
        elif args.live: live()
        else: check()
    except (OSError, ValueError) as exc:
        raise SystemExit('Publication check failed: ' + str(exc))
