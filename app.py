
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os

# Load .env first
load_dotenv()

# Debug print (optional)
print("🔍 Pinecone API Key:", os.getenv("PINECONE_API_KEY"))

from chatbot_agent.bot import get_bot_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    bot_reply = get_bot_response(user_msg)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
