/**
 * @fileoverview Video details page functionality.
 * Handles marking videos as watched/unwatched via API.
 */
/**
 * Configuration constants
 */
declare const VideoDetailsConfig: {
    /** API base URL */
    readonly API_BASE_URL: "http://localhost:5010";
    /** API endpoint for marking videos as watched */
    readonly MARK_WATCHED_ENDPOINT: "/api/profile/mark_watched";
    /** API endpoint for marking videos as unwatched */
    readonly MARK_UNWATCHED_ENDPOINT: "/api/profile/mark_unwatched";
    /** Content type for JSON requests */
    readonly JSON_CONTENT_TYPE: "application/json";
};
/**
 * Interface for mark watched/unwatched request
 */
interface MarkWatchedRequest {
    video_id: number;
}
/**
 * Interface for API response
 */
interface ApiResponse {
    success: boolean;
    message?: string;
}
/**
 * Handles video details page functionality
 */
declare class VideoDetailsController {
    private form;
    private button;
    /**
     * Create a VideoDetailsController instance
     */
    constructor();
    /**
     * Initialize the controller
     */
    private init;
    /**
     * Set up event listeners
     */
    private setupEventListeners;
    /**
     * Handle form submission
     * @param e - Submit event
     */
    private handleSubmit;
    /**
     * Mark video as watched
     * @param videoId - ID of video to mark as watched
     */
    private markWatched;
    /**
     * Mark video as unwatched
     * @param videoId - ID of video to mark as unwatched
     */
    private markUnwatched;
}
declare let videoDetailsController: VideoDetailsController;
//# sourceMappingURL=videoDetails.d.ts.map