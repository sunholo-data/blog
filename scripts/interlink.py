#!/usr/bin/env python3
"""Add contextual internal + cross-property links to blog posts.

Anchor text is the phrase already in the prose, so links read naturally and the
anchor carries the term we want to rank for. Only the FIRST unprotected
occurrence per (post, target) is linked, and protected regions are never touched:
frontmatter, code fences, inline code, existing links/images, JSX/HTML tags and
heading lines.
"""
import os
import re
import sys

BLOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'blog')
MAX_PER_POST = 8

A = 'https://ailang.sunholo.com'
W = 'https://www.sunholo.com'

# (phrase regex, target url, short label for reporting)
RULES = [
    # === blog -> blog. Listed FIRST because inbound internal links are what
    # the orphaned posts actually lack. ==================================
    (r'coding harnesses', '/blog/ai-coding-an-ai-coding-harness', 'b:harness'),
    (r'AI coding harness', '/blog/ai-coding-an-ai-coding-harness', 'b:harness'),
    (r'loop engineering', '/blog/ai-loop-engineering-dark-software-factory', 'b:loop'),
    (r'dark factory', '/blog/ai-loop-engineering-dark-software-factory', 'b:loop'),
    (r'deontic logic', '/blog/ai-workflows-beyond-extraction', 'b:deontic'),
    (r'freedom of a tight brief', '/blog/ai-freedom-tight-brief', 'b:brief'),
    (r'tight brief', '/blog/ai-freedom-tight-brief', 'b:brief'),
    (r'entropy budgets?', '/blog/ai-freedom-tight-brief', 'b:brief'),
    (r'[Cc]ognitive [Dd]esigns?', '/blog/cognitive-design', 'b:cogdesign'),
    (r'internal monologues?', '/blog/subconscious-genai', 'b:subconscious'),
    (r'AI [Pp]rotocol [Rr]evolution', '/blog/ai-protocol-revolution', 'b:protorev'),
    (r'[Cc]an I [Tt]rust AI', '/blog/wrong-question-ai-trust', 'b:trust'),
    (r'\bWebSummerCamp\b', '/blog/ai-protocols-in-paradise-opatija', 'b:opatija'),
    (r'[Aa]ccounts[- ][Pp]ayable', '/blog/ap-accounts-payable-ai-workflow', 'b:ap'),
    (r'physics students', '/blog/ai-platform-physics-students', 'b:physics'),
    (r'\bMotoko\b', '/blog/who-needs-fable-local-models-ailang', 'b:fable'),
    (r'local open-source models', '/blog/who-needs-fable-local-models-ailang', 'b:fable'),
    # NB: no /blog/ailang-cloud rule -- that post is draft: true, so it is not
    # built and linking to it breaks the build. live_blog_slugs() enforces this.
    (r'[Ww]ebsite [Bb]uilder', '/blog/website-builder', 'b:webbuilder'),
    (r'self-maintaining software', '/blog/ailang-v09', 'b:v09'),
    (r'“I don’t know”', '/blog/any-ai-that-cant-say-i-dont-know', 'b:refusal'),
    (r'IDA Driving AI', '/blog/ida-driving-ai-talk-2026', 'b:ida'),
    (r'AILANG Parse', '/blog/ailang-parse-launch', 'b:parselaunch'),

    # === commercial pages: highest intent ===============================
    (r'AI engineering journey', f'{W}/ai-engineering', 'ai-engineering'),
    (r'\bAI [Ee]ngineer\b', f'{W}/ai-engineering', 'ai-engineering'),
    (r'\bAI engineering\b', f'{W}/ai-engineering', 'ai-engineering'),
    (r'AI platform engineering', f'{W}/ai-platform', 'ai-platform'),
    (r'AI platforms', f'{W}/ai-platform', 'ai-platform'),
    (r'\bMultivac\b', f'{W}/ai-platform', 'ai-platform'),
    (r'AI engineering workshops', f'{W}/workshops', 'workshops'),
    (r'universal document parsing', f'{W}/ailang-parse', 'ailang-parse'),
    (r'deterministic (?:Office|document) (?:parsing|extraction)', f'{W}/ailang-parse',
     'ailang-parse'),
    (r'green energy contracts', f'{W}/case-study-aitana', 'case-aitana'),
    (r'\bAitana\b', f'{W}/case-study-aitana', 'case-aitana'),
    (r'AI in Physics Learning and Assessment', f'{W}/aipla', 'aipla'),

    # === AILANG docs: deep technical terms ==============================
    (r'AI-first programming language', f'{A}/docs/why-ailang', 'why-ailang'),
    (r'a new programming language made exclusively for AI Coders',
     f'{A}/docs/why-ailang', 'why-ailang'),
    (r'AILANG benchmarks', f'{A}/docs/benchmarks/overview', 'benchmarks'),
    (r'open[- ]source (?:coding )?champion', f'{A}/docs/benchmarks/os-model-leaderboard',
     'os-leaderboard'),
    (r'neurosymbolic (?:verification|programming)', f'{A}/docs/guides/contracts', 'contracts'),
    (r'AILANG package registry', f'{A}/docs/packages/explorer', 'packages'),
    (r'function effects', f'{A}/docs/reference/effects', 'effects'),
    (r'effect system', f'{A}/docs/reference/effects', 'effects'),
]


