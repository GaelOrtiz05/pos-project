from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt

import pos_backend
from datetime import datetime, timedelta
class POSLogic:
    def __init__(self):
        self.logic = pos_backend.Login()
        self.data = pos_backend.Database()
        self.add_employee_feedback: "QLabel | None" = None
        self.remove_employee_feedback: "QLabel | None" = None
        self.inventory_feedback: "QLabel | None" = None
        self.current_user = None
        self.items = []
        self.combos = []
        self.cart = []

    def initialize(self, username):
        self.current_user = self.logic.getUser(username)
        self.items = self.data.getItems()
        self.combos = self.data.getCombos()
        self.cart = []

    def show_home_screen(self) -> None: ...
    def show_manager_menu(self) -> None: ...
    def update_cart(self) -> None: ...
    def disp_manage_inventory_menu(self) -> None: ...

    def login_event_handler(self, username, password,layout): # Authenticate login
        username = username.text()
        password = password.text()

        login_success = False

        users = self.logic.getListOfUsers()

        if len(users) == 0:
            self.logic.addUser(username, password, True)
            login_success = True
        elif self.logic.loginUser(username, password) is True:
            login_success = True

        if login_success == True:
            self.initialize(username)
            self.show_home_screen()
        else:
            error_label = QLabel('Incorrect User or Password')
            error_label.setFixedSize(300,50)
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(error_label,5,0,1,2)
            error_label.setStyleSheet("background-color: black;font-size: 20px;border-radius: 10px; color: red;")

    def manager_event_handler(self):
        if self.current_user.isAdmin:
            self.show_manager_menu()
        # else:

    def submit_event_handler(self, username, password, checkbox):
        username_text = username.text().strip()
        password_text = password.text()
        is_admin = checkbox.isChecked()

        if not username_text or not password_text:
            self.show_add_employee_feedback("Username and password are required.", False)
            return

        if self.logic.addUser(username_text, password_text, is_admin):
            self.users = self.logic.getListOfUsers()
            self.manager_feedback_message = f"Added user '{username_text}'."
            self.show_manager_menu()
            return

        self.show_add_employee_feedback(f"Username '{username_text}' is already taken.", False)

    def remove_employee_handler(self,username):
        username = username.text().strip()
        if not username:
            self.remove_employee_feedback.setText("Enter a username.")
            return

        success = self.logic.removeUser(username)
        if success:
            self.remove_employee_feedback.setText("User removed successfully.")
        else:
            self.remove_employee_feedback.setText("User not found.")

    def show_add_employee_feedback(self, message, success):
        if not self.add_employee_feedback:
            return

        color = "#0c401a" if success else "#7a1010"
        self.add_employee_feedback.setText(message)
        self.add_employee_feedback.setStyleSheet(
            f"color: white; font-size: 18px; background-color: {color}; "
            "border-radius: 10px; padding: 6px;"
        )

 #Adds an item to the checkout table based on item id.
    def add_to_cart(self, item):
        if self.data.decrementStock(item.id) == False:
            print(f"'{item.name}' cannot be added: out of stock.")
            return

        for i in self.cart:
            if i["id"] == item.id and not i["isCombo"]:
                i["count"] += 1
                print(f"item count: {i['count']}")
                self.update_cart()
                return

        self.cart.append({"id": item.id,
                          "name": item.name,
                          "price": item.price,
                          "count": 1, # amount in cart 
                          "isCombo": 0
                          })

        self.update_cart()

    #Clears the current cart display.
    def remove_cart_item(self, index):
        if index < 0 or index >= len(self.cart):
            return
        self.data.incrementStock(self.cart[index]["id"])
        if self.cart[index]["count"] > 1:
            self.cart[index]["count"] -= 1
        else:
            self.cart.pop(index)
        self.update_cart()

    def checkout(self):
        order_items = []
        total = 0.0
        for i in self.cart:
                oi = pos_backend.OrderItem()
                oi.itemId = i["id"]
                oi.itemName = i["name"]
                oi.itemPrice = i["price"]
                oi.count = i['count']
                print(f"item count: {i['count']}")
                order_items.append(oi)
                total += i["price"] * i["count"]
        self.data.purchase(order_items, total)
        self.cart = []
        self.update_cart()

    def confirm_item(self, item):
        self.show_home_screen()
        self.add_to_cart(item)

    def confirm_combo(self, combo):
        combo_items = self.data.getComboItems(combo.id)

        for ci in combo_items:
            for ing in self.data.getItemIngredients(ci.id):
                if ing.stock < 1:
                    print(f"'{combo.name}' cannot be added: '{ing.name}' is out of stock.")
                    return

        for ci in combo_items:
            self.data.decrementStock(ci.id)

        for i in self.cart:
            if i["id"] == combo.id and i["isCombo"]:
                i["count"] += 1
                self.show_home_screen()
                return

        subtitle = ", ".join(ci.name for ci in combo_items)
        self.cart.append({"id": combo.id,
                          "name": combo.name,
                          "subtitle": subtitle,
                          "price": combo.price,
                          "count": 1,
                          "isCombo": True})
        self.show_home_screen()

    def update_ingredient_stock(self, ingredient, stock_input, increase=True): #works with disp_manage_inventory
        text = stock_input.text().strip()

        if not text or not text.isdigit(): #fail safe for wrong input
            return  
        if int(text) > 200: # max capacity
            self.inventory_feedback.setText("Inventory Cannot Exceed 200.")
            self.inventory_feedback.show()
            return
        
        self.data.setIngredientStock(increase, ingredient.name, int(text)) #send to cpp db
        self.disp_manage_inventory_menu()
        self.inventory_feedback.hide()

    def calculate_cart_total(self):
        total = 0.0
        for item in self.cart:
            total += item["price"] * item["count"]
        return total

    def get_cart_display_text(self, item):
        item_count = item["count"]

        if item["isCombo"] and "subtitle" in item:
            return f"{item['name']} - ${item['price']:.2f} - x{item_count}\n{item['subtitle']}"
        else:
            return f"{item['name']} - ${item['price']:.2f} - x{item_count}"
        
    def get_sales(self,choice): #reading sales data (choice will determine if we read every sale, monthly or weekly.)
        total_sales = 0
        text = 'lol \n'
        orders = self.data.getOrders() # reading orders
        current_time = datetime.now() #getting current time from sys

        for order in orders:
                order_time = datetime.fromisoformat(order.time)  #checking & getting orders time
                include = False
                if choice == 1:  # today
                    include = (order_time.date() == current_time.date())
                elif choice == 2:  # this weeks
                    start_of_week = current_time - timedelta(days=current_time.weekday()) #compare getting orders in the range  
                    include = (order_time >= start_of_week)
                elif choice == 3:  # All orders
                    include = True
                if include:
                    text += f"Order #{order.id} - Total: ${order.total:.2f}\n" # all orders
                    items = self.data.getOrderItemsById(order.id)
                    for item in items:
                        text += f"   {item.itemName} x{item.count} - ${item.itemPrice:.2f}\n"
                    text += "\n"
                    total_sales += order.total
        order_info = [text,total_sales]
        return order_info


    #Closes the program.
    def close_program(self):
            QApplication.quit()  
        

