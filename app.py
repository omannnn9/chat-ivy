import os
import json
import re
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv

# Load .env vars
load_dotenv()

app = Flask(__name__)

# Load offline knowledge base
with open("ivy_knowledge_base_genz_expanded.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Load API key from environment
API_KEY = os.getenv("OPENROUTER_API_KEY")
USE_AI = bool(API_KEY)

if USE_AI:
    print("✅ AI cloud enabled")
    openai.api_key = API_KEY
    openai.api_base = "https://openrouter.ai/api/v1"
else:
    print("⚠️ No API key found. Using offline mode.")

# Utility: clean and normalize input
def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.strip()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    raw_input = request.json.get("message", "")
    user_input = normalize(raw_input)

    # ✅ Try AI first
    if USE_AI:
        try:
            response = openai.ChatCompletion.create(
                model="openrouter/auto",
                messages=[
                    {"role": "system", "content": "You are Ivy, a Gen Z-style financial expert who explains loans with emojis and friendly energy."},
                    {"role": "user", "content": raw_input}
                ],
                temperature=0.85,
            )
            return jsonify({"reply": response["choices"][0]["message"]["content"]})
        except Exception as e:
            print("⚠️ AI error:", e)

    # 🔍 Offline fallback
    for item in knowledge_base:
        stored_question = normalize(item.get("question", ""))
        if stored_question in user_input:
            return jsonify({"reply": item.get("answer")})

    return jsonify({
        "reply": "Oops 🥲 I couldn’t reach the AI cloud, but I’m still here to help with offline stuff!"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
