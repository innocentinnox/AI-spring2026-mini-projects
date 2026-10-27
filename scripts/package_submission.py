"""Build the final Moodle deliverables.

Each team uploads ONE notebook and ONE PDF. This script copies them to

    dist/CS221_Mini_Projects.ipynb   (run the whole notebook and save it first)
    dist/CS221_Mini_Projects.pdf     (build with `cd report && latexmk` first)

and also builds a fallback zip, because the brief asks teams that use helper
code to zip everything into one file that includes the team details:

    <name>/notebook/CS221_Mini_Projects.ipynb   the notebook (team details in its first cells)
    <name>/notebook/cs221_helpers.py            helper module (must sit next to the notebook)
    <name>/CS221_Mini_Projects.pdf              report/report.pdf (team details on the title page)
    <name>/assignments/...                      starter code + our submission.py files
    <name>/README.md, requirements.txt, environment.yml

Usage (from the repo root):
    python scripts/package_submission.py --name Team07_CS221_MiniProjects
"""

from __future__ import annotations

import argparse
import shutil
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
    parser.add_argument("--name", default="Group13_CS221_MiniProjects", help="zip / top-level folder name")
    parser.add_argument("--allow-missing-pdf", action="store_true", help="package even if the PDF is not built")
    args = parser.parse_args()

    pdf = ROOT / "report" / "report.pdf"
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

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    # The two files that are actually uploaded.
    shutil.copy2(ROOT / "notebook" / "CS221_Mini_Projects.ipynb", dist / "CS221_Mini_Projects.ipynb")
    if pdf.exists():
        shutil.copy2(pdf, dist / "CS221_Mini_Projects.pdf")
    print("upload: dist/CS221_Mini_Projects.ipynb" + ("  +  dist/CS221_Mini_Projects.pdf" if pdf.exists() else ""))

    out = dist / f"{args.name}.zip"
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for src, arc in entries:
            zf.write(src, f"{args.name}/{arc}")
    print(f"fallback zip: {out.relative_to(ROOT)}  ({len(entries)} files, {out.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
