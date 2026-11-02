"""Check local Markdown navigation without network access or project execution."""

import re
import subprocess
import sys
import unicodedata
from collections import deque
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MISSION = '> **Mission:** Reliable technology and informed security decisions'


def without_fences(text):
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return '\n'.join(lines)


class HTMLReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.urls.append(attrs['href'])
        if tag == 'img' and 'src' in attrs:
            self.urls.append(attrs['src'])


def read_page(path):
    text = without_fences(path.read_text(encoding='utf-8'))
    html = HTMLReferences()
    html.feed(text)
    urls = list(html.urls)
    for match in re.finditer(r'!?\[[^\]\n]*\]\(\s*(?:<([^>]+)>|([^\s]+?))(?:\s+["\'][^\n]*?["\'])?\s*\)', text):
        urls.append(match.group(1) or match.group(2))
    anchors, used = set(html.ids), {}
    for match in re.finditer(r'^ {0,3}#{1,6}\s+(.+?)\s*#*$', text, re.M):
        heading = unescape(re.sub(r'<[^>]*>', '', match.group(1))).lower()
        slug = ''.join(c for c in heading if unicodedata.category(c)[0] not in 'PS' or c in '-_')
        slug = slug.replace(' ', '-')
        number = used.get(slug, 0)
        used[slug] = number + 1
        anchors.add(slug + (f'-{number}' if number else ''))
    return urls, anchors


def resolve(source, url):
    parts = urlsplit(unescape(url))
    if parts.scheme or parts.netloc:
        return None, ''
    target = ((ROOT if parts.path.startswith('/') else source.parent) / unquote(parts.path).lstrip('/')).resolve() if parts.path else source
    if target.is_dir() and (target / 'README.md').exists():
        target = target / 'README.md'
    return target, unquote(parts.fragment)


def markdown_paths():
    """Use Git's ignore rules while including new, unstaged documentation."""
    try:
        result = subprocess.run(
            ['git', 'ls-files', '--cached', '--others', '--exclude-standard',
             '-z', '--', '*.md'],
            cwd=ROOT, capture_output=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise RuntimeError('Run portfolio validation from a Git checkout.') from error
    names = result.stdout.decode('utf-8').split('\0')
    return sorted({ROOT / name for name in names if name and (ROOT / name).is_file()})


def main():
    try:
        paths = markdown_paths()
    except RuntimeError as error:
        print('ERROR:', error, file=sys.stderr)
        return True
    pages = {path: read_page(path) for path in paths}
    errors, references, fragments = [], 0, 0
    graph = {}
    for path, (urls, _) in pages.items():
        graph[path] = []
        for url in urls:
            target, fragment = resolve(path, url)
            if target is None:
                continue
            references += 1
            if not target.exists():
                errors.append(f'{path.relative_to(ROOT)}: missing target {url}')
            elif target in pages:
                graph[path].append(target)
                if fragment:
                    fragments += 1
                    if fragment not in pages[target][1]:
                        errors.append(f'{path.relative_to(ROOT)}: missing anchor {url}')
    readmes = [p for p in paths if p.name == 'README.md' and (p.parent == ROOT or re.match(r'^\d\d_', p.relative_to(ROOT).parts[0]))]
    for path in readmes:
        text = path.read_text(encoding='utf-8')
        if text.count('> **Author:** Komiljon Karimov') != 1 or text.count(MISSION) != 1:
            errors.append(f'{path.relative_to(ROOT)}: expected one standard author/mission footer')
        if len(re.findall(r'^# ', without_fences(text), re.M)) != 1:
            errors.append(f'{path.relative_to(ROOT)}: expected one page title')
    reached, queue = set(), deque([ROOT / 'README.md'])
    while queue:
        page = queue.popleft()
        if page in reached:
            continue
        reached.add(page)
        queue.extend(graph.get(page, []))
    for page in readmes:
        if page not in reached:
            errors.append(f'{page.relative_to(ROOT)}: unreachable from portfolio homepage')
    for error in errors:
        print('ERROR:', error, file=sys.stderr)
    print(f'Checked {len(paths)} Markdown files, {references} local references, {fragments} anchors, and {len(readmes)} README pages: {len(errors)} errors.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
