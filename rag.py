from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import csv
import os
from dotenv import load_dotenv
load_dotenv()


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key = "AIzaSyDiI1IfCBpE_6CPTkkguBKMT_BUxYAEusA"
)

def load_data_from_csv(csv_path):
  """Loads data from a CSV file into a list of dictionaries."""
  data = []
  with open(csv_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      data.append(row)
  return data

def embed_data(data):
  """Embeds the text content of each data point."""
  text_list = [item['description'] for item in data] 
  embeddings_list = embeddings.embed_documents(text_list)
  return np.array(embeddings_list)

def search_data(query, data, data_embeddings, top_k=5):
  """
  Searches for related data points based on a query using cosine similarity.

  Args:
      query: The search query.
      data: The list of data points (dictionaries).
      data_embeddings: The pre-computed embeddings for each data point.
      top_k: Number of top results to return.

  Returns:
      A list of top_k dictionaries containing the related data points.
  """
  query_embedding = embeddings.embed_query(query)
  query_embedding = np.array(query_embedding).reshape(1, -1)

 
  similarities = cosine_similarity(query_embedding, data_embeddings)

  
  top_k_indices = similarities.argsort(axis=1)[:, -top_k:][0] 

 
  related_data = [data[i] for i in top_k_indices] 

  return related_data

csv_path = "flipkart_products.csv" 

data = load_data_from_csv(csv_path)
data_embeddings = embed_data(data)
# print(data)
