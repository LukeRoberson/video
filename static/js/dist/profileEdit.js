"use strict";
/**
 * @fileoverview Profile editing functionality for user profiles.
 * Handles renaming profiles, changing profile pictures, displaying watch history,
 * and managing watch history items.
 */
/**
 * Configuration constants for profile editing
 */
const ProfileEditConfig = {
    /** API base URL for new endpoints (separate server) */
    API_BASE_URL: 'http://localhost:5010',
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
 */
class ProfilePictureManager {
    /**
     * Create a ProfilePictureManager instance
     */
    constructor() {
        this.loading = document.getElementById('modalLoading');
        this.carousel = document.getElementById('modalProfilePicCarousel');
        this.carouselInner = this.carousel?.querySelector('.carousel-inner') || null;
        this.prevBtn = document.querySelector('.carousel-control-prev');
        this.nextBtn = document.querySelector('.carousel-control-next');
        this.confirmBtn = document.getElementById('confirmPicSelection');
    }
    /**
     * Load available profile pictures into the modal carousel
     */
    async loadProfilePictures() {
        // Only load if not already loaded
        if (this.carouselInner && this.carouselInner.children.length > 0) {
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
        }
        catch (error) {
            console.error('Error loading profile pictures:', error);
            this.showError('Failed to load images');
        }
    }
    /**
     * Show loading spinner and hide carousel
     */
    showLoading() {
        if (this.loading) {
            this.loading.classList.add('d-flex');
            this.loading.style.display = 'flex';
        }
        if (this.carousel) {
            this.carousel.style.display = 'none';
        }
        if (this.prevBtn) {
            this.prevBtn.style.display = 'none';
        }
        if (this.nextBtn) {
            this.nextBtn.style.display = 'none';
        }
        if (this.confirmBtn) {
            this.confirmBtn.disabled = true;
        }
    }
    /**
     * Show carousel and hide loading spinner
     */
    showCarousel() {
        if (this.loading) {
            this.loading.classList.remove('d-flex');
            this.loading.style.display = 'none';
        }
        if (this.carousel) {
            this.carousel.style.display = 'block';
        }
        if (this.prevBtn) {
            this.prevBtn.style.display = 'block';
        }
        if (this.nextBtn) {
            this.nextBtn.style.display = 'block';
        }
        if (this.confirmBtn) {
            this.confirmBtn.disabled = false;
        }
    }
    /**
     * Show error message in loading area
     * @param message - Error message to display
     */
    showError(message) {
        if (this.loading) {
            this.loading.innerHTML = `<div class="text-danger">${message}</div>`;
        }
    }
    /**
     * Populate carousel with profile picture options
     * @param profilePics - Array of profile picture filenames
     * @param currentImage - Currently selected image filename
     */
    populateCarousel(profilePics, currentImage) {
        if (!this.carouselInner)
            return;
        this.carouselInner.innerHTML = '';
        let hasActiveItem = false;
        profilePics.forEach((pic) => {
            const isActive = pic === currentImage;
            if (isActive)
                hasActiveItem = true;
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
     * @param pic - Profile picture filename
     * @param isActive - Whether this item should be active
     * @returns Carousel item element
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
     */
    confirmSelection() {
        const activeItem = document.querySelector('#modalProfilePicCarousel .carousel-item.active');
        if (!activeItem)
            return;
        const selectedPic = activeItem.getAttribute('data-pic');
        if (!selectedPic)
            return;
        // Update the main profile image
        const profileAvatar = document.getElementById('profileAvatar');
        if (profileAvatar) {
            profileAvatar.src = `${ProfileEditConfig.PROFILE_PICS_PATH}${selectedPic}`;
            profileAvatar.setAttribute('data-selected-image', selectedPic);
        }
        // Close the modal
        const modalElement = document.getElementById('profilePicModal');
        if (modalElement) {
            const modal = bootstrap.Modal.getInstance(modalElement);
            modal?.hide();
        }
    }
}
/**
 * Manages profile data extraction and validation
 * This gets the active profile data from the DOM
 * This is set on the Jinja template as data attributes on the main container
 */
class ProfileDataManager {
    /**
     * Get profile data from DOM data attributes
     * @returns Profile data object
     */
    static getProfileData() {
        const container = document.querySelector('.edit-profile');
        if (!container) {
            throw new Error('Profile container not found');
        }
        return {
            id: parseInt(container.dataset.profileId || '0'),
            image: container.dataset.profileImage || ''
        };
    }
    /**
     * Validate profile name input
     * @param name - Profile name to validate
     * @returns True if valid
     */
    static validateProfileName(name) {
        return !!(name && name.trim().length > 0);
    }
}
/**
 * Handles API calls for profile operations
 */
class ProfileEditApiService {
    /**
     * Delete a profile
     * @param profileId - ID of profile to delete
     */
    static async deleteProfile(profileId) {
        const endpoint = `${ProfileEditConfig.API_BASE_URL}${ProfileEditConfig.DELETE_PROFILE_ENDPOINT.replace('{id}', profileId.toString())}`;
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            credentials: 'include'
        });
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to delete profile');
        }
    }
    /**
     * Update a profile
     * @param profileId - ID of profile to update
     * @param profileData - Profile data to update
     */
    static async updateProfile(profileId, profileData) {
        const endpoint = `${ProfileEditConfig.API_BASE_URL}${ProfileEditConfig.UPDATE_PROFILE_ENDPOINT.replace('{id}', profileId.toString())}`;
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            credentials: 'include',
            body: JSON.stringify(profileData)
        });
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to update profile');
        }
    }
    /**
     * Clear entire watch history for a profile
     * @param profileId - ID of profile
     */
    static async clearHistory(profileId) {
        const endpoint = `${ProfileEditConfig.API_BASE_URL}${ProfileEditConfig.CLEAR_HISTORY_ENDPOINT.replace('{id}', profileId.toString())}`;
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            credentials: 'include'
        });
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to clear history');
        }
    }
    /**
     * Clear a single item from watch history
     * @param profileId - ID of profile
     * @param videoId - ID of video to remove from history
     */
    static async clearHistoryItem(profileId, videoId) {
        const endpoint = `${ProfileEditConfig.API_BASE_URL}${ProfileEditConfig.CLEAR_HISTORY_ENDPOINT.replace('{id}', profileId.toString())}`;
        const requestBody = { video_id: videoId };
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            credentials: 'include',
            body: JSON.stringify(requestBody)
        });
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to remove item');
        }
    }
    /**
     * Mark a video as watched
     * @param profileId - ID of profile
     * @param videoId - ID of video to mark as watched
     */
    static async markWatched(profileId, videoId) {
        const requestBody = { video_id: videoId };
        const response = await fetch(`${ProfileEditConfig.API_BASE_URL}${ProfileEditConfig.MARK_WATCHED_ENDPOINT}?profile=${profileId}`, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            credentials: 'include',
            body: JSON.stringify(requestBody)
        });
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to mark as watched');
        }
    }
}
/**
 * Main controller for profile editing functionality
 */
