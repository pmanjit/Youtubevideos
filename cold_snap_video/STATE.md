# STATE — cold_snap

## Current position
STATE 4 · style anchor built from the user's art reference and rendered in code — AWAITING ANCHOR + SCRIPT APPROVAL (STATE 3 spine not yet cut)

## Completed
- STATE 0 — repo discovery (repo was bare; this project sets the convention)
- STATE 1 Step A — core concept locked: 5-min second-person survival explainer, 16:9, new channel distinct from inkexplainer
- STATE 1 Step B — producer-selected on user delegation ("you chose"): Hook A2 + Thumbnail B1
- STATE 2 — full narration written to `script.md`; 943 words → 5:04 projected
- STATE 4 (early, on purpose) — user supplied the art reference mid-state; palette sampled, line weight measured, engine written, 3 anchors + frame 01 rendered

## Decisions
| # | Decision | Value |
|---|---|---|
| D1 | Slug | `cold_snap` |
| D2 | Runtime | 5 min YouTube, ~930 words |
| D3 | POV | Second-person |
| D4 | Style | **LOCKED** — flat stick-figure vector, sampled from the user reference (see continuity.md) |
| D9 | Rendering | deterministic code (`tools/stick_snap.py`), not an image model |
| D7 | Hook | A2 "Someone Is Already In Your Yard" → frame 01 |
| D8 | Thumbnail | B1 "DON'T OPEN IT" |
| D5 | Voice | `en-US-AndrewNeural` +10% |
| D6 | Aspect | 16:9 |

## Declared exceptions
| # | Date | What | Why | Fallback taken |
|---|---|---|---|---|
| E1 | 2026-10-30 | Image generation unavailable | provider returned `403 PERMISSION_DENIED — account flagged for suspicious activity` on 4/4 calls, including a blank-background control. Not moderation; no re-roll helps | built a deterministic vector engine instead — lower risk, no drift, no per-turn frame cap |
| E2 | 2026-10-30 | Frame 01 foreground hand removed | 4 re-rolls (contour rebuild each time); finger notches unreadable at 9 px line weight | shipped frame without the hand; hook reads through frost + figures |

## Moderation log
_none_

## Reject budget (per turn)
R = 2 re-rolls per frame batch; after 3 failed re-rolls on one frame → ship closest, log exception here.
