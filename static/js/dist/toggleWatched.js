"use strict";
/**
 * @fileoverview Watched videos toggle functionality for video manager.
 * Handles hiding and showing watched videos with localStorage persistence and dynamic content support.
 * Integrates with dynamically loaded video content.
 */
/**
 * Configuration constants for watched video toggle
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
 */
class WatchedVideoVisibilityManager {
    /**
     * Create a watched video visibility manager
     */
    constructor() {
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
     * @param hideWatched - Whether to hide watched videos
     */
    applyWatchedVisibility(hideWatched) {
        this.watchedSelectors.forEach((selector) => {
            const elements = document.querySelectorAll(selector);
            elements.forEach((element) => {
                const htmlElement = element;
                if (hideWatched) {
                    htmlElement.style.display = 'none';
                    htmlElement.setAttribute('data-hidden-by-toggle', 'true');
                }
                else {
                    htmlElement.style.display = '';
                    htmlElement.removeAttribute('data-hidden-by-toggle');
                }
            });
        });
    }
}
/**
 * Handles observation of dynamically added video content
 */
class DynamicContentObserver {
    /**
     * Create a dynamic content observer
     * @param onVideoElementsAdded - Callback when video elements are added
     */
    constructor(onVideoElementsAdded) {
        this.onVideoElementsAdded = onVideoElementsAdded;
        this.observer = null;
    }
    /**
     * Initialize observation of dynamic content
     */
    initialize() {
        this.observer = new MutationObserver((mutations) => {
            let shouldApplyVisibility = false;
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    const addedVideoElements = Array.from(mutation.addedNodes).some((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            const element = node;
                            return element.matches('.video-item, .video-card, .thumbnail, .video-thumbnail') ||
                                element.querySelector('.video-item, .video-card, .thumbnail, .video-thumbnail') !== null;
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
     */
    observeContainers() {
        if (!this.observer)
            return;
        const thumbnailContainers = document.querySelectorAll('.thumbnails');
        thumbnailContainers.forEach((container) => {
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
     */
    disconnect() {
        if (this.observer) {
            this.observer.disconnect();
        }
    }
}
/**
 * Main controller for watched video toggle functionality
 */
class WatchedVideoToggleController {
    /**
     * Create a watched video toggle controller
     */
    constructor() {
        this.toggleElement = null;
        this.visibilityManager = new WatchedVideoVisibilityManager();
        this.contentObserver = null;
    }
    /**
     * Initialize the toggle functionality
     */
    initialize() {
        const element = document.getElementById('watchedToggle');
        if (!element || !(element instanceof HTMLInputElement)) {
            console.warn('Watched toggle element not found');
            return;
        }
        this.toggleElement = element;
        this.setupEventListeners();
        this.loadSavedState();
        this.initializeDynamicContentObserver();
        this.applyInitialVisibility();
    }
    /**
     * Set up event listeners for the toggle
     */
    setupEventListeners() {
        if (!this.toggleElement)
            return;
        this.toggleElement.addEventListener('change', () => {
            this.handleToggleChange();
        });
    }
    /**
     * Handle toggle state changes
     */
    handleToggleChange() {
        if (!this.toggleElement)
            return;
        const isChecked = this.toggleElement.checked;
        this.saveToggleState(isChecked);
        this.applyToggleState(isChecked);
        this.dispatchToggleEvent(isChecked);
    }
    /**
     * Apply toggle state to DOM and visibility
     * @param isChecked - Whether toggle is checked
     */
    applyToggleState(isChecked) {
        if (isChecked) {
            document.body.classList.add(WatchedToggleConfig.BODY_CLASS);
            this.visibilityManager.applyWatchedVisibility(true);
        }
        else {
            document.body.classList.remove(WatchedToggleConfig.BODY_CLASS);
            this.visibilityManager.applyWatchedVisibility(false);
        }
    }
    /**
     * Save toggle state to localStorage
     * @param isChecked - Whether toggle is checked
     */
    saveToggleState(isChecked) {
        localStorage.setItem(WatchedToggleConfig.STORAGE_KEY, isChecked.toString());
    }
    /**
     * Load saved toggle state from localStorage
     */
    loadSavedState() {
        if (!this.toggleElement)
            return;
        const savedState = localStorage.getItem(WatchedToggleConfig.STORAGE_KEY);
        if (savedState === 'true') {
            this.toggleElement.checked = true;
            this.applyToggleState(true);
        }
    }
    /**
     * Initialize dynamic content observer
     */
    initializeDynamicContentObserver() {
        this.contentObserver = new DynamicContentObserver(() => {
            if (this.toggleElement?.checked) {
                this.visibilityManager.applyWatchedVisibility(true);
            }
        });
        this.contentObserver.initialize();
    }
    /**
     * Apply initial visibility to existing content
     */
    applyInitialVisibility() {
        setTimeout(() => {
            if (this.toggleElement?.checked) {
                this.visibilityManager.applyWatchedVisibility(true);
            }
        }, WatchedToggleConfig.INITIAL_LOAD_DELAY);
    }
    /**
     * Dispatch custom event for toggle changes
     * @param isChecked - Whether toggle is checked
     */
    dispatchToggleEvent(isChecked) {
        const toggleEvent = new CustomEvent('watchedToggleChanged', {
            detail: { hideWatched: isChecked }
        });
        document.dispatchEvent(toggleEvent);
    }
    /**
     * Get current toggle state
     * @returns Current toggle state
     */
    getToggleState() {
        return this.toggleElement?.checked || false;
    }
    /**
     * Set toggle state programmatically
     * @param state - New toggle state
     */
    setToggleState(state) {
        if (!this.toggleElement)
            return;
        this.toggleElement.checked = state;
        this.handleToggleChange();
    }
    /**
     * Cleanup and destroy the controller
     */
    destroy() {
        if (this.contentObserver) {
            this.contentObserver.disconnect();
        }
    }
}
// Global instance
let watchedToggleController;
/**
 * Initialize watched video toggle functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function () {
    watchedToggleController = new WatchedVideoToggleController();
    watchedToggleController.initialize();
});
//# sourceMappingURL=toggleWatched.js.map