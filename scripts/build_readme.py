#!/usr/bin/env python3
"""Generate README.md from benchmarks/*.yaml and templates/README.md.j2.

Usage:
  python scripts/build_readme.py           # write README.md
  python scripts/build_readme.py --check   # exit 1 if README.md is out of date
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from collections import Counter
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent.parent
BENCH_DIR = ROOT / "benchmarks"
TEMPLATE_DIR = ROOT / "templates"
README = ROOT / "README.md"
SCHEMA = ROOT / "schema" / "benchmark.schema.json"


def load_entries() -> list[dict]:
    entries = [yaml.safe_load(p.read_text()) for p in sorted(BENCH_DIR.glob("*.yaml"))]
    return sorted(entries, key=lambda e: e["name"].casefold())


def md_cell(text) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def fmt_links(entry: dict) -> str:
    parts = [f"[{label}]({url})" for label, url in entry["links"].items() if url]
    return " · ".join(parts) if parts else "—"


def fmt_scale(entry: dict) -> str:
    scale = entry["scale"]
    parts = []
    if scale["conversations"] is not None:
        parts.append(f"{scale['conversations']:,} conv.")
    if scale["questions"] is not None:
        parts.append(f"{scale['questions']:,} Q")
    if scale["avg_context_length"]:
        parts.append(f"avg {scale['avg_context_length']}")
    return md_cell(" · ".join(parts)) if parts else "—"


def fmt_types(entry: dict) -> str:
    return ", ".join(f"`{t}`" for t in entry["memory_types"])


def date_key(entry: dict):
    # undated entries sort last in the timeline
    return (entry["release_date"] or "9999-99", entry["name"].casefold())


def build_context(entries: list[dict]) -> dict:
    schema = json.loads(SCHEMA.read_text())
    type_order = schema["$defs"]["memory_type"]["enum"]
    level_order = schema["properties"]["repro_level"]["enum"]

    by_type = []
    for mtype in type_order:
        members = sorted((e for e in entries if mtype in e["memory_types"]), key=date_key)
        by_type.append({"type": mtype, "entries": members})

    timeline: dict[str, list[dict]] = {}
    for entry in sorted(entries, key=date_key):
        year = entry["release_date"][:4] if entry["release_date"] else "undated"
        timeline.setdefault(year, []).append(entry)

    levels = Counter(e["repro_level"] for e in entries)
    return {
        "entries": entries,
        "by_type": by_type,
        "timeline": [{"year": y, "entries": es} for y, es in timeline.items()],
        "level_counts": [{"level": lv, "count": levels.get(lv, 0)} for lv in level_order],
    }


def render() -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    env.filters.update(links=fmt_links, scale=fmt_scale, types=fmt_types, cell=md_cell)
    return env.get_template("README.md.j2").render(**build_context(load_entries()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if README.md differs from the generated output")
    args = parser.parse_args()

    output = render()
    if args.check:
        current = README.read_text() if README.exists() else ""
        if current == output:
            print("README.md is up to date")
            return 0
        sys.stdout.writelines(
            difflib.unified_diff(current.splitlines(True), output.splitlines(True), "README.md (committed)", "README.md (generated)")
        )
        print("\nREADME.md is out of date: run python scripts/build_readme.py", file=sys.stderr)
        return 1
    README.write_text(output)
    print(f"wrote {README.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
