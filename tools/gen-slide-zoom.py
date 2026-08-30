#!/usr/bin/env python3
"""Generate the zoom-out figure on slide 4 (What is a system? — tree · body · planet, then → zooms out).
Scenes crossfade with a scale transition driven by .step-item chips (.zs.s1 … .zs.s4)."""
import math, pathlib, random
random.seed(7)
def f(v): return f'{v:.1f}'
BLUE, TEAL, GOLD, INK = '#9db9ff', '#7fe7d4', '#fbbf24', 'rgba(245,245,247,.8)'
def rows(cx, el, ic, pu, d=1.2):
    return f'''<text class="fadein" x="{cx}" y="236" text-anchor="middle" style="--d:{d}s;font-size:12.5px"><tspan style="fill:{BLUE};font-weight:650">elements</tspan> — {el}</text>
        <text class="fadein" x="{cx}" y="262" text-anchor="middle" style="--d:{d+.15}s;font-size:12.5px"><tspan style="fill:{TEAL};font-weight:650">interconnections</tspan> — {ic}</text>
        <text class="fadein" x="{cx}" y="288" text-anchor="middle" style="--d:{d+.3}s;font-size:12.5px"><tspan style="fill:{GOLD};font-weight:650">purpose</tspan> — {pu}</text>'''
def header(cx, txt, d=.4): return f'<text class="fadein lbl-strong" x="{cx}" y="34" text-anchor="middle" style="--d:{d}s;font-size:15px">{txt}</text>'
def tree(cx, gy, s=1.0, cls=''):
    return f'''<g {cls}><line x1="{cx}" y1="{f(gy)}" x2="{cx}" y2="{f(gy-46*s)}" stroke="rgba(196,150,110,.85)" stroke-width="{f(9*s)}" stroke-linecap="round"/>
          <circle cx="{cx}" cy="{f(gy-70*s)}" r="{f(30*s)}" fill="rgba(94,234,212,.30)" stroke="rgba(94,234,212,.7)" stroke-width="1.5"/>
          <circle cx="{f(cx-24*s)}" cy="{f(gy-52*s)}" r="{f(21*s)}" fill="rgba(94,234,212,.30)" stroke="rgba(94,234,212,.7)" stroke-width="1.5"/>
          <circle cx="{f(cx+24*s)}" cy="{f(gy-52*s)}" r="{f(21*s)}" fill="rgba(94,234,212,.30)" stroke="rgba(94,234,212,.7)" stroke-width="1.5"/>
          <path d="M {cx} {f(gy)} l {f(-16*s)} {f(12*s)} M {cx} {f(gy)} l {f(16*s)} {f(12*s)} M {cx} {f(gy)} l {f(-5*s)} {f(16*s)} M {cx} {f(gy)} l {f(6*s)} {f(15*s)}" stroke="rgba(196,150,110,.6)" stroke-width="{f(2*s)}" fill="none" stroke-linecap="round"/></g>'''
def person(cx, gy, s=1.0, color='#7aa2ff', cls=''):
    return f'''<g {cls} stroke="{color}" stroke-width="{f(2.4*s)}" stroke-linecap="round" fill="none"><circle cx="{cx}" cy="{f(gy-98*s)}" r="{f(12*s)}" fill="{color}" stroke="none"/>
          <line x1="{cx}" y1="{f(gy-84*s)}" x2="{cx}" y2="{f(gy-40*s)}"/><line x1="{cx}" y1="{f(gy-74*s)}" x2="{f(cx-22*s)}" y2="{f(gy-46*s)}"/><line x1="{cx}" y1="{f(gy-74*s)}" x2="{f(cx+22*s)}" y2="{f(gy-46*s)}"/>
          <line x1="{cx}" y1="{f(gy-40*s)}" x2="{f(cx-15*s)}" y2="{f(gy)}"/><line x1="{cx}" y1="{f(gy-40*s)}" x2="{f(cx+15*s)}" y2="{f(gy)}"/></g>'''
def animal(cx, gy, s=1.0, color='rgba(251,191,36,.9)'):
    return f'''<g fill="{color}"><ellipse cx="{cx}" cy="{f(gy-7*s)}" rx="{f(9*s)}" ry="{f(4.5*s)}"/><circle cx="{f(cx+10*s)}" cy="{f(gy-11*s)}" r="{f(3.2*s)}"/>
          <path d="M {f(cx-6*s)} {f(gy-4*s)} v {f(4*s)} M {f(cx-2*s)} {f(gy-4*s)} v {f(4*s)} M {f(cx+3*s)} {f(gy-4*s)} v {f(4*s)} M {f(cx+7*s)} {f(gy-4*s)} v {f(4*s)}" stroke="{color}" stroke-width="{f(1.6*s)}"/></g>'''
