class Package:
    def __init__(self, id, address, city, state, zipcode, deadline_time, weight, notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.notes = notes
        self.status = 'AT_HUB'
        self.loaded_time = None
        self.delivered_time = None
        self.truck = None

    def __str__(self):
        return (
            f"Package ID: {self.id}, Address: {self.address}, City: {self.city}, State: {self.state}, Zip: {self.zipcode}, "
            f"Deadline: {self.deadline_time}, Weight: {self.weight},  Status: {self.status}, "
            f"Loaded: {self.loaded_time}, Delivered: {self.delivered_time}, Truck: {self.truck}")