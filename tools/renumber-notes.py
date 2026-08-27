#!/usr/bin/env python3
"""Renumber the speaker-notes panel from DOM order.

Slides in presentation.html are numbered by DOM order, so inserting a slide shifts
every later number. The notes panel hard-codes those numbers in four places per
section:  id="nN"  ·  <span class="num">0N</span>  ·  href="presentation.html#N"
·  "Slide N ↗".  Run this after inserting/removing slides:

    python3 tools/renumber-notes.py          # rewrite in place
    python3 tools/renumber-notes.py --check  # exit 1 if anything would change

It also refreshes the "N slides" pill and the <!-- ==== N ==== --> markers, and
warns when the number of note sections differs from the number of deck slides.
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
NOTES = ROOT / 'thinking-in-systems-notes.html'
DECK = ROOT / 'presentation.html'

def main():
    check = '--check' in sys.argv
    src = NOTES.read_text(encoding='utf-8')
    n_slides = len(re.findall(r'<section class="slide"', DECK.read_text(encoding='utf-8')))

    # Split at each note section so we can renumber per block.
    parts = re.split(r'(?=<section class="note")', src)
    head, blocks = parts[0], parts[1:]
    if len(blocks) != n_slides:
        print(f'warning: {len(blocks)} note sections vs {n_slides} deck slides', file=sys.stderr)

    out = [re.sub(r'<span class="pill">\d+ slides</span>',
                  f'<span class="pill">{n_slides} slides</span>', head)]
    for i, b in enumerate(blocks, 1):
        b = re.sub(r'(<section class="note"[^>]*\bid=")n\d+(")', rf'\g<1>n{i}\2', b, count=1)
        b = re.sub(r'(<span class="num">)\d+(</span>)', rf'\g<1>{i:02d}\2', b, count=1)
        b = re.sub(r'(href="presentation\.html#)\d+(")', rf'\g<1>{i}\2', b, count=1)
        b = re.sub(r'(>Slide )\d+( ↗<)', rf'\g<1>{i}\2', b, count=1)
        # the "<!-- ==== N ==== -->" marker for the *next* section lives at the end of this block
        b = re.sub(r'(<!-- =+ )\S+( =+ -->\s*)$', rf'\g<1>{i+1}\2', b)
        out.append(b)
    new = ''.join(out)

    if new == src:
        print('notes panel already in sync'); return 0
    if check:
        print('notes panel out of sync (run without --check to fix)'); return 1
    NOTES.write_text(new, encoding='utf-8')
    print(f'renumbered {len(blocks)} note sections'); return 0

if __name__ == '__main__':
    sys.exit(main())
