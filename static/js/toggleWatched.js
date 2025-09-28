/**
 * @fileoverview Watched videos toggle functionality for video manager.
 * Handles hiding and showing watched videos with localStorage persistence and dynamic content support.
 * Integrates with dynamically loaded video content.
 */

/**
 * Configuration constants for watched video toggle
 * @readonly
 * @enum {number|string}
 */
const WatchedToggleConfig = {
    /** Local storage key for toggle state */
    STORAGE_KEY: 'hideWatchedVideos',
    /** Delay for DOM updates after mutation */
    DOM_UPDATE_DELAY: 100,
    /** Initial load delay for existing content */
    INITIAL_LOAD_DELAY: 500,
    /** CSS class applied to body when hiding watched videos */
    BODY_CLASS: 'hide-watched'
};

/**
 * Handles visibility toggling of watched video elements
 * @class WatchedVideoVisibilityManager
 */
class WatchedVideoVisibilityManager {
    /**
     * Create a watched video visibility manager
     * @memberof WatchedVideoVisibilityManager
     */
    constructor() {
        /** @private {Array<string>} CSS selectors for watched video elements */
        this.watchedSelectors = [
            '.video-item--watched',
            '.video-card--watched', 
            '.thumbnail--watched',
            '.video-thumbnail--watched',
            '[data-watched="true"]'
        ];
    }

    /**
     * Apply hide/show functionality to all watched videos
     * @param {boolean} hideWatched - Whether to hide watched videos
     * @memberof WatchedVideoVisibilityManager
     */
    applyWatchedVisibility(hideWatched) {
        this.watchedSelectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (hideWatched) {
                    element.style.display = 'none';
                    element.setAttribute('data-hidden-by-toggle', 'true');
                } else {
                    element.style.display = '';
                    element.removeAttribute('data-hidden-by-toggle');
                }
            });
        });
    }
}


/**
 * Handles observation of dynamically added video content
 * @class DynamicContentObserver
 */
class DynamicContentObserver {
    /**
     * Create a dynamic content observer
     * @param {Function} onVideoElementsAdded - Callback when video elements are added
     * @memberof DynamicContentObserver
     */
    constructor(onVideoElementsAdded) {
        /** @private {Function} Callback for when video elements are added */
        this.onVideoElementsAdded = onVideoElementsAdded;
        /** @private {MutationObserver} DOM mutation observer */
        this.observer = null;
    }

    /**
     * Initialize observation of dynamic content
     * @memberof DynamicContentObserver
     */
    initialize() {
        this.observer = new MutationObserver(mutations => {
            let shouldApplyVisibility = false;
            
            mutations.forEach(mutation => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    const addedVideoElements = Array.from(mutation.addedNodes).some(node => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            return node.matches('.video-item, .video-card, .thumbnail, .video-thumbnail') ||
                                   node.querySelector('.video-item, .video-card, .thumbnail, .video-thumbnail');
                        }
                        return false;
                    });
                    
                    if (addedVideoElements) {
                        shouldApplyVisibility = true;
                    }
                }
            });
            
            if (shouldApplyVisibility) {
                setTimeout(() => {
                    this.onVideoElementsAdded();
                }, WatchedToggleConfig.DOM_UPDATE_DELAY);
            }
        });
        
        this.observeContainers();
    }

    /**
     * Observe thumbnail containers for changes
     * @private
     * @memberof DynamicContentObserver
     */
    observeContainers() {
        const thumbnailContainers = document.querySelectorAll('.thumbnails');
        thumbnailContainers.forEach(container => {
            this.observer.observe(container, {
                childList: true,
                subtree: true
            });
        });
        
        const mainContainer = document.querySelector('.video-card');
        if (mainContainer) {
            this.observer.observe(mainContainer, {
                childList: true,
                subtree: true
            });
        }
    }

    /**
     * Disconnect the observer
     * @memberof DynamicContentObserver
     */
    disconnect() {
        if (this.observer) {
            this.observer.disconnect();
        }
    }
}

/**
 * Main controller for watched video toggle functionality
 * @class WatchedVideoToggleController
 */
