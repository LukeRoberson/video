/**
 * @fileoverview Profile editing functionality for user profiles.
 * Handles renaming profiles, changing profile pictures, displaying watch history,
 * and managing watch history items.
 */

/**
 * Configuration constants for profile editing
 * @readonly
 * @enum {string}
 */
const ProfileEditConfig = {
    /** API endpoint for profile pictures */
    PROFILE_PICTURES_ENDPOINT: '/api/profile/pictures',
    /** API endpoint pattern for profile deletion */
    DELETE_PROFILE_ENDPOINT: '/api/profile/delete/{id}',
    /** API endpoint pattern for profile updates */
    UPDATE_PROFILE_ENDPOINT: '/api/profile/update/{id}',
    /** API endpoint pattern for clearing history */
    CLEAR_HISTORY_ENDPOINT: '/api/profile/clear_history/{id}',
    /** API endpoint for marking videos as watched */
    MARK_WATCHED_ENDPOINT: '/api/profile/mark_watched',
    /** Content type for JSON requests */
    JSON_CONTENT_TYPE: 'application/json',
    /** Profile pictures directory path */
    PROFILE_PICS_PATH: '/static/img/profiles/'
};

/**
 * Handles profile picture carousel functionality in the modal
 * @class ProfilePictureManager
 */
class ProfilePictureManager {
    /**
     * Create a ProfilePictureManager instance
     * @memberof ProfilePictureManager
     */
    constructor() {
        /**
         * Loading spinner element
         * @type {HTMLElement}
         */
        this.loading = document.getElementById('modalLoading');
        
        /**
         * Carousel container element
         * @type {HTMLElement}
         */
        this.carousel = document.getElementById('modalProfilePicCarousel');
        
        /**
         * Carousel inner container
         * @type {HTMLElement}
         */
        this.carouselInner = this.carousel?.querySelector('.carousel-inner');
        
        /**
         * Previous button element
         * @type {HTMLElement}
         */
        this.prevBtn = document.querySelector('.carousel-control-prev');
        
        /**
         * Next button element
         * @type {HTMLElement}
         */
        this.nextBtn = document.querySelector('.carousel-control-next');
        
        /**
         * Confirm selection button
         * @type {HTMLElement}
         */
        this.confirmBtn = document.getElementById('confirmPicSelection');
    }

    /**
     * Load available profile pictures into the modal carousel
     * @async
     * @memberof ProfilePictureManager
     */
    async loadProfilePictures() {
        // Only load if not already loaded
        if (this.carouselInner.children.length > 0) {
            this.showCarousel();
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(ProfileEditConfig.PROFILE_PICTURES_ENDPOINT);
            const data = await response.json();
            
            const profileData = ProfileDataManager.getProfileData();
            this.populateCarousel(data.profile_pics, profileData.image);
            this.showCarousel();
            
        } catch (error) {
            console.error('Error loading profile pictures:', error);
            this.showError('Failed to load images');
        }
    }

    /**
     * Show loading spinner and hide carousel
     * @private
     * @memberof ProfilePictureManager
     */
    showLoading() {
        this.loading.classList.add('d-flex');
        this.loading.style.display = 'flex';
        this.carousel.style.display = 'none';
        this.prevBtn.style.display = 'none';
        this.nextBtn.style.display = 'none';
        this.confirmBtn.disabled = true;
    }

    /**
     * Show carousel and hide loading spinner
     * @private
     * @memberof ProfilePictureManager
     */
    showCarousel() {
        this.loading.classList.remove('d-flex');
        this.loading.style.display = 'none';
        this.carousel.style.display = 'block';
        this.prevBtn.style.display = 'block';
        this.nextBtn.style.display = 'block';
        this.confirmBtn.disabled = false;
    }

    /**
     * Show error message in loading area
     * @param {string} message - Error message to display
     * @private
     * @memberof ProfilePictureManager
     */
    showError(message) {
        this.loading.innerHTML = `<div class="text-danger">${message}</div>`;
    }

    /**
     * Populate carousel with profile picture options
     * @param {Array<string>} profilePics - Array of profile picture filenames
     * @param {string} currentImage - Currently selected image filename
     * @private
     * @memberof ProfilePictureManager
     */
    populateCarousel(profilePics, currentImage) {
        this.carouselInner.innerHTML = '';
        let hasActiveItem = false;

        profilePics.forEach((pic) => {
            const isActive = pic === currentImage;
            if (isActive) hasActiveItem = true;

            const carouselItem = this.createCarouselItem(pic, isActive);
            this.carouselInner.appendChild(carouselItem);
        });

        // If no item was marked as active, make the first one active
        if (!hasActiveItem && this.carouselInner.children.length > 0) {
            this.carouselInner.children[0].classList.add('active');
        }
    }

