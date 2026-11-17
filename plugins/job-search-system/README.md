# Core plugin: job-search-system

Builds a career profile, drafts a tailored resume and cover letter for a job the user chooses, checks the draft against the user's confirmed facts, and logs applications in a tracker sheet. The user edits and submits. Nothing is ever submitted for them (decision 013).

Core does not judge fit and has no scoring (decision 031). It has no collector, no overnight task and no Apps Script (decision 028).

Everything personal lives in one system folder in the user's own Google Drive (decision 020). Nothing personal is written to this plugin or to the repo.

## Skills

See `skills/`. Each skill is self-contained (decision 018): its `shared/`, `checks/` and `templates/` folders are copies made by `tools/sync_shared.py`, so never edit them.
