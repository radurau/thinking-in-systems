# Restructure plan — continuity pass (from `notes_as_of_27august.pdf`)

Feedback from the office run: *the slides don't have continuity*. Root cause: slide 11
(the leverage ladder) names 12 rungs, but slides 1–10 only teach three of them
(stocks/flows, R, B). Examples also restart on every slide. This plan makes the ladder
the spine of Part 1 and threads two running examples through it.

**Assumptions** (change here if wrong):
- Slot ≈ 50 min talk + 10 min discussion (matches the notes panel). Notes total 32 min
  of script today, so ~5 new slides (+8 min) fit without trimming.
- Audience: mostly engineers at Tripletex/Visma → trap examples can be technical.
- Deck stays a single self-contained `presentation.html`; every text change needs an
  `i18n-ro.js` key and a notes-panel section. Push only when Radu says so.

Legend: `[ ]` todo · `[x]` done · `[~]` in progress · ✔ = check to run before ticking.

---

## Phase 0 — Mechanics audit (how the deck is wired)

- [x] Slides are `<section class="slide">`, numbered by DOM order; URL hash `#N` and
      `BroadcastChannel('tis-deck')` drive navigation → **inserting a slide renumbers
      everything after it** (notes-panel `id="nN"`, `Slide N ↗` links, `num` spans).
- [x] RO translation is keyed by normalised English innerHTML (`window.__RO__`);
      `__unmatched()` in the deck console lists untranslated strings. ✔ per slide.
- [x] Animation vocabulary: `.r` (rise), `.draw`, `.pop`, `.fadein`, `.pulse`, `.spin`,
      `--d` delay var; SVG figures use `class="fig"` + `.lbl-strong/.lbl-sm`.
- [x] Notes panel: one `<section class="note" id="nN">` per slide with `onscreen` /
      `say` / `cue` paragraphs and a `≈ N min` pill.
- [x] Write `tools/renumber-notes.py` — rewrites nN ids, jump links and num spans from
      DOM order so we can insert slides freely. ✔ 26 rows consistent after first insert.

## Phase 1 — Storyline (target order)

New = ★, changed = ✎, unchanged = ·. "Inherits" = what the slide carries from the one before.

| # | Slide | Rung(s) | Inherits → hands forward | Status |
|---|---|---|---|---|
| 1 | · The world is not a machine | — | hook | done |
| 2 | · One small book | — | book → "a new way of seeing" | done |
| 3 | · Iceberg: event / pattern / structure / mental model | — | → "so what *is* a system?" | done |
| 4 | ✎ Elements · Interconnections · Purpose — football → **basketball** → **play to lose** | — | iceberg's "structure" made concrete → stocks are the visible elements | [x] |
| 5 | ✎ Stocks & flows — bathtub; add "we see stocks, not flows; inflows, not outflows" | 10 | elements you can count → what changes them | [x] |
| 6 | ★ Numbers & buffers — the car lot: order size (a number), 10 days' cover (a buffer) | 12, 11 | bathtub → dealership stock; "buffers stabilise, but a too-big buffer is rigid" | [x] |
| 7 | ✎ Feedback — **bank account** leads, Yellowstone stays as story | — | stock → the system watches its own stock | [x] |
| 8 | · Reinforcing loops | 7 | feedback → more leads to more | done |
| 9 | ✎ Balancing loops — add "goal-seeking, corrects *both* directions; set the goal to cover the leak" | 8 | → what if both loops pull one stock? | [x] |
| 10 | ★ When loops compete — R + B on one stock → S-curve; **limits**: stock-limited (oil) vs flow-limited (fish) | — | → "and the delay makes it worse" | [x] |
| 11 | ✎ Delays — kicker says **Delays**; dealership's 3 delays (perceive / respond / deliver) → oscillation; "multiply by three" (Forrester / George Talaba) | 9 | dealership from #6 → oscillation; → who knows what, when? | [x] |
| 12 | ★ Structure — information flows, rules, self-organization (hallway meter, speed-camera vs police, teams that rewrite their rules) | 6, 5, 4 | delayed info → *where* info arrives; → who sets the goal? | [x] |
| 13 | ✎ Twelve leverage points — **payoff**: every rung has now been a slide; ladder lights up bottom-to-top | all | → the top three rungs deserve their own slides | [x] |
| 14 | ✎ Goals · Paradigms · Transcending — add **goals**: "purpose is deduced from behaviour, not rhetoric" | 3, 2, 1 | → the lens sits inside a bigger system | [x] |
| 15 | ✎ Systems inside systems — **zoom** tree → forest → planet → galaxy; hierarchy, stable intermediate forms, resilience | — | → why we still get surprised | [x] |
| 16 | ★ Why systems surprise us — nonlinear (fertiliser / advertising), no real boundaries, bounded rationality (fisherman with a mortgage) | — | → recurring structures = traps, no villains | [ ] optional |
| 17 | ✎ Eight traps — each with **book example + Tripletex/Visma example** (compute as commons, alarm-threshold drift, AI-micromaxing escalation, vibe-coding as burden-shift, budget rule-beating, effort-not-result boat) | — | → you already live in these | [x] |
| 18 | · You already live inside systems | — | | done |
| 19 | · Your overloaded team, mapped | — | | done |
| 20 | · What structure keeps producing this? | — | | done |
| 21 | ✎ Six moves — fold in 4–5 of the closing guidelines (get the beat, expose mental models, honour information, what's important > what's quantifiable, stay humble) | — | → AI is a new flow | [x] |
| 22–27 | · AI block (6) — add the **discipline-as-leverage** beat to "Aim it high" | — | | [x] |
| 28 | · Don't fight the system | — | | done |
| 29 | · Four questions | — | | done |