def earth(cx, cy, r):
    return f'''<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(122,162,255,.22)" stroke="rgba(157,185,255,.8)" stroke-width="1.5"/>
          <path d="M {cx-r*.55:.1f} {cy-r*.35:.1f} q {r*.25:.1f} {-r*.35:.1f} {r*.55:.1f} {-r*.1:.1f} q {r*.3:.1f} {r*.25:.1f} {-r*.05:.1f} {r*.45:.1f} q {-r*.4:.1f} {r*.1:.1f} {-r*.5:.1f} {-r*.35:.1f} z" fill="rgba(94,234,212,.35)"/>
          <path d="M {cx+r*.1:.1f} {cy+r*.2:.1f} q {r*.35:.1f} {-r*.2:.1f} {r*.45:.1f} {r*.2:.1f} q {-r*.1:.1f} {r*.4:.1f} {-r*.45:.1f} {r*.3:.1f} q {-r*.2:.1f} {-r*.3:.1f} 0 {-r*.5:.1f} z" fill="rgba(94,234,212,.3)"/>'''
# ---------- scene 0: a tree · a human body · a planet ----------
s0 = f'''
      <g class="zsc zsc0">
        {header(150,'a tree')}{header(450,'a human body',.5)}{header(750,'a planet',.6)}
        <g class="pop" style="--d:.5s">{tree(150,186)}</g>
        <g class="pop" style="--d:.65s">{person(450,192)}<circle cx="446" cy="118" r="3.5" fill="#fb7185"/></g>
        <g class="pop" style="--d:.8s">{earth(750,124,62)}
          {tree(736,132,.32)}{person(766,144,.36,'#f5f5f7')}{animal(748,158,.7)}</g>
        {rows(150,'roots, trunk, leaves','sap, water, sunlight','grow, seed, survive')}
        {rows(450,'organs, bones, cells','blood, nerves, hormones','stay alive',1.35)}
        {rows(750,'oceans, forests, creatures','water, carbon, food chains','stay habitable',1.5)}
        <text class="fadein lbl-sm" x="450" y="334" text-anchor="middle" style="--d:2s;font-size:12.5px">three things nobody would call alike — the same three parts in each</text>
      </g>'''
# ---------- scene 1: a forest · a society · a planet with its moon ----------
forest = ''.join(tree(60+i*22.5, 190, 0.34+0.1*((i*7)%3)) for i in range(9))
skyline = ''.join(f'<rect x="{360+i*20}" y="{190-h}" width="15" height="{h}" fill="rgba(245,245,247,.08)" stroke="rgba(245,245,247,.25)"/>' for i,h in enumerate([40,72,55,90,48,66,80,44,60]))
crowd = ''.join(person(372+i*20, 190, 0.34, '#7aa2ff' if i%3 else '#c084fc') for i in range(9))
s1 = f'''
      <g class="zsc zsc1 near">
        {header(150,'a forest')}{header(450,'a society',.5)}{header(750,'a planet',.6)}
        <line x1="50" y1="190" x2="250" y2="190" stroke="rgba(245,245,247,.25)"/>{forest}
        <line x1="350" y1="190" x2="550" y2="190" stroke="rgba(245,245,247,.25)"/>{skyline}{crowd}
        <ellipse cx="750" cy="124" rx="96" ry="34" fill="none" stroke="rgba(245,245,247,.18)" stroke-dasharray="3 6"/>
        {earth(750,124,40)}<circle cx="846" cy="124" r="6" fill="rgba(245,245,247,.6)"><animateMotion dur="9s" repeatCount="indefinite" path="M 0 0 a 96 34 0 1 0 -192 0 a 96 34 0 1 0 192 0"/></circle>
        {rows(150,'trees, soil, deer, fungi','shade, seeds, shared roots','persist through fire and winter',0)}
        {rows(450,'people, roads, laws','trade, language, trust','thrive together',0)}
        {rows(750,'forests, societies, oceans','climate, tides, migration','keep the whole thing alive',0)}
        <text class="lbl-sm" x="450" y="334" text-anchor="middle" style="font-size:12.5px">one level out — still elements, interconnections, purpose</text>
      </g>'''
