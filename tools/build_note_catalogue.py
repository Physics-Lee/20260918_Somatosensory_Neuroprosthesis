"""Build the machine-readable catalogue JSON that accompanies the all-papers note.

Extracts the paper data embedded in
notes/20260918_somatosensory_neuroprosthesis_all_papers_collected_by_zcode.html
(<script type="application/json" id="papers-data">, compact short keys) and rewrites
it with self-describing field names into
notes/20260918_somatosensory_neuroprosthesis_catalogue.json — same convention as the
speech-neuroprosthesis archive's 20260915_braingate_after_t11_catalogue.json. Local
PDF paths are normalized from note-relative ("../papers/...") to repo-relative
("papers/..."). Rerun after editing the note's embedded data; the JSON is always
regenerated from the HTML, so the two cannot drift.

Usage: python tools/build_note_catalogue.py
"""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "notes"
NOTE_GLOB = "*_all_papers_collected_by_zcode.html"
DATA_BLOCK_RE = re.compile(
    r'<script type="application/json" id="papers-data">(.*?)</script>', re.DOTALL
)

ROUTE_LABELS = {
    "icms": "人体皮层内刺激（ICMS）",
    "animal": "动物基础研究",
    "pns": "外周神经刺激",
    "scs": "脊髓刺激",
}


def repo_relative(note_path: str) -> str:
    return note_path.removeprefix("../")


def build_entry(raw: dict) -> dict:
    entry = {
        "date": raw["d"],
        "journal": raw["src"],
        "people": raw["pp"],
        "category": raw["c"],
        "route": raw["era"],
        "route_label": ROUTE_LABELS[raw["era"]],
        "title": raw["zh"],
        "summary": raw["n"],
    }
    if raw.get("m"):
        entry["method"] = raw["m"]
    if raw.get("r"):
        entry["takeaway"] = raw["r"]
    entry["data_status"] = raw["ds"]
    if raw.get("dn"):
        entry["data_note"] = raw["dn"]
    if raw.get("dp"):
        entry["data_platform"] = raw["dp"]
    if raw.get("dl"):
        entry["data_link"] = raw["dl"]
    if raw.get("sz"):
        entry["dataset_size_gb"] = raw["sz"]
    if raw.get("szb"):
        entry["dataset_size_bytes"] = raw["szb"]
    entry["url"] = raw["u"]
    # null marks "checked, no local copy" (Romo 1998, paywalled); see its data_note.
    entry["file"] = repo_relative(raw["f"]) if raw.get("f") else None
    if raw.get("sup"):
        entry["supplement"] = [
            {"file": repo_relative(item["p"]), "label": item["l"]} for item in raw["sup"]
        ]
    entry["authors"] = raw["a"]
    entry["title_en"] = raw["t"]
    entry["english"] = f"{raw['a']} - {raw['t']}"
    return entry


def main() -> None:
    notes = sorted(NOTES_DIR.glob(NOTE_GLOB))
    if len(notes) != 1:
        sys.exit(f"expected exactly one note matching {NOTE_GLOB}, found {len(notes)}")
    note = notes[0]
    html = note.read_text(encoding="utf-8")
    match = DATA_BLOCK_RE.search(html)
    if not match:
        sys.exit(f"no #papers-data JSON block found in {note.name}")
    raw_entries = json.loads(match.group(1))

    catalogue = [build_entry(raw) for raw in raw_entries]

    missing = [
        path
        for entry in catalogue
        for path in (
            [entry["file"]] if entry["file"]
            else []
        ) + [item["file"] for item in entry.get("supplement", [])]
        if not (ROOT / path).exists()
    ]
    for path in missing:
        print(f"WARNING: referenced file missing on disk: {path}")

    status_counts = {}
    route_counts = {}
    for entry in catalogue:
        status_counts[entry["data_status"]] = status_counts.get(entry["data_status"], 0) + 1
        route_counts[entry["route"]] = route_counts.get(entry["route"], 0) + 1

    out_path = NOTES_DIR / f"{note.stem.split('_all_papers')[0]}_catalogue.json"
    out_path.write_text(
        json.dumps(catalogue, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(f"catalogue written: {out_path.name} ({len(catalogue)} papers)")
    print(
        "data status: "
        + ", ".join(f"{k}={v}" for k, v in sorted(status_counts.items()))
    )
    print("routes: " + ", ".join(f"{k}={v}" for k, v in sorted(route_counts.items())))
    if missing:
        print(f"{len(missing)} referenced file(s) missing (see warnings above)")


if __name__ == "__main__":
    main()
