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
    tech(options?: {
        IWillNotUseThisInPlugins: boolean;
    }): {
        el(): HTMLVideoElement;
    };
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
declare class GlobalPlayerManager {
    /** Singleton instance */
    private static instance;
    /** Array of all registered video.js player instances */
    private players;
    /**
     * Creates the singleton instance of GlobalPlayerManager.
     */
    private constructor();
    /**
     * Gets the singleton instance of GlobalPlayerManager.
     * @returns The singleton instance
     */
    static getInstance(): GlobalPlayerManager;
    /**
     * Registers a player instance and sets up play event monitoring.
     * @param player - The video.js player instance to register
     */
    registerPlayer(player: VideoJsPlayer): void;
    /**
     * Unregisters a player instance from management.
     * @param player - The video.js player instance to unregister
     */
    unregisterPlayer(player: VideoJsPlayer): void;
    /**
     * Pauses all players except the currently playing one.
     * @param currentPlayer - The player that should continue playing
     */
    pauseOtherPlayers(currentPlayer: VideoJsPlayer): void;
}
/**
 * Core video player initialization and configuration.
 *
 * Handles the main video.js player setup, TV mode detection,
 * and responsive settings configuration.
 */
declare class VideoPlayerCore {
    /** The HTML element ID for the video player */
    private playerId;
    /** The video.js player instance */
    private player;
    /** The container element */
    container: HTMLElement | null;
    /** Whether the device is detected as a TV */
    private isTV;
    /** Whether the device is a mobile device */
    private isMobile;
    /** Reference to the global player manager */
    private globalManager;
    /**
     * Creates an instance of VideoPlayerCore.
     * @param playerId - The ID of the video element
     */
    constructor(playerId?: string);
    /**
     * Detects if the device is a mobile device.
     * @returns True if mobile device detected
     */
    private detectMobile;
    /**
     * Initializes the video.js player with configuration options.
     * @returns The initialized video.js player instance
     */
    initialize(): VideoJsPlayer;
    /**
     * Sets up touch-based play/pause functionality for mobile devices.
     */
    private setupTouchPlayPause;
    /**
     * Sets up automatic fullscreen behavior for mobile devices.
     */
    private setupMobileFullscreen;
    /**
     * Applies TV-specific settings to the player interface.
     */
    private applyTVSettings;
    /**
     * Sets up event listener for TV mode changes.
     */
    private setupTVModeListener;
}
/**
 * Right-click context menu functionality for the video player.
 *
 * Provides a context menu when right-clicking on the video progress bar,
 * allowing users to copy timestamped URLs for sharing specific moments.
 */
declare class VideoContextMenu {
    /** The video.js player instance */
    private player;
    /** The context menu DOM element */
    private contextMenu;
    /** Flag to prevent theatre mode exit during menu operations */
    private isMenuOperation;
    /**
     * Creates an instance of VideoContextMenu.
     * @param player - The video.js player instance
     */
    constructor(player: VideoJsPlayer);
    /**
     * Initializes the context menu by creating DOM elements and setting up events.
     */
    private init;
    /**
     * Creates the context menu DOM structure and appends it to the document body.
     * @returns The created context menu element
     */
    private createContextMenu;
    /**
     * Sets up event listeners for right-click, menu interactions, and hiding the menu.
     */
    private setupEventListeners;
    /**
     * Shows the context menu at the cursor position.
     * @param e - The right-click mouse event
     * @returns Always returns false to prevent default context menu
     */
    private showMenu;
    /**
     * Adjusts the menu position to ensure it stays within the viewport.
     * @param e - The original mouse event for position reference
     */
    private adjustMenuPosition;
    /**
     * Handles menu item click by copying timestamped URL to clipboard.
     */
    private handleMenuClick;
    /**
     * Hides the context menu when clicking outside of it.
     * @param e - The click event
     */
    private hideMenu;
    /**
     * Hides the context menu and re-enables player pointer events.
     */
    private hideMenuAndReEnablePlayer;
    /**
     * Checks if a menu operation is currently in progress.
     * @returns True if menu operation is active
     */
    isMenuActive(): boolean;
    /**
     * Generates a timestamped URL with the current video playback time.
     * @returns The URL with 't' parameter set to current time in seconds
     */
    private getTimestampedUrl;
    /**
     * Shows a temporary notification message to the user.
     * @param message - The message to display in the notification
     */
    private showNotification;
}
/**
 * Video progress tracking and watched status management.
 *
 * Tracks video playback progress, saves position for resume functionality,
 * and automatically marks videos as watched when 96% complete.
 */
declare class ProgressTracker {
    /** The video.js player instance */
    private player;
    /** The video ID for tracking */
    private videoId;
    /** The user profile ID */
    private profileId;
    /** Initial playback position in seconds */
    private initialTime;
    /** Timestamp of last progress update */
    private lastUpdateTime;
    /** Whether video has been marked as watched */
    private hasMarkedWatched;
    /**
     * Creates an instance of ProgressTracker.
     * @param player - The video.js player instance
     * @param videoId - The video ID for tracking
     * @param profileId - The user profile ID
     * @param initialTime - Initial playback position in seconds
     */
    constructor(player: VideoJsPlayer, videoId: number, profileId: number, initialTime?: number);
    /**
     * Initializes the progress tracker and validates required parameters.
     */
    private init;
    /**
     * Sets up event listeners for video player events.
     */
    private setupEventListeners;
    /**
     * Sets the initial playback position when video metadata is loaded.
     */
    private setInitialPosition;
    /**
     * Removes the progress overlay element from the DOM when playback starts.
     */
    private removeProgressOverlay;
    /**
     * Tracks video playback progress and automatically marks as watched.
     * Updates progress every 2 seconds and marks as watched at 96% completion.
     */
    private trackProgress;
    /**
     * Sends progress update to the server API.
     * @param currentTime - The current playback time in seconds
     */
    private updateProgress;
    /**
     * Marks the video as watched and removes it from in-progress list.
     * Sends API requests to update watched status and clean up progress tracking.
     */
    private markAsWatched;
    /**
     * Handles video playback completion.
     * Removes theatre mode class from container if active.
     */
    private handleVideoEnd;
}
/**
 * Handles URL 't' and 'end' parameters for video snippets, and theme-based snippets.
 *
 * Automatically detects timestamp parameters in the URL or data attributes and
 * creates video snippets by jumping to start time and pausing at end time.
 * Supports both URL parameters (?t=60&end=120) and theme data attributes.
 */
