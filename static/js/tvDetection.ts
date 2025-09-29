/**
 * @fileoverview Comprehensive TV device detection module for web applications.
 * Provides automatic detection of TV devices and manual TV mode management.
 * Supports user preferences, URL parameters, and heuristic-based detection.
 */

/**
 * Configuration constants for TV detection
 */
const TVDetectionConfig = {
    /** Local storage key for TV mode preference */
    STORAGE_KEY: 'tvMode',
    /** URL parameter name for TV mode */
    URL_PARAM: 'tv',
    /** Minimum screen width for 4K TV detection */
    MIN_4K_WIDTH: 2560,
    /** Minimum screen width for HD TV detection */
    MIN_HD_WIDTH: 1920,
    /** Maximum pixel ratio for TV detection */
    MAX_TV_PIXEL_RATIO: 1.5
} as const;

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
class TVDeviceDetector {
    /**
     * Cached user agent string
     */
    private readonly userAgent: string;

    /**
     * Create a TVDeviceDetector instance
     */
    constructor() {
        this.userAgent = navigator.userAgent.toLowerCase();
    }

    /**
     * Perform automatic TV device detection
     * @returns True if device is detected as TV
     */
    detectTVDevice(): boolean {
        return this.checkDefinitiveTVIndicators() || this.checkLargeScreenHeuristics();
    }

    /**
     * Check for definitive TV indicators in user agent
     * @returns True if definitive TV indicators found
     */
    private checkDefinitiveTVIndicators(): boolean {
        return this.isTVUserAgent() || this.isGameConsole();
    }

    /**
     * Check if user agent indicates a TV device
     * @returns True if TV user agent detected
     */
    private isTVUserAgent(): boolean {
        const tvPatterns = /smart-tv|smarttv|googletv|appletv|hbbtv|tizen|webos|roku|viera|aquos/i;
        return tvPatterns.test(this.userAgent);
    }

    /**
     * Check if user agent indicates a game console
     * @returns True if game console detected
     */
    private isGameConsole(): boolean {
        const consolePatterns = /playstation|xbox|nintendo/i;
        return consolePatterns.test(this.userAgent);
    }

    /**
     * Check large screen heuristics for TV detection
     * @returns True if device appears to be a TV based on screen size
     */
    private checkLargeScreenHeuristics(): boolean {
        const screenWidth = window.innerWidth;
        const pixelRatio = window.devicePixelRatio || 1;

        // 4K or larger screens
        if (screenWidth >= TVDetectionConfig.MIN_4K_WIDTH) {
            return true;
        }

        // HD screens with TV-like characteristics
        if (screenWidth >= TVDetectionConfig.MIN_HD_WIDTH) {
            return this.hasNonTouchTVCharacteristics(pixelRatio, screenWidth);
        }

        return false;
    }

    /**
     * Check for non-touch TV characteristics
     * @param pixelRatio - Device pixel ratio
     * @param screenWidth - Screen width in pixels
     * @returns True if device has TV-like characteristics
     */
    private hasNonTouchTVCharacteristics(pixelRatio: number, screenWidth: number): boolean {
        const hasNoTouch = !('ontouchstart' in window) && navigator.maxTouchPoints === 0;
        const hasLowPixelRatio = pixelRatio <= TVDetectionConfig.MAX_TV_PIXEL_RATIO;
        const isFullscreen = window.screen.width === screenWidth;

        return hasNoTouch && hasLowPixelRatio && isFullscreen;
    }
}

/**
 * Manages TV mode preferences and storage
 */
class TVPreferenceManager {
    /**
     * Get TV mode preference from local storage
     * @returns TV mode preference or null if not set
     */
    getUserPreference(): boolean | null {
        const preference = localStorage.getItem(TVDetectionConfig.STORAGE_KEY);
        return preference !== null ? preference === 'true' : null;
    }

    /**
     * Set TV mode preference in local storage
     * @param enabled - Whether TV mode should be enabled
     */
    setUserPreference(enabled: boolean): void {
        localStorage.setItem(TVDetectionConfig.STORAGE_KEY, enabled.toString());
    }

    /**
     * Remove TV mode preference from local storage
     */
    clearUserPreference(): void {
        localStorage.removeItem(TVDetectionConfig.STORAGE_KEY);
    }

    /**
     * Check if user preference exists
     * @returns True if user has set a preference
     */
    hasUserPreference(): boolean {
        return localStorage.getItem(TVDetectionConfig.STORAGE_KEY) !== null;
    }
}

/**
 * Handles URL parameter checking for TV mode
 */
class TVUrlParameterHandler {
    /**
     * Check if TV mode is specified in URL parameters
     * @returns TV mode from URL or null if not specified
     */
    getTVModeFromUrl(): boolean | null {
        const urlParams = new URLSearchParams(window.location.search);
        
        if (!urlParams.has(TVDetectionConfig.URL_PARAM)) {
            return null;
        }

        return urlParams.get(TVDetectionConfig.URL_PARAM) === 'true';
    }

