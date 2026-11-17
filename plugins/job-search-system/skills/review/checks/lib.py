"""Shared helpers for the check scripts. Standard library only, except where
a function says it needs a package (loaded lazily, so a missing package only
matters to the check that needs it).

Must not import anything from outside this folder. The sync tool copies this
folder into skills, where it sits next to ../shared/schemas/.
"""
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA_DIR = HERE.parent / "shared" / "schemas"
REQ_FILE = HERE / "requirements.txt"


class MissingDependency(Exception):
    def __init__(self, name):
        super().__init__(name)
        self.name = name


class CannotRun(Exception):
    """A required input is missing or unreadable (exit code 2)."""

    def __init__(self, message, fix=""):
        super().__init__(message)
        self.message = message
        self.fix = fix


def need(module_name, import_name=None):
    """Import a package or raise MissingDependency."""
    try:
        return __import__(import_name or module_name, fromlist=["_"])
    except ImportError:
        raise MissingDependency(module_name)


def error_exit(message, fix=""):
    print(json.dumps({"error": message, "fix": fix}))
    sys.exit(2)


def missing_dep_exit(name):
    error_exit(f"missing dependency: {name}", f"python3 -m pip install -r {REQ_FILE}")


def today():
    """Today's date. JSS_TODAY (YYYY-MM-DD) overrides it, for tests."""
    override = os.environ.get("JSS_TODAY")
    return date.fromisoformat(override) if override else date.today()


# ----- Normalization. Must match collector/src/Util.gs (see shared/tracker.md).

LEGAL_SUFFIXES = {"inc", "llc", "ltd", "corp", "corporation", "co", "company",
                  "lp", "llp", "plc", "pllc", "pc"}


def norm_text(s):
    s = "" if s is None else str(s)
    s = s.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def norm_employer(s):
    words = [w for w in norm_text(s).split(" ") if w]
    if words and words[0] == "the":
        words.pop(0)
    while len(words) > 1 and words[-1] in LEGAL_SUFFIXES:
        words.pop()
    return " ".join(words)


# Locations that name no place. Two sources can describe the same remote job as
# "Remote" and "United States"; both count as no city so the keys match.
# Whole normalized values only. Must match GENERIC_LOCATIONS_ in collector/src/Util.gs.
GENERIC_LOCATIONS = frozenset([
    "remote", "united states", "us", "u s", "usa", "u s a", "anywhere", "nationwide", "worldwide",
    "remote us", "remote u s", "remote usa", "remote united states", "remote anywhere",
    "remote nationwide", "remote worldwide", "us remote", "u s remote", "usa remote",
    "united states remote", "anywhere remote", "nationwide remote", "worldwide remote",
    "fully remote", "work from home",
])


def city_of(location):
    loc = re.sub(r"\([^)]*\)", " ", str(location or ""))
    city = norm_text(loc.split(",")[0])
    return "" if city in GENERIC_LOCATIONS else city


def dedupe_key(employer, title, location):
    return "|".join([norm_employer(employer), norm_text(title), city_of(location)])


def contains_phrase(hay, needle):
    n = norm_text(needle)
    if not n:
        return False
    return (" " + norm_text(hay) + " ").find(" " + n + " ") >= 0


def find_phrase(text, phrase):
    """Return the text as written for a whole-word, punctuation-insensitive
    match of phrase, or None. A phrase with no letters or digits is matched
    as that literal text (for example a long dash)."""
    tokens = re.findall(r"[A-Za-z0-9]+", phrase.replace("&", " and "))
    if not tokens:
        p = phrase.strip()
        return p if p and p in text else None
    pattern = r"(?<![A-Za-z0-9])" + r"[^A-Za-z0-9]+".join(map(re.escape, tokens)) + r"(?![A-Za-z0-9])"
    m = re.search(pattern, text, re.I)
    return m.group(0) if m else None


# ----- Reading files

def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError) as e:
        raise CannotRun(f"cannot read {path}: {e}", "Check the file is plain UTF-8 text.")


def read_json(path):
    t = read_text(path)
    if t is None:
        return None
    try:
        return json.loads(t)
    except json.JSONDecodeError as e:
        raise CannotRun(f"{path} is not valid JSON: {e}", "Rewrite the file as JSON.")


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


# ----- facts.md

