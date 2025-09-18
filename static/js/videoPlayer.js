/**
 * @file videoPlayer.js
 * @description Handles everything related to the video.js player
 *
 * Initializes the video.js player
 * Sets up the resolution switcher with a default resolution
 * Ensures the control bar is visible
 * Tracks video playback progress
 * Marks a video as watched when 96% of it has been viewed
 * Handles the form submission for marking a video as watched
 */


/**
 * Core video player initialization and configuration.
 * 
 * Handles the main video.js player setup, TV mode detection,
 * and responsive settings configuration.
 * 
 * @class VideoPlayerCore
 * @example
 * const playerCore = new VideoPlayerCore('my-player');
 * const player = playerCore.initialize();
 */
class VideoPlayerCore {
    /**
     * Creates an instance of VideoPlayerCore.
     * 
     * @param {string} [playerId='player'] - The ID of the video element
     * @memberof VideoPlayerCore
     */    
    constructor(playerId = 'player') {
        /** @type {string} The HTML element ID for the video player */
        this.playerId = playerId;
        /** @type {Object|null} The video.js player instance */
        this.player = null;
        /** @type {HTMLElement|null} The container element */
        this.container = null;
        /** @type {boolean} Whether the device is detected as a TV */
        this.isTV = window.tvDetection?.isTV() || false;
    }

    /**
     * Initializes the video.js player with configuration options.
     * 
     * @returns {Object} The initialized video.js player instance
     * @memberof VideoPlayerCore
     */    
    initialize() {
        this.player = videojs(this.playerId, {
            controlBar: {
                skipButtons: { forward: 10, backward: 5 },
                qualitySelector: true,
                currentTimeDisplay: true,
                remainingTimeDisplay: { displayNegative: false }
            },
            aspectRatio: '16:9',
            fluid: true,
            enableSmoothSeeking: true
        });

        this.container = document.getElementById(this.playerId).parentElement;
        this.applyTVSettings();
        this.setupTVModeListener();
        
        return this.player;
    }

    /**
     * Applies TV-specific settings to the player interface.
     * 
     * @private
     * @memberof VideoPlayerCore
     */    
    applyTVSettings() {
        if (!this.isTV || !this.player) return;

        this.player.ready(() => {
            const controlBar = this.player.controlBar.el();
            controlBar.style.height = '60px';
            controlBar.style.fontSize = '1.2em';
            
            this.player.off('userinactive');
            this.player.on('userinactive', () => {
                setTimeout(() => {
                    if (!this.player.paused()) {
                        this.player.userActive(false);
                    }
                }, 8000);
            });
        });
    }

    /**
     * Sets up event listener for TV mode changes.
     * 
     * @private
     * @memberof VideoPlayerCore
     */    
    setupTVModeListener() {
        window.addEventListener('tvModeChanged', (e) => {
            this.isTV = e.detail.isTV;
            this.applyTVSettings();
        });
    }
}


/**
 * Right-click context menu functionality for the video player.
 * 
 * Provides a context menu when right-clicking on the video progress bar,
 * allowing users to copy timestamped URLs for sharing specific moments.
 * 
 * @class VideoContextMenu
 * @example
 * new VideoContextMenu(player); // Adds right-click menu to progress bar
 */
class VideoContextMenu {
    /**
     * Creates an instance of VideoContextMenu.
     * 
     * @param {Object} player - The video.js player instance
     * @memberof VideoContextMenu
     */
    constructor(player) {
        /** @type {Object} The video.js player instance */
        this.player = player;
        /** @type {HTMLElement|null} The context menu DOM element */
        this.contextMenu = null;
        this.init();
    }

    /**
     * Initializes the context menu by creating DOM elements and setting up events.
     * 
     * @private
     * @memberof VideoContextMenu
     */
    init() {
        this.createContextMenu();
        this.setupEventListeners();
    }

