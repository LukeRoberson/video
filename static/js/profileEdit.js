/**
 * profileEdit.js
 * 
 * Handles editing of user profiles
 *  - Rename a profile
 *  - Change a profile picture
 *  - Display watch history
 *  - Manage watch history
 */


/**
 * Gets profile data from the DOM data attributes
 *  profile ID and current image
 * 
 * @returns {id: number, image: string} - The profile data
 */
function getProfileData() {
    const container = document.querySelector('.edit-profile');

    return {
        id: parseInt(container.dataset.profileId),
        image: container.dataset.profileImage
    };
}


/**
 * Loads available profile pictures into the modal carousel.
 * 
 * @returns {void}
 */
function loadProfilePictures() {
    // Loading spinner
    const loading = document.getElementById('modalLoading');

    // Carousel elements
    const carousel = document.getElementById('modalProfilePicCarousel');
    const carouselInner = carousel.querySelector('.carousel-inner');
    const prevBtn = document.querySelector('.carousel-control-prev');
    const nextBtn = document.querySelector('.carousel-control-next');
    const confirmBtn = document.getElementById('confirmPicSelection');
    
    // Only load if not already loaded
    if (carouselInner.children.length > 0) {
        loading.classList.remove('d-flex');
        loading.style.display = 'none';
        carousel.style.display = 'block';
        prevBtn.style.display = 'block';
        nextBtn.style.display = 'block';
        confirmBtn.disabled = false;
        return;
    }

    // Show spinner, hide carousel
    loading.classList.add('d-flex');
    loading.style.display = 'flex';
    carousel.style.display = 'none';
    prevBtn.style.display = 'none';
    nextBtn.style.display = 'none';
    confirmBtn.disabled = true;
    
    // Fetch available profile pictures
    fetch('/api/profile/pictures')
        .then(response => response.json())

        .then(data => {
            const profileData = getProfileData();
            const currentImage = profileData.image;
            
            // Clear existing content
            carouselInner.innerHTML = '';
            let hasActiveItem = false;

            // Create carousel items
            data.profile_pics.forEach((pic, index) => {
                const isActive = pic === currentImage;
                if (isActive) hasActiveItem = true;

                const carouselItem = document.createElement('div');
                carouselItem.className = `carousel-item ${isActive ? 'active selected' : ''}`;
                carouselItem.setAttribute('data-pic', pic);
                
                const img = document.createElement('img');
                img.src = `/static/img/profiles/${pic}`;
                img.alt = pic;
                img.className = 'd-block w-100 profile-pic-option';
                
                carouselItem.appendChild(img);
                carouselInner.appendChild(carouselItem);
            });

            // If no item was marked as active, make the first one active
            if (!hasActiveItem && carouselInner.children.length > 0) {
                carouselInner.children[0].classList.add('active');
            }

            // Hide loading, show carousel and controls
            loading.classList.remove('d-flex');
            loading.style.display = 'none';
            carousel.style.display = 'block';
            prevBtn.style.display = 'block';
            nextBtn.style.display = 'block';
            confirmBtn.disabled = false;
        })

        .catch(error => {
            console.error('Error loading profile pictures:', error);
            loading.innerHTML = '<div class="text-danger">Failed to load images</div>';
        });
}


/**
 * Deletes the current profile by making an API call.
 * On success, redirects to the home page.
 * On failure, displays an error message.
 */
function deleteProfile() {
    // Get profile ID
    const profileData = getProfileData();
    const profileId = profileData.id;
    
    // Make API call
    fetch(`/api/profile/delete/${profileId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })

    .then(response => {
        if (response.ok) {
            // Success - redirect to home page
            window.location.href = '/';
        } else {
            // Handle error
            return response.json().then(data => {
                throw new Error(data.message || 'Failed to delete profile');
            });
        }
    })

    .catch(error => {
        console.error('Error deleting profile:', error);
        alert('Failed to delete profile: ' + error.message);
    });
}


/**
 * Saves changes to the profile by making an API call.
 * On success, redirects to the home page.
 * On failure, displays an error message.
 * 
 * @returns {void}
 */
function saveProfile() {
    // Get profile ID
    const profileData = getProfileData();
    const profileId = profileData.id;

    // Get form data
    const profileNameInput = document.querySelector('.profile-name-input');
    const profileName = profileNameInput.value.trim();

    // Get selected image (either newly selected or current one)
    const profileAvatar = document.getElementById('profileAvatar');
    const selectedImage = profileAvatar.getAttribute('data-selected-image') || profileData.image;

    // Validate input
    if (!profileName) {
        alert('Profile name is required');
        return;
    }

    // JSON body
    const bodyData = {
        name: profileName,
        icon: selectedImage
    };

    // Make API call
    fetch(`/api/profile/update/${profileId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bodyData)
    })

    .then(response => {
        if (response.ok) {
            // Success - redirect to home page
            window.location.href = '/';
        } else {
            // Handle error
            return response.json().then(data => {
                throw new Error(data.message || 'Failed to update profile');
            });
        }
    })

    .catch(error => {
        console.error('Error updating profile:', error);
        alert('Failed to update profile: ' + error.message);
    });
}


