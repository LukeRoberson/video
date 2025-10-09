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

// Declare videojs as a global variable
declare const videojs: any;

/**
 * Interface for video.js player instance
 */
interface VideoJsPlayer {
    ready(callback: () => void): void;
    on(event: string, callback: (...args: any[]) => void): void;
    one(event: string, callback: (...args: any[]) => void): void;
    off(event: string, callback?: (...args: any[]) => void): void;
    currentTime(): number;
    currentTime(seconds: number): VideoJsPlayer;
    duration(): number;
    paused(): boolean;
    play(): Promise<void>;
    pause(): void;
    volume(): number;
    volume(level: number): VideoJsPlayer;
    isFullscreen(): boolean;
    requestFullscreen(): void;
    userActive(active: boolean): void;
    el(): HTMLElement;
    tech(): { el(): HTMLVideoElement };
    controlBar: any;
    bigPlayButton: any;
    posterImage: any;
    getChild(name: string): any;
    addRemoteTextTrack(options: TextTrackOptions, manualCleanup: boolean): void;
}

/**
 * Interface for text track options
 */
interface TextTrackOptions {
    kind: string;
    label: string;
    srclang: string;
    src: string;
    default: boolean;
}

/**
 * Interface for API response structure
 */
interface ApiResponse {
    success: boolean;
    [key: string]: any;
}

/**
 * Type for snippet source
 */
type SnippetSource = 'url' | 'theme' | null;


/**
 * Global video player management for preventing multiple simultaneous playback.
 * 
 * Manages all video player instances and ensures only one video plays at a time
 * by automatically pausing other players when a new one starts playing.
 */
class GlobalPlayerManager {
    /** Singleton instance */
    private static instance: GlobalPlayerManager;
    
    /** Array of all registered video.js player instances */
    private players: VideoJsPlayer[] = [];

    /**
     * Creates the singleton instance of GlobalPlayerManager.
     */
    private constructor() {}

    /**
     * Gets the singleton instance of GlobalPlayerManager.
     * @returns The singleton instance
     */
    static getInstance(): GlobalPlayerManager {
        if (!GlobalPlayerManager.instance) {
            GlobalPlayerManager.instance = new GlobalPlayerManager();
        }
        return GlobalPlayerManager.instance;
    }

