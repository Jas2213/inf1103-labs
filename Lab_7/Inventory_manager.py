import json
import os
from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    @abstractmethod
    def get_fulfilment_info(self):
        pass    

    def update_stock(self, new_stock):
        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.stock = new_stock

    def to_dict(self):
        return {"id": self.product_id, "name": self.name,
                "price": self.price, "stock": self.stock}
    
    def display_information(self):
            return f"Product Information: ID: {self.product_id}, Name: {self.name}, Price: ${self.price:.2f}, Stock: {self.stock}"
    
    @classmethod
    def from_dict(cls, data):
        # Factory method: inspects dictionary keys to instantiate the correct subclass
        if "weight" in data:
            return PhysicalProduct.from_dict(data)
        elif "download_size" in data:
            return DigitalProduct.from_dict(data)
        raise ValueError("Unknown product type in data dictionary.")


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass  
    

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.weight = weight
    
    def calculate_shipping_cost(self):
        # 10 dollar per kg
        return self.weight * 10  
    
    def get_fulfilment_info(self):
        return f"This product requires physical shipping. Weight: {self.weight}kg"

    def display_information(self):
        return super().display_information() + f", Weight: {self.weight}kg"
    def to_dict(self):
        data = super().to_dict()          # reuse the parent's dictionary
        data["weight"] = self.weight      # add the extra field
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], data.get("weight", 0))
    
class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.file_size = download_size

    def to_dict(self):
        data = super().to_dict()          # reuse the parent's dictionary
        data["download_size"] = self.file_size      # add the extra field
        return data
    def get_fulfilment_info(self):
            return f"This product is delivered digitally. File Size: {self.file_size}MB"
    
    def display_information(self):
            return super().display_information() + f", File Size: {self.file_size}MB" 
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], data.get("download_size", 0))

    
    



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
            if isinstance(p, PhysicalProduct):
                print(f"Physical Product: {p.display_information()}")
            elif isinstance(p, DigitalProduct):
                print(f"Digital Product: {p.display_information()}")
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
        print("Select Product Type:")
        print("1. Physical Product")
        print("2. Digital Product")
        while True:
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice == "1":
                product_type = "physical"
                break
            elif choice == "2":
                product_type = "digital"
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        name = input("Product Name: ").strip()
        price = self.read_number("Price: ", float, "Enter a valid price (e.g. 299.99).")
        stock = self.read_number("Stock Quantity: ", int, "Enter a whole number (e.g. 10).")

        if product_type == "physical":
            weight = self.read_number("Weight: ", float, "Enter a valid weight (e.g. 1.5).")
            self.inventory.add(PhysicalProduct(pid, name, price, stock, weight))
        else:
            download_size = self.read_number("Download Size (MB): ", float, "Enter a valid size (e.g. 100.5).")
            self.inventory.add(DigitalProduct(pid, name, price, stock, download_size))
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