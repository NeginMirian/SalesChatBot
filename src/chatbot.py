import os
import sys
import dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from huggingface_hub import InferenceClient
from langchain_huggingface import HuggingFaceEmbeddings
# Load environment variables
dotenv.load_dotenv()

# Get Hugging Face API key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    print("ERROR: Missing Hugging Face API key. Please add it to the .env file.")
    sys.exit(1)

#  Use InferenceClient
client = InferenceClient(
    # model="HuggingFaceH4/zephyr-7b-beta"
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HUGGINGFACE_API_KEY
)

# Define chatbot prompt
template = PromptTemplate(
    input_variables=["history", "input"],
    template="{history}\nUser: {input}\nAssistant:"
)


#
def query_huggingface(input_data):
    """Queries the Hugging Face Inference API."""

    # Convert LangChain output to a string
    if hasattr(input_data, 'to_string'):
        input_text = input_data.to_string()
    else:
        input_text = str(input_data)

    response = client.text_generation(input_text, max_new_tokens=50, temperature=0.3)
    return response



chatbot_chain = template | RunnableLambda(query_huggingface)


def chat_with_bot(user_input, history=""):
    """Handles user queries and generates responses using Hugging Face API."""

    # Update chat history
    history += f"User: {user_input}\nAssistant: "

    # Generate chatbot response
    response = chatbot_chain.invoke({"history": history, "input": user_input})

    return response, history


if __name__ == "__main__":
    history = ""
    while True:
        user_input = input("User: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        response, history = chat_with_bot(user_input, history)
        print(f"Assistant: {response}")

