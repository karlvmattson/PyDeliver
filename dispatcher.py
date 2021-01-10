# Handles dispatching of trucks
import truck


class Dispatcher:

    def __init__(self, time, trucks, drivers, distances):
        self._distances = distances
        self._current_time = time
        self._trucks = trucks
        self._drivers = drivers

    def dispatch_trucks(self):
        current_time = self._current_time
        distance_traveled = 0
        drivers_at_hub = self._drivers
        trucks = self._trucks
        trucks_to_send = len(trucks)
        trucks_returned = 0
        while trucks_returned < trucks_to_send:
            result = trucks[trucks_returned].depart(current_time, self._distances)
            current_time = result[0]
            distance_traveled += result[1]
            trucks_returned += 1

        return [current_time, distance_traveled]
