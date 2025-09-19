/**
 * @file videoPlayer.js
 * @description Complete video player implementation with modular class-based architecture
 *
 * This file provides a comprehensive video player solution built on video.js with
 * the following functionality:
 * - Core video player initialization and TV mode detection
 * - Right-click context menu for timestamped URL sharing
 * - Progress tracking and automatic watched status management
 * - URL timestamp parameter handling (t=seconds)
 * - Custom theatre mode button and keyboard controls
 * - Form-based watched/unwatched status toggling
 *
 * @requires videojs
 * 
 * @example
 * // HTML requirements:
 * // <video id="player" data-video-id="123" data-profile-id="456" data-current-time="120">
 * // <form id="markWatchedForm" data-api-url="/api/profile/mark_watched" data-video-id="123">
 * 
 * // Classes are automatically initialized on DOMContentLoaded
 * 
 * @see {@link VideoPlayerCore} - Core player initialization
 * @see {@link VideoContextMenu} - Right-click context menu
 * @see {@link ProgressTracker} - Progress and watched status tracking  
 * @see {@link UrlTimeHandler} - URL timestamp handling
 * @see {@link CustomControls} - Theatre mode and keyboard controls
 */


/**
 * Global video player management for preventing multiple simultaneous playback.
 * 
 * Manages all video player instances and ensures only one video plays at a time
 * by automatically pausing other players when a new one starts playing.
 * 
 * @class GlobalPlayerManager
 * @example
 * // Automatically initialized - no direct instantiation needed
 * // Registers players automatically when VideoPlayerCore instances are created
 */
class GlobalPlayerManager {
    /**
     * Creates the singleton instance of GlobalPlayerManager.
     * 
     * @memberof GlobalPlayerManager
     */
    constructor() {
        /** @type {Array<Object>} Array of all registered video.js player instances */
        this.players = [];
    }

    /**
     * Gets the singleton instance of GlobalPlayerManager.
     * 
     * @static
     * @returns {GlobalPlayerManager} The singleton instance
     * @memberof GlobalPlayerManager
     */
    static getInstance() {
        if (!GlobalPlayerManager.instance) {
            GlobalPlayerManager.instance = new GlobalPlayerManager();
        }
        return GlobalPlayerManager.instance;
    }

    /**
     * Registers a player instance and sets up play event monitoring.
     * 
     * @param {Object} player - The video.js player instance to register
     * @memberof GlobalPlayerManager
     */
    registerPlayer(player) {
        this.players.push(player);
        
        // Listen for play event and pause other players
        player.on('play', () => {
            this.pauseOtherPlayers(player);
        });
        
        // Clean up when player is disposed
        player.on('dispose', () => {
            this.unregisterPlayer(player);
        });
    }

    /**
     * Unregisters a player instance from management.
     * 
     * @param {Object} player - The video.js player instance to unregister
     * @memberof GlobalPlayerManager
     */
    unregisterPlayer(player) {
        const index = this.players.indexOf(player);
        if (index > -1) {
            this.players.splice(index, 1);
        }
    }

