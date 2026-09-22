"""Grade an adoption's free-text prediction against the measured verdict.

Ported spirit of helicon MAGNET S3 (prediction record): every shortlisted
candidate makes a checkable claim; check it at the next reading. Cold start
is unmeasured — never a default. A held prediction is still correlation,
not attribution: MAGNET does not claim the change caused the delta.

Slice 25: when the prediction names a fraction (`rises by 1/5`), magnet
checks magnitude (+ population when claimed). Direction-only grading is the
naive arm — it invents held when the fraction is wrong.

Slice 26: when the prediction names a stay-at level (`must stay at 5/5`),
magnet checks latest value/pop. Flat-only grading invents held when the
level is wrong.

Slice 28: stay-at without `/pop` (`must stay at 5`), remain/hold/keep/
unchanged-at lexicon, and floor claims (`at least 4/5`). A parsed level
with unknown intent is treated as flat — never no-direction while a level
sits on the table.

Slice 32: recover/restore/regain/rebound are rise. DEMO-ONE-WORKFLOW's
prediction `pass rate recovers by 1` was `no-direction` while Δ +1 and
the claimed amount already parsed — the Devpost demo could not grade its
own restore step. Slice 31 papered over by rewriting the sidecar to
`rises by 1`. Open the prediction text, not the nearest synonym.

Slice 35: negation honesty — `won't fall` / `does not regress` / `should
not drop` are flat, NOT fall. Found by running the object: magnet graded
`won't fall` as fall, inventing held when the score dropped. Ceiling
claims (`at most 3/5`, dual of floor). Target-level (`falls to 2/5`,
`reaches 5/5`) grades latest — direction alone is not the object.

Slice 39: percent without `by` (`rises 20%`) and triples/Nx ratio vs prior.

Slice 40: word form `20 percent` / `per cent` / `pct` is percent-of-pop —
never absolute points (the `%` fix left the word form inventing held on
Δ=+20). `never falls` / `cannot fall` / `won't decrease` are flat — the
Slice 35 negation list missed never/cannot and the verb decrease.

Slice 43: negated *rise* was still rise — `doesn't rise` / `never rises` /
`won't improve` / `cannot improve` invented held on helped. Modal fall
negation missed shall/ought/may (`shall not fall` invented held on hurt).
Bare `no worse` / `no better` / `won't get worse` invented direction held.

Slice 44: trailing comparator percents — `20% higher` / `20% lower` /
`20% more` / `20% less` / `20% up` / `20% down` were unbound (pct=None) so
direction invented held on absolute Δ=+20 while true 20% of pop 5 is +1.

Slice 45: bare `up 1` / `down 1` left amount=None so direction invented held
on Δ=+20 while the claim said magnitude 1 (`up by 1` already graded).

Slice 46: bare signed `+1` / `-1` parsed amount but intent=unknown (word
boundary before `+` fails) → no-direction while a claimable magnitude sat
on the table. Sign owns rise/fall intent.

Slice 47: crash/collapse/soar/dive/plunge/spike `to N`; `from A to B` /
`A → B` transitions — destination is the target. Unbound left no-direction.

Slice 48: arrow glyphs `↑1` / `↓1` left intent=unknown and amount=None →
no-direction while a claimable magnitude sat on the table (↑1/5 parsed
amount via an old FRAC quirk but still no intent; ↓1/5 fully unbound).
Bare `perfect score` / `perfect` / `full score` left target=None →
no-direction; with population known, perfect means latest == pop.

Slice 49: `climbs 1` / `slips 1` left amount=None so direction invented
held on Δ=+20. `grows by 1` / `shrinks by 1` parsed amount but
intent=unknown → no-direction. `5 out of 5` / `score of 5/5` /
`full marks` / bare `100%` left unbound targets.

Slice 50: fat arrows `⬆1` / `⬇1` / `▲1` / `▼1` unbound like ↑/↓ were.
Word magnitudes `by one` / `one point` / `up one` / `rises by two` left
amount=None so direction invented held on Δ=+20. `all green` /
`all passing` / `passes all` unbound perfect-like.

Slice 51: `gains one` / `up a point` / `rises a point` / `gains 1` left
amount=None with rise intent → invents held on Δ=+20 (`gains by one` /
`up by a point` already graded). `loses one` / `plus 1` / `minus 1` /
`adds 1` / `subtracts 1` fully unbound. `regresses by one` amount on
table but intent unknown (`regress` missed `regresses`).

Slice 52: `100 percent` / `100 pct` unbound while `100%` grades.
`5 of 5` unbound while `5 out of 5` grades. `scores 5/5` / `still 5/5`
unbound. `stays green` / `still green` unbound perfect-like.
THE LIE: `remains green` was flat lexicon without perfect resolve →
invents held at latest=4. `zero failures` / `all tests pass` unbound.

Slice 53: emoji presentation `⬆️1` / `⬇️1` (U+2B06/U+2B07 + FE0F)
left amount=None while intent rose/fell → invents held on Δ=+20.
Double-struck `⇑1` / `⇧1` / triangle emoji `🔼1` unbound.
Word-number percents `twenty percent higher` / `improves by twenty
percent` left pct=None → invents held on absolute Δ=+20 while true
20% of pop 5 is +1.

Slice 54: word from→to `from three to four` / `goes from three to five`
/ `from one to zero` left target=None while digit `from 3 to 4` grades.

Slice 55: bare word `three to four` (no `from`) left target=None while
`from three to four` grades. Bare `twenty percent` / `20 percent` / `20%`
(no rise word) left pct=None; `by twenty percent` parsed pct but
intent=unknown → no-direction. Unsigned bare/by percent is a rise claim
— grade Δ vs pop·pct; never invent held on absolute Δ=+20.

Slice 56: bare digit `3 to 4` / `3/5 to 4/5` / `goes 3 to 4` left
target=None while `from 3 to 4` grades. Mixed `three to 4` / `3 to four`
/ `zero to 4` unbound. Destination is still the target.

Slice 57: decimal truncation lie — `2.5%` / `50.5%` matched bare `5%`
(invented pct=5); `rises by 1.5` matched `by 1` (invented amount=1).
Integer claims must refuse digits that sit inside a decimal; leave
unbound rather than invent a truncated figure.

Slice 58: ordinal from→to `3rd to 4th` / `third to fourth` left
target=None while digit/cardinal forms grade. `equals 4/5` /
`equal to 4/5` / `== 4/5` unbound while `exactly 4/5` grades.
THE LIE: `3rd/5 to 4th/5` invented raw=`5 to 4` (partial digit steal
from ordinal-slash garbage) — destination must consume the ordinal.

Slice 59: `same as 4/5` matched flat lexicon `same` with target=None
→ invents prediction-held at any latest. `is`/`was`/`reads`/`measures`/
`matches`/`identical to`/`lands on`/`finishes at`/`comes to`/
`settles on` unbound. Word ordinals `eleventh`/`twelfth` unbound
while digit `11th to 12th` grades.
"""
from __future__ import annotations

import re

from magnet.reporter import Verdict

# Arrow glyph families — Slice 48 thin ↑↓; Slice 50 fat ⬆⬇▲▼⇈⇊;
# Slice 53 double-struck ⇑⇓⇧⇩ + triangle emoji 🔼🔽.
# FE0F (emoji presentation) may follow black arrows — strip before digit claim.
_ARROW_UP = "↑⬆▲⇈⇑⇧🔼"
_ARROW_DOWN = "↓⬇▼⇊⇓⇩🔽"
_ARROW_ANY = _ARROW_UP + _ARROW_DOWN
_FE0F = "\ufe0f"

# Word → int for magnitude ("by one", "two points"). Never ranks by spelling beauty.
_WORD_AMOUNTS = {
    "a": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}

# Slice 53: word → percent ("twenty percent higher"). Distinct from magnitude
# words — twenty is not a point-delta on a 5-pop probe.
_WORD_PERCENTS = {
    "ten": 10,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
    "hundred": 100,
}

