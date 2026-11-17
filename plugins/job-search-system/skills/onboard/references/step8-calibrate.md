# Step 8: Calibrate

Checks that the scorecard agrees with the user's own judgment (decision
011), and tunes the wording in `wants.md` until it mostly does.

## 1. Get sample postings

Ten to twenty real, recent postings in the user's field, a mix of good,
borderline and bad. Use what is available, in this order:

1. Leads already in the tracker (after the user runs Job Search > Run
   collector now).
2. A quick scout run (scout skill).
3. Postings the user pastes or links.

Full postings give better calibration than snippets. Get the full text for
at least half (apply skill, fit mode, steps 2 and 3, without writing to the
tracker).

## 2. The user judges first

Show each posting briefly (title, employer, location and mode, pay, three
or four lines on the work) and ask for one word: **yes**, **maybe** or
**no**, plus a few words on why if they like. Do not show your score yet;
it would anchor them. Show them at the pace the user chose (see "How to
run the interview steps" in `SKILL.md`): one posting, a small batch, or all
of them together.

## 3. Score

Score each posting on the scorecard (`shared/scorecard.md`) and map the
recommendation: Draft to yes, Consider to maybe, Skip to no.

## 4. Compare

Show a short table: posting, the user's call, your call, total, detail.
Agreement means the same call. Count agreements.

For each disagreement, find the dimension that caused it and why. Usually
it is one of:

- an interest or drain worded too broadly or too narrowly
- a missing drain or rule-out (the user said no for a reason not in
  `wants.md`)
- "How to score me" wording that does not match how they decide
- Evidence or Odds scoring a requirement differently than the user sees it

Propose the smallest change to `wants.md` that would fix it. Say it in plain
words first ("I will treat on-call as a bigger drain"), and show the exact
new line if they want to see it. Do not change `facts.md` here, and do not lower the evidence
rules to make a posting pass.

## 5. Adjust and rescore

Apply the changes the user approves, rescore, and compare again. Stop when
about four in five agree (for example 16 of 20), or after two rounds. If
agreement is still low, say so; the dimensions may need rework, which is a
matter for the system's maintainer (decision 011, "What would change it").

Also check the score bar: if most yes postings score just under
`drafting.score_bar`, offer to lower it by one, or the reverse.

## Save

Save `wants.md`. Add one comment line under "How to score me":
`<!-- Calibrated YYYY-MM-DD: N of M agreed. -->`