class ProfileEditController {
    /**
     * Create a ProfileEditController instance
     */
    constructor() {
        this.pictureManager = new ProfilePictureManager();
        this.init();
    }
    /**
     * Initialize the profile edit controller
     */
    init() {
        this.setupEventListeners();
    }
    /**
     * Set up all event listeners
     */
    setupEventListeners() {
        this.setupButtonListeners();
        this.setupModalListeners();
        this.setupHistoryListeners();
    }
    /**
     * Set up main button event listeners
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
     */
    async handleDeleteProfile() {
        if (!confirm('Are you sure you want to delete this profile? This action cannot be undone.')) {
            return;
        }
        try {
            const profileData = ProfileDataManager.getProfileData();
            await ProfileEditApiService.deleteProfile(profileData.id);
            window.location.href = '/';
        }
        catch (error) {
            console.error('Error deleting profile:', error);
            alert('Failed to delete profile: ' + error.message);
        }
    }
    /**
     * Handle profile save operation
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
            await ProfileEditApiService.updateProfile(profileData.id, updateData);
            window.location.href = '/';
        }
        catch (error) {
            console.error('Error updating profile:', error);
            alert('Failed to update profile: ' + error.message);
        }
    }
    /**
     * Handle avatar edit button click
     */
    handleEditAvatar() {
        const modalElement = document.getElementById('profilePicModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    }
    /**
     * Handle clearing entire watch history
     */
    async handleClearHistory() {
        try {
            // Get profile data for API call
            const profileData = ProfileDataManager.getProfileData();
            // API call to clear history
            await ProfileEditApiService.clearHistory(profileData.id);
            // Update the UI to reflect cleared history
            const watchHistoryList = document.getElementById('watchHistoryList');
            if (watchHistoryList)
                watchHistoryList.innerHTML = '';
            this.updateHistoryCount();
            // Update the 'Clear All' button to indicate history is cleared
            const clearAllBtn = document.querySelector('.btn-clear-all');
            if (clearAllBtn) {
                clearAllBtn.disabled = true;
                clearAllBtn.textContent = 'Removed';
            }
        }
        catch (error) {
            console.error('Error clearing history:', error);
            alert('Failed to clear history: ' + error.message);
        }
    }
    /**
     * Handle clearing individual history item
     * @param button - Button that was clicked
     */
    async handleClearHistoryItem(button) {
        try {
            // Get profile data and video ID for API call
            const profileData = ProfileDataManager.getProfileData();
            const videoId = parseInt(button.getAttribute('data-video-id') || '0');
            // API call to clear specific history item
            await ProfileEditApiService.clearHistoryItem(profileData.id, videoId);
            // Remove the history item from the DOM
            const historyItem = document.querySelector(`.history-item[data-video-id="${videoId}"]`);
            historyItem?.remove();
            this.updateHistoryCount();
        }
        catch (error) {
            console.error('Error removing item:', error);
            alert('Failed to remove item: ' + error.message);
        }
    }
    /**
     * Handle marking video as watched
     * @param button - Button that was clicked
     */
    async handleMarkWatched(button) {
        try {
            // Get data from the DOM
            const videoId = parseInt(button.getAttribute('data-video-id') || '0');
            const historyItem = document.querySelector(`.history-item[data-video-id="${videoId}"]`);
            // Get profile data for API call
            const profileData = ProfileDataManager.getProfileData();
            // Call API to mark as watched
            await ProfileEditApiService.markWatched(profileData.id, videoId);
            // Remove the progress bar from the history item
            if (historyItem) {
                historyItem.querySelector('.progress-bar')?.remove();
            }
            // Update the button to indicate it's now watched
            const btn = button;
            btn.disabled = true;
            btn.textContent = 'Watched';
        }
        catch (error) {
            console.error('Error marking as watched:', error);
            alert('Failed to mark as watched: ' + error.message);
        }
    }
    /**
     * Update the watch history count display
     * Used when removing individual items from the history
     * This prevents the need for a full page reload
     */
    updateHistoryCount() {
        // Count remaining history items
        const remaining = document.querySelectorAll('#watchHistoryList .history-item').length;
        // Update UI if there are remaining items
        const countEl = document.querySelector('.history-count');
        if (countEl)
            countEl.textContent = `${remaining} videos watched recently`;
        // Update UI if there are no items left
        const emptyEl = document.getElementById('historyEmpty');
        if (emptyEl)
            emptyEl.style.display = remaining === 0 ? 'block' : 'none';
    }
}
// Global controller instance
let profileEditController;
/**
 * Initialize profile edit functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function () {
    profileEditController = new ProfileEditController();
});
//# sourceMappingURL=profileEdit.js.map