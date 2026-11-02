import collections
import math
from typing import Any, DefaultDict, List, Set, Tuple

############################################################
# Custom Types
# NOTE: You do not need to modify these.

"""
You can think of the keys of the defaultdict as representing the positions in
the sparse vector, while the values represent the elements at those positions.
Any key which is absent from the dict means that that element in the sparse
vector is absent (is zero).
Note that the type of the key used should not affect the algorithm. You can
imagine the keys to be integer indices (e.g., 0, 1, 2) in the sparse vectors,
but it should work the same way with arbitrary keys (e.g., "red", "blue",
"green").
"""
SparseVector = DefaultDict[Any, float]
Position = Tuple[int, int]


############################################################
# Problem 4a

def find_alphabetically_first_word(text: str) -> str:
    """
    Given a string |text|, return the word in |text| that comes first
    lexicographically (i.e., the word that would come first after sorting).
    A word is defined by a maximal sequence of characters without whitespaces.
    Words are case sensitive -- i.e. we may not assume that letters are all in lowercase.
    You might find min() handy here. If the input text is an empty string,
    it is acceptable to either return an empty string or throw an error.
    """
    # BEGIN_SOLUTION
    # str.split() with no argument splits on runs of any whitespace, so each
    # element is exactly one "maximal sequence of characters without whitespace".
    # Python compares strings lexicographically by code point, which is the
    # case-sensitive order the problem asks for ('Z' < 'a').
    words = text.split()
    return min(words) if words else ''
    # END_SOLUTION


############################################################
# Problem 4b

def euclidean_distance(loc1: Position, loc2: Position) -> float:
    """
    Return the Euclidean distance between two locations, where the locations
    are pairs of numbers (e.g., (3, 5)).
    """
    # BEGIN_SOLUTION
    # sqrt((x1 - x2)^2 + (y1 - y2)^2); math.hypot computes exactly this and is
    # numerically more careful than squaring by hand.
    (x1, y1), (x2, y2) = loc1, loc2
    return math.hypot(x1 - x2, y1 - y2)
    # END_SOLUTION


############################################################
# Problem 4c

def mutate_sentences(sentence: str) -> List[str]:
    """
    Given a sentence (sequence of words), return a list of all "similar"
    sentences.
    We define a sentence to be "similar" to the original sentence if
      - it has the same number of words, and
      - each pair of adjacent words in the new sentence also occurs in the
        original sentence (the words within each pair should appear in the same
        order in the output sentence as they did in the original sentence).
    Notes:
      - The order of the sentences you output doesn't matter.
      - You must not output duplicates.
      - Your generated sentence can use a word in the original sentence more
        than once.
    Example:
      - Input: 'the cat and the mouse'
      - Output: ['and the cat and the', 'the cat and the mouse',
                 'the cat and the cat', 'cat and the cat and']
                (Reordered versions of this list are allowed.)
    """
    # BEGIN_SOLUTION
    words = sentence.split()
    length = len(words)

    # Build the "allowed transitions" graph: successors[w] is the set of words
    # that directly follow w somewhere in the original sentence. A similar
    # sentence is exactly a walk of `length` words in this graph.
    successors = collections.defaultdict(set)
    for current_word, next_word in zip(words, words[1:]):
        successors[current_word].add(next_word)

    results = set()  # a set removes duplicate walks automatically

    def extend(path: List[str]) -> None:
        """Depth-first extension of a partial walk until it has `length` words."""
        if len(path) == length:
            results.add(' '.join(path))
            return
        for next_word in successors[path[-1]]:
            extend(path + [next_word])

    # A walk may start at any distinct word of the sentence.
    for start_word in set(words):
        extend([start_word])
    return list(results)
    # END_SOLUTION


############################################################
# Problem 4d

def sparse_vector_dot_product(v1: SparseVector, v2: SparseVector) -> float:
    """
    Given two sparse vectors (vectors where most of the elements are zeros)
    |v1| and |v2|, each represented as collections.defaultdict(float), return
    their dot product.

    You might find it useful to use sum() and a list comprehension.
    This function will be useful later for linear classifiers.
    Note: A sparse vector has most of its entries as 0.
    """
    # BEGIN_SOLUTION
    # Only keys present in BOTH vectors contribute, so iterate over the smaller
    # vector and look the key up in the larger one. Use .get() rather than
    # indexing: indexing a defaultdict would insert zero entries as a side effect.
    if len(v1) > len(v2):
        v1, v2 = v2, v1
    return sum(value * v2.get(key, 0.0) for key, value in v1.items())
    # END_SOLUTION


############################################################
# Problem 4e

def increment_sparse_vector(v1: SparseVector, scale: float, v2: SparseVector,
) -> None:
    """
    Given two sparse vectors |v1| and |v2|, perform v1 += scale * v2.
    If the scale is zero, you are allowed to modify v1 to include any
    additional keys in v2, or just not add the new keys at all.

    NOTE: This function should MODIFY v1 in-place, but not return it.
    Do not modify v2 in your implementation.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_SOLUTION
    # Every key of v2 touches v1; keys of v1 that are absent from v2 stay as
    # they are (scale * 0 adds nothing). .get() keeps this correct even if v1
    # is a plain dict rather than a defaultdict.
    for key, value in v2.items():
        v1[key] = v1.get(key, 0.0) + scale * value
    # END_SOLUTION


############################################################
# Problem 4f

def find_nonsingleton_words(text: str) -> Set[str]:
    """
    Split the string |text| by whitespace and return the set of words that
    occur more than once.
    You might find it useful to use collections.defaultdict(int).
    """
    # BEGIN_SOLUTION
    # Count every word in one pass, then keep the words seen at least twice.
    counts = collections.Counter(text.split())
    return {word for word, count in counts.items() if count > 1}
    # END_SOLUTION
