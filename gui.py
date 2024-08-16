from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLineEdit, QMessageBox
from shopping_logic import ShoppingCart

class ShoppingListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Shopping List")
        self.cart = ShoppingCart()
        self.counters = {}  # Dictionary that stores quantity labels for all of the different items
        self.cumulative_total = 0.0  # Cumulative total to track all calculations (the bottom button)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.total_label = QLabel("Total: $0.00")
        layout.addWidget(self.total_label)

        self.cumulative_label = QLabel("Cumulative Total: $0.00")  # Label for cumulative total
        layout.addWidget(self.cumulative_label)

        # Predefined food items, that go on the groccery list
        food_items = [("Apple", 1.00), ("Banana", 0.50), ("Orange", 0.75), ("Bread", 2.50), ("Milk", 1.25)]
        self.food_buttons = []

        for food, price in food_items:
            hbox = QHBoxLayout()

            label = QLabel(f"{food} - ${price:.2f}")
            hbox.addWidget(label)

            plus_button = QPushButton("+")
            plus_button.clicked.connect(lambda _, f=food, p=price: self.add_item(f, p))
            hbox.addWidget(plus_button)

            counter_label = QLabel("0")  # Counter label which i set to 0
            self.counters[food] = counter_label  # Store reference to the counter label
            hbox.addWidget(counter_label)

            minus_button = QPushButton("-")
            minus_button.clicked.connect(lambda _, f=food: self.remove_item(f))
            hbox.addWidget(minus_button)

            layout.addLayout(hbox)
            self.food_buttons.append((label, plus_button, counter_label, minus_button))

        # tax is set to 5% but this also has discount percentage input
        self.discount_input = QLineEdit()
        self.discount_input.setPlaceholderText("Enter discount (%)")
        layout.addWidget(self.discount_input)

        calculate_button = QPushButton("Calculate Total")
        calculate_button.clicked.connect(self.calculate_total)
        layout.addWidget(calculate_button)

        reset_button = QPushButton("Reset")  # Reset button, to wipe everything fresh
        reset_button.clicked.connect(self.reset_cart)
        layout.addWidget(reset_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_item(self, food: str, price: float):
        self.cart.add_item(food, price)
        self.update_total()
        self.update_counter(food)  # Update counter label

    def remove_item(self, food: str):
        self.cart.remove_item(food)
        self.update_total()
        self.update_counter(food)  # Update counter label

    def calculate_total(self):
        try:
            discount = float(self.discount_input.text())
            if not (1 <= discount <= 100):
                raise ValueError("Discount must be between 1 and 100.")
            discount = discount / 100  # Convert to a decimal 
        except ValueError:
            self.show_error_message("Sorry, that is an invalid discount percentage. Please try again!")
            return  # Exit the method without further math

        total_with_tax = self.cart.calculate_total(discount=discount)
        
        # Add to cumulative total
        self.cumulative_total += total_with_tax
        self.cumulative_label.setText(f"Cumulative Total: ${self.cumulative_total:.2f}")

        # Reset current total
        self.cart.clear_cart()
        self.update_total()

        # Reset counters
        for counter_label in self.counters.values():
            counter_label.setText("0")

    def update_total(self):
        total = self.cart.calculate_total()
        self.total_label.setText(f"Total: ${total:.2f}")

    def update_counter(self, food: str):
        """Updates the quantity counter for the specified food item."""
        quantity = self.cart.get_quantity(food)
        self.counters[food].setText(str(quantity))

    def reset_cart(self):
        self.cart.clear_cart()  # Clears the cart
        self.cumulative_total = 0.0  # Resets cumulative total
        self.update_total()  # Reset total label
        self.cumulative_label.setText("Cumulative Total: $0.00")
        
        # Reset all counters to 0
        for counter_label in self.counters.values():
            counter_label.setText("0")

    def show_error_message(self, message: str):
        """Displays an error message in a pop-up dialog."""
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setWindowTitle("Invalid Input")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_dialog.exec()

