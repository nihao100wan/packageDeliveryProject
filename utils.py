import csv
from hash_table import HashTable
from package import Package

def load_package_data(filepath):
    package_table = HashTable()
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row_number, row in enumerate(reader, start=1):
            if len(row) >= 7:
                try:
                    package_id = int(row[0])
                    address = row[1].strip()
                    city = row[2].strip()
                    state = row[3].strip()
                    zipcode = row[4].strip()
                    deadline_time = row[5].strip()
                    weight = float(row[6])
                    notes = row[7].strip() if len(row) > 7 else ""
                    package = Package(
                        id=package_id,
                        address=address,
                        city=city,
                        state=state,
                        zipcode=zipcode,
                        deadline_time=deadline_time,
                        weight=weight,
                        notes=notes
                    )
                    package_table.insert(package.id, package)
                except Exception as e:
                    print(f"Error inserting package {row_number} (ID: {row[0]}): {e}")
            else:
                print(f"Row {row_number} has insufficient data: {row}")
    return package_table

def load_address_data(filepath):
    address_list = []
    with open(filepath, newline='') as csvfile:
        address_reader = csv.reader(csvfile)
        for row_number, row in enumerate(address_reader, start=1):
            if len(row) >= 3:
                address_list.append({
                    'id': int(row[0].strip()),
                    'name': row[1].strip(),
                    'address': row[2].strip().lower(),
                    'city': row[3].strip() if len(row) > 3 else "",
                    'state': row[4].strip() if len(row) > 4 else "",
                    'zip': row[5].strip() if len(row) > 5 else ""
                })
            else:
                print(f"Row {row_number} has insufficient data: {row}")
    return address_list

def load_distance_data(filepath):
    distance_matrix = []
    with open(filepath, mode='r') as file:
        reader = csv.reader(file)
        for row_number, row in enumerate(reader, start=1):
            distances = [float(x) if x else None for x in row]
            distance_matrix.append(distances)

    num_rows = len(distance_matrix)
    for i in range(num_rows):
        for j in range(num_rows):
            if distance_matrix[i][j] is None and distance_matrix[j][i] is not None:
                distance_matrix[i][j] = distance_matrix[j][i]
            elif distance_matrix[i][j] is None:
                distance_matrix[i][j] = 0.0

    for i in range(num_rows):
        if len(distance_matrix[i]) != num_rows:
            raise ValueError(f"Row {i} in distance matrix does not match the expected number of columns.")
        for j in range(num_rows):
            if distance_matrix[i][j] != distance_matrix[j][i]:
                raise ValueError(f"Distance matrix is not symmetric at indices [{i}][{j}] and [{j}][{i}]")
    return distance_matrix

def find_address_index(address, address_list):
    normalized_address = address.strip().lower()
    for i, addr_dict in enumerate(address_list):
        if addr_dict['address'] == normalized_address:
            return i
    raise ValueError(f"Address '{address}' not found in address list.")

def distance_between(address1, address2, address_list, distance_matrix):
    try:
        index1 = find_address_index(address1, address_list)
        index2 = find_address_index(address2, address_list)
        return distance_matrix[index1][index2] if index1 < index2 else distance_matrix[index2][index1]
    except ValueError as e:
        print(f"Error: {e}")
        raise
