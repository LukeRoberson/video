/**
 * @fileoverview Video addition management for admin interface.
 * Handles fetching videos from CSV data and adding them to the database.
 * Provides table display functionality and individual video addition controls.
 */

/**
 * Configuration constants for video addition
 * @readonly
 * @enum {string}
 */
const VideoAddConfig = {
    /** API endpoint for fetching CSV video data */
    CSV_ENDPOINT: '/api/videos/csv',
    /** API endpoint for adding videos to database */
    ADD_ENDPOINT: '/api/videos/add',
    /** Content type for JSON requests */
    JSON_CONTENT_TYPE: 'application/json',
    /** CSS classes for button states */
    BUTTON_CLASSES: {
        SUCCESS: 'btn-success',
        SECONDARY: 'btn-secondary',
        DISABLED: 'btn-secondary'
    }
};

/**
 * Handles API calls for video operations
 * @class VideoApiService
 */
class VideoApiService {
    /**
     * Fetch videos from CSV endpoint
     * @static
     * @async
     * @returns {Promise<Array>} Array of video objects
     * @throws {Error} If API call fails
     * @memberof VideoApiService
     */
    static async fetchVideosFromCSV() {
        const response = await fetch(VideoAddConfig.CSV_ENDPOINT);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Convert object to array if necessary
        return Array.isArray(data) ? data : Object.values(data);
    }

    /**
     * Add a video to the database
     * @static
     * @async
     * @param {Object} videoData - Video data to add
     * @returns {Promise<Object>} API response data
     * @throws {Error} If API call fails
     * @memberof VideoApiService
     */
    static async addVideoToDatabase(videoData) {
        const response = await fetch(VideoAddConfig.ADD_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': VideoAddConfig.JSON_CONTENT_TYPE
            },
            body: JSON.stringify(videoData)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }
}

/**
 * Handles video table generation and display
 * @class VideoTableManager
 */
class VideoTableManager {
    /**
     * Create a VideoTableManager instance
     * @param {string} containerId - ID of the container element for the table
     * @param {string} wrapperId - ID of the wrapper element to show/hide
     * @memberof VideoTableManager
     */
    constructor(containerId = 'videosTableContainer', wrapperId = 'videosTableWrapper') {
        /**
         * Container element for the video table
         * @type {HTMLElement}
         */
        this.container = document.getElementById(containerId);
        
        /**
         * Wrapper element for the video table
         * @type {HTMLElement}
         */
        this.wrapper = document.getElementById(wrapperId);
    }

    /**
     * Generate and display video table
     * @param {Array<Object>} videos - Array of video objects
     * @memberof VideoTableManager
     */
    displayVideos(videos) {
        if (!videos || videos.length === 0) {
            this.showNoVideosMessage();
            return;
        }

        const tableHTML = this.generateTableHTML(videos);
        this.container.innerHTML = tableHTML;
        this.showTable();
    }

    /**
     * Show no videos found message
     * @private
     * @memberof VideoTableManager
     */
    showNoVideosMessage() {
        this.container.innerHTML = '<p class="text-warning">No videos found.</p>';
    }

    /**
     * Show error message
     * @param {string} message - Error message to display
     * @memberof VideoTableManager
     */
    showError(message = 'Error loading videos.') {
        this.container.innerHTML = `<p class="text-danger">${message}</p>`;
    }

    /**
     * Show the table wrapper
     * @private
     * @memberof VideoTableManager
     */
    showTable() {
        if (this.wrapper) {
            this.wrapper.classList.remove('d-none');
        }
    }

    /**
     * Generate complete table HTML
     * @param {Array<Object>} videos - Array of video objects
     * @returns {string} Complete table HTML
     * @private
     * @memberof VideoTableManager
     */
    generateTableHTML(videos) {
        const tableHeader = this.generateTableHeader();
        const tableBody = this.generateTableBody(videos);
        
        return `
            <table class="table table-dark table-striped">
                ${tableHeader}
                <tbody>
                    ${tableBody}
                </tbody>
            </table>
        `;
    }

