/**
 * @fileoverview Watched videos toggle functionality for video manager.
 * Handles hiding and showing watched videos with localStorage persistence and dynamic content support.
 * Integrates with dynamically loaded video content.
 */
/**
 * Configuration constants for watched video toggle
 */
declare const WatchedToggleConfig: {
    /** Local storage key for toggle state */
    readonly STORAGE_KEY: "hideWatchedVideos";
    /** Delay for DOM updates after mutation */
    readonly DOM_UPDATE_DELAY: 100;
    /** Initial load delay for existing content */
    readonly INITIAL_LOAD_DELAY: 500;
    /** CSS class applied to body when hiding watched videos */
    readonly BODY_CLASS: "hide-watched";
};
/**
 * Handles visibility toggling of watched video elements
 */
declare class WatchedVideoVisibilityManager {
    /** CSS selectors for watched video elements */
    private watchedSelectors;
    /**
     * Create a watched video visibility manager
     */
    constructor();
    /**
     * Apply hide/show functionality to all watched videos
     * @param hideWatched - Whether to hide watched videos
     */
    applyWatchedVisibility(hideWatched: boolean): void;
}
/**
 * Callback type for when video elements are added
 */
type VideoElementsAddedCallback = () => void;
/**
 * Handles observation of dynamically added video content
 */
declare class DynamicContentObserver {
    /** Callback for when video elements are added */
    private onVideoElementsAdded;
    /** DOM mutation observer */
    private observer;
    /**
     * Create a dynamic content observer
     * @param onVideoElementsAdded - Callback when video elements are added
     */
    constructor(onVideoElementsAdded: VideoElementsAddedCallback);
    /**
     * Initialize observation of dynamic content
     */
    initialize(): void;
    /**
     * Observe thumbnail containers for changes
     */
    private observeContainers;
    /**
     * Disconnect the observer
     */
    disconnect(): void;
}
/**
 * Custom event detail for watched toggle changes
 */
interface WatchedToggleEventDetail {
    hideWatched: boolean;
}
/**
 * Custom event for watched toggle changes
 */
interface WatchedToggleEvent extends CustomEvent {
    detail: WatchedToggleEventDetail;
}
/**
 * Main controller for watched video toggle functionality
 */
declare class WatchedVideoToggleController {
    /** Toggle input element */
    private toggleElement;
    /** Visibility manager instance */
    private visibilityManager;
    /** Dynamic content observer instance */
    private contentObserver;
    /**
     * Create a watched video toggle controller
     */
    constructor();
    /**
     * Initialize the toggle functionality
     */
    initialize(): void;
    /**
     * Set up event listeners for the toggle
     */
    private setupEventListeners;
    /**
     * Handle toggle state changes
     */
    private handleToggleChange;
    /**
     * Apply toggle state to DOM and visibility
     * @param isChecked - Whether toggle is checked
     */
    private applyToggleState;
    /**
     * Save toggle state to localStorage
     * @param isChecked - Whether toggle is checked
     */
    private saveToggleState;
    /**
     * Load saved toggle state from localStorage
     */
    private loadSavedState;
    /**
     * Initialize dynamic content observer
     */
    private initializeDynamicContentObserver;
    /**
     * Apply initial visibility to existing content
     */
    private applyInitialVisibility;
    /**
     * Dispatch custom event for toggle changes
     * @param isChecked - Whether toggle is checked
     */
    private dispatchToggleEvent;
    /**
     * Get current toggle state
     * @returns Current toggle state
     */
    getToggleState(): boolean;
    /**
     * Set toggle state programmatically
     * @param state - New toggle state
     */
    setToggleState(state: boolean): void;
    /**
     * Cleanup and destroy the controller
     */
    destroy(): void;
}
declare let watchedToggleController: WatchedVideoToggleController | undefined;
//# sourceMappingURL=toggleWatched.d.ts.map