Deferred / cut unless time allows: rotating-cube "measured in one dimension", spiral for
success-to-the-successful, universe zoom as *opener* (lands better as #15).

## Phase 2 — Infrastructure

- [x] `tools/renumber-notes.py` (see Phase 0). ✔ dry-run diff showed only (stale) comment markers changing.
- [x] Ladder HUD: fixed 12-rung marker at the left edge on slides 5–12 (`data-hud`), rungs light
      cumulatively from each slide's `data-rungs`. ✔ hidden on 4 and 13+, print-hidden, numbers only (RO-safe).
- [x] Bridge lines: every Part-1 slide's `.oneliner` points **forward** to the next slide.
      ✔ read 3→16 in sequence; tweaked 3 (→ definition) and 5 (→ two knobs).

## Phase 3 — Structural slides (order of work = order of dependency)

- [x] #6 ★ Numbers & buffers (dealership intro — needed by #11) — HTML + RO + notes; fits 1600×900
- [x] #11 ✎ Delays (dealership 3 delays; rename kicker; swap chips for the three delays) — shower kept (AI slide calls back to it); notes rewritten with Forrester/Talaba ×3 + Christmas aside
- [x] #10 ★ When loops compete / limits — fishery R+B, S-curve vs overshoot, stock- vs flow-limited
- [x] #12 ★ Structure: information · rules · self-organization — three glass cards (hallway meter / who writes the rules / self-org); traps slide moved to after 'Systems inside systems' (#16)
- [x] #13 ✎ Ladder payoff — sub says 'you have now met every one of these'; all 12 rungs light fully, one per .22s; notes open with the recap
- [x] #14 ✎ add Goals rung — kicker 'The Three at the Top', sub + notes carry 'purpose is deduced from behaviour, not rhetoric' (no third panel: slide already dense)
- [x] Run renumber script; ✔ 28 sections in sync, notes-panel RO coverage complete (pill now carries data-ro)

## Phase 4 — Upgrades to existing slides

- [x] #4 football → basketball → play-to-lose — three `.step-item` acts on →: names swap, court + new passes, red passes into own basket; notes rewritten with cues
- [x] #5 stocks/flows extra lines — notes: 'we see stocks, not flows; the tap before the drain'
- [x] #7 bank-account feedback loop — leads the chips and the notes; Yellowstone kept as the optional story (Vogels callback)
- [x] #9 balancing: both-directions + goal-compensates-leak — sub, leak label on the chart, notes; one-liner bridges to 'never alone' (→ #10)
- [x] #15 zoom-out — NW labels (a cell · a tree · a forest · a planet · a galaxy) mirror the mental-model labels; 'bacteria, not elephants' chip; hierarchy + suboptimization paragraph in notes; title/figure shrunk so it no longer clips
- [x] #16 traps: 'Closer to home' line in every expanded trap (compute commons, alert drift, AI micro-maxing, headcount, vibe-coding, December budgets, effort-not-results boat); notes aside says read 2–3, not all
- [x] #20 six moves + closing guidelines — notes-only: Meadows' coda (get the beat · expose mental models · honour information · important > quantifiable · stay humble); slide already full
- [x] #26 "Aim it high": discipline-as-leverage beat — notes: comfort as an R loop, Liebig's law, 'choose the starving spot'

## Phase 5 — Optional

- [ ] #16 ★ Why systems surprise us (nonlinear · boundaries · bounded rationality) — **deferred**: notes already at 42 min; bounded rationality is covered by the traps' 'no villains' framing. Revisit only if the AI block is trimmed.

## Phase 6 — Every slide, every time (definition of done)

- [ ] Renders without clipping at 1600×900 **and** 1280×720 (slide 15's title clips today;
      at 720p slides 5 and 10 already overflow by ~57px — decide: tighten `.wrap` spacing
      globally under a `max-height` media query, or confirm the projector is 1080p)
- [x] `__unmatched()` returns only the pre-existing decorative letters/numbers; notes panel fully covered.
      `tools/prune-ro.py` removes keys no page uses any more (18 pruned on 27 Aug) — re-run after text edits.
- [x] Notes panel: 28 sections, jumps and numbers in sync (`renumber-notes.py --check`); live-highlight mechanism unchanged (`#nN` by broadcast)
- [~] Reduced-motion: new slides use `.fadein/.pop/.draw` end states and →-driven steps (no timed reveals) — spot-check on a reduce-motion Mac before the talk
- [ ] ⌘P print: one slide per page, HUD hidden (`#hud` has a print rule; slide 4/16 step states print as-is)
- [~] Notes total ≤ 42 min of script — **now exactly 42 min**; if the dry run overruns, trim the AI block first (6 slides / ~8 min)
- [ ] Commit per phase; **no push** until Radu says so

## Phase 7 — Review

- [ ] Dry run start-to-finish, timed
- [ ] Hand the storyline table (Phase 1) to the colleagues who gave the feedback
- [ ] Fix what they flag; then push
