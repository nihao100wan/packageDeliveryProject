from datetime import datetime, timedelta
from utils import distance_between

# Constants
TRUCK_SPEED = 18 / 60  # Speed in miles per minute
START_TIME = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 8, 0, 0)  # Start time for the trucks

class Truck:
    def __init__(self, truck_number):
        self.truck_number = truck_number
        self.packages = []
        self.current_location = '4001 South 700 East'
        self.delivery_log = []
        self.current_time = None

    def load_package(self, package, load_time):
        package.truck = self.truck_number
        package.status = 'EN_ROUTE'
        package.loaded_time = load_time
        self.packages.append(package)

    def load_packages(self, package_ids, package_table, load_time):
        self.current_time = load_time
        for package_id in package_ids:
            package = package_table.search(package_id)
            if package:
                package.truck = self.truck_number
                package.status = 'EN_ROUTE'
                package.loaded_time = load_time
                self.packages.append(package)

    def deliver_packages(self, address_list, distance_matrix, simulate_until=None):
        total_distance = 0.0
        # Set specific start times for each truck
        if self.truck_number == 1:
            self.current_time = START_TIME
        elif self.truck_number == 2:
            self.current_time = START_TIME + timedelta(hours=1, minutes=5)  # 9:05 AM
        elif self.truck_number == 3:
            self.current_time = START_TIME + timedelta(hours=2, minutes=20)  # 10:20 AM

        while self.packages:
            next_package = self._find_closest_package(address_list, distance_matrix)
            distance_to_next = distance_between(self.current_location, next_package.address, address_list,
                                                distance_matrix)
            travel_time = timedelta(minutes=(distance_to_next / TRUCK_SPEED))

            if simulate_until and self.current_time + travel_time > simulate_until:
                break

            self.current_location = next_package.address
            self.current_time += travel_time

            if not simulate_until or self.current_time <= simulate_until:
                next_package.status = 'DELIVERED'
                next_package.delivered_time = self.current_time

            self.delivery_log.append(next_package)
            self.packages.remove(next_package)

            total_distance += distance_to_next

        if not simulate_until:
            distance_to_hub = distance_between(self.current_location, '4001 South 700 East', address_list, distance_matrix)
            return_travel_time = timedelta(minutes=(distance_to_hub / TRUCK_SPEED))

            self.current_location = '4001 South 700 East'
            self.current_time += return_travel_time
            total_distance += distance_to_hub

            print(f"Truck {self.truck_number} returned to hub at {self.current_time}, total distance: {total_distance:.2f} miles")
        return total_distance

    def _find_closest_package(self, address_list, distance_matrix):
        closest_package = None
        closest_distance = float('inf')
        for package in self.packages:
            distance = distance_between(self.current_location, package.address, address_list, distance_matrix)
            if distance < closest_distance:
                closest_distance = distance
                closest_package = package
        return closest_package
