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
            self.users = self.logic.getListOfUsers()
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
        combo1_button = self.create_button(f"Cheeseburger Combo",'#2e302f',300,100)
        combo1_button.clicked.connect(lambda: self.add_to_cart(1))
        combo1_button.clicked.connect(lambda: self.add_to_cart(6))
        combo1_button.clicked.connect(lambda: self.add_to_cart(10))
        combo_row.addWidget(combo1_button) 

        combo2_button = self.create_button(f"Double Cheeseburger Combo",'#2e302f',350,100)
        combo2_button.clicked.connect(lambda: self.add_to_cart(2))
        combo2_button.clicked.connect(lambda: self.add_to_cart(6))
        combo2_button.clicked.connect(lambda: self.add_to_cart(10))
        combo_row.addWidget(combo2_button) 
        
        combo3_button = self.create_button(f"Chicken Nugget Combo",'#2e302f',300,100)
        combo3_button.clicked.connect(lambda: self.add_to_cart(3))
        combo3_button.clicked.connect(lambda: self.add_to_cart(6))
        combo3_button.clicked.connect(lambda: self.add_to_cart(10))
        combo_row.addWidget(combo3_button) 

        combo4_button = self.create_button(f"Chicken Tenders Combo",'#2e302f',300,100)
        combo4_button.clicked.connect(lambda: self.add_to_cart(4))
        combo4_button.clicked.connect(lambda: self.add_to_cart(6))
        combo4_button.clicked.connect(lambda: self.add_to_cart(10))
        combo_row.addWidget(combo4_button) 

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
        cart_widget.setFixedWidth(400) #maybe more?? idk
        cart_widget.setStyleSheet("background-color: #2e302f; border-radius: 10px;")

        #cart items
        cart_title = self.create_label("Cart",'gray',350,50)
        cart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cart_layout.addWidget(cart_title)

        #scroll wheel to handle more items
        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setStyleSheet("border-radius:15px; background-color:black; padding:5px;")       
        self.cart_container = QWidget()
        self.cart_items_layout = QVBoxLayout(self.cart_container)
        self.cart_items_layout.setSpacing(1)
        self.cart_scroll.setWidget(self.cart_container)
        self.cart_layout.insertWidget(1, self.cart_scroll) 
        
        # To place checkout at the bottom
        self.cart_layout.addStretch()  

        checkout_button = self.create_button("Checkout",'#0c401a',300,100) #checkout button
        checkout_button.clicked.connect(lambda: self.data.purchase())
        checkout_button.clicked.connect(lambda: self.update_cart())
        
        self.cart_layout.addWidget(checkout_button,alignment=Qt.AlignmentFlag.AlignCenter)
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
        # View sales button
        view_sales_button = self.create_button('View Sales','gray',300,50)
        layout.addWidget(view_sales_button,1,0) # Where it is row 3, col 0, takes 1 row and 2 columns
        # Manager inventory button
        manage_inventory_button = self.create_button('Manage Inventory','gray',300,50)
        layout.addWidget(manage_inventory_button,2,0)
        if self.manager_feedback_message:
            feedback_label = QLabel(self.manager_feedback_message)
            feedback_label.setFixedSize(360, 45)
            feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            feedback_label.setStyleSheet(
                "color: white; font-size: 18px; background-color: #0c401a; "
                "border-radius: 10px; padding: 6px;"
            )
            layout.addWidget(feedback_label, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            self.manager_feedback_message = ""
        # Back Button
        back_button = self.create_button('Return','red',300,50)
        layout.addWidget(back_button,4,0)
        back_button.clicked.connect(self.show_home_screen)

    def show_add_employee_screen(self): # Add employee
        add_ui = QWidget()
        self.setCentralWidget(add_ui)
        add_ui.setStyleSheet("background-color: black;")

        self.add_employee_feedback = None
        layout = QGridLayout(add_ui)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = self.create_label("Add Employee","",400,50)
        title.setFont(self.create_font(25))

        # Username
        user_label = self.create_label("Username:",'',100,40)
        user_input = QLineEdit()
        user_input.setMaximumSize(200, 40)
        user_input.setStyleSheet("font-size: 18px;border-radius: 15px;background-color: white; color: black")

        # Password
        pass_label = self.create_label("Password:",'',100,40)
        pass_input = QLineEdit()
        pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        pass_input.setFixedSize(250, 40)
        pass_input.setMaximumSize(200, 40)
        pass_input.setStyleSheet("font-size: 18px;border-radius: 15px; background-color: white; color: black")

        # Checkbox
        checkbox = QCheckBox("Admin:")
        checkbox.setStyleSheet("color: white; font-size: 18px; QCheckBox::indicator { width: 20px; height: 20px; }")

        # Submit button
        submit_button = self.create_button('Add-User','green',300,50)
        submit_button.clicked.connect(lambda: self.submit_event_handler(user_input, pass_input, checkbox))

        # Back button
        back_button = self.create_button('Back','red',300,50)
        back_button.clicked.connect(self.show_manager_menu)

        # Add to layout
        layout.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(user_label, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(user_input, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(pass_label, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(pass_input, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(checkbox, 3, 1, 1, 2,alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(submit_button, 4, 0, 1, 3)

        self.add_employee_feedback = QLabel("")
        self.add_employee_feedback.setFixedSize(360, 45)
        self.add_employee_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_employee_feedback.setWordWrap(True)
        self.add_employee_feedback.setStyleSheet(
            "color: white; font-size: 18px; background-color: transparent;"
        )
        layout.addWidget(self.add_employee_feedback, 5, 0, 1, 3,
                         alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(back_button, 6, 0, 1, 3)

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
            self.manager_feedback_message = f"Added user '{username_text}'."
            self.show_manager_menu()
            return

        self.show_add_employee_feedback(f"Username '{username_text}' is already taken.", False)

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
        for i in reversed(range(self.grid.count())):
            widget = self.grid.takeAt(i).widget()
            if widget:
                widget.deleteLater()
        
        list_buttons = []
        

        print (f"{range(self.data.getItemCount())} is the range")
        print(f"category is {category}")
        for i in range(self.data.getItemCount()):
            btn = self.create_button((f"{self.data.getItemName(i+1)}"),'#2e302f',250,150)
            list_buttons.append(btn)
            list_buttons[i].clicked.connect(lambda _, x=i+1: self.add_to_cart(x))
        
        row = 0
        col = 0
        for i in range(self.data.getItemCount()):
            if (self.data.getCategoryID(i+1) == category or category == 0):
                if (col < 4):
                    self.grid.addWidget(list_buttons[i], row, col)
                    print(f"added {self.data.getItemName(i+1)} to grid. index is {i}")
                    col += 1
                else:
                    col = 0
                    row += 1
                    self.grid.addWidget(list_buttons[i], row, col)
                    print(f"added {self.data.getItemName(i+1)} to grid. index is {i}")
                    col += 1
    #Make c++ function to return a vector/list instead of calling it each iteration. 

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
        # putting Items from cart to the screen
        for item in range(self.data.getCartCount()):
            label = self.create_label(f"{self.data.getCheckoutName(item)} - ${self.data.getCheckoutPrice(item)}",'',250,40)
            label.setFont(self.create_font(20))
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.cart_items_layout.addWidget(label)
            t += self.data.getCheckoutPrice(item)

            print(f"added {self.data.getCheckoutName(item)} to cart display")

        if hasattr(self, "total_label"):
            self.total_label.deleteLater()
        self.total_label = self.create_label(f"Total: ${t:.2f}",'',300,225)
        self.total_label.setFont(self.create_font(25))
        self.cart_layout.addWidget(self.total_label)

#Close program function
#-----------------------------------------------------------------------------
    #Closes the program.
    def close_program(self):
        self.clear_cart()
        QApplication.quit()  
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
