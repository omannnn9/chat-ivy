from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Ivy, a friendly Gen Z financial assistant who explains loans, APR, EMIs and budgeting in a fun but helpful tone."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
    except Exception:
        reply = "Oops 🥲 I couldn’t reach the AI cloud, but I’m still here to help with offline stuff!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
