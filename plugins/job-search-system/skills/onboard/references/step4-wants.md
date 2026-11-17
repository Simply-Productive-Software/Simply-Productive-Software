# Step 4: Wants and situation

Fills `wants.md`, the contact and situation parts of `profile.yaml`, and
the basics in `answers.md`. Read each template's comments first; they say
what each field is for.

Ask at the pace the user chose (see "How to run the interview steps" in
`SKILL.md`; ask them if they have not chosen yet). Keep each question
short. Most people know what they do not want better than what they want,
so ask both.

## profile.yaml

1. **Contact**: full name as it should appear on a resume, preferred name,
   email, phone, city, region, country, time zone, links. Then which of
   these should appear on drafts (`show_on_resume`). A street address is
   never used.
2. **Situation** (decision 015). Never ask for age; these fields replace it:
   - About how many years of work count toward the roles you want?
   - What was your most recent level? (individual contributor, senior
     specialist, team lead, manager, manager of managers, or their words)
   - What levels are you aiming for? Would you take a role below your
     recent level?
   - Is this a change of field or function? From what, to what?
   - Is there a gap of six months or more in the last ten years? If so,
     dates, and one or two sentences you would be comfortable seeing in a
     cover letter. Blank is fine: drafts then do not mention it.
3. Leave `modules.experienced_candidate` on `auto` unless the user asks.

## wants.md

Core uses `wants.md` to shape the angle of a cover letter. It never uses it
to rank, judge or refuse a job (decision 031). So two sections matter and
the rest are optional. Ask the two that matter, then offer the others once:
"There are a few more sections (what drains you, logistics, pay, rule-outs,
employers to avoid). Core does not use them to judge jobs, but they stay in
your profile. Want to fill them in now or skip them?" Skip means leave the
template text as it is.

1. **Interests**: the kinds of work, problems, industries or missions that
   pull them in, most important first. Ask for examples of roles they would
   say yes to.
2. **Level**: what they want and what to avoid.

Optional, only if they want them:

3. **Drains**: what wears them down. Push for concrete wording ("rotating
   weekend shifts", not "bad hours").
4. **Logistics**: home base, work modes and on-site days, longest one-way
   commute in minutes, schedule, on-call, travel, relocation.
5. **Pay**: salary floor and hourly floor, as the least they would accept.
6. **Rule-outs**: what makes a posting a no.
7. **Excluded employers**: any employer they will not apply to. No reasons
   needed.

Leave the "How to score me" and "Hard filters" sections of the template as
they are.

## answers.md

Ask for short answers to the template's questions (why looking, why this
kind of role, salary expectations, work authorization, start date,
relocation, tell us about yourself, and the gap if one is listed). Any
fact in an answer must already be a confirmed line in `facts.md`; if it is
not, add and confirm it there first. The user can skip any question.

## Save

Save `profile.yaml`, `wants.md` and `answers.md`. Read `profile.yaml` back
and confirm it parses as YAML.
