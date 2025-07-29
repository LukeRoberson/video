/**
 * Comprehensive TV device detection module
 */
class TVDetection {
    constructor() {
        this.storageKey = 'tvMode';
        this.urlParam = 'tv';
    }

    /**
     * Main TV detection function
     */
    isTV() {
        // Check user preference first
        const userPreference = localStorage.getItem(this.storageKey);
        if (userPreference !== null) {
            return userPreference === 'true';
        }
        
        // Check URL parameter
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has(this.urlParam)) {
            return urlParams.get(this.urlParam) === 'true';
        }
        
        // Auto-detect
        return this.detectTVDevice();
    }

    /**
     * Automatic TV device detection
     */
    detectTVDevice() {
        const userAgent = navigator.userAgent.toLowerCase();
        const screenWidth = window.innerWidth;
        const pixelRatio = window.devicePixelRatio || 1;
        
        // Definitive TV indicators
        const isTVUserAgent = /smart-tv|smarttv|googletv|appletv|hbbtv|tizen|webos|roku|viera|aquos/i.test(userAgent);
        const isGameConsole = /playstation|xbox|nintendo/i.test(userAgent);
        
        if (isTVUserAgent || isGameConsole) return true;
        
        // Large screen heuristics (more restrictive than before)
        const isLikelyTV = screenWidth >= 2560 || // 4K or larger
                          (screenWidth >= 1920 && 
                           !('ontouchstart' in window) && 
                           navigator.maxTouchPoints === 0 &&
                           pixelRatio <= 1.5 &&
                           window.screen.width === screenWidth); // Fullscreen
        
        return isLikelyTV;
    }

    /**
     * Toggle TV mode manually
     */
    toggleTVMode() {
        const currentMode = this.isTV();
        localStorage.setItem(this.storageKey, (!currentMode).toString());
        
        // Dispatch custom event for other components to listen
        window.dispatchEvent(new CustomEvent('tvModeChanged', { 
            detail: { isTV: !currentMode } 
        }));
        
        return !currentMode;
    }

    /**
     * Set TV mode explicitly
     */
    setTVMode(enabled) {
        localStorage.setItem(this.storageKey, enabled.toString());
        window.dispatchEvent(new CustomEvent('tvModeChanged', { 
            detail: { isTV: enabled } 
        }));
    }

    /**
     * Reset to auto-detection
     */
    resetToAuto() {
        localStorage.removeItem(this.storageKey);
        window.dispatchEvent(new CustomEvent('tvModeChanged', { 
            detail: { isTV: this.detectTVDevice() } 
        }));
    }
}

// Create global instance
window.tvDetection = new TVDetection();

// Backward compatibility
window.isTV = () => window.tvDetection.isTV();