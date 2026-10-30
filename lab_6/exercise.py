import json
import os

books = []   # list of dicts: {"title", "author", "available"}
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.json")


def add_book(title, author):
    books.append({"title": title, "author": author, "available": True})


def find_book(title):
    for b in books:
        if b["title"].lower() == title.lower():
            return b
    return None


def checkout_book():
    title = input("Title to check out: ").strip()
    book = find_book(title)
    if book is None:
        print("Book not found.")
    elif not book["available"]:
        print("Already checked out.")
    else:
        book["available"] = False
        save_books()
        print(f"You checked out '{book['title']}'.")


def return_book():
    title = input("Title to return: ").strip()
    book = find_book(title)
    if book is None:
        print("Book not found.")
    elif book["available"]:
        print("That book wasn't checked out.")
    else:
        book["available"] = True
        save_books()
        print(f"You returned '{book['title']}'.")


def list_books():
    if not books:
        print("No books in the library.")
        return
    for b in books:
        status = "Available" if b["available"] else "Checked out"
        print(f"{b['title']} by {b['author']} - {status}")


def save_books():
    with open(file_path, "w") as f:
        json.dump(books, f, indent=4)


def load_books():
    global books
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            books = json.load(f)


def print_menu():
    print("\n1. List books")
    print("2. Check out a book")
    print("3. Return a book")
    print("4. Quit")


load_books()
if not books:
    add_book("Dune", "Frank Herbert")
    add_book("Emma", "Jane Austen")
    add_book("Ulysses", "James Joyce")
    save_books()

running = True
while running:
    print_menu()
    choice = input("Choose: ").strip()
    if choice == "1":
        list_books()
    elif choice == "2":
        checkout_book()
    elif choice == "3":
        return_book()
    elif choice == "4":
        running = False
    else:
        print("Invalid choice.")