import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Load offline knowledge base
with open("ivy_knowledge_base_genz_expanded.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip().lower()

    # 🔁 Try calling OpenRouter first
    if OPENROUTER_API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are Ivy, a helpful Gen Z financial assistant."},
                    {"role": "user", "content": user_message}
                ]
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            result = response.json()
            reply = result["choices"][0]["message"]["content"].strip()
            return jsonify({"reply": reply})
        except Exception as e:
            print("⚠️ OpenRouter error:", e)

    # 🧠 Offline fallback
    for entry in knowledge_base:
        for example in entry.get("examples", []):
            if example.lower() in user_message:
                return jsonify({"reply": entry["response"]})

    # Final fallback message
    return jsonify({
        "reply": "Oops 🥲 I couldn’t reach the AI cloud, but I’m still here to help with offline stuff!"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
