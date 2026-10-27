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
    raise Exception("Not implemented yet")
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
    raise Exception("Not implemented yet")
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
        raise Exception("Not implemented yet")
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
        raise Exception("Not implemented yet")
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
    raise Exception("Not implemented yet")
    # END_YOUR_CODE
