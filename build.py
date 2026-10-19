"""Build complete static pages. Run: python3 build.py"""
from pathlib import Path
from string import Template
from html import escape
from datetime import date
import json, re, shutil
import markdown

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'

def build():
    config = json.loads((ROOT / 'site.json').read_text())
    template = Template((ROOT / 'templates/page.html').read_text())
    posts = []
    for path in sorted((ROOT / 'posts').iterdir()):
        if path.suffix.lower() not in ('.md', '.txt'): continue
        match = re.fullmatch(r'(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)', path.stem)
        if not match: raise ValueError(f'{path.name}: use YYYY-MM-DD-lowercase-slug.md or .txt')
        day = date.fromisoformat(match[1])
        raw = path.read_text(encoding='utf-8')
        meta = {}
        if raw.startswith('---\n'):
            header, sep, raw = raw[4:].partition('\n---\n')
            if not sep: raise ValueError(f'{path.name}: missing closing ---')
            for line in header.splitlines():
                key, colon, value = line.partition(':')
                if not colon: raise ValueError(f'{path.name}: metadata must be key: value')
                meta[key.strip()] = value.strip()
        if meta.get('draft', '').lower() == 'true': continue
        title = meta.get('title', match[2].replace('-', ' ').title())
        body = markdown.markdown(raw, extensions=['extra', 'sane_lists']) if path.suffix.lower() == '.md' else '<div class="plain-text">' + escape(raw) + '</div>'
        posts.append(dict(slug=path.stem, date=day, title=title, body=body, category=meta.get('category','Journal'), excerpt=meta.get('excerpt','Open this entry and spend a little time here.')))
    posts.sort(key=lambda p:(p['date'],p['slug']), reverse=True)
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT/'posts').mkdir(parents=True)
    shutil.copytree(ROOT/'assets', OUT/'assets')
    (OUT/'.nojekyll').touch()
    def page(title, description, content, root):
        return template.substitute(title=escape(title), description=escape(description, quote=True), content=content, root=root, site_title=escape(config['title']), author=escape(config['author']))
    def stamp(p): return f'<span>{escape(p["category"])}</span><time datetime="{p["date"].isoformat()}">{p["date"].strftime("%b %d, %Y")}</time>'
    cards = ''.join(f'<article class="card"><div class="meta">{stamp(p)}</div><h3><a href="posts/{p["slug"]}.html">{escape(p["title"])}</a></h3><p>{escape(p["excerpt"])}</p><a class="read" href="posts/{p["slug"]}.html" aria-label="Read {escape(p["title"],quote=True)}">Read entry <span aria-hidden="true">↗</span></a></article>' for p in posts)
    content = f'<section class="hero"><div><p class="eyebrow">AN OPEN NOTEBOOK</p><h1>{escape(config["intro"])}</h1><p class="lede">{escape(config["description"])}</p><a class="button" href="#journal">Explore the journal <span aria-hidden="true">↓</span></a></div><figure><img src="assets/landscape.svg" alt="Illustrated sun setting above layered green hills"><figcaption>Everyday moment that blur into purpose</figcaption></figure></section><section id="journal"><div class="section-head"><h2>The journal</h2><p>Poems, stories & collected moments</p></div><div class="grid">{cards or "<p>The notebook is waiting for its first entry.</p>"}</div></section><section id="about" class="about"><p class="eyebrow">BEHIND THE NOTEBOOK</p><h2>Hello, I’m {escape(config["author"])}.</h2><p>{escape(config["about"])}</p></section>'
    (OUT/'index.html').write_text(page(config['title'],config['description'],content,'.'))
    for i,p in enumerate(posts):
        nav = '<nav class="post-nav" aria-label="Other entries">'
        for label, index in [('← Newer entry', i-1), ('Older entry →', i+1)]:
            if 0 <= index < len(posts):
                other=posts[index]
                nav += f'<a href="{other["slug"]}.html"><small>{label}</small>{escape(other["title"])}</a>'
        nav += '</nav>'
        content=f'<article class="post"><a class="back" href="../index.html#journal">← Back to the journal</a><header><div class="meta">{stamp(p)}</div><h1>{escape(p["title"])}</h1><p class="lede">{escape(p["excerpt"])}</p></header><div class="prose">{p["body"]}</div>{nav}</article>'
        (OUT/'posts'/f'{p["slug"]}.html').write_text(page(p['title']+' · '+config['title'],p['excerpt'],content,'..'))
    print(f'Built {len(posts)} posts in {OUT}')

if __name__ == '__main__': build()
