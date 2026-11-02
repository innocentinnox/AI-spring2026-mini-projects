#!/usr/bin/python

import random
from typing import Callable, Dict, List, Tuple, TypeVar

from util import *

FeatureVector = Dict[str, int]
WeightVector = Dict[str, float]
Example = Tuple[FeatureVector, int]

############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction


def extract_word_features(x: str) -> FeatureVector:
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x:
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE
    # phi(x) maps each word to its number of occurrences. str.split() with no
    # argument splits on any run of whitespace; words differing only in case
    # ("great" vs "Great") are deliberately kept as different features.
    features: FeatureVector = {}
    for word in x.split():
        features[word] = features.get(word, 0) + 1
    return features
    # END_YOUR_CODE


############################################################
# Problem 3b: stochastic gradient descent

T = TypeVar('T')


def learn_predictor(train_examples: List[Tuple[T, int]],
                   validation_examples: List[Tuple[T, int]],
                   feature_extractor: Callable[[T], FeatureVector],
                   num_epochs: int, eta: float) -> WeightVector:
    '''
    Given |train_examples| and |validation_examples| (each one is a list of (x,y)
    pairs), a |feature_extractor| to apply to x, and the number of epochs to
    train |num_epochs|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Notes:
    - Only use the train_examples for training!
    - You should call evaluate_predictor() on both train_examples and
      validation_examples to see how you're doing as you learn after each epoch.
    - The predictor should output +1 if the score is precisely 0.
    '''
    weights: WeightVector = {}

    # BEGIN_YOUR_CODE
    # Feature extraction is the expensive part, so do it once per example instead
    # of once per epoch. We train on train_features only; validation_features is
    # used purely to report progress.
    train_features = [(feature_extractor(x), y) for x, y in train_examples]
    validation_features = [(feature_extractor(x), y) for x, y in validation_examples]

    def predict(phi: FeatureVector) -> int:
        """sign(w . phi(x)), with the required convention that a score of 0 is +1."""
        return 1 if dot_product(weights, phi) >= 0 else -1

    for epoch in range(num_epochs):
        for phi, y in train_features:
            # Hinge loss: max(0, 1 - (w . phi) y). Its gradient w.r.t. w is
            # -y * phi when the margin (w . phi) y is below 1, and 0 otherwise,
            # so the SGD step w <- w - eta * grad only fires on margin violations.
            margin = dot_product(weights, phi) * y
            if margin < 1:
                increment(weights, eta * y, phi)

        train_error = evaluate_predictor(train_features, predict)
        validation_error = evaluate_predictor(validation_features, predict)
        print(f"epoch {epoch + 1:2d}: train error = {train_error:.4f}, "
              f"validation error = {validation_error:.4f}")
    # END_YOUR_CODE
    return weights


############################################################
# Problem 3c: generate test case


def generate_dataset(num_examples: int, weights: WeightVector) -> List[Example]:
    '''
    Return a set of examples (phi(x), y) randomly which are classified
      correctly by |weights|.
    '''
    random.seed(42)

    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a score for the given weight vector.
    # note that there is intentionally flexibility in how you define phi.
    # y should be 1 or -1 as classified by the weight vector.
    # IMPORTANT: In the case that the score is 0, y should be set to 1.

    # Note that the weight vector can be arbitrary during testing.
    def generate_example() -> Tuple[Dict[str, int], int]:
        # BEGIN_YOUR_CODE
        # Pick a random non-empty subset of the weight vector's features and give
        # each a random small integer count; this plays the role of phi(x).
        feature_names = list(weights.keys())
        num_features = random.randint(1, len(feature_names)) if feature_names else 0
        phi = {name: random.randint(1, 5)
               for name in random.sample(feature_names, num_features)}
        # Label the example with the classifier defined by `weights`, so that by
        # construction it is classified correctly (score 0 counts as +1).
        y = 1 if dot_product(weights, phi) >= 0 else -1
        # END_YOUR_CODE
        return phi, y

    return [generate_example() for _ in range(num_examples)]


############################################################
# Problem 3d: character features