declare class UrlTimeHandler {
    /** The video.js player instance */
    private player;
    /** End time for snippet in seconds */
    private endTime;
    /** Whether we're currently in snippet mode */
    private isSnippet;
    /** Snippet indicator element */
    private snippetIndicator;
    /** Source of snippet ('url' or 'theme') */
    private snippetSource;
    /**
     * Creates an instance of UrlTimeHandler.
     * @param player - The video.js player instance
     */
    constructor(player: VideoJsPlayer);
    /**
     * Initializes the URL time handler by checking for 't' and 'end' parameters or data attributes.
     */
    private init;
    /**
     * Sets up a video snippet with start and end times.
     * @param startTime - The start time in seconds
     * @param endTime - The end time in seconds
     */
    private setupSnippet;
    /**
     * Jumps the video to a specific time and prepares for playback.
     * @param time - The time in seconds to jump to
     */
    private jumpToTime;
    /**
     * Creates visual indicator for snippet mode.
     * @param startTime - Snippet start time
     * @param endTime - Snippet end time
     */
    private createSnippetIndicator;
    /**
     * Highlights the snippet range on the progress bar.
     * @param startTime - Snippet start time
     * @param endTime - Snippet end time
     */
    private highlightSnippetRange;
    /**
     * Sets up snippet-specific controls and behavior.
     */
    private setupSnippetControls;
    /**
     * Exits snippet mode and returns to normal video playback.
     * Only works for URL-based snippets, not theme-based ones.
     */
    private exitSnippetMode;
    /**
     * Formats seconds into MM:SS or HH:MM:SS format.
     * @param seconds - Time in seconds
     * @returns Formatted time string
     */
    private formatTime;
}
/**
 * Custom player controls and buttons.
 *
 * Adds custom functionality to the video player including theatre mode button
 * and keyboard controls for TV devices.
 */
declare class CustomControls {
    /** The video.js player instance */
    private player;
    /** The container element for the player */
    private container;
    /** Whether the device is detected as a TV */
    private isTV;
    /** Whether the device is a mobile device */
    private isMobile;
    /** Bound click handler for theatre mode exit */
    private theatreModeClickHandler;
    /** Reference to context menu for checking menu state */
    private contextMenu;
    /**
     * Creates an instance of CustomControls.
     * @param player - The video.js player instance
     * @param container - The container element for the player
     */
    constructor(player: VideoJsPlayer, container: HTMLElement);
    /**
     * Detects if the device is a mobile device.
     * @returns True if mobile device detected
     */
    private detectMobile;
    /**
     * Initializes custom controls by adding buttons and setting up keyboard controls.
     */
    private init;
    /**
     * Sets a reference to the context menu for state checking.
     * @param contextMenu - The VideoContextMenu instance
     */
    setContextMenu(contextMenu: VideoContextMenu): void;
    /**
     * Sets up click handler for exiting theatre mode when clicking outside the player.
     */
    private setupTheatreModeClickHandler;
    /**
     * Exits theatre mode by removing the theatre-mode class from the container.
     */
    private exitTheatreMode;
    /**
     * Enters theatre mode by adding the theatre-mode class to the container.
     */
    private enterTheatreMode;
    /**
     * Toggles theatre mode on/off.
     */
    private toggleTheatreMode;
    /**
     * Fallback method to hide buttons on mobile (safety net).
     */
    private hideMobileButtonsFallback;
    /**
     * Adds a theatre mode button to the video player control bar.
     */
    private addTheatreButton;
    /**
     * Sets up keyboard controls for TV devices.
     */
    private setupKeyboardControls;
}
/**
 * Subtitle management for video player.
 *
 * Automatically detects and loads subtitle files matching the video ID.
 */
declare class SubtitleManager {
    /** The video.js player instance */
    private player;
    /** The video ID for matching subtitle files */
    private videoId;
    /** Path to subtitle directory */
    private subtitlePath;
    /**
     * Creates an instance of SubtitleManager.
     * @param player - The video.js player instance
     * @param videoId - The video ID to match subtitle file
     */
    constructor(player: VideoJsPlayer, videoId: number);
    /**
     * Initializes subtitle loading by checking for file existence.
     */
    private init;
    /**
     * Checks if subtitle file exists and loads it if available.
     */
    private checkAndLoadSubtitle;
    /**
     * Adds subtitle track to the video player.
     * @param subtitleUrl - The URL to the subtitle file
     */
    private addSubtitleTrack;
}
/**
 * Chapters menu positioner for video player.
 *
 * Adjusts the position of the chapters menu to fit within the viewport,
 * especially for mobile devices in portrait mode.
 */
declare class ChaptersMenuPositioner {
    private player;
    constructor(player: VideoJsPlayer);
    private hook;
    private apply;
}
/**
 * Form submission handler for marking videos as watched/unwatched.
 */
declare const markWatchedForm: HTMLFormElement;
//# sourceMappingURL=videoPlayer.d.ts.map