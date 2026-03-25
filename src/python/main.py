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

    def show_login_screen(self):
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

        login_button.clicked.connect(lambda: self.login_event_handler(user_input, password_input,layout))
        # login_button.clicked.connect(self.show_home_screen)
        
    def login_event_handler(self, username, password,layout):
        username = username.text()
        password = password.text()
        if self.logic.loginUser(username, password) is True:
            self.show_home_screen()
        else:
            error_label = QLabel('Incorrect User or Password')
            error_label.setFixedSize(300,50)
            layout.addWidget(error_label,5,0,1,2)
            error_label.setStyleSheet("background-color: black;font-size: 15px;border-radius: 10px; color: red;")
            

    def show_home_screen(self):
        home_widget = QWidget()
        self.setCentralWidget(home_widget)
        # Declaring the categories
        layout = QGridLayout(home_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Adding Buttons
        All_items = QPushButton('All')
        Entre_Button = QPushButton("Entres")
        Sides_Button = QPushButton("Sides")
        Dessert_Button = QPushButton("Dessert")
        Drink_Button = QPushButton("Drinks")
        Manager_Button = QPushButton("Manager")

        # Customizing the button
        All_items.setStyleSheet("QPushButton {background-color: black ; border-radius: 10px; font-size: 25px;}QPushButton:pressed {background-color: gray;}")
        All_items.setFixedSize(150,50)
        Entre_Button.setStyleSheet("QPushButton {background-color: black ; border-radius: 10px; font-size: 25px;}QPushButton:pressed {background-color: gray;}")
        Entre_Button.setFixedSize(150,50)
        Sides_Button.setStyleSheet("QPushButton {background-color: black ; border-radius: 10px; font-size: 25px;}QPushButton:pressed {background-color: gray;}")
        Sides_Button.setFixedSize(150,50)
        Dessert_Button.setStyleSheet("QPushButton {background-color: black ; border-radius: 10px; font-size: 25px;}QPushButton:pressed {background-color: gray;}")
        Dessert_Button.setFixedSize(150,50)
        Drink_Button.setStyleSheet("QPushButton {background-color: black ; border-radius: 10px; font-size: 25px;}QPushButton:pressed {background-color: gray;}")
        Drink_Button.setFixedSize(150,50)
        Manager_Button.setStyleSheet("QPushButton {background-color: #63130d ; border-radius: 10px; font-size: 25px;}QPushButton:pressed {background-color: gray;}")
        Manager_Button.setFixedSize(150,50)
        # Displaying the categories
        i = 0
        layout.addWidget(All_items,i,0)
        layout.addWidget(Entre_Button,i,1)
        layout.addWidget(Sides_Button,i,2)
        layout.addWidget(Dessert_Button,i,3)
        layout.addWidget(Drink_Button,i,4)
        layout.addWidget(Manager_Button,0,5)

        # Main Combo Buttobs
        for i in range(5):
            combo_button = QPushButton(f"Combo {i}")
            combo_button.setFixedSize(100,100)
            combo_button.setStyleSheet("QPushButton {background-color: gray ; border-radius: 5px; font-size: 20px;}QPushButton:pressed {background-color: black;}")
            layout.addWidget(combo_button,1,i)

        # Scrolling options
        scroll = QScrollArea() # Making scroll area
        scroll.setWidgetResizable(True)   
        container = QWidget() # making a container
        grid = QGridLayout(container) 
        for i in range(10):
            for j in range (5):
                btn = QPushButton(f"Item {i*7+j}")
                btn.setFixedSize(80,80)
                btn.setStyleSheet("QPushButton {background-color: gray ; border-radius: 5px; font-size: 20px;}QPushButton:pressed {background-color: black;}")
                grid.addWidget(btn,i,j)

        #Programming the buttons
        Manager_Button.clicked.connect(self.show_manager_menu) #manager menu



        scroll.setWidget(container)

        # Add scroll area to your main layout
        layout.addWidget(scroll,2,0,1,5)

    def show_manager_menu(self):
        manager_ui = QWidget()
        self.setCentralWidget(manager_ui)
        manager_ui.setStyleSheet("background-color: black;")
        layout = QGridLayout(manager_ui)
        # Add employee Button
        create_new_account_button = QPushButton('Add Employee')
        create_new_account_button.setFixedSize(300,50)
        layout.addWidget(create_new_account_button,0,0) # Where it is row 3, col 0, takes 1 row and 2 columns
        create_new_account_button.setStyleSheet("background-color: purple;font-size: 25px;border-radius: 20px;")
        # View sales button
        view_sales_button = QPushButton('View Sales')
        view_sales_button.setFixedSize(300,50)
        layout.addWidget(view_sales_button,1,0) # Where it is row 3, col 0, takes 1 row and 2 columns
        view_sales_button.setStyleSheet("background-color: gray;font-size: 25px;border-radius: 20px;")
        # ??? Button

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
