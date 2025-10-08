/**
 * @fileoverview Profile editing functionality for user profiles.
 * Handles renaming profiles, changing profile pictures, displaying watch history,
 * and managing watch history items.
 */

/**
 * Configuration constants for profile editing
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
} as const;

/**
 * Interface for profile data from DOM
 */
interface ProfileEditData {
    id: number;
    image: string;
}

/**
 * Interface for profile pictures API response
 */
interface ProfilePicturesResponse {
    success: boolean;
    profile_pics: string[];
}

/**
 * Interface for API response
 */
interface ApiResponse {
    success: boolean;
    message?: string;
}

/**
 * Interface for profile update data
 */
interface ProfileUpdateData {
    name: string;
    icon: string;
}

/**
 * Interface for clear history item request
 */
interface ClearHistoryItemRequest {
    video_id: number;
}

/**
 * Interface for mark watched request
 */
interface MarkWatchedRequest {
    video_id: number;
}

/**
 * Bootstrap Modal interface
 */
interface BootstrapModal {
    show(): void;
    hide(): void;
}

/**
 * Declare bootstrap global
 */
declare const bootstrap: {
    Modal: {
        getInstance(element: HTMLElement): BootstrapModal | null;
        new(element: HTMLElement): BootstrapModal;
    };
};

/**
 * Handles profile picture carousel functionality in the modal
 */
class ProfilePictureManager {
    private loading: HTMLElement | null;
    private carousel: HTMLElement | null;
    private carouselInner: HTMLElement | null;
    private prevBtn: HTMLElement | null;
    private nextBtn: HTMLElement | null;
    private confirmBtn: HTMLButtonElement | null;

    /**
     * Create a ProfilePictureManager instance
     */
    constructor() {
        this.loading = document.getElementById('modalLoading');
        this.carousel = document.getElementById('modalProfilePicCarousel');
        this.carouselInner = this.carousel?.querySelector('.carousel-inner') || null;
        this.prevBtn = document.querySelector('.carousel-control-prev');
        this.nextBtn = document.querySelector('.carousel-control-next');
        this.confirmBtn = document.getElementById('confirmPicSelection') as HTMLButtonElement | null;
    }

