"""Generates notebook/CS221_Mini_Projects.ipynb from the SPEC below.

    python scripts/gen_notebook.py notebook/CS221_Mini_Projects.ipynb

WARNING: this OVERWRITES the notebook (including any cell outputs). Edit the
APPROACH texts / SPEC here and regenerate, or edit the notebook directly in
Jupyter once the team stops regenerating it.
"""
import json, sys
from pathlib import Path

OUT = Path(sys.argv[1])
cells = []

# Approach text per (assignment, problem id). Problems not listed get a TODO.
APPROACH = {
    (1, "4a"): "`str.split()` yields the maximal whitespace-free chunks; Python's `min` over strings is the "
               "case-sensitive lexicographic order the problem asks for. $O(\\text{len})$.",
    (1, "4b"): "`math.hypot(dx, dy)` is $\\sqrt{dx^2+dy^2}$ with better numerical care than squaring by hand.",
    (1, "4c"): "Build a graph `successors[w]` = words that directly follow `w` in the original sentence. A similar "
               "sentence is exactly a walk of the same length in this graph, so we run a depth-first search from every "
               "distinct word and collect completed walks in a `set` (which also removes duplicates).",
    (1, "4d"): "Only keys present in *both* vectors contribute, so iterate over the smaller dict and `.get()` the key "
               "in the larger one (indexing a `defaultdict` would insert zeros as a side effect). $O(\\min(|v_1|,|v_2|))$.",
    (1, "4e"): "Walk the keys of `v2` and add `scale * value` into `v1` in place; keys only in `v1` are untouched because "
               "`scale * 0` adds nothing. `v2` is never modified.",
    (1, "4f"): "One `collections.Counter` pass over the words, then keep those with count $> 1$. $O(\\text{len})$.",
    (2, "3a"): "A plain dictionary of word counts; words are split on whitespace and are case sensitive, as the handout "
               "specifies. This is $\\phi(x)$ for the rest of the problem.",
    (2, "3b"): "Stochastic gradient descent on the hinge loss $\\max(0, 1 - (\\mathbf{w}\\cdot\\phi(x))\\,y)$. Its gradient is "
               "$-y\\,\\phi(x)$ when the margin is below 1 and $0$ otherwise, so each step is `increment(w, eta*y, phi)` "
               "only on margin violations. Features are extracted **once** (not once per epoch), and after every epoch "
               "we print train/validation error. Reaches 2.8% train / 27.4% validation error (targets < 4% / < 30%).",
    (2, "3c"): "Pick a random non-empty subset of the weight vector's features with random small counts as $\\phi(x)$, "
               "then label it with the given classifier ($y = +1$ when the score is $\\ge 0$), so every example is "
               "correct by construction. Used to sanity-check `learn_predictor` with the identity feature extractor.",
    (2, "3d"): "Remove spaces and tabs, then slide a window of $n$ characters and count each window. The closure "
               "captures `n` so the returned function has the same signature as `extract_word_features`.",
    (2, "5b"): "Lloyd's algorithm. Expanding $\\|x-\\mu\\|^2 = \\|x\\|^2 - 2\\,x\\cdot\\mu + \\|\\mu\\|^2$ lets us cache "
               "$\\|x_i\\|^2$ once and $\\|\\mu_j\\|^2$ once per epoch, so the inner loop is a single sparse dot product "
               "per (point, centre) pair. Centres start at $K$ random examples; we stop as soon as assignments stop "
               "changing and report the loss against the final centres.",
    (3, "2a"): "State = current location only. `is_end` checks whether the location carries `end_tag`; successors are "
               "the neighbours in `city_map.distances` with their distances as costs and the neighbour's label as the "
               "action. The search algorithm (UCS) is the one provided in `util.py`.",
    (3, "2b"): "Our query: start at the Gates building and reach the nearest location tagged `amenity=food`.",
    (3, "3a"): "State = (location, sorted tuple of waypoint tags covered so far). Which locations were visited and in what "
               "order is irrelevant to the future, so this is the smallest sufficient memory: $n\\cdot 2^k$ states. "
               "Moving to a neighbour adds whatever waypoint tags it carries; the goal is reached when we stand on an "
               "`end_tag` location *and* the covered tuple equals the full waypoint tuple.",
    (3, "3c"): "Our query: from the Rains dorm, cover `amenity=food`, `landmark=bookstore` and `landmark=green_library` "
               "in any order, and finish at the Gates building.",
    (3, "4a"): "A* is UCS with reduced costs $\\text{cost}'(s,a) = \\text{cost}(s,a) + h(\\text{Succ}(s,a)) - h(s)$. The $h$ "
               "terms telescope along any path to the constant $h(\\text{end}) - h(\\text{start})$, so the optimal path is "
               "unchanged while UCS is steered toward states with small $h$. Start state and goal test are delegated "
               "to the wrapped problem.",
    (3, "4b"): "Precompute the coordinates of every `end_tag` location; the heuristic is the minimum great-circle "
               "distance (`compute_distance`) from the current location to any of them. Straight-line distance never "
               "exceeds walking distance and obeys the triangle inequality, so it is admissible and consistent.",
    (3, "4c"): "Run UCS *backwards* once: from a virtual `END` state connected at cost 0 to every `end_tag` location, "
               "with `is_end` always `False` so the whole graph is exhausted. `ucs.past_costs[loc]` is then the exact "
               "shortest distance from `loc` to the nearest end location (distances are symmetric). Ignoring waypoints "
               "makes it a lower bound, hence admissible; a lookup is $O(1)$.",
}

