#!/usr/bin/env python3
"""Find candidate memory benchmarks among recent arXiv papers and write a triage digest.

Discovery only: this never touches benchmarks/. A candidate still goes through AGENTS.md
(flow B to fill it in, then flow A in a fresh session to review it).

Usage:
  python scripts/discover.py                    # scan the last 14 days and print a summary
  python scripts/discover.py --out digest.md    # also write the Markdown digest (only if something is new)
  python scripts/discover.py --since 2026-09-01 --until 2026-10-11
  python scripts/discover.py --seen earlier.txt # skip arXiv IDs that appear anywhere in this file
  python scripts/discover.py --eval             # how many entries already in benchmarks/ the matcher finds

The scan downloads every paper submitted in the window to the categories in CATEGORIES (about 5,000 a
week) and scores them locally, so the result does not depend on how arXiv's own search tokenizes words.
A paper needs an LLM/agent/robot/video setting and some memory-related topic word; RULES then add up
points for memory vocabulary, benchmark-style titles and "we introduce a benchmark" sentences. Papers
already in benchmarks/, pending/, docs/excluded.md or pending/tools/leads/ are skipped. The score is a
lead generator, not a classifier: a human or agent reads each hit before anything is written down.

Tuning RULES, LIKELY and MAYBE: change them, then run `--eval`. It reports how many papers behind the
current entries still score above MAYBE (optimistic, since the weights were fitted on them). A digest is
about 90 to 100 papers a week at the shipped thresholds (measured 2026-09-01 .. 2026-10-12).
"""
from __future__ import annotations

import argparse
import datetime as dt
import http.client
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

import yaml

ROOT = Path(__file__).resolve().parent.parent
BENCH_DIR = ROOT / "benchmarks"
PENDING_DIR = ROOT / "pending"
LEADS_DIR = PENDING_DIR / "tools" / "leads"
EXCLUDED = ROOT / "docs" / "excluded.md"

API = "https://export.arxiv.org/api/query"
USER_AGENT = "memory-bench-registry-discover (+https://github.com/Fengzdadi/memory-bench-registry)"
DELAY = 3.2  # seconds between requests; arXiv asks for at most one every 3 seconds
RETRIES = 4
PAGE = 500
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}
# Every category that lists an entry in benchmarks/ (checked 2026-10-12). Add one here if a new entry
# turns up outside these; `--eval` shows which entries the scan could not have seen.
CATEGORIES = ["cs.AI", "cs.CL", "cs.LG", "cs.CV", "cs.SE", "cs.IR", "cs.HC", "cs.MA", "cs.CR",
              "cs.RO", "cs.DB", "cs.CY", "cs.MM", "cs.ET", "eess.AS", "cs.SD"]

ARXIV_ID = re.compile(r"arxiv(?:\.org/(?:abs|pdf)/|:|\s)\s*(\d{4}\.\d{4,5})", re.IGNORECASE)
ENTRY_ID = re.compile(r"arxiv\.org/abs/(\d{4}\.\d{4,5})")
GITHUB_BODY_LIMIT = 60_000  # GitHub rejects issue bodies over 65,536 characters


class Paper(NamedTuple):
    id: str
    title: str
    summary: str
    published: str  # v1 submission date, YYYY-MM-DD
    categories: tuple[str, ...]


class Text(NamedTuple):
    title: str
    abstract: str
    both: str  # title and abstract together


class Match(NamedTuple):
    tier: str  # "likely" or "maybe"
    score: float
    why: tuple[str, ...]  # the rules that fired, strongest first


# ---- ranking rules -----------------------------------------------------------------------------
def _rx(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE)


# "memory" meaning hardware or efficiency is removed before looking for memory vocabulary.
HARDWARE = _rx(r"kv[- ]?cache|gpu memory|peak memory|\b(?:hbm|dram|sram|vram)\b|\b(?:host|device|main|on-chip) memory"
               r"|memory[- ](?:efficien\w*|footprint|bandwidth|usage|consumption|overhead|bound|wall|saving|budget"
               r"|access|hierarchy)")
# No trailing \b on "memory" so that names like MemoryBank and MemoryCode count.
MEMORY = _rx(r"\bmemor(?:y|ies)|\bmetamemory|\bremember\w*|\bforget\w*|\bunlearn\w*|\bamnesi\w*"
             r"|\b(?:knowledge|model) edit\w*")
