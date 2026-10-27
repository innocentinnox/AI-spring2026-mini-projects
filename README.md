# CS221 Mini Projects: Group 13

Group workspace for the seven mini projects based on the
[Stanford CS221 Spring 2026 coursework](https://stanford-cs221.github.io/spring2026/#coursework).

* **Theory** goes in one PDF, written in LaTeX in [`report/`](report/).
* **Programming** goes in one Jupyter notebook, [`notebook/CS221_Mini_Projects.ipynb`](notebook/CS221_Mini_Projects.ipynb).
* Both use the same numbering: *Assignment N, Problem k, part (x)*.
* **Deadline:** 5 December 2026, uploaded to Moodle. **Presentations:** 14–19 December 2026 on Zoom.

| No. | Assignment | Official starter | Folder |
|-----|------------|------------------|--------|
| 1 | Foundations | `hw1_foundations` | [`assignments/01_foundations`](assignments/01_foundations) |
| 2 | Sentiment Classification | `hw2_sentiment` | [`assignments/02_sentiment`](assignments/02_sentiment) |
| 3 | Route Planning | `hw3_route` | [`assignments/03_route`](assignments/03_route) |
| 4 | Controlling MountainCar | `hw4_mountaincar` | [`assignments/04_mountaincar`](assignments/04_mountaincar) |
| 5 | Pac-Man | `hw5_pacman` | [`assignments/05_pacman`](assignments/05_pacman) |
| 6 | Bayesian Networks (Car Tracking) | `hw7_car` | [`assignments/06_bayesian`](assignments/06_bayesian) |
| 7 | From Language to Logic | `hw8_logic` | [`assignments/07_logic`](assignments/07_logic) |

`hw6_scheduling` (CSPs) was downloaded but is **not** part of our assignment list. It is kept only under `problems/`.

See [`docs/ASSIGNMENTS.md`](docs/ASSIGNMENTS.md) for a breakdown of every problem: what is written, what is coded,
the required packages, and the known pitfalls.

## Final deliverables (what goes on Moodle)

> **Each team uploads ONE Python notebook and ONE PDF.** Everything in this repo exists to produce those two files.

| Upload | Built from | How |
|--------|-----------|-----|
| `CS221_Mini_Projects.ipynb` | `notebook/CS221_Mini_Projects.ipynb`, executed top to bottom with all outputs saved | Run All in Jupyter, save, then run the packaging script |
| `CS221_Mini_Projects.pdf` | `report/report.pdf`, built from `report/main.tex` + `report/sections/*.tex` | `cd report && latexmk` |

The working notebook is already the final notebook. Each problem's `show_source(...)` cell prints the full
documented implementation into the cell output, and the grader cells print the test results. Once the notebook has
been executed and saved, it contains all of the work, so no separate notebooks have to be merged.
Each member works on their own assignment section and the team **joins the work at the end** by:

1. making sure every `assignments/*/submission.py` is final and every `\todo` in `report/` is gone;
2. running the whole notebook once (Kernel > Restart & Run All) and saving it;
3. building the PDF;
4. running `python scripts/package_submission.py --name Group13_CS221_MiniProjects`, which writes
   `dist/CS221_Mini_Projects.ipynb` and `dist/CS221_Mini_Projects.pdf` (**the two files to upload**) plus a
   fallback zip with the helper code. The brief allows a zip only for teams that use helper files.

## Repository layout

```
assignments/NN_name/   working copy of each starter. We edit ONLY submission.py (between BEGIN/END_YOUR_CODE)
notebook/              CS221_Mini_Projects.ipynb + cs221_helpers.py (isolates the 7 codebases, runs graders)
report/                main.tex, preamble.tex, team.tex, sections/NN_name.tex, figures/NN_name/
report/templates/      official CS221 LaTeX templates (reference only, not compiled)
problems/              untouched extracted downloads (pristine reference; zips are git-ignored)
scripts/               package_submission.py builds the single Moodle zip
docs/                  study notes per assignment
```

## Setup

The graders expect **Python 3.12**. Note that the `python` currently on PATH on this machine is the
Espressif one (3.11), so don't use it.

```bash
conda env create -f environment.yml        # or: py -3.12 -m venv .venv && .venv\Scripts\pip install -r requirements.txt
conda activate cs221
python -m ipykernel install --user --name cs221 --display-name "Python 3.12 (cs221)"
jupyter lab notebook/CS221_Mini_Projects.ipynb
```

If `osmium` (Route Planning) fails to install, see [`assignments/03_route/README.md`](assignments/03_route/README.md).
The Pac-Man and car-tracking GUIs need `tkinter` (included with the python.org and conda builds).

**Report:** install a TeX distribution (MiKTeX or TeX Live, which both include `latexmk`), then
`cd report && latexmk` produces **`report/report.pdf`**, which is committed so the whole team can see the
current state. The auxiliary files go to `report/build/`, which is git-ignored. MiKTeX's automatic package install
(`initexmf --set-config-value [MPM]AutoInstall=1`) fetches any missing LaTeX packages on the first build.

## Workflow

1. Implement in `assignments/NN_name/submission.py`, with clear docstrings and comments, because we are graded on readability.
2. Test with `python grader.py <part>` inside that folder, or with the matching notebook cell (`run_grader(N, "3a-0-basic")`).
3. In the notebook, fill the **Approach** cell for each problem and run its experiment cells. Save figures to `report/figures/NN_name/`.
4. Write the theory in `report/sections/NN_name.tex`, inside the `solution` environments. Search for `\todo` to find what is left.
5. Keep team details identical in `report/team.tex` and the notebook's first table.
6. Package: `python scripts/package_submission.py --name Group13_CS221_MiniProjects` creates `dist/<name>.zip`.
