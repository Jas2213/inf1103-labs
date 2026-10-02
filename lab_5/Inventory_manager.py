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
    global next_order_id
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open("user.json", "w") as file:
            json.dump(user_data, file, indent=4)
        print("No inventory file found. Created a new one.")
        return

    print("Current Orders:\n")
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or "," not in line:
                continue
            parts = line.split(",")
            order_id = int(parts[0].strip())
            product_name = parts[1].strip()
            quantity = int(parts[2].strip())
            inventory.append([order_id, product_name, quantity])
            print(line)
            if order_id >= next_order_id:
                next_order_id = order_id + 1
    print()

def save_inventory(dictionary):
    with open(file_path, "w") as file:
        for item in inventory_list:
            file.write(f"{item[0]},{item[1]},{item[2]}\n")
    print(f"Order successfully saved to {os.path.basename(file_path)}")
 

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

def add_product(inventory):
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
    save_inventory(inventory)  # write to inventory.json right away
    print("Product added successfully!")


def generate_report(total_units, failed_attempts):
    print("Failed Entries:", failed_attempts)
    print("Total Units processed:", total_units)



def print_main_menu():
    print("1. Display All Product")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")

def menu_actions():
    actions = {
        "1": load_inventory,
        "2": add_product,
        "3":
        "4":
        "5":
        "6":
    }

load_inventory()

session_value = True
while session_value:
    print_main_menu()
    choice = input("Choose an option: ").strip()
    if choice == "6": #Quitting program
        print("Saving Inventory before exit...")
        save_inventory()
        print("Inventory saved succesfully.")
        break
    action = actions.get(choice)
    if action:
            action()
    else:
            print("Invalid choice, try again.")
    userinput = input("Enter Quantity: ")

    is_quit, is_valid, quantity, failed_entries = get_valid_input(
        userinput, failed_entries, total_inventory
    )

    if is_quit:
        print("Exiting program.")
        generate_report(total_inventory, failed_entries)
        save_inventory(inventory, transactions, total_inventory)
        break



    if is_valid:
        order_id = next_order_id
        next_order_id += 1

        update_inventory_list(inventory, order_id, product_name, quantity)
        total_inventory = process_delivery(total_inventory, quantity)
        tax = calculate_tax(total_inventory)

        print(f"\nNew Order Added:\n{order_id},{product_name},{quantity}\n")

        transactions.append([order_id, product_name, quantity, total_inventory, tax])