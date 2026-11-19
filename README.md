# simply-productive-software

A catalog of Claude plugins from Simply Productive Software. Each plugin is a set of skills you add to Claude. This repo is the catalog and the plugin files; nothing runs from here.

**Status: early testing.** The plugins are not ready for general use, and the layout may change.

## Plugins

| Plugin | What it does |
| --- | --- |
| `job-search-system` | Builds a job-search profile, tailors a resume and cover letter to a job you give it, reviews the draft, and tracks applications in your Google Drive. Nothing in it submits applications, sends email or fills in forms. You do that yourself. |

## Add this marketplace

**Claude on the web or desktop app:** open Customize, then Plugins, then Add, then Add marketplace, and enter `Simply-Productive-Software/simply-productive-software`. You do not need a GitHub account.

**Claude Code:**

```
/plugin marketplace add Simply-Productive-Software/simply-productive-software
/plugin install job-search-system@simply-productive-software
```

## Data

The job-search-system plugin works with your own Google Drive through connectors you authorize in Claude. It creates folders and files there for your profile, drafts and tracker. This repo holds no personal data. Skills in this marketplace are not reviewed by Anthropic when you add them from a repo, so read what you install.

## Docs

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): every file and folder in this repo, what it does and why it is needed, and how a release gets here

## Contact

simplyproductivesoftware.com
