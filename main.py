# Karl Mattson - #001253438
# This program simulates delivery of packages

import distancetable
import packagehash
import datetime
import truck
import truckloader
import dispatcher


# get distances from CSV
distances = distancetable.Distances()

# get packages from CSV
packages = packagehash.PackageHash()

# set up scenario variables
total_trucks = 3
total_drivers = 2
vehicle_speed = 18
truck_load_limit = 16
starting_time = datetime.datetime.strptime("08:00", '%H:%M')

# create trucks
truck_list = [truck.Truck(starting_time) for i in range(total_trucks)]

# load trucks
truck_loader = truckloader.TruckLoader(total_drivers, truck_load_limit, starting_time, vehicle_speed)
truck_loader.load_trucks(truck_list, packages, distances)
# for t in range(len(truck_list)):
#     print("Truck " + repr(t) + " has " + repr(truck_list[t].package_count()) + " packages.")
print("Load process finished...")
#exit(0)
# send trucks on deliveries
dispatcher = dispatcher.Dispatcher(starting_time, truck_list, total_drivers, distances)
results = dispatcher.dispatch_trucks()

# print results
print("Finished time is " + results[0].strftime("%H:%M"))
print("Finished distance is " + repr(results[1]))










# #test code for package table import
# packages.print_contents()


# test code for distance table import
# test_addresses = ['HUB', '1060 Dalton Ave S', '1330 2100 S','1488 4800 S', '177 W Price Ave', '195 W Oakland Ave']
# for i in range(len(test_addresses)):
#     for j in range(len(test_addresses)):
#         print("Source: " + test_addresses[i] + " --- Destination: " + test_addresses[j] +
#               " --- Distance: " + repr(distances.get_distance(test_addresses[i], test_addresses[j])))