PERSONAL = _rx(r"\bpersonali[sz]\w*|\bpersonas?\b|\buser (?:profil|model|prefer)\w*")
SESSION = _rx(r"\bmulti-?session|\bcross-?session|\bacross sessions|\blife-?long\b|\bstateful\b|\bpersistent\b"
              r"|\blong-term\W+(?:\w+\W+){0,3}(?:dialogue|conversation|interaction|chat|user|persona)"
              r"|\b(?:interaction|conversation|dialogue|chat) history")
EXPERIENCE = _rx(r"\bskills?\b|\bexperiences?\b|\bself-(?:evol|improv)\w*|\bevolv\w*|\bcontinual\w*"
                 r"|\bprocedur\w*|\bworkflows?\b|\breusable\b|\binsights?\b|\bcross-task\b")
LONG_TERM = _rx(r"\blong-term\b|\blong-horizon\b|\blife-?long\b")
AGENT = _rx(r"\bagents?\b|\bagentic\b|\bllms?\b|\blanguage models?\b|\bassistants?\b|\bchatbots?\b")
DIALOGUE = _rx(r"\bdialogue\b|\bconversation\w*|\bchat\b")
# An LLM, agent, dialogue, robot or video setting; keeps neuroscience and hardware papers out.
CONTEXT = _rx(r"\bagents?\b|\bagentic\b|\bllms?\b|\blanguage models?\b|\bassistants?\b|\bchatbots?\b|\bdialogue\b"
              r"|\bconversation\w*|\brobot\w*|\bembodied\b|\bvision-language\b|\bmultimodal\b|\bvideo\b"
              r"|\begocentric\b|\bvlms?\b|\bmllms?\b|\bvla\b|\brag\b|\bretrieval-augmented\b")
# Signs that the paper itself brings an evaluation resource.
TITLE_BENCH = _rx(r"bench|dataset|testbed|test bed|\bsuite\b|\bcorpus\b|leaderboard|\barena\b|\bgym\b")
TITLE_EVAL = _rx(r"evaluat|\bprob(?:e|ing)\b|\baudit|diagnos|assess")
RESOURCE_NOUN = (r"(?:benchmark|dataset|test ?bed|(?:test|task|evaluation) suite|suite|corpus|leaderboard|\w*bench"
                 r"|evaluation (?:framework|protocol|scheme|harness))s?")
RESOURCE = _rx(r"\b" + RESOURCE_NOUN + r"\b")
CLAIM_VERB = _rx(r"\b(?:introduc|present|propos|construct|build|built|curat|releas|develop|creat|establish|collect"
                 r"|contribut|defin|instantiat|design|formali[sz])\w*\W+(?:\w+\W+){0,10}?" + RESOURCE_NOUN + r"\b")
CLAIM_APPOS = _rx(r"\ban?\s+(?:[\w-]+\s+){0,4}?" + RESOURCE_NOUN + r"\b")
REVEAL = _rx(r"\breveal|\bstruggle|\bfall short|\bsubstantial gap|\bremain(?:s)? challenging|\bfail to\b")

# (label, test, weight). The weights are rounded log-odds from a logistic regression of the registry's
# 203 arXiv abstracts against the 4,721 other papers in CATEGORIES submitted 2026-09-01 .. 2026-10-09 that
# pass the CONTEXT and TOPICS test. In 5-fold cross-validation the refit model recovers 81% of held-out
# registry papers while listing 40 unknown papers a week, and 91% at 80 a week.
RULES: list[tuple[str, Callable[[Text], bool], float]] = [
    ("memory in title", lambda t: bool(MEMORY.search(t.title)), 1.0),
    ("memory", lambda t: bool(MEMORY.search(t.both)), 2.0),
    ("memory 3+ times", lambda t: len(MEMORY.findall(t.both)) >= 3, 1.0),
    ("bench-like title", lambda t: bool(TITLE_BENCH.search(t.title)), 1.5),
    ("eval-like title", lambda t: bool(TITLE_EVAL.search(t.title)), 0.5),
    ("introduces a benchmark", lambda t: bool(CLAIM_VERB.search(t.abstract)), 2.0),
    ("'a benchmark of'", lambda t: bool(CLAIM_APPOS.search(t.abstract)), 1.0),
    ("benchmark 2+ times", lambda t: len(RESOURCE.findall(t.abstract)) >= 2, 0.5),
    ("agent or LLM", lambda t: bool(AGENT.search(t.both)), 1.0),
    ("dialogue", lambda t: bool(DIALOGUE.search(t.both)), 0.5),
    ("long-term", lambda t: bool(LONG_TERM.search(t.both)), 1.0),
    ("multi-session", lambda t: bool(SESSION.search(t.both)), 0.5),
    ("personalization", lambda t: bool(PERSONAL.search(t.both)), 0.5),
    ("skills or experience", lambda t: bool(EXPERIENCE.search(t.both)), 0.5),
    ("reveals a gap", lambda t: bool(REVEAL.search(t.abstract)), 1.0),
]
TOPICS = (MEMORY, PERSONAL, SESSION, EXPERIENCE)  # a paper needs at least one of these, whatever its score
# Score thresholds for the two tiers of the digest. On the same corpus, 30 and 91 unknown papers a week score
# at least LIKELY and MAYBE; 79% and 93% of the registry papers do.
LIKELY, MAYBE = 8.0, 6.5