    /**
     * Registers a player instance and sets up play event monitoring.
     * @param player - The video.js player instance to register
     */
    registerPlayer(player: VideoJsPlayer): void {
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
    unregisterPlayer(player: VideoJsPlayer): void {
        const index = this.players.indexOf(player);
        if (index > -1) {
            this.players.splice(index, 1);
        }
    }

    /**
     * Pauses all players except the currently playing one.
     * @param currentPlayer - The player that should continue playing
     */
    pauseOtherPlayers(currentPlayer: VideoJsPlayer): void {
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
    /** The HTML element ID for the video player */
    private playerId: string;
    
    /** The video.js player instance */
    private player: VideoJsPlayer | null = null;
    
    /** The container element */
    public container: HTMLElement | null = null;
    
    /** Whether the device is detected as a TV */
    private isTV: boolean;
    
    /** Whether the device is a mobile device */
    private isMobile: boolean;
    
    /** Reference to the global player manager */
    private globalManager: GlobalPlayerManager;

    /**
     * Creates an instance of VideoPlayerCore.
     * @param playerId - The ID of the video element
     */
    constructor(playerId: string = 'player') {
        this.playerId = playerId;
        this.isTV = window.tvDetection?.isTV() || false;
        this.isMobile = this.detectMobile();
        this.globalManager = GlobalPlayerManager.getInstance();
    }

    /**
     * Detects if the device is a mobile device.
     * @returns True if mobile device detected
     */
    private detectMobile(): boolean {
        const mobileTest = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        const touchTest = navigator.maxTouchPoints && navigator.maxTouchPoints > 2 && /MacIntel/.test(navigator.platform);
        return mobileTest || Boolean(touchTest);
    }

    /**
     * Initializes the video.js player with configuration options.
     * @returns The initialized video.js player instance
     */
    initialize(): VideoJsPlayer {
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
        
        return this.player!;
    }

    /**
     * Sets up touch-based play/pause functionality for mobile devices.
     */
    private setupTouchPlayPause(): void {
        if (!this.player) return;
        
        // Check if device has touch capability
        const hasTouchSupport = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        
        if (!hasTouchSupport) return;
    
        this.player.ready(() => {
            if (!this.player) return;
            
            const videoElement = this.player.tech().el();
            const playerElement = this.player.el();
            let touchStartTime = 0;
            let touchMoved = false;
    
            // Handle touch start
            const handleTouchStart = (_e: TouchEvent): void => {
                touchStartTime = Date.now();
                touchMoved = false;
            };
    
            // Handle touch move (to detect if user is scrolling)
            const handleTouchMove = (_e: TouchEvent): void => {
                touchMoved = true;
            };
    
            // Handle touch end - toggle play/pause if it was a tap
            const handleTouchEnd = (e: TouchEvent): void => {
                if (!this.player) return;
                
                const touchEndTime = Date.now();
                const touchDuration = touchEndTime - touchStartTime;
                
                const target = e.target as HTMLElement;
                
                // Only trigger play/pause if conditions are met
                if (touchDuration < 300 && !touchMoved && !target.closest('.vjs-control-bar')) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    if (this.player.paused()) {
                        this.player.play();
                    } else {
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
    private setupMobileFullscreen(): void {
        if (!this.isMobile || !this.player) return;

        this.player.ready(() => {
            if (!this.player) return;
            
            // Enter fullscreen when play is triggered on mobile
            this.player.on('play', () => {
                if (!this.player) return;
                
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
    private applyTVSettings(): void {
        if (!this.isTV || !this.player) return;

        this.player.ready(() => {
            if (!this.player) return;
            
            const controlBar = this.player.controlBar.el();
            controlBar.style.height = '60px';
            controlBar.style.fontSize = '1.2em';
            
            this.player.off('userinactive');
            this.player.on('userinactive', () => {
                if (!this.player) return;
                
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
    private setupTVModeListener(): void {
        window.addEventListener('tvModeChanged', (e: Event) => {
            const customEvent = e as any;
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
    /** The video.js player instance */
    private player: VideoJsPlayer;
    
    /** The context menu DOM element */
    private contextMenu: HTMLElement;

    /**
     * Creates an instance of VideoContextMenu.
     * @param player - The video.js player instance
     */
    constructor(player: VideoJsPlayer) {
        this.player = player;
        this.contextMenu = this.createContextMenu();
        this.init();
    }

    /**
     * Initializes the context menu by creating DOM elements and setting up events.
     */
    private init(): void {
        this.setupEventListeners();
    }

    /**
     * Creates the context menu DOM structure and appends it to the document body.
     * @returns The created context menu element
     */
    private createContextMenu(): HTMLElement {
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
    private setupEventListeners(): void {
        const progressControl = this.player.controlBar.progressControl.el();
        const menuItem = this.contextMenu.querySelector('.video-context-menu-item') as HTMLElement;

        // Right-click handler
        progressControl.addEventListener('contextmenu', (e: MouseEvent) => this.showMenu(e));
        
        // Prevent right-click issues
        ['mousedown', 'mouseup'].forEach(event => {
            progressControl.addEventListener(event, (e: MouseEvent) => {
                if (e.button === 2) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            });
        });

        // Menu item click
        menuItem.addEventListener('click', (e: MouseEvent) => this.handleMenuClick(e));
        
        // Hide menu when clicking elsewhere
        document.addEventListener('click', (e: MouseEvent) => this.hideMenu(e), true);
    }

    /**
     * Shows the context menu at the cursor position.
     * @param e - The right-click mouse event
     * @returns Always returns false to prevent default context menu
     */
    private showMenu(e: MouseEvent): boolean {
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
     * @param e - The original mouse event for position reference
     */
    private adjustMenuPosition(e: MouseEvent): void {
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
     * @param e - The click event on the menu item
     */
    private handleMenuClick(e: MouseEvent): void {
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
     * @param e - The click event
     */
    private hideMenu(e: MouseEvent): void {
        if (this.contextMenu.style.display === 'block') {
            if (!this.contextMenu.contains(e.target as Node)) {
                this.hideMenuAndReEnablePlayer();
                e.preventDefault();
                e.stopPropagation();
            }
        }
    }

    /**
     * Hides the context menu and re-enables player pointer events.
     */
    private hideMenuAndReEnablePlayer(): void {
        this.contextMenu.style.display = 'none';
        this.player.el().style.pointerEvents = '';
    }

    /**
     * Generates a timestamped URL with the current video playback time.
     * @returns The URL with 't' parameter set to current time in seconds
     */
    private getTimestampedUrl(): string {
        const currentTime = Math.floor(this.player.currentTime());
        const url = new URL(window.location.href);
        url.searchParams.set('t', currentTime.toString());
        return url.toString();
    }

    /**
     * Shows a temporary notification message to the user.
     * @param message - The message to display in the notification
     */
    private showNotification(message: string): void {
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
    /** The video.js player instance */
    private player: VideoJsPlayer;
    
    /** The video ID for tracking */
    private videoId: number;
    
    /** The user profile ID */
    private profileId: number;
    
    /** Initial playback position in seconds */
    private initialTime: number;
    
    /** Timestamp of last progress update */
    private lastUpdateTime: number = 0;
    
    /** Whether video has been marked as watched */
    private hasMarkedWatched: boolean = false;

    /**
     * Creates an instance of ProgressTracker.
     * @param player - The video.js player instance
     * @param videoId - The video ID for tracking
     * @param profileId - The user profile ID
     * @param initialTime - Initial playback position in seconds
     */
    constructor(player: VideoJsPlayer, videoId: number, profileId: number, initialTime: number = 0) {
        this.player = player;
        this.videoId = videoId;
        this.profileId = profileId;
        this.initialTime = initialTime;
        
        this.init();
    }

    /**
     * Initializes the progress tracker and validates required parameters.
     */
    private init(): void {
        if (!this.profileId || !this.videoId) {
            console.error('Missing profileId or videoId. Progress tracking will not work.');
            return;
        }

        this.setupEventListeners();
    }

    /**
     * Sets up event listeners for video player events.
     */
    private setupEventListeners(): void {
        this.player.on('loadedmetadata', () => this.setInitialPosition());
        this.player.on('play', () => this.removeProgressOverlay());
        this.player.on('timeupdate', () => this.trackProgress());
        this.player.on('ended', () => this.handleVideoEnd());
    }

    /**
     * Sets the initial playback position when video metadata is loaded.
     */
    private setInitialPosition(): void {
        if (this.initialTime > 0) {
            console.log('Setting playback position to:', this.initialTime);
            this.player.currentTime(this.initialTime);
        }
    }

    /**
     * Removes the progress overlay element from the DOM when playback starts.
     */
    private removeProgressOverlay(): void {
        const progressOverlay = document.querySelector('.progress-overlay');
        if (progressOverlay) {
            progressOverlay.remove();
            console.log('Custom progress bar removed.');
        }
    }

    /**
     * Tracks video playback progress and automatically marks as watched.
     * Updates progress every 2 seconds and marks as watched at 96% completion.
     */
    private trackProgress(): void {
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
     * @param currentTime - The current playback time in seconds
     */
    private updateProgress(currentTime: number): void {
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
     */
    private markAsWatched(): void {
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
     */
    private handleVideoEnd(): void {
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
    /** The video.js player instance */
    private player: VideoJsPlayer;
    
    /** End time for snippet in seconds */
    private endTime: number | null = null;
    
    /** Whether we're currently in snippet mode */
    private isSnippet: boolean = false;
    
    /** Snippet indicator element */
    private snippetIndicator: HTMLElement | null = null;
    
    /** Source of snippet ('url' or 'theme') */
    private snippetSource: SnippetSource = null;

    /**
     * Creates an instance of UrlTimeHandler.
     * @param player - The video.js player instance
     */
    constructor(player: VideoJsPlayer) {
        this.player = player;
        this.init();
    }

    /**
     * Initializes the URL time handler by checking for 't' and 'end' parameters or data attributes.
     */
    private init(): void {
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
     * @param startTime - The start time in seconds
     * @param endTime - The end time in seconds
     */
    private setupSnippet(startTime: number, endTime: number): void {
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
    private jumpToTime(time: number): void {
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
    private createSnippetIndicator(startTime: number, endTime: number): void {
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
            const closeBtn = this.snippetIndicator.querySelector('.snippet-close') as HTMLElement;
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
    private highlightSnippetRange(startTime: number, endTime: number): void {
        console.log('highlightSnippetRange called - start:', startTime, 'end:', endTime);
        
        const createHighlight = (): void => {
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
     */
    private setupSnippetControls(): void {
        // Monitor playback to pause at end time
        const checkEndTime = (): void => {
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
            let startTime: number | null = null;

            if (this.snippetSource === 'url') {
                const urlParams = new URLSearchParams(window.location.search);
                const startParam = urlParams.get('t');
                startTime = startParam ? parseInt(startParam, 10) : null;
            } else if (this.snippetSource === 'theme') {
                const videoElement = this.player.el();
                const startAttr = videoElement.getAttribute('data-snippet-start');
                startTime = startAttr ? parseInt(startAttr, 10) : null;
            }
            
            if (startTime !== null && this.endTime !== null) {
                if (currentTime < startTime) {
                    this.player.currentTime(startTime);
                } else if (currentTime > this.endTime) {
                    this.player.currentTime(this.endTime);
                }
            }
        });
    }

    /**
     * Exits snippet mode and returns to normal video playback.
     * Only works for URL-based snippets, not theme-based ones.
     */
    private exitSnippetMode(): void {
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
        const url = new URL(window.location.href);
        url.searchParams.delete('end');
        window.history.replaceState({}, '', url.toString());
    }

    /**
     * Formats seconds into MM:SS or HH:MM:SS format.
     * @param seconds - Time in seconds
     * @returns Formatted time string
     */
    private formatTime(seconds: number): string {
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
    /** The video.js player instance */
    private player: VideoJsPlayer;
    
    /** The container element for the player */
    private container: HTMLElement;
    
    /** Whether the device is detected as a TV */
    private isTV: boolean;
    
    /** Whether the device is a mobile device */
    private isMobile: boolean;
    
    /** Bound click handler for theatre mode exit */
    private theatreModeClickHandler: ((e: MouseEvent) => void) | null = null;

    /**
     * Creates an instance of CustomControls.
     * @param player - The video.js player instance
     * @param container - The container element for the player
     */
    constructor(player: VideoJsPlayer, container: HTMLElement) {
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
    private detectMobile(): boolean {
        const mobileTest = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        const touchTest = navigator.maxTouchPoints && navigator.maxTouchPoints > 2 && /MacIntel/.test(navigator.platform);
        return mobileTest || Boolean(touchTest);
    }

    /**
     * Initializes custom controls by adding buttons and setting up keyboard controls.
     */
    private init(): void {
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
     * Sets up click handler for exiting theatre mode when clicking outside the player.
     */
    private setupTheatreModeClickHandler(): void {
        this.theatreModeClickHandler = (e: MouseEvent): void => {
            // Only handle clicks when in theatre mode
            if (!this.container.classList.contains('theatre-mode')) {
                return;
            }
            
            // Check if click is outside the video player container
            if (!this.container.contains(e.target as Node)) {
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
    private exitTheatreMode(): void {
        this.container.classList.remove('theatre-mode');
    }

    /**
     * Enters theatre mode by adding the theatre-mode class to the container.
     */
    private enterTheatreMode(): void {
        this.container.classList.add('theatre-mode');
    }

    /**
     * Toggles theatre mode on/off.
     */
    private toggleTheatreMode(): void {
        if (this.container.classList.contains('theatre-mode')) {
            this.exitTheatreMode();
        } else {
            this.enterTheatreMode();
        }
    }

    /**
     * Fallback method to hide buttons on mobile (safety net).
     */
    private hideMobileButtonsFallback(): void {
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
    private addTheatreButton(): void {
        const Button = videojs.getComponent('Button');
        const customControls = this; // Capture reference to CustomControls instance
        
        class TheatreButton extends Button {
            constructor(player: VideoJsPlayer, options: any) {
                super(player, options);
                (this as any).controlText("Theatre Mode");
                (this as any).addClass('vjs-theatre-button');
            }
            
            handleClick(): void {
                customControls.toggleTheatreMode();
            }
        }
    
        videojs.registerComponent('TheatreButton', TheatreButton);
        
        const controlBar = this.player.getChild('controlBar');
        const fullscreenIndex = controlBar.children()
            .findIndex((child: any) => child.name && child.name() === 'FullscreenToggle');
        const insertIndex = fullscreenIndex > 0 ? fullscreenIndex : controlBar.children().length - 1;
        
        controlBar.addChild('TheatreButton', {}, insertIndex);
    }

    /**
     * Sets up keyboard controls for TV devices.
     */
    private setupKeyboardControls(): void {
        document.addEventListener('keydown', (e: KeyboardEvent) => {
            if (!(document.activeElement as HTMLElement)?.closest('.video-js') || !this.isTV) return;

            const actions: Record<string, () => void> = {
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
    /** The video.js player instance */
    private player: VideoJsPlayer;
    
    /** The video ID for matching subtitle files */
    private videoId: number;
    
    /** Path to subtitle directory */
    private subtitlePath: string = '/static/subtitles';

    /**
     * Creates an instance of SubtitleManager.
     * @param player - The video.js player instance
     * @param videoId - The video ID to match subtitle file
     */
    constructor(player: VideoJsPlayer, videoId: number) {
        this.player = player;
        this.videoId = videoId;
        this.init();
    }

    /**
     * Initializes subtitle loading by checking for file existence.
     */
    private init(): void {
        if (!this.videoId) {
            console.log('No video ID provided for subtitles');
            return;
        }

        this.checkAndLoadSubtitle();
    }

    /**
     * Checks if subtitle file exists and loads it if available.
     */
    private checkAndLoadSubtitle(): void {
        const subtitleUrl = `${this.subtitlePath}/${this.videoId}.vtt`;
        
        // Check if subtitle file exists
        fetch(subtitleUrl, { method: 'HEAD' })
            .then(response => {
                if (response.ok) {
                    console.log(`Subtitle file found: ${subtitleUrl}`);
                    this.addSubtitleTrack(subtitleUrl);
                } else {
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
    private addSubtitleTrack(subtitleUrl: string): void {
        this.player.ready(() => {
            // Add text track to player using video.js method
            this.player.addRemoteTextTrack({
                kind: 'subtitles',
                label: 'English',
                srclang: 'en',
                src: subtitleUrl,
                default: false  // Set to true to enable by default
            }, false);
            
            console.log(`Subtitle track added: ${subtitleUrl}`);
        });
    }
}

/**
 * Main video player initialization event handler.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Find all video elements with the video-js class
    const videoElements = document.querySelectorAll<HTMLVideoElement>('video.video-js');
    
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
            new VideoContextMenu(player);
            if (playerCore.container) {
                new CustomControls(player, playerCore.container);
            }
            new UrlTimeHandler(player);
            new ProgressTracker(player, videoId, profileId, currentTime);
            new SubtitleManager(player, videoId);
            
            // Ensure control bar is visible
            player.controlBar.show();
        });
    });
});


/**
 * Form submission handler for marking videos as watched/unwatched.
 */
const markWatchedForm = document.getElementById('markWatchedForm') as HTMLFormElement;
if (markWatchedForm) {
    markWatchedForm.addEventListener('submit', function(e: Event) {
        e.preventDefault();

        const apiUrl = this.dataset.apiUrl || '';
        const videoId = this.dataset.videoId || '';

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ video_id: videoId })
        })
        .then(response => response.json())
        .then((data: ApiResponse) => {
            if (data.success && this.dataset.apiUrl === '/api/profile/mark_watched') {
                const button = this.querySelector('button');
                if (button) button.textContent = 'Watched!';
                this.dataset.apiUrl = '/api/profile/mark_unwatched';
            }
            else if (data.success && this.dataset.apiUrl === '/api/profile/mark_unwatched') {
                const button = this.querySelector('button');
                if (button) button.textContent = 'Unwatched!';
                this.dataset.apiUrl = '/api/profile/mark_watched';
            }
        })
        .catch(err => console.error('Error updating watched status:', err));
    });
}
