# Contains algorithm for truck loading
import truck
import distancetable
import packagehash
import package


def get_closest_package(location, package_list, packages, distances):
    closest_package = 0
    closest_distance = float("inf")
    for p in package_list:
        distance_to_package = distancetable.Distances.get_distance(
            distances, location, packagehash.PackageHash.get_package(packages, p))
        if distance_to_package < closest_distance:
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
        done = False

        while not done:

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
                # if truck time passes delivery requirement push package back onto package_bucket for the next truck
                # make sure truck doesn't leave before earliest delivery







            break





            # Queue up trucks 1 and 2 from their pool and the full set of packages
            #     If a truck has >= 8 packages, is close to hub, and their sublist is empty return to hub
            #     Finish other truck
            # Queue up truck 3


            # check if we are finished
            if len(package_bucket) == 0:
                done = True
                for b in truck_bucket:
                    if len(b) > 0:
                        done = False

        return trucks

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
