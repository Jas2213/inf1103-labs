print("Hello World")
inventory = []          # list of [order_id, product_name, quantity]
transactions = []       # list of [order_id, product_name, quantity, running_total, tax]
total_inventory = 0
failed_entries = 0
next_order_id = 1001
import json
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "orders.txt")

#Check whether inventory.json exists. Create
 
# load_inventory() to load
# inventory.json if it exists.
 
# Otherwise, begin with an empty inventory.
 
# Create
# save_inventory() and save data to inventory.json.
user_data = {
    "ID": "P01",
    "Product Name": "Widget",
   "Price": 19.99,
    "Stock": 100,
}


def load_inventory():
    """Load inventory.json into the global list, or start empty."""
    global inventory
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, "r") as f:
                inventory = json.load(f)
            print("inventory.json found. Inventory loaded successfully.")
            return
        except json.JSONDecodeError:
            print("inventory.json is corrupted. Starting empty.")
    else:
        print("No inventory file found. Starting with an empty inventory.")
    inventory = []


def save_inventory():
    """Write the global list to inventory.json."""
    with open(file_path, "w") as f:
        json.dump(inventory, f, indent=4)
    print("Inventory saved to inventory.json")

def get_valid_input(userinput, failed_entries, total_inventory):
    if userinput.lower() == "quit":
        return True, False, 0, failed_entries

    if not userinput.isdigit():
        print("Please input a valid positive number!")
        return False, False, 0, failed_entries + 1

    quantity = int(userinput)

    if quantity < 0:
        print("No negative numbers!")
        return False, False, 0, failed_entries + 1

    return False, True, quantity, failed_entries


def process_delivery(current_total, new_value):
    updated_total = current_total + new_value
    return updated_total


def calculate_tax(amount):
    tax = amount / 100 * 10
    return int(tax)


def update_inventory_list(inventory_list, order_id, product_name, quantity):
    inventory_list.append([order_id, product_name, quantity])

def add_product():
    """Prompt for each field, validate, append, and save to JSON."""
    print("Add New Product")
    
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


def generate_report(total_units, failed_attempts):
    print("Failed Entries:", failed_attempts)
    print("Total Units processed:", total_units)

def search_product():
    """Prompt for a product ID and show the matching product, if any."""
    print("Search Product")
    pid = input("Enter Product ID: ").strip().upper()
 
    if not pid:
        print("ID cannot be empty.")
        return
 
    for p in inventory:
        if p["id"].upper() == pid:
            print("Product found:")
            print("-" * 48)
            print(f"ID: {p['id']} | Name: {p['name']} | "
                  f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
            print("-" * 48)
            return
 
    print(f"No product found with ID '{pid}'.")    

def update_stock():
    """Find a product by ID, prompt for a new stock quantity, and save."""
    print("Update Stock")
    pid = input("Enter Product ID: ").strip().upper()
 
    if not pid:
        print("ID cannot be empty.")
        return
 
    for p in inventory:
        if p["id"].upper() == pid:
            print(f"Found: {p['name']} (current stock: {p['stock']})")
 
            while True:
                try:
                    new_stock = int(input("New Stock Quantity: "))
                    if new_stock < 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Enter a whole number (e.g. 10).")
 
            p["stock"] = new_stock
            save_inventory()
            print("Stock updated successfully!")
            return
 
    print(f"No product found with ID '{pid}'.")


def print_main_menu():
    print("1. Display All Product")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")

def display_all_products():
    """Read inventory.json from disk and print every product."""
    if not os.path.exists(file_path):
        print("inventory.json not found. Add a product first.")
        return
 
    try:
        with open(file_path, "r") as f:
            products = json.load(f)
    except json.JSONDecodeError:
        print("inventory.json is empty or corrupted.")
        return
 
    if not products:
        print("Inventory is empty.")
        return
 
    print("Current Inventory")
    print("-" * 48)
    for p in products:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)

  

load_inventory()

session_value = True
while session_value:
    actions = {
            "1": display_all_products,
            "2": add_product,
            "3": update_stock,
            "4": search_product,
            "5": save_inventory
            
        }
    print_main_menu()
    choice = input("Enter option: ").strip()
    if choice == "6":
        print("Saving Inventory before exit...")
        save_inventory()
        break
    action = actions.get(choice)
    if action:
        action()
    else:
        print("Invalid choice, try again.")


