"""Rebuild final registry entries from a fill/verify/reconcile workflow journal and write benchmarks/<slug>.yaml.

usage: python journal_to_yaml.py <journal.jsonl> <benchmarks_dir> <log_out.json> [slug ...]
"""
import json
import sys
from pathlib import Path

import yaml

journal, out_dir, log_out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
only = set(sys.argv[4:])

labels, results = {}, {}
for line in journal.read_text().splitlines():
    j = json.loads(line)
    if j["type"] == "started":
        labels[j["key"]] = j["label"]
    elif j["type"] == "result":
        results[labels.get(j["key"], j["key"])] = j.get("result")

slugs = sorted({lab.split(":", 1)[1] for lab in results if lab.startswith("fill:")})
ORDER = ["name", "slug", "release_date", "venue", "memory_types", "links", "scale", "metrics", "judge_model",
         "repro_level", "repro_checked_at", "run_records", "notes", "sources"]


class Dumper(yaml.SafeDumper):
    pass


def str_rep(d, s):
    style = "|" if "\n" in s else None
    return d.represent_scalar("tag:yaml.org,2002:str", s, style=style)


Dumper.add_representer(str, str_rep)

# neutral voice for registry-side observations (agents sometimes wrote in first person)
PHRASES = [
    ("but I counted 1,427 QA items in it, not 1,209", "but a registry count of it gives 1,427 QA items, not 1,209"),
    ("holds 1,427 QA items by my count", "holds 1,427 QA items (registry count)"),
    ("(I counted 44 of 401", "(registry check: 44 of 401"),
    ("I recounted locomo10.json and got the same", "A registry recount of locomo10.json gives the same"),
    ("The released MemData files I checked hold", "The released MemData files checked by the registry hold"),
    ("Our own arithmetic on", "Registry arithmetic on"),
    ("These counts come from our inspection, not from the paper.", "These counts come from the registry's inspection, not from the paper."),
]


def neutral(obj):
    if isinstance(obj, str):
        for a, b in PHRASES:
            obj = obj.replace(a, b)
        return obj
    if isinstance(obj, list):
        return [neutral(x) for x in obj]
    if isinstance(obj, dict):
        return {k: neutral(v) for k, v in obj.items()}
    return obj


# candidate slugs whose verified benchmark name turned out different
SLUG_RENAME = {"the-agent-s-first-day": "traineebench"}

# warnings reviewed by hand and judged to be caveats rather than reasons to exclude
ACCEPTED_WARNINGS = {
    "agent-memory-bench",  # no paper, but official repo + HF dataset exist; links.paper stays null
}

log = {}
for slug in slugs:
    if only and slug not in only:
        continue
    fill = results.get(f"fill:{slug}")
    rec = results.get(f"reconcile:{slug}")
    ver = results.get(f"verify:{slug}")
    final = rec or fill
    if not final:
        print("missing", slug)
        continue
    entry = {k: final.get(k) for k in ORDER if k not in ("run_records",)}
    slug = SLUG_RENAME.get(slug, slug)
    entry["slug"] = slug
    entry["run_records"] = []
    entry["links"] = {k: entry["links"].get(k) for k in ("paper", "code", "data")}
    entry["scale"] = {k: entry["scale"].get(k) for k in ("conversations", "questions", "avg_context_length", "notes")}
    # fold non-schema source keys into the schema field they document
    SRC_ALIAS = {"repro_checked_at": "repro_level", "name_title": "name", "title": "name"}
    VALID_SRC = {"name", "release_date", "venue", "memory_types", "links.paper", "links.code", "links.data", "scale.conversations",
                 "scale.questions", "scale.avg_context_length", "scale.notes", "metrics", "judge_model", "repro_level", "notes"}
    srcs = {}
    for k, v in (entry.get("sources") or {}).items():
        if not v or k == "registry_warning":
            continue
        k2 = SRC_ALIAS.get(k, k)
        if k2 not in VALID_SRC:
            k2 = "notes"
        srcs[k2] = f"{srcs[k2]}; {v}" if k2 in srcs else v
    entry["sources"] = srcs
    if entry["repro_level"] == "unverified":
        entry["repro_checked_at"] = None
    entry = neutral({k: entry[k] for k in ORDER})
    text = yaml.dump(entry, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=10**9, default_flow_style=False)
    warning = final.get("registry_warning")
    if slug in ACCEPTED_WARNINGS:
        warning = None
    if warning:
        # candidate flagged as not belonging in the registry: park it for review instead of publishing it
        (log_out.parent / "quarantine").mkdir(exist_ok=True)
        (log_out.parent / "quarantine" / f"{slug}.yaml").write_text(text)
    else:
        (out_dir / f"{slug}.yaml").write_text(text)
    log[slug] = {
        "reconciled": rec is not None,
        "warning": final.get("registry_warning"),
        "disputes": [c for c in (ver or {}).get("checks", []) if c["status"] != "ok"],
        "repro_evidence": final.get("repro_evidence"),
        "draft_vs_final": {k: [fill.get(k), final.get(k)] for k in ORDER if k in fill and fill.get(k) != final.get(k)} if rec else {},
    }
    print("QUARANTINED" if warning else "wrote", slug, entry["repro_level"], "(reconciled)" if rec else "", warning or "")
log_out.write_text(json.dumps(log, indent=1, ensure_ascii=False))
