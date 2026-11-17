#!/usr/bin/env python3
"""Validate a JSON file against one of the system's schemas.

    python3 checks/validate.py SCHEMA FILE

SCHEMA is posting-extract, claim-map or review-result, loaded from
../shared/schemas/<SCHEMA>.json. Prints {"valid": true} or
{"valid": false, "errors": [...]}. Exit 0 valid, 1 not valid, 2 could not run.
"""
import json
import sys

import lib


def path_of(error):
    p = "$"
    for part in error.absolute_path:
        p += f"[{part}]" if isinstance(part, int) else f".{part}"
    return p


def validate(schema_name, data):
    jsonschema = lib.need("jsonschema")
    schema_file = lib.SCHEMA_DIR / f"{schema_name}.json"
    if not schema_file.is_file():
        raise lib.CannotRun(f"unknown schema: {schema_name}",
                            "Use posting-extract, claim-map or review-result.")
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    v = jsonschema.Draft202012Validator(schema)
    errors = sorted(v.iter_errors(data), key=lambda e: list(map(str, e.absolute_path)))
    return [f"{path_of(e)}: {e.message}" for e in errors]


def main():
    if len(sys.argv) != 3:
        lib.error_exit("usage: validate.py SCHEMA FILE")
    name, file = sys.argv[1], sys.argv[2]
    try:
        data = lib.read_json(file)
        if data is None:
            lib.error_exit(f"file not found: {file}")
        errors = validate(name, data)
    except lib.MissingDependency as e:
        lib.missing_dep_exit(e.name)
    except lib.CannotRun as e:
        lib.error_exit(e.message, e.fix)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}))
        sys.exit(1)
    print(json.dumps({"valid": True}))


if __name__ == "__main__":
    main()
