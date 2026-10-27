#!/usr/bin/python3

import grader_util
import util
import string
from util import *

grader = grader_util.Grader()
submission = grader.load('submission')

############################################################
# check python version

import sys
import warnings

if not (sys.version_info[0]==3 and sys.version_info[1]==12):
    warnings.warn("Must be using Python 3.12 \n")

############################################################
# Problem 1: building intuition
############################################################

grader.add_manual_part('1a', max_points=2, description='simulate SGD')
grader.add_manual_part('1b', max_points=2, description='create small dataset')

############################################################
# Problem 2: predicting movie ratings
############################################################

grader.add_manual_part('2a', max_points=2, description='loss')
grader.add_manual_part('2b', max_points=3, description='gradient')
grader.add_manual_part('2c', max_points=3, description='smallest magnitude')

############################################################
# Problem 3: sentiment classification
############################################################

### 3a

# Basic sanity check for feature extraction
def test3a0():
    ans = {"a":2, "b":1}
    grader.require_is_equal(ans, submission.extract_word_features("a b a"))
grader.add_basic_part('3a-0-basic', test3a0, max_seconds=1, description="basic test")

def test3a1():
    random.seed(42)
    sentence = ' '.join([random.choice(['a', 'aa', 'ab', 'b', 'c']) for _ in range(100)])
    submission_ans = submission.extract_word_features(sentence)
grader.add_hidden_part('3a-1-hidden', test3a1, max_seconds=1, description="test multiple instances of the same word in a sentence")

### 3b

def test3b0():
    train_examples = (("hello world", 1), ("goodnight moon", -1))
    test_examples = (("hello", 1), ("moon", -1))
    feature_extractor = submission.extract_word_features
    weights = submission.learn_predictor(train_examples, test_examples, feature_extractor, num_epochs=20, eta=0.01)
    grader.require_is_greater_than(0, weights["hello"])
    grader.require_is_less_than(0, weights["moon"])
grader.add_basic_part('3b-0-basic', test3b0, max_seconds=1, description="basic sanity check for learning correct weights on two training and testing examples each")

def test3b1():
    train_examples = (("hi bye", 1), ("hi hi", -1))
    test_examples = (("hi", -1), ("bye", 1))
    feature_extractor = submission.extract_word_features
    weights = submission.learn_predictor(train_examples, test_examples, feature_extractor, num_epochs=20, eta=0.01)
    grader.require_is_less_than(0, weights["hi"])
    grader.require_is_greater_than(0, weights["bye"])
grader.add_basic_part('3b-1-basic', test3b1, max_seconds=2, description="test correct overriding of positive weight due to one negative instance with repeated words")

def test3b2():
    train_examples = read_examples('polarity.train')
    validation_examples = read_examples('polarity.dev')
    feature_extractor = submission.extract_word_features
    weights = submission.learn_predictor(train_examples, validation_examples, feature_extractor, num_epochs=20, eta=0.01)
    output_weights(weights, 'weights')
    output_error_analysis(validation_examples, feature_extractor, weights, 'error-analysis')  # Use this to debug
    trainError = evaluate_predictor(train_examples, lambda x : (1 if dot_product(feature_extractor(x), weights) >= 0 else -1))
    validationError = evaluate_predictor(validation_examples, lambda x : (1 if dot_product(feature_extractor(x), weights) >= 0 else -1))
    print(("Official: train error = %s, validation error = %s" % (trainError, validationError)))
    grader.require_is_less_than(0.04, trainError)
    grader.require_is_less_than(0.30, validationError)
grader.add_basic_part('3b-2-basic', test3b2, max_points=2, max_seconds=16, description="test classifier on real polarity dev dataset")

### 3c

def test3c0():
    weights = {"hello": 1, "world": 1}
    data = submission.generate_dataset(5, weights)
    for datapt in data:
        grader.require_is_equal((util.dot_product(datapt[0], weights) >= 0), (datapt[1] == 1))
grader.add_basic_part('3c-0-basic', test3c0, max_seconds=2, description="test correct generation of small dataset labels")

def test3c1():
    weights = {}
    for _ in range(100):
        k = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        v = random.uniform(-1, 1)
        weights[k] = v
    data = submission.generate_dataset(100, weights)
    for phi, y in data:
        grader.require_is_equal(util.dot_product(phi, weights) >= 0, y == 1)
grader.add_basic_part('3c-1-basic', test3c1, max_seconds=2, description="test correct generation of large random dataset labels")

### 3d

