# main.py

class User:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Phone: {self.phone}")


class Customer(User):
    def __init__(self, name, phone, address):
        super().__init__(name, phone)
        self.address = address
        self.orders = []

    def place_order(self, order):
        self.orders.append(order)
        print(f"\n{self.name} placed Order #{order.order_id}")


class FoodItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def display(self):
        print(f"{self.name} - ₹{self.price}")


class Restaurant:
    def __init__(self, name):
        self.name = name
        self.menu = []

    def add_food(self, food):
        self.menu.append(food)

    def show_menu(self):
        print(f"\n--- {self.name} Menu ---")
        for index, food in enumerate(self.menu, start=1):
            print(f"{index}. {food.name} - ₹{food.price}")


class Order:
    def __init__(self, order_id, customer, restaurant):
        self.order_id = order_id
        self.customer = customer
        self.restaurant = restaurant
        self.items = []
        self.status = "Pending"

    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        return sum(item.price for item in self.items)

    def update_status(self, status):
        self.status = status
        print(f"Order #{self.order_id} Status: {self.status}")

    def show_order(self):
        print(f"\nOrder #{self.order_id}")
        print(f"Customer: {self.customer.name}")
        print(f"Restaurant: {self.restaurant.name}")

        print("Items:")
        for item in self.items:
            print(f"- {item.name} (₹{item.price})")

        print(f"Total Bill: ₹{self.calculate_total()}")
        print(f"Current Status: {self.status}")


class DeliveryPartner(User):
    def __init__(self, name, phone):
        super().__init__(name, phone)

    def deliver_order(self, order):
        print(f"\n{self.name} accepted Order #{order.order_id}")

        order.update_status("Preparing")
        order.update_status("Out for Delivery")
        order.update_status("Delivered")


# -------------------------------
# DEMO
# -------------------------------

print("===== Welcome to Mini Zomato =====")

# Create Restaurant
restaurant = Restaurant("Pizza Hub")

# Add Food Items
pizza = FoodItem("Margherita Pizza", 250)
burger = FoodItem("Veg Burger", 150)
fries = FoodItem("French Fries", 100)

restaurant.add_food(pizza)
restaurant.add_food(burger)
restaurant.add_food(fries)

# Show Menu
restaurant.show_menu()

# Create Customer
customer = Customer(
    "Gokul",
    "9876543210",
    "Chennai"
)

# Create Order
order = Order(
    order_id=101,
    customer=customer,
    restaurant=restaurant
)

order.add_item(pizza)
order.add_item(fries)

customer.place_order(order)

# Show Order Details
order.show_order()

# Create Delivery Partner
partner = DeliveryPartner(
    "Ravi",
    "9999999999"
)

# Deliver Order
partner.deliver_order(order)

print("\n===== Order Completed Successfully =====")