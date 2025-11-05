"use strict";
/**
 * @fileoverview Video addition management for admin interface.
 * Handles fetching videos from CSV data and adding them to the database.
 * Provides table display functionality and individual video addition controls.
 */
/**
 * Configuration constants for video addition
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
 */
class VideoApiService {
    /**
     * Fetch videos from CSV endpoint
     * @returns Array of video objects
     * @throws Error if API call fails
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
     * @param videoData - Video data to add
     * @returns API response data
     * @throws Error if API call fails
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
 */
class VideoTableManager {
    /**
     * Create a VideoTableManager instance
     * @param containerId - ID of the container element for the table
     * @param wrapperId - ID of the wrapper element to show/hide
     */
    constructor(containerId = 'videosTableContainer', wrapperId = 'videosTableWrapper') {
        this.container = document.getElementById(containerId);
        this.wrapper = document.getElementById(wrapperId);
    }
    /**
     * Generate and display video table
     * @param videos - Array of video objects
     */
    displayVideos(videos) {
        if (!this.container)
            return;
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
     */
    showNoVideosMessage() {
        if (this.container) {
            this.container.innerHTML = '<p class="text-warning">No videos found.</p>';
        }
    }
    /**
     * Show error message
     * @param message - Error message to display
     */
    showError(message = 'Error loading videos.') {
        if (this.container) {
            this.container.innerHTML = `<p class="text-danger">${message}</p>`;
        }
    }
    /**
     * Show the table wrapper
     */
    showTable() {
        if (this.wrapper) {
            this.wrapper.classList.remove('d-none');
        }
    }
    /**
     * Generate complete table HTML
     * @param videos - Array of video objects
     * @returns Complete table HTML
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
     * @returns Table header HTML
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
     * @param videos - Array of video objects
     * @returns Table body HTML
     */
    generateTableBody(videos) {
        return videos.map(video => this.generateVideoRow(video)).join('');
    }
    /**
     * Generate a single video row HTML
     * @param video - Video object
     * @returns Video row HTML
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
     * @param value - Value to check
     * @returns Status cell HTML
     */
    generateStatusCell(value) {
        if (value) {
            return `<span style="color: green;" title="${this.sanitizeAttribute(value)}">✔</span>`;
        }
        return '<span style="color: red;">✘</span>';
    }
    /**
     * Sanitize text for HTML display
     * @param text - Text to sanitize
     * @returns Sanitized text
     */
    sanitizeText(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    /**
     * Sanitize text for HTML attributes
     * @param text - Text to sanitize
     * @returns Sanitized text
     */
    sanitizeAttribute(text) {
        return text.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }
}
/**
 * @class VideoAdditionHandler
 *
 * Handles individual video addition operations
 */
class VideoAdditionHandler {
    /**
     * @method constructor
     *
     * Create a VideoAdditionHandler instance
     */
    constructor() {
        this.setupEventListeners();
    }
    /**
     * @method setupEventListeners
     *
     * Set up event listeners for video addition buttons
     */
    setupEventListeners() {
        // Use event delegation to handle dynamically created buttons
        document.addEventListener('click', (event) => {
            const target = event.target;
            if (target.classList.contains('video-add-btn')) {
                this.handleAddVideo(target);
            }
        });
    }
    /**
     * @method handleAddVideo
     *
     * Handle video addition button click
     *
     * @param button - The clicked button
     */
    async handleAddVideo(button) {
        try {
            const videoData = this.extractVideoData(button);
            // Add date_added in correct format
            videoData.date_added = this.getCurrentDateTimeFormatted();
            // Disable button immediately to prevent double-clicks
            this.disableButton(button);
            const response = await VideoApiService.addVideoToDatabase(videoData);
            this.showSuccessMessage(response.message || 'Video added to the database successfully!');
            this.markButtonAsCompleted(button);
        }
        catch (error) {
            console.error('Error adding video to the database:', error);
            this.showErrorMessage('An error occurred while adding the video.');
            this.enableButton(button); // Re-enable button on error
        }
    }
    /**
     * @method getCurrentDateTimeFormatted
     *
     * Get current date and time in the format: YYYY-MM-DD HH:MM:SS
     *
     * @returns Formatted date string
     */
    getCurrentDateTimeFormatted() {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }
    /**
     * Extract video data from button's data attribute
     * @param button - Button element
     * @returns Video data object
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
     * @param button - Button to disable
     */
    disableButton(button) {
        button.disabled = true;
        button.textContent = '...';
    }
    /**
     * Enable the add button
     * @param button - Button to enable
     */
    enableButton(button) {
        button.disabled = false;
        button.textContent = '+';
    }
    /**
     * Mark button as completed
     * @param button - Button to mark as completed
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
     * @param message - Success message
     */
    showSuccessMessage(message) {
        alert(message); // Could be replaced with a better notification system
    }
    /**
     * Show error message to user
     * @param message - Error message
     */
    showErrorMessage(message) {
        alert(message); // Could be replaced with a better notification system
    }
}
/**
 * Main controller for video addition functionality
 */
class VideoAddController {
    /**
     * Create a VideoAddController instance
     * @param listButtonId - ID of the list videos button
     */
    constructor(listButtonId = 'listVideosBtn') {
        this.tableManager = new VideoTableManager();
        // Initialize the addition handler to set up event listeners
        new VideoAdditionHandler();
        this.listButton = document.getElementById(listButtonId);
        this.init();
    }
    /**
     * Initialize the video add controller
     */
    init() {
        if (this.listButton) {
            this.setupListButton();
        }
        else {
            console.warn('List videos button not found');
        }
    }
    /**
     * Set up the list videos button event listener
     */
    setupListButton() {
        if (!this.listButton)
            return;
        this.listButton.addEventListener('click', () => {
            this.handleListVideos();
        });
    }
    /**
     * Handle list videos button click
     */
    async handleListVideos() {
        try {
            this.setLoadingState(true);
            const videos = await VideoApiService.fetchVideosFromCSV();
            console.log('Videos data:', videos);
            this.tableManager.displayVideos(videos);
        }
        catch (error) {
            console.error('Error fetching videos:', error);
            this.tableManager.showError('Error loading videos.');
        }
        finally {
            this.setLoadingState(false);
        }
    }
    /**
     * Set loading state for list button
     * @param isLoading - Whether to show loading state
     */
    setLoadingState(isLoading) {
        if (!this.listButton)
            return;
        if (isLoading) {
            this.listButton.disabled = true;
            this.listButton.textContent = 'Loading...';
        }
        else {
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
document.addEventListener('DOMContentLoaded', function () {
    videoAddController = new VideoAddController();
});
// Expose global function for backward compatibility (if needed)
/**
 * @deprecated Use VideoAddController instead
 */
window.addToDatabase = function (_video, _button) {
    console.warn('addToDatabase function is deprecated. Use VideoAddController instead.');
    // Could implement backward compatibility here if needed
};
//# sourceMappingURL=videoAdd.js.map