def text_of(paper: Paper) -> Text:
    return Text(HARDWARE.sub(" ", paper.title), paper.summary, HARDWARE.sub(" ", f"{paper.title}. {paper.summary}"))


def classify(paper: Paper) -> Match | None:
    text = text_of(paper)
    if not CONTEXT.search(text.both) or not any(topic.search(text.both) for topic in TOPICS):
        return None
    fired = [(weight, label) for label, test, weight in RULES if test(text)]
    score = sum(weight for weight, _ in fired)
    if score < MAYBE:
        return None
    why = tuple(label for _, label in sorted(fired, key=lambda f: -f[0])[:4])
    return Match("likely" if score >= LIKELY else "maybe", score, why)


# ---- arXiv client ------------------------------------------------------------------------------
class Arxiv:
    """Minimal client for the arXiv Atom API: one request at a time, spaced DELAY seconds apart."""

    def __init__(self) -> None:
        self._last = 0.0

    def get(self, **params) -> ET.Element:
        url = f"{API}?{urllib.parse.urlencode(params)}"
        failure: Exception | None = None
        for attempt in range(1, RETRIES + 1):
            pause = DELAY - (time.monotonic() - self._last)
            if pause > 0:
                time.sleep(pause)
            self._last = time.monotonic()
            try:
                request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(request, timeout=90) as response:
                    return ET.fromstring(response.read())
            except (OSError, http.client.HTTPException, ET.ParseError) as exc:  # URLError and timeouts are OSErrors
                failure = exc
                print(f"  arXiv API error on try {attempt}/{RETRIES}: {exc}", file=sys.stderr)
                if attempt < RETRIES:
                    time.sleep(10 * attempt)
        raise RuntimeError(f"arXiv API failed after {RETRIES} tries: {failure}")


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_papers(feed: ET.Element) -> list[Paper]:
    papers = []
    for entry in feed.findall("atom:entry", NS):
        url = entry.findtext("atom:id", "", NS)
        if "/api/errors" in url:  # malformed queries come back as a single entry pointing here
            raise RuntimeError(f"arXiv API error: {squash(entry.findtext('atom:summary', '', NS))}")
        found = ENTRY_ID.search(url)
        if not found:
            continue
        papers.append(Paper(
            id=found.group(1),
            title=squash(entry.findtext("atom:title", "", NS)),
            summary=squash(entry.findtext("atom:summary", "", NS)),
            published=entry.findtext("atom:published", "", NS)[:10],
            categories=tuple(c.get("term", "") for c in entry.findall("atom:category", NS)),
        ))
    return papers


def fetch_pages(client: Arxiv, **params) -> list[Paper]:
    """Read every page of a query. Fails rather than returning a partial list."""
    papers: list[Paper] = []
    while True:
        feed = client.get(start=len(papers), max_results=PAGE, **params)
        total = int(feed.findtext("opensearch:totalResults", "0", NS))
        page = parse_papers(feed)
        papers += page
        if len(papers) >= total:
            return papers
        if not page:
            raise RuntimeError(f"arXiv returned an empty page after {len(papers)} of {total} results")


