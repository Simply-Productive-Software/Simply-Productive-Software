"""The individual checks. Each takes a Context and returns (blockers, warnings).

A blocker is a dict with the keys of a blocker in
shared/schemas/review-result.json: check, document, quote, detail, fix.
"""
import re

import lib
import validate as validate_mod

DOCS = ("resume", "cover_letter", "answers")


def blocker(check, document, detail, quote=None, fix=None):
    return {"check": check, "document": document, "quote": quote,
            "detail": detail, "fix": fix}


def warning(check, detail):
    return {"check": check, "detail": detail}


class Context:
    """Everything the checks read, loaded once."""

    def __init__(self, workdir):
        self.dir = workdir
        self.text = {}
        for d in DOCS:
            t = lib.read_text(workdir / f"{d}.txt")
            if t is not None:
                self.text[d] = t.lstrip("﻿")
        self.pdfs = {d: workdir / f"{d}.pdf" for d in ("resume", "cover_letter")
                     if (workdir / f"{d}.pdf").is_file()}
        self.facts_raw = lib.read_text(workdir / "facts.md")
        self.voice_raw = lib.read_text(workdir / "voice.md")
        self.profile_raw = lib.read_text(workdir / "profile.yaml")
        self.posting_md = lib.read_text(workdir / "posting.md")
        self.posting_json = None
        self.posting_json_error = None
        pj = workdir / "posting.json"
        if pj.is_file():
            try:
                import json
                self.posting_json = json.loads(pj.read_text(encoding="utf-8"))
            except ValueError as e:
                self.posting_json_error = f"posting.json is not valid JSON: {e}"
        self.lead = lib.read_json(workdir / "lead.json") or {}
        self.claims = lib.read_json(workdir / "claims.json")
        self._facts = None
        self._voice = None
        self._profile = None

    @property
    def facts(self):
        if self._facts is None:
            self._facts = lib.parse_facts(self.facts_raw or "")
        return self._facts

    @property
    def voice(self):
        if self._voice is None:
            self._voice = lib.parse_voice(self.voice_raw or "")
        return self._voice

    @property
    def profile(self):
        if self._profile is None:
            self._profile = lib.parse_profile(self.profile_raw or "")
        return self._profile

    @property
    def contact(self):
        return self.profile.get("contact") or {}


# ----------------------------------------------------------------- scanning

MONTH = (r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|"
         r"sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)")
MONTH_NUM = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7,
             "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}

DATE_PATTERNS = [
    (re.compile(r"(?<![A-Za-z])" + MONTH + r"\.?\s+(?:\d{1,2}(?:st|nd|rd|th)?,?\s+)?((?:19|20)\d{2})(?!\d)", re.I),
     lambda m: f"{m.group(2)}-{MONTH_NUM[m.group(1)[:3].lower()]:02d}"),
    (re.compile(r"(?<![\d/])(0?[1-9]|1[0-2])/((?:19|20)\d{2})(?!\d)"),
     lambda m: f"{m.group(2)}-{int(m.group(1)):02d}"),
    (re.compile(r"(?<![\d-])((?:19|20)\d{2})-(0[1-9]|1[0-2])(?![\d-])"),
     lambda m: f"{m.group(1)}-{m.group(2)}"),
    (re.compile(r"(?<![A-Za-z0-9$,.])(?:FY\s?)?((?:19|20)\d{2})(?!\d|,\d|\.\d|\s?%)"),
     lambda m: m.group(1)),
]

NUM_RE = re.compile(
    r"(?<![A-Za-z0-9.$,])(\$)?(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?"
    r"(?:\s?(k|m|b)\b|\s(thousand|million|billion)\b)?"
    r"(\s?%|\s(?:percent|per cent)\b)?(?![A-Za-z0-9])", re.I)
HEDGE_RE = re.compile(r"(about|roughly|approximately|around|nearly|almost|~)\s*\$?$", re.I)
MULT = {"k": 1e3, "thousand": 1e3, "m": 1e6, "million": 1e6, "b": 1e9, "billion": 1e9}


def _blank(text, span):
    return text[:span[0]] + " " * (span[1] - span[0]) + text[span[1]:]


def scrub(text, contact_values=()):
    """Remove contact details and list markers, keeping character positions."""
    for rx in (EMAIL_RE_, URL_RE_, PHONE_RE_, STREET_RE):
        for m in list(rx.finditer(text)):
            text = _blank(text, m.span())
    for v in contact_values:
        if v:
            pat = re.escape(str(v))
            if str(v)[0].isalnum():
                pat = r"(?<![A-Za-z0-9])" + pat
            if str(v)[-1].isalnum():
                pat = pat + r"(?![A-Za-z0-9])"
            text = re.sub(pat, lambda m: " " * len(m.group(0)), text, flags=re.I)
    return re.sub(r"(?m)^(\s*)\d+[.)](?=\s)", lambda m: " " * len(m.group(0)), text)


EMAIL_RE_, URL_RE_, PHONE_RE_ = lib.EMAIL_RE, lib.URL_RE, lib.PHONE_RE


