# The profile folder and the tracker

Every skill works from two things the user owns: a profile folder in their
Google Drive (decision 006) and a tracker Google Sheet (decision 004).
Neither is ever copied into this plugin or the repo.

## Finding them

Everything for one setup lives in one **system folder** (decision 020):
`Profile/` (the eight files), `Applications/` (dated folders) and the
tracker sheet. A user can have more than one system folder.

1. If the user gave a folder or sheet link in this conversation, use it. A
   system folder link: its profile folder is the subfolder that holds
   `profile.yaml`. A link to a folder that holds `profile.yaml` itself: that
   is the profile folder, and its parent is the system folder.
2. Otherwise search Drive for a file titled exactly `profile.yaml` whose
   content has `schema_version:`. Its parent folder is the profile folder and
   the parent's parent is the system folder. If there is more than one,
   list the system folder names (and where each sits) and ask which one. In
   unattended mode use the system folder named in the task's prompt; if
   none is named and there is more than one, stop and record the problem
   (see `unattended.md`).
3. Read `settings.yaml` in the profile folder. `locations.tracker_sheet_url`
   is the tracker, `locations.output_folder_url` is where application
   folders go and `locations.system_folder_url` is the system folder.
   Settings made before decision 020 have no system folder line; the
   profile folder's parent is the system folder then.
4. If no profile folder exists, the user has not onboarded. Offer the
   onboard skill and stop.
5. Stay with the one system folder you found or were given for the rest of
   the conversation. Never mix files from two.

Check once per session that the tracker's hidden Config tab has
`profile_folder_id` equal to the folder you found. If it differs, tell the
user: the overnight collector is reading a different folder.

## Reading

Read files with the Drive connector. Profile files are plain text files
(`text/plain`, `.md` or `.yaml` names), not Google Docs. The collector reads
them as raw text, so they must stay plain text.

What each file is for:

| File | Use it for | Never |
| --- | --- | --- |
| `profile.yaml` | Contact details for drafts, situation fields, module switches | Ask for or infer age (decision 015) |
| `facts.md` | The only source of claims in a draft. Use `[confirmed]` lines only | Use `[unconfirmed]` lines in a draft |
| `wants.md` | Scoring, flags, hard filters | Override the user's own scoring words with the generic anchors |
| `voice.md` | Tone, spelling, length, banned phrases | Copy sample text into a draft |
| `stories.md` | Picking evidence for a posting | Use a story whose fact IDs are not all confirmed |
| `answers.md` | Application questions | Answer EEO, age or attestation questions |
| `sources.yaml` | Where to search | Store API keys here |
| `settings.yaml` | Caps, score bar, models, formats, file names | Treat a missing key as an error. Missing keys fall back to `shared/default-settings.yaml` (a copy of the template) |

Keep a working copy of what you read in a local folder,
`jss-work/<YYYY-MM-DD>/`, so the check scripts can read it. Delete nothing
from Drive. The local folder holds personal data: never commit it, never
copy it into the plugin folder.

## Writing a profile file

Only change a profile file when the user has approved the exact change,
except where a skill says otherwise (onboarding writes the files it is
filling in).

1. If you can edit the file in place (for example the Drive folder is
   mounted on the user's computer), do that.
2. If the connector can only create files (the usual case), create the new
   version first with the same name, `contentMimeType: text/plain` and
   `disableConversionToGoogleType: true`, in the same folder. Then move the
   old file to the trash. Creating first means the collector never finds
   the file missing. Trashed files stay recoverable for about 30 days.
3. Read the new file back and confirm it parses (YAML loads; facts lines
   keep the `- [confirmed] F-001 | ... | ... | ...` shape).
4. Tell the user what changed in one or two lines.

## Local test mode

For tests, demos and anyone without Google set up yet, the profile can be a
local folder, for example `examples/marisol-teague/profile/`. Say "use the
local profile at <path>" to switch it on. In test mode:

- Read profile files from that folder. Write nothing to it.
- Write tracker rows as JSON lines to `jss-work/<date>/tracker-rows.jsonl`,
  one object per row, keyed by the tracker column names, with an extra key
  `"tab"`.
- Write `posting.md`, extracts and drafts to `jss-work/<date>/<employer>-<title>/`.
- Postings come from files or pasted text, not from the web, unless the user
  asks.
- State at the top of every reply that test mode is on.
