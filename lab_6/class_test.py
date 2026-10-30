
import json
import os


class Products:
    def __init__(self, product_id, product_name, stock, price):
        self.product_id = product_id
        self.product_name = product_name
        self.stock = stock
        self.price = price

    def update_stock(self, new_stock):
        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.stock = new_stock

    def display_product(self):
        pass

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        save_inventory()  # write to inventory.json right away
        print("Product added successfully!")

    
    # Product ID (must be unique and non-empty)
    while True:
        pid = input("Product ID: ").strip().upper()
        if not pid:
            print("ID cannot be empty.")
        elif any(p["id"] == pid for p in inventory):
            print("That ID already exists.")
        else:
            break
    
    name = input("Product Name: ").strip()
 
    # Price (must be a non-negative number)
    while True:
        try:
            price = float(input("Price: "))
            if price < 0:
                raise ValueError
            break
        except ValueError:
            print("Enter a valid price (e.g. 299.99).")
 
    # Stock (must be a non-negative integer)
    while True:
        try:
            stock = int(input("Stock Quantity: "))
            if stock < 0:
                raise ValueError
            break
        except ValueError:
            print("Enter a whole number (e.g. 10).")
 
    inventory.append({"id": pid, "name": name, "price": price, "stock": stock})
    save_inventory()  # write to inventory.json right away
    print("Product added successfully!")
         
    pass

class  Main_Program:
    def __init__(self):
        self.inventory = Inventory()
        self.failed_attempts = 0
        self.total_units = 0
        self.file_handler = FileHandler()
        self.inventory = self.file_handler.load()
        self.running = True





    def print_main_menu():
    print("1. Display All Product")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")

    pass

class File_Handling:
    pass    
