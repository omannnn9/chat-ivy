import os
import json
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load knowledge base
with open("ivy_knowledge_base_genz_expanded.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Load API key from environment variable
API_KEY = os.getenv("OPENROUTER_API_KEY")
USE_AI = API_KEY is not None

if USE_AI:
    print("🔑 AI cloud available.")
    openai.api_key = API_KEY
    openai.api_base = "https://openrouter.ai/api/v1"
else:
    print("⚠️ No AI API key found. Using offline fallback.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "Hmm, could you say that again? 🤔"})

    # Try AI cloud if available
    if USE_AI:
        try:
            response = openai.ChatCompletion.create(
                model="openrouter/auto",
                messages=[
                    {"role": "system", "content": "You are Ivy, a Gen Z-style friendly financial assistant that explains loans clearly with emojis and energy."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.8,
            )
            return jsonify({"reply": response["choices"][0]["message"]["content"]})
        except Exception as e:
            print("⚠️ AI error:", e)

    # Offline fallback using question matching
    user_input_lower = user_input.lower()
    for item in knowledge_base:
        if "questions" in item and isinstance(item["questions"], list):
            for q in item["questions"]:
                if q.lower() in user_input_lower:
                    return jsonify({"reply": item.get("answer", "Hmm... I’ll get back to you on that! 😅")})

    # If nothing matches
    return jsonify({"reply": "Oops 🥲 I couldn’t reach the AI cloud, but I’m still here to help with offline stuff!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
