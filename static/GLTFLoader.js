/**
 * @author Don McCurdy / https://www.donmccurdy.com
 */

THREE.GLTFLoader = function ( manager ) {

	this.manager = ( manager !== undefined ) ? manager : THREE.DefaultLoadingManager;

};

THREE.GLTFLoader.prototype = {

	constructor: THREE.GLTFLoader,

	load: function ( url, onLoad, onProgress, onError ) {

		const loader = new THREE.FileLoader( this.manager );
		loader.setResponseType( 'arraybuffer' );
		loader.load( url, ( data ) => {

			try {
				this.parse( data, url, onLoad );
			} catch ( e ) {
				if ( onError ) {
					onError( e );
				} else {
					throw e;
				}
			}

		}, onProgress, onError );

	},

	parse: function ( data, path, onLoad ) {
		// Simple fallback parser just to allow the app to run.
		// You can replace this with the full parser if needed.
		console.warn( '⚠️ GLTFLoader.parse() stub called — please implement or use a full version of GLTFLoader.' );
		onLoad( new THREE.Group() ); // empty fallback model
	}
};
