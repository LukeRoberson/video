"use strict";
/**
 * @fileoverview Profile management functionality for user profiles.
 * Handles creating new profiles, editing existing profiles, getting profile lists,
 * setting active profiles, and managing profile operations.
 */
/**
 * Configuration constants for profile management
 */
const ProfileMgmtConfig = {
    /** API base URL for new endpoints (separate server) */
    API_BASE_URL: 'http://localhost:5010',
    /** API base URL for legacy endpoints */
    LEGACY_API_BASE_URL: 'http://localhost:5000',
    /** API endpoint for creating profiles */
    CREATE_PROFILE_ENDPOINT: '/api/profile/create',
    /** API endpoint for getting active profile */
    GET_ACTIVE_ENDPOINT: '/api/profile/get_active',
    /** API endpoint for setting active profile */
    SET_ACTIVE_ENDPOINT: '/api/profile/set_active',
    /** API endpoint pattern for deleting profiles */
    DELETE_PROFILE_ENDPOINT: '/api/profile/delete/{id}',
    /** API endpoint pattern for editing profiles */
    EDIT_PROFILE_ENDPOINT: '/edit_profile/{id}',
    /** Content type for JSON requests */
    JSON_CONTENT_TYPE: 'application/json',
    /** Profile pictures directory path */
    PROFILE_PICS_PATH: '/static/img/profiles/',
    /** Default profile image */
    DEFAULT_PROFILE_IMAGE: 'guest.png',
    /** Default profile name */
    DEFAULT_PROFILE_NAME: 'Guest'
};
/**
 * Handles API calls for profile operations
 */
class ProfileApiService {
    /**
     * Create a new profile
     * @param profileData - Profile data
     * @returns API response data
     */
    static async createProfile(profileData) {
        const response = await fetch(ProfileMgmtConfig.CREATE_PROFILE_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileMgmtConfig.JSON_CONTENT_TYPE
            },
            body: JSON.stringify(profileData)
        });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    }
    /**
     * Get the currently active profile
     * @returns Active profile data
     */
    static async getActiveProfile() {
        const response = await fetch(`${ProfileMgmtConfig.API_BASE_URL}${ProfileMgmtConfig.GET_ACTIVE_ENDPOINT}`, {
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    }
    /**
     * Set a profile as active
     * @param profileData - Profile data
     * @returns API response data
     */
    static async setActiveProfile(profileData) {
        const url = `${ProfileMgmtConfig.API_BASE_URL}${ProfileMgmtConfig.SET_ACTIVE_ENDPOINT}`;
        console.log('Setting active profile with data:', profileData);
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': ProfileMgmtConfig.JSON_CONTENT_TYPE
            },
            credentials: 'include',
            body: JSON.stringify(profileData)
        });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    }
    /**
     * Delete a profile
     * @param profileId - Profile ID to delete
     * @returns API response data
     */
    static async deleteProfile(profileId) {
        const endpoint = ProfileMgmtConfig.DELETE_PROFILE_ENDPOINT.replace('{id}', profileId);
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': ProfileMgmtConfig.JSON_CONTENT_TYPE
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    }
}
/**
 * Handles profile creation form functionality
 */
class ProfileCreationHandler {
    /**
     * Create a ProfileCreationHandler instance
     * @param formId - ID of the profile creation form
     */
    constructor(formId = 'profile-create-form') {
        this.form = document.getElementById(formId);
        if (this.form) {
            this.setupEventListeners();
        }
    }
    /**
     * Set up form event listeners
     */
    setupEventListeners() {
        this.form?.addEventListener('submit', (e) => this.handleSubmit(e));
    }
    /**
     * Handle form submission
     * @param e - Form submit event
     */
    async handleSubmit(e) {
        console.log('Profile creation form submitted');
        e.preventDefault();
        try {
            const formData = this.extractFormData();
            const response = await ProfileApiService.createProfile(formData);
            console.log('Profile created:', response);
            this.redirectToProfileSelection();
        }
        catch (error) {
            console.error('Error creating profile:', error);
            alert('Failed to create profile: ' + error.message);
        }
    }
    /**
     * Extract form data
     * @returns Form data object
     */
    extractFormData() {
        const nameInput = document.getElementById('name');
        const imageInput = document.getElementById('profile_pic');
        return {
            name: nameInput.value,
            image: imageInput.value
        };
    }
    /**
     * Redirect to profile selection page
     */
    redirectToProfileSelection() {
        window.location.href = '/select_profile';
    }
}
/**
 * Manages active profile display in the UI
 */
class ActiveProfileManager {
    /**
     * Create an ActiveProfileManager instance
     */
    constructor() {
        this.profileNameElement = document.getElementById('profile-name');
        this.profileImageElement = document.getElementById('profile-img');
        this.loadActiveProfile();
    }
    /**
     * Load and display active profile information
     */
    async loadActiveProfile() {
        try {
            const response = await ProfileApiService.getActiveProfile();
            const activeProfile = response.data.active_profile;
            console.log('Active profile:', activeProfile.name);
            this.updateProfileDisplay(activeProfile);
        }
        catch (error) {
            console.error('Error loading active profile:', error);
            this.updateProfileDisplay({}); // Use defaults
        }
    }
    /**
     * Update profile display elements
     * @param profile - Profile data
     */
    updateProfileDisplay(profile) {
        if (this.profileNameElement) {
            this.profileNameElement.textContent = profile.name || ProfileMgmtConfig.DEFAULT_PROFILE_NAME;
        }
        if (this.profileImageElement) {
            const imageName = profile.image || ProfileMgmtConfig.DEFAULT_PROFILE_IMAGE;
            this.profileImageElement.src = ProfileMgmtConfig.PROFILE_PICS_PATH + imageName;
            this.profileImageElement.alt = profile.name || ProfileMgmtConfig.DEFAULT_PROFILE_NAME;
        }
    }
}
/**
 * Manages profile selection functionality
 */