    /**
     * Creates the context menu DOM structure and appends it to the document body.
     * 
     * @private
     * @memberof VideoContextMenu
     */
    createContextMenu() {
        this.contextMenu = document.createElement('div');
        this.contextMenu.className = 'video-context-menu';
        
        const menuItem = document.createElement('div');
        menuItem.textContent = 'Copy link at current time';
        menuItem.className = 'video-context-menu-item';

        this.contextMenu.appendChild(menuItem);
        document.body.appendChild(this.contextMenu);
    }

    /**
     * Sets up event listeners for right-click, menu interactions, and hiding the menu.
     * 
     * @private
     * @memberof VideoContextMenu
     */
    setupEventListeners() {
        const progressControl = this.player.controlBar.progressControl.el();
        const menuItem = this.contextMenu.querySelector('.video-context-menu-item');

        // Right-click handler
        progressControl.addEventListener('contextmenu', (e) => this.showMenu(e));
        
        // Prevent right-click issues
        ['mousedown', 'mouseup'].forEach(event => {
            progressControl.addEventListener(event, (e) => {
                if (e.button === 2) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }
            });
        });

        // Menu item click
        menuItem.addEventListener('click', (e) => this.handleMenuClick(e));
        
        // Hide menu when clicking elsewhere
        document.addEventListener('click', (e) => this.hideMenu(e), true);
    }

    /**
     * Shows the context menu at the cursor position.
     * 
     * @param {MouseEvent} e - The right-click mouse event
     * @returns {boolean} Always returns false to prevent default context menu
     * @private
     * @memberof VideoContextMenu
     */
    showMenu(e) {
        e.preventDefault();
        
        this.player.el().style.pointerEvents = 'none';
        
        this.contextMenu.style.left = e.pageX + 'px';
        this.contextMenu.style.top = e.pageY + 'px';
        this.contextMenu.style.display = 'block';
        
        this.adjustMenuPosition(e);
        return false;
    }

    /**
     * Adjusts the menu position to ensure it stays within the viewport.
     * 
     * @param {MouseEvent} e - The original mouse event for position reference
     * @private
     * @memberof VideoContextMenu
     */
    adjustMenuPosition(e) {
        const rect = this.contextMenu.getBoundingClientRect();
        if (rect.right > window.innerWidth) {
            this.contextMenu.style.left = (e.pageX - rect.width) + 'px';
        }
        if (rect.bottom > window.innerHeight) {
            this.contextMenu.style.top = (e.pageY - rect.height) + 'px';
        }
    }

    /**
     * Handles menu item click by copying timestamped URL to clipboard.
     * 
     * @param {MouseEvent} e - The click event on the menu item
     * @private
     * @memberof VideoContextMenu
     */
    handleMenuClick(e) {
        e.preventDefault();
        e.stopPropagation();
       
        const timestampedUrl = this.getTimestampedUrl();
        
        navigator.clipboard.writeText(timestampedUrl)
            .then(() => this.showNotification('Link copied to clipboard!'))
            .catch(err => {
                console.error('Could not copy text: ', err);
                this.showNotification('Could not copy text!');
            });
        
        this.hideMenuAndReEnablePlayer();
    }

    /**
     * Hides the context menu when clicking outside of it.
     * 
     * @param {MouseEvent} e - The click event
     * @private
     * @memberof VideoContextMenu
     */
    hideMenu(e) {
        if (this.contextMenu.style.display === 'block') {
            if (!this.contextMenu.contains(e.target)) {
                this.hideMenuAndReEnablePlayer();
                e.preventDefault();
                e.stopPropagation();
            }
        }
    }

    /**
     * Hides the context menu and re-enables player pointer events.
     * 
     * @private
     * @memberof VideoContextMenu
     */
    hideMenuAndReEnablePlayer() {
        this.contextMenu.style.display = 'none';
        this.player.el().style.pointerEvents = '';
    }

    /**
     * Generates a timestamped URL with the current video playback time.
     * 
     * @returns {string} The URL with 't' parameter set to current time in seconds
     * @private
     * @memberof VideoContextMenu
     */
    getTimestampedUrl() {
        const currentTime = Math.floor(this.player.currentTime());
        const url = new URL(window.location.href);
        url.searchParams.set('t', currentTime);
        return url.toString();
    }

    /**
     * Shows a temporary notification message to the user.
     * 
     * @param {string} message - The message to display in the notification
     * @private
     * @memberof VideoContextMenu
     */
    showNotification(message) {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.className = 'video-notification';
        
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.add('show'), 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}


