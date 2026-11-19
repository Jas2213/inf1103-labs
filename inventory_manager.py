from __future__ import annotations
import json
import os
from abc import ABC, abstractmethod

from collections.abc import Callable

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> str:
        return (f"Supplier Information: ID: {self.supplier_id}, Name: {self.name}, "
                f"Contact Email: {self.contact_email}")

    def to_dict(self) -> dict:
        return {"supplier_id": self.supplier_id, "name": self.name,
                "contact_email": self.contact_email}

    @classmethod
    def from_dict(cls, data: dict) -> Supplier:
        return cls(data["supplier_id"], data["name"], data["contact_email"])

class DiscountStrategy(ABC):
    

    @abstractmethod
    def apply(self, total, float) -> float:
        pass
class NoDiscount(DiscountStrategy):
    def apply(self,total,float) -> float:
        return total
    
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        self.percentage: float = percentage
    def apply (self, total, float ) -> float:
        return total * (1 - self.percentage/100)
    

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        self.threshold: float = threshold
        self.amount: float = amount
    def apply(self, total: float) -> float:
        return total - self.amount if total >= self.threshold else total

class StudentDiscount(DiscountStrategy):
    def __init__(self, percentage: float = 5) -> None:
        self.percentage: float = percentage
    def apply (self, total, float) -> float:
        return total * (1 - self.percentage/100)

        
class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self.product_id: str = product_id
        self.name: str = name
        self.price: float = price
        self.stock: int = stock
        self.supplier: Supplier = supplier

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass    

    def update_stock(self, new_stock: int) -> None:
        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.stock = new_stock

    def to_dict(self) -> dict:
        return {"id": self.product_id, "name": self.name,
                "price": self.price, "stock": self.stock,
                "supplier": self.supplier.to_dict()}
    
    def display_information(self) -> str:
            return f"Product Information: ID: {self.product_id}, Name: {self.name}, Price: ${self.price:.2f}, Stock: {self.stock}"
    
    @classmethod
    def from_dict(cls, data: dict) -> Product:
        
        if "weight" in data:
            return PhysicalProduct.from_dict(data)
        elif "download_size" in data:
            return DigitalProduct.from_dict(data)
        raise ValueError("Unknown product type in data dictionary.")


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass
    
class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.weight: float = weight

    def calculate_shipping_cost(self) -> float:
        # 10 dollar per kg
        return self.weight * 10

    def get_fulfilment_info(self) -> str:
        return f"This product requires physical shipping. Weight: {self.weight}kg"

    def display_information(self) -> str:
        return ("Physical Product: " + super().display_information()
                + f", Weight: {self.weight}kg, Shipping Cost: ${self.calculate_shipping_cost():.2f}"
                + f", {self.supplier.display_information()}")

    def to_dict(self) -> dict:
        data = super().to_dict()          # reuse the parent's dictionary
        data["weight"] = self.weight      # add the extra field
        return data

    @classmethod
    def from_dict(cls, data: dict) -> PhysicalProduct:
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   data.get("weight", 0), Supplier.from_dict(data["supplier"]))
    
class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.file_size: float = download_size

    def to_dict(self) -> dict:
        data = super().to_dict()          # reuse the parent's dictionary
        data["download_size"] = self.file_size      # add the extra field
        return data
    def get_fulfilment_info(self) -> str:
            return f"This product is delivered digitally. File Size: {self.file_size}MB"

    def display_information(self) -> str:
            return ("Digital Product: " + super().display_information()
                    + f", File Size: {self.file_size}MB, {self.supplier.display_information()}")

    @classmethod
    def from_dict(cls, data: dict) -> DigitalProduct:
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   data.get("download_size", 0), Supplier.from_dict(data["supplier"]))

class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def add_order(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)
    
class Inventory:
    def __init__(self) -> None:
        self.products: list[Product] = []

    def find_product(self, product_id: str) -> Product | None:
        product_id = product_id.upper()
        for p in self.products:
            if p.product_id.upper() == product_id:
                return p
        return None

    def add_product(self, product: Product) -> None:
        if self.find_product(product.product_id):
            raise ValueError("That ID already exists.")
        self.products.append(product)

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product:
            self.products.remove(product)
            return True
        return False
    def display_all_products(self) -> None:
        if not self.products:
            print("Inventory is empty.")
            return
        print("Current Inventory")
        print("-" * 48)
        for product in self.products:
            print(product.display_information())
        print("-" * 48)

class FileHandler:
    def __init__(self, filename:str ="inventory.json") -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path: str = os.path.join(script_dir, filename)

    def load(self) -> Inventory:
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

    def save(self, inventory: Inventory) -> None:
        with open(self.file_path, "w") as f:
            json.dump([p.to_dict() for p in inventory.products], f, indent=4)
        print("Inventory saved.")


class MainProgram:
    def __init__(self) -> None:
        self.file_handler: FileHandler = FileHandler()
        self.inventory: Inventory = self.file_handler.load()
        self.running: bool = True

    
    @staticmethod
    def read_number(prompt: str, cast: Callable[[str], float], error: str) -> float:
        while True:
            try:
                value = cast(input(prompt))
                if value < 0:
                    raise ValueError
                return value
            except ValueError:
                print(error)

    # --- menu actions ---
    def display_all_products(self) -> None:
        self.inventory.display_all_products()

    def add_product(self) -> None:
        print("Add New Product")
        while True:
            pid = input("Product ID: ").strip().upper()
            if not pid:
                print("ID cannot be empty.")
            elif self.inventory.find_product(pid):
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
        supplier_id = input("Supplier ID: ").strip()
        supplier_name = input("Supplier Name: ").strip()
        supplier_email = input("Supplier Contact Email: ").strip()
        supplier = Supplier(supplier_id, supplier_name, supplier_email)
        if product_type == "physical":
            weight = self.read_number("Weight: ", float, "Enter a valid weight (e.g. 1.5).")
            self.inventory.add_product(PhysicalProduct(pid, name, price, stock, weight, supplier))
        else:
            download_size = self.read_number("Download Size (MB): ", float, "Enter a valid size (e.g. 100.5).")
            self.inventory.add_product(DigitalProduct(pid, name, price, stock, download_size, supplier))
        self.file_handler.save(self.inventory)
        print("Product added successfully!")

    def update_stock(self) -> None:
        print("Update Stock")
        pid = input("Enter Product ID: ").strip().upper()
        product = self.inventory.find_product(pid)
        if product is None:
            print(f"No product found with ID '{pid}'.")
            return

        print(f"Found: {product.name} (current stock: {product.stock})")
        new_stock = self.read_number("New Stock Quantity: ", int, "Enter a whole number (e.g. 10).")
        product.update_stock(new_stock)
        self.file_handler.save(self.inventory)
        print("Stock updated successfully!")

    def search_product(self) -> None:
        print("Search Product")
        pid = input("Enter Product ID: ").strip().upper()
        product = self.inventory.find_product(pid)
        if product:
            print("Product found:")
            print("-" * 48)
            print(product.display_information())
            print("-" * 48)
        else:
            print(f"No product found with ID '{pid}'.")

    def save_inventory(self) -> None:
        self.file_handler.save(self.inventory)

    def quit(self) -> None:
        print("Saving Inventory before exit...")
        self.save_inventory()
        self.running = False

    def print_main_menu(self) -> None:
        print("\n1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

    def run(self) -> None:
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