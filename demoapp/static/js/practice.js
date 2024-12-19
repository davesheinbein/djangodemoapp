function openModal(url) {
	console.log('🚀 ~ url:', url);
	fetch(url)
		.then((response) => response.json())
		.then((data) => {
			if (data.success) {
				const modalBody =
					document.getElementById('modal-body');
				if (modalBody) {
					modalBody.innerHTML = data.html;
					document.getElementById('modal').style.display =
						'block';
				}
			}
		})
		.catch((error) => {
			console.error('Error:', error);
		});
}

function closeModal() {
	const modal = document.getElementById('modal');
	if (modal) {
		modal.style.display = 'none';
	}
}

function submitForm(event, url) {
	event.preventDefault();
	const form = event.target;
	const formData = new FormData(form);
	fetch(url, {
		method: 'POST',
		body: formData,
		headers: {
			'X-CSRFToken': form.querySelector(
				'[name=csrfmiddlewaretoken]'
			).value,
		},
	})
		.then((response) => response.json())
		.then((data) => {
			if (data.success) {
				const profileList =
					document.querySelector('.practice ul');
				const newProfile = document.createElement('li');
				newProfile.innerHTML = `${data.profile.username} - ${data.profile.bio}`;
				profileList.appendChild(newProfile);
				closeModal();
			} else {
				// Handle form errors
				const errors = data.errors;
				for (const [field, messages] of Object.entries(
					errors
				)) {
					const errorElement = form.querySelector(
						`[name=${field}]`
					).nextElementSibling;
					errorElement.innerHTML = messages.join(', ');
				}
			}
		})
		.catch((error) => {
			console.error('Error:', error);
		});
}

function updateProfile(event, url) {
	event.preventDefault();
	const form = event.target;
	const formData = new FormData(form);
	const data = {};
	formData.forEach((value, key) => {
		data[key] = value;
	});
	fetch(url, {
		method: 'PUT',
		body: JSON.stringify(data),
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': form.querySelector(
				'[name=csrfmiddlewaretoken]'
			).value,
		},
	})
		.then((response) => response.json())
		.then((data) => {
			if (data.success) {
				const profileList =
					document.querySelector('.practice ul');
				const profileItem = profileList.querySelector(
					`li[data-id="${data.profile.id}"]`
				);
				profileItem.innerHTML = `${data.profile.username} - ${data.profile.bio}`;
				closeModal();
			} else {
				// Handle form errors
				const errors = data.errors;
				for (const [field, messages] of Object.entries(
					errors
				)) {
					const errorElement = form.querySelector(
						`[name=${field}]`
					).nextElementSibling;
					errorElement.innerHTML = messages.join(', ');
				}
			}
		})
		.catch((error) => {
			console.error('Error:', error);
		});
}

function editProfile(event, url) {
	event.preventDefault();
	const form = event.target;
	const formData = new FormData(form);
	fetch(url, {
		method: 'POST',
		body: formData,
		headers: {
			'X-CSRFToken': form.querySelector(
				'[name=csrfmiddlewaretoken]'
			).value,
		},
	})
		.then((response) => response.json())
		.then((data) => {
			if (data.success) {
				const profileList =
					document.querySelector('.practice ul');
				const profileItem = profileList.querySelector(
					`li[data-id="${data.profile.id}"]`
				);
				profileItem.innerHTML = `${data.profile.username} - ${data.profile.bio}`;
				closeModal();
			} else {
				// Handle form errors
				const errors = data.errors;
				for (const [field, messages] of Object.entries(
					errors
				)) {
					const errorElement = form.querySelector(
						`[name=${field}]`
					).nextElementSibling;
					errorElement.innerHTML = messages.join(', ');
				}
			}
		})
		.catch((error) => {
			console.error('Error:', error);
		});
}

function deleteProfile(profileId) {
	fetch(`/practice/delete_profile/${profileId}/`, {
		method: 'DELETE',
		headers: {
			'X-CSRFToken': '{{ csrf_token }}',
		},
	})
		.then((response) => response.json())
		.then((data) => {
			if (data.success) {
				const profileItem = document.querySelector(
					`li[data-id="${profileId}"]`
				);
				if (profileItem) {
					profileItem.remove();
				}
				console.log(data.message);
			} else {
				console.log('Error: ' + data.error);
			}
		})
		.catch((error) => {
			console.error('Error:', error);
		});
}

document.addEventListener('DOMContentLoaded', function () {
	const addCategoryForm = document.getElementById('addCategoryForm');
	if (addCategoryForm) {
		addCategoryForm.addEventListener('submit', function (event) {
			event.preventDefault();
			const formData = new FormData(this);
			fetch("{% url 'add_category' %}", {
				method: 'POST',
				body: formData,
				headers: {
					'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
				},
			})
				.then((response) => response.json())
				.then((data) => {
					if (data.success) {
						const categoryList = document.querySelector('.practice ul:nth-of-type(2)');
						const newCategory = document.createElement('li');
						newCategory.innerHTML = data.category.name;
						categoryList.appendChild(newCategory);
						closeModal();
					} else {
						console.error('Error: ' + JSON.stringify(data.errors));
					}
				})
				.catch((error) => {
					console.error('Error:', error);
				});
		});
	}

	const addTagForm = document.getElementById('addTagForm');
	if (addTagForm) {
		addTagForm.addEventListener('submit', function (event) {
			event.preventDefault();
			const formData = new FormData(this);
			fetch("{% url 'add_tag' %}", {
				method: 'POST',
				body: formData,
				headers: {
					'X-CSRFToken': formData.get(
						'csrfmiddlewaretoken'
					),
				},
			})
				.then((response) => response.json())
				.then((data) => {
					if (data.success) {
						console.error(data.message);
						location.reload();
					} else {
						console.error(
							'Error: ' + JSON.stringify(data.errors)
						);
					}
				})
				.catch((error) => {
					console.error('Error:', error);
				});
		});
	}

	// Close modal on escape key press
	document.addEventListener('keydown', function (event) {
		if (event.key === 'Escape') {
			closeModal();
		}
	});

	// Close modal on click outside of modal content
	document
		.getElementById('modal')
		.addEventListener('click', function (event) {
			if (event.target === this) {
				closeModal();
			}
		});
});

function deleteArticle(articleId) {
	fetch(`/practice/delete_article/${articleId}/`, {
		method: 'DELETE',
		headers: {
			'X-CSRFToken': '{{ csrf_token }}',
		},
	})
		.then((response) => response.json())
		.then((data) => {
			if (data.success) {
				console.error(data.message);
				location.reload();
			} else {
				console.error('Error: ' + data.error);
			}
		})
		.catch((error) => {
			console.error('Error:', error);
		});
}
