# Handles dispatching of trucks
import truck
import datetime


class Dispatcher:
    format = "%H:%M"

    def __init__(self, time, trucks, drivers, distances):
        self._distances = distances
        self._current_time = time
        self._trucks = trucks
        self._drivers = drivers

    def dispatch_trucks(self):
        current_time = self._current_time
        distance_traveled = 0
        drivers_at_hub = self._drivers
        driver_availability = []
        trucks = self._trucks
        trucks_to_send = len(trucks)
        trucks_returned = 0
        last_truck_returned = self._current_time

        # check if there are no more packages to deliver
        while trucks_returned < trucks_to_send:
            # check if truck is eligible to depart

            for t in trucks:
                if drivers_at_hub > 0 and t.package_count() > 0 and t.get_earliest_departure() <= current_time:
                    # if so, send truck
                    drivers_at_hub -= 1
                    print("Sending truck at " + current_time.strftime(self.format))
                    result = t.depart(current_time, self._distances)
                    print("Truck returned at " + result[0].strftime(self.format) + " after driving " + repr(
                        result[1]) + " miles.")
                    distance_traveled += result[1]
                    if last_truck_returned < result[0]:
                        last_truck_returned = result[0]
                    trucks_returned += 1
                    # add driver to driver queue
                    if len(driver_availability) == 0:
                        driver_availability.append(result[0])
                    else:
                        for i in range(len(driver_availability)):
                            if result[0] <= driver_availability[i]:
                                driver_availability.insert(i, result[0])
                                break

            # check if we are done
            if trucks_returned == trucks_to_send:
                break

            # if no truck eligible to depart, advance time until a truck is eligible
            # are we out of drivers?
            if drivers_at_hub == 0:
                print("Waiting for driver...")
                # advance time until a driver is available
                current_time = driver_availability.pop(0)
                drivers_at_hub += 1
            else:
                # we must be waiting for a truck to reach its earliest departure
                # advance time to next available truck
                print("Waiting for next truck to be eligible to depart...")
                earliest_truck = [0, float("inf")]
                for t in range(len(trucks)):
                    departure = trucks[t].get_earliest_departure()
                    if trucks[t].package_count() > 0 and departure < earliest_truck[1]:
                        earliest_truck[0] = t
                        earliest_truck[1] = departure
                current_time = earliest_truck[1]

        # if not, return results
        return [last_truck_returned, distance_traveled]

        # most basic algorithm, sends trucks one at a time
        # result = trucks[trucks_returned].depart(current_time, self._distances)
        # current_time = result[0]
        # distance_traveled += result[1]
        # trucks_returned += 1
