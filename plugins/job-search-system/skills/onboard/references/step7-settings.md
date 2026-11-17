# Step 7: Settings

`settings.yaml` already holds the Pro plan defaults (decision 012). This
step checks them with the user.

1. Ask which Claude plan they have (Pro or Max). Set `plan`.
   - Pro: keep the defaults (2 drafts a night, score bar 9, Sonnet drafts
     and reviews).
   - Max: show the suggested Max values at the bottom of the file and ask
     whether to apply them. Say they are unmeasured starting points.
2. Confirm the run times in their time zone (`profile.yaml`):
   `schedule.collector_time` (default 01:00) and `schedule.nightly_time`
   (default 03:00). The nightly task runs late so the plan's usage window
   resets before their day starts.
3. Ask which file formats they want for drafts (`output.formats`; default
   Google Doc and PDF). Mention that PDFs exported from the Google Doc parse
   well in application portals.
4. Leave everything else at the defaults unless they ask. Point out that
   any value can be changed later by asking.

Save `settings.yaml`, changing only the lines they chose, and confirm it
parses.