def extract_character_features(n: int) -> Callable[[str], FeatureVector]:
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces mapped to their n-gram counts.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that 1 <= n <= len(x).
    '''
    def extract(x: str) -> Dict[str, int]:
        # BEGIN_YOUR_CODE
        # Drop spaces and tabs so n-grams may stretch across word boundaries,
        # then count every window of n consecutive characters.
        text = x.replace(' ', '').replace('\t', '')
        features: Dict[str, int] = {}
        for i in range(len(text) - n + 1):
            ngram = text[i:i + n]
            features[ngram] = features.get(ngram, 0) + 1
        return features
        # END_YOUR_CODE

    return extract


############################################################
# Problem 3e:


def test_values_of_n(n: int):
    '''
    Use this code to test different values of n for extract_character_features
    This code is exclusively for testing.
    Your full written solution for this problem must be in sentiment.pdf.
    '''
    train_examples = read_examples('polarity.train')
    validation_examples = read_examples('polarity.dev')
    feature_extractor = extract_character_features(n)
    weights = learn_predictor(train_examples,
                             validation_examples,
                             feature_extractor,
                             num_epochs=20,
                             eta=0.01)
    output_weights(weights, 'weights')
    output_error_analysis(validation_examples, feature_extractor, weights,
                        'error-analysis')  # Use this to debug
    trainError = evaluate_predictor(
        train_examples, lambda x:
        (1 if dot_product(feature_extractor(x), weights) >= 0 else -1))
    validationError = evaluate_predictor(
        validation_examples, lambda x:
        (1 if dot_product(feature_extractor(x), weights) >= 0 else -1))
    print(("Official: train error = %s, validation error = %s" %
           (trainError, validationError)))


############################################################
# Problem 5: k-means
############################################################


def kmeans(examples: List[Dict[str, float]], K: int,
           max_epochs: int) -> Tuple[List, List, float]:
    '''
    Perform K-means clustering on |examples|, where each example is a sparse feature vector.

    examples: list of examples, each example is a string-to-float dict representing a sparse vector.
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    max_epochs: maximum number of epochs to run (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments (i.e. if examples[i] belongs to centers[j], then assignments[i] = j),
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE
    # Squared distance ||x - c||^2 = ||x||^2 - 2 x.c + ||c||^2. The ||x||^2 terms
    # never change and the ||c||^2 terms change only once per epoch, so we cache
    # both and the inner loop costs a single sparse dot product per (x, c) pair.
    example_sq_norms = [dot_product(x, x) for x in examples]

    def squared_distance(i: int, j: int, center_sq_norms: List[float]) -> float:
        return (example_sq_norms[i]
                - 2 * dot_product(examples[i], centers[j])
                + center_sq_norms[j])

    def assign_all(centers_sq: List[float]) -> Tuple[List[int], float]:
        """Assign each example to its nearest centre; also return the total loss."""
        assignments, loss = [], 0.0
        for i in range(len(examples)):
            distances = [squared_distance(i, j, centers_sq) for j in range(K)]
            best = min(range(K), key=distances.__getitem__)
            assignments.append(best)
            loss += distances[best]
        return assignments, loss

    # Initialise the K centres to K distinct random examples.
    centers = [dict(x) for x in random.sample(examples, K)]
    assignments: List[int] = []

    for _ in range(max_epochs):
        # Step 1 (E-step): reassign points to the nearest centre.
        new_assignments, _ = assign_all([dot_product(c, c) for c in centers])
        if new_assignments == assignments:
            break  # nothing moved -> the algorithm has converged
        assignments = new_assignments

        # Step 2 (M-step): move every centre to the mean of its assigned points.
        sums = [{} for _ in range(K)]
        counts = [0] * K
        for i, j in enumerate(assignments):
            increment(sums[j], 1.0, examples[i])
            counts[j] += 1
        for j in range(K):
            if counts[j] > 0:  # an empty cluster keeps its previous centre
                centers[j] = {f: v / counts[j] for f, v in sums[j].items()}

    # Final loss, measured against the final centres.
    assignments, total_loss = assign_all([dot_product(c, c) for c in centers])
    return centers, assignments, total_loss
    # END_YOUR_CODE
