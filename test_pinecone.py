from pinecone import Pinecone, ServerlessSpec

# Paste your full API key here (not the hidden one with asterisks)

API_KEY = "you-pinecone-api-key"  # Use your full key here


pc = Pinecone(api_key=API_KEY)

# Now do stuff
print("Available Indexes:", pc.list_indexes().names())

