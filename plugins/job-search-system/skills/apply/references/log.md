# Log mode

Keeps the tracker matching what the user decided. Do all of the steps for
the case without being asked again.

## Applied

The user says they submitted (for example "applied to <title> at
<employer>").

1. **Find the lead** by Lead ID, link or dedupe key, and check for the same
   job on more than one row (different sources). A different role at the
   same employer is a different lead; leave it alone. If there is no row,
   create one (Source `pasted`) with what the user gives you.
2. **Folder.** If the lead has a Draft folder, use it. If not, create one in
   the output folder (`output.folder_name`) and save what exists: the
   posting (`posting.md`, if captured), and any resume, cover letter or
   answers the user shares.
3. **Final versions.** Ask the user which files they actually submitted, if
   they did not say. If they edited the drafts, ask them to save the final
   versions into the folder (or paste the text). Do not guess which version
   went out.
4. **Leads row.** Status `Applied`, Status date today, Next action
   cleared, on every matching row.
5. **Applications row.** Append it as `shared/tracker.md` describes. Folder,
   Resume and Cover letter link to the submitted versions.
6. **Learn from the edits** (decision 007). If final versions exist and
   differ from the drafts, compare them:
   - Wording the user changed, especially the same kind of change more than
     once: propose additions to `voice.md` (a trait, a banned phrase, a
     preferred wording).
   - A claim the user added that is not in `facts.md`: propose a new fact
     line with the next free ID and ask the user to confirm it. Until they
     do, it stays out of `facts.md`, and future drafts cannot use it.
   - A claim the user removed: ask whether the fact is wrong (fix or delete
     the line) or just not right for this job (no change).
   Show each proposal as the exact line to add or change. Write only what
   the user approves (`shared/profile.md`). Keep this to a few proposals;
   skip trivial edits.
7. **Next step.** Name the next best lead: Ready rows first, then Needs you,
   by Score, and any deadline within a week.

## Skipped

The user passes on a lead. Status `Skipped`, Status date today, and Skip
reason in the user's words (short). Clear Next action. Update every
matching row.

## Parked

The user wants to come back later. There is no Parked status. Leave Status
as it is, set Follow-up date if the user gives one, and add a short line to
Notes (the user asked, so writing Notes is fine).

## Closed

The posting is gone or no longer accepting applications. Status `Closed`.
If an Applications row exists, leave it; the posting closing after the user
applied says nothing about the outcome.

## Outcome updates

If the user reports a response (a screen, an interview, a rejection),
update the Applications row: Stage reached, Outcome, First response date,
Next step date. Do not change the Leads row.

## If something is not in the tracker

Say so in one line and continue. Never add or rename columns to make
something fit.
