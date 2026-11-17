# HTML layout for the resume and cover letter

This file says how `resume.html` and `cover_letter.html` look. It does not
say what they contain; `writing-rules.md` does that.

## Why every element carries its own style

The HTML becomes a Google Doc, and the PDF is exported from that doc. Google's
HTML import gives bare tags its own defaults: a 24 pt name, 18 pt section
headings, 14 pt role lines, and no space between paragraphs. Those defaults
are what made drafts look wrong. So every element gets an inline `style`
attribute with the values below. Do not rely on a `<style>` block or
classes; the import does not apply them reliably.

## Sizes and spacing

| Element | Tag | Size | Weight | Space above / below |
| --- | --- | --- | --- | --- |
| Name (first line) | `h1` | 15 pt | bold | 0 / 2 pt |
| Contact line | `p` | 11 pt | normal | 0 / 10 pt |
| Section heading (resume) | `h2` | 13 pt | bold | 12 / 4 pt |
| Role line (resume) | `h3` | 12 pt | bold | 8 / 2 pt |
| Paragraph (summary, skills, cover letter, greeting, sign-off) | `p` | 11 pt | normal | 0 / 8 pt |
| List | `ul` | n/a | n/a | 0 / 6 pt |
| Bullet | `li` | 11 pt | normal | 0 / 2 pt |

Body text is always 11 pt. Headings are slightly larger, in steps of 1 to 2
pt, and never more than 15 pt. All text is Arial.

## Rules

- One `p` per paragraph. Do not use `<br>` or empty paragraphs for space.
- Use only `h1`, `h2`, `h3`, `p`, `ul` and `li`, plus `u` for an
  underlined skills category label (see Skills below). No tables, divs,
  spans, images or links styled as buttons.
- Put a role's title, employer, location and dates in one `h3`, separated
  by commas. It may wrap onto a second line.
- Do not change a size or margin to make a draft fit. If the resume is over
  the length in `voice.md`, cut text instead.
- The style strings below are exact. Copy them.

## Style strings

```
h1       font-family:Arial,sans-serif;font-size:15pt;font-weight:bold;margin:0 0 2pt 0;
contact  font-family:Arial,sans-serif;font-size:11pt;margin:0 0 10pt 0;
h2       font-family:Arial,sans-serif;font-size:13pt;font-weight:bold;margin:12pt 0 4pt 0;
h3       font-family:Arial,sans-serif;font-size:12pt;font-weight:bold;margin:8pt 0 2pt 0;
p        font-family:Arial,sans-serif;font-size:11pt;margin:0 0 8pt 0;
ul       margin:0 0 6pt 0;
li       font-family:Arial,sans-serif;font-size:11pt;margin:0 0 2pt 0;
```

## Skills

Each category is one `li`. The label is wrapped in `<u>` and the colon
follows it: `<li style="[li]"><u>Languages</u>: Go, Python</li>`. If
`facts.md` has a `Skills intro:` line (decision 024), it is one `h3`
directly under the Skills `h2`, before the `ul`. The `u` tag takes no style
attribute.

## Resume skeleton

```html
<html><body>
<h1 style="[h1]">Full Name</h1>
<p style="[contact]">City, ST | phone | email | link</p>
<h2 style="[h2]">Summary</h2>
<p style="[p]">...</p>
<h2 style="[h2]">Experience</h2>
<h3 style="[h3]">Title, Employer, Location, Dates</h3>
<ul style="[ul]">
<li style="[li]">...</li>
</ul>
</body></html>
```

## Cover letter skeleton

```html
<html><body>
<h1 style="[h1]">Full Name</h1>
<p style="[contact]">City, ST | phone | email | link</p>
<p style="[p]">Hello,</p>
<p style="[p]">First paragraph.</p>
<p style="[p]">Sign-off name</p>
</body></html>
```

Replace each `[name]` with its style string from the list above.

## Checked on

Tested on 2026-11-12 by importing the fictional Marisol Teague drafts into a
Google Doc and exporting the PDF. Measured in the PDF: name 15 pt, section
headings 13 pt, role lines 12 pt, body 11 pt, resume on one page, a visible
gap between cover letter paragraphs.
