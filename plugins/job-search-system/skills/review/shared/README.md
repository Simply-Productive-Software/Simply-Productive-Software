# shared/

Rules and schemas that more than one skill uses. This folder is the only
place to edit them.

Each skill must work on its own, because some installs (for example a
plugin uploaded to claude.ai) give each skill its own folder with no
access to the rest of the repo. So `tools/sync_shared.py` copies this
folder into every skill as `skills/<name>/shared/`, and copies the check
scripts and profile templates into the skills that need them. Never edit
the copies. Run the tool after any change here:

```sh
python3 tools/sync_shared.py          # copy
python3 tools/sync_shared.py --check  # fail if any copy is out of date
```

| File | What it covers | Used by |
| --- | --- | --- |
| `profile.md` | Finding, reading and writing the user's profile folder and tracker; local test mode | All skills |
| `tracker.md` | Reading and writing the tracker by header name, Lead IDs, statuses, dedupe | apply, scout, onboard |
| `scorecard.md` | How to score a posting on the 12-point scorecard (decision 011) | apply, scout, onboard |
| `untrusted-input.md` | How posting and email text is handled (decisions 009 and 017) | apply, scout, review |
| `writing-rules.md` | What a draft may and may not say (decision 014), format rules that keep files parsable | apply, review |
| `cover-letter.md` | How to choose the angle and the one or two examples, tell them as stories, close, revise and review a letter (decision 026) | apply, review |
| `skill-categories.yaml` | The `tech` and `general` presets of skill categories: label, meaning, examples and what does not belong (decision 023) | onboard, review |
| `html-layout.md` | Type sizes, spacing and exact inline styles for `resume.html` and `cover_letter.html`, so the Google Doc and PDF look right | apply, review |
| `unattended.md` | How skills behave when run by the nightly task with no one present | apply, review, scout |
| `modules/` | Optional drafting modules switched on by situation fields (decision 015) | apply, review |
| `schemas/` | JSON shapes for the posting extract, the reviewer result and the claim map | apply, review, checks |

The sync tool also puts `templates/tracker-schema.yaml` and
`templates/profile/settings.yaml` (as `default-settings.yaml`) into each
skill's `shared/` folder, so skills can read the scorecard anchors, column
names and default settings. They are not kept in this folder; `templates/`
stays their only source.
