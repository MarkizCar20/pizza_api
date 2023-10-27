#Definition of all models used in API
class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self, user, items):
        self.user = user
        self.items = items
        self.status = "Pending"

class User:
    def __init__(self, username, email, address):
        self.username = username
        self.email = email
        self.address = address

