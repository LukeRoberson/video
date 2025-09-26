/**
 * @fileoverview Profile management functionality for user profiles.
 * Handles creating new profiles, editing existing profiles, getting profile lists,
 * setting active profiles, and managing profile operations.
 */

/**
 * Configuration constants for profile management
 * @readonly
 * @enum {string}
 */
const ProfileMgmtConfig = {
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
 * @class ProfileApiService
 */
class ProfileApiService {
    /**
     * Create a new profile
     * @static
     * @async
     * @param {Object} profileData - Profile data
     * @param {string} profileData.name - Profile name
     * @param {string} profileData.image - Profile image filename
     * @returns {Promise<Object>} API response data
     * @memberof ProfileApiService
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
     * @static
     * @async
     * @returns {Promise<Object>} Active profile data
     * @memberof ProfileApiService
     */
    static async getActiveProfile() {
        const response = await fetch(ProfileMgmtConfig.GET_ACTIVE_ENDPOINT);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Set a profile as active
     * @static
     * @async
     * @param {Object} profileData - Profile data
     * @param {string} profileData.profile_id - Profile ID
     * @param {string} profileData.profile_admin - Profile admin status
     * @returns {Promise<Object>} API response data
     * @memberof ProfileApiService
     */
    static async setActiveProfile(profileData) {
        const response = await fetch(ProfileMgmtConfig.SET_ACTIVE_ENDPOINT, {
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
     * Delete a profile
     * @static
     * @async
     * @param {string} profileId - Profile ID to delete
     * @returns {Promise<Object>} API response data
     * @memberof ProfileApiService
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
 * @class ProfileCreationHandler
 */
class ProfileCreationHandler {
    /**
     * Create a ProfileCreationHandler instance
     * @param {string} formId - ID of the profile creation form
     * @memberof ProfileCreationHandler
     */
    constructor(formId = 'profile-create-form') {
        /**
         * Profile creation form element
         * @type {HTMLFormElement}
         */
        this.form = document.getElementById(formId);
        
        if (this.form) {
            this.setupEventListeners();
        }
    }

    /**
     * Set up form event listeners
     * @private
     * @memberof ProfileCreationHandler
     */
    setupEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    /**
     * Handle form submission
     * @async
     * @param {Event} e - Form submit event
     * @private
     * @memberof ProfileCreationHandler
     */
    async handleSubmit(e) {
        console.log('Profile creation form submitted');
        e.preventDefault();

        try {
            const formData = this.extractFormData();
            const response = await ProfileApiService.createProfile(formData);
            
            console.log('Profile created:', response);
            this.redirectToProfileSelection();
            
        } catch (error) {
            console.error('Error creating profile:', error);
            alert('Failed to create profile: ' + error.message);
        }
    }

    /**
     * Extract form data
     * @returns {Object} Form data object
     * @private
     * @memberof ProfileCreationHandler
     */
    extractFormData() {
        return {
            name: document.getElementById('name').value,
            image: document.getElementById('profile_pic').value
        };
    }

    /**
     * Redirect to profile selection page
     * @private
     * @memberof ProfileCreationHandler
     */
    redirectToProfileSelection() {
        window.location.href = '/select_profile';
    }
}

/**
 * Manages active profile display in the UI
 * @class ActiveProfileManager
 */
class ActiveProfileManager {
    /**
     * Create an ActiveProfileManager instance
     * @memberof ActiveProfileManager
     */
    constructor() {
        /**
         * Profile name display element
         * @type {HTMLElement}
         */
        this.profileNameElement = document.getElementById('profile-name');
        
        /**
         * Profile image display element
         * @type {HTMLImageElement}
         */
        this.profileImageElement = document.getElementById('profile-img');
        
        this.loadActiveProfile();
    }

    /**
     * Load and display active profile information
     * @async
     * @memberof ActiveProfileManager
     */
    async loadActiveProfile() {
        try {
            const response = await ProfileApiService.getActiveProfile();
            const activeProfile = response.data.active_profile;
            
            console.log('Active profile:', activeProfile.name);
            this.updateProfileDisplay(activeProfile);
            
        } catch (error) {
            console.error('Error loading active profile:', error);
            this.updateProfileDisplay({}); // Use defaults
        }
    }

    /**
     * Update profile display elements
     * @param {Object} profile - Profile data
     * @param {string} [profile.name] - Profile name
     * @param {string} [profile.image] - Profile image filename
     * @private
     * @memberof ActiveProfileManager
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
 * @class ProfileSelectionManager
 */
class ProfileSelectionManager {
    /**
     * Create a ProfileSelectionManager instance
     * @memberof ProfileSelectionManager
     */
    constructor() {
        /**
         * Profile list items
         * @type {NodeList}
         */
        this.profileItems = document.querySelectorAll('.list-group-item[data-profile-id]');
        
        this.setupEventListeners();
    }

    /**
     * Set up event listeners for profile selection
     * @private
     * @memberof ProfileSelectionManager
     */
    setupEventListeners() {
        this.profileItems.forEach(item => {
            item.addEventListener('click', (e) => this.handleProfileSelection(e, item));
        });
    }

    /**
     * Handle profile selection click
     * @async
     * @param {Event} e - Click event
     * @param {HTMLElement} item - Profile list item element
     * @private
     * @memberof ProfileSelectionManager
     */
    async handleProfileSelection(e, item) {
        e.preventDefault();

        try {
            const profileData = this.extractProfileData(item);
            const response = await ProfileApiService.setActiveProfile(profileData);
            
            if (response.success) {
                this.redirectToNextPage();
            } else {
                throw new Error('Failed to set active profile');
            }
            
        } catch (error) {
            console.error('Error setting active profile:', error);
            alert('Failed to select profile: ' + error.message);
        }
    }

    /**
     * Extract profile data from list item
     * @param {HTMLElement} item - Profile list item element
     * @returns {Object} Profile data
     * @private
     * @memberof ProfileSelectionManager
     */
    extractProfileData(item) {
        const profileId = item.getAttribute('data-profile-id');
        const profileAdmin = item.getAttribute('data-profile-admin');
        
        console.log('Setting admin status:', profileAdmin);
        
        return {
            profile_id: profileId,
            profile_admin: profileAdmin
        };
    }

    /**
     * Redirect to next page or home
     * @private
     * @memberof ProfileSelectionManager
     */
    redirectToNextPage() {
        const params = new URLSearchParams(window.location.search);
        const nextUrl = params.get('next') || '/';
        window.location.href = nextUrl;
    }
}

/**
 * Handles profile operations like edit and delete
 * @class ProfileOperationsHandler
 */
class ProfileOperationsHandler {
    /**
     * Edit a profile by redirecting to edit page
     * @param {string} profileId - Profile ID to edit
     * @param {Event} [event] - Click event to prevent bubbling
     * @memberof ProfileOperationsHandler
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
     * @async
     * @param {string} profileId - Profile ID to delete
     * @memberof ProfileOperationsHandler
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
            } else {
                throw new Error(response.message || 'Unknown error');
            }
            
        } catch (error) {
            console.error('Error deleting profile:', error);
            alert('An error occurred while deleting the profile: ' + error.message);
        }
    }

    /**
     * Validate profile ID
     * @param {string} profileId - Profile ID to validate
     * @returns {boolean} True if valid
     * @private
     * @memberof ProfileOperationsHandler
     */
    validateProfileId(profileId) {
        return profileId && profileId !== 'undefined' && profileId !== 'null' && profileId.trim() !== '';
    }

    /**
     * Show confirmation dialog for profile deletion
     * @returns {boolean} True if user confirmed
     * @private
     * @memberof ProfileOperationsHandler
     */
    confirmDeletion() {
        return confirm('Are you sure you want to delete this profile? This action cannot be undone.');
    }
}

/**
 * Main controller for profile management functionality
 * @class ProfileMgmtController
 */
class ProfileMgmtController {
    /**
     * Create a ProfileMgmtController instance
     * @memberof ProfileMgmtController
     */
    constructor() {
        /**
         * Profile creation handler
         * @type {ProfileCreationHandler}
         */
        this.creationHandler = new ProfileCreationHandler();
        
        /**
         * Active profile manager
         * @type {ActiveProfileManager}
         */
        this.activeProfileManager = new ActiveProfileManager();
        
        /**
         * Profile selection manager
         * @type {ProfileSelectionManager}
         */
        this.selectionManager = new ProfileSelectionManager();
        
        /**
         * Profile operations handler
         * @type {ProfileOperationsHandler}
         */
        this.operationsHandler = new ProfileOperationsHandler();
        
        this.exposeGlobalFunctions();
    }

    /**
     * Expose functions globally for template usage
     * @private
     * @memberof ProfileMgmtController
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
     * @returns {ProfileOperationsHandler} Operations handler
     * @memberof ProfileMgmtController
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
document.addEventListener('DOMContentLoaded', function() {
    profileMgmtController = new ProfileMgmtController();
});