/**
 * @fileoverview Profile management functionality for user profiles.
 * Handles creating new profiles, editing existing profiles, getting profile lists,
 * setting active profiles, and managing profile operations.
 */
/**
 * Configuration constants for profile management
 */
declare const ProfileMgmtConfig: {
    /** API endpoint for creating profiles */
    readonly CREATE_PROFILE_ENDPOINT: "/api/profile/create";
    /** API endpoint for getting active profile */
    readonly GET_ACTIVE_ENDPOINT: "/api/profile/get_active";
    /** API endpoint for setting active profile */
    readonly SET_ACTIVE_ENDPOINT: "/api/profile/set_active";
    /** API endpoint pattern for deleting profiles */
    readonly DELETE_PROFILE_ENDPOINT: "/api/profile/delete/{id}";
    /** API endpoint pattern for editing profiles */
    readonly EDIT_PROFILE_ENDPOINT: "/edit_profile/{id}";
    /** Content type for JSON requests */
    readonly JSON_CONTENT_TYPE: "application/json";
    /** Profile pictures directory path */
    readonly PROFILE_PICS_PATH: "/static/img/profiles/";
    /** Default profile image */
    readonly DEFAULT_PROFILE_IMAGE: "guest.png";
    /** Default profile name */
    readonly DEFAULT_PROFILE_NAME: "Guest";
};
/**
 * Interface for profile creation data
 */
interface ProfileCreateData {
    name: string;
    image: string;
}
/**
 * Interface for active profile data
 */
interface ProfileData {
    id: string;
    name: string;
    image: string;
    is_admin: boolean;
}
/**
 * Interface for API response containing active profile
 */
interface ActiveProfileResponse {
    success: boolean;
    data: {
        active_profile: ProfileData;
    };
}
/**
 * Interface for API response for profile operations
 */
interface ApiResponse {
    success: boolean;
    message?: string;
    data?: unknown;
}
/**
 * Interface for setting active profile data
 */
interface SetActiveProfileData {
    profile_id: string;
    profile_admin: string;
}
/**
 * Handles API calls for profile operations
 */
declare class ProfileApiService {
    /**
     * Create a new profile
     * @param profileData - Profile data
     * @returns API response data
     */
    static createProfile(profileData: ProfileCreateData): Promise<ApiResponse>;
    /**
     * Get the currently active profile
     * @returns Active profile data
     */
    static getActiveProfile(): Promise<ActiveProfileResponse>;
    /**
     * Set a profile as active
     * @param profileData - Profile data
     * @returns API response data
     */
    static setActiveProfile(profileData: SetActiveProfileData): Promise<ApiResponse>;
    /**
     * Delete a profile
     * @param profileId - Profile ID to delete
     * @returns API response data
     */
    static deleteProfile(profileId: string): Promise<ApiResponse>;
}
/**
 * Handles profile creation form functionality
 */
declare class ProfileCreationHandler {
    private form;
    /**
     * Create a ProfileCreationHandler instance
     * @param formId - ID of the profile creation form
     */
    constructor(formId?: string);
    /**
     * Set up form event listeners
     */
    private setupEventListeners;
    /**
     * Handle form submission
     * @param e - Form submit event
     */
    private handleSubmit;
    /**
     * Extract form data
     * @returns Form data object
     */
    private extractFormData;
    /**
     * Redirect to profile selection page
     */
    private redirectToProfileSelection;
}
/**
 * Manages active profile display in the UI
 */
declare class ActiveProfileManager {
    private profileNameElement;
    private profileImageElement;
    /**
     * Create an ActiveProfileManager instance
     */
    constructor();
    /**
     * Load and display active profile information
     */
    private loadActiveProfile;
    /**
     * Update profile display elements
     * @param profile - Profile data
     */
    private updateProfileDisplay;
}
/**
 * Manages profile selection functionality
 */
declare class ProfileSelectionManager {
    private profileItems;
    /**
     * Create a ProfileSelectionManager instance
     */
    constructor();
    /**
     * Set up event listeners for profile selection
     */
    private setupEventListeners;
    /**
     * Handle profile selection click
     * @param e - Click event
     * @param item - Profile list item element
     */
    private handleProfileSelection;
    /**
     * Extract profile data from list item
     * @param item - Profile list item element
     * @returns Profile data
     */
    private extractProfileData;
    /**
     * Redirect to next page or home
     */
    private redirectToNextPage;
}
/**
 * Handles profile operations like edit and delete
 */
declare class ProfileOperationsHandler {
    /**
     * Edit a profile by redirecting to edit page
     * @param profileId - Profile ID to edit
     * @param event - Click event to prevent bubbling
     */
    editProfile(profileId: string, event?: Event): void;
    /**
     * Delete a profile with confirmation
     * @param profileId - Profile ID to delete
     */
    deleteProfile(profileId: string): Promise<void>;
    /**
     * Validate profile ID
     * @param profileId - Profile ID to validate
     * @returns True if valid
     */
    private validateProfileId;
    /**
     * Show confirmation dialog for profile deletion
     * @returns True if user confirmed
     */
    private confirmDeletion;
}
/**
 * Main controller for profile management functionality
 */
declare class ProfileMgmtController {
    private readonly creationHandler;
    private readonly activeProfileManager;
    private readonly selectionManager;
    private readonly operationsHandler;
    /**
     * Create a ProfileMgmtController instance
     */
    constructor();
    /**
     * Expose functions globally for template usage
     */
    private exposeGlobalFunctions;
    /**
     * Get the operations handler instance
     * @returns Operations handler
     */
    getOperationsHandler(): ProfileOperationsHandler;
}
declare let profileMgmtController: ProfileMgmtController;
//# sourceMappingURL=profileMgmt.d.ts.map