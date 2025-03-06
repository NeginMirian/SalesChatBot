import os
import sys
import dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from huggingface_hub import InferenceClient
from langchain_huggingface import HuggingFaceEmbeddings
from search_engine import find_similar_products  # Correct import for the RAG function

# Load environment variables
dotenv.load_dotenv()

# Get Hugging Face API key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    print("ERROR: Missing Hugging Face API key. Please add it to the .env file.")
    sys.exit(1)

# Use InferenceClient
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HUGGINGFACE_API_KEY
)

# Define chatbot prompt template
template = PromptTemplate(
    input_variables=["history", "input", "product_info"],
    template="{history}\nUser: {input}\nAssistant: {product_info}\nAssistant (further response):"
)


def query_huggingface(input_data):
    """Queries the Hugging Face API."""

    # Convert input_data to string if needed
    if hasattr(input_data, 'to_string'):
        input_text = input_data.to_string()
    else:
        input_text = str(input_data)  # Ensure it's a string

    # Send request to Hugging Face API
    response = client.text_generation(input_text, max_new_tokens=50, temperature=0.3)

    return response


chatbot_chain = template | RunnableLambda(query_huggingface)


def chat_with_bot(user_input, history=""):
    """Handles user queries, retrieves relevant products, and generates responses using Hugging Face API."""

    product_info = ""

    # Check if user input is related to products
    if "product" in user_input.lower() or "buy" in user_input.lower() or "sneakers" in user_input.lower():
        products = find_similar_products(user_input)  # Get relevant products
        product_info = products.to_string(index=False) if not products.empty else "No matching products found."

    # Update chat history
    history += f"User: {user_input}\nAssistant: "

    # Invoke chatbot with the corrected parameters(invoke is the most important langchain function!)
    response = chatbot_chain.invoke({
        "history": history,
        "input": user_input,
        "product_info": product_info
    })

    return response, history


if __name__ == "__main__":
    history = ""
    while True:
        user_input = input("User: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        response, history = chat_with_bot(user_input, history)
        print(f"Assistant: {response}")




