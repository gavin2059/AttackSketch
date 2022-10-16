from typing import Callable
from sklearn.utils import murmurhash3_32

"""
Factory for generating hash functions
"""


class HashFactory:
    """
    Initializes a new Hash Factory
    """

    def __init__(self):
        self.seed = 777777

    """
    Gets a hash function
    Inputs:
        table_size (int) - the number of hash table slots the hash function outputs to
    Outputs:
        (Callable) - the generated hash function
    """

    def getFunction(self, table_size: int) -> Callable:
        self.seed += 111111
        seed_copy = self.seed  # prevent all functions using the same seed by reference
        return lambda x: murmurhash3_32(x, seed=seed_copy) % table_size
