#!/usr/bin/env python3
"""Run the code checks on one application's working folder.

    python3 checks/run_checks.py --workdir DIR [--skip NAMES] [--only NAMES]

Checks: posting, facts_trace, skills, target, contact, language, pdf, claims.
Prints one JSON object. Exit 0 passed, 1 blockers found, 2 could not run.
See checks/README.md for the folder layout and the output shape.
"""
import argparse
import json
import sys
from pathlib import Path

import lib

ORDER = ["posting", "facts_trace", "skills", "target", "contact", "language", "pdf", "claims"]


def parse_names(value, flag):
    names = [n.strip() for n in (value or "").split(",") if n.strip()]
    bad = [n for n in names if n not in ORDER]
    if bad:
        raise lib.CannotRun(f"unknown check name in {flag}: {', '.join(bad)}",
                            "Use: " + ", ".join(ORDER))
    return names


def run(workdir, skip, only):
    import checkers
    if not workdir.is_dir():
        raise lib.CannotRun(f"working folder not found: {workdir}", "Check the --workdir path.")
    ctx = checkers.Context(workdir)
    for name, val in (("facts.md", ctx.facts_raw), ("voice.md", ctx.voice_raw), ("profile.yaml", ctx.profile_raw)):
        if val is None:
            raise lib.CannotRun(f"missing input: {name}", f"Copy {name} from the profile folder into the working folder.")
    if not ctx.text and not ctx.pdfs:
        raise lib.CannotRun("no draft files in the working folder",
                            "Add resume.txt, cover_letter.txt or answers.txt (and PDFs if they exist).")
    ctx.profile  # parse now so a bad profile.yaml is exit 2
    ctx.voice
    docs = [d for d in checkers.DOCS if d in ctx.text]

    ran, skipped, blockers, warnings = [], [], [], []

    def skip_reason(name):
        if only and name not in only:
            return "not selected by --only"
        if name in skip:
            return "skipped by --skip"
        return None

    fns = {"posting": checkers.check_posting, "facts_trace": checkers.check_facts_trace,
           "skills": checkers.check_skills,
           "target": checkers.check_target, "contact": checkers.check_contact,
           "language": checkers.check_language, "pdf": checkers.check_pdf,
           "claims": checkers.check_claims}
    for name in ORDER:
        reason = skip_reason(name)
        if not reason:
            if name == "pdf" and not ctx.pdfs:
                reason = "no PDFs in the working folder"
            elif name == "claims" and ctx.claims is None:
                reason = "no claims.json"
            elif name in ("facts_trace", "contact", "language") and not docs:
                reason = "no draft text files"
            elif name == "skills" and "resume" not in ctx.text:
                reason = "needs resume.txt"
            elif name == "target" and ("cover_letter" not in ctx.text or not ctx.lead):
                reason = "needs cover_letter.txt and lead.json"
        if reason:
            skipped.append({"check": name, "reason": reason})
            continue
        b, w = fns[name](ctx, docs)
        ran.append(name)
        blockers += b
        warnings += w
    return {"schema_version": 1, "ran": ran, "skipped": skipped,
            "passed": not blockers, "blockers": blockers, "warnings": warnings}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--skip", default="")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    try:
        result = run(Path(a.workdir), parse_names(a.skip, "--skip"), parse_names(a.only, "--only"))
    except lib.MissingDependency as e:
        lib.missing_dep_exit(e.name)
    except lib.CannotRun as e:
        lib.error_exit(e.message, e.fix)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