    /**
     * Check if URL contains TV parameter
     * @returns True if TV parameter exists in URL
     */
    hasUrlParameter(): boolean {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.has(TVDetectionConfig.URL_PARAM);
    }
}

/**
 * Manages TV mode change events
 */
class TVEventManager {
    /**
     * Dispatch TV mode change event
     * @param isTV - Current TV mode state
     */
    dispatchTVModeChanged(isTV: boolean): void {
        const event = new CustomEvent('tvModeChanged', {
            detail: { isTV }
        }) as TVModeChangeEvent;
        
        window.dispatchEvent(event);
    }

    /**
     * Add event listener for TV mode changes
     * @param callback - Callback function to execute on TV mode change
     * @returns Cleanup function to remove event listener
     */
    onTVModeChanged(callback: (isTV: boolean) => void): () => void {
        const handler = (event: TVModeChangeEvent) => callback(event.detail.isTV);
        window.addEventListener('tvModeChanged', handler as EventListener);
        
        // Return cleanup function
        return () => window.removeEventListener('tvModeChanged', handler as EventListener);
    }
}

/**
 * Comprehensive TV device detection and management system
 */
class TVDetection {
    /**
     * TV device detector instance
     */
    private readonly detector: TVDeviceDetector;
    
    /**
     * TV preference manager instance
     */
    private readonly preferenceManager: TVPreferenceManager;
    
    /**
     * URL parameter handler instance
     */
    private readonly urlHandler: TVUrlParameterHandler;
    
    /**
     * Event manager instance
     */
    private readonly eventManager: TVEventManager;

    /**
     * Create a TVDetection instance
     */
    constructor() {
        this.detector = new TVDeviceDetector();
        this.preferenceManager = new TVPreferenceManager();
        this.urlHandler = new TVUrlParameterHandler();
        this.eventManager = new TVEventManager();
    }

    /**
     * Main TV detection function with priority order:
     * 1. User preference (localStorage)
     * 2. URL parameter
     * 3. Automatic detection
     * @returns True if device should be treated as TV
     */
    isTV(): boolean {
        // Check user preference first (highest priority)
        const userPreference = this.preferenceManager.getUserPreference();
        if (userPreference !== null) {
            return userPreference;
        }
        
        // Check URL parameter (medium priority)
        const urlTV = this.urlHandler.getTVModeFromUrl();
        if (urlTV !== null) {
            return urlTV;
        }
        
        // Fall back to automatic detection (lowest priority)
        return this.detector.detectTVDevice();
    }

    /**
     * Toggle TV mode manually and save preference
     * @returns New TV mode state
     */
    toggleTVMode(): boolean {
        const currentMode = this.isTV();
        const newMode = !currentMode;
        
        this.setTVMode(newMode);
        return newMode;
    }

    /**
     * Set TV mode explicitly and save preference
     * @param enabled - Whether TV mode should be enabled
     */
    setTVMode(enabled: boolean): void {
        this.preferenceManager.setUserPreference(enabled);
        this.eventManager.dispatchTVModeChanged(enabled);
    }

    /**
     * Reset to automatic detection by clearing user preference
     */
    resetToAuto(): void {
        this.preferenceManager.clearUserPreference();
        const autoDetectedMode = this.detector.detectTVDevice();
        this.eventManager.dispatchTVModeChanged(autoDetectedMode);
    }

    /**
     * Get current TV mode source (preference, URL, or auto-detection)
     * @returns Object containing mode source information
     */
    getTVModeInfo(): TVModeInfo {
        const userPreference = this.preferenceManager.getUserPreference();
        if (userPreference !== null) {
            return { isTV: userPreference, source: 'preference' };
        }
        
        const urlTV = this.urlHandler.getTVModeFromUrl();
        if (urlTV !== null) {
            return { isTV: urlTV, source: 'url' };
        }
        
        const autoDetected = this.detector.detectTVDevice();
        return { isTV: autoDetected, source: 'auto' };
    }

    /**
     * Add event listener for TV mode changes
     * @param callback - Callback function
     * @returns Cleanup function
     */
    onTVModeChanged(callback: (isTV: boolean) => void): () => void {
        return this.eventManager.onTVModeChanged(callback);
    }

    /**
     * Get device detector instance for advanced usage
     * @returns Device detector instance
     */
    getDetector(): TVDeviceDetector {
        return this.detector;
    }

    /**
     * Force refresh of TV detection state
     */
    refresh(): void {
        const currentMode = this.isTV();
        this.eventManager.dispatchTVModeChanged(currentMode);
    }
}

// Global window interface extension
declare global {
    interface Window {
        tvDetection: TVDetection;
        isTV: () => boolean;
    }
}

// Create global instance
window.tvDetection = new TVDetection();

/**
 * Backward compatibility function
 * @deprecated Use window.tvDetection.isTV() instead
 * @returns True if device is TV
 */
window.isTV = (): boolean => window.tvDetection.isTV();

export {
    TVDetection,
    TVDeviceDetector,
    TVPreferenceManager,
    TVUrlParameterHandler,
    TVEventManager,
    TVDetectionConfig,
    type TVModeInfo,
    type TVModeChangeEvent
};