class WatchedVideoToggleController {
    /**
     * Create a watched video toggle controller
     * @memberof WatchedVideoToggleController
     */
    constructor() {
        /** @private {HTMLElement} Toggle input element */
        this.toggleElement = null;
        /** @private {WatchedVideoVisibilityManager} Visibility manager instance */
        this.visibilityManager = new WatchedVideoVisibilityManager();
        /** @private {DynamicContentObserver} Dynamic content observer instance */
        this.contentObserver = null;
    }

    /**
     * Initialize the toggle functionality
     * @memberof WatchedVideoToggleController
     */
    initialize() {
        this.toggleElement = document.getElementById('watchedToggle');
        
        if (!this.toggleElement) {
            console.warn('Watched toggle element not found');
            return;
        }

        this.setupEventListeners();
        this.loadSavedState();
        this.initializeDynamicContentObserver();
        this.applyInitialVisibility();
    }

    /**
     * Set up event listeners for the toggle
     * @private
     * @memberof WatchedVideoToggleController
     */
    setupEventListeners() {
        this.toggleElement.addEventListener('change', () => {
            this.handleToggleChange();
        });
    }

    /**
     * Handle toggle state changes
     * @private
     * @memberof WatchedVideoToggleController
     */
    handleToggleChange() {
        const isChecked = this.toggleElement.checked;
        
        this.saveToggleState(isChecked);
        this.applyToggleState(isChecked);
        this.dispatchToggleEvent(isChecked);
    }

    /**
     * Apply toggle state to DOM and visibility
     * @param {boolean} isChecked - Whether toggle is checked
     * @private
     * @memberof WatchedVideoToggleController
     */
    applyToggleState(isChecked) {
        if (isChecked) {
            document.body.classList.add(WatchedToggleConfig.BODY_CLASS);
            this.visibilityManager.applyWatchedVisibility(true);
        } else {
            document.body.classList.remove(WatchedToggleConfig.BODY_CLASS);
            this.visibilityManager.applyWatchedVisibility(false);
        }
    }

    /**
     * Save toggle state to localStorage
     * @param {boolean} isChecked - Whether toggle is checked
     * @private
     * @memberof WatchedVideoToggleController
     */
    saveToggleState(isChecked) {
        localStorage.setItem(WatchedToggleConfig.STORAGE_KEY, isChecked.toString());
    }

    /**
     * Load saved toggle state from localStorage
     * @private
     * @memberof WatchedVideoToggleController
     */
    loadSavedState() {
        const savedState = localStorage.getItem(WatchedToggleConfig.STORAGE_KEY);
        if (savedState === 'true') {
            this.toggleElement.checked = true;
            this.applyToggleState(true);
        }
    }

    /**
     * Initialize dynamic content observer
     * @private
     * @memberof WatchedVideoToggleController
     */
    initializeDynamicContentObserver() {
        this.contentObserver = new DynamicContentObserver(() => {
            if (this.toggleElement.checked) {
                this.visibilityManager.applyWatchedVisibility(true);
            }
        });
        this.contentObserver.initialize();
    }

    /**
     * Apply initial visibility to existing content
     * @private
     * @memberof WatchedVideoToggleController
     */
    applyInitialVisibility() {
        setTimeout(() => {
            if (this.toggleElement.checked) {
                this.visibilityManager.applyWatchedVisibility(true);
            }
        }, WatchedToggleConfig.INITIAL_LOAD_DELAY);
    }

    /**
     * Dispatch custom event for toggle changes
     * @param {boolean} isChecked - Whether toggle is checked
     * @private
     * @memberof WatchedVideoToggleController
     */
    dispatchToggleEvent(isChecked) {
        const toggleEvent = new CustomEvent('watchedToggleChanged', {
            detail: { hideWatched: isChecked }
        });
        document.dispatchEvent(toggleEvent);
    }
}

// Global instance
let watchedToggleController;

/**
 * Initialize watched video toggle functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    watchedToggleController = new WatchedVideoToggleController();
    watchedToggleController.initialize();
});
