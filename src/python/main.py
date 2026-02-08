import os
import sys

from PySide6.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QGridLayout,
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence

import pos_backend

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Keyboard Shorcuts
        # Standard keys found in link below
        # https://doc.qt.io/qtforpython-6/PySide6/QtGui/QKeySequence.html#PySide6.QtGui.QKeySequence.StandardKey
        self.shortcut_close = QShortcut(QKeySequence.StandardKey.Close, self)
        self.shortcut_close.activated.connect(self.close)

        # Initialize C++ POS class from backend module and save it to self.pos
        self.logic = pos_backend.POS()

        # Set Window Title
        self.setWindowTitle("POS")
        self.resize(800, 600)
        
        # Don't know what this does but i saw it in a yt video so... :)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QGridLayout(central) 

        # Declaring a text label that contains the total price
        self.label_total = QLabel(f"Total: ${self.logic.getTotal():.2f}")
        
        # Toolbar at bottom of window
        self.statusBar().showMessage("Fast Food Menu:")

        # Add the previously declared text label to the screen
        layout.addWidget(self.label_total, 0 , 0, Qt.AlignmentFlag.AlignTop)

        # Declaring button for salad
        self.button_salad = QPushButton("Salad ($8.00)")
        # Lambda waits for a click and then runs the button_clicked helper function
        self.button_salad.clicked.connect(lambda: self.menu_button_event_handler("Salad", 8.00))
        # Place the button on the screen
        layout.addWidget(self.button_salad, 0,2)

        # Same thing
        self.button_patty_melt = QPushButton("Patty Melt ($5.49)")
        self.button_patty_melt.clicked.connect(lambda: self.menu_button_event_handler("Patty Melt", 5.49))
        layout.addWidget(self.button_patty_melt, 0, 3)

        # Clear Button
        self.button_clear = QPushButton("Clear")
        self.button_clear.clicked.connect(lambda: self.clear_button_event_handler())
        layout.addWidget(self.button_clear, 0,4)


    def clear_button_event_handler(self):
        ## Uses the c++ function clear to clear cart
        self.logic.clear()
        self.label_total.setText(f"Total: ${self.logic.getTotal():.2f}")

    def menu_button_event_handler(self, name, price):
        # Uses the c++ function addItem to calculate the price
        self.logic.addItem(name, price)
        # Uses the c++ function getTotal to fetch price
        self.label_total.setText(f"Total: ${self.logic.getTotal():.2f}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

