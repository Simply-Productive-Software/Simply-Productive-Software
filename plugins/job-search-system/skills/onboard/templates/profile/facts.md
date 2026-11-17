# Career facts

<!--
This file is the only source of truth for what a draft can say about you
(decision 014). The drafter may use a fact only if its line is marked
[confirmed]. The reviewer and the code checks trace every claim in a draft
back to a confirmed line here, by its ID.

How lines work:
- One fact per line, in this shape:
    - [confirmed] F-001 | Employer | Title | Detail
  or, for facts not tied to one employer:
    - [confirmed] F-040 | - | - | Detail
- [unconfirmed] means "found in an old resume or profile, not yet checked
  with you". Drafts never use these. Onboarding confirms them with you a few
  at a time, and you can change the marker yourself.
- IDs never get reused. If a fact is wrong, fix it or delete the line. If it
  is replaced, give the new version a new ID.
- Put numbers exactly as you want them said. If the code check finds a
  number, date, title or employer in a draft that is not in a confirmed line,
  the draft is blocked.
- Graduation years and early-career dates are optional. Leave them out if
  you would rather they not appear. Drafts never add dates you did not give.
-->

## Roles

<!--
One line per role. Detail holds the dates as YYYY-MM to YYYY-MM (or
"present") and the location if you want it shown.
-->

- [unconfirmed] F-001 | Employer | Title | YYYY-MM to YYYY-MM, City, Region

## Results and scope

<!--
What you did and what changed because of it. Group by employer. Include
scope (team size, budget, volume) only where you can stand behind the
number.
-->

### Employer

- [unconfirmed] F-010 | Employer | Title | What you did, and the result

## Skills and tools

<!--
Only skills you would be comfortable being tested on in an interview. Note
the level in plain words if it matters ("daily use", "basic", "used on one
project in 2019"). A draft never drops a limiting level like "basic",
unless you set a Skills intro line in Wording rules below (decision 024),
which then carries the qualifier for every skill in the list. Put the
level in the first sentence of the fact when you have no intro line.

Each skill sits under a ### heading that names its category. The category
is part of the confirmed fact (decision 023): a draft lists a skill only
under the category it sits under here, and the code check blocks a draft
that puts it anywhere else.

Use the category labels from your preset (skills_preset in profile.yaml;
the presets are in shared/skill-categories.yaml). Leave out categories you
have nothing for. You may add your own category; it is a ### heading like
any other. There is no soft-skill category, and certifications stay in the
section below.
-->

### Category

- [unconfirmed] F-030 | - | - | Skill or tool, with level

## Education, licenses and certifications

- [unconfirmed] F-040 | - | - | Credential, institution, year (year optional)

## Other facts

<!--
Volunteer work, awards, languages, publications, anything else a draft
might use.

Names a reader outside your employer will not know (decision 025): add a
line for each internal product, feature, project, team or tool name, and
for any term that could mean more than one thing. Write it as
"Name is <what it is, in one line>", with the employer in the employer
field. Drafts say what the name is the first time it appears, in your
words, then use the name alone. Example:
  - [unconfirmed] F-051 | Employer | - | Harvest is a tool our
    clinics use to schedule pharmacy deliveries
-->

- [unconfirmed] F-050 | - | - | Fact

## Wording rules

<!--
Fixed rules for how certain facts are phrased. The drafter follows these and
the reviewer checks them. Examples:
  - Say "100+ hires", not "hundreds of hires".
  - Call the 2022 project a pilot, not a launch.

Optional skills intro (decision 024). One line, exactly this shape:
  - Skills intro: Experience with:
The resume then prints that text under the Skills heading, and skills are
listed as plain names with no level words. Leave the line out and drafts
print a level such as "basic" next to the skill instead.

Keep rules in plain sentences. The code checks read the resume text, so a
rule that asks for parentheses or semicolons in a skills line, or for a
category label that is not a heading above, will block every draft.
-->

- Rule

## Do not claim

<!--
Things you do not have, or have only lightly, that a posting might tempt a
drafter to imply. The reviewer blocks any draft that claims these.
Example: "No people management. Led projects, did not manage staff."
-->

- Item
