# cold_snap_video

Second-person survival explainer: the temperature drops, and the real threat is the people around you who are also out of everything.

| | |
|---|---|
| Runtime target | 5 min (~930 words) |
| POV | Second-person |
| Aspect | 16:9 |
| Voice | `en-US-AndrewNeural` @ +10% (Kaggle only) |
| Style | derived from user art reference |

## Pipeline
```
brief.md ──► script.md ──► visuals.csv ──► refs/ ──► frames/ ──► Kaggle
                            (word-reactive)  (anchors)  (beats)   (TTS+mux)
```

## Files
- `brief.md` — concept, positioning, locked defaults
- `script.md` — final narration (STATE 2)
- `visuals.csv` — the spine: one row per spoken micro-beat (STATE 3)
- `continuity.md` — style/subject invariants + anchor prompts (STATE 4)
- `frames/` — `beatNNmNN.png`, named to match `visuals.csv`
- `refs/` — approved style anchors
- `STATE.md` — state-machine ledger, exceptions, moderation log
- `metadata.json`, `youtube.txt` — publish artifacts
- `../run_cold_snap_kaggle.sh` — the only place audio exists

## Hard rule
No TTS, no voice audition, no audio mixing, no FFmpeg encode in this repo. Silent estimates only.
