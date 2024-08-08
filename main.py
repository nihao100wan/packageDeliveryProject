from datetime import datetime, timedelta
from truck import Truck
from utils import load_address_data, load_distance_data, load_package_data

# Define the start time for all trucks
START_TIME = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 8, 0, 0)

# Function to update the address of package 9
def update_package_address(package_9, package_5):
    # Update package 9's address details to match package 5's
    package_9.address = package_5.address
    package_9.city = package_5.city
    package_9.state = package_5.state
    package_9.zipcode = package_5.zipcode

# Function to print details of a package
def print_package_details(package, current_time):
    address_display = package.address
    city_display = package.city
    state_display = package.state
    zip_display = package.zipcode

    status = package.status if package.status else 'AT_HUB'
    delivered_time_display = package.delivered_time.strftime(
        "%Y-%m-%d %H:%M:%S") if package.delivered_time else "Not delivered"

    print(f"Package ID: {package.id}, Address: {address_display}, City: {city_display}, State: {state_display}, Zip: {zip_display}, "
          f"Weight: {package.weight}, Deadline: {package.deadline_time}, Status: {status}, Notes: {package.notes}, "
          f"Loaded Time: {package.loaded_time}, Delivered Time: {delivered_time_display}, Truck: {package.truck}")

# Function to print details of all packages
def print_all_packages(package_table, current_time):
    print("\nAll Packages:\n")
    for package_id in range(1, 41):  # Assuming package IDs are 1 through 40
        package = package_table.search(package_id)
        if package:
            print_package_details(package, current_time)

# Function to simulate delivery for a package based on a specified time
def simulate_delivery_for_package(package, address_list, distance_matrix, simulate_until):
    if package.truck:
        # Create a Truck object based on the package's assigned truck number
        truck = Truck(package.truck)

        # Determine the load time based on the truck number
        if truck.truck_number == 1:
            loaded_time = START_TIME
        elif truck.truck_number == 2:
            loaded_time = START_TIME + timedelta(hours=1, minutes=5)  # 9:05 AM
        elif truck.truck_number == 3:
            loaded_time = START_TIME + timedelta(hours=2, minutes=20)  # 10:20 AM
        else:
            print(f"Unknown truck number: {truck.truck_number}")
            return

        # Load the package onto the truck at the determined start time
        truck.load_package(package, loaded_time)

        # Simulate delivery for the package until the specified time
        truck.deliver_packages(address_list, distance_matrix, simulate_until=simulate_until)

def main():
    # Filepaths for the CSV files
    address_file = 'CSV/addressCSV.csv'
    distance_file = 'CSV/distanceCSV.csv'
    package_file = 'CSV/packageCSV.csv'

    # Load data from CSV files into respective data structures
    addressCSV = load_address_data(address_file)
    distance_matrix = load_distance_data(distance_file)
    package_table = load_package_data(package_file)

    current_time = datetime.now()
    cutoff_time = START_TIME + timedelta(hours=2, minutes=20)  # 10:20 AM cutoff time

    # Print all packages at the start of the program
    print_all_packages(package_table, current_time)

    # Initialize trucks with unique IDs
    trucks = [Truck(1), Truck(2), Truck(3)]

    # Load packages onto trucks with specific load times
    trucks[0].load_packages([1, 13, 5, 14, 15, 16, 19, 20, 29, 30, 31, 37, 40], package_table, START_TIME)
    trucks[1].load_packages([2, 3, 4, 7, 8, 18, 6, 25, 32, 34, 28, 36, 38], package_table, START_TIME + timedelta(hours=1, minutes=5))
    trucks[2].load_packages([9, 10, 11, 12, 17, 21, 35, 22, 23, 24, 26, 27, 33, 39], package_table, START_TIME + timedelta(hours=2, minutes=20))

    while True:
        print_menu()  # Display menu options
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            continue

        if choice == 1:
            # Update the address for package 9 if necessary
            package_5 = package_table.search(5)
            package_9 = package_table.search(9)

            if package_5 and package_9:
                if current_time >= cutoff_time:
                    update_package_address(package_9, package_5)

            total_mileage = 0.0
            for truck in trucks:
                try:
                    print(f"Delivering packages with Truck {truck.truck_number}...")
                    mileage = truck.deliver_packages(addressCSV, distance_matrix)
                    total_mileage += mileage
                    print(f"Truck {truck.truck_number} Return Time: {truck.current_time}")
                except Exception as e:
                    print(f"Error during delivery with Truck {truck.truck_number}: {e}")
            print(f"Total Mileage: {total_mileage:.2f} miles")
            print_all_packages(package_table, current_time)

        elif choice == 2 or choice == 3:
            try:
                if choice == 2:
                    package_id = int(input("Enter Package ID: "))
                    time_str = input("Enter Time (HH:MM): ")
                    package_ids = [package_id]
                elif choice == 3:
                    time_str = input("Enter Time (HH:MM): ")
                    package_ids = range(1, 41)

                time_obj = datetime.strptime(time_str, "%H:%M").replace(year=current_time.year, month=current_time.month, day=current_time.day)

                package_5 = package_table.search(5)
                if not package_5:
                    print("Package 5 not found.")
                    continue

                for package_id in package_ids:
                    package = package_table.search(package_id)
                    if package:
                        if package.id == 9 and time_obj >= cutoff_time:
                            update_package_address(package, package_5)
                        simulate_delivery_for_package(package, addressCSV, distance_matrix, simulate_until=time_obj)
                        print_package_details(package, time_obj)
                    else:
                        print(f"Package ID {package_id} not found.")
            except ValueError:
                print("Invalid input. Please enter a valid time in HH:MM format.")
                continue

        elif choice == 4:
            print("Thank you for choosing WGUPS. BYE!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

# Function to print the main menu options
def print_menu():
    print()
    print("Welcome to Western Governors University Parcel Service (WGUPS)")
    print("1. Deliver all packages and show total mileage")
    print("2. Check status of a specific package at a specific time")
    print("3. Check status of all packages at a specific time")
    print("4. Exit")

if __name__ == '__main__':
    main()
