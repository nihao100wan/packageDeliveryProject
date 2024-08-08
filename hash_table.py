class HashTable:
    def __init__(self, size=20):
        # Initialize the hash table with empty buckets
        self.size = size
        self.table = [[] for _ in range(size)]

    def insert(self, key, value):
        # Insert a key-value pair into the hash table
        index = hash(key) % self.size
        for idx, (k, v) in enumerate(self.table[index]):
            if k == key:  # If key already exists, update the value
                self.table[index][idx] = (key, value)
                return
        self.table[index].append((key, value))  # Otherwise, add the new key-value pair

    def update(self, key, value):
        # Update the value for a given key
        index = hash(key) % self.size
        for idx, (k, v) in enumerate(self.table[index]):
            if k == key:  # If key exists, update the value
                self.table[index][idx] = (key, value)
                return
        self.insert(key, value)  # If key does not exist, insert it

    def search(self, key):
        # Find and return the value for a given key
        index = hash(key) % self.size
        for k, v in self.table[index]:
            if k == key:  # If key is found, return the value
                return v
        return None  # If key is not found, return None

    def lookup(self, key):
        # Look up the package details by the package ID
        package = self.search(key)  # Search for the package by key
        if package:  # If package is found, return its details
            return {
                'delivery address': package.address,
                'delivery deadline': package.deadline_time,
                'delivery city': package.city,
                'delivery zip code': package.zipcode,
                'package weight': package.weight,
                'delivery status': package.status,
                'delivery time': package.delivered_time
            }
        return None  # If package is not found, return None

    def print_table(self):
        # Print the entire hash table for debugging
        for i, bucket in enumerate(self.table):  # Iterate through each bucket
            print(f"Bucket {i}: {bucket}")  # Print the contents of the bucket
