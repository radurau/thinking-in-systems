#!/usr/bin/env python3
"""List (or remove) Romanian keys in i18n-ro.js that no page uses any more.

The deck and the notes panel look translations up by the normalised English
innerHTML of each translatable element, so a key becomes dead whenever its
English text is edited. Collect the live keys from both pages first (run in
each page's console, or via a browser tool):

    JSON.stringify([...document.querySelectorAll(SEL.join(','))].map(el =>
        el.innerHTML.replace(/\\s+/g,' ').trim()))

save them as JSON arrays, then:

    python3 tools/prune-ro.py deck-keys.json notes-keys.json          # report
    python3 tools/prune-ro.py deck-keys.json notes-keys.json --write  # remove

Keys are matched after the same whitespace normalisation the pages apply.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RO = ROOT / 'i18n-ro.js'
ENTRY = re.compile(r'^\[`(.*?)`, `.*?`\],\n', re.M | re.S)

def norm(s): return re.sub(r'\s+', ' ', s).strip()

def main():
    files = [a for a in sys.argv[1:] if not a.startswith('--')]
    write = '--write' in sys.argv
    used = set()
    for f in files:
        used.update(norm(k) for k in json.loads(pathlib.Path(f).read_text(encoding='utf-8')))
    src = RO.read_text(encoding='utf-8')
    dead = [m for m in ENTRY.finditer(src) if norm(m.group(1)) not in used]
    print(f'{len(list(ENTRY.finditer(src)))} keys, {len(used)} live strings, {len(dead)} unused')
    for m in dead:
        print('  -', m.group(1)[:100].replace('\n', ' '))
    if write and dead:
        for m in reversed(dead):
            src = src[:m.start()] + src[m.end():]
        RO.write_text(src, encoding='utf-8')
        print(f'removed {len(dead)} keys')
    return 0

if __name__ == '__main__':
    sys.exit(main())
