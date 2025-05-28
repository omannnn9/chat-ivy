const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userText = input.value.trim();
  if (!userText) return;

  appendMessage(userText, "user");
  input.value = "";

  const reply = await getReply(userText);
  appendMessage(reply, "ivy");
});

function appendMessage(text, sender) {
  const msg = document.createElement("div");
  msg.className = "message " + sender;
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function getReply(prompt) {
  // In production, you'd call your backend Flask or Render API here.
  // For now, return a mock reply:
  if (prompt.toLowerCase().includes("apr")) {
    return "APR stands for Annual Percentage Rate 💡 — it’s the total cost of borrowing over a year.";
  } else {
    return "Hmm 🤔 I’m still learning that one. Try asking about loans, APR, or how to calculate interest!";
  }
}

// 3D Ivy model (Three.js)
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.module.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.150.1/examples/jsm/loaders/GLTFLoader.js';

const container = document.getElementById("model-container");

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

const loader = new GLTFLoader();
loader.load('/static/ivy-model.glb', (gltf) => {
  const model = gltf.scene;
  model.scale.set(1.5, 1.5, 1.5);
  scene.add(model);

  function animate() {
    requestAnimationFrame(animate);
    model.rotation.y += 0.01;
    renderer.render(scene, camera);
  }

  animate();
});
