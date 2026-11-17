---
name: onboard
description: Use when someone wants to set up the job search system, start onboarding, continue onboarding, or redo part of their setup (facts, sorting skills into categories, wants, voice, sources, settings, calibration). Creates their profile folder and tracker and tailors the system to them.
---

# Onboard

Sets the system up for one person. Everything personal ends up in their own
Google Drive, inside one system folder they choose or create and name
(decision 020): a profile folder made from `templates/profile/` (decision
006), an applications folder and a tracker sheet, either copied from the
published template or built by a one-time paste of the collector script
when no template link exists (decisions 004 and 019). Nothing personal is written to this plugin or to the repo.

Onboarding takes about an hour in total and can stop after any step. Each
step saves its work, and the next session picks up where the last one
stopped.

## Steps

| # | Step | Detail | Done when |
| --- | --- | --- | --- |
| 1 | Welcome and check tools | below | The user knows what will happen; Drive and Sheets are reachable (or test mode is chosen) |
| 2 | Storage | `references/step2-storage.md` (they choose an existing system folder or create a new one and name it; the tracker comes from the template link or a one-time paste) | System folder holds `Profile`, `Applications` and the tracker; settings has all three URLs |
| 3 | Career facts | `references/step3-facts.md` | Every role and most results in `facts.md` are `[confirmed]`; every skill sits under a category heading and `skills_preset` is set; Do not claim has at least one line; the user says the story bank is big enough for now |
| 4 | Wants and situation | `references/step4-wants.md` | `wants.md` sections, its Hard filters block, `profile.yaml` contact and situation, and the basics in `answers.md` are filled in |
| 5 | Voice | `references/step5-voice.md` | `voice.md` has samples, traits, format and a banned list the user has edited |
| 6 | Sources | `references/step6-sources.md` | `sources.yaml` has at least one enabled source; alert label set up if alerts are used |
| 7 | Settings | `references/step7-settings.md` | `settings.yaml` matches the user's plan and times |
| 8 | Calibrate | `references/step8-calibrate.md` | The user and the scorecard agree on most sample postings |
| 9 | Schedule | `references/step9-schedule.md` | The collector's daily trigger is installed and the nightly task is set up |

## Where to start

1. Look for existing system folders (`shared/profile.md`).
2. None: start at step 1.
3. Found: do the tool check from step 1 (skip the welcome), then ask in
   step 2 whether to use one or create a new one. If they create a new
   one, start at step 1's welcome and go through every step. If they use
   one, work out which steps are done from its files, using the "Done
   when" column. A file still holding template placeholders
   ("Your answer.", "Interest", `F-001 | Employer | Title`) is not done.
   Show the user a short checklist and continue at the first step not done,
   unless they ask for a specific step. If `facts.md` has skills but no
   category headings under Skills and tools, list "Sort your skills" on
   the checklist (`references/step3-facts.md`, one-time pass).

The user can ask to redo any step later ("redo my voice", "update my
wants"). Read the current file first and change only what they ask.

## Step 1: Welcome and check tools

Tell the user, in a few lines:

- What the system does: finds leads overnight, scores them against what
  they want, drafts a resume and cover letter for the best few, and has
  them checked. They decide and submit. It never submits anything.
- What onboarding needs: their resumes or career notes, about an hour
  (in pieces is fine), a Google account, and later a few minutes in their
  Gmail and the tracker sheet. Without a template link, that includes one
  copy and paste of the collector script into the sheet, which Claude walks
  them through.
- That nothing about them leaves their own Google Drive and this Claude
  account.

Then check that the Google Drive and Google Sheets connectors work (a quick
search in Drive). If they are not connected, suggest connecting them. If
the user cannot or will not connect Google, offer local test mode
(`shared/profile.md`): they can try the facts, wants and voice steps with
files here, but nothing will run overnight.

## How to run the interview steps

- **Ask how they want to respond.** The first time you have more than a
  couple of things for the user to confirm or answer (usually step 3's
  confirm), ask once, as a short choice:
  1. **One at a time.** One item, wait for the reply, next.
  2. **Small batches.** About five items in a numbered list, they reply to
     the batch.
  3. **All at once.** The whole list, numbered and grouped, they reply in
     one message.

  Use their choice for the rest of onboarding, in steps 3, 4 and 8. If they
  say "faster", "slower" or "one at a time", switch. If they have no
  preference, use small batches. In every mode show the exact text, accept
  the same replies (yes, a correction, delete, skip, not sure) and offer
  examples when a question is abstract. In the all-at-once mode they can
  reply by number ("1-8 yes, 9 fix: ..., 11 delete"); anything they do
  not mention stays unconfirmed, and you ask about those afterwards.
  Silence is never a yes.
- Show every link on a line of its own, plain, with nothing after it: no
  period, comma, bracket or quote, and not inside a sentence or a code
  span. Trailing punctuation gets copied into the link and breaks it (Drive
  folder IDs can end in a hyphen, so a stray period is easy to miss). Put
  the sentence before the link, never after it on the same line.
- When the user uses a name or term that is unknown to you or could mean
  more than one thing (an internal product, a team name, an acronym), ask
  what it is, in one line, for a reader who has never worked there. If it
  could appear in a resume or letter, save the answer as a term fact in
  Other facts (`Name is <what it is>`, decision 025). Do this in any step.
- Draft from what the user says and show the exact text before saving.
  The user edits; their words win. One exception: the "How to score me"
  lines in `wants.md` are saved without being shown line by line, because
  they restate the user's earlier answers (step 4 explains). Show them
  whenever the user asks.
- Save after each step (`shared/profile.md`, Writing a profile file), and
  say in one line what was saved.
- Never ask for age or date of birth (decision 015). If the user offers it,
  do not record it, and say the system does not use it.
- Never ask for API keys in the chat. Keys go into the tracker's menu (Job
  Search > Set API keys), which keeps them in the sheet's script
  properties.
- Do not put salary history, health, family or other personal details into
  any file unless the user asks for a specific line.

## Finishing

When all nine steps are done, tell the user in a few lines:

- What happens tonight (the collector runs at `schedule.collector_time`),
  and what to look at in the morning: the Leads tab, and the Next action
  column on every row that is not blank. It says what to do. Also today's
  Run Log row, where Errors names a night the nightly task did not run.
- How to use it day to day: paste a posting to get a fit read and a draft
  (apply skill), ask to find jobs (scout skill), say "I applied to..." to
  log it.
- If the overnight drafting task is available in this version, how it was
  set up; if not, that they run the apply skill on Shortlisted leads until
  it is.
