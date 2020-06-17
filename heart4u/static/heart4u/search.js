document.addEventListener('DOMContentLoaded', () => {

	// resize profile pic to circle for search results
	document.querySelectorAll('.user-pic').forEach((user) => {
		container = user.children[0];
		pic = user.children[0].children[0];

		if (pic.width===pic.height) {
			container.className = 'user-pic-square';
		}
		else if (pic.width>pic.height) {
			container.className = 'user-pic-landscape';
		}
		else if (pic.width<pic.height) {
			container.className = 'user-pic-portrait';
		};
	});

});