# ---------- scene 2: the solar system ----------
orbits = ''.join(f'<ellipse cx="450" cy="200" rx="{rx}" ry="{rx*.38:.1f}" fill="none" stroke="rgba(245,245,247,.16)"/>' for rx in (48,80,116,156,204,252,300,346))
angs = [0.6,2.4,4.9,1.4,3.6,5.6,0.9,2.9]; planets=''
for i,(rx,a) in enumerate(zip((48,80,116,156,204,252,300,346),angs)):
    px,py = 450+rx*math.cos(a), 200+rx*.38*math.sin(a)
    if i==2:
        planets += f'<circle cx="{f(px)}" cy="{f(py)}" r="5" fill="#7aa2ff"/><circle class="pulse" cx="{f(px)}" cy="{f(py)}" r="7" fill="none" stroke="#7aa2ff" stroke-width="1.5"/><text class="lbl-sm" x="{f(px+10)}" y="{f(py-8)}" style="fill:#9db9ff;font-size:12px">Earth — every forest and every society</text>'
    else:
        planets += f'<circle cx="{f(px)}" cy="{f(py)}" r="{2.5+(i%3)*1.2:.1f}" fill="rgba(245,245,247,{.5+.1*(i%3):.1f})"/>'
s2 = f'''
      <g class="zsc zsc2 near">
        {header(450,'the solar system')}
        {orbits}<circle cx="450" cy="200" r="15" fill="#fbbf24"/><circle cx="450" cy="200" r="24" fill="none" stroke="rgba(251,191,36,.35)"/>
        {planets}
        <text class="lbl-sm" x="450" y="372" text-anchor="middle" style="font-size:12.5px">elements — a star and its planets · interconnections — gravity, light · purpose — none we chose; it just holds</text>
      </g>'''
# ---------- scene 3: the galaxy ----------
stars=''
for arm in range(2):
    for k in range(300):
        t = 0.25 + k*0.0165; r = 12*math.exp(0.66*t)
        if r>330: break
        a = t + arm*math.pi + random.uniform(-.14,.14); rr = r*random.uniform(.9,1.1)
        x,y = 450+rr*math.cos(a), 200+rr*.42*math.sin(a)
        stars += f'<circle cx="{f(x)}" cy="{f(y)}" r="{random.choice([.7,.9,1.1,1.5])}" fill="rgba(245,245,247,{random.uniform(.3,.85):.2f})"/>'
for k in range(160):   # faint disk haze between the arms
    a = random.uniform(0,2*math.pi); r = random.uniform(20,300)
    stars += f'<circle cx="{f(450+r*math.cos(a))}" cy="{f(200+r*.42*math.sin(a))}" r="{random.choice([.5,.7])}" fill="rgba(245,245,247,{random.uniform(.08,.22):.2f})"/>'
sun_a = 0.25+95*0.0165*2; sun_r=12*math.exp(0.66*sun_a); sx,sy = 450+sun_r*math.cos(sun_a), 200+sun_r*.42*math.sin(sun_a)
s3 = f'''
      <g class="zsc zsc3 near">
        {header(450,'the galaxy')}
        <ellipse cx="450" cy="200" rx="230" ry="92" fill="rgba(200,162,255,.025)"/><ellipse cx="450" cy="200" rx="70" ry="28" fill="rgba(251,191,36,.16)"/><ellipse cx="450" cy="200" rx="24" ry="10" fill="rgba(251,191,36,.55)"/>
        {stars}
        <circle cx="{f(sx)}" cy="{f(sy)}" r="3.5" fill="#fbbf24"/><circle class="pulse" cx="{f(sx)}" cy="{f(sy)}" r="6" fill="none" stroke="#fbbf24" stroke-width="1.5"/>
        <text class="lbl-sm" x="{f(sx-12)}" y="{f(sy-10)}" text-anchor="end" style="fill:#fbbf24;font-size:12px">the Sun — one of 100 billion</text>
        <text class="lbl-sm" x="450" y="372" text-anchor="middle" style="font-size:12.5px">elements — stars, gas, dust · interconnections — gravity again · purpose — still none of ours</text>
      </g>'''
# ---------- scene 4: the universe ----------
gal=''
for k in range(46):
    x,y = random.uniform(40,860), random.uniform(50,340); r=random.uniform(3,11); rot=random.uniform(0,180)
    gal += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r*random.uniform(.3,.7))}" transform="rotate({rot:.0f} {f(x)} {f(y)})" fill="rgba(245,245,247,{random.uniform(.15,.45):.2f})"/>'
s4 = f'''
      <g class="zsc zsc4 near">
        {header(450,'the universe')}
        {gal}
        <ellipse cx="450" cy="200" rx="12" ry="5" transform="rotate(-30 450 200)" fill="rgba(251,191,36,.6)"/><circle class="pulse" cx="450" cy="200" r="16" fill="none" stroke="#fbbf24" stroke-width="1.5"/>
        <text class="lbl-sm" x="466" y="188" style="fill:#fbbf24;font-size:12px">ours — one of two trillion</text>
        <text class="lbl-sm" x="450" y="372" text-anchor="middle" style="font-size:12.5px">systems inside systems, as far as anyone can see — and you can't see the forest for the trees from inside any of them</text>
      </g>'''