    /**
     * Load available profile pictures into the modal carousel
     */
    async loadProfilePictures(): Promise<void> {
        // Only load if not already loaded
        if (this.carouselInner && this.carouselInner.children.length > 0) {
            this.showCarousel();
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(ProfileEditConfig.PROFILE_PICTURES_ENDPOINT);
            const data: ProfilePicturesResponse = await response.json();
            
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
     */
    private showLoading(): void {
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
    private showCarousel(): void {
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
    private showError(message: string): void {
        if (this.loading) {
            this.loading.innerHTML = `<div class="text-danger">${message}</div>`;
        }
    }

    /**
     * Populate carousel with profile picture options
     * @param profilePics - Array of profile picture filenames
     * @param currentImage - Currently selected image filename
     */
    private populateCarousel(profilePics: string[], currentImage: string): void {
        if (!this.carouselInner) return;
        
        this.carouselInner.innerHTML = '';
        let hasActiveItem = false;

        profilePics.forEach((pic) => {
            const isActive = pic === currentImage;
            if (isActive) hasActiveItem = true;

            const carouselItem = this.createCarouselItem(pic, isActive);
            this.carouselInner!.appendChild(carouselItem);
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
    private createCarouselItem(pic: string, isActive: boolean): HTMLElement {
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
    confirmSelection(): void {
        const activeItem = document.querySelector('#modalProfilePicCarousel .carousel-item.active');
        if (!activeItem) return;

        const selectedPic = activeItem.getAttribute('data-pic');
        if (!selectedPic) return;
        
        // Update the main profile image
        const profileAvatar = document.getElementById('profileAvatar') as HTMLImageElement;
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
 */
class ProfileDataManager {
    /**
     * Get profile data from DOM data attributes
     * @returns Profile data object
     */
    static getProfileData(): ProfileEditData {
        const container = document.querySelector('.edit-profile') as HTMLElement;
        
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
    static validateProfileName(name: string): boolean {
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
    static async deleteProfile(profileId: number): Promise<void> {
        const endpoint = ProfileEditConfig.DELETE_PROFILE_ENDPOINT.replace('{id}', profileId.toString());
        
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            }
        });

        if (!response.ok) {
            const data: ApiResponse = await response.json();
            throw new Error(data.message || 'Failed to delete profile');
        }
    }

    /**
     * Update a profile
     * @param profileId - ID of profile to update
     * @param profileData - Profile data to update
     */
    static async updateProfile(profileId: number, profileData: ProfileUpdateData): Promise<void> {
        const endpoint = ProfileEditConfig.UPDATE_PROFILE_ENDPOINT.replace('{id}', profileId.toString());
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            body: JSON.stringify(profileData)
        });

        if (!response.ok) {
            const data: ApiResponse = await response.json();
            throw new Error(data.message || 'Failed to update profile');
        }
    }

    /**
     * Clear entire watch history for a profile
     * @param profileId - ID of profile
     */
    static async clearHistory(profileId: number): Promise<void> {
        const endpoint = ProfileEditConfig.CLEAR_HISTORY_ENDPOINT.replace('{id}', profileId.toString());
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            }
        });

        if (!response.ok) {
            const data: ApiResponse = await response.json();
            throw new Error(data.message || 'Failed to clear history');
        }
    }

    /**
     * Clear a single item from watch history
     * @param profileId - ID of profile
     * @param videoId - ID of video to remove from history
     */
    static async clearHistoryItem(profileId: number, videoId: number): Promise<void> {
        const endpoint = ProfileEditConfig.CLEAR_HISTORY_ENDPOINT.replace('{id}', profileId.toString());
        
        const requestBody: ClearHistoryItemRequest = { video_id: videoId };
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const data: ApiResponse = await response.json();
            throw new Error(data.message || 'Failed to remove item');
        }
    }

    /**
     * Mark a video as watched
     * @param videoId - ID of video to mark as watched
     */
    static async markWatched(videoId: number): Promise<void> {
        const requestBody: MarkWatchedRequest = { video_id: videoId };
        
        const response = await fetch(ProfileEditConfig.MARK_WATCHED_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileEditConfig.JSON_CONTENT_TYPE
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const data: ApiResponse = await response.json();
            throw new Error(data.message || 'Failed to mark as watched');
        }
    }
}

/**
 * Main controller for profile editing functionality
 */
class ProfileEditController {
    private pictureManager: ProfilePictureManager;

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
    private init(): void {
        this.setupEventListeners();
    }

    /**
     * Set up all event listeners
     */
    private setupEventListeners(): void {
        this.setupButtonListeners();
        this.setupModalListeners();
        this.setupHistoryListeners();
    }

    /**
     * Set up main button event listeners
     */
    private setupButtonListeners(): void {
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
    private setupModalListeners(): void {
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
    private setupHistoryListeners(): void {
        const clearAllBtn = document.querySelector('.btn-clear-all');
        clearAllBtn?.addEventListener('click', () => this.handleClearHistory());

        document.querySelectorAll('.btn-remove-item').forEach(button => {
            button.addEventListener('click', () => this.handleClearHistoryItem(button as HTMLElement));
        });

        document.querySelectorAll('.btn-mark-watched').forEach(button => {
            button.addEventListener('click', () => this.handleMarkWatched(button as HTMLElement));
        });
    }

    /**
     * Handle profile deletion with confirmation
     */
    private async handleDeleteProfile(): Promise<void> {
        if (!confirm('Are you sure you want to delete this profile? This action cannot be undone.')) {
            return;
        }

        try {
            const profileData = ProfileDataManager.getProfileData();
            await ProfileEditApiService.deleteProfile(profileData.id);
            window.location.href = '/';
        } catch (error) {
            console.error('Error deleting profile:', error);
            alert('Failed to delete profile: ' + (error as Error).message);
        }
    }

    /**
     * Handle profile save operation
     */
    private async handleSaveProfile(): Promise<void> {
        try {
            const profileData = ProfileDataManager.getProfileData();
            const profileNameInput = document.querySelector('.profile-name-input') as HTMLInputElement;
            const profileName = profileNameInput.value.trim();

            if (!ProfileDataManager.validateProfileName(profileName)) {
                alert('Profile name is required');
                return;
            }

            const profileAvatar = document.getElementById('profileAvatar') as HTMLImageElement;
            const selectedImage = profileAvatar.getAttribute('data-selected-image') || profileData.image;

            const updateData: ProfileUpdateData = {
                name: profileName,
                icon: selectedImage
            };

            await ProfileEditApiService.updateProfile(profileData.id, updateData);
            window.location.href = '/';
        } catch (error) {
            console.error('Error updating profile:', error);
            alert('Failed to update profile: ' + (error as Error).message);
        }
    }

    /**
     * Handle avatar edit button click
     */
    private handleEditAvatar(): void {
        const modalElement = document.getElementById('profilePicModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    }

    /**
     * Handle clearing entire watch history
     */
    private async handleClearHistory(): Promise<void> {
        try {
            const profileData = ProfileDataManager.getProfileData();
            await ProfileEditApiService.clearHistory(profileData.id);
            
            const clearAllBtn = document.querySelector('.btn-clear-all') as HTMLButtonElement;
            if (clearAllBtn) {
                clearAllBtn.disabled = true;
                clearAllBtn.textContent = 'Removed';
            }
        } catch (error) {
            console.error('Error clearing history:', error);
            alert('Failed to clear history: ' + (error as Error).message);
        }
    }

    /**
     * Handle clearing individual history item
     * @param button - Button that was clicked
     */
    private async handleClearHistoryItem(button: HTMLElement): Promise<void> {
        try {
            const profileData = ProfileDataManager.getProfileData();
            const videoId = parseInt(button.getAttribute('data-video-id') || '0');
            
            await ProfileEditApiService.clearHistoryItem(profileData.id, videoId);
            
            const btn = button as HTMLButtonElement;
            btn.disabled = true;
            btn.textContent = 'Removed';
        } catch (error) {
            console.error('Error removing item:', error);
            alert('Failed to remove item: ' + (error as Error).message);
        }
    }

    /**
     * Handle marking video as watched
     * @param button - Button that was clicked
     */
    private async handleMarkWatched(button: HTMLElement): Promise<void> {
        try {
            const videoId = parseInt(button.getAttribute('data-video-id') || '0');
            await ProfileEditApiService.markWatched(videoId);
            
            const btn = button as HTMLButtonElement;
            btn.disabled = true;
            btn.textContent = 'Watched';
        } catch (error) {
            console.error('Error marking as watched:', error);
            alert('Failed to mark as watched: ' + (error as Error).message);
        }
    }
}

// Global controller instance
let profileEditController: ProfileEditController;

/**
 * Initialize profile edit functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    profileEditController = new ProfileEditController();
});
