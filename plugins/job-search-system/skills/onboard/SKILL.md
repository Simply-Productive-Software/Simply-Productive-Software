---
name: onboard
description: Use when someone wants to set up the job search system, start onboarding, continue onboarding, or redo part of their setup (facts, sorting skills into categories, wants, voice, output settings). Creates their Drive folders and tracker sheet and builds their profile.
---

# Onboard

Sets the system up for one person. Everything personal ends up in their own
Google Drive, inside one system folder they choose or create and name
(decision 020): a profile folder made from `templates/profile/` (decision
006), an applications folder and a tracker sheet that onboarding builds from
scratch with the Drive and Sheets connectors (decisions 028 and 032). Nothing
personal is written to this plugin or to the repo.

Onboarding takes about an hour in total and can stop after any step. Each
step saves its work, and the next session picks up where the last one
stopped.

## Steps

| # | Step | Detail | Done when |
| --- | --- | --- | --- |
| 1 | Welcome and check tools | below | The user knows what will happen; Drive and Sheets are reachable |
| 2 | Storage | `references/step2-storage.md` (they choose an existing system folder or create a new one and name it; the tracker sheet is built here) | System folder holds `Profile`, `Applications` and the tracker; settings has all three links; the tracker's Config tab has the schema version and the profile folder ID |
| 3 | Career facts | `references/step3-facts.md` | Every role and most results in `facts.md` are `[confirmed]`; every skill sits under a category heading and `skills_preset` is set; Do not claim has at least one line; the user says the story bank is big enough for now |
| 4 | Wants and situation | `references/step4-wants.md` | `profile.yaml` contact and situation, the basics in `answers.md`, and the Interests and Level sections of `wants.md` are filled in. The other `wants.md` sections are optional and can stay as the template |
| 5 | Voice | `references/step5-voice.md` | `voice.md` has samples, traits, format and a banned list the user has edited |
| 6 | Output | `references/step6-settings.md` | `settings.yaml` has the file formats the user wants |

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

- What the system does: builds their profile from their own career history,
  then, when they give it a job they have chosen, drafts a tailored resume
  and cover letter from facts they have confirmed, has the draft checked, and
  saves it to their Drive. A tracker sheet keeps a row for each job and what
  happened to it. They edit and submit. It never submits anything. It does
  not decide which jobs they should apply for.
- What onboarding needs: their resumes or career notes, about an hour
  (in pieces is fine), and a Google account with the Drive and Sheets
  connectors turned on. Setup creates the folders and the tracker sheet for
  them.
- That nothing about them leaves their own Google Drive and this Claude
  account.
- The terms, in plain words. It is a beta, provided as is, with no
  warranty. The drafts are written by AI and can be wrong or incomplete, so
  they must read and check every resume, cover letter and answer before they
  use it, and they are responsible for the facts they confirm and for what
  they send. It does not guarantee interviews, offers or any result. They use
  it at their own risk and accept all risks of using it. It is for their own
  job search only, and the license says what they may and may not do with the
  plugin.

Ask the user to say they understand and accept this before you go on. If they
do not, stop and create nothing.

Then check that the Google Drive and Google Sheets connectors work (a quick
search in Drive). If either is not connected, say which one, ask the user to
turn it on, and stop. Onboarding does not go on without them. When they come
back, start again at step 1.

Local test mode (`shared/profile.md`) is for tests and demos. Use it only
when the user says to use a local profile.

## How to run the interview steps

- **Ask how they want to respond.** The first time you have more than a
  couple of things for the user to confirm or answer (usually step 3's
  confirm), ask once, as a short choice:
  1. **One at a time.** One item, wait for the reply, next.
  2. **Small batches.** About five items in a numbered list, they reply to
     the batch.
  3. **All at once.** The whole list, numbered and grouped, they reply in
     one message.

  Use their choice for the rest of onboarding, in steps 3 and 4. If they
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
  The user edits; their words win.
- Save after each step (`shared/profile.md`, Writing a profile file), and
  say in one line what was saved.
- Never ask for age or date of birth (decision 015). If the user offers it,
  do not record it, and say the system does not use it.
- Never ask for passwords or API keys in the chat.
- Do not put salary history, health, family or other personal details into
  any file unless the user asks for a specific line.

## Finishing

When all six steps are done, tell the user in a few lines:

- Where everything is: the system folder, with Profile, Applications and the
  tracker sheet.
- How to use it: paste a job posting or a link and ask for a resume and cover
  letter (apply skill). Read and edit the drafts, apply on the employer's
  site, then say "I applied to..." so it is logged. They can also say they
  skipped, parked or found a job closed.
- Ask them to check anything in the profile files they want changed, and that
  they can ask to redo any step.
