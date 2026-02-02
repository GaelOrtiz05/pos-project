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


script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, "build", "debug"))

# Adjusts build paths depending on os
if sys.platform in ["darwin", "linux"]:
    sys.path.append(os.path.join(script_dir, "build"))
else:
    sys.path.append(os.path.join(script_dir, "build", "Debug"))

import backend

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Keyboard Shorcuts
        # Standard keys found in link below
        # https://doc.qt.io/qtforpython-6/PySide6/QtGui/QKeySequence.html#PySide6.QtGui.QKeySequence.StandardKey
        self.shortcut_close = QShortcut(QKeySequence.StandardKey.Close, self)
        self.shortcut_close.activated.connect(self.close)

        # Initialize C++ POS class from backend module and save it to self.pos
        self.logic = backend.POS()
        
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
        self.btn_salad = QPushButton("Salad ($8.00)")
        # Lambda waits for a click and then runs the button_clicked helper function
        self.btn_salad.clicked.connect(lambda: self.button_clicked("Salad", 8.00))
        # Place the button on the screen
        layout.addWidget(self.btn_salad, 0,2)

        # Same thing
        self.btn_patty_melt = QPushButton("Patty Melt ($5.49)")
        self.btn_patty_melt.clicked.connect(lambda: self.button_clicked("Patty Melt", 5.49))
        layout.addWidget(self.btn_patty_melt, 0, 3)

        # Clear Button
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(lambda: self.button_clicked_clear())
        layout.addWidget(self.btn_clear, 0,4)


    def button_clicked_clear(self):
        ## Uses the c++ function clear to clear cart
        self.logic.clear()
        self.label_total.setText(f"Total: ${self.logic.getTotal():.2f}")

    def button_clicked(self, name, price):
        # Uses the c++ function addItem to calculate the price
        self.logic.addItem(name, price)
        # Uses the c++ function getTotal to fetch price
        self.label_total.setText(f"Total: ${self.logic.getTotal():.2f}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