    /**
     * Generate table header HTML
     * @returns {string} Table header HTML
     * @private
     * @memberof VideoTableManager
     */
    generateTableHeader() {
        return `
            <thead>
                <tr>
                    <th>Video Name</th>
                    <th>URL</th>
                    <th>Main Cat</th>
                    <th>Sub Cat</th>
                    <th>1080</th>
                    <th>720</th>
                    <th>480</th>
                    <th>360</th>
                    <th>240</th>
                    <th>Thumb</th>
                    <th>Time</th>
                    <th>Action</th>
                </tr>
            </thead>
        `;
    }

    /**
     * Generate table body HTML
     * @param {Array<Object>} videos - Array of video objects
     * @returns {string} Table body HTML
     * @private
     * @memberof VideoTableManager
     */
    generateTableBody(videos) {
        return videos.map(video => this.generateVideoRow(video)).join('');
    }

    /**
     * Generate a single video row HTML
     * @param {Object} video - Video object
     * @returns {string} Video row HTML
     * @private
     * @memberof VideoTableManager
     */
    generateVideoRow(video) {
        const videoJson = JSON.stringify(video).replace(/"/g, '&quot;');
        
        return `
            <tr>
                <td>${this.sanitizeText(video.video_name || 'N/A')}</td>
                <td>${this.generateStatusCell(video.video_url)}</td>
                <td>${this.sanitizeText(video.main_cat_name || 'N/A')}</td>
                <td>${this.sanitizeText(video.sub_cat_name || 'N/A')}</td>
                <td>${this.generateStatusCell(video.url_1080)}</td>
                <td>${this.generateStatusCell(video.url_720)}</td>
                <td>${this.generateStatusCell(video.url_480)}</td>
                <td>${this.generateStatusCell(video.url_360)}</td>
                <td>${this.generateStatusCell(video.url_240)}</td>
                <td>${this.generateStatusCell(video.thumbnail)}</td>
                <td>${this.sanitizeText(video.duration || 'N/A')}</td>
                <td>
                    <button 
                        class="btn btn-success btn-sm video-add-btn" 
                        title="Add to Database" 
                        data-video='${videoJson}'>
                        +
                    </button>
                </td>
            </tr>
        `;
    }

    /**
     * Generate status cell with checkmark or X
     * @param {string} value - Value to check
     * @returns {string} Status cell HTML
     * @private
     * @memberof VideoTableManager
     */
    generateStatusCell(value) {
        if (value) {
            return `<span style="color: green;" title="${this.sanitizeAttribute(value)}">✔</span>`;
        }
        return '<span style="color: red;">✘</span>';
    }

    /**
     * Sanitize text for HTML display
     * @param {string} text - Text to sanitize
     * @returns {string} Sanitized text
     * @private
     * @memberof VideoTableManager
     */
    sanitizeText(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Sanitize text for HTML attributes
     * @param {string} text - Text to sanitize
     * @returns {string} Sanitized text
     * @private
     * @memberof VideoTableManager
     */
    sanitizeAttribute(text) {
        return text.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }
}

/**
 * Handles individual video addition operations
 * @class VideoAdditionHandler
 */
class VideoAdditionHandler {
    /**
     * Create a VideoAdditionHandler instance
     * @memberof VideoAdditionHandler
     */
    constructor() {
        this.setupEventListeners();
    }

    /**
     * Set up event listeners for video addition buttons
     * @private
     * @memberof VideoAdditionHandler
     */
    setupEventListeners() {
        // Use event delegation to handle dynamically created buttons
        document.addEventListener('click', (event) => {
            if (event.target.classList.contains('video-add-btn')) {
                this.handleAddVideo(event.target);
            }
        });
    }

    /**
     * Handle video addition button click
     * @async
     * @param {HTMLButtonElement} button - The clicked button
     * @private
     * @memberof VideoAdditionHandler
     */
    async handleAddVideo(button) {
        try {
            const videoData = this.extractVideoData(button);
            
            // Disable button immediately to prevent double-clicks
            this.disableButton(button);
            
            const response = await VideoApiService.addVideoToDatabase(videoData);
            
            this.showSuccessMessage(response.message || 'Video added to the database successfully!');
            this.markButtonAsCompleted(button);
            
        } catch (error) {
            console.error('Error adding video to the database:', error);
            this.showErrorMessage('An error occurred while adding the video.');
            this.enableButton(button); // Re-enable button on error
        }
    }

    /**
     * Extract video data from button's data attribute
     * @param {HTMLButtonElement} button - Button element
     * @returns {Object} Video data object
     * @private
     * @memberof VideoAdditionHandler
     */
    extractVideoData(button) {
        const videoJson = button.getAttribute('data-video');
        if (!videoJson) {
            throw new Error('No video data found in button');
        }
        
        return JSON.parse(videoJson);
    }

    /**
     * Disable the add button
     * @param {HTMLButtonElement} button - Button to disable
     * @private
     * @memberof VideoAdditionHandler
     */
    disableButton(button) {
        button.disabled = true;
        button.textContent = '...';
    }

    /**
     * Enable the add button
     * @param {HTMLButtonElement} button - Button to enable
     * @private
     * @memberof VideoAdditionHandler
     */
    enableButton(button) {
        button.disabled = false;
        button.textContent = '+';
    }

    /**
     * Mark button as completed
     * @param {HTMLButtonElement} button - Button to mark as completed
     * @private
     * @memberof VideoAdditionHandler
     */
    markButtonAsCompleted(button) {
        button.disabled = true;
        button.classList.remove(VideoAddConfig.BUTTON_CLASSES.SUCCESS);
        button.classList.add(VideoAddConfig.BUTTON_CLASSES.DISABLED);
        button.textContent = '✓';
        button.title = 'Already added to database';
    }

    /**
     * Show success message to user
     * @param {string} message - Success message
     * @private
     * @memberof VideoAdditionHandler
     */
    showSuccessMessage(message) {
        alert(message); // Could be replaced with a better notification system
    }

    /**
     * Show error message to user
     * @param {string} message - Error message
     * @private
     * @memberof VideoAdditionHandler
     */
    showErrorMessage(message) {
        alert(message); // Could be replaced with a better notification system
    }
}

/**
 * Main controller for video addition functionality
 * @class VideoAddController
 */
class VideoAddController {
    /**
     * Create a VideoAddController instance
     * @param {string} listButtonId - ID of the list videos button
     * @memberof VideoAddController
     */
    constructor(listButtonId = 'listVideosBtn') {
        /**
         * Video table manager instance
         * @type {VideoTableManager}
         */
        this.tableManager = new VideoTableManager();
        
        /**
         * Video addition handler instance
         * @type {VideoAdditionHandler}
         */
        this.additionHandler = new VideoAdditionHandler();
        
        /**
         * List videos button element
         * @type {HTMLButtonElement}
         */
        this.listButton = document.getElementById(listButtonId);
        
        this.init();
    }

    /**
     * Initialize the video add controller
     * @memberof VideoAddController
     */
    init() {
        if (this.listButton) {
            this.setupListButton();
        } else {
            console.warn('List videos button not found');
        }
    }

    /**
     * Set up the list videos button event listener
     * @private
     * @memberof VideoAddController
     */
    setupListButton() {
        this.listButton.addEventListener('click', () => {
            this.handleListVideos();
        });
    }

    /**
     * Handle list videos button click
     * @async
     * @private
     * @memberof VideoAddController
     */
    async handleListVideos() {
        try {
            this.setLoadingState(true);
            
            const videos = await VideoApiService.fetchVideosFromCSV();
            console.log('Videos data:', videos);
            
            this.tableManager.displayVideos(videos);
            
        } catch (error) {
            console.error('Error fetching videos:', error);
            this.tableManager.showError('Error loading videos.');
        } finally {
            this.setLoadingState(false);
        }
    }

    /**
     * Set loading state for list button
     * @param {boolean} isLoading - Whether to show loading state
     * @private
     * @memberof VideoAddController
     */
    setLoadingState(isLoading) {
        if (isLoading) {
            this.listButton.disabled = true;
            this.listButton.textContent = 'Loading...';
        } else {
            this.listButton.disabled = false;
            this.listButton.textContent = 'List Videos';
        }
    }
}

// Global controller instance
let videoAddController;

/**
 * Initialize video addition functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    videoAddController = new VideoAddController();
});

// Expose global function for backward compatibility (if needed)
/**
 * @deprecated Use VideoAddController instead
 * @global
 */
window.addToDatabase = function(video, button) {
    console.warn('addToDatabase function is deprecated. Use VideoAddController instead.');
    // Could implement backward compatibility here if needed
};