def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)})

def code(text):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                  "source": text.strip("\n").splitlines(keepends=True)})

TODO_APPROACH = "**Approach.** _TODO: explain the idea, data structures and complexity before showing the code._"

# --------------------------------------------------------------------------- front matter
md(r"""
# CS221 Mini Projects — Programming Part

**Course:** Artificial Intelligence: Principles and Techniques (based on Stanford CS221, Spring 2026 coursework)
**Deliverables:** each team uploads to Moodle **one notebook** (this file, executed with all outputs, for the programming part)
and **one PDF** (`report/report.pdf`, for the theoretical part). Both use the same numbering.
**Deadline:** 5 December 2026 · **Presentations:** 14–19 December 2026 (Zoom)
""")

md(r"""
## Team Members

| # | Full name | Student Number | Registration Number |
|---|-----------|----------------|---------------------|
| 1 | MUJUNI INNOCENT | 2400707155 | 24/U/07155/PS |
| 2 | _TODO_ | _TODO_ | _TODO_ |
| 3 | _TODO_ | _TODO_ | _TODO_ |
| 4 | _TODO_ | _TODO_ | _TODO_ |
| 5 | _TODO_ | _TODO_ | _TODO_ |
| 6 | _TODO_ | _TODO_ | _TODO_ |
| 7 | _TODO_ | _TODO_ | _TODO_ |
| 8 | _TODO_ | _TODO_ | _TODO_ |
| 9 | _TODO_ | _TODO_ | _TODO_ |
| 10 | _TODO_ | _TODO_ | _TODO_ |

**Team:** Group 13

> Keep this table identical to `report/team.tex`.
""")

md(r"""
## Contents

| No. | Assignment | Programming problems in this notebook | Code folder |
|-----|------------|----------------------------------------|-------------|
| 1 | Foundations | 4a–4f (Python warm-up functions) | `assignments/01_foundations` |
| 2 | Sentiment Classification | 3a–3e (linear classifier, SGD, n-grams), 5b (k-means) | `assignments/02_sentiment` |
| 3 | Route Planning | 2a–2b, 3a & 3c (search problems), 4a–4c (A\*) | `assignments/03_route` |
| 4 | Controlling MountainCar | 3a–3c (value iteration), 4a–4d (Q-learning), 5c (constrained RL) | `assignments/04_mountaincar` |
| 5 | Pac-Man | 1b (minimax), 2a (alpha-beta), 3b (expectimax), 4a (evaluation, extra credit) | `assignments/05_pacman` |
| 6 | Bayesian Networks (Car Tracking) | 1c (observe), 2c (elapseTime), 4b (sensor deception) | `assignments/06_bayesian` |
| 7 | From Language to Logic | 1a–1c, 2a–2d, 3a, 4a, 5a–5c (extra credit) | `assignments/07_logic` |

Written / theoretical answers for every assignment are in the PDF report, which uses the same numbering.

### How this notebook is organised

* Each assignment's implementation lives in `assignments/<NN_name>/submission.py`. That is the
  starter file the official grader imports, and the only file the course staff ask us to modify.
* For each programming problem the notebook (1) states the task, (2) explains our approach,
  (3) displays the documented source with `show_source`, (4) runs the official tests, and
  (5) where the problem asks for it, runs experiments and saves figures into `report/figures/`.
* `cs221_helpers.py` isolates the seven starter codebases from each other: several of them
  use the same module names (`util`, `submission`, `grader`).
""")

