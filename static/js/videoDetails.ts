/**
 * @fileoverview Video details page functionality.
 * Handles marking videos as watched/unwatched via API.
 */

/**
 * Configuration constants
 */
const VideoDetailsConfig = {
    /** API base URL */
    API_BASE_URL: 'http://localhost:5010',
    /** API endpoint for marking videos as watched */
    MARK_WATCHED_ENDPOINT: '/api/profile/mark_watched',
    /** API endpoint for marking videos as unwatched */
    MARK_UNWATCHED_ENDPOINT: '/api/profile/mark_unwatched',
    /** Content type for JSON requests */
    JSON_CONTENT_TYPE: 'application/json'
} as const;

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
class VideoDetailsController {
    private form: HTMLFormElement | null;
    private button: HTMLButtonElement | null;

    /**
     * Create a VideoDetailsController instance
     */
    constructor() {
        this.form = document.getElementById('markWatchedForm') as HTMLFormElement | null;
        this.button = this.form?.querySelector('button[type="submit"]') as HTMLButtonElement | null;
        
        this.init();
    }

    /**
     * Initialize the controller
     */
    private init(): void {
        if (this.form) {
            this.setupEventListeners();
        }
    }

    /**
     * Set up event listeners
     */
    private setupEventListeners(): void {
        this.form?.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    /**
     * Handle form submission
     * @param e - Submit event
     */
    private async handleSubmit(e: Event): Promise<void> {
        e.preventDefault();

        if (!this.form) return;

        const videoId = parseInt(this.form.dataset.videoId || '0');
        const isCurrentlyWatched = this.form.dataset.isWatched === 'true';
        console.log(`Video ID: ${videoId}, Currently Watched: ${isCurrentlyWatched}`);

        try {
            if (this.button) {
                this.button.disabled = true;
            }

            if (isCurrentlyWatched) {
                await this.markUnwatched(videoId);
            } else {
                await this.markWatched(videoId);
            }

            // Reload page to update UI
            window.location.reload();

        } catch (error) {
            console.error('Error updating watched status:', error);
            alert('Failed to update watched status: ' + (error as Error).message);
            
            if (this.button) {
                this.button.disabled = false;
            }
        }
    }

    /**
     * Mark video as watched
     * @param videoId - ID of video to mark as watched
     */
    private async markWatched(videoId: number): Promise<void> {
        const requestBody: MarkWatchedRequest = { video_id: videoId };

        const response = await fetch(
            `${VideoDetailsConfig.API_BASE_URL}${VideoDetailsConfig.MARK_WATCHED_ENDPOINT}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': VideoDetailsConfig.JSON_CONTENT_TYPE
                },
                credentials: 'include',
                body: JSON.stringify(requestBody)
            }
        );

        if (!response.ok) {
            const data: ApiResponse = await response.json();
            throw new Error(data.message || 'Failed to mark video as watched');
        }
    }

    /**
     * Mark video as unwatched
     * @param videoId - ID of video to mark as unwatched
     */
    private async markUnwatched(videoId: number): Promise<void> {
        const requestBody: MarkWatchedRequest = { video_id: videoId };

        const response = await fetch(
            `${VideoDetailsConfig.API_BASE_URL}${VideoDetailsConfig.MARK_UNWATCHED_ENDPOINT}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': VideoDetailsConfig.JSON_CONTENT_TYPE
                },
                credentials: 'include',
                body: JSON.stringify(requestBody)
            }
        );

        if (!response.ok) {
            const data: ApiResponse = await response.json();
            throw new Error(data.message || 'Failed to mark video as unwatched');
        }
    }
}

// Global controller instance
let videoDetailsController: VideoDetailsController;

/**
 * Initialize video details functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    videoDetailsController = new VideoDetailsController();
});