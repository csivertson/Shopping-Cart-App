from PyQt6.QtWidgets import QApplication
from gui import ShoppingListApp

def main():
    app = QApplication([])
    window = ShoppingListApp()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
