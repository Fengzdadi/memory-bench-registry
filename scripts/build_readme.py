#!/usr/bin/env python3
"""Generate README.md (English) and README.zh-CN.md from benchmarks/*.yaml and templates/.

Usage:
  python scripts/build_readme.py           # write the READMEs
  python scripts/build_readme.py --check   # exit 1 if any README is out of date
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
# (template, output) pairs, one per language
OUTPUTS = [("README.md.j2", ROOT / "README.md"), ("README.zh-CN.md.j2", ROOT / "README.zh-CN.md")]
SCHEMA = ROOT / "schema" / "benchmark.schema.json"


def load_entries() -> list[dict]:
    entries = [yaml.safe_load(p.read_text()) for p in sorted(BENCH_DIR.glob("*.yaml"))]
    return sorted(entries, key=lambda e: e["name"].casefold())


def md_cell(text) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def fmt_name(entry: dict) -> str:
    # name links to the YAML file, which holds the full details and sources
    return f"[{md_cell(entry['name'])}](benchmarks/{entry['slug']}.yaml)"


def fmt_links(entry: dict) -> str:
    parts = [f"[{label}]({url})" for label, url in entry["links"].items() if url]
    # non-breaking spaces keep "paper · code · data" on one line in narrow table columns
    return "&nbsp;·&nbsp;".join(parts) if parts else "—"


def fmt_scale(entry: dict) -> str:
    scale = entry["scale"]
    parts = []
    if scale["conversations"] is not None:
        parts.append(f"{scale['conversations']:,}&nbsp;conv.")
    if scale["questions"] is not None:
        parts.append(f"{scale['questions']:,}&nbsp;Q")
    return "<br>".join(parts) if parts else "—"


def fmt_types(entry: dict) -> str:
    return ", ".join(f"`{t}`" for t in entry["memory_types"])


def newest_first(entries) -> list[dict]:
    # newest release first; ties by name; undated entries last
    by_name = sorted(entries, key=lambda e: e["name"].casefold())
    dated = sorted((e for e in by_name if e["release_date"]), key=lambda e: e["release_date"], reverse=True)
    return dated + [e for e in by_name if not e["release_date"]]


def fmt_date(entry: dict) -> str:
    # U+2011 (non-breaking hyphen) stops "2026-10" from wrapping in narrow columns
    return entry["release_date"].replace("-", "\u2011") if entry["release_date"] else "—"


def fmt_month(entry: dict) -> str:
    # within a year section only the month is shown
    return entry["release_date"][5:7] if entry["release_date"] else "—"


def build_context(entries: list[dict]) -> dict:
    schema = json.loads(SCHEMA.read_text())
    type_order = schema["$defs"]["memory_type"]["enum"]
    level_order = schema["properties"]["repro_level"]["enum"]

    by_type = []
    for mtype in type_order:
        members = newest_first(e for e in entries if mtype in e["memory_types"])
        by_type.append({"type": mtype, "entries": members})

    by_year: dict[str, list[dict]] = {}
    for entry in newest_first(entries):
        year = entry["release_date"][:4] if entry["release_date"] else "undated"
        by_year.setdefault(year, []).append(entry)

    levels = Counter(e["repro_level"] for e in entries)
    return {
        "entries": newest_first(entries),
        "by_type": by_type,
        "by_year": [{"year": y, "entries": es} for y, es in by_year.items()],
        "level_counts": [{"level": lv, "count": levels.get(lv, 0)} for lv in level_order],
    }


def render(template: str, context: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    env.filters.update(name=fmt_name, date=fmt_date, month=fmt_month, links=fmt_links, scale=fmt_scale, types=fmt_types, cell=md_cell)
    return env.get_template(template).render(**context)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if any README differs from the generated output")
    args = parser.parse_args()

    context = build_context(load_entries())
    stale = False
    for template, path in OUTPUTS:
        output = render(template, context)
        name = path.relative_to(ROOT)
        if not args.check:
            path.write_text(output)
            print(f"wrote {name}")
            continue
        current = path.read_text() if path.exists() else ""
        if current == output:
            print(f"{name} is up to date")
            continue
        stale = True
        sys.stdout.writelines(
            difflib.unified_diff(current.splitlines(True), output.splitlines(True), f"{name} (committed)", f"{name} (generated)")
        )
        print(f"\n{name} is out of date: run python scripts/build_readme.py", file=sys.stderr)
    if stale:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
