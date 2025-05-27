# client.py
import re
import json
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env (for OPENAI_API_KEY)
load_dotenv()
client = OpenAI()

# Load Ivy’s local knowledge base
with open("ivy_knowledge_base_genz_expanded.json", "r", encoding="utf-8") as f:
    ivy_knowledge = json.load(f)

# 💸 Local loan calculator
def local_loan_calc(amount, rate_pct, term_years):
    r = rate_pct / 100 / 12
    n = term_years * 12
    payment = (amount * r) / (1 - (1 + r) ** -n)
    return round(payment, 2)

# 📊 Detect and handle loan calculation requests
def try_local_calculation(user_input):
    m = re.search(r"([\d,]+(?:\.\d+)?)\s*(?:dollar[s]?|usd)?\s*at\s*([\d\.]+)%\s*for\s*(\d+)\s*(?:year[s]?|yr)", user_input, re.IGNORECASE)
    if not m:
        return None
    amount = float(m.group(1).replace(",", ""))
    rate = float(m.group(2))
    years = int(m.group(3))
    monthly = local_loan_calc(amount, rate, years)
    return f"Alright bestie 😎 — for a loan of ${amount:,.2f} at {rate}% over {years} years, your monthly payment would be **around ${monthly:.2f}** 💸\nLet me know if you wanna compare options or change the rate 📊"

# 💬 Local knowledge base lookup
def try_knowledge_base(user_input):
    lowered = user_input.lower()
    for key, response in ivy_knowledge.items():
        if key in lowered:
            return response
    return None

# 🧠 Chat handler
def chat(user_input, history):
    # 1. Try offline knowledge base
    offline_response = try_knowledge_base(user_input)
    if offline_response:
        return offline_response, history + [{"role": "assistant", "content": offline_response}]
    
    # 2. Try local calculator
    local_calc = try_local_calculation(user_input)
    if local_calc:
        return local_calc, history + [{"role": "assistant", "content": local_calc}]
    
    # 3. Fallback to GPT-4o via API
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=history + [{"role": "user", "content": user_input}],
            temperature=0.8
        )
        reply = response.choices[0].message.content
        return reply, history + [{"role": "assistant", "content": reply}]
    except Exception as e:
        return "Oops! 🥲 I couldn’t reach the cloud brain right now. But I can still help with things like APR, EMI, or calculating your monthly payment — just ask!", history

# 🚀 Start chat loop
def main():
    print("Ivy: Hey hey! 👋 I’m Ivy — your Gen Z loan bestie 💸\nAsk me anything about loans, APR, EMIs or how to slay your money game 💅")
    history = [{"role": "system", "content": "You are Ivy, a Gen Z-style financial chatbot that explains loans, APR, EMIs, and credit with emojis, humor, and crystal clarity."}]
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Ivy: Byeee 👋 Keep slaying your finances and come back anytime 💖")
            break
        reply, history = chat(user_input, history)
        print("Ivy:", reply)

if __name__ == "__main__":
    main()