# Lexical intent only — never ranks by the prediction's wording beauty.
# improv(?:e|…) — bare `improv` failed word-boundary on "improves" (Slice 35).
_RISE = re.compile(
    r"\b("
    r"ris(?:e|es|ing)|up|improv(?:e|es|ed|ing|ement)?|increas(?:e|es|ed|ing)?|"
    r"higher|helped|gain|gains|jump|jumps|boost|boosts|\+\s*\d|coverage rises|"
    r"climb(?:s|ed|ing)?|"
    r"grow(?:s|ing|th)?|"
    r"add|adds|adding|"
    r"doubles?|twice|triples?|quadruples?|tenfold|"
    r"recover(?:s|ed|ing|y)?|restor(?:e|es|ed|ing)|regain(?:s|ed|ing)?|"
    r"rebound(?:s|ed|ing)?|"
    r"soar(?:s|ed|ing)?|spik(?:e|es|ed|ing)?|balloon(?:s|ed|ing)?|"
    r"better"
    r")\b",
    re.I,
)
_FALL = re.compile(
    r"\b(fall|falls|falling|drop|drops|dropping|hurt|decreas(?:e|es|ed|ing)?|"
    r"declin(?:e|es|ed|ing)?|worsen(?:s|ed|ing)?|slip(?:s|ped|ping)?|"
    r"halves?|half|"
    r"lower|down|regress(?:es|ed|ing)?|worse|"
    r"shrink(?:s|ing)?|"
    r"lose|loses|losing|subtract(?:s|ed|ing)?|"
    r"crash(?:es|ed|ing)?|collaps(?:e|es|ed|ing)?|dive(?:s|d|ing)?|"
    r"plung(?:e|es|ed|ing)?|"
    r"simplify|simplifies|simplifying|streamline|relax|remove|strip|undo|revert|weaken)\b",
    re.I,
)
# Negated fall/rise MUST win before _FALL/_RISE. THE LIE Slice 35 fixed:
# "won't fall" was fall → invents held when the score drops.
# Slice 40: "never falls" / "cannot fall" / "won't decrease" were still fall —
# inventing held on hurt. never/cannot/can't + decrease/worsen close the gap.
# Slice 43: negated rise (`doesn't rise` / `never rises` / `won't improve`)
# was still rise → inventing held on helped. shall/ought/may not fall still
# fall. Bare `no worse` / `no better` / `get worse` under negation.
_FALL_VERBS = (
    r"fall|falls|falling|drop|drops|dropping|regress|regresses|regressing|"
    r"decline|declines|declining|worsen|worsens|worsening|"
    r"slip|slips|slipping|hurt|hurts|decrease|decreases|decreasing|"
    r"get\s+worse|gets\s+worse|getting\s+worse"
)
_RISE_VERBS = (
    r"rise|rises|rising|improv(?:e|es|ed|ing|ement)?|"
    r"increas(?:e|es|ed|ing)?|gain|gains|boost|boosts|jump|jumps|"
    r"climb(?:s|ed|ing)?|get\s+better|gets\s+better|getting\s+better"
)
# Modals + never/cannot — contractions and "ought not to" included.
_NEG_MODAL = (
    r"(?:won'?t|will\s+not|must\s+not|should\s+not|shall\s+not|"
    r"ought\s+not(?:\s+to)?|may\s+not|does\s+not|do\s+not|did\s+not|"
    r"doesn'?t|don'?t|never|cannot|can'?t)"
)
_NEGATED_MOVE = re.compile(
    rf"(?:"
    rf"{_NEG_MODAL}\s+(?:{_FALL_VERBS})|"
    rf"{_NEG_MODAL}\s+(?:{_RISE_VERBS})|"
    rf"no\s+regression|"
    rf"no\s+decrease|"
    # Bare no-worse / no-better are flat (not fall/rise). "no worse than N"
    # and "no better than N" also match — floor/ceiling parsers still own the
    # bound; intent must not invent direction held beneath/above the bound.
    rf"no\s+worse|"
    rf"no\s+better|"
    rf"non[-\s]?regression|"
    rf"without\s+(?:falling|dropping|regressing|decreasing|worsening|slipping|"
    rf"rising|improving|increasing)|"
    rf"not\s+rise"
    rf")",
    re.I,
)
_FLAT = re.compile(
    r"\b(unchanged|no\s+change|same|stable|flat|"
    r"no\s+coverage\s+change|nothing\s+moves?|still\s+pass|"
    # Slice 52: green/perfect stay phrases move to _PERFECT_UNBOUND —
    # remain(s) green alone was flat without perfect resolve → invents held.
    r"stay(?:s|ing)?\s+at|must\s+stay|"
    r"remain(?:s|ing)?\s+at|hold(?:s|ing)?\s+at|keep(?:s|ing)?\s+at|"
    r"must\s+(?:remain|hold|keep)|"
    r"exactly|must\s+be\s+exactly|"
    # Slice 38: below/above-bound stay phrases — "no lower than" contains "lower"
    # (fall lexicon) but is a floor claim, not a fall.
    r"no\s+lower\s+than|no\s+less\s+than|never\s+(?:fall\s+)?below|"
    r"stay(?:s|ing)?\s+above|remain(?:s|ing)?\s+above|keep(?:s|ing)?\s+above"
    r")\b",
    re.I,
)

