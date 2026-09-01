# Screenshots · Devpost gallery

Capture from terminal (macOS: Cmd+Shift+4). Font: 16pt+ monospaced.

---

## Required 3 (minimum)

### 1 · Embarrassing case (`magnet demo`)

```bash
magnet demo
```

**Capture:** Block showing `naive verdict helped` vs `magnet verdict baseline` after 1 reading.

**Caption:** "MAGNET refuses to trend on one reading."

---

### 2 · Eval arms (`magnet eval`)

```bash
magnet eval
```

**Capture:** Table with naive / magnet / silent_null columns.

**Caption:** "We ship the baseline arm that embarrasses us."

---

### 3 · Strands loop (`magnet agent-run`)

```bash
magnet agent-run
```

**Capture:** `MODE: strands agent loop` + tool dispatch list + receipt footer.

**Caption:** "Real Strands Agents SDK — four tools, SQLite log."

---

## Optional 4th · Adoption timeline

```bash
magnet history
```

**Caption:** "Adoption log for your stack changes."

---

## Optional 5th · Bedrock (Oscar only)

```bash
magnet agent-run --model bedrock
```

Only if live run succeeds. Caption: "Amazon Bedrock model choosing tools."

---

## Architecture image

Export `docs/architecture.md` mermaid to PNG, or screenshot from GitHub rendered README.
