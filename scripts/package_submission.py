"""Build the single zip uploaded to Moodle.

The course instructions say that teams using helper code next to their notebook
must zip everything into one file that includes the team details. This script
collects:

    <name>/notebook/CS221_Mini_Projects.ipynb   the notebook (team details in its first cells)
    <name>/notebook/cs221_helpers.py            helper module (must sit next to the notebook)
    <name>/CS221_Mini_Projects.pdf              report/build/main.pdf (team details on the title page)
    <name>/assignments/...                      starter code + our submission.py files
    <name>/README.md, requirements.txt, environment.yml

Usage (from the repo root):
    python scripts/package_submission.py --name Team07_CS221_MiniProjects
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_PARTS = {"__pycache__", ".ipynb_checkpoints", ".DS_Store", "__MACOSX"}


def iter_files(base: Path):
    for path in sorted(base.rglob("*")):
        if path.is_file() and not SKIP_PARTS.intersection(path.parts):
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--name", default="CS221_MiniProjects", help="zip / top-level folder name")
    parser.add_argument("--allow-missing-pdf", action="store_true", help="package even if the PDF is not built")
    args = parser.parse_args()

    pdf = ROOT / "report" / "build" / "main.pdf"
    if not pdf.exists() and not args.allow_missing_pdf:
        print(f"error: {pdf.relative_to(ROOT)} not found - build the report first (cd report && latexmk)",
              file=sys.stderr)
        return 1

    entries: list[tuple[Path, str]] = [
        (ROOT / "notebook" / "CS221_Mini_Projects.ipynb", "notebook/CS221_Mini_Projects.ipynb"),
        (ROOT / "notebook" / "cs221_helpers.py", "notebook/cs221_helpers.py"),
        (ROOT / "README.md", "README.md"),
        (ROOT / "requirements.txt", "requirements.txt"),
        (ROOT / "environment.yml", "environment.yml"),
    ]
    if pdf.exists():
        entries.append((pdf, "CS221_Mini_Projects.pdf"))
    entries += [(p, p.relative_to(ROOT).as_posix()) for p in iter_files(ROOT / "assignments")]

    out = ROOT / "dist" / f"{args.name}.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for src, arc in entries:
            zf.write(src, f"{args.name}/{arc}")
    print(f"wrote {out.relative_to(ROOT)}  ({len(entries)} files, {out.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
