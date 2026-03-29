import os
import sys

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
    QHBoxLayout
)

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
        pos_label = QLabel("Point of Sale System")
        pos_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        user_label = QLabel("Username")
        pass_label = QLabel("Password")
        pos_label.setStyleSheet("background-color: black ; border-radius: 10px; font-size: 25px;")
        pass_label.setStyleSheet("background-color: black ; border-radius: 10px; font-size: 25px;")
        user_label.setStyleSheet("background-color: black ; border-radius: 10px; font-size: 25px;")
        user_label.setMaximumSize(150,50)
        pass_label.setMaximumSize(150,50)
        pos_label.setFixedSize(300,50)
        # user_label.setGeometry(100, 200, 200, 200) # position x,y and then size x,y
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
        login_button = QPushButton('Login')
        login_button.setFixedSize(300,50)
        layout.addWidget(login_button,4,0,1,2)
        login_button.setStyleSheet("background-color: green;font-size: 35px;border-radius: 10px; color: white;")

       # create_new_account_button = QPushButton('Add Employee')
        #create_new_account_button.setFixedSize(300,50)
        #layout.addWidget(create_new_account_button,3,0,1,2) # Where it is row 3, col 0, takes 1 row and 2 columns
        # create_new_account_button.setStyleSheet("background-color: purple;font-size: 25px;border-radius: 20px;")

        login_button.clicked.connect(lambda: self.login_event_handler(user_input, password_input, layout))
        # login_button.clicked.connect(self.show_home_screen)
        
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

        all_items = self.create_button('All', 'black', 150, 50)
        entre_button = self.create_button('Entre', 'black', 150, 50)
        sides_button = self.create_button('Sides', 'black', 150, 50)
        dessert_button = self.create_button('Dessert', 'black', 150, 50)
        drink_button = self.create_button('Drinks', 'black', 150, 50)
        manager_button = self.create_button('Manager', 'black', 150, 50)
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
        user_label = QLabel(f"Logged in as: {self.current_user.name}")
        user_label.setStyleSheet("""background-color: gray; color: white;font-size: 20px;padding: 8px;border-radius: 10px;""")
        user_label.setFixedHeight(50)
        top_row.addWidget(user_label)

        main_layout.addLayout(top_row)

        combo_row = QHBoxLayout()
        combo_row.setSpacing(100)
        #displaying the categories
        for i in range(5):
            combo_button = QPushButton(f"Combo {i+1}")
            combo_button.setFixedSize(200, 100)
            combo_button.setStyleSheet("""
                QPushButton {background-color: gray;border-radius: 10px;font-size: 18px;color: white;}
                QPushButton:pressed {background-color: black;}""")
            combo_row.addWidget(combo_button)

        combo_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(combo_row)

        # Scroll Box - main combo items will be here 
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: black; border: none;")

        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(10)

        for i in range(10):
            for j in range(5):
                btn = self.create_button((f"Item {i*5+j+1}"),'gray',150,150)
                grid.addWidget(btn, i, j)

        scroll.setWidget(container)
        #main_layout.addWidget(scroll)
        # Bottom section (items + cart)
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        # LEFT SIDE (scroll box)
        bottom_row.addWidget(scroll, 3)  

        # RIGHT SIDE (cart panel)
        cart_widget = QWidget()
        cart_layout = QVBoxLayout(cart_widget)
        cart_widget.setFixedWidth(400) #maybe more?? idk
        cart_widget.setStyleSheet("background-color: gray; border-radius: 10px;")
        cart_title = QLabel("Cart")
        cart_title.setStyleSheet("color: white; font-size: 22px;")
        cart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cart_layout.addWidget(cart_title)

        # cart items printing w/ price and stuff
        for i in range(3): # testing the # of items
            item = QLabel(f"Item {i+1}")
            item.setStyleSheet("color: white; font-size: 16px;")
            cart_layout.addWidget(item)

        cart_layout.addStretch()  
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
        create_new_account_button = QPushButton('Add Employee')
        create_new_account_button.setFixedSize(300,50)
        layout.addWidget(create_new_account_button,0,0) # Where it is row 3, col 0, takes 1 row and 2 columns
        create_new_account_button.setStyleSheet("background-color: purple;font-size: 25px;border-radius: 20px;")
        create_new_account_button.clicked.connect(self.show_add_employee_screen)
        # View sales button
        view_sales_button = QPushButton('View Sales')
        view_sales_button.setFixedSize(300,50)
        layout.addWidget(view_sales_button,1,0) # Where it is row 3, col 0, takes 1 row and 2 columns
        view_sales_button.setStyleSheet("background-color: gray;font-size: 25px;border-radius: 20px;")
        # Back Button
        back_button = self.create_button('Return','red',300,75)
        layout.addWidget(back_button,2,0)
        back_button.clicked.connect(self.show_home_screen)

    def show_add_employee_screen(self): # Add employee
        add_ui = QWidget()
        self.setCentralWidget(add_ui)
        add_ui.setStyleSheet("background-color: black;")

        layout = QGridLayout(add_ui)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("Add Employee")
        title.setStyleSheet("color: white; font-size: 30px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Username
        user_label = QLabel("Username:")
        user_label.setStyleSheet("color: white; font-size: 20px;")

        user_input = QLineEdit()
        user_input.setFixedSize(250, 40)
        user_input.setStyleSheet("font-size: 18px;border-radius: 15px;background-color: white")

        # Password
        pass_label = QLabel("Password:")
        pass_label.setStyleSheet("color: white; font-size: 20px;")

        pass_input = QLineEdit()
        pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        pass_input.setFixedSize(250, 40)
        pass_input.setStyleSheet("font-size: 18px;border-radius: 15px; background-color: white")

        # Checkbox
        checkbox = QCheckBox("Admin:")

        # Submit button
        submit_button = self.create_button('Add-User','green')
        submit_button.clicked.connect(lambda: self.submit_event_handler(user_input, pass_input, checkbox.isChecked()))

        # Back button (optional but clutch)
        back_button = self.create_button('Back','red')
        back_button.clicked.connect(self.show_manager_menu)

        # Add to layout
        layout.addWidget(title, 0, 0, 1, 2)
        layout.addWidget(user_label, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(user_input, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(pass_label, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(pass_input, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(checkbox, 3, 1, 1, 2)
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
        btn.setStyleSheet(f"""QPushButton {{background-color: {color};font-size: 25px;border-radius: 20px;}}QPushButton:pressed {{background-color: gray;}}""")
        return btn
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