def protected_mask(txt):
    """True where a link must NOT be inserted."""
    mask = [False] * len(txt)

    def block(a, b):
        for i in range(max(0, a), min(len(txt), b)):
            mask[i] = True

    # frontmatter
    if txt.startswith('---'):
        end = txt.find('\n---', 3)
        if end != -1:
            block(0, end + 4)
    # NB: re.S only where the region genuinely spans lines. Applying it to the
    # heading pattern makes ".*$" swallow the whole document.
    for pat, flags in (
        (r'```.*?```', re.S),                     # fenced code
        (r':::.*?:::', re.S),                     # admonitions
        (r'`[^`\n]+`', 0),                        # inline code
        (r'!\[[^\]]*\]\([^)]*\)', 0),             # images
        (r'\[[^\]]*\]\([^)]*\)', 0),              # existing links
        (r'<[^>]+>', 0),                          # html / jsx tags
        (r'^#{1,6} .*$', re.M),                   # headings
        (r'^\s*(?:import|export) .*$', re.M),     # mdx imports
    ):
        for m in re.finditer(pat, txt, flags):
            block(m.start(), m.end())
    return mask


def live_blog_slugs():
    """Slugs of posts that actually build: a draft post is not published, so
    linking to it is a broken link (onBrokenLinks: throw catches this)."""
    live = set()
    for f in os.listdir(BLOG):
        if not f.endswith(('.md', '.mdx')):
            continue
        txt = open(os.path.join(BLOG, f)).read()
        if re.search(r'(?m)^draft:\s*true\s*$', txt):
            continue
        m = re.search(r'(?m)^slug:\s*/?(\S+)\s*$', txt)
        if m:
            live.add(m.group(1).lstrip('/'))
    return live


LIVE = None


def add_links(path, budget):
    txt = open(path).read()
    orig = txt
    added = []
    # self-link check must use the frontmatter slug: the filename often differs
    # (2026-06-02-ida-ailang-talk-retrospective.mdx is slug /ida-driving-ai-talk-2026)
    m = re.search(r'(?m)^slug:\s*/?(\S+)\s*$', txt)
    own_slug = m.group(1).lstrip('/') if m else None
    for phrase, url, label in RULES:
        if len(added) >= budget:
            break
        if url in txt:               # already linked somewhere in this post
            continue
        if url.startswith('/blog/'):
            target = url.rsplit('/', 1)[1]
            if target == own_slug:
                continue             # never self-link
            if LIVE is not None and target not in LIVE:
                print(f'   !! skip {label}: /blog/{target} is not a live post',
                      file=sys.stderr)
                continue
        mask = protected_mask(txt)
        for m in re.finditer(phrase, txt):
            if any(mask[m.start():m.end()]):
                continue
            anchor = m.group(0)
            txt = txt[:m.start()] + f'[{anchor}]({url})' + txt[m.end():]
            added.append((label, anchor, url))
            break
    if txt != orig:
        with open(path, 'w') as f:
            f.write(txt)
    return added


def main():
    global LIVE
    LIVE = live_blog_slugs()
    dry = '--dry' in sys.argv
    total = 0
    for path in sorted(os.listdir(BLOG)):
        if not path.endswith(('.md', '.mdx')):
            continue
        full = os.path.join(BLOG, path)
        before = open(full).read()
        added = add_links(full, MAX_PER_POST)
        if dry:
            with open(full, 'w') as f:
                f.write(before)
        if added:
            print(f'\n{path}')
            for label, anchor, url in added:
                print(f'   +{label:16} "{anchor}" -> {url}')
            total += len(added)
    print(f'\n{total} links added')


if __name__ == '__main__':
    main()
