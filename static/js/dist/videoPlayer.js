"use strict";
/**
 * @file videoPlayer.ts
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
 */
/**
 * Configuration constants API endpoints and settings.
 */
const ApiConfig = {
    /** API base URL for new endpoints (separate server) */
    API_BASE_URL: 'http://localhost:5010',
    /** API base URL for legacy endpoints */
    LEGACY_API_BASE_URL: 'http://localhost:5000',
    /** API endpoint for marking videos as watched */
    MARK_WATCHED_ENDPOINT: '/api/profile/mark_watched',
    /** API endpoint for marking videos as unwatched */
    MARK_UNWATCHED_ENDPOINT: '/api/profile/mark_unwatched',
    /** API endpoint for in-progress videos */
    IN_PROGRESS_ENDPOINT: '/api/profile/in_progress',
};
/**
 * Global video player management for preventing multiple simultaneous playback.
 *
 * Manages all video player instances and ensures only one video plays at a time
 * by automatically pausing other players when a new one starts playing.
 */
class GlobalPlayerManager {
    /**
     * Creates the singleton instance of GlobalPlayerManager.
     */
    constructor() {
        /** Array of all registered video.js player instances */
        this.players = [];
    }
    /**
     * Gets the singleton instance of GlobalPlayerManager.
     * @returns The singleton instance
     */
    static getInstance() {
        if (!GlobalPlayerManager.instance) {
            GlobalPlayerManager.instance = new GlobalPlayerManager();
        }
        return GlobalPlayerManager.instance;
    }
    /**
     * Registers a player instance and sets up play event monitoring.
     * @param player - The video.js player instance to register
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
     * @param player - The video.js player instance to unregister
     */
    unregisterPlayer(player) {
        const index = this.players.indexOf(player);
        if (index > -1) {
            this.players.splice(index, 1);
        }
    }
    /**
     * Pauses all players except the currently playing one.
     * @param currentPlayer - The player that should continue playing
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
 */
class VideoPlayerCore {
    /**
     * Creates an instance of VideoPlayerCore.
     * @param playerId - The ID of the video element
     */
    constructor(playerId = 'player') {
        /** The video.js player instance */
        this.player = null;
        /** The container element */
        this.container = null;
        this.playerId = playerId;
        this.isTV = window.tvDetection?.isTV() || false;
        this.isMobile = this.detectMobile();
        this.globalManager = GlobalPlayerManager.getInstance();
    }
    /**
     * Detects if the device is a mobile device.
     * @returns True if mobile device detected
     */
    detectMobile() {
        const mobileTest = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        const touchTest = navigator.maxTouchPoints && navigator.maxTouchPoints > 2 && /MacIntel/.test(navigator.platform);
        return mobileTest || Boolean(touchTest);
    }
    /**
     * Initializes the video.js player with configuration options.
     * @returns The initialized video.js player instance
     */
    initialize() {
        this.player = videojs(this.playerId, {
            controlBar: {
                skipButtons: { forward: 10, backward: 5 },
                qualitySelector: true,
                currentTimeDisplay: true,
                remainingTimeDisplay: { displayNegative: false },
                // Disable PiP button on mobile
                pictureInPictureToggle: !this.isMobile
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
        this.container = document.getElementById(this.playerId)?.parentElement || null;
        this.applyTVSettings();
        this.setupTVModeListener();
        this.setupMobileFullscreen();
        this.setupTouchPlayPause();
        // Register with global manager for multi-player coordination
        if (this.player) {
            this.globalManager.registerPlayer(this.player);
        }
        return this.player;
    }
    /**
     * Sets up touch-based play/pause functionality for mobile devices.
     */
    setupTouchPlayPause() {
        if (!this.player)
            return;
        // Check if device has touch capability
        const hasTouchSupport = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        if (!hasTouchSupport)
            return;
        this.player.ready(() => {
            if (!this.player)
                return;
            const videoElement = this.player.tech({ IWillNotUseThisInPlugins: true }).el();
            const playerElement = this.player.el();
            let touchStartTime = 0;
            let touchMoved = false;
            // Handle touch start
            const handleTouchStart = (_e) => {
                touchStartTime = Date.now();
                touchMoved = false;
            };
            // Handle touch move (to detect if user is scrolling)
            const handleTouchMove = (_e) => {
                touchMoved = true;
            };
            // Handle touch end - toggle play/pause if it was a tap
            const handleTouchEnd = (e) => {
                if (!this.player)
                    return;
                const touchEndTime = Date.now();
                const touchDuration = touchEndTime - touchStartTime;
                const target = e.target;
                // Only trigger play/pause if conditions are met
                if (touchDuration < 300 && !touchMoved && !target.closest('.vjs-control-bar')) {
                    e.preventDefault();
                    e.stopPropagation();
                    if (this.player.paused()) {
                        this.player.play();
                    }
                    else {
                        this.player.pause();
                    }
                }
            };
            // Add event listeners to both video element and player container
            [videoElement, playerElement].forEach(element => {
                if (element) {
                    element.addEventListener('touchstart', handleTouchStart, { passive: true });
                    element.addEventListener('touchmove', handleTouchMove, { passive: true });
                    element.addEventListener('touchend', handleTouchEnd, { passive: false });
                }
            });
            // Clean up event listeners when player is disposed
            this.player.on('dispose', () => {
                [videoElement, playerElement].forEach(element => {
                    if (element) {
                        element.removeEventListener('touchstart', handleTouchStart);
                        element.removeEventListener('touchmove', handleTouchMove);
                        element.removeEventListener('touchend', handleTouchEnd);
                    }
                });
            });
        });
    }
    /**
     * Sets up automatic fullscreen behavior for mobile devices.
     */
    setupMobileFullscreen() {
        if (!this.isMobile || !this.player)
            return;
        this.player.ready(() => {
            if (!this.player)
                return;
            // Enter fullscreen when play is triggered on mobile
            this.player.on('play', () => {
                if (!this.player)
                    return;
                if (!this.player.isFullscreen()) {
                    // Small delay to ensure video is actually playing
                    setTimeout(() => {
                        if (this.player && !this.player.paused()) {
                            this.player.requestFullscreen();
                        }
                    }, 100);
                }
            });
        });
    }
    /**
     * Applies TV-specific settings to the player interface.
     */
    applyTVSettings() {
        if (!this.isTV || !this.player)
            return;
        this.player.ready(() => {
            if (!this.player)
                return;
            const controlBar = this.player.controlBar.el();
            controlBar.style.height = '60px';
            controlBar.style.fontSize = '1.2em';
            this.player.off('userinactive');
            this.player.on('userinactive', () => {
                if (!this.player)
                    return;
                setTimeout(() => {
                    if (this.player && !this.player.paused()) {
                        this.player.userActive(false);
                    }
                }, 8000);
            });
        });
    }
    /**
     * Sets up event listener for TV mode changes.
     */
    setupTVModeListener() {
        window.addEventListener('tvModeChanged', (e) => {
            const customEvent = e;
            this.isTV = customEvent.detail.isTV;
            this.applyTVSettings();
        });
    }
}
/**
 * Right-click context menu functionality for the video player.
 *
 * Provides a context menu when right-clicking on the video progress bar,
 * allowing users to copy timestamped URLs for sharing specific moments.
 */
class VideoContextMenu {
    /**
     * Creates an instance of VideoContextMenu.
     * @param player - The video.js player instance
     */
    constructor(player) {
        /** Flag to prevent theatre mode exit during menu operations */
        this.isMenuOperation = false;
        this.player = player;
        this.contextMenu = this.createContextMenu();
        this.init();
    }
    /**
     * Initializes the context menu by creating DOM elements and setting up events.
     */
    init() {
        this.setupEventListeners();
    }
    /**
     * Creates the context menu DOM structure and appends it to the document body.
     * @returns The created context menu element
     */
    createContextMenu() {
        const contextMenu = document.createElement('div');
        contextMenu.className = 'video-context-menu';
        const menuItem = document.createElement('div');
        menuItem.textContent = 'Copy link at current time';
        menuItem.className = 'video-context-menu-item';
        contextMenu.appendChild(menuItem);
        document.body.appendChild(contextMenu);
        return contextMenu;
    }
    /**
     * Sets up event listeners for right-click, menu interactions, and hiding the menu.
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
                }
            });
        });
        // Menu item click - stop propagation immediately
        menuItem.addEventListener('click', (e) => {
            this.isMenuOperation = true;
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            this.handleMenuClick();
            // Reset flag after a short delay to allow the click to fully process
            setTimeout(() => {
                this.isMenuOperation = false;
            }, 100);
        }, true);
        // Hide menu when clicking elsewhere
        document.addEventListener('click', (e) => this.hideMenu(e), true);
    }
    /**
     * Shows the context menu at the cursor position.
     * @param e - The right-click mouse event
     * @returns Always returns false to prevent default context menu
     */
    showMenu(e) {
        e.preventDefault();
        // Set flag immediately when menu is shown
        this.isMenuOperation = true;
        this.player.el().style.pointerEvents = 'none';
        this.contextMenu.style.left = e.pageX + 'px';
        this.contextMenu.style.top = e.pageY + 'px';
        this.contextMenu.style.display = 'block';
        this.adjustMenuPosition(e);
        return false;
    }
    /**
     * Adjusts the menu position to ensure it stays within the viewport.
     * @param e - The original mouse event for position reference
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
     */
    handleMenuClick() {
        const timestampedUrl = this.getTimestampedUrl();
        navigator.clipboard.writeText(timestampedUrl)
            .then(() => this.showNotification('Link copied to clipboard!'))
            .catch(err => {
            console.error('Could not copy text: ', err);
            this.showNotification('Could not copy text!');
        });
        this.hideMenuAndReEnablePlayer();
        // Keep flag active longer to prevent theatre mode exit
        setTimeout(() => {
            this.isMenuOperation = false;
        }, 200);
    }
    /**
     * Hides the context menu when clicking outside of it.
     * @param e - The click event
     */
    hideMenu(e) {
        if (this.contextMenu.style.display === 'block') {
            if (!this.contextMenu.contains(e.target)) {
                this.hideMenuAndReEnablePlayer();
                e.preventDefault();
                e.stopPropagation();
                // Keep flag active longer to prevent theatre mode exit
                setTimeout(() => {
                    this.isMenuOperation = false;
                }, 200);
            }
        }
    }
    /**
     * Hides the context menu and re-enables player pointer events.
     */
    hideMenuAndReEnablePlayer() {
        this.contextMenu.style.display = 'none';
        this.player.el().style.pointerEvents = '';
    }
    /**
     * Checks if a menu operation is currently in progress.
     * @returns True if menu operation is active
     */
    isMenuActive() {
        return this.isMenuOperation;
    }
    /**
     * Generates a timestamped URL with the current video playback time.
     * @returns The URL with 't' parameter set to current time in seconds
     */
    getTimestampedUrl() {
        const currentTime = Math.floor(this.player.currentTime());
        const url = new URL(window.location.href);
        url.searchParams.set('t', currentTime.toString());
        return url.toString();
    }
    /**
     * Shows a temporary notification message to the user.
     * @param message - The message to display in the notification
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
 */
class ProgressTracker {
    /**
     * Creates an instance of ProgressTracker.
     * @param player - The video.js player instance
     * @param videoId - The video ID for tracking
     * @param profileId - The user profile ID
     * @param initialTime - Initial playback position in seconds
     */
    constructor(player, videoId, profileId, initialTime = 0) {
        /** Timestamp of last progress update */
        this.lastUpdateTime = 0;
        /** Whether video has been marked as watched */
        this.hasMarkedWatched = false;
        this.player = player;
        this.videoId = videoId;
        this.profileId = profileId;
        this.initialTime = initialTime;
        this.init();
    }
    /**
     * Initializes the progress tracker and validates required parameters.
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
     */
    setupEventListeners() {
        this.player.on('loadedmetadata', () => this.setInitialPosition());
        this.player.on('play', () => this.removeProgressOverlay());
        this.player.on('timeupdate', () => this.trackProgress());
        this.player.on('ended', () => this.handleVideoEnd());
    }
    /**
     * Sets the initial playback position when video metadata is loaded.
     */
    setInitialPosition() {
        if (this.initialTime > 0) {
            this.player.currentTime(this.initialTime);
        }
    }
    /**
     * Removes the progress overlay element from the DOM when playback starts.
     */
    removeProgressOverlay() {
        // Get the progress overlay element
        const progressOverlay = document.querySelector('.progress-overlay');
        if (progressOverlay) {
            // Remove the overlay from the DOM
            progressOverlay.remove();
            // Ensure initial position is set
            // (if loadedmetadata fired before play)
            if (this.initialTime > 0 && this.player.currentTime() === 0) {
                this.setInitialPosition();
            }
        }
    }
    /**
     * Tracks video playback progress and automatically marks as watched.
     * Updates progress every 2 seconds and marks as watched at 96% completion.
     */
    trackProgress() {
        const currentTime = Math.floor(this.player.currentTime());
        const duration = Math.floor(this.player.duration());
        const now = Date.now();
        if (this.hasMarkedWatched)
            return;
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
     * @param currentTime - The current playback time in seconds
     */
    updateProgress(currentTime) {
        fetch(`${ProfileMgmtConfig.API_BASE_URL}${ApiConfig.IN_PROGRESS_ENDPOINT}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                video_id: this.videoId,
                current_time: currentTime
            })
        }).catch(err => console.error('Error updating progress:', err));
    }
    /**
     * Marks the video as watched and removes it from in-progress list.
     * Sends API requests to update watched status and clean up progress tracking.
     */
    markAsWatched() {
        this.hasMarkedWatched = true;
        // Remove from in-progress
        fetch(`${ProfileMgmtConfig.API_BASE_URL}${ApiConfig.IN_PROGRESS_ENDPOINT}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ video_id: this.videoId })
        }).catch(err => console.error('Error removing from progress:', err));
        // Mark as watched
        fetch(`${ApiConfig.API_BASE_URL}${ApiConfig.MARK_UNWATCHED_ENDPOINT}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ video_id: this.videoId })
        }).catch(err => console.error('Error marking video as watched:', err));
    }
    /**
     * Handles video playback completion.
     * Removes theatre mode class from container if active.
     */
    handleVideoEnd() {
        console.log('Video playback completed.');
        const container = this.player.el().parentElement;
        if (container && container.classList.contains('theatre-mode')) {
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
 */
class UrlTimeHandler {
    /**
     * Creates an instance of UrlTimeHandler.
     * @param player - The video.js player instance
     */
    constructor(player) {
        /** End time for snippet in seconds */
        this.endTime = null;
        /** Whether we're currently in snippet mode */
        this.isSnippet = false;
        /** Snippet indicator element */
        this.snippetIndicator = null;
        /** Source of snippet ('url' or 'theme') */
        this.snippetSource = null;
        this.player = player;
        this.init();
    }
    /**
     * Initializes the URL time handler by checking for 't' and 'end' parameters or data attributes.
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
            }
            else {
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
            }
            else {
                this.jumpToTime(start);
            }
        }
        else if (themeStartTime) {
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
     * @param startTime - The start time in seconds
     * @param endTime - The end time in seconds
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
     * @param time - The time in seconds to jump to
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
     * @param startTime - Snippet start time
     * @param endTime - Snippet end time
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
     * @param startTime - Snippet start time
     * @param endTime - Snippet end time
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
            }
            else {
                console.log('Duration is still 0, retrying...');
            }
        };
        // If duration is available now, create highlight immediately
        if (this.player.duration() > 0) {
            createHighlight();
        }
        else {
            // Otherwise, wait for loadedmetadata event
            console.log('Waiting for video metadata to load...');
            this.player.one('loadedmetadata', createHighlight);
        }
    }
    /**
     * Sets up snippet-specific controls and behavior.
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
            if (!this.isSnippet)
                return;
            const currentTime = this.player.currentTime();
            let startTime = null;
            if (this.snippetSource === 'url') {
                const urlParams = new URLSearchParams(window.location.search);
                const startParam = urlParams.get('t');
                startTime = startParam ? parseInt(startParam, 10) : null;
            }
            else if (this.snippetSource === 'theme') {
                const videoElement = this.player.el();
                const startAttr = videoElement.getAttribute('data-snippet-start');
                startTime = startAttr ? parseInt(startAttr, 10) : null;
            }
            if (startTime !== null && this.endTime !== null) {
                if (currentTime < startTime) {
                    this.player.currentTime(startTime);
                }
                else if (currentTime > this.endTime) {
                    this.player.currentTime(this.endTime);
                }
            }
        });
    }
    /**
     * Exits snippet mode and returns to normal video playback.
     * Only works for URL-based snippets, not theme-based ones.
     */
    exitSnippetMode() {
        // Only allow exiting URL-based snippets
        if (this.snippetSource !== 'url')
            return;
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
        const url = new URL(window.location.href);
        url.searchParams.delete('end');
        window.history.replaceState({}, '', url.toString());
    }
    /**
     * Formats seconds into MM:SS or HH:MM:SS format.
     * @param seconds - Time in seconds
     * @returns Formatted time string
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
 * and keyboard controls for TV devices.
 */
class CustomControls {
    /**
     * Creates an instance of CustomControls.
     * @param player - The video.js player instance
     * @param container - The container element for the player
     */
    constructor(player, container) {
        /** Bound click handler for theatre mode exit */
        this.theatreModeClickHandler = null;
        /** Reference to context menu for checking menu state */
        this.contextMenu = null;
        this.player = player;
        this.container = container;
        this.isTV = window.tvDetection?.isTV() || false;
        this.isMobile = this.detectMobile();
        this.init();
    }
    /**
     * Detects if the device is a mobile device.
     * @returns True if mobile device detected
     */
    detectMobile() {
        const mobileTest = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        const touchTest = navigator.maxTouchPoints && navigator.maxTouchPoints > 2 && /MacIntel/.test(navigator.platform);
        return mobileTest || Boolean(touchTest);
    }
    /**
     * Initializes custom controls by adding buttons and setting up keyboard controls.
     */
    init() {
        // Only add theatre button if not on mobile
        if (!this.isMobile) {
            this.addTheatreButton();
            this.setupTheatreModeClickHandler();
        }
        this.setupKeyboardControls();
        // Additional safety check to hide any buttons that might have been created
        if (this.isMobile) {
            this.player.ready(() => {
                this.hideMobileButtonsFallback();
            });
        }
    }
    /**
     * Sets a reference to the context menu for state checking.
     * @param contextMenu - The VideoContextMenu instance
     */
    setContextMenu(contextMenu) {
        this.contextMenu = contextMenu;
    }
    /**
     * Sets up click handler for exiting theatre mode when clicking outside the player.
     */
    setupTheatreModeClickHandler() {
        this.theatreModeClickHandler = (e) => {
            // Only handle clicks when in theatre mode
            if (!this.container.classList.contains('theatre-mode')) {
                return;
            }
            // Don't exit theatre mode if context menu is active
            if (this.contextMenu && this.contextMenu.isMenuActive()) {
                return;
            }
            // Check if the click target is the context menu itself
            const target = e.target;
            const contextMenuElement = document.querySelector('.video-context-menu');
            if (contextMenuElement && contextMenuElement.contains(target)) {
                return;
            }
            // Check if click is outside the video player container
            if (!this.container.contains(target)) {
                this.exitTheatreMode();
            }
        };
        // Add the event listener to the document
        document.addEventListener('click', this.theatreModeClickHandler, true);
        // Clean up event listener when player is disposed
        this.player.on('dispose', () => {
            if (this.theatreModeClickHandler) {
                document.removeEventListener('click', this.theatreModeClickHandler, true);
                this.theatreModeClickHandler = null;
            }
        });
    }
    /**
     * Exits theatre mode by removing the theatre-mode class from the container.
     */
    exitTheatreMode() {
        this.container.classList.remove('theatre-mode');
    }
    /**
     * Enters theatre mode by adding the theatre-mode class to the container.
     */
    enterTheatreMode() {
        this.container.classList.add('theatre-mode');
    }
    /**
     * Toggles theatre mode on/off.
     */
    toggleTheatreMode() {
        if (this.container.classList.contains('theatre-mode')) {
            this.exitTheatreMode();
        }
        else {
            this.enterTheatreMode();
        }
    }
    /**
     * Fallback method to hide buttons on mobile (safety net).
     */
    hideMobileButtonsFallback() {
        // Hide picture-in-picture button on mobile (fallback)
        const pipButton = this.player.controlBar.getChild('PictureInPictureToggle');
        if (pipButton) {
            pipButton.el().style.display = 'none';
        }
        // Hide theatre button on mobile (fallback)
        const theatreButton = this.player.controlBar.getChild('TheatreButton');
        if (theatreButton) {
            theatreButton.el().style.display = 'none';
        }
    }
    /**
     * Adds a theatre mode button to the video player control bar.
     */
    addTheatreButton() {
        const Button = videojs.getComponent('Button');
        const customControls = this; // Capture reference to CustomControls instance
        class TheatreButton extends Button {
            constructor(player, options) {
                super(player, options);
                this.controlText("Theatre Mode");
                this.addClass('vjs-theatre-button');
            }
            handleClick() {
                customControls.toggleTheatreMode();
            }
        }
        videojs.registerComponent('TheatreButton', TheatreButton);
        const controlBar = this.player.getChild('controlBar');
        const fullscreenIndex = controlBar.children()
            .findIndex((child) => child.name && child.name() === 'FullscreenToggle');
        const insertIndex = fullscreenIndex > 0 ? fullscreenIndex : controlBar.children().length - 1;
        controlBar.addChild('TheatreButton', {}, insertIndex);
    }
    /**
     * Sets up keyboard controls for TV devices.
     */
    setupKeyboardControls() {
        document.addEventListener('keydown', (e) => {
            if (!document.activeElement?.closest('.video-js') || !this.isTV)
                return;
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
 * Subtitle management for video player.
 *
 * Automatically detects and loads subtitle files matching the video ID.
 */
class SubtitleManager {
    /**
     * Creates an instance of SubtitleManager.
     * @param player - The video.js player instance
     * @param videoId - The video ID to match subtitle file
     */
    constructor(player, videoId) {
        /** Path to subtitle directory */
        this.subtitlePath = '/static/subtitles';
        this.player = player;
        this.videoId = videoId;
        this.init();
    }
    /**
     * Initializes subtitle loading by checking for file existence.
     */
    init() {
        if (!this.videoId) {
            console.log('No video ID provided for subtitles');
            return;
        }
        this.checkAndLoadSubtitle();
    }
    /**
     * Checks if subtitle file exists and loads it if available.
     */
    checkAndLoadSubtitle() {
        const subtitleUrl = `${this.subtitlePath}/${this.videoId}.vtt`;
        // Check if subtitle file exists
        fetch(subtitleUrl, { method: 'HEAD' })
            .then(response => {
            if (response.ok) {
                console.log(`Subtitle file found: ${subtitleUrl}`);
                this.addSubtitleTrack(subtitleUrl);
            }
            else {
                console.log(`No subtitle file found: ${subtitleUrl}`);
            }
        })
            .catch(err => {
            console.log('Error checking subtitle file:', err);
        });
    }
    /**
     * Adds subtitle track to the video player.
     * @param subtitleUrl - The URL to the subtitle file
     */
    addSubtitleTrack(subtitleUrl) {
        this.player.ready(() => {
            // Add text track to player using video.js method
            this.player.addRemoteTextTrack({
                kind: 'subtitles',
                label: 'English',
                srclang: 'en',
                src: subtitleUrl,
                default: false // Set to true to enable by default
            }, false);
            console.log(`Subtitle track added: ${subtitleUrl}`);
        });
    }
}
/**
 * Chapters menu positioner for video player.
 *
 * Adjusts the position of the chapters menu to fit within the viewport,
 * especially for mobile devices in portrait mode.
 */
class ChaptersMenuPositioner {
    constructor(player) {
        this.player = player;
        this.player.ready(() => this.hook());
    }
    hook() {
        const controlBar = this.player.controlBar;
        if (!controlBar || !controlBar.chaptersButton)
            return;
        const button = controlBar.chaptersButton;
        const menuEl = button?.menu?.el();
        if (!menuEl)
            return;
        const apply = () => this.apply(menuEl);
        button.on('menuopen', apply);
        button.on('menuclose', () => {
            menuEl.style.maxHeight = '';
            menuEl.style.left = '';
            menuEl.style.right = '';
        });
        window.addEventListener('resize', apply);
        window.addEventListener('orientationchange', () => setTimeout(apply, 150));
    }
    apply(menuEl) {
        const portrait = window.innerHeight >= window.innerWidth;
        const content = menuEl.querySelector('.vjs-menu-content');
        if (portrait) {
            menuEl.style.left = `${Math.max(10, (window.innerWidth - menuEl.offsetWidth) / 2)}px`;
            menuEl.style.right = 'auto';
            menuEl.style.bottom = '48px';
            if (content)
                content.style.maxHeight = `${Math.round(window.innerHeight * 0.5)}px`;
        }
        else {
            menuEl.style.left = `${Math.max(10, (window.innerWidth - menuEl.offsetWidth) / 2)}px`;
            menuEl.style.right = 'auto';
            menuEl.style.bottom = '56px';
            if (content)
                content.style.maxHeight = `${Math.round(window.innerHeight * 0.85)}px`;
        }
    }
}
/**
 * Main video player initialization event handler.
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
        const profileId = parseInt(videoElement.getAttribute('data-profile-id') || '0', 10);
        const videoId = parseInt(videoElement.getAttribute('data-video-id') || '0', 10);
        const currentTime = parseInt(videoElement.getAttribute('data-current-time') || '0', 10);
        // Initialize all modules when player is ready
        player.ready(() => {
            const contextMenu = new VideoContextMenu(player);
            const customControls = playerCore.container ? new CustomControls(player, playerCore.container) : null;
            // Link context menu to custom controls for theatre mode protection
            if (customControls) {
                customControls.setContextMenu(contextMenu);
            }
            // Initialize theatre mode handler
            if (playerCore.container) {
                handleTheatreMode(player, playerCore.container);
            }
            new UrlTimeHandler(player);
            new ProgressTracker(player, videoId, profileId, currentTime);
            new SubtitleManager(player, videoId);
            new ChaptersMenuPositioner(player);
            // Ensure control bar is visible
            player.controlBar.show();
        });
    });
});
/**
 * Handle theatre mode transitions
 * Manages wrapper positioning when entering/exiting theatre mode
 *
 * @param player - Video.js player instance
 * @param container - The video wrapper container element
 */
function handleTheatreMode(player, container) {
    const wrapper = container;
    if (!wrapper) {
        console.warn('Video wrapper not found for theatre mode handling');
        return;
    }
    // Store original parent and styles
    let originalParent = null;
    let originalNextSibling = null;
    /**
     * Enter theatre mode - move wrapper to document body
     */
    function enterTheatreMode() {
        // Store original position in DOM
        originalParent = wrapper.parentElement;
        originalNextSibling = wrapper.nextSibling;
        // Apply theatre mode styles
        wrapper.classList.add('theatre-mode-active');
        document.body.appendChild(wrapper);
        // Force reflow
        void wrapper.offsetWidth;
        // Disable body scroll
        document.body.style.overflow = 'hidden';
        console.log('Entered theatre mode');
    }
    /**
     * Exit theatre mode - restore wrapper to original position
     */
    function exitTheatreMode() {
        if (!originalParent)
            return;
        // Remove theatre mode class
        wrapper.classList.remove('theatre-mode-active');
        // Restore original position in DOM
        if (originalNextSibling) {
            originalParent.insertBefore(wrapper, originalNextSibling);
        }
        else {
            originalParent.appendChild(wrapper);
        }
        // Re-enable body scroll
        document.body.style.overflow = '';
        // Clear stored values
        originalParent = null;
        originalNextSibling = null;
        console.log('Exited theatre mode');
    }
    // Watch for theatre-mode class changes
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                if (wrapper.classList.contains('theatre-mode')) {
                    if (!wrapper.classList.contains('theatre-mode-active')) {
                        enterTheatreMode();
                    }
                }
                else {
                    if (wrapper.classList.contains('theatre-mode-active')) {
                        exitTheatreMode();
                    }
                }
            }
        });
    });
    // Start observing
    observer.observe(wrapper, {
        attributes: true,
        attributeFilter: ['class']
    });
    // Clean up on player dispose
    player.on('dispose', () => {
        observer.disconnect();
        if (wrapper.classList.contains('theatre-mode-active')) {
            exitTheatreMode();
        }
    });
}
//# sourceMappingURL=videoPlayer.js.map