import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# FastAPI Backend URL
API_URL = os.getenv("API_BASE_URL")

st.title("Chatbot App")
st.write("Enter your query below and get a response from the chatbot.")

# Input for user query
query = st.text_input("Your Query:")

if st.button("Send Query"):
    if query:
        response = requests.post(f"{API_URL}/query", json={"query": query})
        if response.status_code == 200:
            result = response.json()["result"]
            st.success(result)
        else:
            st.error("Error processing request")
    else:
        st.warning("Please enter a query.")

# # Add buttons for database management
# st.subheader("Database Management")

# if st.button("Delete Collection"):
#     response = requests.delete(f"{API_URL}/delete-collection")
#     if response.status_code == 200:
#         st.success("All documents deleted successfully")
#     else:
#         st.error("Error deleting documents")

# if st.button("Reinitialize Data"):
#     response = requests.post(f"{API_URL}/reinitialize-data")
#     if response.status_code == 200:
#         st.success("Data reinitialized successfully")
#     else:
#         st.error("Error reinitializing data")
