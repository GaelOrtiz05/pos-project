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
from PySide6.QtGui import QShortcut, QKeySequence,QKeySequence,QGuiApplication

import pos_backend 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        all_items = self.create_button('All', '#2e302f', 150, 50)
        entre_button = self.create_button('Entre', '#2e302f', 150, 50)
        sides_button = self.create_button('Sides', '#2e302f', 150, 50)
        dessert_button = self.create_button('Dessert', '#2e302f', 150, 50)
        drink_button = self.create_button('Drinks', '#2e302f', 150, 50)
        manager_button = self.create_button('Manager', '#2e302f', 150, 50)
        logout_button = self.create_button('Logout', '#540612', 150, 50)

        top_row.addWidget(all_items)
        top_row.addWidget(entre_button)
        top_row.addWidget(sides_button)
        top_row.addWidget(dessert_button)
        top_row.addWidget(drink_button)
        top_row.addWidget(manager_button)
        top_row.addWidget(logout_button)
        top_row.setAlignment(Qt.AlignmentFlag.AlignCenter) # centering the buttons
        # Disp username
        user_label = self.create_label(f"Logged in as: {self.current_user.name}",'#2e302f',50,50)
        user_label.setMaximumSize(500,50)
        top_row.addWidget(user_label)

        main_layout.addLayout(top_row)

        #------------------------------------
        combo_row = QHBoxLayout()
        combo_row.setSpacing(75)
        #displaying the categories
        
        #Displays Combo Buttons 1-4
        #--------------------------------------------------------------------
        combo1_button = self.create_button(f"Cheeseburger Combo",'#2e302f',300,100)
        combo1_button.clicked.connect(lambda: self.data.addCheckout("Cheeseburger"))
        combo_row.addWidget(combo1_button) 

        combo2_button = self.create_button(f"Double Cheeseburger Combo",'#2e302f',350,100)
        combo2_button.clicked.connect(lambda: self.data.addCheckout("Double Cheeseburger"))
        combo_row.addWidget(combo2_button) 

        combo3_button = self.create_button(f"Chicken Nugget Combo",'#2e302f',300,100)
        combo3_button.clicked.connect(lambda: self.data.addCheckout("Chicken Nuggets"))
        combo_row.addWidget(combo3_button) 

        combo4_button = self.create_button(f"Chicken Tenders Combo",'#2e302f',300,100)
        combo4_button.clicked.connect(lambda: self.data.addCheckout("Chicken Tenders"))
        combo_row.addWidget(combo4_button) 

        combo_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(combo_row)
        #------------------------------------------------------------------------------------------
        # Scroll Box - main combo items will be here 
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: black; border: none;")

        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(10)


       #Grid
        #--------------------------------------------------------------------------------------------
        #for i in range(10):
        #    for j in range(5):
        #        btn = self.create_button((f"Item {i*5+j+1}"),'#2e302f',150,150)
        #        grid.addWidget(btn, i, j)

        # manual grid of items, loop implementation is planned.
        btn_cheeseburger = self.create_button("Cheeseburger", '#2e302f', 250, 150)
        grid.addWidget(btn_cheeseburger, 0, 0)
        btn_cheeseburger.clicked.connect(lambda: self.data.addCheckout("Cheeseburger"))

        btn_d_cheeseburger = self.create_button("Double Cheeseburger", '#2e302f', 250, 150)
        grid.addWidget(btn_d_cheeseburger, 0, 1)
        btn_d_cheeseburger.clicked.connect(lambda: self.data.addCheckout("Double Cheeseburger"))

        btn_chk_nuggets = self.create_button("Chicken Nuggets", '#2e302f', 250, 150)
        grid.addWidget(btn_chk_nuggets, 0, 2)
        btn_chk_nuggets.clicked.connect(lambda: self.data.addCheckout("Chicken Nuggets"))


        btn_ckn_tenders = self.create_button("Chicken Tenders", '#2e302f', 250, 150)
        grid.addWidget(btn_ckn_tenders, 0, 3)
        btn_ckn_tenders.clicked.connect(lambda: self.data.addCheckout("Chicken Tenders"))

        #----------------------------
        btn_sm_fries = self.create_button("Small Fries", '#2e302f', 250, 150)
        grid.addWidget(btn_sm_fries, 1, 0)

        btn_med_fries = self.create_button("Medium Fries", '#2e302f', 250, 150)
        grid.addWidget(btn_med_fries, 1, 1)

        btn_lg_fries = self.create_button("Large Fries", '#2e302f', 250, 150)
        grid.addWidget(btn_lg_fries, 1, 2)

        btn_xl_fries = self.create_button("XL Fries", '#2e302f', 250, 150)
        grid.addWidget(btn_xl_fries, 1, 3)

        #----------------------------
        btn_sm_drink = self.create_button("Small Drink", '#2e302f', 250, 150)
        grid.addWidget(btn_sm_drink, 2, 0)

        btn_med_drink = self.create_button("Medium Drink", '#2e302f', 250, 150)
        grid.addWidget(btn_med_drink, 2, 1)

        btn_lg_drink = self.create_button("Large Drink", '#2e302f', 250, 150)
        grid.addWidget(btn_lg_drink, 2, 2)

        btn_xl_drink = self.create_button("XL Drink", '#2e302f', 250, 150)
        grid.addWidget(btn_xl_drink, 2, 3)
        #---------------------------------------------------------------------------


        scroll.setWidget(container)
        #main_layout.addWidget(scroll)
        # Bottom section (items + cart)
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)
        # LEFT SIDE (scroll box)
        bottom_row.addWidget(scroll, 3)  
        # RIGHT SIDE (cart panel)
        cart_widget = QWidget()
        self.cart_layout = QVBoxLayout(cart_widget)
        cart_widget.setFixedWidth(400) #maybe more?? idk
        cart_widget.setStyleSheet("background-color: #2e302f; border-radius: 10px;")
        cart_title = self.create_label("Cart",'gray',400,50)
        cart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cart_layout.addWidget(cart_title)
  
        # cart items printing w/ price and stuff
        for i in range(3): # testing the # of items
            item = QLabel(f"Item {i+1}")
            item.setStyleSheet("color: white; font-size: 16px;")
            self.cart_layout.addWidget(item)

        self.cart_layout.addStretch()  # To place checkout at the bottom

        checkout_button = self.create_button("Checkout",'#0c401a',300,100) #checkout button
        # checkout_button.setStyleSheet('font-size: 25px;')
        checkout_button.clicked.connect(lambda: self.data.purchase())
        
        self.cart_layout.addWidget(checkout_button,alignment=Qt.AlignmentFlag.AlignCenter)
        bottom_row.addWidget(cart_widget, 1)  # smaller than scroll
        # add the scroll and cart to main layout
        main_layout.addLayout(bottom_row)
        #programming the button 
        logout_button.clicked.connect(self.show_login_screen) #logoin screen
        manager_button.clicked.connect(lambda: self.manager_event_handler())

    # added event handler
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
        # Back Button
        back_button = self.create_button('Return','red',300,50)
        layout.addWidget(back_button,3,0)
        back_button.clicked.connect(self.show_home_screen)

    def show_add_employee_screen(self): # Add employee
        add_ui = QWidget()
        self.setCentralWidget(add_ui)
        add_ui.setStyleSheet("background-color: black;")

        layout = QGridLayout(add_ui)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = self.create_label("Add Employee","",400,50)
        title.setStyleSheet('font-size: 25px')

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
        checkbox.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; }")

        # Submit button
        submit_button = self.create_button('Add-User','green',300,50)
        submit_button.clicked.connect(lambda: self.submit_event_handler(user_input, pass_input, checkbox.isChecked()))

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
        layout.addWidget(back_button, 5, 0, 1, 3)

    # added submit event handler
    # should probably validate input to make sure there are no spaces in username, or password
    def submit_event_handler(self, username, password, isAdmin):
        username = username.text()
        password = password.text()
        self.logic.addUser(username, password, isAdmin)

    def create_button(self, text, color="gray", width=300, height=50): 
        btn = QPushButton(text)
        btn.setFixedSize(width, height)
        btn.setStyleSheet(f"QPushButton {{background-color: {color};font-size: 25px;border-radius: 20px;}}QPushButton:pressed {{background-color: gray;}}QPushButton:hover{{ background-color: blue;}}")
        return btn
    
    def create_label(self,text,color = 'gray',width=300,height = 50):
        label = QLabel(text)
        label.setFixedSize(width,height)
        label.setStyleSheet(f"background-color: {color};font-size: 25px; border-radius: 10px; color: white;")
        return label
    
    def add_to_cart(self): # this function will add the items to screen
        self.update_cart()
        pass
    def update_cart(self): #update cart each time item is added
        for i in range(self.cart_layout.count()): #clear current cart
            widget = self.cart_layout.itemAt(i).widget()
            if widget and widget.text() != "Cart":
                widget.deleteLater()
        # putting Items from cart to the screen
      #  for item in cart:
      #      label = QLabel(f"{item.name} - ${item.price}")
      #      label.setStyleSheet("color: white;")
      #      self.cart_layout.insertWidget(self.cart_layout.count()-1, label)


    def close_program(self):
        QApplication.quit()  
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