def scan(text):
    """Find dates and numbers. Returns (dates, nums).
    dates: list of (token as written, normalized 'YYYY' or 'YYYY-MM').
    nums: list of (token as written, value, hedged)."""
    dates = []
    work = text
    for rx, norm in DATE_PATTERNS:
        for m in list(rx.finditer(work)):
            dates.append((m.group(0).strip(), norm(m)))
            work = _blank(work, m.span())
    nums = []
    for m in NUM_RE.finditer(work):
        dollar, whole, frac, suf1, suf2, pct = m.groups()
        suffix = (suf1 or suf2 or "").lower()
        if suf1 and not dollar:
            continue  # 340B, 5K: an identifier, not a quantity
        value = float(whole.replace(",", "") + (frac or ""))
        if suffix:
            value *= MULT[suffix]
        hedged = bool(HEDGE_RE.search(work[max(0, m.start() - 16):m.start()]))
        nums.append((m.group(0).strip(), round(value, 6), hedged))
    return dates, nums


# ------------------------------------------------------------- facts_trace

def _fact_index(facts):
    idx = {"conf_nums": {}, "unconf_nums": {}, "conf_months": set(), "conf_years": set(),
           "unconf_dates": {}}
    for f in facts:
        dates, nums = scan(lib.fact_text(f))
        conf = f["status"] == "confirmed"
        for tok, v, h in nums:
            d = idx["conf_nums" if conf else "unconf_nums"]
            d.setdefault(v, []).append((f["id"], h))
        for tok, n in dates:
            if conf:
                if len(n) == 7:
                    idx["conf_months"].add(n)
                idx["conf_years"].add(n[:4])
            else:
                idx["unconf_dates"].setdefault(n, []).append(f["id"])
    return idx


def _exempt(ctx):
    """Numbers and dates allowed without a fact: the target job title and
    employer, and the capture date and deadline of the posting."""
    nums, dates = set(), set()
    pj = ctx.posting_json or {}
    for s in (ctx.lead.get("title"), ctx.lead.get("employer"), pj.get("title"), pj.get("employer")):
        d, n = scan(s or "")
        nums.update(v for _, v, _ in n)
        dates.update(x for _, x in d)
    extra = []
    m = re.search(r"^Captured:\s*(\d{4}-\d{2}-\d{2})", ctx.posting_md or "", re.M)
    if m:
        extra.append(m.group(1))
    if pj.get("deadline"):
        extra.append(pj["deadline"])
    for e in extra:
        dates.update({e[:4], e[:7]})
    return nums, dates


ROLE_HEADINGS = {"experience", "work experience", "professional experience",
                 "employment", "employment history", "work history", "relevant experience"}
OTHER_HEADINGS = {"summary", "professional summary", "profile", "skills", "technical skills",
                  "education", "certifications", "certificates", "licenses", "projects",
                  "volunteer", "volunteering", "awards", "languages", "additional information",
                  "education and certifications", "licenses and certifications"}


def _heading_key(line):
    return re.sub(r"[^a-z ]", "", line.lower().replace("&", "and")).strip()


