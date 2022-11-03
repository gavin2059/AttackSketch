from typing import Callable
from sklearn.utils import murmurhash3_32
import random

"""
Factory for generating hash functions
"""


class HashFactory:
    """
    Initializes a new Hash Factory
    """

    def __init__(self):
        self.seed = 777777
        random.seed(99)

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

    """
    Gets a 2-universal hash function
    Inputs:
        table_size (int) - the number of hash table slots the hash function outputs to
        a (int) - the first constant in the 2-universal hash function
        b (int) - the second constant in the 2-universal hash function
    Outputs:
        (Callable) - the generated hash function
    """

    def get2UnivFunction(self, table_size: int, a: int = 0, b: int = 0) -> Callable:
        if not a:
            a = random.randint(0, 9999999)
        if not b:
            b = random.randint(0, 9999999)
        print(a, b)
        return lambda x: (a * x + b) % table_size
