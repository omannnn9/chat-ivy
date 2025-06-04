from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai, os, json

app = Flask(__name__)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    with open("ivy_knowledge_base_genz_expanded.json", "r", encoding="utf-8") as f:
        ivy_knowledge = json.load(f)
except:
    ivy_knowledge = []

def search_offline(user_input):
    for item in ivy_knowledge:
        if any(kw.lower() in user_input.lower() for kw in item.get("keywords", [])):
            return item.get("answer")
    return "Hmm, I’m not sure about that 🤔 — but I’m learning more every day!"

def get_response(user_input):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Ivy, a smart, friendly loan assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI failed:", e)
        return search_offline(user_input)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    reply = get_response(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
