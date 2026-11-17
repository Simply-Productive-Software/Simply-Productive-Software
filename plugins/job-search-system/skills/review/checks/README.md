# checks/

Python scripts that check drafts for what code can verify exactly (decision
007). The review skill runs them; the apply and scout skills use the
validator and the dedupe key. `tools/sync_shared.py` copies this folder
(without `tests/`) into `skills/apply/`, `skills/review/` and
`skills/scout/`, so the scripts must not import anything from outside this
folder except `../shared/schemas/`, which sits at the same relative path in
the repo and in every skill copy.

**Status:** built. The scripts follow this contract, and `tests/` has a passing
draft plus a bad draft for each blocker type. Run the tests with
`python3 -m pip install -r checks/requirements.txt pytest reportlab` and
`python3 -m pytest checks/tests`. `reportlab` is needed by the PDF tests only.

## Behavior beyond the contract text

These were decided while building. They narrow what counts as a blocker or
spell out something the contract left open.

- **Exemptions in `facts_trace`.** Numbers in the target job title and
  employer name, and the posting's captured date and deadline, are not
  traced to facts. Email addresses, links, phone numbers, street addresses
  and the contact values in `profile.yaml` are removed before numbers and
  dates are scanned. Contact values are matched as whole words.
- **Links.** A link in a draft must be one the profile lists under
  `show_on_resume.links`, or the posting's own link (`link` in the lead, `apply_link` or `source_url` in the extract). A dotted tool name such as Split.io is not a link if it appears word for word in a confirmed fact. Anything starting with http or www is always a link.
- **Resume headings.** `voice.md` may add an optional line
  `Resume headings: A, B, C`. The PDF check accepts those headings as well
  as the standard ones.
- **PDF name check.** A resume PDF must start with the full name. The check
  reads the start of the text with whitespace collapsed, because PDFs
  exported from Google Docs extract with one word per line. In other PDFs the name must appear after emails and links are
  removed, because those often contain the name.
- **Spelling.** English dictionary only. A word is a blocker only if it is
  lowercase, 4 or more letters, not in the allow-list (facts, profile,
  posting, voice, UK-to-US variants) and the checker has a likely
  correction. Other unknown words are warnings.
- **Heuristics.** Wrong-employer detection in the cover letter (the
  greeting and opening paragraph) and role-header matching in the resume
  (the line plus its neighbours) are heuristics. They can miss a case or
  flag an odd layout. A blocker names the quote so the reviewer can judge.
- **Numbers in `answers.md`** are not allowed in a draft unless a confirmed
  fact has them.
- **Test date.** The environment variable `JSS_TODAY` (YYYY-MM-DD)
  overrides today's date. Tests use it.

## Requirements

- Python 3.10 or later. Dependencies in `requirements.txt`: `pypdf`,
  `pyspellchecker`, `pyyaml`, `jsonschema`. Nothing that needs a network
  connection at run time.
- If an import fails, exit with code 2 and print
  `{"error": "missing dependency: <name>", "fix": "python3 -m pip install -r <path>/requirements.txt"}`.
  The skills install and retry once.
- No personal data in the repo. Tests use `examples/marisol-teague/` and
  fixtures made for her.

## Commands

### `run_checks.py`

```sh
python3 checks/run_checks.py --workdir DIR [--skip NAMES] [--only NAMES]
```

`NAMES` is a comma-separated list of check names (below). Reads the files in
`DIR`, runs the checks, prints one JSON object to stdout:

```json
{
  "schema_version": 1,
  "ran": ["posting", "facts_trace", "skills", "target", "contact", "language", "claims"],
  "skipped": [{"check": "pdf", "reason": "skipped by --skip"}],
  "passed": false,
  "blockers": [
    {"check": "unconfirmed_fact", "document": "resume", "quote": "$400K", "detail": "Number appears only in unconfirmed fact F-017.", "fix": null}
  ],
  "warnings": [
    {"check": "posting", "detail": "Open status last checked 4 days ago."}
  ]
}
```

