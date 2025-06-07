import os
import json
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load OpenRouter API key
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
print("🔑 API key loaded:", bool(OPENROUTER_API_KEY))

# Load offline fallback knowledge base
with open("ivy_knowledge_base_genz_expanded.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip().lower()

    # ✅ Try OpenRouter API
    if OPENROUTER_API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://chat-ivy-353j.onrender.com",  # Required by OpenRouter
                "X-Title": "Ivy",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are Ivy, a helpful, friendly Gen Z-style financial assistant who explains everything clearly."},
                    {"role": "user", "content": user_message}
                ]
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            print("🌐 OpenRouter status:", response.status_code)
            print("🌐 OpenRouter response:", response.text)

            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"].strip()
                return jsonify({"reply": reply})
            else:
                print("⚠️ AI call failed, falling back to local responses.")
        except Exception as e:
            print("❌ Error with OpenRouter API:")
            import traceback
            traceback.print_exc()

    # 🔁 Offline fallback if OpenRouter fails or is unreachable
    for entry in knowledge_base:
        for example in entry.get("examples", []):
            if example.lower() in user_message:
                return jsonify({"reply": entry["response"]})

    return jsonify({
        "reply": "Oops 🥲 I couldn’t reach the AI cloud, but I’m still here to help with offline stuff!"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
