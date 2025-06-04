// static/GLTFLoader.js (used as a bridge for loading via module)
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.module.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.149.0/examples/jsm/loaders/GLTFLoader.js';

window.THREE = window.THREE || {};
window.THREE.GLTFLoader = GLTFLoader;