# ---------- scene 5: zoom back in — cells in a leaf · cells in a body · atoms in the Earth ----------
leafcells=''
for r_ in range(3):
    for c_ in range(4):
        x=100+c_*26+(13 if r_%2 else 0); y=92+r_*24
        leafcells+=f'<rect x="{x}" y="{y}" width="22" height="18" rx="6" fill="rgba(94,234,212,.14)" stroke="rgba(94,234,212,.7)" stroke-width="1.2"/><circle cx="{x+7}" cy="{y+9}" r="2.6" fill="#22c55e"/><circle cx="{x+15}" cy="{y+9}" r="2.6" fill="#22c55e"/>'
bodycells=''
for (cx,cy) in [(420,110),(462,98),(500,120),(438,150),(482,158),(520,150)]:
    bodycells+=f'<circle cx="{cx}" cy="{cy}" r="21" fill="rgba(122,162,255,.14)" stroke="rgba(157,185,255,.75)" stroke-width="1.3"/><circle cx="{cx}" cy="{cy}" r="7" fill="rgba(192,132,252,.85)"/><circle cx="{cx-9}" cy="{cy+8}" r="2" fill="rgba(245,245,247,.5)"/>'
def atom(cx,cy,sc,dur):
    out=f'<circle cx="{cx}" cy="{cy}" r="{6*sc:.1f}" fill="#fbbf24"/><circle cx="{cx+4*sc:.1f}" cy="{cy-3*sc:.1f}" r="{4*sc:.1f}" fill="#fb7185"/><circle cx="{cx-4*sc:.1f}" cy="{cy+3*sc:.1f}" r="{4*sc:.1f}" fill="#fb7185"/>'
    for k,rot in enumerate((0,60,120)):
        out+=f'<ellipse cx="{cx}" cy="{cy}" rx="{42*sc:.1f}" ry="{14*sc:.1f}" transform="rotate({rot} {cx} {cy})" fill="none" stroke="rgba(245,245,247,.35)"/>'
        out+=f'<circle r="{3.2*sc:.1f}" fill="#9dd6fc" transform="rotate({rot} {cx} {cy})"><animateMotion dur="{dur+k*.7:.1f}s" repeatCount="indefinite" path="M {cx+42*sc:.1f} {cy} a {42*sc:.1f} {14*sc:.1f} 0 1 0 {-84*sc:.1f} 0 a {42*sc:.1f} {14*sc:.1f} 0 1 0 {84*sc:.1f} 0"/></circle>'
    return out
atoms=atom(750,128,1.0,3.2)+atom(672,168,.5,2.4)+atom(830,172,.55,2.8)
s5 = f'''
      <g class="zsc zsc5 far">
        {header(150,'cells in a leaf')}{header(450,'cells in a body',.5)}{header(750,'atoms in the Earth',.6)}
        <path d="M 78 130 Q 150 40 226 130 Q 150 214 78 130 Z" fill="rgba(94,234,212,.06)" stroke="rgba(94,234,212,.5)" stroke-width="1.5"/>
        <path d="M 82 130 H 222" stroke="rgba(94,234,212,.35)" stroke-width="1.2"/>
        {leafcells}
        {bodycells}
        {atoms}
        {rows(150,'cells, chloroplasts, veins','sap, sugar, sunlight','turn light into food',0)}
        {rows(450,'cells, nuclei, membranes','signals, blood, oxygen','keep the body alive',0)}
        {rows(750,'nuclei, electrons','bonds, charge','none of ours — it just holds',0)}
        <text class="lbl-sm" x="450" y="334" text-anchor="middle" style="font-size:12.5px">zoom back in — the same three parts, all the way down</text>
      </g>'''
svg = f'''    <svg class="fig zoomfig" viewBox="0 0 900 400" aria-hidden="true" style="margin-top:.6vh;max-width:min(1040px,72vw)">
      <!-- generated by tools/gen-slide-zoom.py — six scenes: → zooms out four times, then back in -->{s0}{s1}{s2}{s3}{s4}{s5}
    </svg>
'''
p = pathlib.Path(__file__).resolve().parent.parent / 'presentation.html'; s = p.read_text()
i = s.index('4 · WHAT IS A SYSTEM ====='); j = s.index("5 · MEADOWS' TEST =====")
seg = s[i:j]; a = seg.index('    <svg class="fig zoomfig"'); b = seg.index('</svg>', a) + len('</svg>\n')
s = s[:i] + seg[:a] + svg + seg[b:] + s[j:]; p.write_text(s); print('zoom figure regenerated')
