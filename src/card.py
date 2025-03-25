import pandas as pd
import sys
import os

# the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_and_clean_data

# Load dataset
df = load_and_clean_data()

# Initialize an empty cart
cart = []


def add_to_card(stock_code, quantity):
    """Adds a product to the shopping cart."""
    product = df[df['StockCode'] == stock_code]

    if not product.empty:
        cart.append({
            'StockCode': stock_code,
            'Description': product['Description'].values[0],
            'Quantity': quantity,
            'UnitPrice': product['UnitPrice'].values[0]
        })
        print(f"Added {quantity} x {product['Description'].values[0]} to the cart.")
    else:
        print("Product not found!")


def view_card():
    """Displays the cart contents."""
    if not cart:
        print("Your cart is empty.")
        return

    total = 0
    print("\nYour Cart:")
    for item in cart:
        item_total = item['Quantity'] * item['UnitPrice']
        total += item_total
        print(f"{item['Quantity']} x {item['Description']} @ £{item['UnitPrice']} each = £{item_total:.2f}")

    print(f"\n Total: £{total:.2f}\n")

# # Example test
# if __name__ == "__main__":
#     add_to_card('85123A', 2)
#     view_card()