    /**
     * Create a carousel item element
     * @param {string} pic - Profile picture filename
     * @param {boolean} isActive - Whether this item should be active
     * @returns {HTMLElement} Carousel item element
     * @private
     * @memberof ProfilePictureManager
     */
    createCarouselItem(pic, isActive) {
        const carouselItem = document.createElement('div');
        carouselItem.className = `carousel-item ${isActive ? 'active selected' : ''}`;
        carouselItem.setAttribute('data-pic', pic);
        
        const img = document.createElement('img');
        img.src = `${ProfileEditConfig.PROFILE_PICS_PATH}${pic}`;
        img.alt = pic;
        img.className = 'd-block w-100 profile-pic-option';
        
        carouselItem.appendChild(img);
        return carouselItem;
    }

    /**
     * Confirm the selected profile picture
     * @memberof ProfilePictureManager
     */
    confirmSelection() {
        const activeItem = document.querySelector('#modalProfilePicCarousel .carousel-item.active');
        if (!activeItem) return;

        const selectedPic = activeItem.getAttribute('data-pic');
        
        // Update the main profile image
        const profileAvatar = document.getElementById('profileAvatar');
        profileAvatar.src = `${ProfileEditConfig.PROFILE_PICS_PATH}${selectedPic}`;
        profileAvatar.setAttribute('data-selected-image', selectedPic);
        
        // Close the modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('profilePicModal'));
        modal.hide();
    }
}

/**
 * Manages profile data extraction and validation
 * @class ProfileDataManager
 */
class ProfileDataManager {
    /**
     * Get profile data from DOM data attributes
     * @static
     * @returns {Object} Profile data object
     * @returns {number} returns.id - Profile ID
     * @returns {string} returns.image - Current profile image filename
     * @memberof ProfileDataManager
     */
    static getProfileData() {
        const container = document.querySelector('.edit-profile');
        
        if (!container) {
            throw new Error('Profile container not found');
        }

        return {
            id: parseInt(container.dataset.profileId),
            image: container.dataset.profileImage
        };
    }

    /**
     * Validate profile name input
     * @static
     * @param {string} name - Profile name to validate
     * @returns {boolean} True if valid
     * @memberof ProfileDataManager
     */
    static validateProfileName(name) {
        return name && name.trim().length > 0;
    }
}

/**
 * Handles API calls for profile operations
 * @class ProfileApiService
 */
class ProfileApiService {
    /**
     * Delete a profile
     * @static
     * @async
     * @param {number} profileId - ID of profile to delete
     * @returns {Promise<void>}
     * @memberof ProfileApiService
     */
    static async deleteProfile(profileId) {
        const endpoint = ProfileEditConfig.DELETE_PROFILE_ENDPOINT.replace('{id}', profileId);
        
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to delete profile');
        }
    }

    /**
     * Update a profile
     * @static
     * @async
     * @param {number} profileId - ID of profile to update
     * @param {Object} profileData - Profile data to update
     * @param {string} profileData.name - Profile name
     * @param {string} profileData.icon - Profile icon filename
     * @returns {Promise<void>}
     * @memberof ProfileApiService
     */
    static async updateProfile(profileId, profileData) {
        const endpoint = ProfileEditConfig.UPDATE_PROFILE_ENDPOINT.replace('{id}', profileId);
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            body: JSON.stringify(profileData)
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to update profile');
        }
    }

    /**
     * Clear entire watch history for a profile
     * @static
     * @async
     * @param {number} profileId - ID of profile
     * @returns {Promise<void>}
     * @memberof ProfileApiService
     */
    static async clearHistory(profileId) {
        const endpoint = ProfileEditConfig.CLEAR_HISTORY_ENDPOINT.replace('{id}', profileId);
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to clear history');
        }
    }

    /**
     * Clear a single item from watch history
     * @static
     * @async
     * @param {number} profileId - ID of profile
     * @param {number} videoId - ID of video to remove from history
     * @returns {Promise<void>}
     * @memberof ProfileApiService
     */
    static async clearHistoryItem(profileId, videoId) {
        const endpoint = ProfileEditConfig.CLEAR_HISTORY_ENDPOINT.replace('{id}', profileId);
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            body: JSON.stringify({ video_id: videoId })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to remove item');
        }
    }

    /**
     * Mark a video as watched
     * @static
     * @async
     * @param {number} videoId - ID of video to mark as watched
     * @returns {Promise<void>}
     * @memberof ProfileApiService
     */
    static async markWatched(videoId) {
        const response = await fetch(ProfileEditConfig.MARK_WATCHED_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            body: JSON.stringify({ video_id: videoId })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to mark as watched');
        }
    }
}

/**
 * Main controller for profile editing functionality
 * @class ProfileEditController
 */
class ProfileEditController {
    /**
     * Create a ProfileEditController instance
     * @memberof ProfileEditController
     */
    constructor() {
        /**
         * Profile picture manager instance
         * @type {ProfilePictureManager}
         */
        this.pictureManager = new ProfilePictureManager();
        
        this.init();
    }

    /**
     * Initialize the profile edit controller
     * @memberof ProfileEditController
     */
    init() {
        this.setupEventListeners();
    }

    /**
     * Set up all event listeners
     * @private
     * @memberof ProfileEditController
     */
    setupEventListeners() {
        this.setupButtonListeners();
        this.setupModalListeners();
        this.setupHistoryListeners();
    }

