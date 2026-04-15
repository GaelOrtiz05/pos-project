#access files
import os
#access environment
import sys

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
from PySide6.QtGui import QShortcut, QKeySequence,QKeySequence,QGuiApplication, QFont

import pos_backend 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager_feedback_message = ""
        screen = QGuiApplication.primaryScreen()
        size = screen.availableGeometry()
        window_length = size.width()
        window_height = size.height()
        self.setWindowTitle("POS")
        self.resize(window_length, window_height)
        self.show_login_screen()

        self.shortcut_close = QShortcut(QKeySequence.StandardKey.Close, self)
        self.shortcut_close.activated.connect(self.close)

        self.logic = pos_backend.Login()
        self.data = pos_backend.Database()

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
    
    def login_event_handler(self, username, password,layout): # Authenticate login
        username = username.text()
        password = password.text()
        if self.logic.loginUser(username, password) is True:
            self.current_user = self.logic.getUser(username)
            # self.user = self.logic.getListOfUsers()
            # self.itemsByCategory = self.data.getItemsByCategory()
            self.items = self.data.getItems()
            self.show_home_screen()
        else:
            error_label = QLabel('Incorrect User or Password')
            error_label.setFixedSize(300,50)
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(error_label,5,0,1,2)
            error_label.setStyleSheet("background-color: black;font-size: 20px;border-radius: 10px; color: red;")


    #POS HOME SCREEN
    #-------------------------------------------------------------------------------- 
    def show_home_screen(self):  # Main UI

        home_widget = QWidget()
        self.setCentralWidget(home_widget)
        home_widget.setStyleSheet("background-color: black;")

        main_layout = QVBoxLayout(home_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        #Top Row Layout - categories, username, manager, logout
        #---------------------------------------------------------------------------
        # Row for the categories
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        all_items = self.create_button('All', '#2e302f', 150, 50)
        all_items.clicked.connect(lambda: self.load_grid(0))

        entre_button = self.create_button('Entre', '#2e302f', 150, 50)
        entre_button.clicked.connect(lambda: self.load_grid(1))

        sides_button = self.create_button('Sides', '#2e302f', 150, 50)
        sides_button.clicked.connect(lambda: self.load_grid(2))

        dessert_button = self.create_button('Dessert', '#2e302f', 150, 50)
        dessert_button.clicked.connect(lambda: self.load_grid(3))

        drink_button = self.create_button('Drinks', '#2e302f', 150, 50)
        drink_button.clicked.connect(lambda: self.load_grid(4))
        
        if self.current_user.isAdmin:
            manager_button = self.create_button('Manager', '#2e302f', 150, 50)
        
        logout_button = self.create_button('Logout', '#540612', 150, 50)

        for button in [all_items, entre_button, sides_button, dessert_button, drink_button] + ([manager_button] if self.current_user.isAdmin else []) + [logout_button]:
            top_row.addWidget(button)
        top_row.setAlignment(Qt.AlignmentFlag.AlignCenter) # centering the buttons
        # Disp username
        user_label = self.create_label(f"Logged in as: {self.current_user.name}",'#2e302f',500,50)
        top_row.addWidget(user_label)

        main_layout.addLayout(top_row)

        #------------------------------------
        combo_row = QHBoxLayout()
        combo_row.setSpacing(75)
        #displaying the categories
        
        #Displays Combo Buttons 1-4
        #--------------------------------------------------------------------
        combo1_button = self.create_button(f"Combo #1",'#2e302f',300,100)
        combo1_button.clicked.connect(lambda: self.add_to_cart(1))
        combo1_button.clicked.connect(lambda: self.add_to_cart(6))
        combo1_button.clicked.connect(lambda: self.add_to_cart(10))
        combo_row.addWidget(combo1_button) 

        combo2_button = self.create_button(f"Combo #2",'#2e302f',350,100)
        combo2_button.clicked.connect(lambda: self.add_to_cart(2))
        combo2_button.clicked.connect(lambda: self.add_to_cart(6))
        combo2_button.clicked.connect(lambda: self.add_to_cart(10))
        combo_row.addWidget(combo2_button) 
        
        combo3_button = self.create_button(f"Combo #3",'#2e302f',300,100)
        combo3_button.clicked.connect(lambda: self.add_to_cart(3))
        combo3_button.clicked.connect(lambda: self.add_to_cart(6))
        combo3_button.clicked.connect(lambda: self.add_to_cart(10))
        combo_row.addWidget(combo3_button) 

        # combo4_button = self.create_button(f"Chicken Tenders Combo",'#2e302f',300,100)
        # combo4_button.clicked.connect(lambda: self.add_to_cart(4))
        # combo4_button.clicked.connect(lambda: self.add_to_cart(6))
        # combo4_button.clicked.connect(lambda: self.add_to_cart(10))
        # combo_row.addWidget(combo4_button) 

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
        cart_widget.setStyleSheet("background-color: #2e302f; border-radius: 14px;")

        # cart title
        cart_title = QLabel("Cart")
        cart_title.setFixedHeight(50)
        cart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cart_title.setFont(self.create_font(20, 600))
        cart_title.setStyleSheet(
            "background-color: #888888; color: white; border-radius: 12px;"
        )
        self.cart_layout.addWidget(cart_title)

        # scroll wheel to handle more items
        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setStyleSheet(
            "QScrollArea { border-radius: 15px; background-color: black; padding: 6px; }"
        )
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
        self.total_label.setStyleSheet(
            "background-color: #151515; color: white; border: 2px solid #0c401a; border-radius: 14px;"
        )

        checkout_button = self.create_button("Checkout", '#0c401a', 320, 90)
        checkout_button.clicked.connect(lambda: self.data.purchase())
        checkout_button.clicked.connect(lambda: self.update_cart())

        footer_layout.addWidget(self.total_label)
        footer_layout.addWidget(checkout_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.cart_layout.addWidget(footer_widget)
        bottom_row.addWidget(cart_widget, 1)  # smaller than scroll

        # add the scroll and cart to main layout
        main_layout.addLayout(bottom_row)

        #Logout button functionality
        #-----------------------------------------------------------------------------
        #programming the button 
        logout_button.clicked.connect(self.show_login_screen) #logoin screen
        if self.current_user.isAdmin:
            manager_button.clicked.connect(lambda: self.manager_event_handler())

        self.update_cart() # to update cart each time we go back to home screen, so it doesn't show old items after purchase

    # manager functions
    #--------------------------------------------------------------------------------
    def manager_event_handler(self):
        if self.current_user.isAdmin:
            self.show_manager_menu()
        # else:

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


    # added submit event handler
    # should probably validate input to make sure there are no spaces in username, or password
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

    #GUI element functions
    #-----------------------------------------------------------------------------
    #Button creation shortcut.
    def create_button(self, text, color="gray", width=300, height=50): 
        btn = QPushButton(text)
        btn.setFixedSize(width, height)
        btn.setFont(self.create_font(25, 600))
        btn.setStyleSheet(f"""QPushButton {{background-color: {color};color: white;font-size: 25px;font-weight: 600;border: 3px;border-radius: 25px;padding: 10px;}}QPushButton:hover {{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 {color},stop:1 #797b8a);color: #222;}}QPushButton:pressed {{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #d0d0d0,stop:1 #a0a0a0);}}""")       
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(2)
        shadow.setYOffset(2)
        shadow.setColor(Qt.gray)
        btn.setGraphicsEffect(shadow)

        return btn
    
    #label creation shortcut.
    def create_label(self,text,color = 'gray',width=300,height = 50):
        if not color:
            color = "transparent"
        label = QLabel(text)
        label.setFixedSize(width,height)
        label.setFont(self.create_font(25))
        label.setStyleSheet(f"background-color: {color};font-size: 25px; border-radius: 10px; color: white; padding: 5px")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(Qt.black)
        label.setGraphicsEffect(shadow)
        return label

    #Loads main grid with items from the items table based on category_id
    #Category 0 = all, 1 = entre, 2 = sides, 3 = dessert, 4 = drinks
    def load_grid(self,category = 0):                
        for items in reversed(range(self.grid.count())):
            widget = self.grid.takeAt(items).widget()
            if widget:
                widget.deleteLater()
        
        list_buttons = []
        
        self.items = self.data.getItems()

        # print (f"{range(self.data.getItemCount())} is the range")
        # print(f"category is {category}")

        for idx, items in enumerate(self.items):
            btn = self.create_button((f"{items.name}"),'#2e302f',250,150)
            list_buttons.append(btn)
            list_buttons[idx].clicked.connect(lambda _, x=items: self.disp_ingredients_menu(x))
        row = 0
        col = 0
        for idx, items in enumerate(self.items):
            if (items.categoryId == category or category == 0):
                if (col < 4):
                    self.grid.addWidget(list_buttons[idx], row, col)
                    print(f"added {items.name} to grid. index is {idx}")
                    col += 1
                else:
                    col = 0
                    row += 1
                    self.grid.addWidget(list_buttons[idx], row, col)
                    print(f"added {items.name} to grid. index is {idx}")
                    col += 1
 
    #     for i in range(self.data.getItemCount()):
    #         btn = self.create_button((f"{self.items.name(0)}"),'#2e302f',250,150)
    #         list_buttons.append(btn)
    #         list_buttons[i].clicked.connect(lambda _, x=i+1: self.disp_ingredients_menu(x))        
    #     row = 0
    #     col = 0
    #     for i in range(self.data.getItemCount()):
    #         if (self.data.getCategoryID(i+1) == category or category == 0):
    #             if (col < 4):
    #                 self.grid.addWidget(list_buttons[i], row, col)
    #                 print(f"added {self.data.getItemName(i+1)} to grid. index is {i}")
    #                 col += 1
    #             else:
    #                 col = 0
    #                 row += 1
    #                 self.grid.addWidget(list_buttons[i], row, col)
    #                 print(f"added {self.data.getItemName(i+1)} to grid. index is {i}")
    #                 col += 1
    # #Make c++ function to return a vector/list instead of calling it each iteration. 

    #Font shortcut function.     
    def create_font(self, point_size, weight=QFont.Weight.Normal):
        font = QFont()
        font.setPointSize(point_size)
        if isinstance(weight, int):
            weight = QFont.Weight(weight)
        font.setWeight(weight)
        return font

#Checkout cart functions
#-----------------------------------------------------------------------------
    #Adds an item to the checkout table based on item id.
    def add_to_cart(self, item): # this function will add the items to screen
        self.data.addCheckout(item)
        self.update_cart()

    #Clears the current cart display.
    def clear_cart(self):
        for i in reversed(range(self.cart_items_layout.count())):
            widget = self.cart_items_layout.takeAt(i).widget()
            if widget:
                widget.deleteLater()
        
    #adds item to the cart display.
    def update_cart(self): #update cart each time item is added
        t = 0.0
        self.clear_cart()
        checkout_items = self.data.getCheckout()
        # putting Items from cart to the screen
        for checkout_item in checkout_items:
            item_name = checkout_item.itemName
            item_price = checkout_item.itemPrice
            label = QLabel(f"{item_name} - ${item_price:.2f}")
            label.setFixedHeight(self.cart_item_row_height)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.setFont(self.create_font(18))
            label.setStyleSheet(
                "background-color: #111111; color: white; border-radius: 10px; padding-left: 12px;"
            )
            self.cart_items_layout.addWidget(label)
            t += item_price

            print(f"added {item_name} to cart display")

        if len(checkout_items) == 0:
            empty_label = QLabel("No items in cart")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setFont(self.create_font(16))
            empty_label.setStyleSheet(
                "background-color: transparent; color: #a0a0a0;"
            )
            self.cart_items_layout.addStretch()
            self.cart_items_layout.addWidget(empty_label)
            self.cart_items_layout.addStretch()

        self.total_label.setText(f"Total: ${t:.2f}")

    def disp_sales_menu(self):
        sales_ui = QWidget()
        self.setCentralWidget(sales_ui)
        sales_ui.setStyleSheet("background-color: black;")
        layout = QGridLayout(sales_ui)
        # Add employee Button
        todays_sales = self.create_button('Sale Today','gray',300,50)
        layout.addWidget(todays_sales,0,0)
        weekly_sales = self.create_button('Sale This Week','gray',300,50)
        layout.addWidget(weekly_sales,0,1)
        monthly_sales = self.create_button('Sale This Month','gray',300,50)
        layout.addWidget(monthly_sales,0,2)

        back_button = self.create_button('Back','red',300,50)
        back_button.clicked.connect(self.show_manager_menu)
        layout.addWidget(back_button,0,3)



    def disp_ingredients_menu(self, item):
        ingredients_ui = QWidget()
        self.setCentralWidget(ingredients_ui)
        ingredients_ui.setStyleSheet("background-color: black;")
        layout = QGridLayout(ingredients_ui)
        #titles
        self.items = self.data.getItems()
        title = self.create_label(f"Customize {item.name}", "", 500, 50)
        layout.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        #confrim (sending to cart)
        confirm_button = self.create_button('Confirm', 'green', 300, 50)
        confirm_button.clicked.connect(lambda: self.confirm_item(item.id))
        layout.addWidget(confirm_button, 1, 0)

        #go to home screen
        back_button = self.create_button('Back', 'red', 300, 50)
        back_button.clicked.connect(self.show_home_screen)
        layout.addWidget(back_button, 1, 1)

    def confirm_item(self, item): # will connect this to the ingredients screen
        self.data.addCheckout(item)
        self.show_home_screen()
        self.update_cart()
#Close program function
#-----------------------------------------------------------------------------
    #Closes the program.
    def close_program(self):
        QApplication.quit()  
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