- Each blocker has the same shape as a blocker in
  `shared/schemas/review-result.json`, and its `check` value is one of that
  schema's enum values. `fix` may be null.
- `passed` is true only if no check produced a blocker.
- Exit codes: 0 passed, 1 blockers found, 2 could not run (missing input,
  missing dependency, unreadable file). On exit 2, print
  `{"error": "...", "fix": "..."}`.
- A check whose input files are absent is skipped with a reason (for
  example `pdf` with no PDFs), except `posting`, whose missing input is a
  blocker.

### `validate.py`

```sh
python3 checks/validate.py SCHEMA FILE
```

`SCHEMA` is `posting-extract`, `claim-map` or `review-result`, loaded from
`../shared/schemas/<SCHEMA>.json`. Prints `{"valid": true}` or
`{"valid": false, "errors": ["<json path>: <message>", ...]}`. Exit 0 if
valid, 1 if not, 2 if the file is not JSON or the schema is missing.

### `dedupe_key.py`

```sh
python3 checks/dedupe_key.py --employer "..." --title "..." --location "..."
```

Prints the key. Must match `dedupeKey_()` in `collector/src/Util.gs`
exactly (normalization rules in `shared/tracker.md`). Tests compare against
cases taken from `collector/test/units.test.js`, plus: `The Acme Co.` +
`Sr. Analyst` + `Spokane, WA (Hybrid)` gives `acme|sr analyst|spokane`.

## Working folder layout

`run_checks.py` reads these from `--workdir`. All are optional except where
a check says otherwise.

| File | What |
| --- | --- |
| `resume.txt`, `cover_letter.txt`, `answers.txt` | Draft text. For drafts the system made, written by the drafter. For a user's own draft, exported from a Google Doc as plain text, so do not depend on exact layout |
| `resume.pdf`, `cover_letter.pdf` | Exported from the Google Doc |
| `claims.json` | Claim map (`shared/schemas/claim-map.json`) |
| `posting.md` | Full posting text. First two lines `Source: <url>` and `Captured: <YYYY-MM-DD>` |
| `posting.json` | Posting extract (`shared/schemas/posting-extract.json`) |
| `lead.json` | `{"lead_id", "employer", "title", "link", "is_open", "open_checked"}`; `is_open` is `open`, `closed` or `unknown`; `open_checked` is `YYYY-MM-DD` |
| `facts.md`, `voice.md`, `profile.yaml` | Copies of the user's profile files |

## Parsing the profile files

- `facts.md`: fact lines match
  `^- \[(confirmed|unconfirmed)\] (F-\d{3,}) \| (.*?) \| (.*?) \| (.*)$`
  (employer, title, detail; `-` means none). Ignore `<!-- -->` comments.
  Each fact records its `section` (the nearest `##` heading) and its
  `subsection` (the nearest `###` heading under that section, or empty; a
  new `##` heading clears it). Under Results and scope the subsections are
  employers; under Skills and tools they are skill categories (decision
  023). Roles are found by section, so a `###` heading never hides them.
  The "Do not claim" and "Wording rules" sections are for the reviewer, not
  for code.
- `voice.md`: the banned phrases are the lines of the first fenced block
  under the "Banned phrases" heading. The "Spelling and format" section
  gives the spelling variety (`US`, `UK`, `Canadian`, `Australian`).
- `profile.yaml`: `contact` and `contact.show_on_resume`.

## The checks

### `posting` (blocks: `posting_missing`, `posting_closed`)

- Blocker `posting_missing` if `posting.md` is missing, has fewer than 120
  words after the two header lines, or `posting.json` is missing, invalid,
  or has `full_text: false`. Decision 010: never draft from a snippet.
- Blocker `posting_closed` if `lead.json` has `is_open: "closed"`.
- Warning if `open_checked` is missing or more than 3 days old.

