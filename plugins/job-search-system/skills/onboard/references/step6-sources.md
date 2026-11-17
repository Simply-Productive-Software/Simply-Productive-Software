# Step 6: Sources

Fills `sources.yaml` so the overnight collector has places to look. Read the
template's comments first. Suggest sources from the user's field, location
and work modes; do not assume one field's boards fit another.

## 1. Job alert emails (most users)

Alerts from big boards catch the most postings for the least setup.

1. Ask which boards they already get alerts from, and which ones are used
   in their field (search if unsure, and say which you found).
2. For boards they want, walk them through creating an alert with their
   key titles and location. They do this on the board's site; you cannot.
3. Walk them through a Gmail filter so these emails get a label:
   - In Gmail search, enter `from:(<sender 1> OR <sender 2>)` with the
     senders' addresses (look at one alert email to find the address).
   - Click "Show search options" then "Create filter", tick "Apply the
     label", create the label `job-alerts` (or the label they prefer), and
     tick "Also apply filter to matching conversations".
   If the Gmail connector can create labels, you can create the label for
   them; the filter itself they make in Gmail.
4. Fill `gmail_alerts`: `enabled: true`, the label, and `sender_domains`
   (for example `linkedin.com`, `indeed.com`). The collector has parsers for
   some senders only; it shows which in Job Search > Check configuration.
   Alerts from other senders are still kept but read less well.

## 2. Job search APIs (optional)

- **Adzuna** covers many countries with keyword and distance search. It
  needs a free key, so offer it: "Adzuna is a job site with a free key.
  Setting it up takes about five minutes. Want to do it now?" If they say
  yes, walk them through `adzuna-key.md` in this folder, one step at a
  time and in your own words, not by pasting the whole guide:
  1. Sign up (the form fields, and what to put in the required ones).
  2. Find the application ID and application key.
  3. Enter them with Job Search > Set API keys. Say that the first prompt
     asks for an Anthropic key, which they leave empty, and that the next
     two are the Adzuna ID and key.
  4. Run Job Search > Check configuration and tell you what Adzuna shows.
  After each step, ask them to tell you when it is done. Never ask them to
  paste a key into the chat. If they do, tell them to keep it out of the
  chat, and carry on without using it; suggest they get a new key from
  their Adzuna account if they are worried. If they would rather skip,
  leave Adzuna off and note it so you can offer it again later. Free terms
  cover personal use. Add one or two searches (`what`, `where`,
  `distance_miles`) once the key is set, or now if they plan to.
- **USAJOBS** for US federal roles, if relevant to them. Same key handling.

## 3. Employer watchlist

Ask for employers they would especially like to work for. For each:

1. Find the careers page.
2. Work out the applicant tracking system from the job links:
   `boards.greenhouse.io/<board>` or `job-boards.greenhouse.io/<board>` is
   Greenhouse; `jobs.lever.co/<company>` is Lever;
   `jobs.ashbyhq.com/<name>` is Ashby; `<tenant>.wd<N>.myworkdayjobs.com`
   is Workday. Otherwise `other`, or `unknown` if you cannot tell.
3. Add an entry with `name`, `careers_url`, `ats`, `board` (when known) and
   optional title `keywords`.

Tell them the collector reads Greenhouse and Lever boards every night, and
the scout skill checks the others when asked.

## 4. Feeds

Remote job feeds (`remoteok`, `weworkremotely`, `himalayas`) are planned but
not all built; the collector shows unbuilt ones as STUB. Turn one on only if
the user works remotely in a field those feeds cover.

## Save

Save `sources.yaml` and confirm it parses as YAML. If the tracker is linked,
ask the user to run Job Search > Check configuration and tell you any
warnings.
