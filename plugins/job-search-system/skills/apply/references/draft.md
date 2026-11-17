# Draft mode

Goal: a tailored resume and cover letter built only from confirmed facts,
reviewed, saved in a dated folder, with the Leads row showing Ready or
Needs you.

## 1. Preconditions

All must hold. If one does not, say which and stop (unattended: set the
status shown and move on).

| Condition | If not |
| --- | --- |
| Fit mode has run on the full posting: `posting.md` and a valid `posting.json` with `full_text: true` exist | Run fit mode first |
| The job is open (`is_open` is not `closed`) | Status `Closed` |
| Score is at or above `drafting.score_bar` | Interactive: say so and draft only if the user asks anyway. Unattended: never draft; the fit step already set the status |
| Unattended: fewer than `drafting.draft_cap` drafts made tonight | Leave the lead as it is for the next night |
| No hard filter hit and no rule-out | Do not draft |

Set Status `Drafting`.

## 2. Plan

Write a short plan in the working folder (`plan.md`). It is for you and the
user, not for the employer.

1. **Top requirements**, from the extract, in order.
2. **Evidence map**: for each requirement, the confirmed fact IDs and any
   story (`stories.md`) whose fact IDs are all confirmed. Mark requirements
   with no confirmed evidence. Those are gaps: never fill them with
   unconfirmed facts or invented detail.
3. **Situation**: career change, lower level, gap, and whether the
   experienced-candidate module is on (`shared/writing-rules.md`). If on,
   read `shared/modules/experienced-candidate.md`.
4. **Angle**: one sentence on why this person fits this job, made only of
   confirmed facts and the user's own reasons (`answers.md`, `wants.md`).
5. **Letter plan** (`shared/cover-letter.md`): what the employer needs most,
   the one or two examples chosen (story IDs or fact IDs) and what each one
   shows, and the reason for the role if the user has given one.
6. **What is thin**: at most three lines. The user will see this. Include a
   required item the facts do not show, and any chosen example that has
   little detail.

## 3. Write

Follow `shared/writing-rules.md` and `voice.md`. Write, in the working
folder:

- `resume.html` and `resume.txt`
- `cover_letter.html` and `cover_letter.txt`

Write both HTML files with the markup and inline styles in
`shared/html-layout.md` (11 pt body, slightly larger headings, space between
paragraphs). Do not write bare tags. The layout never changes the wording.
- `claims.json`: the claim map for both, in the shape of
  `shared/schemas/claim-map.json`

Write the letter by `shared/cover-letter.md`: one or two examples told as
stories (what happened, what the user did, what changed, why it matters
for this role), a plain close about how the user would help, and the
length in `voice.md`. Do not reuse an old letter's text as evidence.

Build the resume from the facts for this posting. Do not start from an old
resume's structure or wording. Choose and order facts so the top two
requirements are met in the first third of the page. Every bullet must be
in the claim map with its fact IDs.

Before moving on, reread both drafts once against the posting and the
claim map. Remove any claim you cannot map to a confirmed fact.

If the user also asked for answers to application questions, draft them
from `answers.md` and confirmed facts into `answers.txt`, add them to the
claim map as document `answers`, and skip any EEO, age or attestation
question with a note that the user answers it.

If the user asks to revise a letter that already exists, follow "Revising an
existing letter" in `shared/cover-letter.md`: keep their voice, change only
what they ask, check any new claim against `facts.md`, and run review again.

## 4. Review before upload

Run the review skill on the working folder (round 0). It runs the code
checks and an independent reviewer and returns a result in the shape of
`shared/schemas/review-result.json`. The PDF check cannot run yet; the
review skill knows to skip it before upload.

If the result is Blocked and fix rounds remain (`drafting.fix_rounds`,
default 1):

- Fix only the blockers, using the reviewer's `fix` lines and only
  confirmed facts. Do not rewrite unrelated text.
- Update `claims.json`, then run the review again (round 1, and so on).

A blocker with `fix: null` (for example a requirement the user cannot
meet, or a fact that needs confirming) cannot be fixed by you. Stop fixing
and go to upload; the lead will be Needs you.

## 5. Save

Create the application folder in `locations.output_folder_url`, named by
`output.folder_name` (default `{date} {employer} - {title}`; strip
characters Drive does not allow, such as `/`). Then, for each format in
`output.formats`:

- `google_doc`: create a Google Doc from `resume.html` and one from
  `cover_letter.html` (Drive connector, `contentMimeType: text/html`,
  converted to a Google Doc). Names from `output.resume_file_name` and
  `output.cover_letter_file_name`.
- `pdf`: export each Google Doc as `application/pdf`, save the PDF in the
  working folder, then upload it to the application folder. If there is no
  Google Doc (google_doc not in formats), create one, export, and trash it.
- `docx`: export each Google Doc as `.docx` the same way.
- `markdown`: upload the `.txt` versions as `.md` plain text files.

Also save `posting.md` (if `output.save_posting` is true), `posting.json`,
`claims.json`, `plan.md` and the review result as `review.json`, all as
plain text files.

In local test mode, write all of this to `jss-work/<date>/<folder name>/`
instead.

## 6. PDF check

If a PDF was made, run the review skill's PDF check on the downloaded PDFs
(`review` skill, "after upload" step). A failure is a blocker. Do not try
to fix layout problems by building a PDF another way; report it.

## 7. Status

Update the Leads row:

- Draft folder: the folder link.
- Review result: `Pass` or `Blocked` (`Not reviewed` if the review could
  not run).
- Review notes: blockers left, then the recruiter-read notes, under about
  60 words. Put the full detail in `review.json`.
- Next action: the line for the case from `shared/tracker.md`.
- Status: `Ready` only if the final review result is Pass, the code checks
  ran and passed, the reviewer was independent, and the PDF check passed or
  no PDF was made. Otherwise `Needs you`.

## 8. Tell the user (interactive)

- The folder and the status, in one line.
- What is thin (from the plan), at most three lines.
- Blockers left, if any, and what the user can do about each (often:
  confirm a fact, or decide to leave a requirement unaddressed).
- The reviewer's notes, briefly.

The user edits the drafts and submits. When they say they applied, run log
mode.