def fetch_window(client: Arxiv, since: dt.date, until: dt.date) -> list[Paper]:
    """All papers first submitted from `since` through `until` (UTC, inclusive) in CATEGORIES."""
    categories = " OR ".join(f"cat:{c}" for c in CATEGORIES)
    papers: dict[str, Paper] = {}
    day = since
    while day <= until:  # one query per day keeps each result set small enough to page through reliably
        stamp = day.strftime("%Y%m%d")
        query = f"({categories}) AND submittedDate:[{stamp}0000 TO {stamp}2359]"
        batch = fetch_pages(client, search_query=query, sortBy="submittedDate", sortOrder="ascending")
        print(f"  {day}: {len(batch)} papers", file=sys.stderr)
        papers.update((p.id, p) for p in batch)
        day += dt.timedelta(days=1)
    return list(papers.values())


def fetch_by_id(client: Arxiv, ids: list[str]) -> dict[str, Paper]:
    found: dict[str, Paper] = {}
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        found.update((p.id, p) for p in fetch_pages(client, id_list=",".join(chunk)))
    return found


# ---- what the registry already knows -----------------------------------------------------------
def arxiv_ids(text: str) -> set[str]:
    return set(ARXIV_ID.findall(text))


def load_yaml(path: Path) -> dict:
    try:
        doc = yaml.safe_load(path.read_text())
    except yaml.YAMLError:
        return {}  # a half-written draft must not stop discovery
    return doc if isinstance(doc, dict) else {}


def paper_ids(doc: dict) -> set[str]:
    return arxiv_ids(str((doc.get("links") or {}).get("paper") or ""))


def known_ids() -> set[str]:
    ids: set[str] = set()
    for path in [*BENCH_DIR.glob("*.yaml"), *PENDING_DIR.rglob("*.yaml")]:
        ids |= paper_ids(load_yaml(path))
    ids |= arxiv_ids(EXCLUDED.read_text())
    for path in LEADS_DIR.glob("*.json"):
        leads = json.loads(path.read_text()).get("leads", {})
        ids |= arxiv_ids(f"{leads.get('registry_key') or ''} {leads.get('paper_hint') or ''}")
    return ids


# ---- digest ------------------------------------------------------------------------------------
def md_text(text: str, limit: int = 170) -> str:
    """Make arXiv-supplied text inert in GitHub Markdown: no mentions, issue references, links or HTML."""
    if len(text) > limit:
        text = text[:limit].rstrip() + "…"
    text = text.replace("&", "&amp;")
    text = re.sub(r"([\\`*_\[\]<>~$])", r"\\\1", text)
    return text.replace("@", "＠").replace("#", "＃")


def render_line(paper: Paper, match: Match) -> str:
    cats = ", ".join(paper.categories[:3])
    return (f"- [ ] [{paper.id}](https://arxiv.org/abs/{paper.id}) **{md_text(paper.title)}**"
            f" · {cats} · {paper.published} · score {match.score:g}: {', '.join(match.why)}")


def render_digest(window: str, scanned: int, known: int, hits: list[tuple[Paper, Match]], limit: int) -> str:
    likely = [h for h in hits if h[1].tier == "likely"]
    maybe = [h for h in hits if h[1].tier == "maybe"]

    def body(keep: int) -> str:
        shown_likely = likely[:keep]
        shown_maybe = maybe[:max(0, keep - len(shown_likely))]
        lines = [
            f"Window {window} (UTC). Scanned {scanned:,} papers; {known} were skipped because they are already in "
            f"the registry, pending drafts, docs/excluded.md or an earlier digest. {len(hits)} new matches.",
            "",
            "Papers are ranked by a keyword score over the title and abstract (see RULES in scripts/discover.py), "
            "so treat them as leads, not facts. Tick the ones worth adding; each ticked paper then goes through "
            "AGENTS.md flow B (fill) and flow A (review).",
            "",
            f"## Likely ({len(likely)})",
            "",
            *[render_line(p, m) for p, m in shown_likely],
            "",
            f"## Maybe ({len(maybe)})",
            "",
            "Lower scores. Skim these after the Likely list.",
            "",
            "<details>",
            f"<summary>Show the list ({len(maybe)})</summary>",
            "",
            *[render_line(p, m) for p, m in shown_maybe],
            "",
            "</details>",
        ]
        hidden = len(hits) - len(shown_likely) - len(shown_maybe)
        if hidden:
            lines += ["", f"{hidden} lower-ranked matches were not listed."]
        return "\n".join(lines) + "\n"

    keep = min(limit, len(hits))
    while len(body(keep)) > GITHUB_BODY_LIMIT and keep > 0:
        keep = max(0, keep - 10)  # too long for a GitHub issue: drop the lowest-ranked entries
    return body(keep)


