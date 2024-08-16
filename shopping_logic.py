class ShoppingCart:
    TAX_RATE = 0.05  # 5% tax, doesnt change it stays at 5%

    def __init__(self):
        self.items = {}

    def add_item(self, item: str, price: float):
        if item in self.items:
            self.items[item]['quantity'] += 1
        else:
            self.items[item] = {'price': price, 'quantity': 1}

    def remove_item(self, item: str):
        if item in self.items and self.items[item]['quantity'] > 0:
            self.items[item]['quantity'] -= 1
            if self.items[item]['quantity'] == 0:
                del self.items[item]

    def calculate_total(self, discount: float = 0.0) -> float:
        total = sum(item['price'] * item['quantity'] for item in self.items.values())
        total *= (1 + self.TAX_RATE)
        total *= (1 - discount)
        return total

    def get_quantity(self, item: str) -> int:
        """Returns the quantity of the given item in the cart."""
        if item in self.items:
            return self.items[item]['quantity']
        return 0

    def clear_cart(self):
        """Clears all items from the cart."""
        self.items.clear()
