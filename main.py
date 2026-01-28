import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
import fast_logic  # THIS IS YOUR C++ CODE!

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("C++ & Python Bridge")
        
        # Setup UI Elements
        self.layout = QVBoxLayout()
        self.input_a = QLineEdit(placeholderText="Number A")
        self.input_b = QLineEdit(placeholderText="Number B")
        self.btn = QPushButton("Calculate in C++")
        self.result_label = QLabel("Result will appear here")

        # Connect button to C++ function
        self.btn.clicked.connect(self.run_calculation)

        # Add to screen
        self.layout.addWidget(self.input_a)
        self.layout.addWidget(self.input_b)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.result_label)
        self.setLayout(self.layout)

    def run_calculation(self):
        # Get numbers from UI, send to C++, and show result
        val_a = int(self.input_a.text())
        val_b = int(self.input_b.text())
        
        answer = fast_logic.add(val_a, val_b) # Calling C++!
        self.result_label.setText(f"C++ says the answer is: {answer}")

app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec())
