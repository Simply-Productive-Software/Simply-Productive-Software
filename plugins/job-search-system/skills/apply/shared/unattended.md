# Running with no one present

The nightly task (build step 6) runs the apply, review and scout skills at
night with no one to answer questions. A skill is in unattended mode when
the prompt that started it says so ("unattended", or it comes from the
nightly task). Otherwise assume the user is present.

## Rules

1. **Never ask.** Where a skill would ask the user, take the safe choice
   listed in that skill and record what you chose. The safe choice is
   always the one that sends less, claims less and marks the lead for the
   user: usually Status Needs you.
2. **Stay inside settings.** Never go past `drafting.draft_cap`,
   `screening.shortlist_max` or `drafting.fix_rounds`, and never draft
   below `drafting.score_bar`. Use the models named in settings.
3. **Never change the profile.** Profile updates are proposed to the user,
   never written, in unattended mode. Put proposals in the lead's Review
   notes or the Run Log Notes.
4. **Nothing outbound.** Same rule as always (decision 013), with no
   exceptions for "urgent" leads or deadlines.
5. **Leave a trail.** Every lead you touch gets its Status, Status date and,
   if relevant, Why, Flags and Review notes updated. Fill the nightly
   columns of today's Run Log row (the collector creates the row; add one
   if it is missing): write Nightly started first and Nightly finished
   last. The collector reports a night with no start time. Set Next action
   on every lead the user must act on (`shared/tracker.md`). Put short error messages in Errors.
6. **Fail closed.** If a source, the profile or the tracker cannot be read,
   or a check script cannot run, do not guess. Mark affected leads Needs
   you with the reason, record the error, and move on to the next lead.
7. **Ready means checked.** A draft is Ready only if the code checks ran and
   passed and an independent reviewer (a separate context) found no
   blockers. If either could not run, the status is Needs you.