class ProfileSelectionManager {
    /**
     * Create a ProfileSelectionManager instance
     */
    constructor() {
        this.profileItems = document.querySelectorAll('.list-group-item[data-profile-id]');
        this.setupEventListeners();
    }
    /**
     * Set up event listeners for profile selection
     */
    setupEventListeners() {
        this.profileItems.forEach(item => {
            item.addEventListener('click', (e) => this.handleProfileSelection(e, item));
        });
    }
    /**
     * Handle profile selection click
     * @param e - Click event
     * @param item - Profile list item element
     */
    async handleProfileSelection(e, item) {
        e.preventDefault();
        try {
            const profileData = this.extractProfileData(item);
            const response = await ProfileApiService.setActiveProfile(profileData);
            if (response.success) {
                this.redirectToNextPage();
            }
            else {
                throw new Error('Failed to set active profile');
            }
        }
        catch (error) {
            console.error('Error setting active profile:', error);
            alert('Failed to select profile: ' + error.message);
        }
    }
    /**
     * Extract profile data from list item
     * @param item - Profile list item element
     * @returns Profile data
     */
    extractProfileData(item) {
        const profileId = item.getAttribute('data-profile-id') || '';
        const profileAdmin = item.getAttribute('data-profile-admin') || '';
        console.log('Setting admin status:', profileAdmin);
        return {
            profile_id: profileId,
            profile_admin: profileAdmin
        };
    }
    /**
     * Redirect to next page or home
     */
    redirectToNextPage() {
        const params = new URLSearchParams(window.location.search);
        const nextUrl = params.get('next') || '/';
        window.location.href = nextUrl;
    }
}
/**
 * Handles profile operations like edit and delete
 */
class ProfileOperationsHandler {
    /**
     * Edit a profile by redirecting to edit page
     * @param profileId - Profile ID to edit
     * @param event - Click event to prevent bubbling
     */
    editProfile(profileId, event) {
        if (event) {
            event.stopPropagation();
            event.preventDefault();
        }
        console.log('Editing profile - Raw value:', profileId);
        console.log('Editing profile - Type:', typeof profileId);
        console.log('Editing profile - Is null/undefined?', profileId == null);
        if (!this.validateProfileId(profileId)) {
            console.error('Invalid profileId provided to editProfile function');
            alert('Error: Invalid profile ID');
            return;
        }
        const editUrl = ProfileMgmtConfig.EDIT_PROFILE_ENDPOINT.replace('{id}', profileId);
        console.log('Redirecting to:', editUrl);
        window.location.href = editUrl;
    }
    /**
     * Delete a profile with confirmation
     * @param profileId - Profile ID to delete
     */
    async deleteProfile(profileId) {
        console.log('Deleting profile:', profileId);
        if (!this.validateProfileId(profileId)) {
            alert('Error: Invalid profile ID');
            return;
        }
        if (!this.confirmDeletion()) {
            return;
        }
        try {
            const response = await ProfileApiService.deleteProfile(profileId);
            if (response.success) {
                console.log('Profile deleted successfully');
                window.location.reload();
            }
            else {
                throw new Error(response.message || 'Unknown error');
            }
        }
        catch (error) {
            console.error('Error deleting profile:', error);
            alert('An error occurred while deleting the profile: ' + error.message);
        }
    }
    /**
     * Validate profile ID
     * @param profileId - Profile ID to validate
     * @returns True if valid
     */
    validateProfileId(profileId) {
        return !!(profileId && profileId !== 'undefined' && profileId !== 'null' && profileId.trim() !== '');
    }
    /**
     * Show confirmation dialog for profile deletion
     * @returns True if user confirmed
     */
    confirmDeletion() {
        return confirm('Are you sure you want to delete this profile? This action cannot be undone.');
    }
}
/**
 * Main controller for profile management functionality
 */
class ProfileMgmtController {
    /**
     * Create a ProfileMgmtController instance
     */
    constructor() {
        this.creationHandler = new ProfileCreationHandler();
        this.activeProfileManager = new ActiveProfileManager();
        this.selectionManager = new ProfileSelectionManager();
        this.operationsHandler = new ProfileOperationsHandler();
        this.exposeGlobalFunctions();
        // Ensure handlers are initialized (prevents unused warning)
        void this.creationHandler;
        void this.activeProfileManager;
        void this.selectionManager;
    }
    /**
     * Expose functions globally for template usage
     */
    exposeGlobalFunctions() {
        window.editProfile = (profileId, event) => {
            this.operationsHandler.editProfile(profileId, event);
        };
        window.deleteProfile = (profileId) => {
            this.operationsHandler.deleteProfile(profileId);
        };
    }
    /**
     * Get the operations handler instance
     * @returns Operations handler
     */
    getOperationsHandler() {
        return this.operationsHandler;
    }
}
// Global controller instance
let profileMgmtController;
/**
 * Initialize profile management functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function () {
    profileMgmtController = new ProfileMgmtController();
});
//# sourceMappingURL=profileMgmt.js.map