# Contains algorithm for truck loading
import truck
import distancetable
import packagehash
import package


class TruckLoader:
    _load_limit = 0
    _drivers = 0
    _start_time = 0
    _vehicle_speed = 0

    def __init__(self, drivers, load_limit, start_time, truck_speed):
        self._drivers = drivers
        self._load_limit = load_limit
        self._start_time = start_time
        self._vehicle_speed = truck_speed

    def load_trucks(self, trucks, packages, distances):

        # Assumption: we have enough trucks for all packages
        # Assumption: we don't want to re-load any trucks mid-day

        # This algorithm loads all packages onto trucks in order without regard to any requirements or efficiency
        # Operates in O(n) time where n is the number of packages
        truck_pointer = 0
        packages_in_truck = 0
        for p in packages:
            # make sure current truck has room for packages, move to next truck if not
            if packages_in_truck == self._load_limit:
                truck_pointer += 1
                packages_in_truck = 0

            trucks[truck_pointer].load_package(p)
            packages_in_truck += 1
            # print("Loaded package " + repr(p.get_id()) + " onto truck " + repr(truck_pointer + 1))

        return trucks
