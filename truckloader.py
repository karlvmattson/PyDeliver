# Contains algorithm for truck loading
import truck
import distancetable
import packagehash
import package
import datetime


def get_closest_package(location, package_list, packages, distances):
    closest_package = 0
    closest_distance = float("inf")
    for p in package_list:
        distance_to_package = distances.get_distance(
            location, packagehash.PackageHash.get_package(packages, p).get_address())
        if distance_to_package < closest_distance:
            closest_package = p
            closest_distance = distance_to_package

    return [closest_package, closest_distance]


def get_farthest_package(package_list, packages, distances):
    location = "HUB"
    farthest_distance = 0
    farthest_package = None
    for p in package_list:

        distance_to_package = distances.get_distance(
            location, packagehash.PackageHash.get_package(packages, p).get_address())
        if distance_to_package > farthest_distance:
            farthest_package = p
            farthest_distance = distance_to_package

    return [farthest_package, farthest_distance]


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

    def load_onto_truck(self, target_truck, location, current_time, package_list, packages, distances, depth_first):
        new_location = location
        new_time = current_time
        leftover_packages = []
        farthest_package = 0

        # if going for depth first, start with the furthest package from the depot and run from there
        if depth_first:
            # find farthest package
            result = get_farthest_package(package_list, packages, distances)
            farthest_package = result[0]
        else:
            result = [None, None]

        while len(package_list) > 0:
            # find next package
            if farthest_package > 0:
                farthest_package = 0
            else:
                result = get_closest_package(location, package_list, packages, distances)
            closest_distance = result[1]
            next_package = result[0]
            new_location = packages.get_package(next_package).get_address()
            target_truck.load_package(packages.get_package(next_package))
            package_list.remove(next_package)

            # update truck's departure time
            if target_truck.get_earliest_departure() < packages.get_package(next_package).get_requested_departure():
                target_truck.set_earliest_departure(packages.get_package(next_package).get_requested_departure())

            # see if truck is full
            if len(target_truck.delivery_queue) == self._load_limit:
                # move remaining packages to leftovers
                leftover_packages.extend(package_list)
                return [new_location, new_time, leftover_packages]

        return [new_location, new_time, leftover_packages]

    def load_trucks(self, trucks, packages, distances):

        # Assumption: we have enough trucks for all packages
        # Assumption: we don't want to re-load any trucks mid-day

        # Create a bucket for each truck and an additional bucket for available packages
        package_bucket = []
        truck_bucket = [[] for t in range(len(trucks))]

        # Copy package ids into their requested buckets to be loaded to trucks
        for p in packages:
            if len(p.get_requested_truck()) > 0:
                truck_bucket[int(p.get_requested_truck()) - 1].append(p.get_id())
            else:
                package_bucket.append(p.get_id())

        # Queue up deliveries
        # done = False
        #
        # while not done:

        for t in range(len(trucks)):
            truck_time = self._start_time
            truck_location = "HUB"
            early_packages = []

            for p in range(len(truck_bucket[t])):
                p_id = truck_bucket[t][p]
                if packages.get_package(p_id).get_deadline() != "EOD":
                    early_packages.append(truck_bucket[t][p])
            for p in range(len(package_bucket)):
                p_id = package_bucket[p]
                if packages.get_package(p_id).get_deadline() != "EOD":
                    early_packages.append(package_bucket[p])
            for i in early_packages:
                if i in truck_bucket[t]:
                    truck_bucket[t].remove(i)
                elif i in package_bucket:
                    package_bucket.remove(i)

            print("Truck " + repr(t + 1) + " has " + repr(len(early_packages)) + " early packages to deliver.")

            # peel off packages in groups by delivery time, then run greedy on those subgroups from last location
            while len(early_packages) > 0:
                current_earliest = datetime.datetime.max
                current_list = []
                for p in range(len(early_packages)):
                    p_id = early_packages[p]
                    if packages.get_package(p_id).get_deadline() < current_earliest:
                        current_list.clear()
                        current_earliest = packages.get_package(p_id).get_deadline()
                        current_list.append(p_id)
                    elif packages.get_package(p_id).get_deadline() == current_earliest:
                        current_list.append(p_id)
                results = self.load_onto_truck(trucks[t], truck_location, truck_time, current_list, packages, distances,
                                               False)
                # [new_location, new_time, leftover_packages]
                # make sure any leftover packages go to the next truck
                if len(results[2]) > 0:
                    print(repr(len(results[2])) + " packages did not get onto the truck! Check for delivery errors.")
                    truck_bucket[t + 1].extend(results[2])
                # update truck time and location
                truck_location = results[0]
                truck_time = results[1]

                # remove any packages on the truck from the early list
                for p in trucks[t].delivery_queue:
                    if p.get_id() in early_packages:
                        early_packages.remove(p.get_id())

                # repeats process until early packages are loaded

            # finish truck-specific packages
            if len(truck_bucket[t]) > 0:
                self.load_onto_truck(trucks[t], truck_location, truck_time, truck_bucket[t], packages, distances, True)

            # pass package_bucket to be loaded to the truck until truck is full or bucket runs out
            if len(package_bucket) > 0:
                results = self.load_onto_truck(trucks[t], truck_location, truck_time,
                                               package_bucket, packages, distances, True)
                package_bucket = results[2]
            print("Truck " + repr(t + 1) + " is loaded with " + repr(len(trucks[t].delivery_queue)) + " packages!")

        return trucks

        # Queue up trucks 1 and 2 from their pool and the full set of packages
        #     If a truck has >= 8 packages, is close to hub, and their sublist is empty return to hub
        #     Finish other truck
        # Queue up truck 3

        # check if we are finished
        # if len(package_bucket) == 0:
        #     done = True
        #     for b in truck_bucket:
        #         if len(b) > 0:
        #             done = False

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
