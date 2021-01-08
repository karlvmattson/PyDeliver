# Implements a direct-address hash table. Self-adjusts to resize the table as needed.
# All operations run in O(1) time
class PackageHash:
    _hash_table = []

    def __init__(self):
        # start with array size 20
        self._hash_table = [None]*20

    # Self-adjusting function
    def add(self, package):
        # this is the hashing function, directly map to package id
        new_id = package.get_id()-1

        # resize list if it is too small for the new id
        if new_id >= len(self._hash_table):
            self._hash_table.append([None] * (1 + new_id - len(self._hash_table)))

        # store new information
        self._hash_table[new_id] = package

    def remove(self, key):
        # make sure key is valid
        if key - 1 < len(self._hash_table):
            self._hash_table[key-1] = None

    def get_package(self, key):
        # make sure key is valid
        if key - 1 < len(self._hash_table):
            return self._hash_table[key - 1]
        else:
            return None

