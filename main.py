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

# display user interface and get user input
is_valid_input = False
user_input = ""
while not is_valid_input:
    print("WGUPS truck simulation.")
    print("Enter a time to stop simulation (HH:MM AM/PM)")
    print("or press enter to run program to its conclusion.")
    user_input = input("-->  ")
    if user_input == "":
        user_input = datetime.datetime.strptime("22:00", "%H:%M")
        is_valid_input = True
    else:
        try:
            user_input = datetime.datetime.strptime(user_input, "%I:%M %p")
            is_valid_input = True
        except ValueError:
            print(ValueError("Incorrect format, should be HH:MM AM/PM"))

# send trucks on deliveries
dispatcher = dispatcher.Dispatcher(starting_time, truck_list, total_drivers, distances)
results = dispatcher.dispatch_trucks(user_input)

# print results
packages.print_all()
print("Finished time is " + results[0].strftime("%H:%M"))
print("Finished distance is " + repr(results[1]))
