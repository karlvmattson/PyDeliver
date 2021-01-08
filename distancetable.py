# Holds the distance dictionary
import csvimport


class Distances:
    _distance_dict = {}

    def __init__(self):
        self._distance_dict = csvimport.import_distances()

    def get_distances(self):
        return self._distance_dict

    def get_distance(self, source_address, destination_address):
        if source_address + destination_address in self._distance_dict.keys():
            return self._distance_dict[source_address + destination_address]
        elif destination_address + source_address in self._distance_dict.keys():
            return self._distance_dict[destination_address + source_address]
        elif source_address == destination_address:
            return 0
        else:
            return None
