#!/usr/bin/env python3
"""Mirror Substack posts into this Docusaurus blog.

The Substack RSS feed carries FULL post content (not an excerpt), so mirroring
needs no pasted URLs and no scraping.

    scripts/mirror_substack.py list
        Fetch the feed and report which posts are not yet mirrored here.

    scripts/mirror_substack.py fetch <url-fragment> <slug>
        Convert one post to markdown and download its images into
        .substack-staging/. Leaves image alt text empty on purpose.

    scripts/mirror_substack.py assemble <config.json>
        Turn staged bodies into blog/<date>-<slug>.mdx with frontmatter and
        real alt text. See scripts/MIRRORING-GUIDE.md for the config shape.

Requires `cwebp` (brew install webp) for image conversion. Stdlib only.
"""
import argparse
import difflib
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

FEED = 'https://markedmondson.substack.com/feed'
NS = {'content': 'http://purl.org/rss/1.0/modules/content/'}
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGING = os.path.join(REPO, '.substack-staging')


# ------------------------------------------------------------------ feed access

def load_feed(refresh=False):
    os.makedirs(STAGING, exist_ok=True)
    cached = os.path.join(STAGING, 'feed.xml')
    if refresh or not os.path.exists(cached):
        req = urllib.request.Request(FEED, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(cached, 'wb') as f:
            f.write(data)
    return ET.parse(cached).getroot().findall('.//item')


def get_item(frag, items):
    for i in items:
        if frag in (i.findtext('link') or ''):
            return i
    raise SystemExit(f'no feed item matching {frag!r}')


# --------------------------------------------------------------- preprocessing

def skip_to_close(h, pos, tag):
    """Given pos just after an opening <tag>, return pos just after its </tag>."""
    depth = 1
    pat = re.compile(r'<(/?)' + tag + r'\b[^>]*>')
    while depth:
        m = pat.search(h, pos)
        if not m:
            return len(h)
        depth += -1 if m.group(1) else 1
        pos = m.end()
    return pos


def drop_div(h, cls):
    """Remove <div class="...cls..."> ... </div>, respecting nesting."""
    out, pos = [], 0
    pat = re.compile(r'<div[^>]*class="[^"]*\b' + re.escape(cls) + r'\b[^"]*"[^>]*>')
    while True:
        m = pat.search(h, pos)
        if not m:
            out.append(h[pos:])
            break
        out.append(h[pos:m.start()])
        pos = skip_to_close(h, m.end(), 'div')
    return ''.join(out)


def strip_widgets(h):
    """Remove Substack subscribe forms, share buttons and paywall furniture."""
    for cls in ('subscription-widget-wrap-editor', 'subscription-widget-wrap',
                'subscribe-widget', 'button-wrapper', 'captioned-button-wrap',
                'digest-post-embed', 'poll-embed', 'pencraft'):
        h = drop_div(h, cls)
    h = re.sub(r'<svg\b.*?</svg>', '', h, flags=re.S)
    h = re.sub(r'<form\b.*?</form>', '', h, flags=re.S)
    return h


def extract_media(h):
    """Replace figures and youtube embeds with @@MEDIAn@@ tokens."""
    media = []

    def fig_repl(m):
        block = m.group(0)
        im = re.search(r'<img[^>]*data-attrs="([^"]*)"', block)
        attrs = {}
        if im:
            try:
                attrs = json.loads(html.unescape(im.group(1)))
            except json.JSONDecodeError:
                pass
        # Prefer the rendered substackcdn url: it has EXIF orientation applied.
        # The raw S3 original in data-attrs does not, and cwebp ignores EXIF, so
        # iPhone photos come out rotated if you use it.
        im2 = re.search(r'<img[^>]*\ssrc="([^"]+)"', block)
        src = (html.unescape(im2.group(1)) if im2 else None) or attrs.get('src')
        if not src:
            return ''
        cap = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', block, re.S)
        media.append({
            'kind': 'img',
            'src': html.unescape(src),
            'alt': (attrs.get('alt') or '').strip(),
            'title': (attrs.get('title') or '').strip(),
            'caption': to_inline_md(cap.group(1)) if cap else '',
            'top': bool(attrs.get('topImage')),
        })
        return f'\n\n@@MEDIA{len(media) - 1}@@\n\n'

    h = re.sub(r'<figure\b.*?</figure>', fig_repl, h, flags=re.S)

    out, pos = [], 0
    ytpat = re.compile(r'<div[^>]*class="[^"]*\byoutube-wrap\b[^"]*"[^>]*>')
    while True:
        m = ytpat.search(h, pos)
        if not m:
            out.append(h[pos:])
            break
        out.append(h[pos:m.start()])
        end = skip_to_close(h, m.end(), 'div')
        block = h[m.start():end]
        vid = None
        da = re.search(r'data-attrs="([^"]*)"', block)
        if da:
            try:
                vid = json.loads(html.unescape(da.group(1))).get('videoId')
            except json.JSONDecodeError:
                pass
        if not vid:
            emb = re.search(r'embed/([A-Za-z0-9_-]{6,})', block)
            vid = emb.group(1) if emb else None
        if vid:
            media.append({'kind': 'yt', 'id': vid})
            out.append(f'\n\n@@MEDIA{len(media) - 1}@@\n\n')
        pos = end
    return ''.join(out), media


# ------------------------------------------------------------------ html -> md

INLINE_SKIP = {'button', 'input', 'source', 'picture', 'svg'}


class MD(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.buf = []
        self.stack = []
        self.list_stack = []
        self.href = None
        self.skip = 0
        self.li_depth = 0
        self.emph = []  # (marker, buffer index) per open strong/em/a span

    def out(self, s):
        self.buf.append(s)

    def close_emph(self, href=None):
        """Emit an emphasis or link span with padding whitespace moved OUTSIDE
        the markers. Substack writes "<strong>Read - </strong>" and
        "<a ...>Fable 5.0 </a>": "** x **" is not bold in markdown, and the space
        inside "[ x ]" is often the only separator from the next word."""
        if not self.emph:
            return
        marker, start = self.emph.pop()
        inner = ''.join(self.buf[start:])
        del self.buf[start:]
        stripped = inner.strip()
        if not stripped:
            self.out(inner if href is None else '')
            return
        lead = inner[:len(inner) - len(inner.lstrip())]
        trail = inner[len(inner.rstrip()):]
        if marker == '[':
            body = f'[{stripped}]({href})' if href else stripped
        else:
            body = f'{marker}{stripped}{marker}'
        self.out(f'{lead}{body}{trail}')

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.skip or tag in INLINE_SKIP:
            if tag in INLINE_SKIP:
                self.skip += 1
            return
        if tag in ('p', 'div'):
            # a <p> inside a <li> must not break the bullet onto a new line
            if not self.li_depth:
                self.out('\n\n')
        elif re.fullmatch(r'h[1-6]', tag):
            self.out('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag == 'br':
            self.out('  \n')
        elif tag == 'hr':
            self.out('\n\n---\n\n')
        elif tag in ('strong', 'b'):
            self.emph.append(('**', len(self.buf)))
        elif tag in ('em', 'i'):
            self.emph.append(('*', len(self.buf)))
        elif tag == 'code':
            self.out('`')
        elif tag == 'pre':
            self.out('\n\n```\n')
            self.stack.append('pre')
        elif tag == 'a':
            self.href = a.get('href')
            self.emph.append(('[', len(self.buf)))
        elif tag in ('ul', 'ol'):
            # indent a nested list past its parent's marker so CommonMark keeps
            # it inside that item ("- " is 2 cols, "1. " is 3)
            if self.list_stack:
                p_kind, _, p_pad = self.list_stack[-1]
                pad = p_pad + ('   ' if p_kind == 'ol' else '  ')
            else:
                pad = ''
            self.list_stack.append([tag, 0, pad])
            # a blank line here would close the parent item and restart numbering
            self.out('\n' if self.li_depth else '\n\n')
        elif tag == 'li':
            self.li_depth += 1
            if self.list_stack:
                self.list_stack[-1][1] += 1
                kind, n, pad = self.list_stack[-1]
                self.out('\n' + pad + (f'{n}. ' if kind == 'ol' else '- '))
        elif tag == 'blockquote':
            self.stack.append('quote')
            self.out('\n\n')

    def handle_endtag(self, tag):
        if tag in INLINE_SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in ('strong', 'b', 'em', 'i'):
            self.close_emph()
        elif tag == 'code' and 'pre' not in self.stack:
            self.out('`')
        elif tag == 'pre':
            self.out('\n```\n\n')
            if self.stack and self.stack[-1] == 'pre':
                self.stack.pop()
        elif tag == 'a':
            self.close_emph(href=self.href)
            self.href = None
        elif tag == 'li':
            self.li_depth = max(0, self.li_depth - 1)
        elif tag in ('ul', 'ol'):
            if self.list_stack:
                self.list_stack.pop()
            self.out('\n' if self.li_depth else '\n\n')
        elif tag == 'blockquote':
            if self.stack and self.stack[-1] == 'quote':
                self.stack.pop()
            self.out('\n\n')
        elif tag in ('p', 'div'):
            if not self.li_depth:
                self.out('\n\n')

    def handle_data(self, d):
        if self.skip:
            return
        if 'pre' in self.stack:
            self.out(d)
            return
        d = re.sub(r'\s+', ' ', d)
        if d.strip() == '' and (not self.buf or self.buf[-1].endswith((' ', '\n'))):
            return
        # MDX evaluates {...} as JS and reads "<x" as JSX, so prose like
        # "(<1s" or "{verdict, proposed_fix}" must be escaped
        d = d.replace('{', '&#123;').replace('}', '&#125;').replace('<', '&lt;')
        self.out(d)

    def result(self):
        return ''.join(self.buf)


def to_inline_md(frag):
    p = MD()
    p.feed(frag)
    return re.sub(r'\s+', ' ', p.result()).strip()


CTA_RE = re.compile(
    r'(?m)^\[(?:Subscribe now|Leave a comment|Share(?: this post)?|Give a gift '
    r'subscription|Pledge your support)\]\([^)]*\)[ \t]*$\n?')


def tidy(md):
    # Substack CTAs that sit outside a widget div survive as bare links
    md = CTA_RE.sub('', md)
    md = re.sub(r'[ \t]+\n', '\n', md)
    md = re.sub(r'\n{3,}', '\n\n', md)
    # tidy space before sentence punctuation, but never before a word (" .ail")
    md = re.sub(r' +([,.;:!?])(?=\s|$)', r'\1', md)
    # collapse spaces mid-line only: keeps "  \n" hard breaks and list indents
    md = re.sub(r'(?<=\S)  +(?=\S)', ' ', md)
    # a stray leading space turns an MDX block (iframe, image) into indented text
    md = re.sub(r'(?m)^ (?=[!<#])', '', md)
    # NB: do NOT strip leading spaces before list markers (breaks nesting), and
    # do NOT strip spaces inside "[ ... ]" (that space separates words).
    # Emphasis padding is handled in MD.close_emph, at the parser level.
    return md.strip() + '\n'


# ----------------------------------------------------------------------- images

def slugify(s, n=40):
    return re.sub(r'[^a-z0-9]+', '-', (s or '').lower()).strip('-')[:n].strip('-')


def sniff_ext(data):
    """The CDN url ends in .png but serves f_auto, so sniff the real format."""
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return '.webp'
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return '.png'
    if data[:3] == b'\xff\xd8\xff':
        return '.jpg'
    if data[:6] in (b'GIF87a', b'GIF89a'):
        return '.gif'
    return '.png'


def download_images(media, outdir, slug):
    os.makedirs(outdir, exist_ok=True)
    for idx, m in enumerate(media):
        if m['kind'] != 'img':
            continue
        hint = slugify(m['alt'] or m['title'] or m['caption']) or f'img-{idx + 1:02d}'
        base = f'{idx + 1:02d}-{hint}'
        req = urllib.request.Request(m['src'], headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
        except Exception as e:  # noqa: BLE001
            print(f'  !! failed {m["src"]}: {e}', file=sys.stderr)
            m['file'] = None
            continue
        ext = sniff_ext(data)
        raw = os.path.join(outdir, base + ext)
        with open(raw, 'wb') as f:
            f.write(data)
        final = raw
        if ext in ('.png', '.jpg', '.jpeg'):
            webp = os.path.join(outdir, base + '.webp')
            r = subprocess.run(['cwebp', '-quiet', '-q', '82', raw, '-o', webp],
                               capture_output=True)
            if r.returncode == 0 and os.path.getsize(webp) < os.path.getsize(raw):
                os.remove(raw)
                final = webp
            elif os.path.exists(webp):
                os.remove(webp)  # keep the smaller original
        m['file'] = f'./img/{slug}/{os.path.basename(final)}'
        print(f'  img {idx + 1:02d} -> {m["file"]} ({os.path.getsize(final) // 1024}kB)')


def render_media(m):
    if m['kind'] == 'yt':
        return ('<iframe width="100%" height="420" '
                f'src="https://www.youtube.com/embed/{m["id"]}" '
                'title="YouTube video" frameBorder="0" '
                'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
                'gyroscope; picture-in-picture" allowFullScreen '
                "style={{borderRadius:'8px'}}></iframe>")
    if not m.get('file'):
        return ''
    alt = (m['alt'] or m['caption'] or '').replace('[', '').replace(']', '')
    s = f'![{alt}]({m["file"]})'
    if m['caption']:
        s += f'\n\n*{m["caption"]}*'
    return s


# --------------------------------------------------------------------- commands

def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', (s or '').lower())


def cmd_list(args):
    """Report which feed posts look unmirrored.

    Matching is fuzzy on the title, because a mirrored post is sometimes
    retitled for the blog. Anything ambiguous is reported as '?' rather than
    guessed either way; add a known pair to scripts/mirrored-overrides.json
    to silence it for good.
    """
    items = load_feed(refresh=args.refresh)
    ovr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mirrored-overrides.json')
    overrides = json.load(open(ovr_path)) if os.path.exists(ovr_path) else {}

    have = []
    for f in sorted(glob.glob(os.path.join(REPO, 'blog', '*.md')) +
                    glob.glob(os.path.join(REPO, 'blog', '*.mdx'))):
        txt = open(f).read()
        t = re.search(r'(?m)^title:\s*(.+?)\s*$', txt)
        title = (t.group(1).strip('\'"') if t else '')
        have.append((title, os.path.basename(f)))

    missing, unsure = [], []
    print(f'{"substack post":56} {"published":12} mirrored')
    for i in items:
        title = (i.findtext('title') or '').strip()
        pub = (i.findtext('pubDate') or '')[5:16]
        link = i.findtext('link') or ''
        sslug = link.split('/p/')[-1]

        if sslug in overrides:
            print(f'{title[:56]:56} {pub:12} yes  {overrides[sslug]} (override)')
            continue

        best, score = None, 0.0
        for h, fn in have:
            r = difflib.SequenceMatcher(None, norm(title), norm(h)).ratio()
            if r > score:
                best, score = fn, r
        if score > 0.75:
            state = f'yes  {best}'
        elif score > 0.45:
            state = f'?    maybe {best} ({score:.2f}) -- check, then add override'
            unsure.append(sslug)
        else:
            state = f'NO   fetch fragment: {sslug}'
            missing.append(sslug)
        print(f'{title[:56]:56} {pub:12} {state}')

    print(f'\n{len(missing)} clearly unmirrored, {len(unsure)} ambiguous.')
    if missing:
        print('Next: scripts/mirror_substack.py fetch <fragment> <slug>')


def cmd_fetch(args):
    items = load_feed(refresh=args.refresh)
    item = get_item(args.fragment, items)
    slug = args.slug
    raw = item.find('content:encoded', NS).text

    h, media = extract_media(strip_widgets(raw))
    p = MD()
    p.feed(h)
    md = tidy(p.result())

    os.makedirs(STAGING, exist_ok=True)
    print(f'{slug}: {len(media)} media item(s)')
    download_images(media, os.path.join(STAGING, 'img', slug), slug)

    md = tidy(re.sub(r'@@MEDIA(\d+)@@',
                     lambda m: render_media(media[int(m.group(1))]), md))

    meta = {'title': (item.findtext('title') or '').strip(),
            'link': item.findtext('link'),
            'pubDate': item.findtext('pubDate'),
            'media': media}
    with open(os.path.join(STAGING, f'{slug}.body.md'), 'w') as f:
        f.write(md)
    with open(os.path.join(STAGING, f'{slug}.meta.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    print(f'  wrote .substack-staging/{slug}.body.md ({len(md)} chars)')
    print('  now write frontmatter + alt text into a config and run: assemble')


def fix_headings(md):
    """Substack's biggest header is h1, but the post title is already the page
    h1. Shift so the top level used in the body lands on h2."""
    levels = {len(m) for m in re.findall(r'(?m)^(#{1,6}) ', md)}
    if not levels or min(levels) == 2:
        return md
    shift = 2 - min(levels)
    return re.sub(r'(?m)^(#{1,6}) ',
                  lambda m: '#' * max(2, min(6, len(m.group(1)) + shift)) + ' ', md)


def yaml_str(key, val):
    return f"{key}: '{val}'" if '"' in val else f'{key}: "{val}"'


def cmd_assemble(args):
    posts = json.load(open(args.config))
    for p in posts if isinstance(posts, list) else [posts]:
        slug, date = p['slug'], p['date']
        body = open(os.path.join(STAGING, f'{slug}.body.md')).read()
        meta = json.load(open(os.path.join(STAGING, f'{slug}.meta.json')))
        alts = {int(k): v for k, v in p['images'].items()}

        imgdir = os.path.join(REPO, 'blog', 'img', slug)
        os.makedirs(imgdir, exist_ok=True)
        hero, n = None, 0
        for m in meta['media']:
            if m['kind'] != 'img' or not m.get('file'):
                continue
            n += 1
            if n not in alts:
                raise SystemExit(f'{slug}: no name/alt configured for image {n}')
            name, alt = alts[n]
            src = os.path.join(STAGING, 'img', slug, os.path.basename(m['file']))
            newbase = f'{n:02d}-{name}{os.path.splitext(src)[1]}'
            shutil.copy2(src, os.path.join(imgdir, newbase))
            newrel = f'./img/{slug}/{newbase}'
            body = body.replace(f'![]({m["file"]})', f'![{alt}]({newrel})')
            body = body.replace(m['file'], newrel)
            if n == p.get('hero', 1):
                hero = newrel

        body = fix_headings(body)
        paras = body.split('\n\n')
        lead, rest = paras[0], '\n\n'.join(paras[1:])

        fm = ['---', yaml_str('title', p['title']), 'authors: me',
              f'tags: [{", ".join(p["tags"])}]']
        if hero:
            fm.append(f'image: {hero}')
        fm += [f'slug: /{slug}', yaml_str('description', p['description']),
               '---', '', '']

        out = '\n'.join(fm) + lead + '\n\n<!-- truncate -->\n\n' + rest
        out = re.sub(r'(?m)^ (?=[!<#])', '', out)
        path = os.path.join(REPO, 'blog', f'{date}-{slug}.mdx')
        with open(path, 'w') as f:
            f.write(out)
        print(f'blog/{date}-{slug}.mdx ({len(out)} chars, {n} images, hero={p.get("hero", 1)})')
    print('\nNow run: yarn build')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--refresh', action='store_true', help='re-download the feed')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('list', help='report posts not yet mirrored')
    f = sub.add_parser('fetch', help='convert one post into .substack-staging/')
    f.add_argument('fragment', help='distinctive part of the substack url')
    f.add_argument('slug', help='blog slug to use')
    a = sub.add_parser('assemble', help='build blog mdx from staged bodies')
    a.add_argument('config', help='json config (see scripts/MIRRORING-GUIDE.md)')
    args = ap.parse_args()
    {'list': cmd_list, 'fetch': cmd_fetch, 'assemble': cmd_assemble}[args.cmd](args)


if __name__ == '__main__':
    main()
