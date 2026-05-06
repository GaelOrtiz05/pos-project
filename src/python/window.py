# access files
import os
import platform
from functools import partial

# access environment
import sys

from pos_logic import POSLogic

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
from datetime import datetime
# shortcuts, inputs, etc.
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QColor, QFont, QFontMetrics, QGuiApplication, QIcon, QKeySequence, QLinearGradient, QPainter, QPainterPath, QPen, QPixmap, QShortcut

# Easier access to GUI elements
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QDialog,
    
)


class ImageButton(QPushButton):
    def __init__(self, text, image_path, width, height, font, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(font)
        self.button_text = text
        self.image_path = image_path

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(22)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 120))
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        # Draw image scaled to fill
        if self.image_path and os.path.exists(self.image_path):
            pixmap = QPixmap(self.image_path)
            scaled = pixmap.scaled(
                rect.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (rect.width() - scaled.width()) // 2
            y = (rect.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)

            if self.underMouse():
                painter.fillRect(rect, QColor(0, 0, 0, 40))
            if self.isDown():
                painter.fillRect(rect, QColor(0, 0, 0, 60))
        else:
            painter.fillRect(rect, QColor("#1e1530"))

        # Draw text background at bottom
        font = self.font()
        painter.setFont(font)

        lines = self.button_text.split("\n")
        fm = QFontMetrics(font)
        line_height = fm.height()
        total_height = len(lines) * line_height

        text_box_height = 40
        text_box_y = rect.height() - text_box_height

        gradient = QLinearGradient(0, text_box_y, 0, rect.height())
        gradient.setColorAt(0, QColor("#6387d6"))
        gradient.setColorAt(1, QColor("#2563eb"))
        painter.fillRect(0, text_box_y, rect.width(), text_box_height, gradient)

        border_pen = QPen(QColor("#F6F6F6"), 1)
        painter.setPen(border_pen)
        painter.drawRect(0, text_box_y, rect.width() - 1, text_box_height - 1)

        start_y = text_box_y + (text_box_height - total_height) / 2 + fm.ascent()

        for i, line in enumerate(lines):
            text_width = fm.horizontalAdvance(line)
            x = (rect.width() - text_width) / 2
            y = start_y + i * line_height

            path = QPainterPath()
            path.addText(x, y, font, line)

            stroke_pen = QPen(QColor("black"), 2)
            stroke_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.strokePath(path, stroke_pen)
            painter.fillPath(path, QColor("white"))

        painter.end()


class MainWindow(QMainWindow, POSLogic):
    def __init__(self):
        QMainWindow.__init__(self)
        POSLogic.__init__(self)
        self.manager_feedback_message = ""
        self.current_category = 0
        self._resize_timer = None
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
        if hasattr(self, "_enter_shortcuts"):
            for shortcut in self._enter_shortcuts:
                shortcut.deleteLater()
        self._enter_shortcuts = []

    def bind_enter_key(self, handler):
        self.clear_enter_shortcuts()
        for key in [Qt.Key_Return, Qt.Key_Enter]:
            enter_shortcut = QShortcut(QKeySequence(key), self)
            enter_shortcut.activated.connect(handler)
            self._enter_shortcuts.append(enter_shortcut)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        try:
            if hasattr(self, 'grid') and self.grid is not None and hasattr(self, 'scroll') and self.scroll is not None:
                if self._resize_timer is not None:
                    self._resize_timer.stop()
                self._resize_timer = QTimer(self)
                self._resize_timer.setSingleShot(True)
                self._resize_timer.timeout.connect(lambda: self.load_grid_of_items(self.current_category))
                self._resize_timer.start(200)
        except RuntimeError:
            pass

    def show_login_screen(self):  # Login Screen
        # creating a container
        central = QWidget()
        # put the container in the main window
        self.setCentralWidget(central)
        central.setStyleSheet(
            "background-color: #ffffff;"
        )  # Chaning the background color

        # creating a grid layour inside the container
        layout = QGridLayout(central)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # PUTTING EVERYTHING IN THE MIDDLE/CENTER
        layout.setHorizontalSpacing(14)
        layout.setVerticalSpacing(14)

        # now making a label
        pos_label = self.create_label("Point of Sale System", "#111827", 300, 50)
        pos_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        user_label = self.create_label("Username", "#111827", 150, 50)
        pass_label = self.create_label("Password", "#111827", 150, 50)

        layout.addWidget(pos_label, 0, 0, 2, 2)
        layout.addWidget(user_label, 2, 0)
        layout.addWidget(pass_label, 3, 0)

        # QLineEdit() = Text Input
        user_input = QLineEdit()
        user_input.setMaximumSize(150, 50)
        layout.addWidget(user_input, 2, 1)
        user_input.setStyleSheet(
            "background-color: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 18px; color: #111827; padding: 6px;"
        )

        password_input = QLineEdit()
        password_input.setMaximumSize(150, 50)
        password_input.setEchoMode(QLineEdit.EchoMode.Password)  # ***
        layout.addWidget(password_input, 3, 1)
        password_input.setStyleSheet(
            "background-color: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 18px; color: #111827; padding: 6px;"
        )

        # QPushButton() = Button
        login_button_label = "Login"
        is_first_time = len(self.logic.getListOfUsers()) == 0
        confirm_password_input = None

        if is_first_time:
            login_button_label = "Register"

            confirm_label = self.create_label("Confirm", "#111827", 150, 50)
            layout.addWidget(confirm_label, 4, 0)

            confirm_password_input = QLineEdit()
            confirm_password_input.setMaximumSize(150, 50)
            confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addWidget(confirm_password_input, 4, 1)
            confirm_password_input.setStyleSheet(
                "background-color: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 18px; color: #111827; padding: 6px;"
            )

            first_time_label = QLabel("will become the admin account.")
            first_time_label.setFixedSize(300, 50)
            first_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            first_time_label.setStyleSheet(
                "background-color: transparent; border-radius: 1px; font-size: 14px; color: #6b7280;"
            )
            layout.addWidget(first_time_label, 7, 0, 1, 2)

        if is_first_time:
            button_row = 5
        else:
            button_row = 4

        login_button = self.create_button(login_button_label, "#2563eb", 300, 50)
        layout.addWidget(login_button, button_row, 0, 1, 2)

        quit_button = self.create_button("Quit", "#2563eb", 300, 50)
        quit_row = button_row + 1
        layout.addWidget(quit_button, quit_row, 0, 1, 2)

        login_button.clicked.connect(
            lambda: self.login_event_handler(
                user_input, password_input, layout, confirm_password_input
            )
        )
        quit_button.clicked.connect(lambda: self.close_program())

        self.bind_enter_key(
            lambda: self.login_event_handler(
                user_input, password_input, layout, confirm_password_input
            )
        )



    def show_home_screen(self):  # Main UI
        home_widget = QWidget()
        self.setCentralWidget(home_widget)
        home_widget.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f8fafc, stop:1 #e2e8f0);")

        main_layout = QVBoxLayout(home_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Row for the categories
        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        all_items_button = self.create_button("All", "#2563eb", 150, 50)
        all_items_button.clicked.connect(lambda: self.load_grid_of_items(0))

        entrees_button = self.create_button("Entrées", "#2563eb", 150, 50)
        entrees_button.clicked.connect(lambda: self.load_grid_of_items(1))

        sides_button = self.create_button("Sides", "#2563eb", 150, 50)
        sides_button.clicked.connect(lambda: self.load_grid_of_items(2))

        desserts_button = self.create_button("Desserts", "#2563eb", 150, 50)
        desserts_button.clicked.connect(lambda: self.load_grid_of_items(3))

        drinks_button = self.create_button("Drinks", "#2563eb", 150, 50)
        drinks_button.clicked.connect(lambda: self.load_grid_of_items(4))

        if self.current_user.isAdmin:
            manager_button = self.create_button("Manager", "#2563eb", 150, 50)

        logout_button = self.create_button("Logout", "#f3f4f6", 150, 50)

        for button in (
            [
                all_items_button,
                entrees_button,
                sides_button,
                desserts_button,
                drinks_button,
            ]
            + ([manager_button] if self.current_user.isAdmin else [])
            + [logout_button]
        ):
            top_row.addWidget(button)

        top_row.setAlignment(Qt.AlignmentFlag.AlignCenter)  # centering the buttons

        # Disp username
        user_label = self.create_label(
            f"Logged in as: {self.current_user.name}", "#111827", 500, 50
        )

        top_row.addStretch()
        top_row.addWidget(user_label)
        main_layout.addLayout(top_row)

        combo_row = QHBoxLayout()
        combo_row.setSpacing(20)

        # Displays Combo Buttons
        list_of_combos = self.data.getCombos()
        for combo in list_of_combos:
            button = self.create_button(f"{combo.name}", "#f3f4f6", 260, 120)
            button.setStyleSheet("QPushButton {background-color: #f3f4f6; color: #111827; border: 1px solid #e5e7eb; border-radius: 6px; padding: 8px; font-size: 18px; font-weight: 600;} QPushButton:hover {background-color: #e5e7eb; color: #0066ff;} QPushButton:pressed {background-color: #dbeafe; padding-top: 10px;}")
            button.clicked.connect(lambda _, c=combo: self.confirm_combo(c))
            combo_row.addWidget(button)

        combo_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(combo_row)

        # ------------------------------------------------------------------------------------------
        # Scroll Box - main combo items will be here
        scroll = QScrollArea()
        self.scroll = scroll
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea {background-color: transparent; border: none;} QScrollBar:vertical {width: 8px; background: transparent;} QScrollBar::handle:vertical {background: #d1d5db; border-radius: 4px;}"
        )

        container = QWidget()
        container.setStyleSheet("background-color: transparent;")

        self.grid = QGridLayout(container)
        self.grid.setSpacing(12)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grid.setContentsMargins(15, 15, 15, 15)

        # Prevent rows/columns from stretching to fill empty space
        for i in range(10):
            self.grid.setRowStretch(i, 0)
            self.grid.setColumnStretch(i, 0)

        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # load grid with all items after layout is calculated
        scroll.setWidget(container)
        QTimer.singleShot(0, lambda: self.load_grid_of_items(0))

        # Bottom section (items + cart)
        # -----------------------------------------------------------------------------------------
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        # LEFT SIDE (scroll box)
        bottom_row.addWidget(scroll, 2)

        # RIGHT SIDE (cart panel)
        cart_widget = QWidget()
        self.cart_layout = QVBoxLayout(cart_widget)
        self.cart_layout.setContentsMargins(14, 14, 14, 14)
        self.cart_layout.setSpacing(12)

        cart_widget.setFixedWidth(500)
        cart_widget.setStyleSheet(
            "background-color: #f9fafb; border-radius: 10px; border: 1px solid #e5e7eb;")

        # cart title
        cart_title = QLabel("Current Sale")
        cart_title.setFixedHeight(45)
        cart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cart_title.setFont(self.create_font(20, 600))
        cart_title.setStyleSheet("background-color: transparent; color: #111827; border: none; font-size: 20px; font-weight: 600;")

        self.cart_layout.addWidget(cart_title)

        # scroll wheel to handle more items
        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setStyleSheet("QScrollArea {background-color: white; border: 1px solid #e5e7eb; border-radius: 6px;} QScrollBar:vertical {width: 8px; background: transparent;} QScrollBar::handle:vertical {background: #d1d5db; border-radius: 4px;}")

        self.cart_container = QWidget()
        self.cart_container.setStyleSheet("background-color: white;")

        self.cart_items_layout = QVBoxLayout(self.cart_container)
        self.cart_items_layout.setContentsMargins(10, 10, 10, 10)
        self.cart_items_layout.setSpacing(8)
        self.cart_items_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.cart_scroll.setMinimumHeight(350)
        self.cart_scroll.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.cart_scroll.setWidget(self.cart_container)
        self.cart_layout.addWidget(self.cart_scroll, 1)
        self.cart_layout.addStretch()

        # footer with persistent total + checkout action
        footer_widget = QWidget()
        footer_widget.setStyleSheet("background-color: transparent;")

        footer_layout = QVBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(10)

        self.total_label = QLabel("Total: $0.00")
        self.total_label.setFixedHeight(52)
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_label.setFont(self.create_font(22, 600))
        self.total_label.setStyleSheet("background-color: #f3f4f6; color: #111827; border: 1px solid #e5e7eb; border-radius: 6px; font-weight: 600;")

        checkout_button = self.create_button("Checkout", "#0066ff", 320, 70)
        checkout_button.clicked.connect(self.checkout)
        footer_layout.addWidget(self.total_label)
        footer_layout.addWidget(checkout_button, alignment=Qt.AlignmentFlag.AlignCenter)

        footer_widget.setFixedHeight(150)
        self.cart_layout.addWidget(footer_widget)

        bottom_row.addWidget(cart_widget, 1)  # smaller than scroll

        # add the scroll and cart to main layout
        main_layout.addLayout(bottom_row)

        # Logout button functionality
        logout_button.clicked.connect(self.show_login_screen)

        if self.current_user.isAdmin:
            manager_button.clicked.connect(lambda: self.manager_event_handler())

        self.update_cart()  # to update cart each time we go back to home screen, so it doesn't show old items after purchase
    # manager functions
    def show_manager_menu(self):  # Admins

        manager_ui = QWidget()
        self.setCentralWidget(manager_ui)
        manager_ui.setStyleSheet("background-color: #f9fafb;")
        layout = QGridLayout(manager_ui)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(22)

        title = QLabel("Manager menu")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(self.create_font(30, 700))
        title.setStyleSheet(
            "color: white; background: transparent; margin-bottom: 10px;"
        )
        layout.addWidget(title, 0, 0, 1, 2)

        # View employees button
        view_employees_button = self.create_button(
            "View Employees", "#2563eb", 320, 100
        )
        layout.addWidget(view_employees_button, 2, 0)
        view_employees_button.clicked.connect(self.show_view_employees_screen)
        # View sales button
        view_sales_button = self.create_button("View Sales", "#2563eb", 320, 100)
        layout.addWidget(view_sales_button, 2, 1)
        view_sales_button.clicked.connect(self.display_sales_menu)
        # Manager inventory button
        manage_inventory_button = self.create_button("Manage Inventory", "#2563eb", 660, 100)
        manage_inventory_button.clicked.connect(self.display_manage_inventory_menu)
        layout.addWidget(manage_inventory_button, 3, 0, 1, 2)

        if self.manager_feedback_message:
            feedback_label = QLabel(self.manager_feedback_message)
            feedback_label.setFixedSize(660, 50)
            feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            feedback_label.setFont(self.create_font(15, 600))
            feedback_label.setStyleSheet("color: white; font-size: 15px; background-color: #0c401a; border-radius: 14px; padding: 8px;")
            layout.addWidget(
                feedback_label, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
            )
            self.manager_feedback_message = ""

        # Back Button
        back_button = self.create_button("Return", "2563eb", 660, 75)
        layout.addWidget(back_button, 5, 0, 1, 2)
        back_button.clicked.connect(self.show_home_screen)

    def show_view_employees_screen(self):
        employees_ui = QWidget()
        self.setCentralWidget(employees_ui)
        employees_ui.setStyleSheet("background-color: #f9fafb;")

        main_layout = QVBoxLayout(employees_ui)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = self.create_label("Employees", "", 400, 50)
        title.setFont(self.create_font(25))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: #f9fafb; border: none;")

        container = QWidget()
        list_layout = QVBoxLayout(container)
        list_layout.setSpacing(10)

        self.users = self.logic.getListOfUsers()
        for user in self.users:
            if user.role == 2:
                role = "Owner"
            elif user.role == 1:
                role = "Admin"
            else:
                role = "Employee"
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(8)

            user_label = self.create_label(f"{user.name} ({role})", "#f9fafb", 500, 50)
            user_label.setStyleSheet("background-color: #2563eb; color: white; border-radius: 8px; padding: 10px; font-size: 18px; font-weight: 600;")
            row_layout.addWidget(user_label)

            if self.current_user.role > user.role and user.id != self.current_user.id:
                remove_button = self.create_button("x", "red", 40, 40)
                remove_button.clicked.connect(
                    lambda _, n=user.name: self.confirm_remove_employee(n)
                )
                row_layout.addWidget(remove_button)

            list_layout.addWidget(row_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        list_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        add_button = self.create_button("Add Employee", "#2563eb", 300, 50)
        add_button.clicked.connect(self.show_add_employee_screen)
        main_layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignCenter)

        back_button = self.create_button("Back", "#2563eb", 300, 50)
        back_button.clicked.connect(self.show_manager_menu)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def confirm_remove_employee(self, name):
        confirm_ui = QWidget()
        self.setCentralWidget(confirm_ui)
        confirm_ui.setStyleSheet("background-color: black;")

        outer_layout = QVBoxLayout(confirm_ui)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addStretch()

        card = QWidget()
        card.setFixedSize(650, 260)
        card.setStyleSheet("background-color: #1f1f1f; border-radius: 14px;")
        card_layout = QGridLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setHorizontalSpacing(16)
        card_layout.setVerticalSpacing(16)

        title = self.create_label(f"Remove {name}?", "", 360, 44)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(self.create_font(20, 600))
        card_layout.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        confirm_button = self.create_button("Confirm", "green", 220, 48)
        confirm_button.clicked.connect(lambda: self.view_remove_employee_handler(name))
        card_layout.addWidget(
            confirm_button, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )

        back_button = self.create_button("Back", "red", 220, 48)
        back_button.clicked.connect(self.show_view_employees_screen)
        card_layout.addWidget(back_button, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        outer_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout.addStretch()

    def show_add_employee_screen(self):  # Add employee
        add_ui = QWidget()
        self.setCentralWidget(add_ui)
        add_ui.setStyleSheet("background-color: #f9fafb;")

        layout = QGridLayout(add_ui)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(18)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = self.create_label("Add Employee", "#111827", 400, 50)
        title.setFont(self.create_font(25))

        # Username
        user_label = self.create_label("Username:", "#111827", 140, 40)
        user_input = QLineEdit()
        user_input.setFixedSize(260, 40)
        user_input.setStyleSheet(
            "font-size: 18px; border-radius: 15px; background-color: white; color: black; padding-left: 12px;"
        )

        # Password
        pass_label = self.create_label("Password:", "#111827", 140, 40)
        pass_input = QLineEdit()
        pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        pass_input.setFixedSize(260, 40)
        pass_input.setStyleSheet(
            "font-size: 18px; border-radius: 15px; background-color: white; color: black; padding-left: 12px;"
        )

        # Checkbox
        checkbox = QCheckBox("Admin")
        checkbox.setStyleSheet("color: #2563eb; font-size: 18px;")

        # Buttons
        submit_button = self.create_button("Add User", "#2563eb", 300, 50)
        submit_button.clicked.connect(
            lambda: self.submit_event_handler(user_input, pass_input, checkbox)
        )

        self.bind_enter_key(
            lambda: self.submit_event_handler(user_input, pass_input, checkbox)
        )

        back_button = self.create_button("Back", "#2563eb", 300, 50)
        back_button.clicked.connect(self.show_view_employees_screen)

        # Feedback
        self.add_employee_feedback = QLabel("")
        self.add_employee_feedback.setFixedSize(360, 45)
        self.add_employee_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_employee_feedback.setWordWrap(True)
        self.add_employee_feedback.setStyleSheet(
        "color: #111827; font-size: 18px; background-color: transparent; font-weight: 600;"
        )

        # Layout
        layout.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(user_label, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(user_input, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(pass_label, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(pass_input, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(checkbox, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(
            submit_button, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            back_button, 5, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.add_employee_feedback,
            6,
            0,
            1,
            2,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

    # Loads main grid with items from the items table based on category_id
    # Category 0 = all, 1 = entre, 2 = sides, 3 = dessert, 4 = drinks
    def load_grid_of_items(self, category=0):
        for item in reversed(range(self.grid.count())):
            widget = self.grid.takeAt(item).widget()
            if widget:
                widget.deleteLater()
        list_buttons = []
        self.list_of_items = self.data.getItems()
        # create buttons
        for idx, item in enumerate(self.list_of_items):
            # check if item is available
            if self.data.Check_Stock(item.id) == True:
                image_path = item.image

                if image_path and not os.path.isabs(image_path):
                    image_path = os.path.join(BASE_DIR, image_path)

                button = self.create_button(
                    f"{item.name}", "#f3f4f6", 210, 210, image_path
                )  # clicable

                button.setStyleSheet(
                    "QPushButton {background-color: #f3f4f6; color: #111827; border: 1px solid #e5e7eb; border-radius: 6px; padding: 8px; font-size: 15px; font-weight: 600;} QPushButton:hover {background-color: #e5e7eb; color: #0066ff;} QPushButton:pressed {background-color: #dbeafe; padding-top: 10px;}")
                button.clicked.connect(
                    lambda _, x=item: self.display_item_ingredients_menu(x))
            else:
                button = self.create_button(
                    f"{item.name}\n(Unavailable)", "#e5e7eb", 150, 150)

                button.setStyleSheet("QPushButton {background-color: #e5e7eb; color: #9ca3af; border: 1px solid #e5e7eb; border-radius: 6px; padding: 8px; font-size: 15px; font-weight: 600;}")
                button.setEnabled(False)  # cant click

            list_buttons.append(button)

        self.current_category = category

        # Calculate columns dynamically based on available scroll width
        button_width = 210
        spacing = 12
        margins = 30
        if hasattr(self, 'scroll') and self.scroll is not None:
            scroll_width = self.scroll.viewport().width()
            if scroll_width < 200:
                # Fallback before layout is fully processed
                scroll_width = max(200, self.width() - 580)
            available_width = scroll_width - margins
        else:
            available_width = max(200, self.width() - 580)

        max_cols = max(1, int((available_width + spacing) / (button_width + spacing)))

        grid_row = 0
        grid_col = 0

        # place buttons
        for idx, item in enumerate(self.list_of_items):
            if item.categoryId == category or category == 0:
                if grid_col < max_cols:
                    self.grid.addWidget(list_buttons[idx], grid_row, grid_col)
                    grid_col += 1
                else:
                    grid_col = 0
                    grid_row += 1
                    self.grid.addWidget(list_buttons[idx], grid_row, grid_col)
                    grid_col += 1

    def clear_cart(self):
        if self.cart_items_layout is not None:
            while self.cart_items_layout.count():
                item = self.cart_items_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()

    # adds item to the cart display.
    def update_cart(self):

        try:
            self.clear_cart()

            for index, item in enumerate(self.cart):
                display = self.get_cart_display_text(item)

                row_widget = QWidget()
                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(0, 0, 0, 0)
                row_layout.setSpacing(8)

                label = QLabel(display)
                label.setMinimumHeight(60)
                label.setMaximumHeight(100)
                label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                label.setFont(self.create_font(18))
                label.setStyleSheet(
                    "background-color: #0066ff; color: white; border: 1px solid #374151; border-radius: 10px; padding: 8px;")

                remove_button = self.create_button("x", "#2563eb", 40, 40)
                remove_button.clicked.connect(partial(self.remove_from_checkout_tables, item["checkoutID"]))

                row_layout.addWidget(label, 1)
                row_layout.addWidget(remove_button)

                self.cart_items_layout.addWidget(row_widget)

            if len(self.cart) == 0:
                empty_label = QLabel("No items in cart")
                empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                empty_label.setFont(self.create_font(16))
                empty_label.setStyleSheet("background-color: transparent; color: #0066ff;")
                self.cart_items_layout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignCenter)

            total = self.calculate_cart_total()
            self.total_label.setText(f"Total: ${total:.2f}")
        except RuntimeError as e:
            print(f"RuntimeError in update_cart: {e}")
        

    def display_sales_menu(self):
        sales_ui = QWidget()
        self.setCentralWidget(sales_ui)
        sales_ui.setStyleSheet("background-color: #f9fafb;")
        layout = QGridLayout(sales_ui)
        layout.setSpacing(22)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel("View Sales")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(self.create_font(30, 700))
        title.setStyleSheet(
            "color: white; background: transparent; margin-bottom: 10px;"
        )
        layout.addWidget(title, 0, 0, 1, 2)

        # Add employee Button
        todays_sales = self.create_button("Sale Today", "#2563eb", 350, 100)
        todays_sales.clicked.connect(lambda: self.display_sales(1))
        layout.addWidget(todays_sales, 2, 0)
        weekly_sales = self.create_button("Sale This Week", "#2563eb", 350, 100)
        weekly_sales.clicked.connect(lambda: self.display_sales(2))
        layout.addWidget(weekly_sales, 2, 1)
        all_sales = self.create_button("All Sales", "#2563eb", 350, 100)
        all_sales.clicked.connect(lambda: self.display_sales(3))
        layout.addWidget(all_sales, 3, 0)

        back_button = self.create_button("Back", "2563eb", 350, 100)
        back_button.clicked.connect(self.show_manager_menu)
        layout.addWidget(back_button, 3, 1)

    def display_sales(self, choice):  # choice will be 1 2 or 3
        # TITLE AND STUFF
        sales_ui = QWidget()
        self.setCentralWidget(sales_ui)
        sales_ui.setStyleSheet("background-color: #f9fafb;")
        layout = QGridLayout(sales_ui)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(22)
        # titles
        title = QLabel("Sale History")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(self.create_font(30, 700))
        title.setStyleSheet(
            "color: white; background: transparent; margin-bottom: 10px;"
        )
        # LOGIC INFO AND SMALL GUI
        sales_info = self.get_sales(choice)
        sales_text = sales_info[0]
        total = sales_info[1]
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(12)
        container_layout.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedSize(800, 800)
        scroll.setStyleSheet("QScrollArea{ border: none; background: transparent;}")
        orders = sales_text.split("Order #")
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(12)
        container_layout.setContentsMargins(0, 0, 0, 0)
        # Loop to seprate orders.
        for order in orders:
            if order.strip() == "":
                continue
            order = "Order #" + order
            label = QLabel(order)
            label.setWordWrap(True)
            label.setFont(self.create_font(17, 500))
            label.setAlignment(Qt.AlignmentFlag.AlignTop)
            label.setStyleSheet("color: black; background-color: #f9fafb; border: 1px solid #2f2750; border-radius: 18px; padding: 18px 16px; font-size: 17px;")
            container_layout.addWidget(label)
        container_layout.setSpacing(16)
        scroll.setWidget(container)
        total_sales_label = self.create_label(
            f"Total Sale $:{total:.2f} ", "black", 800, 100
        )
        back_button = self.create_button("Back", "#0066ff", 800, 50)
        back_button.clicked.connect(self.display_sales_menu)
        # PLACing lablels
        layout.addWidget(title, 0, 0, 1, 2)
        layout.addWidget(scroll, 1, 0, 1, 2)
        layout.addWidget(total_sales_label, 2, 0, 1, 2)
        layout.addWidget(back_button, 3, 0, 1, 2)




    def display_item_ingredients_menu(self, item):
        item_ingredients_ui = QWidget()
        self.setCentralWidget(item_ingredients_ui)
        item_ingredients_ui.setStyleSheet("background-color: #f3f4f6;")

        # Outer layout fills the window, but centers a smaller card
        background_layout = QVBoxLayout(item_ingredients_ui)
        background_layout.setContentsMargins(0, 0, 0, 0)
        background_layout.addStretch()

        card = QWidget()
        card.setFixedSize(650, 400)  # make this smaller/larger as needed
        card.setStyleSheet("background-color: #0066ff; border-radius: 14px;")
        card_layout = QGridLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setHorizontalSpacing(16)
        card_layout.setVerticalSpacing(16)

        title = self.create_label(f"Customize {item.name}", "", 360, 44)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(self.create_font(20, 600))

        card_layout.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.list_of_ItemIngredients = self.data.getItemIngredients(item.id)
        
        
        ingredient_label_list = []
        ingredient_id_list = []
        minus_button_list = []
        plus_button_list = []

        current_grid_row = last_grid_row = 1
        for idx, ingredient in enumerate(self.list_of_ItemIngredients):    
            ingredient_name = self.create_label(ingredient.name,"", 100, 40)
            ingredient_name.setStyleSheet("color: white; font-size: 18px;")
            ingredient_id_list.append(ingredient.id)

            ingredient_label = self.create_label(f"x{1}","", 100, 40)
            ingredient_label.setStyleSheet("color: white; font-size: 18px;")
            ingredient_label_list.append(ingredient_label)

            minus_button = self.create_button("-", "2563eb", 60, 40)
            minus_button_list.append(minus_button)
            minus_button_list[idx].clicked.connect(lambda _, x=idx: 
                                                   [ingredient_label_list[x].setText(f"x{int(ingredient_label_list[x].text()[1:]) - 1}")] 
                                                   if int(ingredient_label_list[x].text()[1:])>0 
                                                   else None)

            plus_button = self.create_button("+", "2563eb", 60, 40)
            plus_button_list.append(plus_button)
            plus_button_list[idx].clicked.connect(lambda _, x=idx: 
                                                  [ingredient_label_list[x].setText(f"x{int(ingredient_label_list[x].text()[1:]) + 1}")] 
                                                  if int(ingredient_label_list[x].text()[1:])<2 
                                                  else None)
            
            if (ingredient.isRemovable):
                card_layout.addWidget(ingredient_name, 1 + current_grid_row, 0)
                card_layout.addWidget(ingredient_label, 1 + current_grid_row,1)                
                card_layout.addWidget(minus_button, 1 + current_grid_row,2)
                card_layout.addWidget(plus_button, 1 + current_grid_row,3) 
                current_grid_row +=1
                last_grid_row = 1 + current_grid_row
            
        confirm_button = self.create_button("Confirm", "#f3f4f6", 220, 48)
        confirm_button.clicked.connect(lambda: self.confirm_item(item,
                                                                 [int(label.text()[1:]) for label in ingredient_label_list],
                                                                 ingredient_id_list))

        card_layout.addWidget(confirm_button, last_grid_row, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        back_button = self.create_button("Back", "#f3f4f6", 220, 48)
        back_button.clicked.connect(self.show_home_screen)
        card_layout.addWidget(back_button, last_grid_row, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        background_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        background_layout.addStretch()


    def show_receipt_popup(self, receipt_text, total):
        popup = QDialog(self)
        popup.setWindowTitle("Purchase Complete")
        popup.setFixedSize(400, 500)
        popup.setStyleSheet("background-color: #f9fafb;")

        layout = QVBoxLayout(popup)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        current_date = datetime.now().strftime("%m/%d/%Y %I:%M %p")

        title = QLabel("Purchase Complete")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(self.create_font(22, 700))
        title.setStyleSheet("color: #111827; background-color: transparent;")

        date_label = QLabel(f"Date: {current_date}")
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_label.setStyleSheet("color: #374151; font-size: 16px;")

        items_label = QLabel(f"Items Purchased:\n\n{receipt_text}\nTotal: ${total:.2f}")
        items_label.setWordWrap(True)
        items_label.setStyleSheet("background-color: white; color: #111827; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; font-size: 16px;")

        close_button = self.create_button("Close", "#2563eb", 250, 50)
        close_button.clicked.connect(popup.accept)

        layout.addWidget(title)
        layout.addWidget(date_label)
        layout.addWidget(items_label)
        layout.addStretch()
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        popup.exec()

    def display_manage_inventory_menu(self):
        manage_inventory_ui = QWidget()
        self.setCentralWidget(manage_inventory_ui)
        manage_inventory_ui.setStyleSheet("background-color: #ffffff;")

        main_layout = QVBoxLayout(manage_inventory_ui)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        title = self.create_label("manage inventory", "", 450, 50)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(self.create_font(25, 600))
        title.setStyleSheet("color: #111827; background-color: transparent;")
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea {background-color: #ffffff; border: none;} QScrollBar:vertical {width: 8px; background: transparent;} QScrollBar::handle:vertical {background: #d1d5db; border-radius: 4px;}")

        container = QWidget()
        container.setStyleSheet("background-color: #ffffff;")

        list_layout = QVBoxLayout(container)
        list_layout.setContentsMargins(10, 10, 10, 10)
        list_layout.setSpacing(12)

        inventory_items = self.data.getIngredients()  # reading from cpp

        for ingredient in inventory_items:  # going through the list
            row_widget = QWidget()
            row_widget.setStyleSheet("background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px;")
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(14, 12, 14, 12)
            row_layout.setSpacing(12)

            name_label = self.create_label(f"{ingredient.name}", "#ffffff", 250, 50)
            name_label.setStyleSheet("color: #f9fafb; background-color: #2563eb; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 18px; font-weight: 600;")

            stock_label = self.create_label(f"Stock: {ingredient.stock}", "#ffffff", 160, 50)
            stock_label.setStyleSheet("color: #f9fafb; background-color: #2563eb; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 18px; font-weight: 600;")

            # text edits
            stock_input = QLineEdit()
            stock_input.setFixedSize(140, 45)
            stock_input.setStyleSheet("background-color: #ffffff; color: #111827; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 18px; padding: 6px;")

            # set button
            Increase_button = self.create_button("Increase", "#2563eb", 160, 45)
            Increase_button.clicked.connect(
                lambda _, ing=ingredient, inp=stock_input: self.update_ingredient_stock(
                    ing, inp, increase=True
                )
            )

            Decrease_button = self.create_button("Decrease", "#2563eb", 160, 45)
            Decrease_button.setStyleSheet("QPushButton {background-color: #f3f4f6; color: #111827; border: 1px solid #e5e7eb; border-radius: 6px; padding: 8px; font-size: 18px; font-weight: 600;} QPushButton:hover {background-color: #e5e7eb; color: #0066ff;} QPushButton:pressed {background-color: #dbeafe; padding-top: 10px;}")
            Decrease_button.clicked.connect(
                lambda _, ing=ingredient, inp=stock_input: self.update_ingredient_stock(
                    ing, inp, increase=False
                )
            )

            # adding items
            row_layout.addWidget(name_label)
            row_layout.addWidget(stock_label)
            row_layout.addWidget(stock_input)
            row_layout.addWidget(Increase_button)
            row_layout.addWidget(Decrease_button)

            list_layout.addWidget(row_widget)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        # back button
        back_button = self.create_button("Back", "f3f4f6", 300, 50)
        back_button.setStyleSheet("QPushButton {background-color: #f3f4f6; color: #111827; border: 1px solid #e5e7eb; border-radius: 6px; padding: 8px; font-size: 18px; font-weight: 600;} QPushButton:hover {background-color: #e5e7eb; color: #0066ff;} QPushButton:pressed {background-color: #dbeafe; padding-top: 10px;}")
        back_button.clicked.connect(self.show_manager_menu)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.inventory_feedback = self.create_label("", "transparent", 400, 40)
        self.inventory_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inventory_feedback.setStyleSheet("color: #111827; background-color: transparent; border: none; font-weight: 600;")
        self.inventory_feedback.hide()

        main_layout.addWidget(self.inventory_feedback)

    # MODULE FUNCTIONS: BUTTON, LABEL, AND FONT
    def create_font(self, point_size, weight=QFont.Weight.Normal):
        font = QFont("Inter")
        font.setPointSize(point_size)
        if isinstance(weight, int):
            weight = QFont.Weight(weight)
        font.setWeight(weight)
        return font

    def create_button(self, text, color="#2563eb", width=300, height=55, image=None):
        font = self.create_font(18, QFont.Weight.DemiBold)
        if image and os.path.exists(image):
            return ImageButton(text, image, width, height, font)

        btn = QPushButton(text)
        btn.setFixedSize(width, height)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(font)

        text_color = "white" if color == "#2563eb" else "#111827"

        btn.setStyleSheet(f"QPushButton {{background-color: {color}; color: {text_color}; border: 1px solid #e5e7eb; border-radius: 6px; padding: 8px 14px; font-size: 18px; font-weight: 600;}} QPushButton:hover {{background-color: #0052cc; color: white;}} QPushButton:pressed {{background-color: #0047b3; padding-top: 10px;}}")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 35))
        btn.setGraphicsEffect(shadow)

        return btn


    def create_label(self, text, color="white", width=300, height=55):
        label = QLabel(text)
        label.setFixedSize(width, height)
        label.setFont(self.create_font(18, QFont.Weight.Medium))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"QLabel {{background-color: transparent; color: {color}; border: none; padding: 4px; font-size: 18px;}}")

        return label
