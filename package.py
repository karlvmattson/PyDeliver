# A single package to be delivered
import datetime


class Package:

    def __init__(self, new_id, address, deadline, city, state,
                 postal_code, weight, requested_truck, requested_departure):
        self._id = new_id
        self._address = address
        self._deadline = deadline
        self._city = city
        self._state = state
        self._zip = postal_code
        self._weight = weight
        self._requested_truck = requested_truck
        self._departed = datetime.datetime.min
        self._delivered = datetime.datetime.min
        self._status = "At the hub"
        if requested_departure == "":
            self._requested_departure = datetime.datetime.min
        else:
            self._requested_departure = datetime.datetime.strptime(requested_departure.replace(" AM", ""), "%H:%M")

    def set_id(self, new_id):
        self._id = new_id

    def get_id(self):
        return self._id

    def set_address(self, new_address):
        self._address = new_address

    def get_address(self):
        return self._address

    def set_deadline(self, new_deadline):
        self._deadline = new_deadline

    def get_deadline(self):
        if self._deadline == "EOD":
            return self._deadline
        else:
            return datetime.datetime.strptime(self._deadline.replace(" AM", ""), "%H:%M")

    def set_city(self, new_city):
        self._city = new_city

    def get_city(self):
        return self._city

    def set_state(self, new_state):
        self._state = new_state

    def get_state(self):
        return self._state

    def set_zip(self, new_zip):
        self._zip = new_zip

    def get_zip(self):
        return self._zip

    def set_weight(self, new_weight):
        self._weight = new_weight

    def get_weight(self):
        return self._weight

    def set_status(self, new_status):
        self._status = new_status

    def get_status(self):
        return self._status

    def set_departed(self, new_departed):
        self._departed = new_departed

    def get_departed(self):
        return self._departed

    def set_delivered(self, new_delivered):
        self._delivered = new_delivered

    def get_delivered(self):
        return self._delivered

    def set_requested_truck(self, new_requested_truck):
        self._requested_truck = new_requested_truck

    def get_requested_truck(self):
        return self._requested_truck

    def set_requested_departure(self, new_requested_departure):
        self._requested_departure = new_requested_departure

    def get_requested_departure(self):
        return self._requested_departure
