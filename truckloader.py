# Contains algorithm for truck loading
import datetime
import packagehash


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


def get_closest_outward_package(location, package_list, packages, distances):
    closest_package = 0
    closest_distance = float("inf")
    for p in package_list:
        distance_to_package = distances.get_distance(
            location, packagehash.PackageHash.get_package(packages, p).get_address())
        if distance_to_package < closest_distance and distances.get_distance(
            "HUB", packagehash.PackageHash.get_package(packages, p).get_address()) > \
                distances.get_distance("HUB", location):
            closest_package = p
            closest_distance = distance_to_package

    return [closest_package, closest_distance]


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

    def load_onto_truck(self, target_truck, location, current_time, package_list,
                        packages, distances, depth_first, optional_packages):
        new_location = location
        new_time = current_time
        leftover_packages = []

        while len(package_list) > 0 and len(target_truck.delivery_queue) < self._load_limit:
            # find next package
            if (self._load_limit - len(target_truck.delivery_queue)) == len(package_list):
                result = get_closest_package(location, package_list, packages, distances)
            elif depth_first:
                result = get_closest_outward_package(location, package_list + optional_packages, packages, distances)
                if result[0] == 0:
                    result = get_closest_package(location, package_list + optional_packages, packages, distances)
            else:
                result = get_closest_package(location, package_list + optional_packages, packages, distances)
                if result[1] > 0:
                    result = get_closest_package(location, package_list, packages, distances)
            next_package = result[0]
            new_location = packages.get_package(next_package).get_address()
            target_truck.load_package(packages.get_package(next_package))
            if next_package in package_list:
                package_list.remove(next_package)
            else:
                optional_packages.remove(next_package)

            # update truck's departure time
            if target_truck.get_earliest_departure() < packages.get_package(next_package).get_requested_departure():
                target_truck.set_earliest_departure(packages.get_package(next_package).get_requested_departure())

            # see if truck is full
           # print("Truck has " + repr(len(target_truck.delivery_queue)) + " packages out of " + repr(self._load_limit))
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
        truck_bucket = [[] for _ in range(len(trucks))]

        # Copy package ids into their requested buckets to be loaded to trucks
        for p in packages:
            if len(p.get_requested_truck()) > 0:
                truck_bucket[int(p.get_requested_truck()) - 1].append(p.get_id())
            else:
                package_bucket.append(p.get_id())

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

           # print("Truck " + repr(t + 1) + " has " + repr(len(early_packages)) + " early packages to deliver.")
            trucks[t].early_package_count = len(early_packages)

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
                                               False, truck_bucket[t] + package_bucket)
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
                    if p.get_id() in package_bucket:
                        package_bucket.remove(p.get_id())
                    if p.get_id() in truck_bucket[t]:
                        truck_bucket[t].remove(p.get_id())

                # repeats process until early packages are loaded

            # finish truck-specific packages
            if len(truck_bucket[t]) > 0:
                self.load_onto_truck(trucks[t], truck_location, truck_time,
                                     truck_bucket[t], packages, distances, True, package_bucket)
                for p in trucks[t].delivery_queue:
                    if p.get_id() in package_bucket:
                        package_bucket.remove(p.get_id())

            # pass package_bucket to be loaded to the truck until truck is full or bucket runs out
            if len(package_bucket) > 0:
                results = self.load_onto_truck(trucks[t], truck_location, truck_time,
                                               package_bucket, packages, distances, True, [])
                for p in trucks[t].delivery_queue:
                    if p.get_id() in package_bucket:
                        package_bucket.remove(p.get_id())
            # print("Truck " + repr(t + 1) + " is loaded with " + repr(len(trucks[t].delivery_queue)) + " packages!")

        return trucks