/**
 * Clears the entire watch history for the current profile.
 * On success, updates the UI to reflect the cleared history.
 * On failure, displays an error message.
 * 
 * @returns {void}
 */
function clearHistory() {
    fetch('/api/profile/clear_history/{{ profile.id }}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })

    .then(response => {
        if (response.ok) {
            // Update UI to reflect Removed status
            clearAllBtn.disabled = true;
            clearAllBtn.textContent = 'Removed';
        } else {
            return response.json().then(data => {
                throw new Error(data.message || 'Failed to clear history');
            });
        }
    })
    
    .catch(error => {
        console.error('Error clearing history:', error);
        alert('Failed to clear history: ' + error.message);
    });
}


/**
 * Clears a single item from the watch history for the current profile.
 * On success, updates the UI to reflect the removed item.
 * 
 * @param {*} button 
 */
function clearHistoryItem(button) {
    // Get profile ID
    const profileData = getProfileData();
    const profileId = profileData.id;
    const videoId = button.getAttribute('data-video-id');

    // API call
    fetch(`/api/profile/clear_history/${profileId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_id: videoId })
    })

    .then(response => {
        if (response.ok) {
            // Update UI to reflect Removed status
            button.disabled = true;
            button.textContent = 'Removed';
        } else {
            return response.json().then(data => {
                throw new Error(data.message || 'Failed to remove item');
            });
        }
    })
    
    .catch(error => {
        console.error('Error removing item:', error);
        alert('Failed to remove item: ' + error.message);
    });
}


/**
 * Mark a video as watched for the current profile.
 * On success, updates the UI to reflect the watched status.
 * 
 * @param {*} button 
 */
function markWatched(button) {
    // Get the video ID
    const videoId = button.getAttribute('data-video-id');

    // API call
    fetch('/api/profile/mark_watched', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_id: videoId })
    })

    .then(response => {
        if (response.ok) {
            // Update UI to reflect watched status
            button.disabled = true;
            button.textContent = 'Watched';
        } else {
            return response.json().then(data => {
                throw new Error(data.message || 'Failed to mark as watched');
            });
        }
    })
    
    .catch(error => {
        console.error('Error marking as watched:', error);
        alert('Failed to mark as watched: ' + error.message);
    });
}


document.addEventListener('DOMContentLoaded', function() {
    // Get the buttons
    const saveBtn = document.querySelector('.btn-save');
    const deleteBtn = document.querySelector('.btn-delete');
    const editBtn = document.querySelector('.edit-icon');
    const clearAllBtn = document.querySelector('.btn-clear-all');
    
    // Delete button click handler
    deleteBtn.addEventListener('click', function() {
        // Show confirmation dialog
        if (confirm('Are you sure you want to delete this profile? This action cannot be undone.')) {
            deleteProfile();
        }
    });

    // Save button click handler
    saveBtn.addEventListener('click', function() {
        saveProfile();
    });

    // Edit icon click handler (for changing avatar)
    editBtn.addEventListener('click', function() {
        // Show the modal
        const modal = new bootstrap.Modal(document.getElementById('profilePicModal'));
        modal.show();
    });

    // Add modal event listener to load images when modal is shown
    document.getElementById('profilePicModal').addEventListener('shown.bs.modal', function() {
        loadProfilePictures();
    });

    // Clear all history button click handler
    clearAllBtn.addEventListener('click', function() {
        clearHistory();
    });

    // Clear individual item button click handler
    document.querySelectorAll('.btn-remove-item').forEach(button => {
        button.addEventListener('click', function() {
            clearHistoryItem(this);
        });
    });

    // Mark as watched button click handler
    document.querySelectorAll('.btn-mark-watched').forEach(button => {
        button.addEventListener('click', function() {
            markWatched(this);
        });
    });
    

});

document.getElementById('confirmPicSelection').addEventListener('click', function() {
    const activeItem = document.querySelector('#modalProfilePicCarousel .carousel-item.active');
    const selectedPic = activeItem.getAttribute('data-pic');
    
    // Update the main profile image
    document.getElementById('profileAvatar').src = `/static/img/profiles/${selectedPic}`;
    
    // Store the selection for saving later
    document.getElementById('profileAvatar').setAttribute('data-selected-image', selectedPic);
    
    // Close the modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('profilePicModal'));
    modal.hide();
});
