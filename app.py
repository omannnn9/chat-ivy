# app.py
from flask import Flask, request, jsonify, render_template
import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

app = Flask(__name__)
load_dotenv()
client = OpenAI()

# Load offline knowledge
with open("ivy_knowledge_base_genz_expanded.json", "r", encoding="utf-8") as f:
    ivy_knowledge = json.load(f)

def local_loan_calc(amount, rate_pct, term_years):
    r = rate_pct / 100 / 12
    n = term_years * 12
    payment = (amount * r) / (1 - (1 + r) ** -n)
    return round(payment, 2)

def try_local_calculation(user_input):
    m = re.search(r"([\d,]+(?:\.\d+)?)\s*(?:dollar[s]?|usd)?\s*at\s*([\d\.]+)%\s*for\s*(\d+)\s*(?:year[s]?|yr)", user_input, re.IGNORECASE)
    if not m:
        return None
    amount = float(m.group(1).replace(",", ""))
    rate = float(m.group(2))
    years = int(m.group(3))
    monthly = local_loan_calc(amount, rate, years)
    return f"Alright bestie 😎 — for a loan of ${amount:,.2f} at {rate}% over {years} years, your monthly payment would be **around ${monthly:.2f}** 💸"

def try_knowledge_base(user_input):
    lowered = user_input.lower()
    for key, response in ivy_knowledge.items():
        if key in lowered:
            return response
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    # 1. Check local knowledge
    response = try_knowledge_base(user_input)
    if response:
        return jsonify({"reply": response})
    # 2. Check loan calc
    calc = try_local_calculation(user_input)
    if calc:
        return jsonify({"reply": calc})
    # 3. GPT fallback
    try:
        chat_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Ivy, a Gen Z financial chatbot who uses emojis, fun tone, and gives clear answers about loans, APR, and money."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.8
        )
        reply = chat_response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Oops! 🥲 I couldn’t reach my cloud brain. But I can still help with APRs, loans, or EMIs if you ask!"})

if __name__ == "__main__":
    app.run(debug=True)