def test3d0():
    fe = submission.extract_character_features(3)
    sentence = "hello world"
    ans = {"hel":1, "ell":1, "llo":1, "low":1, "owo":1, "wor":1, "orl":1, "rld":1}
    grader.require_is_equal(ans, fe(sentence))
grader.add_basic_part('3d-0-basic', test3d0, max_seconds=1, description="test basic character n-gram features")

def test3d1():
    random.seed(42)
    for i in range(10):
        sentence = ' '.join([random.choice(['a', 'aa', 'ab', 'b', 'c']) for _ in range(100)])
        for n in range(1, 4):
            submission_ans = submission.extract_character_features(n)(sentence)
grader.add_hidden_part('3d-1-hidden', test3d1, max_seconds=2, description="test feature extraction on repeated character n-grams")

### 3e

grader.add_manual_part('3e', max_points=3, description='explain value of n-grams')

############################################################
# Problem 4: maximum group loss
############################################################

grader.add_manual_part('4a', max_points=2, description='summarize prediction rules')
grader.add_manual_part('4b', max_points=3, description='classifier 1 average loss')
grader.add_manual_part('4c', max_points=3, description='classifier 2 average loss')
grader.add_manual_part('4d', max_points=4, description='deploying classifier')
############################################################
# Problem 5: clustering
############################################################

grader.add_manual_part('5a', max_points=2, description='simulating 2-means')

# basic test for k-means
def test5b0():
    random.seed(42)
    x1 = {0:0, 1:0}
    x2 = {0:0, 1:1}
    x3 = {0:0, 1:2}
    x4 = {0:0, 1:3}
    x5 = {0:0, 1:4}
    x6 = {0:0, 1:5}
    examples = [x1, x2, x3, x4, x5, x6]
    centers, assignments, total_cost = submission.kmeans(examples, 2, max_epochs=10)
    
    grader.require_is_true(grader_util.is_collection(centers))
    grader.require_is_true(isinstance(centers[0], dict))
    grader.require_is_true(isinstance(list(centers[0].values())[0], float) or isinstance(list(centers[0].values())[0], int))
    grader.require_is_true(len(assignments) == len(examples))
    for assignment in assignments:
        grader.require_is_true(assignment in [0, 1])
    # (there are two stable centroid locations)
    grader.require_is_true(round(total_cost, 3) == 4 or round(total_cost, 3) == 5.5 or round(total_cost, 3) == 5.0)
grader.add_basic_part('5b-0-basic', test5b0, max_seconds=1, description="test basic k-means on hardcoded datapoints")

def test5b1():
    random.seed(42)
    K = 6
    best_centers = None
    best_assignments = None
    best_total_cost = None
    examples = generate_clustering_examples(num_examples=1000, num_words_per_topic=3, num_filler_words=1000)
    centers, assignments, total_cost = submission.kmeans(examples, K, max_epochs=100)
grader.add_hidden_part('5b-1-hidden', test5b1, max_points=1, max_seconds=4, description="test stability of cluster assignments")

def test5b2():
    random.seed(42)
    K = 6
    best_centers = None
    best_assignments = None
    best_total_cost = None
    examples = generate_clustering_examples(num_examples=1000, num_words_per_topic=3, num_filler_words=1000)
    centers, assignments, total_cost = submission.kmeans(examples, K, max_epochs=100)
grader.add_hidden_part('5b-2-hidden', test5b2, max_points=1, max_seconds=4, description="test stability of cluster locations")

def test5b3():
    random.seed(42)
    K = 6
    best_centers = None
    best_assignments = None
    best_total_cost = None
    examples = generate_clustering_examples(num_examples=10000, num_words_per_topic=3, num_filler_words=10000)
    centers, assignments, total_cost = submission.kmeans(examples, K, max_epochs=100)
    grader.require_is_less_than(10e6, total_cost)
    averages = []

    for center in centers:
        xs = [examples[i] for i in range(len(examples)) if centers[assignments[i]] == center]
        all_words = []
        for x in xs:
            for key in list(x.keys()):
                if key not in all_words:
                    all_words.append(key)
        word_vals = [(word, sum([x[word] for x in xs])*1.0/len(xs)) for word in all_words]
        avg = dict(word_vals)
        averages.append(avg)

grader.add_hidden_part('5b-3-hidden', test5b3, max_points=2, max_seconds=11, description="make sure the code runs fast enough")

grader.add_manual_part('5c', max_points=2, description='scaling kmeans')

grader.grade()
