# Core plugin: job-search-system

Builds a career profile, drafts a tailored resume and cover letter for a job the user chooses, checks the draft against the user's confirmed facts, and logs applications in a tracker sheet. The user edits and submits. Nothing is ever submitted for them (decision 013).

Core does not judge fit and has no scoring (decision 031). It has no collector, no overnight task and no Apps Script (decision 028).

Everything personal lives in one system folder in the user's own Google Drive (decision 020). Nothing personal is written to this plugin or to the repo.

## Requirements

The user's own Google Drive and Google Sheets connectors, turned on in Claude. Onboarding checks for them and stops, naming the one that is missing.

## Use at your own risk

Beta, provided as is, with no warranty. The drafts are written by AI and can be wrong or incomplete. The user must read and check everything before using it, is responsible for the facts they confirm and for what they send, and uses the plugin at their own risk. Nothing is guaranteed. The license says what the user may and may not do with the plugin (the `LICENSE` file in the plugin folder).

## Skills

See `skills/`. Each skill is self-contained (decision 018): its `shared/`, `checks/` and `templates/` folders are copies made by `tools/sync_shared.py`, so never edit them.