### `facts_trace` (blocks: `claim_not_traced`, `unconfirmed_fact`)

Every number, date, employer and title in the drafts must appear in a
confirmed fact line.

- **Numbers**: integers, decimals, percentages, money (`$212,000`,
  `$212K`, `$1.2M`), counts (`14 cabinets`), ranges. Compare by value after
  normalizing (`$212K` equals `212,000`; `31%` equals `31 percent`). Hedged
  numbers keep their hedge: `about 40` in a fact allows `about 40` or
  `roughly 40`, not a bare `40`.
- **Dates**: years and month-years in any common form (`2021`, `Jun 2021`,
  `June 2021`, `06/2021`, `2021-06`), normalized to `YYYY` or `YYYY-MM`. A
  draft date must appear in a confirmed fact line.
- **Employers and titles**: in the resume's experience section, lines that
  contain a date range are role headers. Each must contain the employer and
  title of a confirmed Roles line (normalized as in `shared/tracker.md`).
  Any employer named anywhere in the drafts that matches only an
  unconfirmed line is a blocker.
- Allowed without a fact: numbers and dates that are part of the contact
  details in `profile.yaml`, the target job title and employer from
  `lead.json`, ordinal list markers, and numbers inside the posting's own
  job title.
- A value found only in unconfirmed lines: `unconfirmed_fact`, naming the
  fact IDs. Found nowhere: `claim_not_traced`.

### `skills` (blocks: `wrong_category`, `claim_not_traced`, `unconfirmed_fact`, `overstated`, `other`)

The Skills section of `resume.txt` (decision 023). Skipped without
`resume.txt`; does nothing if the resume has no Skills heading. The section
runs from a `Skills` (or `Technical Skills`, `Skills and tools`, `Core
skills`, `Key skills`) heading to the next known heading.

Each line should be `Label: item, item`. Labels are compared with the
`###` headings under `## Skills and tools` in `facts.md`, case and
punctuation ignored.

- A line with parentheses or a semicolon: `other`.
- A line with no label: `other`. The fix names the categories its items are
  confirmed under.
- A label that is not a category heading: `wrong_category`, listing the
  categories.
