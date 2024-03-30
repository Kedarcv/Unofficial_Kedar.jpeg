import tkinter as tk
import serial
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create the inventory table if it doesn't already exist
c.execute('''CREATE TABLE IF NOT EXISTS inventory
             (product_name TEXT, quantity INTEGER)''')

# Initialize the inventory dictionary
inventory = {}

# Open the serial port for the barcode scanner
ser = serial.Serial('/dev/ttyACM0', 9600)

# Function to handle incoming barcode scans
def handle_scan(event=None):
    # Read the barcode data from the serial port
    data = ser.readline().decode('utf-8').strip()

    # Find the product in the inventory
    product = None
    for item in inventory.items():
        if item[1]['barcode'] == data:
            product = item[0]
            break

    # If the product was found, add it to the shopping cart
    if product:
        shopping_cart.append(product)
        update_total()

# Function to update the total cost of the shopping cart
def update_total():
    total = 0
    for item in shopping_cart:
        total += inventory[item]['price'] * inventory[item]['quantity']
    total_label.config(text=f'Total: ${total:.2f}')

# Function to process the payment and clear the shopping cart
def process_payment():
    # TODO: Implement payment processing

    # Clear the shopping cart
    shopping_cart.clear()
    update_total()

# Set up the main window
window = tk.Tk()
window.title('Shop Inventory')

# Add a barcode scanner input field
scan_entry = tk.Entry(window, width=30)
scan_entry.pack()
scan_entry.bind('<Return>', handle_scan)

# Add a listbox for the shopping cart
shopping_cart_listbox = tk.Listbox(window, width=50, height=10)
shopping_cart_listbox.pack()

# Add a label for the total cost
total_label = tk.Label(window, text='Total: $0.00')
total_label.pack()

# Add a button for processing payments
pay_button = tk.Button(window, text='Process Payment', command=process_payment)
pay_button.pack()

# Initialize the shopping cart
shopping_cart = []

# Start the main event loop
window.mainloop()

# Close the database connection
conn.close()