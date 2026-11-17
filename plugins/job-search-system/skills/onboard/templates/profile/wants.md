# What I want

<!--
This file decides what counts as a good lead for you. The scorecard
(decision 011) reads its meaning from here, so be specific. Onboarding fills
it in from a short interview. Edit it whenever your thinking changes.

Two kinds of content:
- The "Hard filters" block is read by the overnight collector before any
  scoring. Anything that hits a hard filter is dropped before it reaches the
  Leads tab. The reason is kept in the hidden Seen tab and counted in the Run
  Log, so it is not looked at again. Keep it in the fenced yaml block so the
  script can parse it.
- Everything else is read by the model when it scores and drafts.

Your situation (experience, level, career change, gap) lives in
profile.yaml, not here.
-->

## Interests

<!-- Kinds of work, problems, industries or missions that pull you in. Most
important first. -->

- Interest

## Drains

<!-- Things that wear you down. These feed the Drains dimension of the
scorecard: a posting that shows several of these scores low even if
everything else fits. Be concrete ("rotating weekend shifts", not "bad
hours"). -->

- Drain

## Logistics

- Home base: City, Region
- Work mode: remote / hybrid / on-site, and how many on-site days you will do
- Longest commute you will do, one way: N minutes
- Schedule: hours and days you can work
- On-call: none / occasional / fine
- Travel: how much is fine
- Relocation: no / yes, to where

## Pay

<!-- Floors are the least you would accept, not what you hope for. Hourly
math: hourly rate x 2,080 hours = yearly equivalent. Contract and part-time
roles are compared on the same yearly basis unless you say otherwise below. -->

- Salary floor: $N a year
- Hourly floor: $N an hour
- Notes: for example, how you treat contract roles, benefits, or a posting
  with no pay listed

## Level

<!-- What level of role you want, in your own words, and anything you want
to avoid about level. -->

- Level

## Rule-outs

<!-- Things that make a posting a no, explained in words. The machine-readable
version is the Hard filters block below; keep the two in step. -->

- Rule-out

## Excluded employers

<!-- Employers you will not apply to, for any reason. You do not need to give
reasons. These also go in the Hard filters block. -->

- Employer

## How to score me

<!--
Plain-language meaning of each scorecard dimension for you. 2 is a strong
yes, 1 is mixed or unknown, 0 is a strong no. The scoring steps use these
words, so write them the way you would explain them to a friend helping you
search. The full scale is in templates/tracker-schema.yaml.
-->

- Wants match: what makes a role a 2 for you, and what makes it a 0
- Evidence: which of your confirmed facts should count most
- Logistics: what is a 2 and what is a 0 on location, schedule and mode
- Pay: 2 if at or above the floor, 1 if unknown or slightly under, 0 if
  clearly under. Change this if you want something different.
- Drains: how many of your drains, or which ones, push a role to 0
- Odds: what makes you a realistic candidate, and what makes you a long shot

## Hard filters

```yaml
# Read by the collector. Matching is case-insensitive.
excluded_employers: []        # Exact employer names, plus common variants.
title_blocklist: []           # Words or phrases. A title containing any of these is dropped.
title_allowlist: []           # Optional. If set, a title must contain one of these to pass.
required_work_modes: []       # Any of: remote, hybrid, onsite. Empty means any.
locations:                    # The collector does not geocode. max_distance_miles is passed to
                              # sources that can filter by distance (Adzuna). Elsewhere it is
                              # not enforced; a posting in another state scores low on Logistics.
  home: ""                    # City, Region
  max_distance_miles: 0       # 0 means no distance filter.
pay_floor_yearly: 0           # Drops a posting only when its listed top of range is below this.
                              # Postings with no pay listed pass and are scored as unknown.
max_posting_age_days: 30      # How old a posting can be. This is the posting's age,
                              # not anything about you.
other_blocked_phrases: []     # Phrases in the snippet that rule a posting out.
```
