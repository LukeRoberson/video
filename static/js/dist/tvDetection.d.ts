/**
 * @fileoverview Comprehensive TV device detection module for web applications.
 * Provides automatic detection of TV devices and manual TV mode management.
 * Supports user preferences, URL parameters, and heuristic-based detection.
 */
/**
 * Configuration constants for TV detection
 */
declare const TVDetectionConfig: {
    /** Local storage key for TV mode preference */
    readonly STORAGE_KEY: "tvMode";
    /** URL parameter name for TV mode */
    readonly URL_PARAM: "tv";
    /** Minimum screen width for 4K TV detection */
    readonly MIN_4K_WIDTH: 2560;
    /** Minimum screen width for HD TV detection */
    readonly MIN_HD_WIDTH: 1920;
    /** Maximum pixel ratio for TV detection */
    readonly MAX_TV_PIXEL_RATIO: 1.5;
};
/**
 * TV mode information interface
 */
interface TVModeInfo {
    /** Current TV mode state */
    isTV: boolean;
    /** Source of the mode determination */
    source: 'preference' | 'url' | 'auto';
}
/**
 * TV mode change event detail interface
 */
interface TVModeChangeEvent extends CustomEvent {
    detail: {
        isTV: boolean;
    };
}
/**
 * Handles automatic TV device detection based on various heuristics
 */
declare class TVDeviceDetector {
    /**
     * Cached user agent string
     */
    private readonly userAgent;
    /**
     * Create a TVDeviceDetector instance
     */
    constructor();
    /**
     * Perform automatic TV device detection
     * @returns True if device is detected as TV
     */
    detectTVDevice(): boolean;
    /**
     * Check for definitive TV indicators in user agent
     * @returns True if definitive TV indicators found
     */
    private checkDefinitiveTVIndicators;
    /**
     * Check if user agent indicates a TV device
     * @returns True if TV user agent detected
     */
    private isTVUserAgent;
    /**
     * Check if user agent indicates a game console
     * @returns True if game console detected
     */
    private isGameConsole;
    /**
     * Check large screen heuristics for TV detection
     * @returns True if device appears to be a TV based on screen size
     */
    private checkLargeScreenHeuristics;
    /**
     * Check for non-touch TV characteristics
     * @param pixelRatio - Device pixel ratio
     * @param screenWidth - Screen width in pixels
     * @returns True if device has TV-like characteristics
     */
    private hasNonTouchTVCharacteristics;
}
/**
 * Manages TV mode preferences and storage
 */
declare class TVPreferenceManager {
    /**
     * Get TV mode preference from local storage
     * @returns TV mode preference or null if not set
     */
    getUserPreference(): boolean | null;
    /**
     * Set TV mode preference in local storage
     * @param enabled - Whether TV mode should be enabled
     */
    setUserPreference(enabled: boolean): void;
    /**
     * Remove TV mode preference from local storage
     */
    clearUserPreference(): void;
    /**
     * Check if user preference exists
     * @returns True if user has set a preference
     */
    hasUserPreference(): boolean;
}
/**
 * Handles URL parameter checking for TV mode
 */
declare class TVUrlParameterHandler {
    /**
     * Check if TV mode is specified in URL parameters
     * @returns TV mode from URL or null if not specified
     */
    getTVModeFromUrl(): boolean | null;
    /**
     * Check if URL contains TV parameter
     * @returns True if TV parameter exists in URL
     */
    hasUrlParameter(): boolean;
}
/**
 * Manages TV mode change events
 */
declare class TVEventManager {
    /**
     * Dispatch TV mode change event
     * @param isTV - Current TV mode state
     */
    dispatchTVModeChanged(isTV: boolean): void;
    /**
     * Add event listener for TV mode changes
     * @param callback - Callback function to execute on TV mode change
     * @returns Cleanup function to remove event listener
     */
    onTVModeChanged(callback: (isTV: boolean) => void): () => void;
}
/**
 * Comprehensive TV device detection and management system
 */
declare class TVDetection {
    /**
     * TV device detector instance
     */
    private readonly detector;
    /**
     * TV preference manager instance
     */
    private readonly preferenceManager;
    /**
     * URL parameter handler instance
     */
    private readonly urlHandler;
    /**
     * Event manager instance
     */
    private readonly eventManager;
    /**
     * Create a TVDetection instance
     */
    constructor();
    /**
     * Main TV detection function with priority order:
     * 1. User preference (localStorage)
     * 2. URL parameter
     * 3. Automatic detection
     * @returns True if device should be treated as TV
     */
    isTV(): boolean;
    /**
     * Toggle TV mode manually and save preference
     * @returns New TV mode state
     */
    toggleTVMode(): boolean;
    /**
     * Set TV mode explicitly and save preference
     * @param enabled - Whether TV mode should be enabled
     */
    setTVMode(enabled: boolean): void;
    /**
     * Reset to automatic detection by clearing user preference
     */
    resetToAuto(): void;
    /**
     * Get current TV mode source (preference, URL, or auto-detection)
     * @returns Object containing mode source information
     */
    getTVModeInfo(): TVModeInfo;
    /**
     * Add event listener for TV mode changes
     * @param callback - Callback function
     * @returns Cleanup function
     */
    onTVModeChanged(callback: (isTV: boolean) => void): () => void;
    /**
     * Get device detector instance for advanced usage
     * @returns Device detector instance
     */
    getDetector(): TVDeviceDetector;
    /**
     * Force refresh of TV detection state
     */
    refresh(): void;
}
declare global {
    interface Window {
        tvDetection: TVDetection;
        isTV: () => boolean;
    }
}
export { TVDetection, TVDeviceDetector, TVPreferenceManager, TVUrlParameterHandler, TVEventManager, TVDetectionConfig, type TVModeInfo, type TVModeChangeEvent };
//# sourceMappingURL=tvDetection.d.ts.map