from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt

import pos_backend
from datetime import datetime, timedelta

class CheckoutGroup:
    def __init__(self,group_id,group_type,name,price):
        self.group_id = group_id
        self.group_type = group_type
        self.name = name
        self.price = price
        self.items = []

class CheckoutGroupItems:
    def __init__(self,item_id,name,price):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.modifiers = []

class CheckoutModifiers:
    def __init__(self,ingredient_id,name,change):
        self.ingredient_id = ingredient_id
        self.name = name
        self.change = change



class POSLogic:
    def __init__(self):
        self.logic = pos_backend.Login()
        self.data = pos_backend.Database()
        self.add_employee_feedback: "QLabel | None" = None
        self.inventory_feedback: "QLabel | None" = None
        self.current_user = None
        self.items = []
        self.combos = []
        
    def initialize(self, username):
        self.current_user = self.logic.getUser(username)
        self.items = self.data.getItems()
        self.combos = self.data.getCombos()
        self.cart = []
        self.checkout_group_counter = 0

    def show_home_screen(self) -> None: ...
    def show_manager_menu(self) -> None: ...
    def show_view_employees_screen(self) -> None: ...
    def update_cart(self) -> None: ...
    def display_manage_inventory_menu(self) -> None: ...

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
                self.show_home_screen()
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
            error_label.setStyleSheet("background-color: #2563eb ;font-size: 20px;border-radius: 10px; color: white;")

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
            f"color: white; font-size: 18px; background-color: {color}; "
            "border-radius: 10px; padding: 6px;"
        )


    #Cart methods
    

    def add_item_to_cart(self, item):
        group = CheckoutGroup(group_id=self.checkout_group_counter,
                              group_type="item",
                              name = item.name,
                              price=item.price)
        
        group.items.append(CheckoutGroupItems(item.item_id,item.name,item.price))

        self.cart.append(group)
        self.checkout_group_counter += 1
        self.update_cart()
    
    def add_combo_to_cart(self,combo):
        group = CheckoutGroup(group_id=self.checkout_group_counter,
                              group_type="combo",
                              name= combo.name,
                              price= combo.price)
        combo_items = self.data.getComboItems(combo.item_id)

        for comboItem in combo_items:
            group.items.append(CheckoutGroupItems(comboItem.id, comboItem.name,0.00))

        self.cart.append(group)
        self.checkout_group_counter += 1

        
        self.update_cart()

    def add_modifer(self,group_id, item_id,ingredient,change):
        group = next(group for group in self.cart if group.group_id == group_id)
        if not group: return
        item = next(item for item in group.items if item.item_id == item_id)
        if not item: return
        item.modifiers.append(CheckoutModifiers (ingredient.id,ingredient.name,change))


    def remove_group_from_checkout(self,group_id):
        self.cart = [group for group in self.cart if group.group_id != group_id]
        self.update_cart()

    def checkout(self):
        total = 0
        order_items = []
        receipt_text = ""
        for group in self.cart:
            for item in group.items:
                ingredients = self.data.getItemIngredients(item.item_id)
                for ingredient in ingredients:
                    self.data.setIngredientStock(False,ingredient.name,1)


        for group in self.cart:
            for item in group.items:
            
                order_item = pos_backend.OrderItem()
                order_item.itemId = item.item_id
                order_item.itemName = item.name

                order_item.count = 1
                order_items.append(order_item)
                total += item.price

                receipt_text += f"{item.name} x1 - ${total:.2f}\n"
        self.data.Process_Purchase(order_items,total)
        self.show_receipt_popup(receipt_text, total)
        
        self.cart = []
        self.update_cart()

        
    def update_ingredient_stock(self, ingredient, stock_input, increase=True): #works with disp_manage_inventory
        stock_input_text = stock_input.text().strip()

        if stock_input_text == "": #fail safe for empty input
            self.inventory_feedback.setText("Enter a stock amount.")
            self.inventory_feedback.show()
            return

        if not stock_input_text.isdigit(): #fail safe for wrong input
            self.inventory_feedback.setText("Invalid input. Enter a whole number.")
            self.inventory_feedback.show()
            return

        amount = int(stock_input_text)

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
        for group in self.cart:
            for item in group.items:
                total += item.price
        return total



    def get_sales(self,choice): #reading sales data (choice will determine if we read every sale, monthly or weekly.)
        total_sales = 0
        order_into_text = ' \n'
        list_of_orders = self.data.getOrders() # reading orders
        current_time = datetime.now() #getting current time from sys

        for order in list_of_orders:
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
                    order_into_text += f"Order #{order.id} \n Total: ${order.total:.2f} \n Date: {order_time.date()}\n" # all orders
                    list_of_orderitems = self.data.getOrderItemsById(order.id)
                    for item in list_of_orderitems:
                        order_into_text += f"   {item.itemName} x{item.count} - ${item.itemPrice:.2f}\n"
                    order_into_text += "\n"
                    total_sales += order.total

        list_of_order_info = [order_into_text,total_sales]
        return list_of_order_info
    #Closes the program.
    def close_program(self):
            QApplication.quit()  
        

