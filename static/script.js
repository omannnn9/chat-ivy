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
    addMessage("ivy", "Oops! Couldn't connect. Try again later.");
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

// ✅ Import three.js and loader via CDN
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.module.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.150.1/examples/jsm/loaders/GLTFLoader.js';

const container = document.getElementById("model-container");
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 300, 0.1, 1000);
camera.position.set(0, 1.5, 3);

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(container.clientWidth, 300);
container.appendChild(renderer.domElement);

const light = new THREE.HemisphereLight(0xffffff, 0x444444);
light.position.set(0, 1, 0);
scene.add(light);

const loader = new GLTFLoader();
loader.load("/static/ivy-model.glb", (gltf) => {
  const model = gltf.scene;
  model.scale.set(1.5, 1.5, 1.5);
  model.position.y = -1.2;
  scene.add(model);

  function animate() {
    requestAnimationFrame(animate);
    model.rotation.y += 0.01;
    renderer.render(scene, camera);
  }

  animate();
}, undefined, (err) => {
  console.error("❌ Failed to load Ivy's 3D model:", err);
});
