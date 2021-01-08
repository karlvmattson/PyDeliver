# A single package to be delivered
class Package:
    _id = 0
    _address = ""
    _deadline = ""
    _city = ""
    _zip = ""
    _weight = 0.0
    _status = ""

    def __init__(self, new_id, address, deadline, city, postal_code, weight, status):
        self._id = new_id
        self._address = address
        self._deadline = deadline
        self._city = city
        self._zip = postal_code
        self._weight = weight
        self._status = status

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
        return self._deadline

    def set_city(self, new_city):
        self._city = new_city

    def get_city(self):
        return self._city

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