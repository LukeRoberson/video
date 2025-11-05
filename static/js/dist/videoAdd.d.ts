/**
 * @fileoverview Video addition management for admin interface.
 * Handles fetching videos from CSV data and adding them to the database.
 * Provides table display functionality and individual video addition controls.
 */
/**
 * Configuration constants for video addition
 */
declare const VideoAddConfig: {
    /** API endpoint for fetching CSV video data */
    readonly CSV_ENDPOINT: "/api/videos/csv";
    /** API endpoint for adding videos to database */
    readonly ADD_ENDPOINT: "/api/videos/add";
    /** Content type for JSON requests */
    readonly JSON_CONTENT_TYPE: "application/json";
    /** CSS classes for button states */
    readonly BUTTON_CLASSES: {
        readonly SUCCESS: "btn-success";
        readonly SECONDARY: "btn-secondary";
        readonly DISABLED: "btn-secondary";
    };
};
/**
 * Interface for video data structure
 */
interface VideoData {
    video_name?: string;
    video_url?: string;
    main_cat_name?: string;
    sub_cat_name?: string;
    url_1080?: string;
    url_720?: string;
    url_480?: string;
    url_360?: string;
    url_240?: string;
    thumbnail?: string;
    duration?: string;
    date_added?: string;
}
/**
 * Interface for video add API response structure
 */
interface VideoAddApiResponse {
    success?: boolean;
    message?: string;
    error?: string;
}
/**
 * Handles API calls for video operations
 */
declare class VideoApiService {
    /**
     * Fetch videos from CSV endpoint
     * @returns Array of video objects
     * @throws Error if API call fails
     */
    static fetchVideosFromCSV(): Promise<VideoData[]>;
    /**
     * Add a video to the database
     * @param videoData - Video data to add
     * @returns API response data
     * @throws Error if API call fails
     */
    static addVideoToDatabase(videoData: VideoData): Promise<VideoAddApiResponse>;
}
/**
 * Handles video table generation and display
 */
declare class VideoTableManager {
    /** Container element for the video table */
    private container;
    /** Wrapper element for the video table */
    private wrapper;
    /**
     * Create a VideoTableManager instance
     * @param containerId - ID of the container element for the table
     * @param wrapperId - ID of the wrapper element to show/hide
     */
    constructor(containerId?: string, wrapperId?: string);
    /**
     * Generate and display video table
     * @param videos - Array of video objects
     */
    displayVideos(videos: VideoData[]): void;
    /**
     * Show no videos found message
     */
    private showNoVideosMessage;
    /**
     * Show error message
     * @param message - Error message to display
     */
    showError(message?: string): void;
    /**
     * Show the table wrapper
     */
    private showTable;
    /**
     * Generate complete table HTML
     * @param videos - Array of video objects
     * @returns Complete table HTML
     */
    private generateTableHTML;
    /**
     * Generate table header HTML
     * @returns Table header HTML
     */
    private generateTableHeader;
    /**
     * Generate table body HTML
     * @param videos - Array of video objects
     * @returns Table body HTML
     */
    private generateTableBody;
    /**
     * Generate a single video row HTML
     * @param video - Video object
     * @returns Video row HTML
     */
    private generateVideoRow;
    /**
     * Generate status cell with checkmark or X
     * @param value - Value to check
     * @returns Status cell HTML
     */
    private generateStatusCell;
    /**
     * Sanitize text for HTML display
     * @param text - Text to sanitize
     * @returns Sanitized text
     */
    private sanitizeText;
    /**
     * Sanitize text for HTML attributes
     * @param text - Text to sanitize
     * @returns Sanitized text
     */
    private sanitizeAttribute;
}
/**
 * @class VideoAdditionHandler
 *
 * Handles individual video addition operations
 */
declare class VideoAdditionHandler {
    /**
     * @method constructor
     *
     * Create a VideoAdditionHandler instance
     */
    constructor();
    /**
     * @method setupEventListeners
     *
     * Set up event listeners for video addition buttons
     */
    private setupEventListeners;
    /**
     * @method handleAddVideo
     *
     * Handle video addition button click
     *
     * @param button - The clicked button
     */
    private handleAddVideo;
    /**
     * @method getCurrentDateTimeFormatted
     *
     * Get current date and time in the format: YYYY-MM-DD HH:MM:SS
     *
     * @returns Formatted date string
     */
    private getCurrentDateTimeFormatted;
    /**
     * Extract video data from button's data attribute
     * @param button - Button element
     * @returns Video data object
     */
    private extractVideoData;
    /**
     * Disable the add button
     * @param button - Button to disable
     */
    private disableButton;
    /**
     * Enable the add button
     * @param button - Button to enable
     */
    private enableButton;
    /**
     * Mark button as completed
     * @param button - Button to mark as completed
     */
    private markButtonAsCompleted;
    /**
     * Show success message to user
     * @param message - Success message
     */
    private showSuccessMessage;
    /**
     * Show error message to user
     * @param message - Error message
     */
    private showErrorMessage;
}
/**
 * Main controller for video addition functionality
 */
declare class VideoAddController {
    /** Video table manager instance */
    private tableManager;
    /** List videos button element */
    private listButton;
    /**
     * Create a VideoAddController instance
     * @param listButtonId - ID of the list videos button
     */
    constructor(listButtonId?: string);
    /**
     * Initialize the video add controller
     */
    private init;
    /**
     * Set up the list videos button event listener
     */
    private setupListButton;
    /**
     * Handle list videos button click
     */
    private handleListVideos;
    /**
     * Set loading state for list button
     * @param isLoading - Whether to show loading state
     */
    private setLoadingState;
}
declare let videoAddController: VideoAddController;
//# sourceMappingURL=videoAdd.d.ts.map