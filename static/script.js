const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const chatBox = document.getElementById("chat-box");

// Submit chat
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
    addMessage("ivy", "Oops! Couldn't connect. Try again later.");
  }
});

// Chat renderer
function addMessage(sender, text) {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;

  if (sender === "ivy") {
    const img = document.createElement("img");
    img.src = "/static/ivy-profile.png";
    img.className = "chat-pfp";
    msg.appendChild(img);
  }

  const span = document.createElement("span");
  span.innerText = text;
  msg.appendChild(span);
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Typing animation
function addTyping() {
  const msg = document.createElement("div");
  msg.className = "message ivy typing";
  msg.innerHTML = `<img src="/static/ivy-profile.png" class="chat-pfp" /><span>Typing...</span>`;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
  const typing = document.querySelector(".typing");
  if (typing) typing.remove();
}

// 3D Model loader
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.module.js";
import { GLTFLoader } from "https://cdn.jsdelivr.net/npm/three@0.150.1/examples/jsm/loaders/GLTFLoader.js";

const container = document.getElementById("model-container");
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, container.clientWidth / 300, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(container.clientWidth, 300);
container.appendChild(renderer.domElement);

const loader = new GLTFLoader();
loader.load("/static/ivy-model.glb", (gltf) => {
  const model = gltf.scene;
  model.scale.set(1.5, 1.5, 1.5);
  scene.add(model);
  model.position.y = -1;

  camera.position.z = 3;
  function animate() {
    requestAnimationFrame(animate);
    model.rotation.y += 0.01;
    renderer.render(scene, camera);
  }
  animate();
});
