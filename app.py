from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai
import os
import json

app = Flask(__name__)
load_dotenv()

# Load OpenAI key if present
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load fallback JSON knowledge base
try:
    with open("ivy_knowledge_base_genz_expanded.json", "r", encoding="utf-8") as f:
        ivy_knowledge = json.load(f)
except Exception as e:
    print("Failed to load JSON:", e)
    ivy_knowledge = []

# 🧠 Local fallback answer
def search_offline_knowledge(user_input):
    for item in ivy_knowledge:
        keywords = item.get("keywords", [])
        if any(kw.lower() in user_input.lower() for kw in keywords):
            return item.get("answer")
    return "Hmm, I’m not sure about that 🤔 — but I’m learning more every day!"

# 🌐 AI + fallback response
def get_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # use gpt-3.5-turbo if you're on free tier
            messages=[
                {"role": "system", "content": "You are Ivy, a smart, friendly Gen Z financial chatbot. Speak informally but clearly. Give real, accurate help about loans."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI Error:", e)
        return search_offline_knowledge(user_input)

# 🎯 Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    reply = get_response(user_input)
    return jsonify({"reply": reply})

# 🏁 Run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
