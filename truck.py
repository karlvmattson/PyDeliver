# A delivery truck
import package
import distancetable
import packagehash
import time
import datetime


class Truck:
    _speed = 18

    def __init__(self, earliest_departure):
        self.format = "%H:%M"
        self.delivery_queue = []
        self._distance_traveled = 0
        self._current_time = datetime.datetime.min
        self._current_location = "HUB"
        self._earliest_departure = earliest_departure
        self.early_package_count = 0

    def package_count(self):
        return len(self.delivery_queue)

    def get_speed(self):
        return self._speed

    def set_speed(self, new_speed):
        self._speed = new_speed

    def get_earliest_departure(self):
        return self._earliest_departure

    def set_earliest_departure(self, new_earliest_departure):
        self._earliest_departure = new_earliest_departure

    def get_current_time(self):
        return self._current_time

    def set_current_time(self, new_time):
        self._current_time = new_time

    def get_current_location(self):
        return self._current_location

    def set_current_location(self, new_location):
        self._current_location = new_location

    def get_distance_traveled(self):
        return self._distance_traveled

    def set_distance_traveled(self, new_distance_traveled):
        self._distance_traveled = new_distance_traveled

    def load_package(self, package):
        self.delivery_queue.append(package)

    def deliver(self, package):
        package.set_status("Delivered")
        package.set_delivered(self._current_time)
        if package.get_deadline() != "EOD":
            if package.get_deadline() < self._current_time:
                print("Package was delivered late!")

    # Moves the truck from its current location to a destination.
    # Increments truck time based on distance and truck speed.
    def travel(self, destination, distance_table, end_time):

        # calculate distance to next stop
        distance = distance_table.get_distance(self._current_location, destination)

        # increment distance and time, set current location to next stop
        self.set_distance_traveled(self.get_distance_traveled() + distance)
        time = self.get_current_time()
        new_time = time + datetime.timedelta(hours=(distance / self.get_speed()))
        if new_time > end_time:
            self.set_current_time(end_time)
            return False

        self.set_current_time(new_time)
        self.set_current_location(destination)
        return True

    # main delivery simulation for an individual truck
    def depart(self, time, distancetable, end_time):
        self.set_current_time(time)

        # set all packages on truck to En route and log their departure time
        for package in self.delivery_queue:
            package.set_status("En route")
            package.set_departed(time)

        # load next package
        for package in self.delivery_queue:
            # travel to next stop
            if not self.travel(package.get_address(), distancetable, end_time):
                # we ran up against the user specified stop time
                return [self.get_current_time(), self.get_distance_traveled()]

            # deliver current package
            self.deliver(package)

        # clear delivery queue
        self.delivery_queue.clear()

        # when finished delivering packages return to hub
        self.travel("HUB", distancetable, end_time)

        # return current time and distance traveled
        return [self.get_current_time(), self.get_distance_traveled()]
