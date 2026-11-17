# Step 9: Schedule

## Collector (stage one)

1. Ask the user to open the tracker and run **Job Search > Check
   configuration**. Fix anything it reports before going on.
2. Ask them to run **Job Search > Run collector now** once and tell you the
   summary. Look at the new Leads rows with them: do the leads and screen
   scores look sensible? If not, go back to step 6 (sources) or step 8
   (calibration).
3. Ask them to run **Job Search > Install daily trigger**. It runs the
   collector every day at about `schedule.collector_time`.

## Nightly task (stage two)

The nightly task gets the full posting for shortlisted leads, scores them,
drafts and reviews (decision 003). Its prompt is `bundle/nightly-prompt.md`
in this skill's folder. The user never needs the repo.

1. Read `bundle/nightly-prompt.md`. Take the text between its two lines.
   Fill the two `<<...>>` values: `locations.system_folder_url` and
   `locations.tracker_sheet_url` from `settings.yaml`. Leave the date
   placeholder for the task to fill each run.
2. Show the user, in plain words, what the task may do: read the profile
   folder, write to the tracker and the Applications folder, fetch
   postings, and start a reviewer. And what it may not do: send email,
   touch the calendar, use a browser, fill forms, post or share anything
   (decisions 013 and 021). Ask for a yes before creating it.
3. If a scheduling tool is available (look with the tool search; it may be
   called create_trigger), create a daily scheduled task at
   `schedule.nightly_time` in the user's timezone, with the filled prompt.
   If the tool lets you set which tools the task may use, use the list in
   the bundle file. If it does not, say so: the prompt wording is then the
   only control. Say which approval setting the task got. Confirm it saved
   and tell the user how to find it.
4. If there is no scheduling tool, show the filled prompt and the
   schedule, and walk the user through making the scheduled task by hand,
   one step at a time. Say this is the one place they copy and paste.
5. Offer a test run now: run the filled prompt once in this session,
   marked as a test, on the user's current Shortlisted leads, and show
   what it did. Do not run it without a yes.
6. Once the task exists (created, or the user confirms they made it), set
   `schedule.nightly_enabled: true` in `settings.yaml`. The collector then
   reports any night the task did not run in the Run Log Errors cell. Tell
   the user: each morning, open the Leads tab and read the Next action
   column on every row that is not blank. It says what to do. If today's
   Run Log row has Errors, read that first.
7. Whether a scheduled run can use the plugin's skills and the user's
   Drive, Docs and Sheets connectors is not yet confirmed (build step 7).
   If the first morning shows nothing happened, check the task's last run
   first.

## Done

Show the finishing summary from `SKILL.md`.