/**
 * Video progress tracking and watched status management.
 * 
 * Tracks video playback progress, saves position for resume functionality,
 * and automatically marks videos as watched when 96% complete.
 * 
 * @class ProgressTracker
 * @example
 * new ProgressTracker(player, 123, 456, 120); // Start at 2:00
 */
class ProgressTracker {
    /**
     * Creates an instance of ProgressTracker.
     * 
     * @param {Object} player - The video.js player instance
     * @param {number} videoId - The video ID for tracking
     * @param {number} profileId - The user profile ID
     * @param {number} [initialTime=0] - Initial playback position in seconds
     * @memberof ProgressTracker
     */
    constructor(player, videoId, profileId, initialTime = 0) {
        this.player = player;
        this.videoId = videoId;
        this.profileId = profileId;
        this.initialTime = initialTime;
        /** @type {number} Timestamp of last progress update */
        this.lastUpdateTime = 0;
        /** @type {boolean} Whether video has been marked as watched */
        this.hasMarkedWatched = false;
        
        this.init();
    }

    /**
     * Initializes the progress tracker and validates required parameters.
     * 
     * @private
     * @memberof ProgressTracker
     */
    init() {
        if (!this.profileId || !this.videoId) {
            console.error('Missing profileId or videoId. Progress tracking will not work.');
            return;
        }

        this.setupEventListeners();
    }

    /**
     * Sets up event listeners for video player events.
     * 
     * @private
     * @memberof ProgressTracker
     */
    setupEventListeners() {
        this.player.on('loadedmetadata', () => this.setInitialPosition());
        this.player.on('play', () => this.removeProgressOverlay());
        this.player.on('timeupdate', () => this.trackProgress());
        this.player.on('ended', () => this.handleVideoEnd());
    }

    /**
     * Sets the initial playback position when video metadata is loaded.
     * 
     * @private
     * @memberof ProgressTracker
     */
    setInitialPosition() {
        if (this.initialTime > 0) {
            console.log('Setting playback position to:', this.initialTime);
            this.player.currentTime(this.initialTime);
        }
    }

    /**
     * Removes the progress overlay element from the DOM when playback starts.
     * 
     * @private
     * @memberof ProgressTracker
     */
    removeProgressOverlay() {
        const progressOverlay = document.querySelector('.progress-overlay');
        if (progressOverlay) {
            progressOverlay.remove();
            console.log('Custom progress bar removed.');
        }
    }

    /**
     * Tracks video playback progress and automatically marks as watched.
     * Updates progress every 2 seconds and marks as watched at 96% completion.
     * 
     * @private
     * @memberof ProgressTracker
     */
    trackProgress() {
        const currentTime = Math.floor(this.player.currentTime());
        const duration = Math.floor(this.player.duration());
        const now = Date.now();

        if (this.hasMarkedWatched) return;

        // Update progress every 2 seconds
        if (now - this.lastUpdateTime >= 2000 && currentTime > 5) {
            this.lastUpdateTime = now;
            this.updateProgress(currentTime);
        }

        // Mark as watched at 96%
        if (currentTime >= duration * 0.96 && !this.hasMarkedWatched) {
            this.markAsWatched();
        }
    }

