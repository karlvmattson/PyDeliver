# Functions for importing required csv files
import csv
import packagehash
import package


# Imports distance table.
# Runs in O(n*n) time where n is the number of addresses in the table
def import_distances():
    distance_reader = csv.reader(open('WGUPS Distance Table.csv'), delimiter=',', skipinitialspace=True)

    distance_dict = {}
    col_headers = distance_reader.__next__()

    # iterate through each row to create dict entries
    for row in distance_reader:
        source_address = row[0]
        # iterate through each column in the row
        for i in range(1, len(row)):
            current_cell = float(row[i])
            if current_cell == 0:
                break
            destination_address = col_headers[i]
            distance_dict[source_address + destination_address] = current_cell
    return distance_dict


# Imports package table.
# Runs in O(n) time where n is the number of packages to import
def import_packages(package_hash):
    package_reader = csv.reader(open('WGUPS Package File.csv'), delimiter=',', skipinitialspace=True)

    col_headers = package_reader.__next__()

    # iterate through each row to load packages
    for row in package_reader:
        package_id = int(row[0])
        address = row[1]
        city = row[2]
        state = row[3]
        postal_code = row[4]
        deadline = row[5]
        weight = row[6]
        truck = row[7]
        depart = row[8]

        # create package object
        new_package = package.Package(package_id, address, deadline, city, state, postal_code, weight, truck, depart)

        # add package to hash table
        package_hash.add(new_package)

        # test that package added correctly
        # print((package_hash.get_package(package_id)).get_address())
