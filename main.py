import csv
import datetime
from HashMap import ChainingHashTable

hash_table = ChainingHashTable()

package_file = 'package_file.csv'
distance_file = 'distance_file.csv'
address_file = 'address_file.csv'

# Opening the package_file, and loading it into a list.
with open(package_file, newline='') as csvreader1:
  package_list = list(csv.reader(csvreader1, delimiter=','))

# Opening the distance_file, and loading them into a list.
with open(distance_file, newline='') as csvreader2:
  distance_list = list(csv.reader(csvreader2, delimiter=','))

# Opening the address_file, and loading it into a list.
with open(address_file, newline='') as csvreader3:
  address_list = list(csv.reader(csvreader3, delimiter=','))


def load_package_info(package_info_file):
  global hash_table  # Use the global hash_table variable
  with open(package_info_file) as packages:
    package_info = csv.reader(packages)
    for p in package_info:
      package_id_number = int(p[0])
      package_address = p[1]
      package_city = p[2]
      package_state = p[3]
      package_zip_code = p[4]
      package_deadline = p[5]
      package_weight = p[6]
      package_note = p[7]
      delivery_status = "At Hub"
      delivery_time = None

      package_information = [
        package_id_number, package_address, package_city, package_state,
        package_zip_code, package_deadline, package_weight, package_note,
        delivery_status, delivery_time
      ]

      hash_table.insert(package_id_number, package_information
                        )  # Use the hash_table instance to insert the package


def get_address_id(address_string):
  for row in address_list:
    if str(address_string) in row[2]:
      return int(row[0])


def get_address_str(package_id):
  for row in package_list:
    if str(package_id) in row[0]:
      return str(row[1])


def calculate_distance(location1, location2):
  found_distance = distance_list[int(location1)][int(location2)]
  if found_distance == '':
    found_distance = distance_list[int(location2)][int(location1)]

  return float(found_distance)


def check_package_status(package_id, time):
  package_info = hash_table.search(package_id)

  if package_info is None:
    return "Package not found in the system."

  delivery_status = package_info[8]
  delivery_time = package_info[9]

  if delivery_status == "Delivered":
    return "Package has been delivered."

  if delivery_time is None or time < delivery_time:
    return "Package is still in transit."

  return "Package has been delivered."


def show_package_delivery_time():
  package_id = int(input("Enter the Package ID: "))
  time = input("Enter the time in the format 'HH:MM:SS': ")
  time = datetime.datetime.strptime(time, "%H:%M:%S").time()

  package_info = hash_table.search(package_id)

  if package_info is not None:
    delivery_time = package_info[9]
    if delivery_time is not None:
      if time >= delivery_time:
        print("Package", package_id, "was delivered at:", delivery_time)
      else:
        print("Package", package_id, "is scheduled for delivery at:",
              delivery_time)
    else:
      print("Package", package_id, "has not been delivered yet.")
  else:
    print("Package", package_id, "not found in the system.")


def find_nearest_package(current_location, truck_packages):
  shortest_distance = 100
  location = current_location
  nearest_package_id = 0

  for package in truck_packages:
    distance = calculate_distance(location,
                                  get_address_id(get_address_str(package)))
    if distance < shortest_distance:
      shortest_distance = distance
      nearest_package_id = package

  return nearest_package_id


def sort_packages(start_location, truck_packages, truck_departure_time):
  sorted_packages = []
  available_packages = truck_packages.copy()
  current_location = start_location

  while len(available_packages) > 0:
    nearest_package = find_nearest_package(current_location,
                                           available_packages)
    sorted_packages.append(nearest_package)
    available_packages.remove(nearest_package)
    current_location = get_address_id(get_address_str(nearest_package))

    package_info = hash_table.search(
      nearest_package
    )  # Use the hash_table instance to search for package info
    package_info[-1] = truck_departure_time

  return sorted_packages


def calculate_total_distance(truck_list, truck_num):
  truck_distance = 0
  i = 0
  while i < len(truck_list) - 1:
    truck_distance += calculate_distance(
      get_address_id(get_address_str(truck_list[i])),
      get_address_id(get_address_str(truck_list[i + 1])))
    i += 1

  if truck_num == 1:
    truck_distance += calculate_distance(
      get_address_id(get_address_str(truck_list[len(truck_list) - 1])), 0)
  return truck_distance


truck1_packages = [2, 4, 11, 12, 17, 19, 22, 23, 31, 32, 33, 40]
truck2_packages = [5, 14, 15, 16, 18, 20, 21, 25, 26, 28, 34, 36, 37, 38]
truck3_packages = [1, 3, 6, 7, 8, 9, 10, 13, 24, 27, 29, 30, 35, 39]

truck1_leave_time = datetime.datetime.strptime("08:00:00", "%H:%M:%S").time()
truck2_leave_time = datetime.datetime.strptime("09:05:00", "%H:%M:%S").time()
truck3_leave_time = datetime.datetime.strptime("10:20:00", "%H:%M:%S").time()


class Main:
  load_package_info(package_file)

  sorted_truck1_packages = sort_packages(0, truck1_packages, truck1_leave_time)
  sorted_truck2_packages = sort_packages(0, truck2_packages, truck2_leave_time)
  sorted_truck3_packages = sort_packages(0, truck3_packages, truck3_leave_time)

  total_distance_truck1 = calculate_total_distance(sorted_truck1_packages, 1)
  total_distance_truck2 = calculate_total_distance(sorted_truck2_packages, 2)
  total_distance_truck3 = calculate_total_distance(sorted_truck3_packages, 3)

  print("WGUPS by Luke Tyrrell\n")
  print("Total Distance Traveled: " +
        str(total_distance_truck1 + total_distance_truck2 +
            total_distance_truck3))
  print("Truck 1: " + str(total_distance_truck1))
  print("Truck 2: " + str(total_distance_truck2))
  print("Truck 3: " + str(total_distance_truck3))
  user = input("Please Select an Option:\n"
               "1: Find Package Information at Specific Time\n"
               "2: Show Package Delivery Order\n")

  if user == "1":
    print("Available Package IDs:")
    for package_id in sorted_truck1_packages + sorted_truck2_packages + sorted_truck3_packages:
      print(package_id)
    user_package = str(input("Enter the Package ID: "))
    time = input("Enter the time in the format 'HH:MM:SS' ")
    time = datetime.datetime.strptime(time, "%H:%M:%S").time()
    status = check_package_status(user_package, time)
    print("Package", user_package, "status at", time, ":", status)

  if user == "2":
    print("Package Delivery Order:\n"
          "Truck 1: " + str(sorted_truck1_packages) + "\nTruck 2: " +
          str(sorted_truck2_packages) + "\nTruck 3: " +
          str(sorted_truck3_packages))
