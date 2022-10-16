from bitarray import bitarray
from math import log, ceil
from HashFactory import HashFactory

"""
Simple Bloom Filter
"""


class BloomFilter:
    """
    Initializes a new Bloom Filter

    Inputs:
        false_positive_rate (int) - the desired false positive rate
        expected_keys (int) - the expected number of entries
        k (int) - the number of hash functions
        table_slots (int) - the number of hash table slots
    """

    def __init__(
        self,
        false_positive_rate: int,
        expected_keys: int,
        k: int = None,
        table_slots: int = None,
    ):
        self.expected_keys = expected_keys

        # get table slots
        if not table_slots:
            min_table_slots = log(false_positive_rate, 0.618) * expected_keys
            table_slots = 1
            while table_slots < min_table_slots:
                table_slots *= 2
        self.bitmap = bitarray("0" * table_slots)
        self.table_slots = table_slots

        # Generate hash functions
        if not k:
            k = ceil((table_slots / expected_keys * log(2)))  # R / N * ln(2)
            if false_positive_rate:
                while abs(
                    false_positive_rate - self.getExpectedFalsePositiveRate(k - 1)
                ) > abs(self.getExpectedFalsePositiveRate(k)):
                    k -= 1
        hash_factory = HashFactory()
        self.hash_functions = [
            hash_factory.getFunction(table_size=table_slots) for i in range(k)
        ]

    """
    Inserts a new key into the Bloom Filter

    Inputs:
        key (int) - the key to insert
    """

    def insert(self, key: int):
        for h in self.hash_functions:
            bit_to_set = h(key)
            self.bitmap[bit_to_set] = 1

    """
    Queries the Bloom Filter for a key

    Inputs:
        key (int) - the key to query for
    Outputs:
        (bool) - whether the key was previously inserted
    """

    def query(self, key: int) -> bool:
        for h in self.hash_functions:
            bit_to_check = h(key)
            if not self.bitmap[bit_to_check]:
                return False
        return True

    """
    Gets the expected false positive rate of the bloom filter

    Outputs:
        (float) - the calculated false positive rate
    """

    def getExpectedFalsePositiveRate(self, k: int) -> float:
        return (1 - (1 - 1 / self.table_slots) ** (k * self.expected_keys)) ** k