    /**
     * Sends progress update to the server API.
     * 
     * @private
     * @param {number} currentTime - The current playback time in seconds
     * @memberof ProgressTracker
     */
    updateProgress(currentTime) {
        fetch('/api/profile/in_progress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                video_id: this.videoId,
                current_time: currentTime
            })
        }).catch(err => console.error('Error updating progress:', err));
    }

    /**
     * Marks the video as watched and removes it from in-progress list.
     * Sends API requests to update watched status and clean up progress tracking.
     * 
     * @private
     * @memberof ProgressTracker
     */
    markAsWatched() {
        this.hasMarkedWatched = true;

        // Remove from in-progress
        fetch('/api/profile/in_progress', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ video_id: this.videoId })
        }).catch(err => console.error('Error removing from progress:', err));

        // Mark as watched
        fetch('/api/profile/mark_watched', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ video_id: this.videoId })
        }).catch(err => console.error('Error marking video as watched:', err));
    }

    /**
     * Handles video playback completion.
     * Removes theatre mode class from container if active.
     * 
     * @private
     * @memberof ProgressTracker
     */
    handleVideoEnd() {
        console.log('Video playback completed.');
        const container = this.player.el().parentElement;
        if (container.classList.contains('theatre-mode')) {
            container.classList.remove('theatre-mode');
        }
    }
}


/**
 * Handles URL 't' parameter for jumping to specific times.
 * 
 * Automatically detects timestamp parameters in the URL and
 * seeks the video to that position when initialized.
 * 
 * @class UrlTimeHandler
 * @example
 * // URL: /video/123?t=120
 * new UrlTimeHandler(player); // Will jump to 2:00
 */
class UrlTimeHandler {
    /**
     * Creates an instance of UrlTimeHandler.
     * 
     * @param {Object} player - The video.js player instance
     * @memberof UrlTimeHandler
     */
    constructor(player) {
        /** @type {Object} The video.js player instance */
        this.player = player;
        this.init();
    }

    /**
     * Initializes the URL time handler by checking for 't' parameter.
     * 
     * @private
     * @memberof UrlTimeHandler
     */
    init() {
        const urlParams = new URLSearchParams(window.location.search);
        const jumpTo = urlParams.get('t');
        
        if (jumpTo) {
            this.jumpToTime(parseInt(jumpTo, 10));
        }
    }

    /**
     * Jumps the video to a specific time and prepares for playback.
     * 
     * @param {number} time - The time in seconds to jump to
     * @memberof UrlTimeHandler
     */
    jumpToTime(time) {
        this.player.ready(() => {
            this.player.currentTime(time);
            this.player.pause();
            this.player.bigPlayButton.hide();
            
            this.player.on('seeked', () => {
                this.player.bigPlayButton.show();
                this.player.posterImage.hide();
                this.player.controlBar.show();
            });
        });
    }
}


/**
 * Custom player controls and buttons.
 * 
 * Adds custom functionality to the video player including theatre mode button
 * and keyboard controls for TV devices. Enhances the default video.js controls
 * with additional user interface elements.
 * 
 * @class CustomControls
 * @example
 * new CustomControls(player, container); // Adds theatre button and keyboard controls
 */
class CustomControls {
    /**
     * Creates an instance of CustomControls.
     * 
     * @param {Object} player - The video.js player instance
     * @param {HTMLElement} container - The container element for the player
     * @memberof CustomControls
     */
    constructor(player, container) {
        /** @type {Object} The video.js player instance */
        this.player = player;
        /** @type {HTMLElement} The container element for the player */
        this.container = container;
        /** @type {boolean} Whether the device is detected as a TV */
        this.isTV = window.tvDetection?.isTV() || false;
        this.init();
    }

    /**
     * Initializes custom controls by adding buttons and setting up keyboard controls.
     * 
     * @private
     * @memberof CustomControls
     */
    init() {
        this.addTheatreButton();
        this.setupKeyboardControls();
    }

    /**
     * Adds a theatre mode button to the video player control bar.
     * Creates a custom video.js button component that toggles theatre mode
     * by adding/removing the 'theatre-mode' class from the container.
     * 
     * @private
     * @memberof CustomControls
     */
    addTheatreButton() {
        const Button = videojs.getComponent('Button');
        const container = this.container; // Capture the container reference
        
        class TheatreButton extends Button {
            constructor(player, options) {
                super(player, options);
                this.controlText("Theatre Mode");
                this.addClass('vjs-theatre-button');
            }
            
            handleClick() {
                container.classList.toggle('theatre-mode'); // Use the captured container
            }
        }
    
        videojs.registerComponent('TheatreButton', TheatreButton);
        
        const controlBar = this.player.getChild('controlBar');
        const fullscreenIndex = controlBar.children()
            .findIndex(child => child.name && child.name() === 'FullscreenToggle');
        const insertIndex = fullscreenIndex > 0 ? fullscreenIndex : controlBar.children().length - 1;
        
        controlBar.addChild('TheatreButton', {}, insertIndex);
    }
    
