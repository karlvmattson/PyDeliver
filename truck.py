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
        self._current_time = 0
        self._current_location = "HUB"
        self._earliest_departure = earliest_departure

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
        package.set_status("Loaded")
        #   print("Now carrying " + repr(len(self.delivery_queue)) + " packages.")

    def deliver(self, package):
        package.set_status("Delivered")
        package.set_delivered(self._current_time)
        if package.get_deadline() != "EOD":
            if package.get_deadline() < self._current_time:
                print("Package was delivered late!")

    def travel(self, destination, distance_table):

        # calculate distance to next stop
        distance = distance_table.get_distance(self._current_location, destination)
        #print("Distance from " + self._current_location + " to " + destination + " is " + repr(distance))

        # increment distance and time, set current location to next stop
        #print("Time before traveling is " + self.get_current_time().strftime(self.format))
        self.set_distance_traveled(self.get_distance_traveled() + distance)
        time = self.get_current_time()
        new_time = time + datetime.timedelta(hours=(distance / self.get_speed()))
        self.set_current_time(new_time)
        #print("Time after traveling is " + self.get_current_time().strftime(self.format))
        self.set_current_location(destination)

    # main simulation for an individual truck
    def depart(self, time, distancetable):
        self.set_current_time(time)

        # set all packages on truck to En route and log their departure time
        for package in self.delivery_queue:
            package.set_status("En route")
            package.set_departed(time)

        # load next package
        for package in self.delivery_queue:
            # travel to next stop
            self.travel(package.get_address(), distancetable)

            # deliver current package
            self.deliver(package)

        # clear delivery queue
        self.delivery_queue.clear()

        # when finished delivering packages return to hub
        self.travel("HUB", distancetable)

        # return current time and distance traveled
        return [self.get_current_time(), self.get_distance_traveled()]