FACT_RE = re.compile(
    r"^- \[(confirmed|unconfirmed)\] (F-\d{3,}) \| (.*?) \| (.*?) \| (.*)$")


def parse_facts(text):
    """Return a list of dicts: status, id, employer, title, detail, section
    and subsection. Employer and title are '' where the line has '-'.

    section is the nearest ## heading (Roles, Skills and tools, ...).
    subsection is the nearest ### heading under it (an employer under
    Results and scope, a category under Skills and tools), or '' if there is
    none. A new ## heading clears the subsection."""
    facts = []
    section = ""
    subsection = ""
    for line in strip_comments(text).splitlines():
        h = re.match(r"^(#{2,3})\s+(.*?)\s*$", line)
        if h:
            if len(h.group(1)) == 2:
                section = h.group(2)
                subsection = ""
            else:
                subsection = h.group(2)
            continue
        m = FACT_RE.match(line.rstrip())
        if not m:
            continue
        status, fid, emp, title, detail = m.groups()
        facts.append({
            "status": status, "id": fid,
            "employer": "" if emp.strip() == "-" else emp.strip(),
            "title": "" if title.strip() == "-" else title.strip(),
            "detail": detail.strip(), "section": section,
            "subsection": subsection,
        })
    return facts


def skills_intro(facts_raw):
    """The optional per-person Skills intro line from facts.md (decision 024):
    a line such as '- Skills intro: Experience with:' in Wording rules.
    Returns the text after the colon, or None."""
    m = re.search(r"^\s*[-*]?\s*Skills intro:[ \t]*(.+?)\s*$", strip_comments(facts_raw or ""), re.M | re.I)
    return m.group(1).strip() if m else None


def fact_text(f):
    return " ".join(x for x in (f["employer"], f["title"], f["detail"]) if x)


def is_role(f):
    return f["section"].lower().startswith("roles")


def is_skill(f):
    return f["section"].lower().startswith("skills")


def skill_categories(facts):
    """The category headings under Skills and tools, in file order."""
    out = []
    for f in facts:
        if is_skill(f) and f["subsection"] and f["subsection"] not in out:
            out.append(f["subsection"])
    return out


# ----- voice.md

def _section(text, heading):
    m = re.search(r"^#{1,3}\s+" + re.escape(heading) + r"\s*$(.*?)(?=^#{1,3}\s|\Z)",
                  text, re.S | re.M | re.I)
    return m.group(1) if m else None


def parse_voice(text):
    """Return dict: banned (list), spelling (str), resume_pages (int or None),
    headings (extra resume heading names)."""
    text = strip_comments(text)
    banned = []
    sec = _section(text, "Banned phrases")
    if sec:
        m = re.search(r"```[^\n]*\n(.*?)```", sec, re.S)
        if m:
            banned = [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
    spelling = "US"
    pages = None
    headings = []
    sec = _section(text, "Spelling and format") or ""
    m = re.search(r"Spelling:\s*([A-Za-z]+)", sec)
    if m:
        spelling = m.group(1)
    m = re.search(r"Resume length:\s*(\d+)\s*page", sec, re.I)
    if m:
        pages = int(m.group(1))
    m = re.search(r"Resume headings:\s*(.+)", sec, re.I)
    if m:
        headings = [h.strip() for h in m.group(1).split(",") if h.strip()]
    return {"banned": banned, "spelling": spelling, "resume_pages": pages,
            "headings": headings}


# ----- profile.yaml

def parse_profile(text):
    yaml = need("pyyaml", "yaml")
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise CannotRun(f"profile.yaml is not valid YAML: {e}", "Fix the YAML.")
    if not isinstance(data, dict) or "contact" not in data:
        raise CannotRun("profile.yaml has no contact section", "Check profile.yaml.")
    return data


# ----- Text extraction helpers

URL_RE = re.compile(
    r"https?://[^\s<>)\]]+|www\.[^\s<>)\]]+|"
    r"\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|org|net|io|example|co|us|edu|gov|dev|app)\b(?:/[^\s<>)\]]*)?",
    re.I)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]\d{4}(?!\d)")


def digits(s):
    return re.sub(r"\D", "", s or "")


def norm_url(u):
    u = (u or "").strip().lower().rstrip(".,;)")
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    return u.rstrip("/")


def words(text):
    return re.findall(r"[a-z0-9]+", (text or "").lower())
