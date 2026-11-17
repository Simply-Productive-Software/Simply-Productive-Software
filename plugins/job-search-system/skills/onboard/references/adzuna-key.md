# Get a free Adzuna key

Adzuna is a job search site with a free developer interface. With a key, the
overnight collector searches Adzuna for jobs near you and adds new ones to
your tracker. This is optional. Without it, your job alerts and employer
watchlist still work.

Time: about five minutes. Cost: free, no card. This guide is for the user
and for the onboard skill, which walks the user through it one step at a
time (step 6, `step6-sources.md`).

## 1. Sign up

Open the signup page:

https://developer.adzuna.com/signup

The form asks for:

- **Username, email and password.** Choose your own.
- **Organisation or group name, and website.** Both are required. Use your
  own name and a site that is really yours, such as your LinkedIn profile.
- **Intended use.** Choose the personal job search option.
- **Average monthly visitors.** Choose the lowest range (0 to 5,000).
- **Primary market.** Pick where you are searching (for example North
  America).
- **Industry.** Optional.

Agree to the terms and submit. If Adzuna emails you a confirmation link,
open it first.

## 2. Find your two values

Adzuna gives you two values, an **application ID** (`app_id`) and an
**application key** (`app_key`). You need both. They are shown in your
Adzuna developer account after you sign up. If you cannot find them, look
for a page or section about your API key or application, and check your
email.

Keep them private. Do not paste them into the chat, into a file in Drive,
or anywhere public.

## 3. Enter them in your tracker

1. Open your tracker sheet.
2. Choose **Job Search**, then **Set API keys**.
3. Google shows three prompts, one after another:
   1. *Anthropic API key (optional)*: leave it empty and continue.
   2. *Adzuna app id*: paste your application ID.
   3. *Adzuna app key*: paste your application key.
4. You will see "Saved in this script's private properties, not in the
   sheet." The values are stored with the script, not in a cell.

The first time, Google may ask you to authorize the script again. That is
expected.

## 4. Check it

Choose **Job Search**, then **Check configuration**. The line for the
`adzuna` source should say `ON`. Warnings about empty files are normal at
this stage. If it says `off`, the keys were not saved or the searches are
missing from `sources.yaml`.

## Limits and terms

- Adzuna's terms allow personal job searching with the API. Each person
  should use their own key for their own search.
- The free key is meant for trying the service out. The limit depends on
  your plan, is shown in your Adzuna account, and Adzuna can change it.
- Ongoing business use, or using the data in a product or to generate
  leads, needs a licence from Adzuna. This system is for your own search.

Terms: https://developer.adzuna.com/docs/terms_of_service

## If something goes wrong

- **Wrong value pasted.** Run **Set API keys** again and re-enter all
  three prompts. Leaving a prompt empty keeps the value already saved.
- **Check configuration still says `off`.** Confirm `sources.yaml` has at
  least one Adzuna search and `enabled: true`.
- **Searches stop working later.** Your key may have hit its limit or been
  turned off. Sign in at developer.adzuna.com and check your account.
- **You would rather skip it.** Leave the prompts empty. You can come back
  to this later.
