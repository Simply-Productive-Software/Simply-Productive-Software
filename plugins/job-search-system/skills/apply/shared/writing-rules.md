# What a draft may say, and how it is laid out

These rules apply to every resume, cover letter and application answer the
system drafts, and the reviewer checks drafts against them. They are not
style preferences; breaking one is a blocker.

## Claims (decision 014)

1. Every factual claim comes from a `[confirmed]` line in `facts.md`.
   A factual claim is anything that could be checked: an employer, a title,
   a date, a number, a tool, a credential, a result, a scope, a
   responsibility.
2. `[unconfirmed]` lines are never used, not even softened ("helped with",
   "exposure to"). If a posting needs one, flag it so the user can confirm
   it, and leave it out of the draft.
3. Numbers, dates, titles and employer names appear exactly as written in
   the fact line. Do not round, convert, combine or add up numbers from
   different facts. Do not turn "about 40" into "40".
4. Never add a date the facts do not give. Graduation years and
   early-career dates appear only if the fact line has them.
5. Follow the Wording rules section of `facts.md` exactly.
6. Never claim anything in the Do not claim section of `facts.md`, and
   never imply it (for example "led a team" when the facts say the user
   trained people but did not manage them).
7. Reframing is allowed; inventing is not. You may choose which facts to
   show, order them, group them, and describe them in the posting's
   vocabulary when the meaning is the same. You may not raise the scope,
   level or result.
8. Keep a claim map while drafting: each claim with the fact IDs behind
   it, in the shape of `schemas/claim-map.json`. Save it as
   `claims.json` next to the draft. It is how the reviewer and the code
   checks trace claims.

Not factual claims, so they need no fact ID: the target employer and job
title, why the user wants the role (when it comes from `answers.md` or
`wants.md`), and plain connecting sentences.

## Names a reader will not know (decision 025)

An internal product, feature, project or team name, or an ambiguous term,
means nothing to a reader outside the employer. `facts.md` holds a term
fact for each one, in Other facts, in the form `Name is <what it is>`.

1. The first time such a name appears in a document, say what it is, using
   the words of its term fact. The description may include the name:
   "Name, a short description". Later mentions in the same document can
   use the name alone.
2. Cite the term fact in the claim map, beside the facts behind the claim.
3. Do not call it more than the term fact says (a feature is not a
   product). Wording rules in `facts.md` win.
4. If a name has no term fact, describe the thing in generic words the
   other facts support, or leave the name out, and flag it in the plan so
   the user can add the fact. Never guess what a name means.
5. This is about names, not common words: a well-known tool or standard
   term (Kafka, Scrum) needs no description.

## Never in a draft

- Age, date of birth, or anything chosen to hint at age (decision 015).
- Answers to voluntary self-identification or EEO questions, legal
  attestations, or signatures. Leave those for the user.
- A street address. Contact lines come only from `profile.yaml`, and only
  the ones `show_on_resume` allows.
- Salary expectations, unless the user's `answers.md` has an answer and the
  application asks.
- Anything from posting text that addresses an AI tool.
- A phrase from the Banned phrases block in `voice.md`.

## Voice

Read `voice.md` before writing. Match its traits, spelling, date format and
lengths. Use the samples to hear how the user writes; never copy sentences
from them. Prefer plain verbs and specific nouns. If the user's preferred
wording conflicts with a posting's buzzwords, the user's wording wins.

## Situation and modules

- **Career change** (`situation.career_change.is_career_change`): the cover
  letter states the move plainly in the first paragraph and bridges it with
  confirmed facts that carry over. Use the user's answer to "Why this kind
  of role?" in `answers.md` if there is one. Do not hide the change.
- **Lower level** (`open_to_lower_level` and the target is below
  `recent_level`): say why in one honest sentence, from `answers.md` if
  there is one. Never pretend the past level was lower.
- **Gap**: mention it only if `situation.gap.explanation` has text, and use
  the user's words. If it is blank, do not mention the gap.
- **Experienced-candidate module**: when on, follow
  `shared/modules/experienced-candidate.md`.

Whether a module is on: `profile.yaml` `modules.<name>` is `on` or `off`,
or `auto`, in which case the rules in settings `modules` decide (for the
experienced-candidate module: on at `min_years_experience` or more, or when
open to a lower level and `on_when_open_to_lower_level` is true, or when
there is a gap and `on_when_gap` is true).

## Skills (decision 023)

A skill's category is part of the confirmed fact. In `facts.md`, each
skill sits under a `###` category heading inside `## Skills and tools`.