code(r"""
# Notebook setup: shared helpers + environment check (the graders expect Python 3.12).
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))          # the notebook folder holds cs221_helpers.py
from cs221_helpers import (ASSIGNMENTS, use_assignment, load, run_grader, run_script,
                           show_source, environment_report, REPO_ROOT)

environment_report()
""")

# --------------------------------------------------------------------------- assignments
SPEC = [
    dict(n=1, title="Foundations", intro=r"""
Warm-up in optimisation, probability, complexity and ethics. Problems 1–3 are written (PDF §1).
**Problem 4** asks for six short Python functions, using **standard library only, no numpy**.
These helpers (sparse vectors in particular) come back in later assignments.
""", problems=[
        ("4a", "find_alphabetically_first_word", "Return the lexicographically smallest word of a string (words = whitespace-separated).",
         ["find_alphabetically_first_word"], ["4a-0-basic", "4a-1-basic", "4a-2-basic"]),
        ("4b", "euclidean_distance", "Euclidean distance between two 2-D points.",
         ["euclidean_distance"], ["4b-0-basic"]),
        ("4c", "mutate_sentences", "All sentences of the same length whose adjacent word pairs all appear adjacent in the original sentence.",
         ["mutate_sentences"], ["4c-0-basic"]),
        ("4d", "sparse_vector_dot_product", "Dot product of two sparse vectors represented as `collections.defaultdict(float)`.",
         ["sparse_vector_dot_product"], ["4d-0-basic"]),
        ("4e", "increment_sparse_vector", "In-place `v1 += scale * v2` for sparse vectors.",
         ["increment_sparse_vector"], ["4e-0-basic"]),
        ("4f", "find_nonsingleton_words", "Set of words that occur more than once in a text.",
         ["find_nonsingleton_words"], ["4f-0-basic"]),
    ], experiments=[]),

    dict(n=2, title="Sentiment Classification", intro=r"""
Linear classification of Rotten-Tomatoes reviews with hinge loss + SGD, character n-gram features,
and k-means. Problems 1, 2, 4 and the written parts of 3e/5a/5c are in PDF §2.
**No numpy/sklearn**: use `util.dot_product` / `util.increment` on dict feature vectors.
Targets: **< 4 % train error** and **< 30 % validation error**.
""", problems=[
        ("3a", "extract_word_features", "Map a review to a word-count feature vector φ(x) (dict).",
         ["extract_word_features"], ["3a-0-basic"]),
        ("3b", "learn_predictor (SGD on hinge loss)", "Learn weights with SGD on hinge loss; print train/validation error each epoch.",
         ["learn_predictor"], ["3b-0-basic", "3b-1-basic", "3b-2-basic"]),
        ("3c", "generate_dataset", "Generate synthetic examples whose label is the sign of w·φ(x), to sanity-check the learner.",
         ["generate_dataset"], ["3c-0-basic", "3c-1-basic"]),
        ("3d", "extract_character_features", "Character n-gram counts, ignoring spaces and tabs.",
         ["extract_character_features"], ["3d-0-basic"]),
        ("5b", "kmeans", "k-means with random initial centres from the data; precompute squared norms so the distance updates stay fast.",
         ["kmeans"], ["5b-0-basic"]),
    ], experiments=[
        ("3e", "Choosing n for character n-grams", r"""
Train with the same settings as 3b (20 epochs, η = 0.01) for n = 1..10 and compare validation errors.
The table is reproduced in PDF §2 (3e). Takes a few minutes: large n produces hundreds of thousands of features.
""", r"""
import contextlib, io
sub = load("submission")
import util
train = util.read_examples("polarity.train")
dev = util.read_examples("polarity.dev")

print(f"{'n':>2}  {'train error':>11}  {'validation error':>16}  {'#features':>9}")
for n in range(1, 11):
    fe = sub.extract_character_features(n)
    with contextlib.redirect_stdout(io.StringIO()):          # hide the per-epoch prints
        w = sub.learn_predictor(train, dev, fe, num_epochs=20, eta=0.01)
    predict = lambda x: 1 if util.dot_product(fe(x), w) >= 0 else -1
    print(f"{n:>2}  {util.evaluate_predictor(train, predict):>11.4f}  "
          f"{util.evaluate_predictor(dev, predict):>16.4f}  {len(w):>9}")
"""),
    ]),

    dict(n=3, title="Route Planning", intro=r"""
Model route planning on the Stanford OpenStreetMap graph as search problems solved by UCS / A\*.
Problems 1, 2b-c, 3b-d are written (PDF §3). Requires `osmium`, `plotly`, `pandas` (see README).
Focus on **modelling** (state design); UCS is provided in `util.py`.
""", problems=[
        ("2a", "ShortestPathProblem", "Shortest path from `start_location` to *any* location carrying `end_tag`.",
         ["ShortestPathProblem"], ["2a-1-basic", "2a-2-basic", "2a-4-basic", "2a-5-basic", "2a-6-basic"]),
        ("2b", "get_stanford_shortest_path_problem (custom)", "Our chosen start/end tag; writes `path.json` for `visualization.py`.",
         ["get_stanford_shortest_path_problem"], ["2b-custom"]),
        ("3a", "WaypointsShortestPathProblem", "Shortest path covering an unordered set of waypoint tags. The state must stay compact: (location, set of waypoints covered).",
         ["WaypointsShortestPathProblem"], ["3a-1-basic", "3a-2-basic", "3a-3-basic", "3a-4-basic", "3a-6-basic", "3a-7-basic", "3a-8-basic"]),
        ("3c", "get_stanford_waypoints_shortest_path_problem (custom)", "Our chosen waypoint route; writes `path.json`.",
         ["get_stanford_waypoints_shortest_path_problem"], ["3c-custom"]),
        ("4a", "a_star_reduction", "A\\* as UCS on a new problem with reduced costs cost'(s,a) = cost(s,a) + h(succ) − h(s).",
         ["a_star_reduction"], ["4a-1-basic", "4a-2-basic", "4a-3-basic"]),
        ("4b", "StraightLineHeuristic", "Consistent heuristic: straight-line (geodesic) distance to the nearest end-tag location.",
         ["StraightLineHeuristic"], ["4b-heuristic-1-basic", "4b-astar-1-basic", "4b-astar-2-basic"]),
        ("4c", "NoWaypointsHeuristic", "Heuristic = exact shortest-path distance ignoring waypoints (precomputed with UCS from the end tags).",
         ["NoWaypointsHeuristic"], ["4c-heuristic-1-basic", "4c-astar-1-basic", "4c-astar-2-basic"]),
    ], experiments=[
        ("viz", "Route figures for the report (2b, 3c)", r"""
`visualization.py` draws the map with Plotly and opens it in the browser. `scripts/route_figures.py` reuses its
`plot_map` to solve our custom problems and export static PNGs to `report/figures/03_route/` (needs `kaleido`).
""", r"""
run_script(3, str(REPO_ROOT / "scripts" / "route_figures.py"))
"""),
    ]),

    dict(n=4, title="Controlling MountainCar", intro=r"""
MDPs and reinforcement learning on Gymnasium's MountainCar: value iteration, model-based Monte Carlo,
tabular and Fourier-feature Q-learning, and constrained (safe) exploration.
Problems 1, 2, 3c, 4d, 4e, 5a, 5b, 5d are written (PDF §4). Requires `gymnasium`, `pygame`, `numpy`, `matplotlib`.
""", problems=[
        ("3a", "value_iteration", "Value iteration on a dict-based transition model `(s, a) -> [(s', prob, reward)]` until the change is below ε; return the greedy policy.",
         ["value_iteration"], ["3a-0-basic", "3a-1-basic"]),
        ("3b", "ModelBasedMonteCarlo", "Estimate T̂ and R̂ from experience; re-run value iteration every `calc_val_iter_every` steps; ε-greedy `get_action`.",
         ["ModelBasedMonteCarlo"], ["3b-0-basic", "3b-1-basic", "3b-2-basic", "3b-3-basic"]),
        ("4a", "TabularQLearning", "ε-greedy action selection and the tabular Q-learning update.",
         ["TabularQLearning"], ["4a-0-basic", "4a-1-basic"]),
        ("4b", "fourier_feature_extractor", "Fourier basis φ(s) = cos(π c·(scale ⊙ s)) for all c ∈ {0..m}^k (outer-sum construction).",
         ["fourier_feature_extractor"], ["4b-0-basic"]),
        ("4c", "FunctionApproxQLearning", "Q(s,a) = w_a · φ(s); gradient-style weight update.",
         ["FunctionApproxQLearning"], ["4c-0-basic", "4c-1-basic", "4c-2-basic"]),
        ("5c", "ConstrainedQLearning", "Only allow actions with velocity_{t+1} < threshold; return None when no action is valid.",
         ["ConstrainedQLearning"], ["5c-helper"]),
    ], experiments=[
        ("train", "Training curves for 3c and 4d", r"""
Each command trains three trials and saves reward plots (`mcvi_*.png`, `tabular_*.png`, `fapprox_*.png`).
Copy the plots you discuss into `report/figures/04_mountaincar/`.
""", r"""
import shutil
for agent, prefix in [("value-iteration", "mcvi"), ("tabular", "tabular"), ("function-approximation", "fapprox")]:
    run_script(4, "train.py", "--agent", agent)
    for png in ASSIGNMENTS[4].path.glob(f"{prefix}_*.png"):
        shutil.copy(png, ASSIGNMENTS[4].figures / png.name)
"""),
        ("5b", "Removing the speed limit (5b)", "Run function approximation with `max_speed=100000` for the written answer to 5b.", r"""
run_script(4, "train.py", "--agent", "function-approximation", "--max_speed=100000")
"""),
    ]),

    dict(n=5, title="Pac-Man", intro=r"""
Adversarial search for multi-agent Pac-Man: minimax with multiple min layers, alpha-beta pruning,
expectimax against random ghosts, and a custom evaluation function (extra credit).
Problems 1a, 3a, 4b, 5 are written (PDF §5). Standard library + tkinter only.
**Sanity values:** minimax root value on `minimaxClassic` = 9, 8, 7, −492 for depths 1–4;
on `mediumClassic` = 9, 18, 27, 36.
""", problems=[
        ("1b", "MinimaxAgent", "Depth-limited minimax. One depth = Pac-Man plus every ghost moving once.",
         ["MinimaxAgent"], ["1b-0-basic", "1b-1-basic", "1b-2-basic", "1b-3-basic"]),
        ("2a", "AlphaBetaAgent", "Minimax with α-β pruning generalised to several min agents; must return the same values as minimax.",
         ["AlphaBetaAgent"], ["2a-0-basic", "2a-1-basic", "2a-2-basic", "2a-3-basic"]),
        ("3b", "ExpectimaxAgent", "Ghost layers average uniformly over their legal actions.",
         ["ExpectimaxAgent"], ["3b-0-basic", "3b-1-basic", "3b-2-basic", "3b-3-basic"]),
        ("4a", "better_evaluation_function (extra credit)", "State evaluation function; target is winning > 50 % on `smallClassic` at depth 2 with a high average score.",
         ["better_evaluation_function"], ["4a-1-basic"]),
    ], experiments=[
        ("5", "Minimax vs expectimax on trappedClassic (Problem 5)", r"""
Run each agent many times without graphics (`-q`) and record win rates and scores for PDF §5.
""", r"""
run_script(5, "pacman.py", "-p", "MinimaxAgent", "-l", "trappedClassic", "-a", "depth=3", "-q", "-n", "10")
run_script(5, "pacman.py", "-p", "ExpectimaxAgent", "-l", "trappedClassic", "-a", "depth=3", "-q", "-n", "10")
"""),
    ]),

    dict(n=6, title="Bayesian Networks (Car Tracking)", intro=r"""
HMM-style exact inference to track other cars from noisy microphone distances: an emission update
(`observe`), a transition update (`elapseTime`), and a sensor-deception variant.
Problems 1a-b, 2a-b, 3, 4a, 4c-f are written (PDF §6). Always call `util.pdf(mean, std, value)`
positionally, as the handout requires.
""", problems=[
        ("1c", "ExactInference.observe", "Multiply each tile's belief by p(d_t | c) = N(d_t; ‖a_t − c‖, σ²) and normalise.",
         ["submission.ExactInference.observe"], ["1c-0-basic", "1c-1-basic"]),
        ("2c", "ExactInference.elapseTime", "Forward step: belief'(c') ∝ Σ_c belief(c) · transProb[(c, c')], then normalise.",
         ["submission.ExactInference.elapseTime"], ["2c-0-basic"]),
        ("4b", "ExactInferenceWithSensorDeception.observe", "Apply the skew transform D' = D/(1+s²) + √(2/(1+s²)) before the usual emission update.",
         ["submission.ExactInferenceWithSensorDeception.observe"], ["4b-0-basic"]),
    ], experiments=[
        ("drive", "Visual checks (optional, opens a Tk window)", r"""
`drive.py` is not graded, but it is useful for the observations in 4b/4e (particle filter vs exact inference).
""", r"""
# run_script(6, "drive.py", "-a", "-p", "-d", "-k", "1", "-i", "exactInference")
# run_script(6, "drive.py", "-a", "-d", "-k", "3", "-i", "particleFilter")
"""),
    ]),

    dict(n=7, title="From Language to Logic", intro=r"""
Translate English into propositional / first-order logic formulas (`logic.py`), solve a liar puzzle,
encode a theorem about odd/even integers, and (extra credit) write semantic-parsing grammar rules.
Problems 6 and 7 are written (PDF §7). **All tests are visible**: passing every local test means full credit.
""", problems=[
        ("1", "Propositional logic (1a–1c)", "Summer ∧ California → ¬Rain; Wet ↔ (Rain ∨ Sprinklers); Day ⊕ Night.",
         ["formula1a", "formula1b", "formula1c"], ["1a", "1b", "1c"]),
        ("2", "First-order logic (2a–2d)", "Parents, childless persons, Father and Granddaughter definitions.",
         ["formula2a", "formula2b", "formula2c", "formula2d"], ["2a", "2b", "2c", "2d"]),
        ("3a", "Liar puzzle", "Six formulas: four testimonies, exactly one truth-teller, exactly one culprit.",
         ["liar"], ["3a-0", "3a-1", "3a-2", "3a-3", "3a-4", "3a-5", "3a-all", "3a-run"]),
        ("4a", "Odd and even integers", "Six axioms; the query (an even number larger than every x) is checked by model checking.",
         ["ints"], ["4a-0", "4a-1", "4a-2", "4a-3", "4a-4", "4a-5", "4a-all", "4a-run"]),
        ("5", "Semantic parsing (extra credit)", "Three `GrammarRule`s for the given sentence templates.",
         ["createRule1", "createRule2", "createRule3"], ["5a-1", "5b-1", "5c-1"]),
    ], experiments=[]),
]