    /**
     * Sets up keyboard controls for TV devices.
     * Adds arrow key navigation for seeking and volume control,
     * plus Enter key for play/pause functionality.
     * 
     * @private
     * @memberof CustomControls
     */
    setupKeyboardControls() {
        document.addEventListener('keydown', (e) => {
            if (!document.activeElement?.closest('.video-js') || !this.isTV) return;

            const actions = {
                'ArrowLeft': () => this.player.currentTime(Math.max(0, this.player.currentTime() - 10)),
                'ArrowRight': () => this.player.currentTime(this.player.currentTime() + 10),
                'ArrowUp': () => this.player.volume(Math.min(1, this.player.volume() + 0.1)),
                'ArrowDown': () => this.player.volume(Math.max(0, this.player.volume() - 0.1)),
                'Enter': () => this.player.paused() ? this.player.play() : this.player.pause()
            };

            if (actions[e.key]) {
                e.preventDefault();
                actions[e.key]();
            }
        });
    }
}


/**
 * Main video player initialization event handler.
 * 
 * Coordinates the initialization of all video player modules when the DOM is ready.
 * Creates the core player instance, retrieves video metadata from DOM attributes,
 * and initializes all supporting modules (context menu, custom controls, URL handling, 
 * and progress tracking) once the player is ready.
 * 
 * @function
 * @name DOMContentLoaded
 * @listens DOMContentLoaded
 * @example
 * // This runs automatically when the page loads
 * // Requires HTML element: <video id="player" data-video-id="123" data-profile-id="456" data-current-time="120">
 */
document.addEventListener('DOMContentLoaded', function () {
    // Initialize core player
    const playerCore = new VideoPlayerCore('player');
    const player = playerCore.initialize();
    
    // Get video data from DOM attributes
    const videoElement = document.getElementById('player');
    const profileId = videoElement.getAttribute('data-profile-id');
    const videoId = videoElement.getAttribute('data-video-id');
    const currentTime = parseInt(videoElement.getAttribute('data-current-time'), 10) || 0;

    // Initialize all modules when player is ready
    player.ready(() => {
        new VideoContextMenu(player);
        new CustomControls(player, playerCore.container);
        new UrlTimeHandler(player);
        new ProgressTracker(player, videoId, profileId, currentTime);
        
        // Ensure control bar is visible
        player.controlBar.show();
    });
});


/**
 * Form submission handler for marking videos as watched/unwatched.
 * 
 * Prevents default form submission and sends AJAX request to toggle
 * the watched status of a video. Updates the button text and API URL
 * based on the response to reflect the current state.
 * 
 * @function
 * @name markWatchedFormSubmit
 * @listens submit
 * @example
 * // Requires HTML form: <form id="markWatchedForm" data-api-url="/api/profile/mark_watched" data-video-id="123">
 */
document.getElementById('markWatchedForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission

    // Get the API URL and video ID from data attributes
    const apiUrl = this.dataset.apiUrl;
    const videoId = this.dataset.videoId;

    // Send a POST request to the server to mark the video as watched
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ video_id: videoId })
    })
    .then(response => response.json()) // Parse the JSON response
    .then(data => {
        // If the server responds with success, update the button
        if (data.success && this.dataset.apiUrl === '/api/profile/mark_watched') {
            this.querySelector('button').textContent = 'Watched!';
            this.dataset.apiUrl = '/api/profile/mark_unwatched';
        }
        else if (data.success && this.dataset.apiUrl === '/api/profile/mark_unwatched') {
            this.querySelector('button').textContent = 'Unwatched!';
            this.dataset.apiUrl = '/api/profile/mark_watched';
        }
    })
    .catch(err => console.error('Error updating watched status:', err));
});
