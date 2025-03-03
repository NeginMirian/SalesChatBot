import pandas as pd
from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from data_loader import load_and_clean_data #Helps load Pandas DataFrames into LangChain.

# Load dataset
df = load_and_clean_data()

# Convert each product row into a LangChain doc for retrival
documents = [
    Document(page_content=row['Description'], metadata={"StockCode": row["StockCode"], "UnitPrice": row["UnitPrice"]})
    for _, row in df.iterrows()
]

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create a FAISS vector
vector_store = FAISS.from_documents(documents, embedding_model)
# How FAISS Works
# Stores vectors for all product descriptions.
# When a user queries a product name, FAISS:
# Embeds the query into a vector.
# Finds the closest product vectors.

# Create a retriever
retriever = vector_store.as_retriever()

def find_similar_products(query, top_n=5):
    """Retrieve top N most relevant products using RAG."""
    retrieved_docs = retriever.get_relevant_documents(query)

# Convert retrieved docs(Converts retrieved doc objects into a Pandas df)
    product_list = [{"Description": doc.page_content, "StockCode": doc.metadata["StockCode"],
                     "UnitPrice": doc.metadata["UnitPrice"]} for doc in retrieved_docs[:top_n]]

    return pd.DataFrame(product_list)


#example
if __name__ == "__main__":
    query = "blue mug"
    recommendations = find_similar_products(query)
    print(recommendations)