for a in SPEC:
    n = a["n"]
    md(f"---\n# Assignment {n}: {a['title']}\n" + a["intro"])
    code(f"""
# Activate Assignment {n}: imports and relative file paths now resolve inside its folder.
hw = use_assignment({n})
sub = load("submission")
""")
    for pid, name, task, symbols, tests in a["problems"]:
        approach = APPROACH.get((n, pid))
        approach = f"**Approach.** {approach}" if approach else TODO_APPROACH
        md(f"## {n}.{pid} — {name}\n\n**Task.** {task}\n\n{approach}")
        objs = ", ".join(s if s.startswith("submission.") else f"sub.{s}" for s in symbols).replace("submission.", "sub.")
        code(f"show_source({objs})")
        code("run_grader({n}, {ids})".format(n=n, ids=", ".join(repr(t) for t in tests)))
    for eid, name, desc, body in a["experiments"]:
        md(f"## {n}.{eid} — {name}\n" + desc)
        code(body)
    md(f"### Assignment {n}: full local grader run\nAll locally available tests. Hidden tests run only on the course autograder.")
    code(f"run_grader({n})")

md(r"""
---
# Conclusion

_TODO: a short summary of results per assignment (tests passed, key experimental numbers), lessons learned,
and how work was split across the team._
""")

nb = {"cells": cells,
      "metadata": {"kernelspec": {"display_name": "Python 3.12 (cs221)", "language": "python", "name": "cs221"},
                   "language_info": {"name": "python", "version": "3.12"}},
      "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i:03d}"
OUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{len(cells)} cells -> {OUT}")