def _experience_lines(text):
    """Non-empty lines of the experience section; the whole text if there is
    no experience heading."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    start = None
    for i, ln in enumerate(lines):
        if _heading_key(ln) in ROLE_HEADINGS:
            start = i + 1
            break
    if start is None:
        return lines
    out = []
    for ln in lines[start:]:
        if _heading_key(ln) in OTHER_HEADINGS:
            break
        out.append(ln)
    return out


def _is_range_line(line):
    if re.match(r"^[-*\u2022\u2013]\s", line):
        return False  # a bullet, not a role header
    dates, _ = scan(line)
    if not dates:
        return False
    return len(dates) >= 2 or bool(re.search(r"\b(present|current|now)\b", line, re.I))


def check_facts_trace(ctx, docs):
    blockers, warnings = [], []
    facts = ctx.facts
    idx = _fact_index(facts)
    ex_nums, ex_dates = _exempt(ctx)
    contact_vals = [ctx.contact.get(k) for k in ("full_name", "preferred_name", "email", "phone", "city", "region")]
    contact_vals += [v for v in (ctx.contact.get("links") or {}).values()]
    target_emp = lib.norm_employer(ctx.lead.get("employer", ""))

    conf_roles = [f for f in facts if lib.is_role(f) and f["status"] == "confirmed" and f["employer"] and f["title"]]
    unconf_roles = [f for f in facts if lib.is_role(f) and f["status"] == "unconfirmed" and f["employer"] and f["title"]]
    conf_emps = {lib.norm_employer(f["employer"]) for f in facts if f["status"] == "confirmed" and f["employer"]}
    unconf_only = {}
    for f in facts:
        e = lib.norm_employer(f["employer"]) if f["employer"] else ""
        if f["status"] == "unconfirmed" and e and e not in conf_emps and e != target_emp:
            unconf_only.setdefault(e, []).append(f["id"])

    for doc in docs:
        text = ctx.text[doc]
        clean = scrub(text, contact_vals)
        dates, nums = scan(clean)
        seen = set()

        def add(b):
            k = (b["check"], b["quote"])
            if k not in seen:
                seen.add(k)
                blockers.append(b)

        for tok, n in dates:
            if n in ex_dates or n[:4] in ex_dates and len(n) == 4:
                continue
            if len(n) == 7:
                ok = n in idx["conf_months"]
            else:
                ok = n in idx["conf_years"]
            if ok:
                continue
            ids = idx["unconf_dates"].get(n) or []
            if ids:
                add(blocker("unconfirmed_fact", doc, f"Date appears only in unconfirmed fact {', '.join(sorted(set(ids)))}.", tok))
            else:
                add(blocker("claim_not_traced", doc, "Date is not in any confirmed fact.", tok,
                            "Remove it, or ask the user to confirm a fact that has it."))

        for tok, v, hedged in nums:
            if v in ex_nums:
                continue
            conf = idx["conf_nums"].get(v)
            if conf:
                if any(not h for _, h in conf) or hedged:
                    continue
                ids = ", ".join(sorted({i for i, _ in conf}))
                add(blocker("claim_not_traced", doc,
                            f"Fact {ids} gives this number as approximate; the draft states it exactly.", tok,
                            "Write it with the same hedge as the fact (for example, 'about')."))
                continue
            unc = idx["unconf_nums"].get(v)
            if unc:
                ids = ", ".join(sorted({i for i, _ in unc}))
                add(blocker("unconfirmed_fact", doc, f"Number appears only in unconfirmed fact {ids}.", tok))
            else:
                add(blocker("claim_not_traced", doc, "Number is not in any confirmed fact.", tok,
                            "Remove it, or ask the user to confirm a fact that has it."))

        if doc == "resume":
            lines = _experience_lines(clean)
            for i, ln in enumerate(lines):
                if not _is_range_line(ln):
                    continue
                window = " ".join(lines[max(0, i - 1): i + 2])
                if any(lib.contains_phrase(window, lib.norm_employer(r["employer"])) and
                       lib.contains_phrase(window, r["title"]) for r in conf_roles):
                    continue
                if any(lib.contains_phrase(window, lib.norm_employer(r["employer"])) and
                       lib.contains_phrase(window, r["title"]) for r in unconf_roles):
                    add(blocker("unconfirmed_fact", doc, "Role matches only an unconfirmed role line.", ln))
                    continue
                same_emp = [r for r in conf_roles if lib.contains_phrase(window, lib.norm_employer(r["employer"]))]
                if same_emp:
                    titles = "; ".join(sorted({r["title"] for r in same_emp}))
                    add(blocker("claim_not_traced", doc,
                                f"Title does not match the confirmed title for this employer ({titles}).", ln,
                                f"Use the confirmed title: {titles}."))
                else:
                    add(blocker("claim_not_traced", doc, "Employer and title are not in any confirmed role.", ln))

        for emp, ids in unconf_only.items():
            q = lib.find_phrase(clean, emp)
            if q:
                add(blocker("unconfirmed_fact", doc,
                            f"Employer appears only in unconfirmed fact {', '.join(sorted(set(ids)))}.", q))
    return blockers, warnings


# ------------------------------------------------------------------ target

def _first_name_region(text):
    """Greeting line plus the paragraph after it."""
    lines = text.splitlines()
    g = None
    for i, ln in enumerate(lines[:20]):
        if re.match(r"\s*(dear|hello|hi|greetings|to whom|good (morning|afternoon))\b", ln, re.I):
            g = i
            break
    if g is None:
        paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
        return paras[1] if len(paras) > 1 else (paras[0] if paras else "")
    out = [lines[g]]
    started = False
    for ln in lines[g + 1:]:
        if ln.strip():
            out.append(ln)
            started = True
        elif started:
            break
    return "\n".join(out)


NAME_RE = (r"((?:[A-Z][\w&'’.-]*)(?:\s+(?:[A-Z][\w&'’.-]*|of|for|and|&)){0,6})")
GREETING_RE = re.compile(r"^(dear|hello|hi|to whom)\b", re.I)
TRIGGER_RE = re.compile(r"\b(appl(?:y|ying|ication)|position|role|opening|opportunity|interest(?:ed)?|join(?:ing)?)\b", re.I)
CONNECT_RE = re.compile(r"(?:\bat|\bwith|\bjoin(?:ing)?|\bapply(?:ing)? to|\bto join)\s+(?:the\s+)?" + NAME_RE)


def check_target(ctx, docs):
    blockers = []
    if "cover_letter" not in ctx.text:
        return blockers, []
    text = ctx.text["cover_letter"]
    emp = ctx.lead.get("employer", "")
    title = ctx.lead.get("title", "")
    posting = ctx.posting_md or ""

    opening = next((s.strip()[:200] for s in re.split(r"(?<=[.!?])\s+|\n", _first_name_region(text)) if s.strip() and not GREETING_RE.match(s.strip())), None)

    emp_ok = lib.contains_phrase(text, lib.norm_employer(emp)) or lib.contains_phrase(text, emp)
    if not emp_ok:
        blockers.append(blocker("wrong_target", "cover_letter",
                                f"The cover letter does not name the employer ({emp}).", opening,
                                f"Name {emp} exactly as the posting does."))

    candidates = [title, re.sub(r"\s*\([^)]*\)", "", title).strip()]
    m = re.match(r"^(.*\S)\s+(?:I{1,3}|IV|V|VI{0,3}|\d)$", title)
    if m:
        stripped = m.group(1)
        marker = title[len(stripped):].strip()
        # Allowed only if the posting itself uses the title without the marker.
        pat = re.compile(re.escape(stripped) + r"(?!\s+" + re.escape(marker) + r"\b)", re.I)
        if pat.search(posting):
            candidates.append(stripped)
    if not any(c and lib.contains_phrase(text, c) for c in candidates):
        blockers.append(blocker("wrong_target", "cover_letter",
                                f"The cover letter does not name the job title ({title}).", opening,
                                f"Name the job as '{title}', the way the posting does."))

    if emp_ok:
        known = " ".join(lib.fact_text(f) for f in ctx.facts) + " " + (ctx.lead.get("employer") or "")
        target = lib.norm_employer(emp)
        region = _first_name_region(text)
        for sentence in re.split(r"(?<=[.!?])\s+|\n", region):
            t = TRIGGER_RE.search(sentence)
            if not t:
                continue
            for m in CONNECT_RE.finditer(sentence[t.start():]):
                name = re.sub(r"\s+(of|for|and|&)$", "", m.group(1)).rstrip(".,")
                n = lib.norm_text(name)
                if not n or lib.contains_phrase(known, name):
                    continue
                if n in target or target in n or n.split()[0] == target.split()[0]:
                    continue
                blockers.append(blocker("wrong_target", "cover_letter",
                                        f"The opening names a different employer than the one being applied to: '{name}'.",
                                        name, f"Name {emp}."))
    return blockers, []


# ----------------------------------------------------------------- contact

STREET_RE = re.compile(
    r"\b\d{1,5}\s+(?:[A-Z][\w.'-]*\s+){1,3}"
    r"(?:Street|Avenue|Road|Boulevard|Drive|Lane|Court|Way|Place|Highway|Parkway|"
    r"St\.|Ave\.|Rd\.|Blvd\.|Dr\.|Ln\.|Ct\.|Pl\.|Hwy\.)(?![A-Za-z])|\bP\.?\s?O\.?\s+Box\s+\d+")


def _is_confirmed_name(token, confirmed_text):
    """A dotted tool name such as Split.io is not a link when it appears word
    for word in a confirmed fact. Anything that starts like a web address
    (http or www) is always a link."""
    if re.match(r"(?:https?://|www\.)", token, re.I):
        return False
    return re.search(r"(?<![\w.])" + re.escape(token) + r"(?![\w])", confirmed_text, re.I) is not None


def check_contact(ctx, docs):
    blockers = []
    c = ctx.contact
    show = c.get("show_on_resume") or {}
    full = (c.get("full_name") or "").strip()
    email = (c.get("email") or "").strip()
    phone = lib.digits(c.get("phone"))[-10:]
    city = (c.get("city") or "").strip()
    links = {k: v for k, v in (c.get("links") or {}).items() if v}
    show_links = set(show.get("links") or [])
    allowed_links = {k: lib.norm_url(v) for k, v in links.items() if k in show_links}
    other_links = {lib.norm_url(v): k for k, v in links.items() if k not in show_links}
    confirmed_text = " ".join(lib.fact_text(f) for f in ctx.facts if f["status"] == "confirmed")
    exempt_hosts = set()
    for u in (ctx.lead.get("link"), (ctx.posting_json or {}).get("apply_link"),
              (ctx.posting_json or {}).get("source_url")):
        if u and u != "pasted":
            exempt_hosts.add(lib.norm_url(u).split("/")[0])

    for doc in docs:
        text = ctx.text[doc]
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if doc in ("resume", "cover_letter"):
            if not lines or lines[0] != full:
                blockers.append(blocker("contact_details", doc,
                                        f"The first line must be the full name exactly ({full}).",
                                        lines[0] if lines else None, f"Start with: {full}"))
        text_wo = text
        for m in lib.EMAIL_RE.finditer(text):
            e = m.group(0)
            if e.lower() != email.lower():
                blockers.append(blocker("contact_details", doc, "Email address is not the one in profile.yaml.", e))
            elif not show.get("email"):
                blockers.append(blocker("contact_details", doc, "Email is shown but show_on_resume.email is false.", e))
            text_wo = text_wo.replace(e, " ")
        for m in lib.PHONE_RE.finditer(text_wo):
            p = m.group(0)
            if not phone or lib.digits(p)[-10:] != phone:
                blockers.append(blocker("contact_details", doc, "Phone number is not the one in profile.yaml.", p))
            elif not show.get("phone"):
                blockers.append(blocker("contact_details", doc, "Phone is shown but show_on_resume.phone is false.", p))
        for m in lib.URL_RE.finditer(text_wo):
            u = m.group(0)
            n = lib.norm_url(u)
            if n in allowed_links.values():
                continue
            if n in other_links:
                blockers.append(blocker("contact_details", doc,
                                        f"The {other_links[n]} link is shown but show_on_resume.links excludes it.", u))
            elif n.split("/")[0] in exempt_hosts:
                continue
            elif _is_confirmed_name(u, confirmed_text):
                continue
            else:
                blockers.append(blocker("contact_details", doc, "Link is not one of the links in profile.yaml.", u))
        if doc in ("resume", "cover_letter"):
            head = "\n".join(lines[:8])
            hl = head.lower()
            if show.get("email") and email and email.lower() not in hl:
                blockers.append(blocker("contact_details", doc, "show_on_resume.email is true but the email is not in the contact line."))
            if show.get("phone") and phone and phone not in lib.digits(head):
                blockers.append(blocker("contact_details", doc, "show_on_resume.phone is true but the phone is not in the contact line."))
            if show.get("city_region") and city and city.lower() not in hl:
                blockers.append(blocker("contact_details", doc, "show_on_resume.city_region is true but the city is not in the contact line."))
            if not show.get("city_region") and city and lib.contains_phrase("\n".join(lines[:4]), city):
                blockers.append(blocker("contact_details", doc, "City is in the contact line but show_on_resume.city_region is false.", city))
            for k, n in allowed_links.items():
                if n not in hl.replace("https://", "").replace("www.", ""):
                    blockers.append(blocker("contact_details", doc, f"show_on_resume.links includes {k} but it is not in the contact line."))
        for m in STREET_RE.finditer(text):
            blockers.append(blocker("never_in_draft", doc, "Looks like a street address. Drafts never include one.",
                                    m.group(0), "Remove it."))
    return blockers, []


# ---------------------------------------------------------------- language

UK_TO_US = [("isation", "ization"), ("ised", "ized"), ("ising", "izing"), ("ise", "ize"),
            ("ours", "ors"), ("our", "or"), ("tre", "ter"), ("yse", "yze"), ("lling", "ling"),
            ("lled", "led"), ("ogue", "og"), ("ence", "ense"), ("ae", "e")]


def _allow_words(ctx):
    allow = set()
    for t in (ctx.facts_raw, ctx.profile_raw, ctx.posting_md, ctx.voice_raw):
        allow.update(re.findall(r"[a-z]+", (t or "").lower()))
    return allow


WORD_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]+(?:['’][A-Za-z]+)?(?![A-Za-z0-9])")


def check_language(ctx, docs):
    blockers, warnings = [], []
    banned = ctx.voice["banned"]
    age_file = lib.HERE / "data" / "age_phrases.txt"
    age = [ln.strip() for ln in age_file.read_text(encoding="utf-8").splitlines()
           if ln.strip() and not ln.startswith("#")] if age_file.is_file() else []
    spell_mod = lib.need("pyspellchecker", "spellchecker")
    spell = spell_mod.SpellChecker()
    allow = _allow_words(ctx)
    variety = ctx.voice["spelling"].lower()

    def known(w):
        if w in spell or w in allow or w.rstrip("s") in allow or (w + "s") in allow:
            return True
        if variety != "us":
            for a, b in UK_TO_US:
                if a in w and w.replace(a, b) in spell:
                    return True
        return False

    contact_vals = [ctx.contact.get(k) for k in ("full_name", "preferred_name", "email", "phone", "city", "region")]
    for doc in docs:
        text = ctx.text[doc]
        for ph in banned:
            q = lib.find_phrase(text, ph)
            if q:
                blockers.append(blocker("banned_phrase", doc, f"Banned phrase from voice.md: '{ph}'.", q,
                                        "Reword it, using the user's preferred wording if voice.md gives one."))
        for ph in age:
            q = lib.find_phrase(text, ph)
            if q:
                blockers.append(blocker("never_in_draft", doc, "Phrase that points at age (decision 015).", q,
                                        "Describe the work or the skill instead."))
        clean = scrub(text, contact_vals)
        seen = set()
        for m in WORD_RE.finditer(clean):
            tok = m.group(0)
            base = re.sub(r"['’]s$", "", tok)
            if tok != tok.lower() or len(base) < 4 or base in seen:
                continue
            seen.add(base)
            w = base.lower()
            if known(w):
                continue
            corr = spell.correction(w)
            if corr and corr != w:
                blockers.append(blocker("spelling", doc, f"Unknown word; likely '{corr}'.", tok,
                                        f"Change to '{corr}' if that is what was meant."))
            elif len(warnings) < 20:
                warnings.append(warning("language", f"Unknown word in {doc}: '{tok}'."))
    return blockers, warnings


# --------------------------------------------------------------------- pdf

PDF_HEADINGS = ["summary", "skills", "experience", "education", "certifications"]


def _fonts(resources, depth=0):
    """Yield (name, embedded) for every font reachable from a resources dict."""
    if resources is None or depth > 4:
        return
    resources = resources.get_object()
    fonts = resources.get("/Font")
    if fonts:
        for name, ref in fonts.get_object().items():
            f = ref.get_object()
            sub = str(f.get("/Subtype", ""))
            if sub == "/Type3":
                yield name, True
                continue
            if sub == "/Type0":
                desc = f.get("/DescendantFonts")
                f = desc.get_object()[0].get_object() if desc else f
            fd = f.get("/FontDescriptor")
            embedded = False
            if fd is not None:
                fd = fd.get_object()
                embedded = any(k in fd for k in ("/FontFile", "/FontFile2", "/FontFile3"))
            yield str(f.get("/BaseFont", name)), embedded
    xo = resources.get("/XObject")
    if xo:
        for ref in xo.get_object().values():
            x = ref.get_object()
            if str(x.get("/Subtype", "")) == "/Form":
                yield from _fonts(x.get("/Resources"), depth + 1)


def check_pdf(ctx, docs):
    blockers, warnings = [], []
    pypdf = lib.need("pypdf")
    full = (ctx.contact.get("full_name") or "").strip()
    headings = [h.lower() for h in PDF_HEADINGS] + [h.lower() for h in ctx.voice["headings"]]
    for doc, path in sorted(ctx.pdfs.items()):
        def bad(detail, quote=None):
            blockers.append(blocker("pdf_parse", doc, f"{path.name}: {detail}", quote,
                                    "Export the PDF again from the Google Doc so fonts are embedded. Do not build it with a script."))
        try:
            reader = pypdf.PdfReader(str(path))
            if reader.is_encrypted:
                bad("the PDF is encrypted.")
                continue
            page_text = [(p.extract_text() or "") for p in reader.pages]
        except Exception as e:
            bad(f"cannot be read ({type(e).__name__}).")
            continue
        text = "\n".join(page_text)
        if not text.strip():
            bad("no text could be extracted.")
            continue
        unembedded = set()
        try:
            for p in reader.pages:
                for name, emb in _fonts(p.get("/Resources")):
                    if not emb:
                        unembedded.add(str(name).lstrip("/"))
        except Exception:
            bad("fonts could not be inspected.")
        if unembedded:
            bad("fonts are not embedded: " + ", ".join(sorted(unembedded)) + ".")
        if full:
            if doc == "resume":
                # PDFs exported from Google Docs extract with each word on its
                # own line, so look at the start of the text, not the first line.
                start = " ".join(text.split())[: len(full) + 20]
                name_ok = lib.norm_text(full) in lib.norm_text(start)
            else:
                # Email addresses and links often contain the name, so remove them first.
                body = re.sub(r"-\n(?=\S)", "-", text)
                body = lib.EMAIL_RE.sub(" ", body)
                body = lib.URL_RE.sub(" ", body)
                name_ok = lib.norm_text(full) in lib.norm_text(body)
            if not name_ok:
                bad("the full name does not appear as the first line." if doc == "resume"
                    else "the full name does not appear in the extracted text.")
        txt = ctx.text.get(doc)
        if txt is not None:
            wanted = [_heading_key(ln) for ln in txt.splitlines() if _heading_key(ln) in headings]
            pdf_lines = [_heading_key(ln) for ln in text.splitlines()]
            pos = 0
            for h in wanted:
                try:
                    pos = pdf_lines.index(h, pos) + 1
                except ValueError:
                    bad(f"heading '{h}' is missing from the PDF text or out of order.")
                    break
            tw = set(w for w in lib.words(txt) if len(w) > 1)
            pw = set(lib.words(text))
            if tw:
                share = len(tw & pw) / len(tw)
                if share < 0.9:
                    bad(f"only {share:.0%} of the words in {doc}.txt appear in the PDF text.")
        pages = ctx.voice["resume_pages"]
        if doc == "resume" and pages and len(page_text) > pages:
            warnings.append(warning("pdf", f"{path.name} has {len(page_text)} pages; voice.md asks for {pages}."))
    return blockers, warnings


# ------------------------------------------------------------------ claims

def check_claims(ctx, docs):
    blockers, warnings = [], []
    if ctx.claims is None:
        return blockers, warnings
    errs = validate_mod.validate("claim-map", ctx.claims)
    if errs:
        return [blocker("other", "all", "claims.json does not match the claim-map schema: " + "; ".join(errs[:3]))], warnings
    by_id = {f["id"]: f for f in ctx.facts}
    for d in ctx.claims["documents"]:
        doc = d["document"]
        text_words = set(lib.words(ctx.text.get(doc, "")))
        for c in d["claims"]:
            q = c["text"][:200]
            if c["kind"] == "fact" and not c["fact_ids"]:
                blockers.append(blocker("claim_not_traced", doc, "A factual claim has no fact IDs.", q))
            for fid in c["fact_ids"]:
                f = by_id.get(fid)
                if f is None:
                    blockers.append(blocker("claim_not_traced", doc, f"Fact {fid} does not exist in facts.md.", q))
                elif f["status"] != "confirmed":
                    blockers.append(blocker("unconfirmed_fact", doc, f"Fact {fid} is not confirmed.", q))
            cw = [w for w in lib.words(c["text"])]
            if doc not in ctx.text:
                warnings.append(warning("claims", f"{doc}.txt is missing, so claims could not be located."))
                break
            if cw and sum(w in text_words for w in cw) / len(cw) < 0.85:
                warnings.append(warning("claims", f"Claim text not found in {doc}: '{q[:80]}'."))
    return blockers, warnings


# ----------------------------------------------------------------- posting

def check_posting(ctx, docs):
    blockers, warnings = [], []
    pm = ctx.posting_md
    if pm is None:
        blockers.append(blocker("posting_missing", "posting", "posting.md is missing.", None,
                                "Get the full posting (apply skill, fit mode) before drafting."))
    else:
        lines = pm.splitlines()
        i = 0
        while i < len(lines) and i < 2 and re.match(r"(Source|Captured):", lines[i]):
            i += 1
        n = len(" ".join(lines[i:]).split())
        if n < 120:
            blockers.append(blocker("posting_missing", "posting",
                                    f"posting.md has {n} words after the header; a full posting has at least 120.", None,
                                    "Get the full posting text. Never draft from a snippet."))
    if ctx.posting_json_error:
        blockers.append(blocker("posting_missing", "posting", ctx.posting_json_error))
    elif ctx.posting_json is None:
        blockers.append(blocker("posting_missing", "posting", "posting.json is missing.", None,
                                "Run the extract step of fit mode."))
    else:
        errs = validate_mod.validate("posting-extract", ctx.posting_json)
        if errs:
            blockers.append(blocker("posting_missing", "posting", "posting.json is invalid: " + "; ".join(errs[:3])))
        elif ctx.posting_json.get("full_text") is not True:
            blockers.append(blocker("posting_missing", "posting", "posting.json says only part of the posting was captured.", None,
                                    "Get the full posting text."))
    if ctx.lead.get("is_open") == "closed":
        blockers.append(blocker("posting_closed", "posting", "The job is closed."))
    checked = ctx.lead.get("open_checked")
    try:
        from datetime import date as _d
        age = (lib.today() - _d.fromisoformat(checked)).days if checked else None
    except ValueError:
        age = None
    if age is None:
        warnings.append(warning("posting", "Open status was never checked (lead.json open_checked is missing)."))
    elif age > 3:
        warnings.append(warning("posting", f"Open status last checked {age} days ago."))
    return blockers, warnings


# ------------------------------------------------------------------ skills

SKILLS_HEADINGS = {"skills", "technical skills", "skills and tools", "core skills", "key skills"}
# Words that limit a level. A draft may not drop one (decision 014).
LIMITING = {"basic", "beginner", "beginning", "introductory", "novice", "limited",
            "familiar", "familiarity", "exposure", "learning"}
SKILL_STOP = {"and", "of", "the", "for", "in", "with", "a", "an", "to", "on"}


def _skill_tokens(s):
    """Lowercase word tokens that keep C++, C#, Node.js and the like whole.
    Plural s is dropped so 'cabinets' matches 'cabinet'."""
    out = []
    for t in re.findall(r"[a-z0-9]+(?:[.+#][a-z0-9+#]*)*", (s or "").lower()):
        t = t.rstrip(".")
        if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
            t = t[:-1]
        if t and t not in SKILL_STOP:
            out.append(t)
    return out


def _initials(s):
    """First letters of the words in s, ignoring small words and level
    words: 'Structured Query Language' gives 'sql'. '' for one word."""
    ws = [w for w in re.findall(r"[A-Za-z][A-Za-z0-9]*", s or "")
          if w.lower() not in SKILL_STOP and w.lower() not in LIMITING]
    return "".join(w[0] for w in ws).lower() if len(ws) >= 2 else ""


def _skills_lines(text, extra_headings):
    """Lines of the resume's Skills section, without bullets. [] if the
    resume has no Skills heading."""
    lines = [ln.strip() for ln in text.splitlines()]
    ends = ROLE_HEADINGS | OTHER_HEADINGS | {_heading_key(h) for h in extra_headings}
    ends -= SKILLS_HEADINGS
    start = next((i + 1 for i, ln in enumerate(lines) if _heading_key(ln) in SKILLS_HEADINGS), None)
    if start is None:
        return []
    out = []
    for ln in lines[start:]:
        if not ln:
            continue
        if _heading_key(ln) in ends or _heading_key(ln) in SKILLS_HEADINGS:
            break
        out.append(re.sub(r"^[-*•]\s+", "", ln))
    return out


def _split_skills_line(line):
    """Return (label or None, items). Parenthetical text is dropped first so
    a colon inside parentheses is not taken for the label."""
    flat = re.sub(r"\([^)]*\)", " ", line)
    label = None
    if ":" in flat:
        label, flat = flat.split(":", 1)
        label = label.strip() or None
    items = [i.strip(" .") for i in re.split(r"[,;]", flat)]
    return label, [i for i in items if i]


class _SkillItem:
    def __init__(self, text):
        self.text = text
        toks = _skill_tokens(text)
        self.level = [t for t in toks if t in LIMITING]
        self.toks = set(t for t in toks if t not in LIMITING)
        self.initials = _initials(text)

    def matches(self, fact):
        if not self.toks:
            return False
        detail = lib.fact_text(fact)
        ft = set(_skill_tokens(detail))
        if self.toks <= ft:
            return True
        if self.initials and self.initials in ft:
            return True  # long form written out, fact has the acronym
        if len(self.toks) == 1:
            # Acronym written, fact has the long form.
            (tok,) = self.toks
            words = [w for w in re.findall(r"[A-Za-z][A-Za-z0-9]*", detail)
                     if w.lower() not in SKILL_STOP]
            for n in range(2, 7):
                for i in range(len(words) - n + 1):
                    if "".join(w[0] for w in words[i:i + n]).lower() == tok:
                        return True
        return False


def _fact_level(fact):
    """A limiting level word in the first sentence of the fact, or None."""
    first = re.split(r"(?<=\.)\s", fact["detail"])[0]
    hit = [t for t in _skill_tokens(first) if t in LIMITING]
    return hit[0] if hit else None


def check_skills(ctx, docs):
    """Skills lines in the resume (decision 023): every label is a category
    heading under Skills and tools in facts.md, and every item is a confirmed
    fact under that heading. Warn only if facts.md has no categories yet."""
    blockers, warnings = [], []
    if "resume" not in ctx.text:
        return blockers, warnings
    lines = _skills_lines(ctx.text["resume"], ctx.voice["headings"])
    if not lines:
        return blockers, warnings
    # Decision 024: an optional Skills intro line (such as "Experience with:")
    # set in facts.md carries the qualifier, so items may print without level
    # words. The line itself is not a skills line.
    intro = lib.skills_intro(ctx.facts_raw)
    intro_printed = False
    if intro:
        kept = []
        for ln in lines:
            if lib.norm_text(ln) == lib.norm_text(intro):
                intro_printed = True
            else:
                kept.append(ln)
        lines = kept
    skills = [f for f in ctx.facts if lib.is_skill(f)]
    confirmed = [f for f in skills if f["status"] == "confirmed"]
    unconfirmed = [f for f in skills if f["status"] == "unconfirmed"]
    other_conf = [f for f in ctx.facts if f["status"] == "confirmed" and not lib.is_skill(f)
                  and not lib.is_role(f)]
    cats = lib.skill_categories(ctx.facts)
    seen = set()

    def add(check, detail, quote, fix=None):
        if (check, quote) not in seen:
            seen.add((check, quote))
            blockers.append(blocker(check, "resume", detail, quote, fix))

    if not cats:
        warnings.append(warning("skills",
                                "facts.md has no skill category headings yet, so skills line labels were not checked. "
                                "The onboard skill can sort the skills into categories (decision 023)."))
        for line in lines:
            for text in _split_skills_line(line)[1]:
                item = _SkillItem(text)
                if not any(item.matches(f) for f in confirmed):
                    warnings.append(warning("skills", f"Skill '{text}' is not in any confirmed skill fact."))
        return blockers, warnings

    by_label = {lib.norm_text(c): c for c in cats}
    cat_list = "; ".join(cats)
    for line in lines:
        if re.search(r"[();]", line):
            add("other", "Skills lines have no parentheses or semicolons (writing rules, Skills).", line[:200],
                "Write 'Label: item, item' and move the detail into a bullet.")
        label, items = _split_skills_line(line)
        cat = by_label.get(lib.norm_text(label)) if label else None
        if label is None:
            homes = []
            for text in items:
                f = next((f for f in confirmed if _SkillItem(text).matches(f) and f["subsection"]), None)
                if f and f["subsection"] not in homes:
                    homes.append(f["subsection"])
            fix = ("Write it as 'Label: item, item'. The items here are confirmed under: " + "; ".join(homes) + "."
                   if homes else "Write it as 'Label: item, item', using a category heading from facts.md.")
            add("other", f"Skills line has no category label. Categories in facts.md: {cat_list}.", line[:200], fix)
        elif cat is None:
            add("wrong_category", f"'{label}' is not a skill category in facts.md. Categories: {cat_list}.", label,
                "Use the category headings from facts.md, and list each item under the category it is confirmed under."
                + ("" if items else " To print an intro line above the skills, add 'Skills intro: <text>' "
                   "to the Wording rules in facts.md (decision 024)."))
        for text in items:
            item = _SkillItem(text)
            here = [f for f in confirmed if f["subsection"] == cat] if cat else []
            hits = [f for f in here if item.matches(f)]
            if hits:
                levels = [_fact_level(f) for f in hits]
                if all(levels) and not item.level and not (intro and intro_printed):
                    f = hits[0]
                    add("overstated",
                        f"{f['id']} gives the level as '{levels[0]}'. A draft keeps a limiting level (decision 014).",
                        text,
                        (f"Print the Skills intro line from facts.md ('{intro}') above the skills lines, "
                         f"or write '{levels[0]} {text}'." if intro
                         else f"Write '{levels[0]} {text}', leave the skill out, or add a 'Skills intro:' "
                              "line to the Wording rules in facts.md (decision 024)."))
                continue
            elsewhere = [f for f in confirmed if f["subsection"] != cat and item.matches(f)]
            if elsewhere and label is None and elsewhere[0]["subsection"]:
                continue  # the no-label blocker already names the category
            if elsewhere:
                f = elsewhere[0]
                where = f["subsection"] or "Skills and tools with no category"
                add("wrong_category", f"{text} is confirmed under {where} ({f['id']})" + (f", not {label}." if label else "."),
                    text, f"Move {text} to the {where} line." if f["subsection"] else
                    "Ask the user to give this skill a category in facts.md.")
                continue
            unc = [f["id"] for f in unconfirmed if item.matches(f)]
            if unc:
                add("unconfirmed_fact", f"Skill appears only in unconfirmed fact {', '.join(unc)}.", text)
                continue
            other = [f for f in other_conf if item.matches(f)]
            if other:
                f = other[0]
                add("wrong_category",
                    f"{text} is confirmed in {f['section']} ({f['id']}), not as a skill. Skills lines list only facts under Skills and tools.",
                    text, "Leave it out of the skills line, or ask the user to confirm it as a skill under a category.")
                continue
            add("claim_not_traced", f"{text} is not in any confirmed skill fact.", text,
                "Remove it, or ask the user to confirm it as a skill under a category.")
    return blockers, warnings
