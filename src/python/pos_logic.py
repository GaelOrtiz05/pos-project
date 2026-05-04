from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt

import pos_backend
from datetime import datetime, timedelta
class POSLogic:
    def __init__(self):
        self.logic = pos_backend.Login()
        self.data = pos_backend.Database()
        self.add_employee_feedback: "QLabel | None" = None
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
    def show_view_employees_screen(self) -> None: ...
    def update_cart(self) -> None: ...
    def disp_manage_inventory_menu(self) -> None: ...

    def login_event_handler(self, username, password, layout, confirm_password=None): # Authenticate login
        username = username.text()
        password = password.text()
        if confirm_password is not None:
            confirm = confirm_password.text()
        else:
            confirm = ""

        login_success = False
        error_message = 'Incorrect User or Password'

        users = self.logic.getListOfUsers()

        if len(users) == 0:
            if not username or not password:
                error_message = 'Username and password are required.'
            elif password != confirm:
                error_message = 'Passwords do not match.'
            else:
                self.logic.addUser(username, password, 2)
                login_success = True
        elif self.logic.loginUser(username, password) is True:
            login_success = True

        if login_success == True:
            self.initialize(username)
            if self.current_user.isAdmin:
                self.show_manager_menu()
            else:
                self.show_home_screen()
        else:
            if len(users) == 0:
                error_row = 8
            else:
                error_row = 6
            error_label = QLabel(error_message)
            error_label.setFixedSize(300,50)
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(error_label,error_row,0,1,2)
            error_label.setStyleSheet("background-color: black;font-size: 20px;border-radius: 10px; color: red;")

    def manager_event_handler(self):
        if self.current_user.isAdmin:
            self.show_manager_menu()
        # else:

    def submit_event_handler(self, username, password, checkbox):
        username_text = username.text().strip()
        password_text = password.text()
        is_admin = checkbox.isChecked()
        if is_admin:
            role = 1
        else:
            role = 0

        if not username_text or not password_text:
            self.show_add_employee_feedback("Username and password are required.", False)
            return

        if self.logic.addUser(username_text, password_text, role):
            self.users = self.logic.getListOfUsers()
            self.manager_feedback_message = f"Added user '{username_text}'."
            self.show_view_employees_screen()
            return

        self.show_add_employee_feedback(f"Username '{username_text}' is already taken.", False)

    def view_remove_employee_handler(self, name):
        self.logic.removeUser(name, self.current_user.role)
        self.show_view_employees_screen()

    def show_add_employee_feedback(self, message, success):
        if not self.add_employee_feedback:
            return

        color = "#0c401a" if success else "#7a1010"
        self.add_employee_feedback.setText(message)
        self.add_employee_feedback.setStyleSheet(
            f"color: white; font-size: 18px; background-color: white; ""border-radius: 10px; padding: 6px;")

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
    #item avalability:
    def item_available(self, item):
        ingredients = self.data.getItemIngredients(item.id)
        for ing in ingredients:
            if ing.stock <= 0:
                return False
        return True

    def confirm_item(self, item, label_list, id_list):
        return_list = []
        for idx, label in enumerate(label_list):
            quantity = int(label.text()[1:])
            for i in range(quantity):
                return_list.append(id_list[idx])
        print(return_list)
        self.Add_To_Checkout(item.id, return_list)
        self.show_home_screen()
        self.add_to_cart(item)

    def Add_To_Checkout(self, item, ingredient_list = []):
        self.data.Add_Item_Into_Checkout_Tables(item, ingredient_list)


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

        if text == "": #fail safe for empty input
            self.inventory_feedback.setText("Enter a stock amount.")
            self.inventory_feedback.show()
            return

        if not text.isdigit(): #fail safe for wrong input
            self.inventory_feedback.setText("Invalid input. Enter a whole number.")
            self.inventory_feedback.show()
            return

        amount = int(text)

        if increase and ingredient.stock + amount > 200: # max capacity
            self.inventory_feedback.setText("Inventory Cannot Exceed 200.")
            self.inventory_feedback.show()
            return

        if not increase and ingredient.stock - amount < 0:
            self.inventory_feedback.setText("Inventory Cannot Go Below 0.")
            self.inventory_feedback.show()
            return

        self.data.setIngredientStock(increase, ingredient.name, amount) #send to cpp db

        self.inventory_feedback.setText("Inventory Updated.")
        self.inventory_feedback.show()

        self.disp_manage_inventory_menu()
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
        text = ' \n'
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
                    text += f"Order #{order.id} \n Total: ${order.total:.2f} \n Date: {order_time.date()}\n" # all orders
                    items = self.data.getOrderItemsById(order.id)
                    for item in items:
                        text += f"   {item.itemName} x{item.count} - ${item.itemPrice:.2f}\n"
                    text += "\n"
                    total_sales += order.total
        order_info = [text,total_sales]
        return order_info

    def Add_To_Cart(self, item):
        print("test")

    #Closes the program.
    def close_program(self):
            QApplication.quit()  
        

