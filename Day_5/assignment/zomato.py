


from typing import List


class User:
    def __init__(self,name,phone_number):
        self.name=name
        self.phone_number=phone_number

    def display_info(self):
        print(f"name: {self.name} PH_Number :{self.phone_number}")

class Customer(User):
    def __init__(self,name,phone_number,address):
        super().__init__(name,phone_number)
        self.address=address
        self.orders=[]

    def place_order(self,order):
        self.orders.append(order)
        print("your order have been placed successfully")


class FoodItem:
    def __init__(self,food_name,price):
        self.food_name=food_name
        self.price=price

    def display_food_details(self):
        print(f"{self.food_name} : Rs.{self.price}")
        

class Restaurant:
    def __init__(self,name):
        self.name=name
        self.menu:List[FoodItem]=[]

    def add_food(self,food:FoodItem):
        self.menu.append(food)

    def show_menu(self):
        for item in self.menu:
            item.display_food_details()

class Order:
    def __init__(self,order_id:str,customer:Customer,restaurant:Restaurant,order_items:List[FoodItem],status="Pending"):
        self.order_id=order_id
        self.customer=customer
        self.restaurant=restaurant
        self.order_items=order_items
        self.status=status

    def add_item(self,item:FoodItem):
        self.order_items.append(item)

    def calculate_total(self):
        total=0
        for item in self.order_items:
            total+=item.price
        return total

    def update_status(self,status):
        print("order status updated to "+status)
        self.status=status
    
    def show_order(self):
        print(f"Order id : {self.order_id}")
        print(f"Customer Name: {self.customer.name}")
        print(f"Restaurant Name: {self.restaurant.name}")
        for item in self.order_items:
            item.display_food_details()
        print(f"order status {self.status}")
        print(f"Bill Total :{self.calculate_total()} ")


class DeliveryPartner(User):
    def __init__(self, name, phone_number):
        super().__init__(name, phone_number)

    def deliver_order(self,order:Order):
        order.update_status("Preparing")
        order.update_status("Out for Delivery")
        order.update_status("Delivered")



# Demo

res=Restaurant("KFC")
food_item1=FoodItem("masala Dosa",150)
food_item2=FoodItem("Panner butter masala",100)
food_item3=FoodItem("Rasagula",70)


res.add_food(food_item1)
res.add_food(food_item2)
res.add_food(food_item3)

res.show_menu()

cust1=Customer("dr.vishu","9876543210","humanities")

order=Order("123",cust1,res,[food_item1,food_item2])



order.show_order()

del_p=DeliveryPartner("abc","1234")

del_p.deliver_order(order)

print("Take some rest!!!!!!")