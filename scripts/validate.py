#!/usr/bin/env python3
"""Validate every benchmarks/*.yaml against schema/benchmark.schema.json plus cross-field rules.

Usage: python scripts/validate.py [files...]   (default: all of benchmarks/*.yaml)
Exit code 1 if any file fails.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "benchmark.schema.json"
BENCH_DIR = ROOT / "benchmarks"

# Fields whose non-null / non-empty value must cite where it came from (hard rule: everything traceable).
SOURCED_FIELDS = [
    "release_date",
    "venue",
    "memory_types",
    "links.paper",
    "links.code",
    "links.data",
    "scale.conversations",
    "scale.questions",
    "scale.avg_context_length",
    "metrics",
    "judge_model",
]
LEVELS = ["unverified", "paper_only", "data_public", "official_script", "smoke_tested", "full_run"]


def get_path(doc: dict, path: str):
    cur = doc
    for part in path.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def is_set(value) -> bool:
    return value is not None and value != [] and value != ""


def check_rules(doc: dict, path: Path) -> list[str]:
    errors = []
    if doc.get("slug") != path.stem:
        errors.append(f"slug '{doc.get('slug')}' does not match file name '{path.stem}'")

    sources = doc.get("sources") or {}
    for field in SOURCED_FIELDS:
        if is_set(get_path(doc, field)) and field not in sources:
            errors.append(f"'{field}' is set but has no entry in sources")

    level = doc.get("repro_level")
    checked = doc.get("repro_checked_at")
    if level == "unverified":
        if checked is not None:
            errors.append("repro_checked_at must be null while repro_level is unverified")
    else:
        if checked is None:
            errors.append(f"repro_level '{level}' requires repro_checked_at")
        if "repro_level" not in sources:
            errors.append(f"repro_level '{level}' requires a sources entry saying what was checked")
    if checked is not None:
        try:
            day = dt.date.fromisoformat(checked)
        except ValueError:
            errors.append(f"repro_checked_at '{checked}' is not a valid date")
        else:
            if day > dt.date.today():
                errors.append(f"repro_checked_at '{checked}' is in the future")

    links = doc.get("links") or {}
    if level in ("official_script", "smoke_tested", "full_run") and not links.get("code"):
        errors.append(f"repro_level '{level}' requires links.code")
    if level == "data_public" and not (links.get("data") or links.get("code")):
        errors.append("repro_level 'data_public' requires links.data or links.code")
    if level in ("smoke_tested", "full_run") and not doc.get("run_records"):
        errors.append(f"repro_level '{level}' requires at least one run_record")
    if level == "paper_only" and not links.get("paper"):
        errors.append("repro_level 'paper_only' requires links.paper")

    release = doc.get("release_date")
    if release:
        year, month = map(int, release.split("-"))
        if dt.date(year, month, 1) > dt.date.today():
            errors.append(f"release_date '{release}' is in the future")
    return errors


def main(argv: list[str]) -> int:
    schema = json.loads(SCHEMA_PATH.read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    files = [Path(a) for a in argv] or sorted(BENCH_DIR.glob("*.yaml"))
    if not files:
        print("no benchmark files found", file=sys.stderr)
        return 1

    failed = 0
    names: dict[str, Path] = {}
    for path in files:
        try:
            doc = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            print(f"{path}: YAML error: {exc}")
            failed += 1
            continue
        errors = [
            f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
            for e in sorted(validator.iter_errors(doc), key=lambda e: list(map(str, e.absolute_path)))
        ]
        if isinstance(doc, dict) and not errors:
            errors += check_rules(doc, path)
            name = doc["name"].casefold()
            if name in names:
                errors.append(f"duplicate name, also used by {names[name].name}")
            names[name] = path
        if errors:
            failed += 1
            shown = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
            for err in errors:
                print(f"{shown}: {err}")

    total = len(files)
    print(f"{total - failed}/{total} files valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
