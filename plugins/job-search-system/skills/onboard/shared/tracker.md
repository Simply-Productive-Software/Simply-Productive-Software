# Reading and writing the tracker

The tracker layout is defined in `shared/tracker-schema.yaml` (copied from
`templates/tracker-schema.yaml`). The overnight collector writes to the same
sheet, so follow these rules exactly.

## Rules

- Find columns by header name. Read row 1 of a tab first and map names to
  column letters. Never assume a column position, even though the order is
  fixed.
- Never add, remove, rename or reorder columns or tabs, and never turn a tab
  into a Google Sheets table. If a column you need is missing, stop and
  tell the user to run Job Search > Check configuration in the sheet.
- Do not touch the hidden Seen and Config tabs, except to read Config's
  `profile_folder_id` and to read Seen's Dedupe key column.
- Dates are text in `YYYY-MM-DD`. Write them as plain strings.
- Every time you change Status, also set Status date to today.
- Write only the columns your step owns (`set_by` in the schema). Leave the
  user's columns (Notes, Follow-up date, Channel and so on) alone unless the
  user asked you to fill them.
- Keep cell text short. Why: one or two sentences. Flags: semicolon
  separated, each under about 12 words. Review notes: under about 60 words.

## Finding a lead's row

Match on Lead ID when you have one. Otherwise compute the dedupe key and
match on Dedupe key. The same job can arrive from several sources; if more
than one row matches, update all of them and say so.

## Dedupe key

`normalized employer | normalized title | normalized city`, computed the
same way as the collector (`collector/src/Util.gs`):

- normalize text: lowercase, `&` becomes ` and `, every run of characters
  other than `a-z` and `0-9` becomes one space, trim.
- employer: normalize, drop a leading `the`, then drop trailing legal
  suffixes (`inc llc ltd corp corporation co company lp llp plc pllc pc`)
  while more than one word is left.
- city: the part of the location before the first comma, after removing
  anything in parentheses, normalized. If the result is a generic location
  that names no place, the city is empty. The list is `GENERIC_LOCATIONS` in
  `checks/lib.py` (remote, united states, us, usa, anywhere, nationwide,
  worldwide and the usual combinations such as "remote united states"). So
  "Remote", "United States" and "US" give the same key for the same employer
  and title. A real place such as "Spokane" or "Remote - Florida" does not.

Keys stored before this rule (for example `acme|engineering manager|remote`)
are rewritten once by the collector: it runs at the start of the next
collector run, or by hand from Job Search > Update dedupe keys (one time).
Until that has run on a tracker, do not match on keys you computed yourself.

Use the check scripts' `dedupe_key` command when it is available
(`checks/README.md`) rather than computing it by hand.

## New rows

A lead found by the scout skill or pasted by the user gets a new Leads row:

- Lead ID: `L-<YYYYMMDD>-<NNN>` for today. Read the Lead ID column, find the
  highest `NNN` already used today, and add 1. Pad to 3 digits.
- Date found: today. Source: `scout` or `pasted`. Source ref: blank for
  pasted leads; for scout leads, the ATS reference if known (for example
  `greenhouse:<board>:<id>`).
- Link: the URL the posting came from. Apply link: the employer's own
  careers page for the job, if found.
- Dedupe key: computed as above.
- Status: `New` if not scored yet. If the step that adds it also scores
  it: `Shortlisted` for Draft (waiting for a draft), `Needs you` for
  Consider, `Skipped` for Skip.

Before adding, check the Dedupe key against both Leads and Seen. If the key
is in Leads, update that row instead. If it is only in Seen with an outcome
starting `filtered`, tell the user it was filtered overnight and why, and
add it only if they still want it.

## Status changes

Use only the statuses in the schema. Who sets what:

| Status | Set when |
| --- | --- |
| Needs posting | Full posting could not be found (decision 010) |
| Drafting | Draft started |
| Ready | Draft passed every blocking check |
| Needs you | Blocker left after the fix rounds; or recommendation Consider; or a decision only the user can make |
| Applied | The user says they submitted |
| Skipped | Recommendation Skip, a hard filter hit, or the user passes. Fill Skip reason |
| Closed | The posting is no longer open |

## Next action

Whenever a step sets a Status that needs the user, it also writes the Next
action cell, in these words (fill the angle brackets). The user sees this
line in the morning and nothing else tells them what to do, so keep to it.
Clear the cell when Status becomes Applied, Skipped or Closed.

| Case | Next action |
| --- | --- |
| Ready | Read the resume and cover letter in the Draft folder, edit them, and apply yourself on the employer's site. Then tell Claude you applied. |
| Needs posting | Find the full posting and paste it into Claude with the apply skill. It will score and draft from there. |
| Needs you, Consider | Close to your score bar. Read Why. If you want it, ask Claude to draft it. |
| Needs you, review blocker | Open the Draft folder. Review notes says what is wrong. Fix it, or ask Claude to fix it and run review again. |
| Needs you, text aimed at an AI | The posting has text aimed at an AI (see Flags). Read it. If you still want the job, paste a clean copy of the posting into Claude. |
| Needs you, a check could not run | A check did not run (see Review notes). Ask Claude to run review on the draft in a normal session. |
| Needs you, anything else | <the reason in a few words, and the one thing the user can do> |
| Shortlisted, over tonight's draft cap | Waiting for tomorrow night. To draft it now, ask Claude. |

## Applications tab

When a lead becomes Applied, append one Applications row: Lead ID, Date
applied (today unless the user gives a date), Employer, Title, Link, Pay,
Score at apply (the Score, or the Screen score if there is no Score),
Folder, Resume, Cover letter, Stage reached `Applied`, Outcome `Open`. Ask
for Channel and Referral or contact only if the user has not said; leave
them blank in unattended mode. Never add a second Applications row for the
same Lead ID; update the existing one.
