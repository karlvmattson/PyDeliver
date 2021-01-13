# Implements a direct-address hash table. Self-adjusts to resize the table as needed.
# All operations run in O(1) time
import csvimport
import datetime


class PackageHash:
    _hash_table = []

    def __init__(self):
        # start with array size 20
        self._hash_table = [None] * 20
        self.load_packages()

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n >= len(self._hash_table):
            raise StopIteration
        else:
            self.n += 1
            return self._hash_table[self.n - 1]

    # Self-adjusting function
    def add(self, package):
        # this is the hashing function, directly map to package id
        new_id = package.get_id() - 1

        # resize list if it is too small for the new id
        if new_id >= len(self._hash_table):
            self._hash_table.extend([None] * (1 + new_id - len(self._hash_table)))

        # store new information
        self._hash_table[new_id] = package

    def remove(self, key):
        # make sure key is valid
        if key - 1 < len(self._hash_table):
            self._hash_table[key - 1] = None

    def get_package(self, key):
        # make sure key is valid
        if key - 1 < len(self._hash_table):
            return self._hash_table[key - 1]
        else:
            return None

    def load_packages(self):
        csvimport.import_packages(self)

    def print_all(self):
        for p in range(len(self._hash_table)):
            if self.get_package(p) is not None:
                pack = self.get_package(p + 1)
                i = pack.get_id()
                address = pack.get_address()
                departure = pack.get_departed()
                delivered = pack.get_delivered()
                deadline = pack.get_deadline()
                status = pack.get_status()
                if status == "At the hub":
                    departure = ""
                    delivered = ""
                elif status == "En route":
                    departure = datetime.datetime.strftime(departure, "%H:%M")
                    delivered = ""
                elif status == "Delivered":
                    departure = datetime.datetime.strftime(departure, "%H:%M")
                    delivered = datetime.datetime.strftime(delivered, "%H:%M")
                print('{:>4}:  Destination: {:<40}  Departed: {:>6}     Delivered: {:>6}     Status: {:<10}'.format(
                    i, address, departure, delivered, status))