- For each item, in this order:
  - It matches a confirmed fact under the line's category: passes, unless
    every matching fact gives a limiting level (`basic`, `beginner`,
    `introductory`, `familiar`, `limited` and similar, in the first
    sentence of the fact) and the item does not keep one: `overstated`.
    The exception (decision 024): if the Wording rules in `facts.md` have a
    `- Skills intro: <text>` line and that text is printed as its own line
    in the Skills section, the items may drop the level. The intro line is
    not treated as a skills line. If the intro is configured but not
    printed, `overstated` still applies and the fix says to print it.
  - It matches a confirmed skill under another category: `wrong_category`,
    naming the right category and fact ID ("Python is confirmed under
    Languages (F-030)").
  - It matches only an unconfirmed skill: `unconfirmed_fact`.
  - It matches a confirmed fact outside Skills and tools (a credential, for
    example): `wrong_category`, "not as a skill".
  - Otherwise: `claim_not_traced`.
- An item matches a fact when all its words (level words aside, plurals
  folded) are in the fact line, so "Power Query" matches "Excel: daily use,
  including Power Query". A long form matches an acronym in the fact by its
  initials ("Structured Query Language" and "SQL"), and an acronym matches
  a long form in the fact the same way. This is what lets a line carry
  both forms as two items ("Amazon Web Services, AWS"), as the writing
  rules ask.
- **Warn only** if `facts.md` has no category headings under Skills and
  tools yet: one warning that labels were not checked, plus a warning for
  each item that is in no confirmed skill fact. No blockers.

What code cannot see (a custom category whose name does not fit the item,
"tools such as Python" in a cover letter) is the reviewer's
`wrong_category` blocker.

### `target` (blocks: `wrong_target`)

- The cover letter names the employer and the job title from `lead.json`
  (normalized match; a title may drop a trailing level marker such as `II`
  only if the posting itself does).
- Blocker if either is missing, or if the cover letter's greeting or first
  paragraph names a different employer as the one being applied to.

### `contact` (blocks: `contact_details`, `never_in_draft`)

- The first non-empty line of the resume and of the cover letter is
  `contact.full_name` exactly.
- Every email, phone number and URL in the drafts belongs to
  `profile.yaml` contact. One that does not: `contact_details`.
- Each contact item appears if and only if `show_on_resume` allows it.
- Anything that looks like a street address: `never_in_draft`.

### `language` (blocks: `banned_phrase`, `spelling`, `never_in_draft`)

- **Banned phrases**: each line of the banned block, case-insensitive,
  matched on word boundaries with punctuation ignored. An entry made only
  of punctuation (such as a long dash) is matched as that literal
  character. Quote each hit.
- **Age hints**: phrases in `data/age_phrases.txt` (for example `decades
  of`, `seasoned veteran`, `digital native`): `never_in_draft` (decision
  015).
- **Spelling**: use the variety from `voice.md`. Build an allow list from
  every word in `facts.md`, `profile.yaml`, `posting.md` and `voice.md`
  (names, tools and jargon come from there). Blocker only for a word that
  is unknown, not on the allow list, all lowercase, at least 4 letters, and
  has a likely correction. Other unknown words are warnings. False
  blockers are worse than a missed typo, because a blocker keeps a draft
  off the morning list.

### `pdf` (blocks: `pdf_parse`)

For each PDF:

- Text extracts and is not empty.
- Every font is embedded (font descriptors have `FontFile`, `FontFile2` or
  `FontFile3`). A PDF built with standard, non-embedded fonts failed to
  parse in a real application portal; that is the case this catches.
- The full name appears in the text.
- The section headings in the matching `.txt` (lines that are exactly one
  of Summary, Skills, Experience, Education, Certifications, or the
  `voice.md` variants) appear in the PDF text in the same order.
- At least 90 percent of the distinct words in the `.txt` appear in the PDF
  text.
- Warning if the page count is over the resume length in `voice.md`.

### `claims` (blocks: `claim_not_traced`, `unconfirmed_fact`)

Runs only if `claims.json` exists.

- It validates against `claim-map.json`.
- Every fact ID exists in `facts.md` and is confirmed.
- A claim of kind `fact` with no fact IDs: `claim_not_traced`.
- Warning if a claim's text cannot be found (roughly) in its document.

## Tests

`checks/tests/` with pytest. At least:

- A good draft for `examples/marisol-teague/postings/01-strong-fit.md`
  (resume, cover letter, claims map) that passes every check.
- One bad draft per blocker type, each failing only that check: a number
  from unconfirmed F-017; a number in no fact; a banned phrase; the wrong
  employer in the cover letter; a phone number that is not in
  `profile.yaml`; her phone shown after a test copy of `profile.yaml` sets
  `show_on_resume.phone: false`; a street address; an age phrase; a
  closed posting; a snippet-only posting; a claim map citing F-035.
- Two PDFs generated in the test: one with an embedded TrueType font
  (passes) and one with a standard non-embedded font (fails `pdf_parse`).
- `dedupe_key.py` against the collector's cases.
- `validate.py` on a good and a bad file for each schema, including the
  extract for each of the three example postings.
- `parse_facts` keeping `section` and `subsection` apart, with roles still
  found when a `###` heading is present.
- `skills`: the bad fixture `fixtures/bad/resume-skills-wrong-label.txt`
  (`Tools: Python, RabbitMQ, ...`) must block with messages that name the
  right category; one test per blocker type; the warn-only path when
  `facts.md` has no categories.

`python3 tools/sync_shared.py --check` must pass after the scripts are
added.
