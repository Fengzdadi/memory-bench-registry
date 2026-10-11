#!/usr/bin/env python3
"""Build the static website into _site/ from benchmarks/*.yaml and site/index.html.

Usage:
  python scripts/build_site.py                # write _site/index.html and _site/benchmarks.json
  python scripts/build_site.py --out some/dir # write somewhere else

Preview locally:  python -m http.server -d _site
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from build_readme import ROOT, SCHEMA, load_entries, newest_first

SITE_DIR = ROOT / "site"
PLACEHOLDER = "__REGISTRY_DATA__"
REPO_URL = "https://github.com/Fengzdadi/memory-bench-registry"


def build_payload() -> dict:
    schema = json.loads(SCHEMA.read_text())
    return {
        "repo": REPO_URL,
        "types": schema["$defs"]["memory_type"]["enum"],
        "levels": schema["properties"]["repro_level"]["enum"],
        "entries": newest_first(load_entries()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=ROOT / "_site", help="output directory (default: _site)")
    args = parser.parse_args()

    payload = build_payload()
    template = (SITE_DIR / "index.html").read_text()
    if template.count(PLACEHOLDER) != 1:
        print(f"site/index.html must contain {PLACEHOLDER} exactly once", file=sys.stderr)
        return 1

    # The data sits in a <script type="application/json"> block. Escaping every "<" as < is valid
    # JSON and keeps "</script>" or "<!--" inside a string from ending or confusing the block.
    inline = json.dumps(payload, ensure_ascii=False, default=str).replace("<", "\\u003c")

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "index.html").write_text(template.replace(PLACEHOLDER, inline))
    # Same data as a standalone file, for anyone who wants to consume the registry programmatically.
    (args.out / "benchmarks.json").write_text(json.dumps(payload["entries"], ensure_ascii=False, indent=1, default=str))
    (args.out / ".nojekyll").touch()
    print(f"wrote {args.out}/index.html and benchmarks.json ({len(payload['entries'])} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
