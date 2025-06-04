/**
 * @author Don McCurdy / https://www.donmccurdy.com
 */

THREE.GLTFLoader = (function () {

	function GLTFLoader(manager) {
		this.manager = (manager !== undefined) ? manager : THREE.DefaultLoadingManager;
		this.dracoLoader = null;
	}

	GLTFLoader.prototype.load = function (url, onLoad, onProgress, onError) {
		const scope = this;
		const loader = new THREE.FileLoader(scope.manager);
		loader.setResponseType('arraybuffer');
		loader.load(url, function (data) {
			try {
				scope.parse(data, url, onLoad);
			} catch (e) {
				if (onError) {
					onError(e);
				} else {
					throw e;
				}
			}
		}, onProgress, onError);
	};

	GLTFLoader.prototype.setDRACOLoader = function (dracoLoader) {
		this.dracoLoader = dracoLoader;
	};

	GLTFLoader.prototype.parse = function (data, path, onLoad) {
		const json = JSON.parse(new TextDecoder().decode(data));
		const scene = new THREE.Group();

		if (json.nodes && Array.isArray(json.nodes)) {
			json.nodes.forEach((node, i) => {
				const mesh = new THREE.Mesh(
					new THREE.BoxGeometry(1, 1, 1),
					new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true })
				);
				mesh.name = node.name || `Box_${i}`;
				mesh.position.x = i * 1.5;
				scene.add(mesh);
			});
		}

		onLoad(scene);
	};

	return GLTFLoader;

})();
