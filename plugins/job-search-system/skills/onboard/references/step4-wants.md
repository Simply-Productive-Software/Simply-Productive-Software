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

Go section by section:

1. **Interests**: the kinds of work, problems, industries or missions that
   pull them in, most important first. Ask for examples of roles that would
   be a yes.
2. **Drains**: what wears them down. Push for concrete wording ("rotating
   weekend shifts", not "bad hours"). Ask which, if any, are deal-breakers
   on their own, and mark those `(deal-breaker)`.
3. **Logistics**: home base, work modes and on-site days, longest one-way
   commute in minutes, schedule, on-call, travel, relocation.
4. **Pay**: salary floor and hourly floor, as the least they would accept.
   Show the hourly math (rate x 2,080). Ask how to treat contract roles and
   postings with no pay listed.
5. **Level**: what they want and what to avoid.
6. **Rule-outs**: what makes a posting a no.
7. **Excluded employers**: any employer they will not apply to. No reasons
   needed.
8. **How to score me**: write the six lines yourself, from their earlier
   answers and confirmed facts, and save them in `wants.md` without showing
   them. Do not show the six lines, the 0 to 2 scale, or the word
   "dimension". Reviewing rules they have never seen is hard, and four of
   the six only restate what they already told you (Wants match, Logistics,
   Pay, Drains). Instead:

   1. Say in two sentences what scoring is for: "I rate each job on a few
      things, like how well it fits what you want, your commute, the pay and
      whether you could get it, so the best ones rise to the top and you can
      see why. Later you will rate some real postings and I will compare, so
      we can fix anything that is off."
   2. Ask the two things only they can judge, in plain questions, with your
      guess in front of them to say yes to or change (at the pace they
      chose):
      - **Strongest proof (Evidence):** "When a job asks for experience,
        which of your results should I treat as your best proof?" Offer the
        three to five confirmed results you would pick, and say which
        skills you would count lightly.
      - **Realistic shots (Odds):** "Which kinds of roles are a solid shot
        for you, which are a stretch, and which are a long shot?" Offer a
        sorting from their level, target roles and confirmed skills.
   3. Put their answers into the Evidence and Odds lines in their words.
   4. Say once: "The rest of the scoring comes from what you already told
      me. If you want to see the exact rules, ask and I will show them, or
      open `wants.md`."

   If they ask to see the scoring lines, show them and let them edit. A 2
   is a strong yes, 1 is mixed or unknown and 0 is a strong no; say that
   when you show them.
9. **Hard filters**: build the yaml block from Rule-outs, Excluded
   employers (with common variants of each name), Logistics and Pay. Keep
   it conservative: only things that are a no every time. Explain that a
   hard filter drops a posting before anyone sees it, so anything borderline
   belongs in Drains or Rule-outs instead, where it lowers the score but
   stays visible.

## answers.md

Ask for short answers to the template's questions (why looking, why this
kind of role, salary expectations, work authorization, start date,
relocation, tell us about yourself, and the gap if one is listed). Any
fact in an answer must already be a confirmed line in `facts.md`; if it is
not, add and confirm it there first. The user can skip any question.

## Save

Save `profile.yaml`, `wants.md` and `answers.md`. Read `profile.yaml` back
and confirm it parses as YAML, and that the Hard filters block in
`wants.md` parses too.
