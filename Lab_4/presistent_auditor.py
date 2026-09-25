print ("Hello World")
transactions =[]
inventory = 0
quitsig = False
total_inventory = 0
failed_entries = 0
print (inventory)
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "inventory.txt")

def get_valid_input(userinput, failed_entries, total_inventory):
    if userinput.lower() == "quit":
        
        return True, False, 0, failed_entries

    if not userinput.isdigit():
        print("Please input a valid positive number!")
        return False, False, 0, failed_entries + 1

    quantity= int(userinput)

    if quantity < 0:
        print("No negative numbers!")
        return False, False, 0, failed_entries + 1

    return False, True, inventory, failed_entries


def process_delivery(current_total, new_value):
    updated_total = current_total + new_value
    print(f"Adding {new_value} units. New Total Inventory: {updated_total}")
    return updated_total
    
def calculate_tax(amount):
    tax = amount/100 * 10
    return int(tax)

def generate_report(total_units, failed_attempts):
    print ("Failed Entries:", failed_attempts)
    print ("Total Units processed:", total_units)
    with open(file_path, "w") as file:
        file.write("Hello, World!")
        print("Here!")

def load_inventory():
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w") as file:
            file.write("")
        print("Current Orders: No previous orders found")
    else:
        with open(file_path, "r") as file:
            print(file.read())
            
def save_inventory(inventory_list, transactions_list, total_units):
    with open(file_path, "w") as file:
        file.write(f"Final Total Inventory: {total_units}\n\n")

        file.write("Current Stock by Product:\n")
        for item in inventory_list:
            file.write(f"  {item[0]}: {item[1]}\n")

        file.write("\nTransaction History:\n")
        if not transactions_list:
            file.write("  No transactions recorded.\n")
        else:
            for t in transactions_list:
                file.write(
                    f"  Product: {t[0]}, Quantity: {t[1]}, "
                    f"Running Total: {t[2]}, Tax: {t[3]}\n"
                )


    
session_value = True
while session_value == True:
    load_inventory()

    product_name = input("Enter product name (or type 'quit' to exit): ")
    
    if product_name.lower() == "quit":
        print("Exiting program.")
        generate_report(total_inventory, failed_entries)
        save_inventory(inventory)
        break

    userinput = input(f"Enter stock quantity for {product_name}(or type 'quit' to exit): ")
    
    
    print (userinput)

    is_quit, is_valid, quantity, failed_entries = get_valid_input(
        userinput, failed_entries, total_inventory
        
    )
    if is_quit:
        print("Exiting program.")
        generate_report(total_inventory, failed_entries)
        save_inventory(total_inventory)
        break
        
    if is_valid:
        transactions.append({
            "product": product_name,
            "quantity": userinput,
            

        })
        print(transactions)
        
        total_inventory = process_delivery(total_inventory, quantity)
        tax = calculate_tax(total_inventory)
        print("this is yo tax:", tax)