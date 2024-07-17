import sqlite3

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('shopkeeper.db')
cursor = conn.cursor()

# Create items table
cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL
                  )''')

conn.commit()

def add_item():
    name = input("Enter item name: ")
    price = float(input("Enter item price: "))
    quantity = int(input("Enter item quantity: "))
    
    cursor.execute("INSERT INTO items (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
    conn.commit()
    print("Item added successfully!")

def view_inventory():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    
    if items:
        print("ID\tName\tPrice\tQuantity")
        print("-" * 30)
        for item in items:
            print(f"{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}")
    else:
        print("No items in inventory.")

def sell_item():
    item_id = int(input("Enter item ID to sell: "))
    quantity = int(input("Enter quantity to sell: "))
    
    cursor.execute("SELECT * FROM items WHERE id=?", (item_id,))
    item = cursor.fetchone()
    
    if item:
        if item[3] >= quantity:
            new_quantity = item[3] - quantity
            cursor.execute("UPDATE items SET quantity=? WHERE id=?", (new_quantity, item_id))
            conn.commit()
            print("Item sold successfully!")
        else:
            print("Not enough quantity in stock.")
    else:
        print("Item not found.")

def main_menu():
    while True:
        print("\nShopkeeper Application")
        print("1. Add Item")
        print("2. View Inventory")
        print("3. Sell Item")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_item()
        elif choice == '2':
            view_inventory()
        elif choice == '3':
            sell_item()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

    # Close the database connection
    conn.close()
