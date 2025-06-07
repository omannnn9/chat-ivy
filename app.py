import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI, OpenAIError

app = Flask(__name__)

# Load your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load offline knowledge base
with open("ivy_knowledge_base_genz_expanded.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Initialize OpenAI client if key is available
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    message_lower = message.lower()

    # Try using OpenAI API first
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're Ivy, a friendly Gen Z loan assistant who explains things in a casual, helpful way."},
                    {"role": "user", "content": message}
                ]
            )
            reply = response.choices[0].message.content.strip()
            return jsonify({"reply": reply})
        except OpenAIError as e:
            print("⚠️ OpenAI API error:", e)

    # Offline fallback: match example phrases
    for entry in knowledge_base:
        examples = entry.get("examples", [])
        for example in examples:
            if example.lower() in message_lower:
                return jsonify({"reply": entry["response"]})

    # Generic fallback if nothing matches
    return jsonify({
        "reply": "Oops 🥲 I couldn’t reach the AI cloud, but I’m still here to help with offline stuff!"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
