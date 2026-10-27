"""Shared plumbing for ``CS221_Mini_Projects.ipynb``.

Every assignment ships its own starter code, and several of them reuse the same
module names (``submission``, ``util``, ``grader``, ``graderUtil``...).  Importing
two of them into one Python process would silently mix them up, so the notebook
never imports an assignment module directly.  Instead each section calls
:func:`use_assignment`, which

1. evicts every module previously imported from ``assignments/`` out of
   ``sys.modules``,
2. puts the chosen assignment folder first on ``sys.path``, and
3. ``chdir``s into it, because the starter code opens data files with relative
   paths (``polarity.train``, ``data/stanford.pbf``, ``layouts/``...).

The official graders call ``sys.exit`` and read ``sys.argv``, so
:func:`run_grader` runs them in a child process with the notebook's interpreter.
"""

from __future__ import annotations

import importlib
import inspect
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSIGNMENTS_ROOT = REPO_ROOT / "assignments"
FIGURES_ROOT = REPO_ROOT / "report" / "figures"


@dataclass(frozen=True)
class Assignment:
    number: int
    slug: str    # folder name under assignments/ and report/figures/
    title: str

    @property
    def path(self) -> Path:
        return ASSIGNMENTS_ROOT / self.slug

    @property
    def figures(self) -> Path:
        return FIGURES_ROOT / self.slug


ASSIGNMENTS = {
    1: Assignment(1, "01_foundations", "Foundations"),
    2: Assignment(2, "02_sentiment", "Sentiment Classification"),
    3: Assignment(3, "03_route", "Route Planning"),
    4: Assignment(4, "04_mountaincar", "Controlling MountainCar"),
    5: Assignment(5, "05_pacman", "Pac-Man"),
    6: Assignment(6, "06_bayesian", "Bayesian Networks (Car Tracking)"),
    7: Assignment(7, "07_logic", "From Language to Logic"),
}


def _is_assignment_module(module: ModuleType) -> bool:
    file = getattr(module, "__file__", None)
    if not file:
        return False
    try:
        Path(file).resolve().relative_to(ASSIGNMENTS_ROOT)
        return True
    except ValueError:
        return False


def use_assignment(number: int) -> Assignment:
    """Make assignment ``number`` the active one for imports and relative paths."""
    a = ASSIGNMENTS[number]
    for name, module in list(sys.modules.items()):
        if module is not None and _is_assignment_module(module):
            del sys.modules[name]
    sys.path[:] = [p for p in sys.path if not _inside(p, ASSIGNMENTS_ROOT)]
    sys.path.insert(0, str(a.path))
    os.chdir(a.path)
    importlib.invalidate_caches()
    a.figures.mkdir(parents=True, exist_ok=True)
    print(f"Active: Assignment {a.number} - {a.title}  ({a.path.relative_to(REPO_ROOT)})")
    return a


def _inside(path: str, root: Path) -> bool:
    try:
        Path(path).resolve().relative_to(root)
        return True
    except (ValueError, OSError):
        return False


def load(module_name: str = "submission") -> ModuleType:
    """Freshly import ``module_name`` from the active assignment (picks up edits)."""
    if module_name in sys.modules:
        return importlib.reload(sys.modules[module_name])
    return importlib.import_module(module_name)


def run_grader(number: int, *test_ids: str, timeout: int | None = 600) -> int:
    """Run the official ``grader.py`` of assignment ``number``.

    ``grader.py`` accepts one exact part name per run (e.g. ``"3a-0-basic"``), so each
    id is run separately.  With no ``test_ids`` the whole grader runs (hidden tests are
    skipped locally).  Returns the number of runs that *crashed*: the graders exit 0
    even when tests fail, so read the printed points to judge correctness.
    """
    failures = 0
    for args in ([[t] for t in test_ids] or [[]]):
        failures += run_script(number, "grader.py", *args, timeout=timeout) != 0
    return failures


def run_script(number: int, *args: str, timeout: int | None = 3600) -> int:
    """Run a starter script (``grader.py``, ``train.py``, ``pacman.py -q``...) in a child process."""
    a = ASSIGNMENTS[number]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "MPLBACKEND": "Agg"}
    proc = subprocess.run([sys.executable, *args], cwd=a.path, env=env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout)
    print(proc.stdout, end="")
    if proc.stderr.strip():
        print(proc.stderr, end="", file=sys.stderr)
    return proc.returncode


def show_source(*objects) -> None:
    """Pretty-print the source of functions/classes so the implementation is visible in the notebook."""
    from IPython.display import Code, display
    for obj in objects:
        display(Code(inspect.getsource(obj), language="python"))


def environment_report() -> None:
    """Print interpreter and package versions (the graders expect Python 3.12)."""
    print(f"Python {sys.version.split()[0]}  ({sys.executable})")
    if sys.version_info[:2] != (3, 12):
        print("  WARNING: CS221 graders expect Python 3.12 - see README.md 'Setup'.")
    for pkg in ("numpy", "matplotlib", "gymnasium", "pygame", "osmium", "plotly", "pandas"):
        try:
            mod = importlib.import_module(pkg)
            print(f"  {pkg:<11} {getattr(mod, '__version__', 'installed')}")
        except Exception as exc:  # noqa: BLE001 - report anything that blocks the import
            print(f"  {pkg:<11} MISSING ({type(exc).__name__})")
    try:
        import tkinter  # noqa: F401 - Pac-Man and car tracking GUIs need Tk
        print("  tkinter     available")
    except ImportError:
        print("  tkinter     MISSING (needed for the Pac-Man / car GUIs, not for graders)")