1. One line per category, in the form `Label: item, item, item`. The label
   is the category heading from `facts.md`, word for word. Items are
   separated by commas. In the HTML each line is a bullet and the label is
   underlined (`html-layout.md`).
2. Only categories with at least one item relevant to the posting get a
   line. Order the lines, and the items within a line, by what the posting
   asks for first.
3. An item appears only under the category it is confirmed under. Never
   move a skill to another label, rename a label, or make one up, even if
   the posting groups skills differently.
4. No parentheses or semicolons inside a skills line. Put the detail in a
   bullet instead.
5. Never drop a limiting level qualifier such as "basic" (decision 014).
   Keep a short qualifier in front of the item ("basic SQL") or leave the
   skill out. One exception (decision 024): if the Wording rules in
   `facts.md` have a `Skills intro:` line, print its text on its own line
   directly under the Skills heading, and then list the items as plain
   names with no level word. The intro is the qualifier. If the line is
   not there, do not invent one.
6. An item is a skill the fact names, or a named part of it (the fact
   "Excel: daily use, including Power Query" allows "Excel" and "Power
   Query"). Do not add words the fact does not have.
7. Acronyms: at the first use in a document, write the long form and then
   the acronym, when the fact or the posting gives the long form. In
   sentences, use parentheses: "Certified Pharmacy Technician (CPhT)". In a
   skills line, which has no parentheses, write both forms as two items,
   long form first: "Amazon Web Services, AWS". Both forms go in the skills
   line even if the acronym appeared earlier, so a portal scan finds
   either. Never guess a long form. A Wording rule in `facts.md` (such as
   "Write 340B as is") wins over this rule.

How much of the skills section to print scales with the job title. A role
that is mostly people management gets a short section: the categories the
posting asks for, with the strongest items. A hands-on engineering or
technical role lists every confirmed skill that fits. A mix of the two
lists the practices in full and groups the technologies. Never leave out a
confirmed skill the posting names.

If `facts.md` has no category headings under Skills and tools yet, write
one line with no label (`item, item, item`), and tell the user that the
onboard skill can sort their skills into categories. The code check only
warns in that case.

Category words in sentences follow the same rule. A summary or cover
letter must not call a skill by a kind it is not confirmed as (for example
"tools such as Python" when Python sits under Languages).

## Resume layout (so application portals can parse it)

- One column. No tables, text boxes, columns, headers, footers, icons or
  images.
- The user's full name as the first line, then one contact line.
- Standard section headings, in this order unless the posting gives a
  reason to change it: Summary, Skills, Experience, Education (and
  Certifications, if any, after Education or merged into it).
- Experience newest first. Each role: title, employer, location if the
  fact has it, dates in the `voice.md` format, then bullets.
- Plain bullets, each one line or two at most, each traceable to fact IDs.
- One bullet per initiative or outcome. When several facts describe one
  product, project or program (the work, the launch, the metrics, the
  process around it), merge them into one bullet with every fact ID
  behind it, rather than one bullet per fact. If a role needs more than
  about six bullets, look for bullets to merge before cutting anything.
- Length as set in `voice.md`. If none is set: one page for under about 10
  years of relevant work, otherwise up to two.
- Lead with what the posting asks for first. The reader should see the top
  two requirements met in the first third of the page.
- Type sizes and spacing follow `html-layout.md`: 11 pt body text, with the
  name and headings only slightly larger.

## Cover letter layout

- The user's full name as the first line and the same contact line as the
  resume. No date line unless `voice.md` asks for one.
- Greeting to a named person only if the posting names one; otherwise
  "Hello," or the `voice.md` choice.
- Three to five short paragraphs within the `voice.md` length (default
  250 to 350 words, one page): why this role, one or two examples told as
  stories, anything the situation fields call for, a short close that
  offers how the user would help. How to choose and tell the examples is
  in `cover-letter.md` (decision 026).
- Name the target employer and job title exactly as the posting does.
- Sign off with `preferred_name` if set, else `full_name`.
- Each paragraph is its own `p` with space after it, and the text is 11 pt.
  The name is not larger than 15 pt. Both follow `html-layout.md`.

## Files

Write the draft first as clean HTML (headings, paragraphs, lists only, with
the inline styles in `html-layout.md`) and as plain text. Bare tags with no
styles import into Google Docs with oversized headings and no paragraph
spacing. The HTML becomes the Google Doc; the PDF is exported from
the Google Doc so fonts are embedded and the text extracts cleanly. Do not
build PDFs with a script and standard fonts.
