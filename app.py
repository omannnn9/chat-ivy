from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# ✅ Use OpenRouter as backend
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
        # 🔁 Claude 3 Sonnet is the model for Ivy's personality
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-sonnet",
            messages=[
                {
                    "role": "system",
                    "content": "You are Ivy, a Gen Z-style friendly and helpful assistant that explains loans, APR, budgeting, EMIs and other finance topics in simple and fun ways."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print("🔥 AI ERROR:", e)
        reply = "Oops 🥲 I couldn’t reach the AI cloud, but I’m still here to help with offline stuff!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
