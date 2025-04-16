import os
import google.generativeai as genai
import requests
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_community.embeddings import GooglePalmEmbeddings
from langchain_community.chat_models import ChatGooglePalm
from langchain.chains import ConversationChain
from langchain.memory import VectorStoreRetrieverMemory
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 🔐 Gemini API Key
genai.configure(api_key="AIzaSyB6IWdtA_E1XjaT3YZxXppENR0A934Vais")  # Replace with your Gemini API key

# 🌐 Real-Time Search via Serper
def get_real_time_info(query):
    headers = {
        'X-API-KEY': 'your-api-key',
        'Content-Type': 'application/json'
    }
    payload = {'q': query}
    response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
    try:
        return response.json()['organic'][0]['snippet']
    except:
        return "No recent data found."

# 🧠 Pinecone Setup
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone with API key
pc = Pinecone(api_key="pcsk_6oqPCr_woxztFJXM7grNr2EDvQfLMsy9HLgYvDY85qoa1MriPL17KdcuTDq1KKPnmrkvC")  # Replace with your key

# Check and create the index if it doesn't exist
if 'ecom-memory' not in pc.list_indexes().names():
    pc.create_index(
        name='your-index-name',
        dimension=1536,  # Replace with your actual dimension size
        metric='metric-name',  # Choose metric (euclidean, cosine, etc.)
        spec=ServerlessSpec(cloud='aws', region='us-west-2')
    )

# Access the created index
index = pc.Index('your-index-name')  # Corrected access method for Index

# 🧠 VectorStore from existing Pinecone index
vectorstore = PineconeVectorStore(index_name="your-index-name", embedding=GooglePalmEmbeddings(google_api_key="AIzaSyB6IWdtA_E1XjaT3YZxXppENR0A934Vais"), namespace="", pinecone_api_key="pcsk_6oqPCr_woxztFJXM7grNr2EDvQfLMsy9HLgYvDY85qoa1MriPL17KdcuTDq1KKPnmrkvC")

# 🔁 Memory
memory = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())

# 💬 LLM (Pass the google_api_key explicitly)
llm = ChatGooglePalm(google_api_key="your-google-api-key")

# 🤖 Conversation Chain
chat = ConversationChain(llm=llm, memory=memory, verbose=True)

# 🔄 Chat Loop
def get_bot_response(user_input):
    try:
        response = chat.run(user_input)
        if not response.strip():  # If memory is empty
            response = get_real_time_info(user_input)
    except Exception as e:
        response = get_real_time_info(user_input)  # Fallback in case of an error
    return response

# Chat loop with combined logic
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Bot: Goodbye!")
        break
    response = get_bot_response(user_input)
    print("Bot:", response)