    /**
     * Set up main button event listeners
     * @private
     * @memberof ProfileEditController
     */
    setupButtonListeners() {
        const saveBtn = document.querySelector('.btn-save');
        const deleteBtn = document.querySelector('.btn-delete');
        const editBtn = document.querySelector('.edit-icon');

        saveBtn?.addEventListener('click', () => this.handleSaveProfile());
        deleteBtn?.addEventListener('click', () => this.handleDeleteProfile());
        editBtn?.addEventListener('click', () => this.handleEditAvatar());
    }

    /**
     * Set up modal event listeners
     * @private
     * @memberof ProfileEditController
     */
    setupModalListeners() {
        const modal = document.getElementById('profilePicModal');
        const confirmBtn = document.getElementById('confirmPicSelection');

        modal?.addEventListener('shown.bs.modal', () => {
            this.pictureManager.loadProfilePictures();
        });

        confirmBtn?.addEventListener('click', () => {
            this.pictureManager.confirmSelection();
        });
    }

    /**
     * Set up watch history event listeners
     * @private
     * @memberof ProfileEditController
     */
    setupHistoryListeners() {
        const clearAllBtn = document.querySelector('.btn-clear-all');
        clearAllBtn?.addEventListener('click', () => this.handleClearHistory());

        document.querySelectorAll('.btn-remove-item').forEach(button => {
            button.addEventListener('click', () => this.handleClearHistoryItem(button));
        });

        document.querySelectorAll('.btn-mark-watched').forEach(button => {
            button.addEventListener('click', () => this.handleMarkWatched(button));
        });
    }

    /**
     * Handle profile deletion with confirmation
     * @async
     * @private
     * @memberof ProfileEditController
     */
    async handleDeleteProfile() {
        if (!confirm('Are you sure you want to delete this profile? This action cannot be undone.')) {
            return;
        }

        try {
            const profileData = ProfileDataManager.getProfileData();
            await ProfileApiService.deleteProfile(profileData.id);
            window.location.href = '/';
        } catch (error) {
            console.error('Error deleting profile:', error);
            alert('Failed to delete profile: ' + error.message);
        }
    }

    /**
     * Handle profile save operation
     * @async
     * @private
     * @memberof ProfileEditController
     */
    async handleSaveProfile() {
        try {
            const profileData = ProfileDataManager.getProfileData();
            const profileNameInput = document.querySelector('.profile-name-input');
            const profileName = profileNameInput.value.trim();

            if (!ProfileDataManager.validateProfileName(profileName)) {
                alert('Profile name is required');
                return;
            }

            const profileAvatar = document.getElementById('profileAvatar');
            const selectedImage = profileAvatar.getAttribute('data-selected-image') || profileData.image;

            const updateData = {
                name: profileName,
                icon: selectedImage
            };

            await ProfileApiService.updateProfile(profileData.id, updateData);
            window.location.href = '/';
        } catch (error) {
            console.error('Error updating profile:', error);
            alert('Failed to update profile: ' + error.message);
        }
    }

    /**
     * Handle avatar edit button click
     * @private
     * @memberof ProfileEditController
     */
    handleEditAvatar() {
        const modal = new bootstrap.Modal(document.getElementById('profilePicModal'));
        modal.show();
    }

    /**
     * Handle clearing entire watch history
     * @async
     * @private
     * @memberof ProfileEditController
     */
    async handleClearHistory() {
        try {
            const profileData = ProfileDataManager.getProfileData();
            await ProfileApiService.clearHistory(profileData.id);
            
            const clearAllBtn = document.querySelector('.btn-clear-all');
            clearAllBtn.disabled = true;
            clearAllBtn.textContent = 'Removed';
        } catch (error) {
            console.error('Error clearing history:', error);
            alert('Failed to clear history: ' + error.message);
        }
    }

    /**
     * Handle clearing individual history item
     * @async
     * @param {HTMLElement} button - Button that was clicked
     * @private
     * @memberof ProfileEditController
     */
    async handleClearHistoryItem(button) {
        try {
            const profileData = ProfileDataManager.getProfileData();
            const videoId = parseInt(button.getAttribute('data-video-id'));
            
            await ProfileApiService.clearHistoryItem(profileData.id, videoId);
            
            button.disabled = true;
            button.textContent = 'Removed';
        } catch (error) {
            console.error('Error removing item:', error);
            alert('Failed to remove item: ' + error.message);
        }
    }

    /**
     * Handle marking video as watched
     * @async
     * @param {HTMLElement} button - Button that was clicked
     * @private
     * @memberof ProfileEditController
     */
    async handleMarkWatched(button) {
        try {
            const videoId = parseInt(button.getAttribute('data-video-id'));
            await ProfileApiService.markWatched(videoId);
            
            button.disabled = true;
            button.textContent = 'Watched';
        } catch (error) {
            console.error('Error marking as watched:', error);
            alert('Failed to mark as watched: ' + error.message);
        }
    }
}

// Global controller instance
let profileEditController;

/**
 * Initialize profile edit functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    profileEditController = new ProfileEditController();
});