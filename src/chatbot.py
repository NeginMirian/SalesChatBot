import os
import sys
import dotenv
from langchain_community.llms.openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from huggingface_hub import InferenceClient
from langchain_huggingface import HuggingFaceEmbeddings
from search_engine import find_similar_products
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
# Load environment variables
dotenv.load_dotenv()

# Get Hugging Face API and OpenAI keys(the priority is OpenAI here, if you want to choose hugging face API key, leave openAI key empty)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

if not (HUGGINGFACE_API_KEY or OPENAI_API_KEY):
    print("ERROR: Missing both Hugging Face and OpenAI API keys. Please add at least one to the .env file.")
    sys.exit(1)

# Use InferenceClient
# client = InferenceClient(
#     model="mistralai/Mistral-7B-Instruct-v0.3",
#     token=HUGGINGFACE_API_KEY
# )

# Define chatbot prompt template
template = PromptTemplate(
    input_variables=["history", "input", "product_info"],
    template="You are a concise and helpful shopping assistant. Provide clear and relevant answers without unnecessary details. \
    Do NOT continue the chat on behalf of the user, and do NOT a lot of generate additional messages. \
    If the user asks about a product, respond with the name, price, and a brief description. Do NOT assume further inquiries. \n\n\
    {history}\nUser: {input}\nAssistant: {product_info}\n"
)

if OPENAI_API_KEY:
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model_name="gpt-3.5-turbo",
        temperature=0.3,
        max_tokens=50
    )


    def query_openai(input_data):
        """Queries the OpenAI API."""
        input_text = str(input_data)
        response = llm.invoke(input_text)
        return response


    active_query_function = query_openai

# Option 2: Hugging Face
elif HUGGINGFACE_API_KEY:
    from huggingface_hub import InferenceClient

    # Configure the Hugging Face Inference Client
    client = InferenceClient(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        token=HUGGINGFACE_API_KEY
    )


    def query_huggingface(input_data):
        """Queries the Hugging Face API."""
        input_text = str(input_data)
        response = client.invoke(input_text, params={"max_new_tokens": 50, "temperature": 0.3})
        return response


    active_query_function = query_huggingface

# Create the chatbot chain using the chosen query function
chatbot_chain = template | RunnableLambda(active_query_function)


# --- Chatbot conversation function ---
def chat_with_bot(user_input, history=""):
    """Handles user queries, retrieves relevant products, and generates responses using the selected API."""
    product_info = ""

    # Check if the query is product-related.
    if "product" in user_input.lower() or "buy" in user_input.lower() in user_input.lower():
        products = find_similar_products(user_input)
        product_info = products.to_string(index=False) if not products.empty else "No matching products found."

    # Update chat history
    history += f"User: {user_input}\nAssistant: "

    # Invoke the chatbot chain with the required parameters
    response = chatbot_chain.invoke({
        "history": history,
        "input": user_input,
        "product_info": product_info
    }).content

    # Append the interaction to history
    history += f"{response}\n"

    return response, history


# --- Main loop ---
if __name__ == "__main__":
    history = ""
    while True:
        user_input = input("User: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        response, history = chat_with_bot(user_input, history)
        print(f"Assistant: {response}")



