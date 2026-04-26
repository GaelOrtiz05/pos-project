#access files
import os
#access environment
import sys
import platform

#Easier access to GUI elements
from PySide6.QtWidgets import (
    QMainWindow,
    QGridLayout,
    QApplication,
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QCheckBox,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    
)

#shortcuts, inputs, etc.
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence,QKeySequence,QGuiApplication, QFont, QColor

from pos_logic import POSLogic

class MainWindow(QMainWindow, POSLogic):

    def __init__(self):
        QMainWindow.__init__(self)
        POSLogic.__init__(self)
        self.manager_feedback_message = ""
        screen = QGuiApplication.primaryScreen()
        size = screen.availableGeometry()
        window_length = size.width()
        window_height = size.height()
        self.setWindowTitle("POS")
        
        if platform.system() == "Windows":
            self.setFixedSize(window_length, window_height)
        else:
            self.resize(window_length, window_height)
        
        self.show_login_screen()
        self.shortcut_close = QShortcut(QKeySequence.StandardKey.Close, self)
        self.shortcut_close.activated.connect(self.close)

    def clear_enter_shortcuts(self):
        if hasattr(self, '_enter_shortcuts'):
            for shortcut in self._enter_shortcuts:
                shortcut.deleteLater()
        self._enter_shortcuts = []

    def bind_enter_key(self, handler):
        self.clear_enter_shortcuts()
        for key in [Qt.Key_Return, Qt.Key_Enter]:
            enter_shortcut = QShortcut(QKeySequence(key), self)
            enter_shortcut.activated.connect(handler)
            self._enter_shortcuts.append(enter_shortcut)

    def show_login_screen(self): # Login Screen
            # creating a container
            central = QWidget()
            # put the container in the main window
            self.setCentralWidget(central)
            central.setStyleSheet("background-color: black;") # Chaning the background color
            # creating a grid layour inside the container
            layout = QGridLayout(central)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter) # PUTTING EVERYTHING IN THE MIDDLE/CENTER
            # now making a label
            pos_label = self.create_label('Point of Sale System','black',300,50)
            pos_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            user_label = self.create_label("Username",'black',150,50)
            pass_label = self.create_label("Password",'black',150,50)
        
            layout.addWidget(pos_label,0,0,2,2)
            layout.addWidget(user_label,2,0)
            layout.addWidget(pass_label,3,0)

            # QLineEdit() = Text Input
            user_input = QLineEdit()
            user_input.setMaximumSize(150,50)
            layout.addWidget(user_input,2,1)
            user_input.setStyleSheet("background-color: white ; border-radius: 5px; font-size: 25px;color: black")

            password_input = QLineEdit()
            password_input.setMaximumSize(150,50)
            password_input.setEchoMode(QLineEdit.EchoMode.Password) # ***
            layout.addWidget(password_input,3,1)
            password_input.setStyleSheet("background-color: white ; border-radius: 5px; font-size: 25px; color:black")


            # QPushButton() = Button
            login_button = self.create_button('Login','green',300,50)
            layout.addWidget(login_button,4,0,1,2)
            quit_button = self.create_button('Quit','red',300,50)
            layout.addWidget(quit_button,6,0,1,2)

            login_button.clicked.connect(lambda: self.login_event_handler(user_input, password_input, layout))
            quit_button.clicked.connect(lambda: self.close_program())        

            self.bind_enter_key(lambda: self.login_event_handler(user_input, password_input, layout))

    def show_home_screen(self):  # Main UI

        home_widget = QWidget()
        self.setCentralWidget(home_widget)
        home_widget.setStyleSheet("background-color: black;")

        main_layout = QVBoxLayout(home_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Row for the categories
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        all_items = self.create_button('All', '#1e1530', 150, 50)
        all_items.clicked.connect(lambda: self.load_grid(0))

        entre_button = self.create_button('Entre', '#1e1530', 150, 50)
        entre_button.clicked.connect(lambda: self.load_grid(1))

        sides_button = self.create_button('Sides', '#1e1530', 150, 50)
        sides_button.clicked.connect(lambda: self.load_grid(2))

        dessert_button = self.create_button('Dessert', '#1e1530', 150, 50)
        dessert_button.clicked.connect(lambda: self.load_grid(3))

        drink_button = self.create_button('Drinks', '#1e1530', 150, 50)
        drink_button.clicked.connect(lambda: self.load_grid(4))
        
        if self.current_user.isAdmin:
            manager_button = self.create_button('Manager', '#1e1530', 150, 50)
        
        logout_button = self.create_button('Logout', '#540612', 150, 50)

        for button in [all_items, entre_button, sides_button, dessert_button, drink_button] + ([manager_button] if self.current_user.isAdmin else []) + [logout_button]:
            top_row.addWidget(button)
        top_row.setAlignment(Qt.AlignmentFlag.AlignCenter) # centering the buttons
        # Disp username
        user_label = self.create_label(f"Logged in as: {self.current_user.name}",'#1e1530',500,50)
        top_row.addWidget(user_label)

        main_layout.addLayout(top_row)
        combo_row = QHBoxLayout()
        combo_row.setSpacing(30)
        #displaying the categories
        
        #Displays Combo Buttons
        
        combos = self.data.getCombos()
        for combo in combos:
            btn = self.create_button(f"{combo.name}", '#1e1530', 400, 80)
            btn.clicked.connect(lambda _, c=combo: self.confirm_combo(c))
            combo_row.addWidget(btn)

        combo_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(combo_row)
        #------------------------------------------------------------------------------------------
        # Scroll Box - main combo items will be here 
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: black; border: none;")
        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setSpacing(10)
        
        #load grid with all items
        self.load_grid(0)

        scroll.setWidget(container)
        #main_layout.addWidget(scroll)
        
        # Bottom section (items + cart)
        #-----------------------------------------------------------------------------------------    
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        # LEFT SIDE (scroll box)
        bottom_row.addWidget(scroll, 3)  

        # RIGHT SIDE (cart panel)
        cart_widget = QWidget()
        self.cart_layout = QVBoxLayout(cart_widget)
        self.cart_layout.setContentsMargins(12, 12, 12, 12)
        self.cart_layout.setSpacing(12)
        cart_widget.setFixedWidth(420)
        cart_widget.setStyleSheet("background-color: #1e1530; border-radius: 14px;")

        # cart title
        cart_title = QLabel("Cart")
        cart_title.setFixedHeight(50)
        cart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cart_title.setFont(self.create_font(20, 600))
        cart_title.setStyleSheet("background-color: #1e1530; border: 1px solid #374151; color: white; border-radius: 12px;")
        self.cart_layout.addWidget(cart_title)

        # scroll wheel to handle more items
        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setStyleSheet(("QScrollArea { background-color: transparent; border: none; } QScrollBar:vertical { width: 8px; background: transparent; } QScrollBar::handle:vertical { background: #374151; border-radius: 4px; }"))
        self.cart_container = QWidget()
        self.cart_items_layout = QVBoxLayout(self.cart_container)
        self.cart_items_layout.setContentsMargins(10, 10, 10, 10)
        self.cart_items_layout.setSpacing(8)
        self.cart_items_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.cart_item_row_height = 52
        self.cart_visible_rows = 4
        visible_rows_height = (
            (self.cart_item_row_height * self.cart_visible_rows)
            + (self.cart_items_layout.spacing() * (self.cart_visible_rows - 1))
            + 20
        )
        self.cart_scroll.setFixedHeight(visible_rows_height)
        self.cart_scroll.setWidget(self.cart_container)
        self.cart_layout.addWidget(self.cart_scroll, 1)

        # footer with persistent total + checkout action
        footer_widget = QWidget()
        footer_layout = QVBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(10)

        self.total_label = QLabel("Total: $0.00")
        self.total_label.setFixedHeight(58)
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_label.setFont(self.create_font(24, 600))
        self.total_label.setStyleSheet("background-color: #16a34a; color: white; border: 2px solid #16a34a; border-radius: 14px;")


        checkout_button = self.create_button("Checkout", '#16a34a', 320, 90)
        checkout_button.clicked.connect(self.checkout)

        footer_layout.addWidget(self.total_label)
        footer_layout.addWidget(checkout_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.cart_layout.addWidget(footer_widget)
        bottom_row.addWidget(cart_widget, 1)  # smaller than scroll

        # add the scroll and cart to main layout
        main_layout.addLayout(bottom_row)

        #Logout button functionality 
        logout_button.clicked.connect(self.show_login_screen)
        if self.current_user.isAdmin:
            manager_button.clicked.connect(lambda: self.manager_event_handler())

        self.update_cart() # to update cart each time we go back to home screen, so it doesn't show old items after purchase

    # manager functions
    def show_manager_menu(self): # Admins

        manager_ui = QWidget()
        self.setCentralWidget(manager_ui)
        manager_ui.setStyleSheet("background-color: black;")
        layout = QGridLayout(manager_ui)
        # Add employee Button
        create_new_account_button = self.create_button('Add Employee','gray',300,50)
        layout.addWidget(create_new_account_button,0,0) # Where it is row 3, col 0, takes 1 row and 2 columns
        create_new_account_button.clicked.connect(self.show_add_employee_screen)
        # View employees button
        view_employees_button = self.create_button('View Employees','gray',300,50)
        layout.addWidget(view_employees_button,1,0)
        view_employees_button.clicked.connect(self.show_view_employees_screen)
        # REmoive employee button
        remove_employee_button = self.create_button('Remove Employee','gray',300,50)
        layout.addWidget(remove_employee_button,2,0)
        remove_employee_button.clicked.connect(self.show_remove_employee_screen)
        # View sales button
        view_sales_button = self.create_button('View Sales','gray',300,50)
        layout.addWidget(view_sales_button,3,0) 
        view_sales_button.clicked.connect(self.disp_sales_menu)
        # Manager inventory button
        manage_inventory_button = self.create_button('Manage Inventory','gray',300,50)
        manage_inventory_button.clicked.connect(self.disp_manage_inventory_menu)

        layout.addWidget(manage_inventory_button,4,0)
        if self.manager_feedback_message:
            feedback_label = QLabel(self.manager_feedback_message)
            feedback_label.setFixedSize(360, 45)
            feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            feedback_label.setStyleSheet(
                "color: white; font-size: 18px; background-color: #0c401a; "
                "border-radius: 10px; padding: 6px;"
            )
            layout.addWidget(feedback_label, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            self.manager_feedback_message = ""
        # Back Button
        back_button = self.create_button('Return','red',300,50)
        layout.addWidget(back_button,6,0)
        back_button.clicked.connect(self.show_home_screen)

    def show_remove_employee_screen(self):  # Remove employee
        remove_ui = QWidget()
        self.setCentralWidget(remove_ui)
        remove_ui.setStyleSheet("background-color: black;")

        self.remove_employee_feedback = None

        layout = QGridLayout(remove_ui)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(18)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = self.create_label("Remove Employee", "", 400, 50)
        title.setFont(self.create_font(25))

        # Username
        user_label = self.create_label("Username:", "", 140, 40)
        user_input = QLineEdit()
        user_input.setFixedSize(260, 40)
        user_input.setStyleSheet("font-size: 18px; border-radius: 15px; background-color: white; color: black; padding-left: 12px;")

        # Submit button
        submit_button = self.create_button("Remove User", "green", 300, 50)
        submit_button.clicked.connect(lambda: self.remove_employee_handler(user_input))
        # Back button
        back_button = self.create_button("Back", "red", 300, 50)
        back_button.clicked.connect(self.show_manager_menu)
        # Feedback label
        self.remove_employee_feedback = QLabel("")
        self.remove_employee_feedback.setFixedSize(360, 45)
        self.remove_employee_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.remove_employee_feedback.setWordWrap(True)
        self.remove_employee_feedback.setStyleSheet("color: white; font-size: 18px; background-color: transparent;")

        # Layout
        layout.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(user_label, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(user_input, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(submit_button, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.remove_employee_feedback, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(back_button, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

    def show_view_employees_screen(self):
        employees_ui = QWidget()
        self.setCentralWidget(employees_ui)
        employees_ui.setStyleSheet("background-color: black;")

        main_layout = QVBoxLayout(employees_ui)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = self.create_label("Employees","",400,50)
        title.setFont(self.create_font(25))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: black; border: none;")

        container = QWidget()
        list_layout = QVBoxLayout(container)
        list_layout.setSpacing(10)

        self.users = self.logic.getListOfUsers()
        for user in self.users:
            role = "Admin" if user.isAdmin else "Employee"
            user_label = self.create_label(f"{user.name} ({role})", '#2e302f', 500, 50)
            list_layout.addWidget(user_label, alignment=Qt.AlignmentFlag.AlignCenter)

        list_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        back_button = self.create_button('Back','red',300,50)
        back_button.clicked.connect(self.show_manager_menu)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def show_add_employee_screen(self):  # Add employee
        add_ui = QWidget()
        self.setCentralWidget(add_ui)
        add_ui.setStyleSheet("background-color: black;")

        layout = QGridLayout(add_ui)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(18)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = self.create_label("Add Employee", "", 400, 50)
        title.setFont(self.create_font(25))

        # Username
        user_label = self.create_label("Username:", "", 140, 40)
        user_input = QLineEdit()
        user_input.setFixedSize(260, 40)
        user_input.setStyleSheet("font-size: 18px; border-radius: 15px; background-color: white; color: black; padding-left: 12px;")

        # Password
        pass_label = self.create_label("Password:", "", 140, 40)
        pass_input = QLineEdit()
        pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        pass_input.setFixedSize(260, 40)
        pass_input.setStyleSheet("font-size: 18px; border-radius: 15px; background-color: white; color: black; padding-left: 12px;")

        # Checkbox
        checkbox = QCheckBox("Admin")
        checkbox.setStyleSheet("color: white; font-size: 18px;")
        
        # Buttons
        submit_button = self.create_button('Add User', 'green', 300, 50)
        submit_button.clicked.connect(lambda: self.submit_event_handler(user_input, pass_input, checkbox))

        self.bind_enter_key(lambda: self.submit_event_handler(user_input, pass_input, checkbox))

        back_button = self.create_button('Back', 'red', 300, 50)
        back_button.clicked.connect(self.show_manager_menu)

        # Feedback
        self.add_employee_feedback = QLabel("")
        self.add_employee_feedback.setFixedSize(360, 45)
        self.add_employee_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_employee_feedback.setWordWrap(True)
        self.add_employee_feedback.setStyleSheet("color: white; font-size: 18px; background-color: transparent;")

        # Layout
        layout.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(user_label, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(user_input, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(pass_label, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(pass_input, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(checkbox, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(submit_button, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.add_employee_feedback, 5, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(back_button, 6, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

    #Loads main grid with items from the items table based on category_id
    #Category 0 = all, 1 = entre, 2 = sides, 3 = dessert, 4 = drinks
    def load_grid(self,category = 0):                
        for item in reversed(range(self.grid.count())):
            widget = self.grid.takeAt(item).widget()
            if widget:
                widget.deleteLater()
        
        list_buttons = []
        
        self.items = self.data.getItems()

        # print (f"{range(self.data.getItemCount())} is the range")
        # print(f"category is {category}")

        for idx, item in enumerate(self.items):
            btn = self.create_button((f"{item.name}"),'#1e1530',300,150)
            list_buttons.append(btn)
            list_buttons[idx].clicked.connect(lambda _, x=item: self.disp_ingredients_menu(x))
        row = 0
        col = 0
        for idx, item in enumerate(self.items):
            if (item.categoryId == category or category == 0):
                if (col < 4):
                    self.grid.addWidget(list_buttons[idx], row, col)
                    # print(f"added {item.name} to grid. index is {idx}")
                    col += 1
                else:
                    col = 0
                    row += 1
                    self.grid.addWidget(list_buttons[idx], row, col)
                    # print(f"added {item.name} to grid. index is {idx}")
                    col += 1
 

    def clear_cart(self): 
        for i in reversed(range(self.cart_items_layout.count())):
            widget = self.cart_items_layout.takeAt(i).widget()
            if widget:
                widget.deleteLater()
     
    #adds item to the cart display.
    def update_cart(self):
        self.clear_cart()

        for index, i in enumerate(self.cart):
            display = self.get_cart_display_text(i)
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(8)
            label = QLabel(display)
            label.setFixedHeight(self.cart_item_row_height)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.setFont(self.create_font(18))
            label.setStyleSheet("background-color: #1e1530; color: white; border: 1px solid #374151; border-radius: 12px; padding: 8px;")

            remove_button = self.create_button("x", "red", 40, 40)
            remove_button.clicked.connect(lambda _, x=index: self.remove_cart_item(x))

            row_layout.addWidget(label, 1)
            row_layout.addWidget(remove_button)

            self.cart_items_layout.addWidget(row_widget)

        if len(self.cart) == 0:
            empty_label = QLabel("No items in cart")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setFont(self.create_font(16))
            empty_label.setStyleSheet("background-color: transparent; color: #a0a0a0;")
            self.cart_items_layout.addStretch()
            self.cart_items_layout.addWidget(empty_label)
            self.cart_items_layout.addStretch()

        total = self.calculate_cart_total()
        self.total_label.setText(f"Total: ${total:.2f}")
    def disp_sales_menu(self):
        sales_ui = QWidget()
        self.setCentralWidget(sales_ui)
        sales_ui.setStyleSheet("background-color: black;")
        layout = QGridLayout(sales_ui)
        # Add employee Button
        todays_sales = self.create_button('Sale Today','gray',300,50)
        todays_sales.clicked.connect(lambda: self.disp_sales(1))
        layout.addWidget(todays_sales,0,0)
        weekly_sales = self.create_button('Sale This Week','gray',300,50)
        weekly_sales.clicked.connect(lambda: self.disp_sales(2))
        layout.addWidget(weekly_sales,0,1)
        all_sales = self.create_button('All Sales','gray',300,50)
        all_sales.clicked.connect(lambda: self.disp_sales(3))
        layout.addWidget(all_sales,0,2)

        back_button = self.create_button('Back','red',300,50)
        back_button.clicked.connect(self.show_manager_menu)
        layout.addWidget(back_button,0,3)

    def disp_sales(self,choice): # choice will be 1 2 or 3
        sales_ui = QWidget()
        self.setCentralWidget(sales_ui)
        sales_ui.setStyleSheet("background-color: black;")
        layout = QGridLayout(sales_ui)
        sales_info = self.get_sales(choice)
        sales_text = sales_info[0]
        total = sales_info[1]
        sales_label = QLabel(sales_text)
        sales_label.setStyleSheet("color: white; font-size: 18px;")

        layout.addWidget(sales_label)
        total_sales_label = self.create_label(f'Total Sale $:{total:.2f} ','black',400,150)
        layout.addWidget(total_sales_label)
        back_button = self.create_button('Back','red',300,50)
        back_button.clicked.connect(self.disp_sales_menu)
        layout.addWidget(back_button,0,3)

    def disp_ingredients_menu(self, item):
        ingredients_ui = QWidget()
        self.setCentralWidget(ingredients_ui)
        ingredients_ui.setStyleSheet("background-color: black;")

        # Outer layout fills the window, but centers a smaller card
        outer_layout = QVBoxLayout(ingredients_ui)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addStretch()

        card = QWidget()
        card.setFixedSize(650, 260)  # make this smaller/larger as needed
        card.setStyleSheet("background-color: #1f1f1f; border-radius: 14px;")
        card_layout = QGridLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setHorizontalSpacing(16)
        card_layout.setVerticalSpacing(16)

        title = self.create_label(f"Customize {item.name}", "", 360, 44)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(self.create_font(20, 600))
        card_layout.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        confirm_button = self.create_button("Confirm", "green", 220, 48)
        confirm_button.clicked.connect(lambda: self.confirm_item(item))
        card_layout.addWidget(confirm_button, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        back_button = self.create_button("Back", "red", 220, 48)
        back_button.clicked.connect(self.show_home_screen)
        card_layout.addWidget(back_button, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        outer_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout.addStretch()

    def disp_manage_inventory_menu(self):
        manage_inventory_ui = QWidget()
        self.setCentralWidget(manage_inventory_ui)
        manage_inventory_ui.setStyleSheet("background-color: black;")

        main_layout = QVBoxLayout(manage_inventory_ui)

        title = self.create_label("manage inventory", "", 450, 50)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(self.create_font(25, 600))
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        #scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: black; border: none;")

        container = QWidget()
        list_layout = QVBoxLayout(container)
        list_layout.setSpacing(12)

        inventory_items = self.data.getIngredients() #reading from cpp

        for ingredient in inventory_items: #going through the list
            row_widget = QWidget()
            row_widget.setStyleSheet("background-color: #1f1f1f; border-radius: 14px;")
            row_layout = QHBoxLayout(row_widget)

            name_label = self.create_label(f"{ingredient.name}", "#2e302f", 250, 50)
            stock_label = self.create_label(f"Stock: {ingredient.stock}", "#2e302f", 160, 50)
            # text edits
            stock_input = QLineEdit()
            stock_input.setFixedSize(140, 45)
            stock_input.setStyleSheet("background-color: white; color: black; border-radius: 10px; font-size: 18px;")
            #set button
            Increase_button = self.create_button("Increase", "green", 160, 45)
            Increase_button.clicked.connect(lambda _, ing=ingredient, inp=stock_input: self.update_ingredient_stock(ing, inp,increase = True))
            Decrease_button = self.create_button("Decrease", "red", 160, 45)
            Decrease_button.clicked.connect(lambda _, ing=ingredient, inp=stock_input: self.update_ingredient_stock(ing, inp, increase=False))

            #adding items
            row_layout.addWidget(name_label)
            row_layout.addWidget(stock_label)
            row_layout.addWidget(stock_input)
            row_layout.addWidget(Increase_button)
            row_layout.addWidget(Decrease_button)

            list_layout.addWidget(row_widget)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        #back button
        back_button = self.create_button('Back', 'red', 300, 50)
        back_button.clicked.connect(self.show_manager_menu)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.inventory_feedback = self.create_label("", "red", 400, 40)
        self.inventory_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.inventory_feedback)

    #MODULE FUNCTIONS: BUTTON, LABEl and FONT AND ??
    def create_font(self, point_size, weight=QFont.Weight.Normal):
        font = QFont("Inter")
        font.setPointSize(point_size)
        if isinstance(weight, int):
            weight = QFont.Weight(weight)
        font.setWeight(weight)
        return font

    def create_button(self, text, color="#2563eb", width=300, height=55):
        btn = QPushButton(text)
        btn.setFixedSize(width, height)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(self.create_font(18, QFont.Weight.DemiBold))
        btn.setStyleSheet(f"QPushButton {{background-color: {color}; color: white; border: none; border-radius: 14px; padding: 10px 18px; font-size: 18px; font-weight: 600;}} QPushButton:hover {{background-color: #1d4ed8;}} QPushButton:pressed {{background-color: #1e40af; padding-top: 12px;}}")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(22)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 120))
        btn.setGraphicsEffect(shadow)
        return btn

    def create_label(self, text, color="#1f2937", width=300, height=55):
        label = QLabel(text)
        label.setFixedSize(width, height)
        label.setFont(self.create_font(18, QFont.Weight.Medium))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"QLabel {{background-color: {color}; color: white; border: 1px solid #374151; border-radius: 14px; padding: 8px; font-size: 18px;}}")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 100))
        label.setGraphicsEffect(shadow)

        return label