/**
 * @fileoverview Profile editing functionality for user profiles.
 * Handles renaming profiles, changing profile pictures, displaying watch history,
 * and managing watch history items.
 */
/**
 * Configuration constants for profile editing
 */
declare const ProfileEditConfig: {
    /** API endpoint for profile pictures */
    readonly PROFILE_PICTURES_ENDPOINT: "/api/profile/pictures";
    /** API endpoint pattern for profile deletion */
    readonly DELETE_PROFILE_ENDPOINT: "/api/profile/delete/{id}";
    /** API endpoint pattern for profile updates */
    readonly UPDATE_PROFILE_ENDPOINT: "/api/profile/update/{id}";
    /** API endpoint pattern for clearing history */
    readonly CLEAR_HISTORY_ENDPOINT: "/api/profile/clear_history/{id}";
    /** API endpoint for marking videos as watched */
    readonly MARK_WATCHED_ENDPOINT: "/api/profile/mark_watched";
    /** Content type for JSON requests */
    readonly JSON_CONTENT_TYPE: "application/json";
    /** Profile pictures directory path */
    readonly PROFILE_PICS_PATH: "/static/img/profiles/";
};
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
        new (element: HTMLElement): BootstrapModal;
    };
};
/**
 * Handles profile picture carousel functionality in the modal
 */
declare class ProfilePictureManager {
    private loading;
    private carousel;
    private carouselInner;
    private prevBtn;
    private nextBtn;
    private confirmBtn;
    /**
     * Create a ProfilePictureManager instance
     */
    constructor();
    /**
     * Load available profile pictures into the modal carousel
     */
    loadProfilePictures(): Promise<void>;
    /**
     * Show loading spinner and hide carousel
     */
    private showLoading;
    /**
     * Show carousel and hide loading spinner
     */
    private showCarousel;
    /**
     * Show error message in loading area
     * @param message - Error message to display
     */
    private showError;
    /**
     * Populate carousel with profile picture options
     * @param profilePics - Array of profile picture filenames
     * @param currentImage - Currently selected image filename
     */
    private populateCarousel;
    /**
     * Create a carousel item element
     * @param pic - Profile picture filename
     * @param isActive - Whether this item should be active
     * @returns Carousel item element
     */
    private createCarouselItem;
    /**
     * Confirm the selected profile picture
     */
    confirmSelection(): void;
}
/**
 * Manages profile data extraction and validation
 */
declare class ProfileDataManager {
    /**
     * Get profile data from DOM data attributes
     * @returns Profile data object
     */
    static getProfileData(): ProfileEditData;
    /**
     * Validate profile name input
     * @param name - Profile name to validate
     * @returns True if valid
     */
    static validateProfileName(name: string): boolean;
}
/**
 * Handles API calls for profile operations
 */
declare class ProfileEditApiService {
    /**
     * Delete a profile
     * @param profileId - ID of profile to delete
     */
    static deleteProfile(profileId: number): Promise<void>;
    /**
     * Update a profile
     * @param profileId - ID of profile to update
     * @param profileData - Profile data to update
     */
    static updateProfile(profileId: number, profileData: ProfileUpdateData): Promise<void>;
    /**
     * Clear entire watch history for a profile
     * @param profileId - ID of profile
     */
    static clearHistory(profileId: number): Promise<void>;
    /**
     * Clear a single item from watch history
     * @param profileId - ID of profile
     * @param videoId - ID of video to remove from history
     */
    static clearHistoryItem(profileId: number, videoId: number): Promise<void>;
    /**
     * Mark a video as watched
     * @param videoId - ID of video to mark as watched
     */
    static markWatched(videoId: number): Promise<void>;
}
/**
 * Main controller for profile editing functionality
 */
declare class ProfileEditController {
    private pictureManager;
    /**
     * Create a ProfileEditController instance
     */
    constructor();
    /**
     * Initialize the profile edit controller
     */
    private init;
    /**
     * Set up all event listeners
     */
    private setupEventListeners;
    /**
     * Set up main button event listeners
     */
    private setupButtonListeners;
    /**
     * Set up modal event listeners
     */
    private setupModalListeners;
    /**
     * Set up watch history event listeners
     */
    private setupHistoryListeners;
    /**
     * Handle profile deletion with confirmation
     */
    private handleDeleteProfile;
    /**
     * Handle profile save operation
     */
    private handleSaveProfile;
    /**
     * Handle avatar edit button click
     */
    private handleEditAvatar;
    /**
     * Handle clearing entire watch history
     */
    private handleClearHistory;
    /**
     * Handle clearing individual history item
     * @param button - Button that was clicked
     */
    private handleClearHistoryItem;
    /**
     * Handle marking video as watched
     * @param button - Button that was clicked
     */
    private handleMarkWatched;
}
declare let profileEditController: ProfileEditController;
//# sourceMappingURL=profileEdit.d.ts.map