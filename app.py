import os
import json
import re
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)

# Load knowledge base
with open("ivy_knowledge_base_genz_expanded.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# OpenRouter API Key
API_KEY = os.getenv("OPENROUTER_API_KEY")
USE_AI = bool(API_KEY)

if USE_AI:
    openai.api_key = API_KEY
    openai.api_base = "https://openrouter.ai/api/v1"
    print("✅ API key loaded")
else:
    print("⚠️ No API key found. Using offline mode.")

def normalize(text):
    return re.sub(r'[^\w\s]', '', text.lower()).strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    raw_input = request.json.get("message", "")
    user_input = normalize(raw_input)

    # If AI is available, use OpenRouter API
    if USE_AI:
        try:
            response = openai.ChatCompletion.create(
                model="openrouter/auto",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Ivy, a Gen Z financial chatbot. Be casual, friendly, and explain loans clearly with emojis."
                    },
                    {"role": "user", "content": raw_input}
                ],
                temperature=0.85,
            )
            return jsonify({"reply": response["choices"][0]["message"]["content"]})
        except Exception as e:
            print("⚠️ AI error:", e)

    # Offline fallback
    for item in knowledge_base:
        stored_question = normalize(item.get("question", ""))
        if stored_question and stored_question in user_input:
            return jsonify({"reply": item.get("answer")})

    return jsonify({
        "reply": "😕 Hmm, I don’t have an answer for that right now.\n"
                 "Want to see what I can help with? 👉 Check out *What Can I Ask Ivy?* on the left!\n"
                 "I’m here to help with all things regarding loans! 💸📄"
    })

@app.route("/help")
def help():
    categories = {
        "💸 Loan Basics": [],
        "🧮 Calculations": [],
        "📊 Interest & APR": [],
        "🏠 Loan Types": [],
        "😊 Friendly Chat": []
    }

    for item in knowledge_base:
        q = item.get("question", "").lower()
        if any(x in q for x in ["calculate", "how much", "emi", "monthly", "payment"]):
            categories["🧮 Calculations"].append(item["question"])
        elif any(x in q for x in ["apr", "interest", "rate"]):
            categories["📊 Interest & APR"].append(item["question"])
        elif any(x in q for x in ["home", "personal", "student", "mortgage", "car"]):
            categories["🏠 Loan Types"].append(item["question"])
        elif any(x in q for x in ["hi", "hello", "thanks", "bye", "who are you", "how are you"]):
            categories["😊 Friendly Chat"].append(item["question"])
        else:
            categories["💸 Loan Basics"].append(item["question"])

    return render_template("help.html", categories=categories)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
