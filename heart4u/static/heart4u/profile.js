document.addEventListener('DOMContentLoaded', () => {

	// resize profile pic to circle on profile page
	container = document.getElementById('profile-pic').children[0];
	pic = document.getElementById('profile-pic').children[0].children[0];

	if (pic.width===pic.height) {
		container.className = 'profile-pic-square';
	}
	else if (pic.width>pic.height) {
		container.className = 'profile-pic-landscape';
	}
	else if (pic.width<pic.height) {
		container.className = 'profile-pic-portrait';
	};


	// resize profile pic to circle for followers/following modal
	$('#view-followers-modal').on('show.bs.modal', () => {
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


	// when show edit profile form, set inputs to user's details by default
	$('#edit-profile-modal').on('show.bs.modal', () => {
		document.getElementById('edit-username').value = document.getElementById('edit-username').dataset.value;
		document.getElementById('edit-firstname').value = document.getElementById('edit-firstname').dataset.value;
		document.getElementById('edit-lastname').value = document.getElementById('edit-lastname').dataset.value;
		document.getElementById('edit-bio').value = document.getElementById('edit-bio').dataset.value;
	});


	// when exit edit profile form without saving changes, reset inputs to user's original details
	$('#edit-profile-modal').on('hidden.bs.modal', () => {
		document.getElementById('edit-username').value = document.getElementById('edit-username').dataset.value;
		document.getElementById('edit-firstname').value = document.getElementById('edit-firstname').dataset.value;
		document.getElementById('edit-lastname').value = document.getElementById('edit-lastname').dataset.value;
		document.getElementById('edit-bio').value = document.getElementById('edit-bio').dataset.value;
	});


	// dismiss edit profile alert after set time
	setTimeout(() => {
		$('#edit-alert').alert('close');
    }, 3000);

});