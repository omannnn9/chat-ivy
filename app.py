from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ✅ Set OpenRouter API key and endpoint
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    try:
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-sonnet",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Ivy — a Gen Z-style AI financial assistant who is friendly, helpful, and explains "
                        "loans, APR, EMIs, budgeting, and financial concepts in a simple, casual, and fun way. Be clear, supportive, and relatable."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print("🔥 AI ERROR:", repr(e))  # Shows detailed error in Render logs
        reply = "Oops 🥲 I couldn’t reach the AI cloud, but I’m still here to help with offline stuff!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
