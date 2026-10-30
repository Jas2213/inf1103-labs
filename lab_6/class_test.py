
import json
import os


class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, new_stock):
        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.stock = new_stock

    def to_dict(self):
        return {"id": self.product_id, "name": self.name,
                "price": self.price, "stock": self.stock}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"])

    def __str__(self):
        return (f"ID: {self.product_id} | Name: {self.name} | "
                f"Price: ${self.price:.2f} | Stock: {self.stock}")

class Inventory:
    def __init__(self):
        self.products = []

    def find(self, product_id):
        product_id = product_id.upper()
        for p in self.products:
            if p.product_id.upper() == product_id:
                return p
            return None

    def add(self, product):
        if self.find(product.product_id):
            raise ValueError("That ID already exists.")
        self.products.append(product)


    
    


class FileHandler:
    def __init__(self, filename="inventory.json"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(script_dir, filename)

    def load(self):
        """Return an Inventory loaded from disk (empty if missing/corrupt)."""
        inventory = Inventory()
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                inventory.products = [Product.from_dict(d) for d in data]
                print("Inventory loaded successfully.")
            except json.JSONDecodeError:
                print("Inventory file is corrupted. Starting empty.")
        else:
            print("No inventory file found. Starting empty.")
        return inventory

    def save(self, inventory):
        with open(self.file_path, "w") as f:
            json.dump([p.to_dict() for p in inventory.products], f, indent=4)
        print("Inventory saved.")


class MainProgram:
    def __init__(self):
        self.file_handler = FileHandler()
        self.inventory = self.file_handler.load()
        self.running = True

    # --- helper: replaces the three copy-pasted validation loops ---
    @staticmethod
    def read_number(prompt, cast, error):
        while True:
            try:
                value = cast(input(prompt))
                if value < 0:
                    raise ValueError
                return value
            except ValueError:
                print(error)

    # --- menu actions ---
    def display_all_products(self):
        if not self.inventory.products:
            print("Inventory is empty.")
            return
        print("Current Inventory")
        print("-" * 48)
        for p in self.inventory.products:
            print(p)
        print("-" * 48)

    def add_product(self):
        print("Add New Product")
        while True:
            pid = input("Product ID: ").strip().upper()
            if not pid:
                print("ID cannot be empty.")
            elif self.inventory.find(pid):
                print("That ID already exists.")
            else:
                break
        name = input("Product Name: ").strip()
        price = self.read_number("Price: ", float, "Enter a valid price (e.g. 299.99).")
        stock = self.read_number("Stock Quantity: ", int, "Enter a whole number (e.g. 10).")

        self.inventory.add(Product(pid, name, price, stock))
        self.file_handler.save(self.inventory)
        print("Product added successfully!")

    def update_stock(self):
        print("Update Stock")
        pid = input("Enter Product ID: ").strip().upper()
        product = self.inventory.find(pid)
        if product is None:
            print(f"No product found with ID '{pid}'.")
            return

        print(f"Found: {product.name} (current stock: {product.stock})")
        new_stock = self.read_number("New Stock Quantity: ", int, "Enter a whole number (e.g. 10).")
        product.update_stock(new_stock)
        self.file_handler.save(self.inventory)
        print("Stock updated successfully!")

    def search_product(self):
        print("Search Product")
        pid = input("Enter Product ID: ").strip().upper()
        product = self.inventory.find(pid)
        if product:
            print("Product found:")
            print("-" * 48)
            print(product)
            print("-" * 48)
        else:
            print(f"No product found with ID '{pid}'.")

    def save_inventory(self):
        self.file_handler.save(self.inventory)

    def quit(self):
        print("Saving Inventory before exit...")
        self.save_inventory()
        self.running = False

    def print_main_menu(self):
        print("\n1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

    def run(self):
        actions = {
            "1": self.display_all_products,
            "2": self.add_product,
            "3": self.update_stock,
            "4": self.search_product,
            "5": self.save_inventory,
            "6": self.quit,
        }
        while self.running:
            self.print_main_menu()
            choice = input("Enter option: ").strip()
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice, try again.")


if __name__ == "__main__":
    MainProgram().run()