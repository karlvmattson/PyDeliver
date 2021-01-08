# Functions for importing required csv files
import csv


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


def import_packages():
    pass
