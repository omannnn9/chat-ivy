console.log("✅ Ivy script loaded");

// Chat functionality
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

// ✅ Load 3D model using Three.js + GLTFLoader
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(250, 250);

const container = document.getElementById("ivy-3d");
if (container) container.appendChild(renderer.domElement);
else console.warn("⚠️ 3D container not found");

const loader = new THREE.GLTFLoader();
loader.load(
  '/static/ivy-model.glb',
  function (gltf) {
    console.log("✅ 3D model loaded successfully.");
    const model = gltf.scene;
    scene.add(model);
    camera.position.z = 2;

    function animate() {
      requestAnimationFrame(animate);
      model.rotation.y += 0.01;
      renderer.render(scene, camera);
    }

    animate();
  },
  undefined,
  function (error) {
    console.error("❌ Failed to load 3D model:", error);
    alert("3D model failed to load. See console for details.");
  }
);
