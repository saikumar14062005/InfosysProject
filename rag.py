# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# import csv
# import os
# # from dotenv import load_dotenv
# # load_dotenv()


# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/embedding-001",
#     google_api_key = "AIzaSyDiI1IfCBpE_6CPTkkguBKMT_BUxYAEusA"
# )

# # from dotenv import load_dotenv
# # import os
# # from langchain.embeddings.google_generative_ai import GoogleGenerativeAIEmbeddings

# # Load environment variables from the .env file
# # load_dotenv()

# # Retrieve the API key from the environment variable
# # google_api_key = os.getenv("GOOGLE_API_KEY")

# # Use the API key in the embeddings initialization
# # embeddings = GoogleGenerativeAIEmbeddings(
# #     model="models/embedding-001",
# #     google_api_key=google_api_key
# # )

# def load_data_from_csv(csv_path):
#   """Loads data from a CSV file into a list of dictionaries."""
#   data = []
#   with open(csv_path, 'r', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#       data.append(row)
#   return data

# def embed_data(data):
#   """Embeds the text content of each data point."""
#   text_list = [item['description'] for item in data] 
#   embeddings_list = embeddings.embed_documents(text_list)
#   return np.array(embeddings_list)

# def search_data(query, data, data_embeddings, top_k=5):
#   """
#   Searches for related data points based on a query using cosine similarity.

#   Args:
#       query: The search query.
#       data: The list of data points (dictionaries).
#       data_embeddings: The pre-computed embeddings for each data point.
#       top_k: Number of top results to return.

#   Returns:
#       A list of top_k dictionaries containing the related data points.
#   """
#   query_embedding = embeddings.embed_query(query)
#   query_embedding = np.array(query_embedding).reshape(1, -1)

 
#   similarities = cosine_similarity(query_embedding, data_embeddings)

  
#   top_k_indices = similarities.argsort(axis=1)[:, -top_k:][0] 

 
#   related_data = [data[i] for i in top_k_indices] 

#   return related_data

# csv_path = "flipkart_products.csv" 

# data = load_data_from_csv(csv_path)
# data_embeddings = embed_data(data)
# # print(data)




from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import csv
import os
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key from the environment
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the embeddings with the API key
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=google_api_key
)

# Initialize Google Generative AI embeddings
# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/embedding-001",
#     google_api_key="AIzaSyDiI1IfCBpE_6CPTkkguBKMT_BUxYAEusA"
# )

def load_data_from_csv(csv_path):
    """Loads data from a CSV file into a list of dictionaries."""
    data = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def embed_and_store_in_faiss(data, vector_store_path="faiss_index"):
    """
    Embeds data and stores it in a FAISS vector database.

    Args:
        data: The list of data points (dictionaries).
        vector_store_path: Path to save the FAISS index.

    Returns:
        A FAISS vector store instance.
    """
    # Extract text content for embedding
    text_list = [item['description'] for item in data]
    documents = [Document(page_content=text, metadata=item) for text, item in zip(text_list, data)]

    # Embed and store in FAISS
    vector_store = FAISS.from_documents(documents, embeddings)

    # Save FAISS index for later use
    vector_store.save_local(vector_store_path)
    return vector_store

def load_faiss_index(vector_store_path="faiss_index"):
    """Loads a saved FAISS index from the specified path."""
    return FAISS.load_local(vector_store_path, embeddings,allow_dangerous_deserialization=True)

# def search_faiss_index_with_threshold(query, vector_store, top_k=3, similarity_threshold=0.8):
#     """
#     Searches for related data points using FAISS vector store with a similarity threshold.

#     Args:
#         query: The search query.
#         vector_store: The FAISS vector store.
#         top_k: Number of top results to return.
#         similarity_threshold: Minimum similarity score to consider a match.

#     Returns:
#         A list of dictionaries containing the related data points or an empty list if no match exceeds the threshold.
#     """
#     # Perform similarity search with scores
#     docs_with_scores = vector_store.similarity_search_with_score(query, k=top_k)

#     # Filter results based on the similarity threshold
#     filtered_results = [
#         (doc, score) for doc, score in docs_with_scores if score >= similarity_threshold
#     ]

#     # Return only the documents that meet the threshold
#     return [doc for doc, _ in filtered_results]

def search_faiss_index_with_threshold(query, vector_store, similarity_threshold=0.6):
    docs_with_scores = vector_store.similarity_search_with_score(query)

    # Filter results based on the similarity threshold
    filtered_results = [
        (doc, score) for doc, score in docs_with_scores if score >= similarity_threshold
    ]

    # Return only the documents that meet the threshold
    return [doc for doc, _ in filtered_results]


# CSV path
csv_path = "flipkart_products.csv"

# Load data from CSV
data = load_data_from_csv(csv_path)

# Embed and store in FAISS
vector_store = embed_and_store_in_faiss(data)

