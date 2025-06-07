import os
import json
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load API Key from environment
API_KEY = os.environ.get("OPENROUTER_API_KEY")
print("🔑 API key loaded:", bool(API_KEY))

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

    # ✅ Try OpenRouter API first
    if API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "Referer": "https://chat-ivy-353j.onrender.com"
            }

            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are Ivy, a friendly Gen Z loan advisor."},
                    {"role": "user", "content": user_message}
                ]
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
                return jsonify({"reply": reply})
            else:
                print("🔁 API error:", response.status_code)
        except Exception as e:
            print("❌ API exception:", str(e))

    # ✅ Offline fallback
    for entry in knowledge_base:
        for example in entry["examples"]:
            if example.lower() in user_message:
                return jsonify({"reply": entry["response"]})

    # If no match found
    return jsonify({"reply": "Oops 🥲 I couldn’t reach the AI cloud, but I’m still here to help with offline stuff!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
