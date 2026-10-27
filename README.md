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
| `CS221_Mini_Projects.ipynb` | `notebook/CS221_Mini_Projects.ipynb`, executed top to bottom with all outputs saved | Run All in Jupyter, save, then `make package` |
| `CS221_Mini_Projects.pdf` | `report/report.pdf`, built from `report/main.tex` + `report/sections/*.tex` | `make report` (also run by `make package`) |

The working notebook is already the final notebook. Each problem's `show_source(...)` cell prints the full
documented implementation into the cell output, and the grader cells print the test results. Once the notebook has
been executed and saved, it contains all of the work, so no separate notebooks have to be merged.
Each member works on their own assignment section and the team **joins the work at the end** by:

1. making sure every `assignments/*/submission.py` is final and every `\todo` in `report/` is gone;
2. running the whole notebook once (Kernel > Restart & Run All) and saving it;
3. running `make package`, which rebuilds the PDF and writes
   `dist/CS221_Mini_Projects.ipynb` and `dist/CS221_Mini_Projects.pdf` (**the two files to upload**) plus a
   fallback zip with the helper code. The brief allows a zip only for teams that use helper files.

## Repository layout

```
assignments/NN_name/   working copy of each starter. We edit ONLY submission.py (between BEGIN/END_YOUR_CODE)
notebook/              CS221_Mini_Projects.ipynb + cs221_helpers.py (isolates the 7 codebases, runs graders)
report/                main.tex, preamble.tex, team.tex, sections/NN_name.tex, figures/NN_name/
report/templates/      official CS221 LaTeX templates (reference only, not compiled)
problems/              untouched extracted downloads (pristine reference; zips are git-ignored)
scripts/               package_submission.py builds the Moodle upload files (dist/)
Makefile               shortcuts: make report / test / notebook / package / env
docs/                  study notes per assignment
```

## Quick start

```powershell
make report                                   # build report/report.pdf
make test A=02_sentiment T=3a-0-basic         # run one grader test (omit T= to run them all)
make notebook                                 # open the notebook
make package                                  # build the two files to upload, in dist/
make help                                     # list every command
```

## One-time setup on Windows

Do these once per computer, in order. Open a **new** terminal after each install so it picks up the new PATH.

| # | What | Why | How |
|---|------|-----|-----|
| 1 | **Git** | version control | <https://git-scm.com/download/win> |
| 2 | **MiKTeX** | builds the PDF report | <https://miktex.org/download> (the "basic" installer is enough) |
| 3 | **GNU Make** | the `make ...` commands | `winget install ezwinports.make` |
| 4 | **Miniconda** | Python 3.12, which the graders expect | `winget install Anaconda.Miniconda3`, then (new terminal) `~/miniconda3/Scripts/conda.exe init bash` in Git Bash, or `~\miniconda3\Scripts\conda.exe init powershell` in PowerShell |
| 5 | Project environment | all Python packages + Jupyter kernel | `make env`, then `conda activate cs221` in every new terminal |

After installing MiKTeX, allow it to download missing LaTeX packages automatically. Without this, the first
build stops and asks for them. You can also set this under MiKTeX Console > Settings > "Always install missing packages".

```powershell
initexmf --set-config-value [MPM]AutoInstall=1
```

Check that everything is in place:

```powershell
git --version; make --version; pdflatex --version; conda --version
```

If a command reports **`command not found`** right after installing it, the terminal still has the old PATH.
A terminal inside **VS Code** inherits VS Code's environment, so close **every** VS Code window and reopen it;
opening a new terminal tab is not enough. Git Bash shows `UCRT64` in its prompt, which is normal.

Notes:

* **Use the conda Python.** The `python` already on PATH on some machines (e.g. Espressif's 3.11) is the wrong
  version. Run `conda activate cs221` first; `python --version` must print 3.12.x.
* If `osmium` (Route Planning) fails to install, see [`assignments/03_route/README.md`](assignments/03_route/README.md).
* The Pac-Man and car-tracking GUIs need `tkinter`, which comes with the conda Python.
* MiKTeX may print `major issue: So far, you have not checked for MiKTeX updates`. This is harmless; open
  MiKTeX Console > Updates once to clear it.
* `make report-watch` (rebuild on save) uses `latexmk`, which needs Perl: `winget install StrawberryPerl.StrawberryPerl`.
  It is optional; `make report` does not need Perl.
* No `make`? Run the same commands by hand. The Makefile is a short list of shell commands, e.g. `make report` is
  `cd report`, then `pdflatex -jobname=report -aux-directory=build main.tex` twice.

## Building the report

```powershell
make report          # -> report/report.pdf  (aux files in report/build/, git-ignored)
make report-clean    # delete report/build/ if a build gets stuck on a stale .aux/.toc
```

`report/report.pdf` **is committed**, so the whole team (and GitHub) always sees the current state. Rebuild it and
commit it together with any `.tex` change. If the build fails, the error and its line number are at the end of
`report/build/report.log` (search for `.tex:`).

Where things go:

| You want to... | Edit |
|----------------|------|
| answer a written question | `report/sections/NN_name.tex`, inside its `\begin{solution} ... \end{solution}` |
| add a figure | save it to `report/figures/NN_name/`, then `\includegraphics[width=0.8\linewidth]{NN_name/file.png}` |
| change team details | `report/team.tex` **and** the first table in the notebook |
| add a macro/package | `report/preamble.tex` |

Find what is left with: `git grep -n "\\todo" report/sections`.

## Working with the project

1. **Pull first:** `git pull`, then `conda activate cs221`.
2. **Code** in `assignments/NN_name/submission.py`, only between `BEGIN_YOUR_CODE` / `END_YOUR_CODE`. Write clear
   docstrings and comments, because we are graded on readability.
3. **Test:** `make test A=NN_name T=<test-id>`. Test IDs are listed in [`docs/ASSIGNMENTS.md`](docs/ASSIGNMENTS.md).
   The graders print points but still exit 0 when tests fail, so read the output.
4. **Notebook:** `make notebook`. In your assignment's section, fill in the **Approach** cells, then run the cells to
   show the source, the grader output and the experiments. Save figures to `report/figures/NN_name/`.
5. **Theory:** write the answers in `report/sections/NN_name.tex`, then run `make report`.
6. **Commit** small, focused changes with a clear message: `git add -A && git commit -m "Sentiment: implement 3a-3b"`, then `git push`.
7. To avoid merge conflicts, each member edits **only their own assignment's files**. The notebook is a single JSON
   file, so agree who commits it when two people edit it on the same day, or send your cells to that person.
