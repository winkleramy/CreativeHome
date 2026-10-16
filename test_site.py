"""Check generated local links, assets, and navigation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
ROOT = Path(__file__).resolve().parent / 'dist'
class Scan(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        for key in ('href','src','poster'):
            if key in a: self.links.append(a[key])
pages={}
for p in ROOT.rglob('*.html'):
    scan=Scan(); scan.feed(p.read_text()); pages[p.resolve()]=scan
assert (ROOT/'index.html').resolve() in pages
for path,scan in pages.items():
    for link in scan.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        assert not u.path.startswith('/'), f'Root-relative link breaks repository hosting: {link}'
        target=(path.parent/unquote(u.path)).resolve() if u.path else path
        assert target.is_relative_to(ROOT.resolve()), f'Link escapes site: {link}'
        assert target.exists(), f'{path.name}: missing {link}'
        if u.fragment and target in pages:
            assert unquote(u.fragment) in pages[target].ids, f'Missing anchor: {link}'
posts=sorted((ROOT/'posts').glob('*.html'),reverse=True)
for i,p in enumerate(posts):
    scan=pages[p.resolve()]
    assert '../index.html#journal' in scan.links
    if i: assert posts[i-1].name in scan.links
    if i+1<len(posts): assert posts[i+1].name in scan.links
print(f'Passed: {len(pages)} pages, local assets, anchors, repository-safe URLs, and post navigation.')
