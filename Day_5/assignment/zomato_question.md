You can give your students a descriptive problem statement like this:

---

## Mini Zomato Application using OOP in Python

### Problem Statement

You have been hired to build a simplified version of a food delivery application similar to Zomato using **Object-Oriented Programming (OOP)** concepts in Python.

The application should allow customers to view restaurant menus, place food orders, and receive deliveries through delivery partners.

Your task is to design the system using classes and objects while demonstrating the following OOP concepts:

* Classes and Objects
* Inheritance
* Encapsulation
* Method Creation
* Object Relationships (Association)

---

### Requirements

#### 1. Create a Parent Class: `User`

* The class should store:

  * Name
  * Phone Number
* Add a method `display_info()` to display user details.

---

#### 2. Create a Child Class: `Customer`

* Inherit from the `User` class.
* Add:

  * Address
  * List of Orders
* Add a method `place_order(order)` that stores an order and prints a confirmation message.

---

#### 3. Create a Class: `FoodItem`

* Store:

  * Food Name
  * Price
* Add a method to display food details.

---

#### 4. Create a Class: `Restaurant`

* Store:

  * Restaurant Name
  * Menu (list of food items)
* Add methods:

  * `add_food(food)` → Adds a food item to the menu.
  * `show_menu()` → Displays all food items available.

---

#### 5. Create a Class: `Order`

* Store:

  * Order ID
  * Customer
  * Restaurant
  * List of Ordered Items
  * Order Status (default: `"Pending"`)
* Add methods:

  * `add_item(item)`
  * `calculate_total()`
  * `update_status(status)`
  * `show_order()`

---

#### 6. Create a Child Class: `DeliveryPartner`

* Inherit from the `User` class.
* Add a method:

  * `deliver_order(order)`

This method should update the order status through the following stages:

1. Preparing
2. Out for Delivery
3. Delivered

---

### Demonstration

Create objects and demonstrate the complete workflow:

1. Create a restaurant.
2. Add at least 3 food items to the menu.
3. Display the menu.
4. Create a customer.
5. Create an order.
6. Add multiple food items to the order.
7. Place the order.
8. Display order details and total bill.
9. Create a delivery partner.
10. Deliver the order by updating its status.
11. Print a success message after delivery.

---

### Sample Output

```text
===== Welcome to Mini Zomato =====

--- Pizza Hub Menu ---
1. Margherita Pizza - ₹250
2. Veg Burger - ₹150
3. French Fries - ₹100

Gokul placed Order #101

Order #101
Customer: Gokul
Restaurant: Pizza Hub

Items:
- Margherita Pizza (₹250)
- French Fries (₹100)

Total Bill: ₹350
Current Status: Pending

Ravi accepted Order #101

Order #101 Status: Preparing
Order #101 Status: Out for Delivery
Order #101 Status: Delivered

===== Order Completed Successfully =====
```

### Bonus Challenge

* Add a `Payment` class.
* Allow multiple restaurants.
* Allow customers to place multiple orders.
* Add a rating system for restaurants.
* Generate unique order IDs automatically.

This exercise will help you practice **Inheritance, Composition, Object Interaction, and Real-World OOP Design** in Python.
