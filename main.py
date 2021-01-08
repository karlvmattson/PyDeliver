# Karl Mattson - #001253438
# This program simulates delivery of packages

import distancetable
import packagehash

# get distances from CSV
distances = distancetable.Distances()

# get packages from CSV
packages = packagehash.PackageHash()




# #test code for package table import
# packages.print_contents()


# test code for distance table import
# test_addresses = ['HUB', '1060 Dalton Ave S', '1330 2100 S','1488 4800 S', '177 W Price Ave', '195 W Oakland Ave']
# for i in range(len(test_addresses)):
#     for j in range(len(test_addresses)):
#         print("Source: " + test_addresses[i] + " --- Destination: " + test_addresses[j] +
#               " --- Distance: " + repr(distances.get_distance(test_addresses[i], test_addresses[j])))