# ---- eval --------------------------------------------------------------------------------------
def evaluate(client: Arxiv) -> int:
    """Run the matcher over the arXiv papers behind benchmarks/ and report what it would have missed."""
    entries = []
    for path in sorted(BENCH_DIR.glob("*.yaml")):
        doc = load_yaml(path)
        ids = sorted(paper_ids(doc))
        if ids:
            entries.append((doc, ids[0]))
    papers = fetch_by_id(client, [i for _, i in entries])

    results = []
    for doc, arxiv_id in entries:
        paper = papers.get(arxiv_id)
        if paper is None:
            print(f"  not returned by arXiv: {doc['slug']} ({arxiv_id})", file=sys.stderr)
            continue
        results.append((doc, paper, classify(paper), not set(paper.categories) & set(CATEGORIES)))

    found = [r for r in results if r[2]]
    print(f"{len(results)} entries with an arXiv paper; the matcher finds {len(found)} "
          f"({len(found) / len(results):.0%}): {sum(r[2].tier == 'likely' for r in found)} likely, "
          f"{sum(r[2].tier == 'maybe' for r in found)} maybe")
    print(f"Outside CATEGORIES (the scan would never see them): {sum(r[3] for r in results)}")
    print("(The weights were fitted on these papers, so this recall is optimistic for new ones.)")
    print("\nBy memory type (entries can have several):")
    totals, hits = Counter(), Counter()
    for doc, _, match, _ in results:
        for t in doc["memory_types"]:
            totals[t] += 1
            hits[t] += bool(match)
    for t, n in totals.most_common():
        print(f"  {t:<24}{hits[t]:>3}/{n:<3} {hits[t] / n:.0%}")
    print("\nMissed:")
    for doc, paper, match, outside in results:
        if not match:
            print(f"  {paper.id}  {doc['name']}  [{', '.join(doc['memory_types'])}]{'  (category)' if outside else ''}")
    return 0


# ---- main --------------------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--days", type=int, default=14, help="scan this many days back, including today (default: 14)")
    parser.add_argument("--since", type=dt.date.fromisoformat, help="first day to scan, YYYY-MM-DD (overrides --days)")
    parser.add_argument("--until", type=dt.date.fromisoformat, help="last day to scan (default: today, UTC)")
    parser.add_argument("--seen", type=Path, help="text file; every arXiv ID in it is skipped (e.g. earlier digests)")
    parser.add_argument("--out", type=Path, help="write the Markdown digest here if there is anything new")
    parser.add_argument("--limit", type=int, default=250, help="most matches to list in the digest (default: 250)")
    parser.add_argument("--eval", action="store_true", help="check the matcher against benchmarks/ instead of scanning")
    args = parser.parse_args()

    client = Arxiv()
    if args.eval:
        return evaluate(client)

    until = args.until or dt.datetime.now(dt.timezone.utc).date()
    since = args.since or until - dt.timedelta(days=args.days - 1)
    print(f"Scanning arXiv {since} to {until}", file=sys.stderr)
    papers = fetch_window(client, since, until)
    if not papers:
        print("arXiv returned no papers for this window; refusing to report an empty scan", file=sys.stderr)
        return 1

    known = known_ids()
    if args.seen:
        known |= arxiv_ids(args.seen.read_text())
    already = sum(p.id in known for p in papers)
    hits = [(p, m) for p in papers if p.id not in known and (m := classify(p))]
    hits.sort(key=lambda h: h[0].id, reverse=True)  # roughly newest first
    hits.sort(key=lambda h: -h[1].score)  # stable: best score first

    counts = Counter(m.tier for _, m in hits)
    print(f"Scanned {len(papers):,} papers; {already} already known; "
          f"{counts['likely']} likely and {counts['maybe']} maybe new matches")
    if hits and args.out:
        args.out.write_text(render_digest(f"{since} to {until}", len(papers), already, hits, args.limit))
        print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
