console.log("✅ Ivy script loaded");

const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  addMessage("you", text);
  input.value = "";
  addTyping();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    removeTyping();
    addMessage("ivy", data.reply);
  } catch (err) {
    removeTyping();
    console.error("❌ Chat error:", err);
    addMessage("ivy", "Oops 🥲 I couldn’t reach the AI cloud, but I’m still here to help with offline stuff!");
  }
});

function addMessage(sender, text) {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;

  if (sender === "ivy") {
    const img = document.createElement("img");
    img.src = "/static/ivy-profile.png";
    img.alt = "Ivy Avatar";
    img.className = "chat-pfp";
    msg.appendChild(img);
  }

  const span = document.createElement("span");
  span.innerText = text;
  msg.appendChild(span);
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function addTyping() {
  const msg = document.createElement("div");
  msg.className = "message ivy typing";
  msg.innerHTML = `<img src="/static/ivy-profile.png" class="chat-pfp" alt="Ivy Avatar" /><span>Typing...</span>`;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
  const typing = document.querySelector(".typing");
  if (typing) typing.remove();
}
