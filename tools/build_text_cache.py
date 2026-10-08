"""Build or refresh the committed PDF text cache under paper_text/.

Mirrors every papers/<paper-dir>/<name>.pdf as paper_text/<paper-dir>/<name>.txt
(UTF-8, LF line endings, "===== PAGE n OF total =====" page markers) and records
source/cache hashes and page counts in paper_text/manifest.json. Existing cache
text is reused whenever the source PDF SHA-256 and the cached text SHA-256 still
match the manifest, so rerunning without changes leaves the tree untouched.

PDFs whose font descriptors pypdf cannot parse (e.g. some Nature/Cell downloads
with more than one /FontFile) fall back to pdfplumber; the manifest records which
extractor produced each entry.

Usage: python tools/build_text_cache.py
"""

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

import pypdf
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "papers"
CACHE_ROOT = ROOT / "paper_text"
MANIFEST_PATH = CACHE_ROOT / "manifest.json"

CACHE_FORMAT = 1
PAGE_MARKER = "===== PAGE n OF total ====="
EXTRACTOR = f"pypdf {pypdf.__version__}"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def extract(source: Path, target: Path) -> dict:
    reader = PdfReader(source)
    pages = len(reader.pages)
    pages_with_text = 0
    replacement_characters = 0
    parts = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages_with_text += 1
        replacement_characters += text.count("\ufffd")
        parts.append(f"\n\n===== PAGE {index} OF {pages} =====\n\n")
        parts.append(text)
    target.parent.mkdir(parents=True, exist_ok=True)
    # newline="" keeps "\n" as-is instead of translating to CRLF on Windows.
    with target.open("w", encoding="utf-8", newline="") as handle:
        handle.write("".join(parts))
    return {
        "pages": pages,
        "pages_with_text": pages_with_text,
        "replacement_characters": replacement_characters,
        "cache_bytes": target.stat().st_size,
    }


def extract_with_pdfplumber(source: Path, target: Path) -> dict:
    import pdfplumber

    pages_with_text = 0
    replacement_characters = 0
    parts = []
    with pdfplumber.open(source) as pdf:
        pages = len(pdf.pages)
        for index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages_with_text += 1
            replacement_characters += text.count("\ufffd")
            parts.append(f"\n\n===== PAGE {index} OF {pages} =====\n\n")
            parts.append(text)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        handle.write("".join(parts))
    return {
        "pages": pages,
        "pages_with_text": pages_with_text,
        "replacement_characters": replacement_characters,
        "cache_bytes": target.stat().st_size,
    }


def main() -> None:
    old_manifest = {}
    if MANIFEST_PATH.exists():
        old_manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        old_documents = {
            entry["source_relative"]: entry
            for entry in old_manifest.get("documents", [])
        }
    else:
        old_documents = {}

    documents = []
    regenerated = 0
    for source in sorted(PAPERS_DIR.rglob("*.pdf")):
        source_relative = source.relative_to(ROOT).as_posix()
        target = CACHE_ROOT / source.relative_to(PAPERS_DIR).with_suffix(".txt")
        cache_relative = target.relative_to(ROOT).as_posix()
        source_sha = sha256_of(source)

        old = old_documents.get(source_relative)
        if (
            old
            and old.get("source_sha256") == source_sha
            and target.exists()
            and sha256_of(target) == old.get("cache_sha256")
        ):
            entry = dict(old)
            status = "reused"
        else:
            try:
                stats = extract(source, target)
                extractor = EXTRACTOR
                status = "extracted"
            except Exception:
                import pdfplumber

                stats = extract_with_pdfplumber(source, target)
                extractor = f"pdfplumber {pdfplumber.__version__}"
                status = "extracted-fallback"
            entry = {
                "source_relative": source_relative,
                "source_sha256": source_sha,
                "extractor": extractor,
                "pages": stats["pages"],
                "pages_with_text": stats["pages_with_text"],
                "replacement_characters": stats["replacement_characters"],
                "cache_text": cache_relative,
                "cache_bytes": stats["cache_bytes"],
                "cache_sha256": sha256_of(target),
            }
            regenerated += 1
        documents.append(entry)
        print(f"{status}\t{entry['pages']} pp\t{cache_relative}")

    expected = {
        entry["cache_text"] for entry in documents
    }
    for stale in sorted(CACHE_ROOT.rglob("*.txt")):
        if stale.relative_to(ROOT).as_posix() not in expected:
            print(f"orphan\t(no source PDF)\t{stale.relative_to(ROOT).as_posix()}")

    manifest = {
        "cache_format": CACHE_FORMAT,
        "encoding": "UTF-8",
        "page_marker": PAGE_MARKER,
        "cache_root": CACHE_ROOT.name,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "document_count": len(documents),
        "documents": documents,
    }
    if documents == old_manifest.get("documents") and not regenerated:
        print(f"up to date: {len(documents)} documents, nothing regenerated")
        return
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(f"manifest written: {len(documents)} documents, {regenerated} regenerated")


if __name__ == "__main__":
    main()
