# Assignment breakdown

Source of truth: each folder's `index.html` (the official handout). **W** = written (PDF), **C** = code (notebook).
The test IDs are the ones accepted by `python grader.py <id>`.

---

## 1. Foundations (`assignments/01_foundations`)
*Warm-up in maths, complexity and ethics. Standard library only; numpy is not allowed in the code.*

| Part | Type | Topic |
|------|------|-------|
| 1a | W | minimise Σ wᵢ(θ − xᵢ)², i.e. the weighted mean; problems when some wᵢ < 0 |
| 1b | W | f(x) = min_s Σ s·xᵢ vs g(x) = Σ min_{sᵢ} sᵢxᵢ: prove f ≥ g |
| 1c | W | expected points of the dice game, via a recurrence on V |
| 1d | W | MLE of p for T,H,H,H,H, using log-likelihood |
| 1e | W | P(A\|B) = P(B\|A), P(A∪B) = 1/3: prove P(A) > 1/6 |
| 1f | W | gradient of the double-sum quadratic + (λ/2)‖w‖² |
| 2a | W | ways to place 3 rectangles on an n×n grid (big-O) |
| 2b | W | min-cost down/right path on an n×2n grid, via DP |
| 3a–d | W | NeurIPS ethics: loan model, stylometry, celebrity faces, iNaturalist |
| 4a–f | C | `find_alphabetically_first_word`, `euclidean_distance`, `mutate_sentences`, `sparse_vector_dot_product`, `increment_sparse_vector`, `find_nonsingleton_words` |

## 2. Sentiment Classification (`assignments/02_sentiment`)
*Uses `util.dot_product` / `util.increment`; no numpy or sklearn. Targets: train error < 4 %, validation error < 30 %.*

| Part | Type | Topic |
|------|------|-------|
| 1a | W | 4 hand SGD steps on hinge loss (η = 0.1) |
| 1b | W | prove the bad/good/not bad/not good set is not linearly separable; add a feature |
| 2a–c | W | squared loss with a sigmoid: loss, gradient in terms of p, vanishing gradient |
| 3a–d | C | `extract_word_features`, `learn_predictor`, `generate_dataset`, `extract_character_features` |
| 3e | W | best n for character n-grams + a review where n-grams beat words |
| 4a–d | W | toxicity: classifiers D and T, average vs max group loss, fairness frameworks, λ |
| 5a | W | 2-means by hand, from two initialisations |
| 5b | C | `kmeans` (precompute ‖x‖², must be fast) |
| 5c | W | is k-means invariant to scaling all dims / some dims? |

## 3. Route Planning (`assignments/03_route`)
*Needs `osmium`, `plotly`, `pandas`. The focus is modelling search problems; UCS is provided.
The handout says `mapUtil.py`, but the file is `map_util.py`.*

| Part | Type | Topic |
|------|------|-------|
| 1a–c | W | grid city cost 1 + max(x, 0); UCS T/F questions |
| 2a | C | `ShortestPathProblem` |
| 2b | C+W | custom Stanford problem → `path.json` → `visualization.py` screenshots |
| 2c | W | externalities of routing apps |
| 3a | C | `WaypointsShortestPathProblem` (compact state: location + covered tags) |
| 3b | W | number of states in terms of n and k |
| 3c | C+W | custom waypoint route + screenshot |
| 3d | W | ride-share drivers, dual use |
| 4a–c | C | `a_star_reduction`, `StraightLineHeuristic`, `NoWaypointsHeuristic` |

## 4. Controlling MountainCar (`assignments/04_mountaincar`)
*Needs `gymnasium==0.28.1`, `pygame`, `numpy 1.26`, `matplotlib`. `train.py` writes plots that the report needs.*

| Part | Type | Topic |
|------|------|-------|
| 1a–b | W | 2 iterations of value iteration on a 5-state chain; policy |
| 2a | W | reduce a γ < 1 MDP to a γ = 1 MDP with an extra absorbing state o |
| 3a–b | C | `value_iteration`, `ModelBasedMonteCarlo` |
| 3c | W | MCVI training plots + when model-based VI fails |
| 4a–c | C | `TabularQLearning`, `fourier_feature_extractor`, `FunctionApproxQLearning` |
| 4d–e | W | tabular vs function approximation plots; when function approximation wins |
| 5a–b | W | Gym's `max_speed`; why removing it barely changes the policy |
| 5c | C+W | `ConstrainedQLearning` (velocity bound) + `grader.py 5c-helper` |
| 5d | W | design harmful MDP A vs safer MDP B for autonomous driving |

## 5. Pac-Man (`assignments/05_pacman`)
*Standard library + tkinter. Run headless with `-q`. Check values: minimaxClassic root = 9, 8, 7, −492 (depths 1–4).
`multi_agents_solution.py` is an unrelated legacy file; ignore it.*

| Part | Type | Topic |
|------|------|-------|
| 1a | W | multi-ghost minimax recurrence V(s, d) |
| 1b | C | `MinimaxAgent` |
| 2a | C | `AlphaBetaAgent` (same values as minimax) |
| 3a | W | expectimax recurrence |
| 3b | C | `ExpectimaxAgent` (trappedClassic: −502 on a loss, 531/532 on a win) |
| 4a–b | C+W | extra credit: `better_evaluation_function` + description |
| 5a–c | W | minimax vs expectimax on trappedClassic; fixing Eval; reward hacking example |

## 6. Bayesian Networks: Car Tracking (`assignments/06_bayesian`)
*About 10 lines of code in total; the difficulty is the probability. Call `util.pdf(mean, std, value)` positionally.*

| Part | Type | Topic |
|------|------|-------|
| 1a–b | W | Bayesian network for a stationary car; joint distribution |
| 1c | C | `ExactInference.observe` (emission update + normalise) |
| 2a–b | W | HMM Bayesian network; joint distribution |
| 2c | C | `ExactInference.elapseTime` (transition update) |
| 3a–b | W | unlabelled distances for K = 2 (sum over permutations); ≥ K! maximisers |
| 4a | W | camera misuse (dual use) |
| 4b | C | `ExactInferenceWithSensorDeception.observe` (skew transform) |
| 4c–f | W | sensor redundancy; particle filter vs exact inference; privacy vs accuracy; adversarial attack |

## 7. From Language to Logic (`assignments/07_logic`)
*All tests are visible, so passing them locally means full credit. Problems 6–7 are written and easy to forget.*

| Part | Type | Topic |
|------|------|-------|
| 1a–c | C | propositional formulas |
| 2a–d | C | FOL: parent, childless, Father, Granddaughter |
| 3a | C | liar puzzle: 6 formulas (`3a-0`…`3a-5`, `3a-all`, `3a-run`) |
| 4a | C | odd/even axioms (`4a-0`…`4a-5`, `4a-all`, `4a-run`) |
| 5a–c | C | extra credit: grammar rules for semantic parsing |
| 6a–c | W | explainability of logic systems |
| 7a–c | W | soundness/completeness: LLMs; safety-critical choice; with a verifier |