    /**
     * Pauses all players except the currently playing one.
     * 
     * @param {Object} currentPlayer - The player that should continue playing
     * @memberof GlobalPlayerManager
     */
    pauseOtherPlayers(currentPlayer) {
        this.players.forEach(player => {
            if (player && player !== currentPlayer && !player.paused()) {
                player.pause();
            }
        });
    }
}


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
        /** @type {boolean} Whether the device is a mobile device */
        this.isMobile = this.detectMobile();
        /** @type {GlobalPlayerManager} Reference to the global player manager */
        this.globalManager = GlobalPlayerManager.getInstance();
    }

    /**
     * Detects if the device is a mobile device.
     * 
     * @returns {boolean} True if mobile device detected
     * @private
     * @memberof VideoPlayerCore
     */
    detectMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               (navigator.maxTouchPoints && navigator.maxTouchPoints > 2 && /MacIntel/.test(navigator.platform));
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
            fluid: false,
            responsive: true,
            enableSmoothSeeking: true,
            // Enable fullscreen on mobile devices
            ...(this.isMobile && {
                fluid: true,
                fill: false
            })
        });

        this.container = document.getElementById(this.playerId).parentElement;
        this.applyTVSettings();
        this.setupTVModeListener();
        this.setupMobileFullscreen();        
        
        // Register with global manager for multi-player coordination
        this.globalManager.registerPlayer(this.player);
        
        return this.player;
    }

    /**
     * Sets up automatic fullscreen behavior for mobile devices.
     * 
     * @private
     * @memberof VideoPlayerCore
     */
    setupMobileFullscreen() {
        if (!this.isMobile) return;

        this.player.ready(() => {
            // Enter fullscreen when play is triggered on mobile
            this.player.on('play', () => {
                if (!this.player.isFullscreen()) {
                    // Small delay to ensure video is actually playing
                    setTimeout(() => {
                        if (!this.player.paused()) {
                            this.player.requestFullscreen();
                        }
                    }, 100);
                }
            });

            // Optional: Exit fullscreen when video is paused
            // Uncomment if you want this behavior
            /*
            this.player.on('pause', () => {
                if (this.player.isFullscreen()) {
                    this.player.exitFullscreen();
                }
            });
            */
        });
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

// ...existing code for other classes...


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
 * Handles URL 't' and 'end' parameters for video snippets, and theme-based snippets.
 * 
 * Automatically detects timestamp parameters in the URL or data attributes and
 * creates video snippets by jumping to start time and pausing at end time.
 * Supports both URL parameters (?t=60&end=120) and theme data attributes.
 * 
 * @class UrlTimeHandler
 * @example
 * // URL: /video/123?t=60&end=120 - 1 minute snippet from 1:00 to 2:00
 * // OR: <video data-snippet-start="60" data-snippet-end="120">
 * new UrlTimeHandler(player);
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
        /** @type {number|null} End time for snippet in seconds */
        this.endTime = null;
        /** @type {boolean} Whether we're currently in snippet mode */
        this.isSnippet = false;
        /** @type {HTMLElement|null} Snippet indicator element */
        this.snippetIndicator = null;
        /** @type {string} Source of snippet ('url' or 'theme') */
        this.snippetSource = null;
        this.init();
    }

    /**
     * Initializes the URL time handler by checking for 't' and 'end' parameters or data attributes.
     *  't' and 'end' are URL parameters
     *  'data-snippet-start' and 'data-snippet-end' are data attributes on the video element
     *  If both are present, URL parameters take priority.
     * 
     * @private
     * @memberof UrlTimeHandler
     */
    init() {
        console.log('UrlTimeHandler init() called');
        
        // Check URL parameters first (takes priority)
        const urlParams = new URLSearchParams(window.location.search);
        const urlStartTime = urlParams.get('t');
        const urlEndTime = urlParams.get('end');
        
        console.log('URL params - t:', urlStartTime, 'end:', urlEndTime);
        
        if (urlStartTime) {
            const start = parseInt(urlStartTime, 10);
            const end = urlEndTime ? parseInt(urlEndTime, 10) : null;
            this.snippetSource = 'url';
            
            console.log('Setting up URL snippet - start:', start, 'end:', end);
            
            if (end && end > start) {
                this.setupSnippet(start, end);
            } else {
                this.jumpToTime(start);
            }
            return;
        }
    
        // Check for theme-based snippet data attributes
        const videoElement = this.player.el();
        const themeStartTime = videoElement.getAttribute('data-snippet-start');
        const themeEndTime = videoElement.getAttribute('data-snippet-end');
        
        console.log('Theme data attributes - start:', themeStartTime, 'end:', themeEndTime);
        
        if (themeStartTime && themeEndTime) {
            const start = parseInt(themeStartTime, 10);
            const end = parseInt(themeEndTime, 10);
            this.snippetSource = 'theme';
            
            console.log('Setting up theme snippet - start:', start, 'end:', end);
            
            if (end > start) {
                this.setupSnippet(start, end);
            } else {
                this.jumpToTime(start);
            }
        } else if (themeStartTime) {
            // Just start time, no end time
            const start = parseInt(themeStartTime, 10);
            this.snippetSource = 'theme';
            console.log('Setting up theme start time only:', start);
            this.jumpToTime(start);
        }
        
        console.log('No snippet parameters found');
    }

    /**
     * Sets up a video snippet with start and end times.
     * 
     * @param {number} startTime - The start time in seconds
     * @param {number} endTime - The end time in seconds
     * @memberof UrlTimeHandler
     */
    setupSnippet(startTime, endTime) {
        this.endTime = endTime;
        this.isSnippet = true;
        
        this.player.ready(() => {
            this.jumpToTime(startTime);
            this.createSnippetIndicator(startTime, endTime);
            this.setupSnippetControls();
        });
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

    /**
     * Creates visual indicator for snippet mode.
     * 
     * @private
     * @param {number} startTime - Snippet start time
     * @param {number} endTime - Snippet end time
     * @memberof UrlTimeHandler
     */
    createSnippetIndicator(startTime, endTime) {
        console.log('Creating snippet indicator - start:', startTime, 'end:', endTime, 'source:', this.snippetSource);
        
        // Create snippet info overlay
        this.snippetIndicator = document.createElement('div');
        this.snippetIndicator.className = 'snippet-indicator';
    
        // Different close button behavior based on snippet source
        const closeButton = this.snippetSource === 'url' ? 
            '<button class="snippet-close" title="Exit snippet mode">×</button>' : 
            ''; // Theme-based snippets don't show close button
        
        this.snippetIndicator.innerHTML = `
            <div class="snippet-info">
                📎 Snippet: ${this.formatTime(startTime)} - ${this.formatTime(endTime)}
                ${closeButton}
            </div>
        `;
        
        console.log('Snippet indicator HTML:', this.snippetIndicator.innerHTML);
        
        // Add to player
        this.player.el().appendChild(this.snippetIndicator);
        
        console.log('Snippet indicator added to player');
        
        // Add close button event listener for URL-based snippets
        if (this.snippetSource === 'url') {
            const closeBtn = this.snippetIndicator.querySelector('.snippet-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => this.exitSnippetMode());
            }
        }
        
        // Add snippet range highlight
        this.highlightSnippetRange(startTime, endTime);
    }

    /**
     * Highlights the snippet range on the progress bar.
     * 
     * @private
     * @param {number} startTime - Snippet start time
     * @param {number} endTime - Snippet end time
     * @memberof UrlTimeHandler
     */
    highlightSnippetRange(startTime, endTime) {
        console.log('highlightSnippetRange called - start:', startTime, 'end:', endTime);
        
        const createHighlight = () => {
            const duration = this.player.duration();
            console.log('Player duration:', duration);
            
            if (duration > 0) {
                const startPercent = (startTime / duration) * 100;
                const endPercent = (endTime / duration) * 100;
                
                console.log('Percentages - start:', startPercent, 'end:', endPercent);
                
                const progressControl = this.player.controlBar.progressControl.el();
                console.log('Progress control element:', progressControl);
                
                const highlight = document.createElement('div');
                highlight.className = 'snippet-highlight';
                highlight.style.left = `${startPercent}%`;
                highlight.style.width = `${endPercent - startPercent}%`;
                
                console.log('Highlight element created:', highlight);
                console.log('Highlight styles:', highlight.style.cssText);
                
                progressControl.appendChild(highlight);
                console.log('Highlight appended to progress control');
            } else {
                console.log('Duration is still 0, retrying...');
            }
        };
        
        // If duration is available now, create highlight immediately
        if (this.player.duration() > 0) {
            createHighlight();
        } else {
            // Otherwise, wait for loadedmetadata event
            console.log('Waiting for video metadata to load...');
            this.player.one('loadedmetadata', createHighlight);
        }
    }
    
    /**
     * Sets up snippet-specific controls and behavior.
     * 
     * @private
     * @memberof UrlTimeHandler
     */
    setupSnippetControls() {
        // Monitor playback to pause at end time
        const checkEndTime = () => {
            if (this.isSnippet && this.endTime && this.player.currentTime() >= this.endTime) {
                this.player.pause();
                this.player.currentTime(this.endTime);
            }
        };
        
        this.player.on('timeupdate', checkEndTime);
        
        // Prevent seeking beyond snippet bounds
        this.player.on('seeking', () => {
            if (!this.isSnippet) return;
            
            const currentTime = this.player.currentTime();
            let startTime;

            if (this.snippetSource === 'url') {
                const urlParams = new URLSearchParams(window.location.search);
                startTime = parseInt(urlParams.get('t'), 10);
            } else if (this.snippetSource === 'theme') {
                const videoElement = this.player.el();
                startTime = parseInt(videoElement.getAttribute('data-snippet-start'), 10);
            }
            
            if (currentTime < startTime) {
                this.player.currentTime(startTime);
            } else if (currentTime > this.endTime) {
                this.player.currentTime(this.endTime);
            }
        });
    }

    /**
     * Exits snippet mode and returns to normal video playback.
     * Only works for URL-based snippets, not theme-based ones.
     * 
     * @memberof UrlTimeHandler
     */
    exitSnippetMode() {
        // Only allow exiting URL-based snippets
        if (this.snippetSource !== 'url') return;

        this.isSnippet = false;
        this.endTime = null;
        
        // Remove snippet indicator
        if (this.snippetIndicator) {
            this.snippetIndicator.remove();
            this.snippetIndicator = null;
        }
        
        // Remove snippet highlight
        const highlight = this.player.el().querySelector('.snippet-highlight');
        if (highlight) {
            highlight.remove();
        }
        
        // Update URL to remove end parameter
        const url = new URL(window.location);
        url.searchParams.delete('end');
        window.history.replaceState({}, '', url);
    }

    /**
     * Formats seconds into MM:SS or HH:MM:SS format.
     * 
     * @private
     * @param {number} seconds - Time in seconds
     * @returns {string} Formatted time string
     * @memberof UrlTimeHandler
     */
    formatTime(seconds) {
        const hrs = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hrs > 0) {
            return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        return `${mins}:${secs.toString().padStart(2, '0')}`;
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
    // Find all video elements with the video-js class
    const videoElements = document.querySelectorAll('video.video-js');
    
    videoElements.forEach(videoElement => {
        const playerId = videoElement.id;
        
        // Initialize core player for each video
        const playerCore = new VideoPlayerCore(playerId);
        const player = playerCore.initialize();
        
        // Get video data from DOM attributes
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
const markWatchedForm = document.getElementById('markWatchedForm');
if (markWatchedForm) {
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
}