# Absolute stay-at level: "must stay at 190/190", "stay at 4/5", "stay at 5",
# "remain at 4/5", "hold at 190", "keep at 5/5", "unchanged at 5/5".
# Population is optional — value-only claims compare latest value alone.
_STAY_AT = re.compile(
    r"(?:must\s+)?"
    r"(?:stay(?:s|ing)?|remain(?:s|ing)?|hold(?:s|ing)?|keep(?:s|ing)?|unchanged)"
    r"\s+at\s+(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Floor claim: "at least 4/5", "no worse than 4/5". Held when latest >= value.
_FLOOR = re.compile(
    r"(?:at\s+least|no\s+worse\s+than)\s+(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Slice 38: below-bound compounds. THE LIE: "won't fall below 3/5" left floor=None
# so unchanged@latest=2 invented held. Held when latest >= value.
_FLOOR_BELOW = re.compile(
    r"(?:"
    r"(?:won'?t|will\s+not|does\s+not|doesn'?t|must\s+not|should\s+not)\s+"
    r"(?:fall|drop|regress|decline|go)\s+(?:below|under)|"
    r"never\s+(?:fall\s+)?below|"
    r"no\s+lower\s+than|"
    r"no\s+less\s+than|"
    r"(?:must\s+not|should\s+not)\s+(?:drop|fall)\s+under"
    r")\s+(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Strict above-bound: "stays above 3/5". Held when latest > value (not ≥).
_FLOOR_ABOVE = re.compile(
    r"(?:must\s+)?"
    r"(?:stay(?:s|ing)?|remain(?:s|ing)?|keep(?:s|ing)?)\s+above\s+"
    r"(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Ceiling claim (dual of floor): "at most 3/5", "no better than 3/5",
# "no more than 4/5", "capped at 4/5", "must not exceed 4/5", "caps at 4/5".
# Slice 57: "up to 4/5" — was rise lexicon (`up`) with no ceiling → invents
# held on any helped while the named ceiling sat unbound.
# Held when latest <= value.
_CEILING = re.compile(
    r"(?:at\s+most|no\s+better\s+than|no\s+more\s+than|capped\s+at|caps?\s+at|"
    r"must\s+not\s+exceed|up\s+to)\s+(\d+)(?:\s*/\s*(\d+))?",
    re.I,
)

# Target-level: "falls to 2/5", "reaches 5/5", "hits 5", "ends at 4/5",
# "lands at 4/5", "returns to 4/5", "climbs to 5/5", "improves to 4/5",
# "exactly 4/5", "must be exactly 4/5", "lands at exactly 4/5".
# Slice 41: "falls to zero" / "goes to zero" / "goes to 0" / "perfect 5/5".
# Slice 47: "crashes to 0" / "collapses to zero" / "soars to 5/5" /
# "dives to 1/5" / "plunges to 0" / "spikes to 5".
# Slice 49: "tops out at 5" / "maxes out at 5/5".
# Slice 58: "equals 4/5" / "equal to 4/5" / "== 4/5" / "must equal 4".
# Slice 59: "same as 4/5" / "is 4/5" / "reads 4/5" / "matches 4/5" /
# "lands on 4/5" / "finishes at 4/5" / "comes to 4/5" / "identical to 4/5".
# Direction alone is not the object — latest must match the named level.
# THE LIE: "falls to zero" left target=None → hurt@latest=1 invented held.
# THE LIE Slice 59: "same as 4/5" left target=None → flat invented held @3.
_TARGET = re.compile(
    r"(?:"
    r"(?:falls?|drops?|rises?|climbs?|improves?|goes?|"
    r"crash(?:es)?|collaps(?:e|es)|soar(?:s)?|dive(?:s)?|plung(?:e|es)|"
    r"spik(?:e|es)|balloon(?:s)?)\s+to|"
    r"down\s+to|"  # Slice 57: "down to 2" was fall with no target
    r"reaches?|hits?|"
    r"(?:ends?|lands?|settles?)\s+at|"
    r"(?:tops?|max(?:es)?)\s+out\s+at|"
    r"returns?\s+to|back\s+to|"
    r"(?:must\s+be\s+)?exactly|"
    # Slice 58: equals / equal to / == — unbound while exactly graded.
    r"(?:(?:must|should|shall)\s+)?equals?|"
    r"(?:(?:is|are|must\s+be|should\s+be)\s+)?equal\s+to|"
    r"==|"
    # Slice 59: same-as invent-held + level copulas / readouts.
    r"same\s+as|identical\s+to|matches|"
    r"(?:is|was|are|were)|"
    r"reads?(?:\s+as)?|measures?(?:\s+at)?|"
    r"lands?\s+on|settles?\s+on|"
    r"(?:finish(?:es)?|comes?(?:\s+out)?)\s+(?:at|to)|"
    r"(?:stands?|sits?)\s+at|clocks?\s+in\s+at|"
    r"perfect|full|max(?:imum)?"
    r")\s+(?:exactly\s+)?(?:zero|(\d+))(?:\s*/\s*(\d+))?",
    re.I,
)

# Slice 49: "5 out of 5" / "5 out of five" — target value/pop.
# Slice 52: bare "5 of 5" (without "out") was unbound.
_OUT_OF = re.compile(
    r"\b(\d+)\s+(?:out\s+)?of\s+(\d+)\b",
    re.I,
)

# Slice 49: "score of 5/5" / "score of 5" — target.
_SCORE_OF = re.compile(
    r"\bscore\s+of\s+(\d+)(?:\s*/\s*(\d+))?\b",
    re.I,
)

# Slice 52: "scores 5/5" / "gets 5/5" / "marks 5/5" / "still 5/5".
# THE LIE: unbound → no-direction while a named level sat on the table.
_SCORES_SLASH = re.compile(
    r"\b(?:scores?|gets?|marks?|still)\s+(\d+)\s*/\s*(\d+)\b",
    re.I,
)

# Ordinal digit suffix — Slice 58. Optional so bare `3 to 4` still grades.
# THE LIE: `3rd/5 to 4th/5` matched raw=`5 to 4` (stole pop digit + dest
# digit from `4th`) because ordinal suffix was not consumed.
_ORD_SFX = r"(?:st|nd|rd|th)?"

# Slice 47: transition claims — destination is the target.
# "from 3/5 to 4/5", "goes from 2 to 0", "3/5 → 4/5", "3→4".
# THE LIE: unbound → no-direction while a named end-state sat on the table.
# Slice 54: word forms "from three to four" / "from one to zero".
# Slice 56: bare digit `3 to 4` / `3/5 to 4/5` (from optional).
# Slice 58: ordinal digit `3rd to 4th` / `from 3rd/5 to 4th/5`.
_FROM_TO = re.compile(
    r"(?:"
    r"(?:(?:goes?|moves?|climbs?|falls?|drops?|rises?)\s+)?"
    r"(?:from\s+)?"
    rf"(?:zero|(\d+){_ORD_SFX})(?:\s*/\s*(?:zero|(\d+){_ORD_SFX}))?"
    rf"\s+to\s+(?:zero|(\d+){_ORD_SFX})(?:\s*/\s*(?:zero|(\d+){_ORD_SFX}))?"
    r"|"
    rf"(?:zero|(\d+){_ORD_SFX})(?:\s*/\s*(?:zero|(\d+){_ORD_SFX}))?"
    rf"\s*(?:→|->|➞)\s*(?:zero|(\d+){_ORD_SFX})(?:\s*/\s*(?:zero|(\d+){_ORD_SFX}))?"
    r")",
    re.I,
)
# Cardinal + ordinal word levels. Longer ordinals BEFORE their cardinal
# prefixes (`fourth` before `four`) so `fourth` is not stolen as `four`.
# Slice 58: `third to fourth` / `from first to second` were unbound.
# Slice 59: `eleventh` / `twelfth` unbound while digit `11th`/`12th` grade.
# Longer ordinals (`eleventh`) before `ten`/`tenth` so prefix steal fails.
_WORD_LEVEL_RE = (
    r"(?:zeroth|zero|first|one|second|two|third|three|fourth|four|"
    r"fifth|five|sixth|six|seventh|seven|eighth|eight|ninth|nine|"
    r"eleventh|eleven|twelfth|twelve|twentieth|twenty|tenth|ten)"
)
_WORD_LEVELS = {
    "zero": 0,
    "zeroth": 0,
    "one": 1,
    "first": 1,
    "two": 2,
    "second": 2,
    "three": 3,
    "third": 3,
    "four": 4,
    "fourth": 4,
    "five": 5,
    "fifth": 5,
    "six": 6,
    "sixth": 6,
    "seven": 7,
    "seventh": 7,
    "eight": 8,
    "eighth": 8,
    "nine": 9,
    "ninth": 9,
    "ten": 10,
    "tenth": 10,
    "eleven": 11,
    "eleventh": 11,
    "twelve": 12,
    "twelfth": 12,
    "twenty": 20,
    "twentieth": 20,
}


def _word_level_value(tok: str | None) -> int | None:
    """Map a digit or cardinal/ordinal word token to an int. None if unbound."""
    if tok is None:
        return None
    if tok.isdigit():
        return int(tok)
    return _WORD_LEVELS.get(tok.lower())


# Slice 54: `from three to four`. Slice 55: bare `three to four` (from optional).
# Slice 56: mixed word/digit `three to 4` / `3 to four` / `zero to 4`.
# Slice 58: ordinal words `third to fourth` / mixed `3rd` via digit path.
# `\b` stops `four` matching inside `fourth` when ordinals are absent.
_FROM_TO_WORDS = re.compile(
    rf"(?:"
    rf"(?:(?:goes?|moves?|climbs?|falls?|drops?|rises?)\s+)?"
    rf"(?:from\s+)?"
    rf"\b({_WORD_LEVEL_RE}|\d+)\b(?:\s*/\s*\b({_WORD_LEVEL_RE}|\d+)\b)?"
    rf"\s+to\s+\b({_WORD_LEVEL_RE}|\d+)\b(?:\s*/\s*\b({_WORD_LEVEL_RE}|\d+)\b)?"
    rf")",
    re.I,
)

# Slice 58/59: equals / same-as / is / reads with word/ordinal destination
# (`equals four` / `same as four` / `is four` / `reads as three`).
# Digit form stays on _TARGET.
_EQUALS_WORD = re.compile(
    rf"(?:"
    rf"(?:(?:must|should|shall)\s+)?equals?|"
    rf"(?:(?:is|are|must\s+be|should\s+be)\s+)?equal\s+to|"
    rf"==|"
    rf"same\s+as|identical\s+to|matches|"
    rf"(?:is|was|are|were)|"
    rf"reads?(?:\s+as)?|measures?(?:\s+at)?|"
    rf"lands?\s+on|settles?\s+on|"
    rf"(?:finish(?:es)?|comes?(?:\s+out)?)\s+(?:at|to)|"
    rf"(?:stands?|sits?)\s+at|clocks?\s+in\s+at"
    rf")\s+(?:exactly\s+)?\b({_WORD_LEVEL_RE})\b(?:\s*/\s*\b({_WORD_LEVEL_RE})\b)?",
    re.I,
)

# Percent unit: `%` or the words percent / per cent / pct.
# Slice 40: "improves by 20 percent" was absolute amount=20 — THE LIE.
# Note: do NOT put \b after `%` — `%` is non-word, so `\b` after it never
# matches before space/end (two non-word chars). Word forms keep \b.
_PCT_UNIT = r"(?:%|percent\b|per\s*cent\b|pct\b)"

# Percent claim: "improves by 20%", "rises by 50%", "+10%".
# Slice 39: also "rises 20%", "improves 20%", "up 50%", "20% improvement"
# (without `by` — was unbound; direction invented held on any rise).
# Slice 40: same patterns with the word "percent" / "per cent" / "pct".
# Slice 42: "50% better" / "50% worse" via better|worse in the trailing group.
# Slice 44: "20% higher" / "20% lower" / "20% more" / "20% less" / "20% up" /
# "20% down" — trailing comparator was unbound → direction invented held on
# absolute-sized Δ (+20) while true 20% of pop 5 is +1.
# Slice 53: word-number percents — `twenty percent higher` / `improves by
# twenty percent` left pct=None → invents held on absolute Δ.
# Integer token that refuses decimal fragments. THE LIE Slice 57:
# bare `(\d+)%` matched the `5` in `2.5%` → invented pct=5; `by (\d+)`
# matched the `1` in `by 1.5` → invented amount=1.
_INT = r"(?<![.\d])(\d+)(?!\.\d)"

_WORD_PCT_RE = (
    r"(?:ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)"
)
_CLAIM_PCT = re.compile(
    rf"(?:"
    rf"(?:by\s*|[+\-]\s*){_INT}\s*{_PCT_UNIT}"  # by 20% / +20 percent
    rf"|"
    rf"(?:by\s*|[+\-]\s*)({_WORD_PCT_RE})\s*{_PCT_UNIT}"  # by twenty percent
    rf"|"
    rf"(?:rises?|falls?|drops?|improves?|increases?|decreases?|climbs?|"
    rf"gains?|jumps?|boosts?|up|down)\s+{_INT}\s*{_PCT_UNIT}"
    rf"|"
    rf"(?:rises?|falls?|drops?|improves?|increases?|decreases?|climbs?|"
    rf"gains?|jumps?|boosts?|up|down)\s+({_WORD_PCT_RE})\s*{_PCT_UNIT}"
    rf"|"
    rf"{_INT}\s*{_PCT_UNIT}\s+(?:improvement|increase|decrease|rise|fall|drop|"
    rf"gain|loss|better|worse|higher|lower|more|less|up|down)"
    rf"|"
    rf"({_WORD_PCT_RE})\s*{_PCT_UNIT}\s+(?:improvement|increase|decrease|rise|"
    rf"fall|drop|gain|loss|better|worse|higher|lower|more|less|up|down)"
    # Slice 55: bare `20%` / `20 percent` / `twenty percent` (no rise word).
    # Must stay AFTER trailing-comparator alts so `20% higher` still binds.
    # `100%` / `100 percent` stay on _PERFECT_UNBOUND via claimed_percent guard.
    rf"|"
    rf"{_INT}\s*{_PCT_UNIT}"
    rf"|"
    rf"({_WORD_PCT_RE})\s*{_PCT_UNIT}"
    rf")",
    re.I,
)

# Ratio claim vs prior: doubles / halves / triples / quadrupples / Nx / N times.
_WORD_FACTORS = {
    "once": 1,
    "one": 1,
    "two": 2,
    "twice": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}
_RATIO = re.compile(
    r"\b(?:"
    r"doubles?|twice(?:\s+as\s+(?:many|high|good|much))?|"
    r"triples?|"
    r"quadruples?|"
    r"halves?|cuts?\s+in\s+half|"
    r"(\d+)\s*x|"
    r"(?:(\d+)|once|one|two|three|four|five|six|seven|eight|nine|ten)\s+times|"
    r"(?:(\d+)|two|three|four|five|six|seven|eight|nine|ten)fold|"
    r"tenfold"
    r")\b",
    re.I,
)

# Claimed magnitude: "rises by 1/5", "falls by 2/7", "+1/5", "by 1/5".
# Slice 48/50: arrow glyphs (thin + fat) own N/P.
_CLAIM_FRAC = re.compile(
    rf"(?:by\s*|[+\-]\s*|[{_ARROW_ANY}]{_FE0F}?\s*[+\-]?)\s*"
    rf"{_INT}\s*/\s*(\d+)",
    re.I,
)
# Claimed absolute delta without population: "rises by 1", "+1", "-2" (not a date).
# Negative lookahead refuses digits that are part of a percent (`20%` / `20 percent`).
# Slice 45: bare `up 1` / `down 1` (without `by`) — was unbound so direction
# invented held on Δ=+20 while the claim said +1.
# Slice 49: bare `climbs 1` / `slips 1` — same lie (intent set, amount=None).
# Slice 51: `gains 1` / `loses 1` / `adds 1` / `subtracts 1` / `plus 1` /
# `minus 1` — same lie (or fully unbound).
# Slice 57: `(?!\.\d)` refuses truncating `by 1.5` → amount=1.
_CLAIM_ABS = re.compile(
    rf"(?:by\s+|rises?\s+by\s+|falls?\s+by\s+|drops?\s+by\s+|"
    rf"climbs?\s+by\s+|improves?\s+by\s+|declines?\s+by\s+|worsens?\s+by\s+|"
    rf"slips?\s+by\s+|grows?\s+by\s+|shrinks?\s+by\s+|"
    rf"gains?\s+by\s+|loses?\s+by\s+|adds?\s+by\s+|subtracts?\s+by\s+|"
    rf"up\s+|down\s+|climbs?\s+|slips?\s+|"
    rf"gains?\s+|loses?\s+|adds?\s+|subtracts?\s+|"
    rf"plus\s+|minus\s+"
    rf")\s*{_INT}(?!\s*/)(?!\s*{_PCT_UNIT})",
    re.I,
)
# Slice 48/50/53: arrow glyphs `↑1` / `⬇1` / `▲1` / `⬆️1` — absolute magnitude.
# THE LIE Slice 53: FE0F between glyph and digit left amount=None → invents held.
_CLAIM_ARROW_ABS = re.compile(
    rf"[{_ARROW_ANY}]{_FE0F}?\s*[+\-]?\s*{_INT}(?!\s*/)(?!\s*{_PCT_UNIT})",
)
# Slice 50: word magnitudes — `by one` / `up one` / `rises by two` / `one point`.
# THE LIE: intent set, amount=None → direction invents held on Δ=+20.
# Slice 51: `gains one` / `loses one` / `plus one` / `up a point` (no `by`).
_WORD_AMOUNT_RE = (
    r"(?:one|two|three|four|five|six|seven|eight|nine|ten)"
)
_MOVE_VERBS = (
    r"up|down|rises?|falls?|drops?|climbs?|slips?|grows?|shrinks?|"
    r"improves?|declines?|worsens?|gains?|loses?|adds?|subtracts?|"
    r"regresses?"
)
_CLAIM_WORD_ABS = re.compile(
    rf"(?:"
    rf"by\s+a\s+point|"
    rf"by\s+{_WORD_AMOUNT_RE}(?:\s+points?)?|"
    rf"(?:{_MOVE_VERBS}|plus|minus)\s+a\s+point|"
    rf"(?:{_MOVE_VERBS}|plus|minus)\s+(?:by\s+)?{_WORD_AMOUNT_RE}"
    rf"(?:\s+points?)?|"
    rf"{_WORD_AMOUNT_RE}\s+points?"
    rf")\b",
    re.I,
)
_CLAIM_SIGNED = re.compile(
    # (?!\d) blocks backtracking into longer numbers (`-20%` must not match `-2`).
    # Slice 57: (?!\.\d) refuses truncating `+1.5` → +1.
    rf"(?<![/\d])([+\-])(\d+)(?!\d)(?!\.\d)(?!\s*/)(?!\s*{_PCT_UNIT})",
    re.I,
)

# Slice 48: unbound perfect / full / max score — no N/N on the table.
# Resolves at check time to latest == population. `perfect 5/5` stays on _TARGET.
# Slice 49: `full marks` / bare `100%` / `one hundred percent` — same resolve.
# Slice 50: `all green` / `all passing` / `passes all` — perfect-like.
# Slice 52: `100 percent` / `100 pct` (word form of bare 100%); stays/still/
# remains/back-to green; zero/no failures; all-tests/everything passes;
# flawless / clean sweep. THE LIE: `remains green` was flat without resolve.
_PERFECT_UNBOUND = re.compile(
    r"(?:"
    r"\b(?:(?:a|the)\s+)?(?:perfect|full|max(?:imum)?)\s+score\b|"
    r"\bfull\s+marks\b|"
    r"\ball\s+(?:green|passing|pass(?:es)?)\b|"
    r"\bpasses\s+all\b|"
    r"\bscore(?:s|d)?\s+(?:a\s+)?perfect\b|"
    r"\b(?:reaches?|gets?|achieves?|hits?)\s+(?:a\s+)?perfect(?:\s+score)?\b|"
    r"\bperfect\b(?!\s*(?:zero|\d))|"
    r"(?<![/\d])100\s*%|"
    r"(?<![/\d])100\s+(?:percent|per\s*cent|pct)\b|"
    r"\bone\s+hundred\s+percent\b|"
    r"\b(?:stay(?:s|ing)?|still|remain(?:s|ing)?|back\s+to)\s+green\b|"
    r"\b(?:zero|no)\s+failures?\b|"
    r"\bnothing\s+fails\b|"
    r"\ball\s+tests?\s+pass(?:es|ing)?\b|"
    r"\beverything\s+passes\b|"
    r"\bpasses\s+everything\b|"
    r"\bflawless\b|"
    r"\bclean\s+sweep\b"
    r")",
    re.I,
)


def prediction_intent(prediction: str) -> str:
    """rise | fall | flat | unknown — derived from the prediction text itself.

    A parsed stay-at / floor / ceiling level with no rise/fall signal is flat:
    naming a required bound is itself a stay claim (Slice 28/35 — never
    no-direction while a bound sits on the table).

    Negated moves (`won't fall`, `doesn't rise`, `shall not fall`) are flat —
    checked before fall/rise lexicon.
    """
    text = prediction or ""
    # Negation and flat first: "won't fall" contains fall but means flat.
    if _NEGATED_MOVE.search(text) or _FLAT.search(text):
        return "flat"
    # Slice 57: "up to N" is a ceiling, not rise — `\bup\b` would steal rise.
    if re.search(r"\bup\s+to\b", text, re.I):
        return "flat"
    if _RISE.search(text) and not _FALL.search(text):
        return "rise"
    if _FALL.search(text) and not _RISE.search(text):
        return "fall"
    if _RISE.search(text) and _FALL.search(text):
        return "unknown"
    # Percent owns `+20%` / `-20%` before signed-absolute intent (Slice 46 —
    # signed backtracking used to steal `-2` from `-20%`).
    if claimed_percent(text)["percent"] is not None and re.search(
        rf"(?<![/\d])\+\s*\d+\s*{_PCT_UNIT}", text
    ):
        return "rise"
    if claimed_percent(text)["percent"] is not None and re.search(
        rf"(?<![/\d])\-\s*\d+\s*{_PCT_UNIT}", text
    ):
        return "fall"
    # Slice 46: bare signed deltas (`+1` / `-1` / `pass rate +1`). `_RISE`
    # puts `\+\s*\d` inside `\b(...)` so the leading boundary fails at string
    # start or after space — amount parsed, intent unknown → no-direction.
    # THE LIE: a claimable magnitude left ungraded. Sign owns intent here.
    signed = _CLAIM_SIGNED.search(text)
    if signed is not None:
        return "rise" if signed.group(1) == "+" else "fall"
    # Slice 51: word plus/minus (`plus 1` / `minus one`) — not in rise/fall
    # lexicon (would collide with "plus or minus" noise), but when a magnitude
    # sits next to them they own direction like signed +/−.
    if re.search(rf"\bplus\s+(?:a\s+point|{_WORD_AMOUNT_RE}|\d+)\b", text, re.I):
        return "rise"
    if re.search(rf"\bminus\s+(?:a\s+point|{_WORD_AMOUNT_RE}|\d+)\b", text, re.I):
        return "fall"
    # Slice 48/50: arrow glyphs are not word characters — lexicon `\b` misses them.
    # THE LIE: `↑1` / `⬆1` amount unbound + intent unknown → no-direction.
    if any(ch in text for ch in _ARROW_UP):
        return "rise"
    if any(ch in text for ch in _ARROW_DOWN):
        return "fall"
    # Level / floor / ceiling on the table ⇒ stay intent even if lexicon missed.
    if (
        claimed_level(text)["value"] is not None
        or claimed_floor(text)["value"] is not None
        or claimed_ceiling(text)["value"] is not None
    ):
        return "flat"
    # Target-only (`reaches 5/5` / `exactly 4/5` / unbound `perfect score`)
    # with no rise/fall word — flat so check_prediction grades the target.
    tgt = claimed_target(text)
    if tgt["value"] is not None or tgt.get("perfect"):
        return "flat"
    # Slice 44: `20% more` / `20% less` have no rise/fall lexicon word — bind
    # intent from the trailing comparator so percent grading can fire.
    # Slice 55: bare / by unsigned percent (`twenty percent` / `20%` /
    # `by 20%`) is a rise claim — pct on the table must not stay no-direction.
    # Signed word (`+twenty percent` / `-twenty percent`) owns rise/fall.
    if claimed_percent(text)["percent"] is not None:
        if re.search(
            rf"(?:\d+|{_WORD_PCT_RE})\s*{_PCT_UNIT}\s+(?:higher|more|up)\b",
            text,
            re.I,
        ):
            return "rise"
        if re.search(
            rf"(?:\d+|{_WORD_PCT_RE})\s*{_PCT_UNIT}\s+(?:lower|less|down)\b",
            text,
            re.I,
        ):
            return "fall"
        if re.search(
            rf"(?<![/\d])\+\s*(?:{_WORD_PCT_RE})\s*{_PCT_UNIT}", text, re.I
        ):
            return "rise"
        if re.search(
            rf"(?<![/\d])\-\s*(?:{_WORD_PCT_RE})\s*{_PCT_UNIT}", text, re.I
        ):
            return "fall"
        return "rise"
    # Triples / Nx without rise word still checkable as rise (factor ≥ 2).
    ratio = claimed_ratio(text)
    if ratio.get("factor") is not None and ratio["factor"] >= 2:
        return "rise"
    return "unknown"


def claimed_level(prediction: str) -> dict:
    """Parse stay-at absolute value (+ optional pop). Not a delta — a required latest."""
    text = prediction or ""
    m = _STAY_AT.search(text)
    if not m:
        return {"value": None, "population": None, "raw": None}
    pop = m.group(2)
    return {
        "value": int(m.group(1)),
        "population": int(pop) if pop is not None else None,
        "raw": m.group(0).strip(),
    }


def claimed_floor(prediction: str) -> dict:
    """Parse floor claim value (+ optional pop).

    Classic: `at least 4/5` — held when latest >= value.
    Slice 38 below-bound: `won't fall below 3/5`, `never below 4/5`,
    `no lower than 3/5` — same ≥ semantics (THE LIE was leaving these unbound).
    Slice 38 above-bound: `stays above 3/5` — exclusive; held when latest > value.
    """
    text = prediction or ""
    # Stay-at owns "stay at N" — floor is a different object.
    if claimed_level(text)["value"] is not None:
        return {"value": None, "population": None, "raw": None, "exclusive": False}
    m = _FLOOR_ABOVE.search(text)
    if m:
        pop = m.group(2)
        return {
            "value": int(m.group(1)),
            "population": int(pop) if pop is not None else None,
            "raw": m.group(0).strip(),
            "exclusive": True,
        }
    m = _FLOOR_BELOW.search(text) or _FLOOR.search(text)
    if not m:
        return {"value": None, "population": None, "raw": None, "exclusive": False}
    pop = m.group(2)
    return {
        "value": int(m.group(1)),
        "population": int(pop) if pop is not None else None,
        "raw": m.group(0).strip(),
        "exclusive": False,
    }


def claimed_ceiling(prediction: str) -> dict:
    """Parse ceiling claim value (+ optional pop). Held when latest <= value.

    Dual of floor (Slice 35). Stay-at / floor own their phrases first.
    """
    text = prediction or ""
    if claimed_level(text)["value"] is not None:
        return {"value": None, "population": None, "raw": None}
    if claimed_floor(text)["value"] is not None:
        return {"value": None, "population": None, "raw": None}
    m = _CEILING.search(text)
    if not m:
        return {"value": None, "population": None, "raw": None}
    pop = m.group(2)
    return {
        "value": int(m.group(1)),
        "population": int(pop) if pop is not None else None,
        "raw": m.group(0).strip(),
    }


def claimed_target(prediction: str) -> dict:
    """Parse target-level (`falls to 2/5`, `reaches 5`). Held when latest == value.

    Stay-at owns `stay at N`. Floor/ceiling own their phrases. Target is the
    directed end-state — direction alone invents held when latest ≠ target.

    Slice 41: `zero` ≡ 0; `goes to` / `perfect` / `full` / `max` open targets.
    THE LIE: `falls to zero` left target=None so hurt@latest=1 invented held.

    Slice 47: crash/collapse/soar/dive/plunge/spike verbs; `from A to B` /
    `A → B` transitions — destination is the target.

    Slice 54: word `from three to four`. Slice 55: bare `three to four`
    (no `from`) — destination is still the target.

    Slice 58: ordinal digit `3rd to 4th` / word `third to fourth` /
    `equals 4/5` / `equal to four` / `== 4/5`. THE LIE: `3rd/5 to 4th/5`
    invented raw=`5 to 4` by stealing digits around ordinal suffixes.

    Slice 59: `same as 4/5` / `is 4/5` / `reads 4/5` / `matches 4/5` /
    `lands on 4/5` / `finishes at 4/5` / `comes to 4/5` / `identical to`.
    THE LIE: `same as 4/5` was flat with no target → invents held @ any latest.

    Slice 48: unbound `perfect score` / bare `perfect` / `full score` —
    `perfect: True` resolves at check time to latest == population.
    """
    text = prediction or ""
    empty = {
        "value": None,
        "population": None,
        "raw": None,
        "perfect": False,
    }
    if claimed_level(text)["value"] is not None:
        return empty
    if claimed_floor(text)["value"] is not None:
        return empty
    if claimed_ceiling(text)["value"] is not None:
        return empty
    m = _TARGET.search(text)
    if m:
        raw = m.group(0).strip()
        if re.search(r"\bzero\b", raw, re.I):
            value = 0
        elif m.group(1) is not None:
            value = int(m.group(1))
        else:
            return empty
        pop = m.group(2)
        return {
            "value": value,
            "population": int(pop) if pop is not None else None,
            "raw": raw,
            "perfect": False,
        }
    # Slice 58: equals four / equal to fourth / == three
    m = _EQUALS_WORD.search(text)
    if m:
        value = _word_level_value(m.group(1))
        if value is None:
            return empty
        pop = _word_level_value(m.group(2)) if m.group(2) is not None else None
        return {
            "value": int(value),
            "population": int(pop) if pop is not None else None,
            "raw": m.group(0).strip(),
            "perfect": False,
        }
    m = _FROM_TO.search(text)
    if m:
        raw = m.group(0).strip()
        # from-form groups 1..4; arrow-form groups 5..8. Destination is groups 3/4 or 7/8.
        # `zero` leaves the digit group None — detect via the raw destination text.
        # Slice 56: bare `3 to 4` (no from) still uses groups 1..4.
        # Slice 58: ordinal suffixes consumed so `3rd/5 to 4th/5` is not `5 to 4`.
        if m.group(1) is not None or m.group(3) is not None or re.search(
            r"\bfrom\b", raw, re.I
        ) or re.search(r"\bto\b", raw, re.I):
            to_chunk = re.split(r"\bto\b", raw, maxsplit=1, flags=re.I)[-1].strip()
            if re.match(r"zero\b", to_chunk, re.I):
                value = 0
                pop = None
            else:
                value = int(m.group(3)) if m.group(3) is not None else None
                pop = m.group(4)
        else:
            # arrow form
            arrow_split = re.split(r"→|->|➞", raw, maxsplit=1)
            to_chunk = arrow_split[-1].strip() if len(arrow_split) > 1 else ""
            if re.match(r"zero\b", to_chunk, re.I):
                value = 0
                pop = None
            else:
                value = int(m.group(7)) if m.group(7) is not None else None
                pop = m.group(8)
        if value is None:
            return empty
        # Destination pop may be in to_chunk as N/P (ordinal suffix stripped by group).
        pop_m = re.search(rf"/\s*(\d+){_ORD_SFX}\b", to_chunk, re.I)
        if pop_m:
            pop = pop_m.group(1)
        return {
            "value": value,
            "population": int(pop) if pop is not None else None,
            "raw": raw,
            "perfect": False,
        }
    # Slice 54/55/56/58: word/ordinal/mixed from→to (from optional) — destination is the target.
    m = _FROM_TO_WORDS.search(text)
    if m:
        raw = m.group(0).strip()
        value = _word_level_value(m.group(3))
        if value is None:
            return empty
        pop = _word_level_value(m.group(4)) if m.group(4) is not None else None
        return {
            "value": int(value),
            "population": int(pop) if pop is not None else None,
            "raw": raw,
            "perfect": False,
        }
    # Slice 49: "5 out of 5" / "score of 5/5"
    m = _OUT_OF.search(text)
    if m:
        return {
            "value": int(m.group(1)),
            "population": int(m.group(2)),
            "raw": m.group(0).strip(),
            "perfect": False,
        }
    m = _SCORE_OF.search(text)
    if m:
        pop = m.group(2)
        return {
            "value": int(m.group(1)),
            "population": int(pop) if pop is not None else None,
            "raw": m.group(0).strip(),
            "perfect": False,
        }
    # Slice 52: scores/gets/marks/still N/N
    m = _SCORES_SLASH.search(text)
    if m:
        return {
            "value": int(m.group(1)),
            "population": int(m.group(2)),
            "raw": m.group(0).strip(),
            "perfect": False,
        }
    # Slice 48/49/52: unbound perfect / full marks / 100% / green / failures
    m = _PERFECT_UNBOUND.search(text)
    if m:
        return {
            "value": None,
            "population": None,
            "raw": m.group(0).strip(),
            "perfect": True,
        }
    return empty


def claimed_ratio(prediction: str) -> dict:
    """Parse doubles/halves/triples/quadruples/Nx/N-times claim vs prior.

    Grades against prior = latest − Δ.
    Slice 37: direction-only invents held on any rise when the claim said doubles.
    Slice 39: triples / 3x / 2x / tenfold.
    Slice 41: quadrupples / `5 times` / `fivefold` (digit `4x` already worked).
    """
    text = prediction or ""
    m = _RATIO.search(text)
    if not m:
        return {"kind": None, "factor": None, "raw": None}
    raw = m.group(0).strip()
    low = raw.lower()
    compact = low.replace(" ", "")
    if "half" in compact or "halves" in compact:
        return {"kind": "half", "factor": 0.5, "raw": raw}
    if "quadruple" in compact:
        return {"kind": "quadruple", "factor": 4, "raw": raw}
    if "triple" in compact:
        return {"kind": "triple", "factor": 3, "raw": raw}
    if compact == "tenfold":
        return {"kind": "tenfold", "factor": 10, "raw": raw}
    # Nx digit group
    if m.group(1) is not None:
        factor = int(m.group(1))
        kind = "double" if factor == 2 else ("triple" if factor == 3 else f"{factor}x")
        return {"kind": kind, "factor": factor, "raw": raw}
    # N times / word times
    if m.group(2) is not None:
        factor = int(m.group(2))
    elif "times" in low:
        word = low.split("times")[0].strip()
        factor = _WORD_FACTORS.get(word)
        if factor is None:
            return {"kind": None, "factor": None, "raw": None}
    # Nfold / wordfold
    elif m.group(3) is not None:
        factor = int(m.group(3))
    elif "fold" in compact:
        word = compact.replace("fold", "")
        factor = _WORD_FACTORS.get(word)
        if factor is None:
            return {"kind": None, "factor": None, "raw": None}
    elif "twice" in compact or compact.startswith("double"):
        return {"kind": "double", "factor": 2, "raw": raw}
    else:
        return {"kind": "double", "factor": 2, "raw": raw}
    kind = (
        "double"
        if factor == 2
        else ("triple" if factor == 3 else ("quadruple" if factor == 4 else f"{factor}x"))
    )
    return {"kind": kind, "factor": factor, "raw": raw}


def claimed_percent(prediction: str) -> dict:
    """Parse percent claim (`improves by 20%`, `rises 20%`). NOT absolute points.

    Slice 36: stripping `%` and treating 20 as absolute Δ was the lie.
    Slice 39: `rises 20%` / `improves 20%` / `20% improvement` without `by`
    were unbound — direction invented held on any rise.
    Slice 40: `improves by 20 percent` / `20 percent improvement` — the word
    form was still absolute amount=20 (held on Δ=+20, missed on true 20%).
    Slice 55: bare `20%` / `20 percent` / `twenty percent` (no rise word).
    Perfect unbound (`100%` / `100 percent`) stays on claimed_target — never
    steal those as percent-of-pop.
    """
    text = prediction or ""
    if claimed_level(text)["value"] is not None:
        return {"percent": None, "raw": None}
    if claimed_floor(text)["value"] is not None:
        return {"percent": None, "raw": None}
    if claimed_ceiling(text)["value"] is not None:
        return {"percent": None, "raw": None}
    tgt = claimed_target(text)
    if tgt["value"] is not None or tgt.get("perfect"):
        return {"percent": None, "raw": None}
    m = _CLAIM_PCT.search(text)
    if not m:
        return {"percent": None, "raw": None}
    raw_tok = next(g for g in m.groups() if g is not None)
    if raw_tok.isdigit():
        pct = int(raw_tok)
    else:
        pct = _WORD_PERCENTS.get(raw_tok.lower())
        if pct is None:
            return {"percent": None, "raw": None}
    return {"percent": int(pct), "raw": m.group(0).strip()}


def claimed_magnitude(prediction: str) -> dict:
    """Parse claimed delta amount + optional population from the prediction text.

    Returns:
      amount      int | None  — absolute size of the claimed move (never signed here)
      population  int | None  — denominator when written as N/P
      raw         str | None  — matched substring for the receipt
    Sign is applied later from intent (rise → +, fall → −, flat → 0).
    Stay-at / floor / ceiling / target / percent are NOT absolute deltas —
    their parsers own those. Percent must not fall through to amount=N.
    """
    text = prediction or ""
    if claimed_level(text)["value"] is not None:
        return {"amount": None, "population": None, "raw": None}
    if claimed_floor(text)["value"] is not None:
        return {"amount": None, "population": None, "raw": None}
    if claimed_ceiling(text)["value"] is not None:
        return {"amount": None, "population": None, "raw": None}
    if claimed_target(text)["value"] is not None:
        return {"amount": None, "population": None, "raw": None}
    # Percent owns `by 20%` — never absolute 20 (Slice 36).
    if claimed_percent(text)["percent"] is not None:
        return {"amount": None, "population": None, "raw": None}
    m = _CLAIM_FRAC.search(text)
    if m:
        return {
            "amount": int(m.group(1)),
            "population": int(m.group(2)),
            "raw": m.group(0).strip(),
        }
    # Slice 48/50: arrow absolute before signed — `↑1` / `⬆1` is not `+1`.
    m = _CLAIM_ARROW_ABS.search(text)
    if m:
        return {
            "amount": int(m.group(1)),
            "population": None,
            "raw": m.group(0).strip(),
        }
    m = _CLAIM_ABS.search(text)
    if m:
        return {"amount": int(m.group(1)), "population": None, "raw": m.group(0).strip()}
    # Slice 50: word magnitudes after digit forms — `by one` / `up one` / `one point`.
    # Slice 51: `gains one` / `up a point` / `plus one`.
    m = _CLAIM_WORD_ABS.search(text)
    if m:
        raw = m.group(0).strip()
        if re.search(r"\ba\s+point\b", raw, re.I):
            return {"amount": 1, "population": None, "raw": raw}
        words = re.findall(
            r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\b",
            raw,
            re.I,
        )
        if words:
            amount = _WORD_AMOUNTS[words[-1].lower()]
            return {"amount": int(amount), "population": None, "raw": raw}
    m = _CLAIM_SIGNED.search(text)
    if m:
        return {"amount": int(m.group(2)), "population": None, "raw": m.group(0).strip()}
    return {"amount": None, "population": None, "raw": None}


def expected_delta_from_claim(intent: str, claim: dict) -> int | None:
    """Signed expected delta from intent + claimed amount. None if no amount."""
    amount = claim.get("amount")
    if amount is None:
        return None
    if intent == "rise":
        return int(amount)
    if intent == "fall":
        return -int(amount)
    if intent == "flat":
        return 0
    return None


def expected_delta_from_percent(intent: str, percent: int | None, population: int | None) -> int | None:
    """Signed expected Δ from percent-of-population. None if pop or pct missing."""
    if percent is None or population is None or population <= 0:
        return None
    amount = int(round(int(population) * int(percent) / 100.0))
    if intent == "rise":
        return amount
    if intent == "fall":
        return -amount
    if intent == "flat":
        return 0
    return None


def _bound_fields(prediction: str) -> dict:
    """Shared claimed_* bundle for naive + magnet checks."""
    return {
        "claimed": claimed_magnitude(prediction),
        "claimed_level": claimed_level(prediction),
        "claimed_floor": claimed_floor(prediction),
        "claimed_ceiling": claimed_ceiling(prediction),
        "claimed_target": claimed_target(prediction),
        "claimed_percent": claimed_percent(prediction),
        "claimed_ratio": claimed_ratio(prediction),
    }


def naive_direction_check(
    prediction: str,
    label: Verdict | str,
    delta: int | None = None,
    *,
    population: int | None = None,
    latest_value: int | None = None,
) -> dict:
    """Two-hour naive arm: grade direction only, ignore claimed fraction/level/bounds.

    This is what magnet did through Slice 24 — it invents prediction-held when
    the claim says rises by 2/5 and the measured delta is +1, or stay-at 5/5
    while latest is 4/5, or stay-at 5 while latest is 4, or at most 3/5 while
    latest is 4, or falls to 2/5 while latest is 3.

    Pre-Slice-35 naive also treated `won't fall` as fall (the lie). Naive here
    still uses the *fixed* intent parser so the arm is "direction only", not
    "broken lexicon" — the embarrassment is ignoring ceiling/target/magnitude.
    """
    intent = prediction_intent(prediction)
    bounds = _bound_fields(prediction)
    if label == "baseline":
        return {
            "outcome": "unmeasured",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "grade": "direction-only",
            **bounds,
            "note": "unmeasured — need two readings before a prediction can be checked",
        }
    if intent == "unknown":
        return {
            "outcome": "no-direction",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "grade": "direction-only",
            **bounds,
            "note": "prediction has no rise/fall/flat signal MAGNET can grade",
        }
    expected = {"rise": "helped", "fall": "hurt", "flat": "unchanged"}[intent]
    held = label == expected
    outcome = "prediction-held" if held else "prediction-missed"
    return {
        "outcome": outcome,
        "intent": intent,
        "verdict": label,
        "delta": delta,
        "population": population,
        "latest_value": latest_value,
        "expected": expected,
        "grade": "direction-only",
        **bounds,
        "note": (
            f"{outcome}: intent={intent} expected={expected} got={label}"
            " — direction only; claimed fraction/level/floor/ceiling/target ignored"
        ),
    }


def _pop_ok(claimed_pop: int | None, measured_pop: int | None) -> bool:
    if claimed_pop is None or measured_pop is None:
        return True
    return int(claimed_pop) == int(measured_pop)


def check_prediction(
    prediction: str,
    label: Verdict | str,
    delta: int | None = None,
    *,
    population: int | None = None,
    latest_value: int | None = None,
) -> dict:
    """Compare prediction intent (+ magnitude/level/floor/ceiling/target when claimed).

    Returns:
      outcome   prediction-held | prediction-missed | unmeasured | no-direction
      intent    rise | fall | flat | unknown
      grade     direction | direction+magnitude | direction+level | floor | ceiling | target
      claimed   {amount, population, raw}
      claimed_level / claimed_floor / claimed_ceiling / claimed_target
      note      always reminds that held ≠ attributed
    """
    intent = prediction_intent(prediction)
    bounds = _bound_fields(prediction)
    claim = bounds["claimed"]
    level = bounds["claimed_level"]
    floor = bounds["claimed_floor"]
    ceiling = bounds["claimed_ceiling"]
    target = bounds["claimed_target"]
    percent = bounds["claimed_percent"]
    ratio = bounds["claimed_ratio"]

    if label == "baseline":
        return {
            "outcome": "unmeasured",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "grade": "direction",
            **bounds,
            "note": "unmeasured — need two readings before a prediction can be checked",
        }

    # Slice 48: unbound `perfect score` resolves to latest == population.
    # Without population, refuse to invent a target (same honesty as percent).
    if target.get("perfect") and target.get("value") is None:
        if population is not None:
            target = {
                **target,
                "value": int(population),
                "population": int(population),
            }
            bounds = {**bounds, "claimed_target": target}
        else:
            return {
                "outcome": "no-direction",
                "intent": intent,
                "verdict": label,
                "delta": delta,
                "population": population,
                "latest_value": latest_value,
                "grade": "target",
                **bounds,
                "note": (
                    "no-direction: perfect score needs population to resolve "
                    "target — will not invent a perfect level"
                ),
            }

    if intent == "unknown":
        return {
            "outcome": "no-direction",
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "grade": "direction",
            **bounds,
            "note": "prediction has no rise/fall/flat signal MAGNET can grade",
        }

    # Floor claims: held when latest >= claimed floor (or > if exclusive).
    # Pop match when both present. Slice 38: below-bound compounds open here.
    if floor.get("value") is not None:
        exclusive = bool(floor.get("exclusive"))
        if latest_value is None:
            floor_ok = False
        else:
            if exclusive:
                floor_ok = int(latest_value) > int(floor["value"])
            else:
                floor_ok = int(latest_value) >= int(floor["value"])
            floor_ok = floor_ok and _pop_ok(floor.get("population"), population)
        outcome = "prediction-held" if floor_ok else "prediction-missed"
        op = ">" if exclusive else "≥"
        why = (
            f"floor claimed {op}{floor['value']}/{floor.get('population')} "
            f"got {latest_value}/{population}"
        )
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": None,
            "expected_delta": None,
            "grade": "floor",
            **bounds,
            "floor_ok": floor_ok,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

    # Ceiling claims (Slice 35): held when latest <= claimed ceiling.
    if ceiling.get("value") is not None:
        if latest_value is None:
            ceiling_ok = False
        else:
            ceiling_ok = int(latest_value) <= int(ceiling["value"])
            ceiling_ok = ceiling_ok and _pop_ok(ceiling.get("population"), population)
        outcome = "prediction-held" if ceiling_ok else "prediction-missed"
        why = (
            f"ceiling claimed ≤{ceiling['value']}/{ceiling.get('population')} "
            f"got {latest_value}/{population}"
        )
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": None,
            "expected_delta": None,
            "grade": "ceiling",
            **bounds,
            "ceiling_ok": ceiling_ok,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

    # Percent-of-pop (Slice 36): expected Δ = round(pop · pct / 100).
    # Never treat `20%` as absolute 20 — that invented held on Δ=+20 / pop 5.
    if percent.get("percent") is not None:
        expected = {"rise": "helped", "fall": "hurt", "flat": "unchanged"}[intent]
        direction_ok = label == expected
        expected_delta = expected_delta_from_percent(
            intent, percent.get("percent"), population
        )
        if expected_delta is None:
            # No population → cannot convert % to Δ; refuse absolute invent.
            return {
                "outcome": "prediction-missed" if not direction_ok else "no-direction",
                "intent": intent,
                "verdict": label,
                "delta": delta,
                "population": population,
                "latest_value": latest_value,
                "expected": expected,
                "expected_delta": None,
                "grade": "percent",
                **bounds,
                "note": (
                    f"{'prediction-missed' if not direction_ok else 'no-direction'}: "
                    f"intent={intent} percent={percent['percent']}% needs population "
                    "to grade — will not invent absolute points"
                ),
            }
        magnitude_ok = delta is not None and int(delta) == int(expected_delta)
        held = direction_ok and magnitude_ok
        outcome = "prediction-held" if held else "prediction-missed"
        if not direction_ok:
            why = f"direction expected={expected} got={label}"
        elif not magnitude_ok:
            why = (
                f"percent {percent['percent']}% of pop {population} → "
                f"claimed Δ {expected_delta:+d} got Δ "
                f"{delta if delta is not None else '—'}"
            )
        else:
            why = f"direction+percent ({percent['percent']}% of {population})"
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": expected,
            "expected_delta": expected_delta,
            "grade": "direction+percent",
            **bounds,
            "magnitude_ok": magnitude_ok,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

    # Doubles/halves/triples/Nx vs prior (Slice 37/39): prior = latest − Δ.
    # Direction alone invents held on a non-matching ratio rise.
    if ratio.get("kind") is not None:
        expected = {"rise": "helped", "fall": "hurt", "flat": "unchanged"}[intent]
        direction_ok = label == expected
        if latest_value is None or delta is None:
            return {
                "outcome": "unmeasured",
                "intent": intent,
                "verdict": label,
                "delta": delta,
                "population": population,
                "latest_value": latest_value,
                "expected": expected,
                "expected_delta": None,
                "grade": "ratio",
                **bounds,
                "note": "unmeasured — ratio claims need latest and Δ to recover prior",
            }
        prior = int(latest_value) - int(delta)
        factor = ratio.get("factor")
        if factor == 0.5 or ratio["kind"] == "half":
            if prior < 0:
                ratio_ok = False
                expected_delta = None
            else:
                expected_latest = prior // 2
                expected_delta = expected_latest - prior
                ratio_ok = (
                    int(latest_value) == expected_latest
                    and int(delta) == expected_delta
                )
        else:
            # double / triple / Nx / tenfold — factor ≥ 2
            f = int(factor) if factor is not None else 2
            if prior <= 0:
                ratio_ok = False
                expected_delta = None
            else:
                expected_latest = f * prior
                expected_delta = expected_latest - prior
                ratio_ok = (
                    int(latest_value) == expected_latest
                    and int(delta) == expected_delta
                )
        held = direction_ok and ratio_ok
        outcome = "prediction-held" if held else "prediction-missed"
        if not direction_ok:
            why = f"direction expected={expected} got={label}"
        elif not ratio_ok:
            why = (
                f"ratio={ratio['kind']} factor={factor} prior={prior} "
                f"latest={latest_value} Δ={delta} "
                f"expected_delta={expected_delta if expected_delta is not None else '—'}"
            )
        else:
            why = f"direction+ratio ({ratio['kind']} prior={prior})"
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": expected,
            "expected_delta": expected_delta,
            "grade": "direction+ratio",
            **bounds,
            "prior": prior,
            "ratio_ok": ratio_ok,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

    expected = {"rise": "helped", "fall": "hurt", "flat": "unchanged"}[intent]
    direction_ok = label == expected
    expected_delta = expected_delta_from_claim(intent, claim)

    level_ok = True
    if level.get("value") is not None:
        if latest_value is None:
            level_ok = False
        else:
            level_ok = int(latest_value) == int(level["value"])
            level_ok = level_ok and _pop_ok(level.get("population"), population)

    target_ok = True
    if target.get("value") is not None:
        if latest_value is None:
            target_ok = False
        else:
            target_ok = int(latest_value) == int(target["value"])
            target_ok = target_ok and _pop_ok(target.get("population"), population)

    # Target-level without stay-at / magnitude (Slice 35).
    # Direction + target when intent is rise/fall; target alone when flat
    # (`reaches 5/5` with no rise word → intent flat via claimed_target).
    if target.get("value") is not None and expected_delta is None and level.get("value") is None:
        if intent == "flat":
            held = target_ok
            grade = "target"
        else:
            held = direction_ok and target_ok
            grade = "direction+target"
        outcome = "prediction-held" if held else "prediction-missed"
        if intent != "flat" and not direction_ok:
            why = f"direction expected={expected} got={label}"
        elif not target_ok:
            why = (
                f"target claimed {target['value']}/{target.get('population')} "
                f"got {latest_value}/{population}"
            )
        else:
            why = "direction+target" if intent != "flat" else "target"
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": expected if intent != "flat" else None,
            "expected_delta": None,
            "grade": grade,
            **bounds,
            "target_ok": target_ok,
            "direction_ok": direction_ok if intent != "flat" else None,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

    if expected_delta is None and level.get("value") is None:
        held = direction_ok
        outcome = "prediction-held" if held else "prediction-missed"
        note = (
            f"{outcome}: intent={intent} expected={expected} got={label}"
            " — correlation, not attribution"
        )
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": expected,
            "expected_delta": None,
            "grade": "direction",
            **bounds,
            "note": note,
        }

    if expected_delta is not None:
        magnitude_ok = delta is not None and int(delta) == int(expected_delta)
        pop_ok = _pop_ok(claim.get("population"), population)
        held = direction_ok and magnitude_ok and pop_ok and level_ok and target_ok
        outcome = "prediction-held" if held else "prediction-missed"
        if not direction_ok:
            why = f"direction expected={expected} got={label}"
        elif not magnitude_ok:
            why = (
                f"magnitude claimed Δ {expected_delta:+d} "
                f"got Δ {delta if delta is not None else '—'}"
            )
        elif not pop_ok:
            why = (
                f"population mismatch claimed={claim['population']} "
                f"measured={population}"
            )
        elif not level_ok:
            why = (
                f"level claimed {level['value']}/{level.get('population')} "
                f"got {latest_value}/{population}"
            )
        elif not target_ok:
            why = (
                f"target claimed {target['value']}/{target.get('population')} "
                f"got {latest_value}/{population}"
            )
        else:
            why = "direction+magnitude"
        grade = "direction+magnitude"
        if level.get("value") is not None:
            grade += "+level"
        if target.get("value") is not None:
            grade += "+target"
        return {
            "outcome": outcome,
            "intent": intent,
            "verdict": label,
            "delta": delta,
            "population": population,
            "latest_value": latest_value,
            "expected": expected,
            "expected_delta": expected_delta,
            "grade": grade,
            **bounds,
            "magnitude_ok": magnitude_ok,
            "population_ok": pop_ok,
            "level_ok": level_ok,
            "target_ok": target_ok,
            "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
        }

    # Stay-at level only (no delta claim).
    held = direction_ok and level_ok
    outcome = "prediction-held" if held else "prediction-missed"
    if not direction_ok:
        why = f"direction expected={expected} got={label}"
    elif not level_ok:
        why = (
            f"level claimed {level['value']}/{level.get('population')} "
            f"got {latest_value}/{population}"
        )
    else:
        why = "direction+level"
    return {
        "outcome": outcome,
        "intent": intent,
        "verdict": label,
        "delta": delta,
        "population": population,
        "latest_value": latest_value,
        "expected": expected,
        "expected_delta": None,
        "grade": "direction+level",
        **bounds,
        "level_ok": level_ok,
        "note": f"{outcome}: intent={intent} {why} — correlation, not attribution",
    }


def render_prediction_check(check: dict) -> str:
    lines = [
        "MAGNET prediction check",
        "",
        f"  intent     {check['intent']}",
        f"  outcome    {check['outcome']}",
        f"  grade      {check.get('grade', 'direction')}",
    ]
    if check.get("expected"):
        lines.append(
            f"  expected   {check['expected']}  got={check['verdict']}"
        )
    claim = check.get("claimed") or {}
    if claim.get("amount") is not None:
        pop = claim.get("population")
        claim_txt = (
            f"{claim['amount']}/{pop}" if pop is not None else str(claim["amount"])
        )
        exp_d = check.get("expected_delta")
        got_d = check.get("delta")
        lines.append(
            f"  claimed Δ  {claim_txt}  expected_delta="
            f"{exp_d if exp_d is not None else '—'}  "
            f"measured_delta={got_d if got_d is not None else '—'}"
        )
        if check.get("population") is not None and pop is not None:
            lines.append(
                f"  claimed pop {pop}  measured_pop={check['population']}"
            )
    level = check.get("claimed_level") or {}
    if level.get("value") is not None:
        pop = level.get("population")
        lvl_txt = f"{level['value']}/{pop}" if pop is not None else str(level["value"])
        lines.append(
            f"  claimed lvl {lvl_txt}  "
            f"latest={check.get('latest_value')}/{check.get('population')}"
        )
    floor = check.get("claimed_floor") or {}
    if floor.get("value") is not None:
        pop = floor.get("population")
        fl_txt = f"{floor['value']}/{pop}" if pop is not None else str(floor["value"])
        lines.append(
            f"  claimed floor ≥{fl_txt}  "
            f"latest={check.get('latest_value')}/{check.get('population')}"
        )
    ceiling = check.get("claimed_ceiling") or {}
    if ceiling.get("value") is not None:
        pop = ceiling.get("population")
        ce_txt = (
            f"{ceiling['value']}/{pop}" if pop is not None else str(ceiling["value"])
        )
        lines.append(
            f"  claimed ceiling ≤{ce_txt}  "
            f"latest={check.get('latest_value')}/{check.get('population')}"
        )
    target = check.get("claimed_target") or {}
    if target.get("value") is not None:
        pop = target.get("population")
        tg_txt = f"{target['value']}/{pop}" if pop is not None else str(target["value"])
        lines.append(
            f"  claimed target {tg_txt}  "
            f"latest={check.get('latest_value')}/{check.get('population')}"
        )
    pct = check.get("claimed_percent") or {}
    if pct.get("percent") is not None:
        lines.append(
            f"  claimed %   {pct['percent']}%  "
            f"expected_delta={check.get('expected_delta') if check.get('expected_delta') is not None else '—'}  "
            f"measured_delta={check.get('delta') if check.get('delta') is not None else '—'}  "
            f"pop={check.get('population')}"
        )
    lines.append(f"  note       {check['note']}")
    return "\n".join(lines)
