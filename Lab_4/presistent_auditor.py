print("Hello World")
inventory = []          # list of [order_id, product_name, quantity]
transactions = []       # list of [order_id, product_name, quantity, running_total, tax]
total_inventory = 0
failed_entries = 0
next_order_id = 1001

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "orders.txt")


def load_inventory():
    global next_order_id
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w") as file:
            file.write("Current Orders: No previous orders found\n")
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


def generate_report(total_units, failed_attempts):
    print("Failed Entries:", failed_attempts)
    print("Total Units processed:", total_units)


def save_inventory(inventory_list, transactions_list, total_units):
    with open(file_path, "w") as file:
        for item in inventory_list:
            file.write(f"{item[0]},{item[1]},{item[2]}\n")
    print(f"Order successfully saved to {os.path.basename(file_path)}")


load_inventory()

session_value = True
while session_value:
    product_name = input("Enter Product Name: ")

    if product_name.lower() == "quit":
        print("Exiting program.")
        generate_report(total_inventory, failed_entries)
        save_inventory(inventory, transactions, total_inventory)
        break

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