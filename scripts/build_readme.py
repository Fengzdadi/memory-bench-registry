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


def fmt_name(entry: dict) -> str:
    # name links to the YAML file, which holds the full details and sources
    return f"[{md_cell(entry['name'])}](benchmarks/{entry['slug']}.yaml)"


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
    return md_cell(" · ".join(parts)) if parts else "—"


def fmt_types(entry: dict) -> str:
    return ", ".join(f"`{t}`" for t in entry["memory_types"])


def newest_first(entries) -> list[dict]:
    # newest release first; ties by name; undated entries last
    by_name = sorted(entries, key=lambda e: e["name"].casefold())
    dated = sorted((e for e in by_name if e["release_date"]), key=lambda e: e["release_date"], reverse=True)
    return dated + [e for e in by_name if not e["release_date"]]


def build_context(entries: list[dict]) -> dict:
    schema = json.loads(SCHEMA.read_text())
    type_order = schema["$defs"]["memory_type"]["enum"]
    level_order = schema["properties"]["repro_level"]["enum"]

    by_type = []
    for mtype in type_order:
        members = newest_first(e for e in entries if mtype in e["memory_types"])
        by_type.append({"type": mtype, "entries": members})

    levels = Counter(e["repro_level"] for e in entries)
    return {
        "entries": newest_first(entries),
        "by_type": by_type,
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
    env.filters.update(name=fmt_name, links=fmt_links, scale=fmt_scale, types=fmt_types, cell=md_cell)
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
