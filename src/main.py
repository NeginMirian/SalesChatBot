
import sys
import os
from src.chatbot import chat_with_bot
from src.card import add_to_card, view_card
from src.search_engine import find_similar_products
# check if `src/` directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Welcome message
print("\nWelcome to the Sales Assistant Chatbot!")
# print("Type 'exit' to quit, 'cart' to view cart, or 'add STOCKCODE QUANTITY' to add to cart.")

# create chat history
history = ""

while True:
    user_input = input("\nUser: ")

    if user_input.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break

    elif user_input.lower() == 'card':
        view_card()

    elif user_input.lower().startswith('add '):
        try:
            _, stock_code, quantity = user_input.split()
            add_to_card(stock_code, int(quantity))
        except ValueError:
            print("Invalid command format.")

    else:
        response, history = chat_with_bot(user_input, history)
        print(f"Assistant: {response}")
