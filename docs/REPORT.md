# Build report · Slice 15–16 · 2026-09-03

## SHIPPED

### Slice 15
- `fixtures/stack-cursor/` — sanitized live Cursor skills (independent stack)
- `magnet replicate` — author vs independent bakeoff; independent LOST shipped
- Author must-beat-naive RED control
- `magnet coverage-delta` — attributed / coincident / nothing-moved
- Frontmatter body fallback (canvas empty YAML → not `metadata:`)

### Slice 16
- **`magnet recover`** — opens the independent-stack loss at its object
- Diagnosis re-derived: 18 noise in top-20 fill only `{planning, writing, design}`
- Temp-covers those caps → magnet **0.625** recall, **0 noise**, beats naive_stars
- Sample noise printed ("plan a wedding", "draft a listing", "colour palette")
- Judge-demo + stranger-pass wired
- 112 pytest tests (re-derived)

## VERIFIED

| Claim | Command |
|-------|---------|
| Tests green | `python3 -m pytest -q` → 112 passed |
| check_docs | `magnet check-docs` → 11 PASS |
| Replicate loss | `magnet replicate` → independent LOST 0.25 < 0.375 |
| Recover win | `magnet recover` → thin LOST, covered 0.625 / 0 noise / WIN |
| Coverage-delta | pdb on stack-cursor → 2/12→3/12 attributed |
| Judge demo | `bash scripts/judge-demo.sh` → JUDGE DEMO OK |

## WRONG

- **Independent thin stack still loses** — that is intentional; recover shows the fix.
- **Synonym primary still 0/3** even after recover (claims tier 3/3).
- **Planted flood still authored** — S4 partial.
- **Bedrock cloud BLOCKED**.
- **PR / merge to main is Oscar's click** — branch `cursor/stack-magnet-night-5e60`.
- **Cover skills in recover are synthetic** — they prove the diagnosis; they are not claimed as Oscar's real stack.
