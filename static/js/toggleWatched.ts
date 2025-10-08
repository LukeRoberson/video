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
} as const;

/**
 * Handles visibility toggling of watched video elements
 */
class WatchedVideoVisibilityManager {
    /** CSS selectors for watched video elements */
    private watchedSelectors: readonly string[];

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
    applyWatchedVisibility(hideWatched: boolean): void {
        this.watchedSelectors.forEach((selector: string) => {
            const elements = document.querySelectorAll(selector);
            elements.forEach((element: Element) => {
                const htmlElement = element as HTMLElement;
                if (hideWatched) {
                    htmlElement.style.display = 'none';
                    htmlElement.setAttribute('data-hidden-by-toggle', 'true');
                } else {
                    htmlElement.style.display = '';
                    htmlElement.removeAttribute('data-hidden-by-toggle');
                }
            });
        });
    }
}

/**
 * Callback type for when video elements are added
 */
type VideoElementsAddedCallback = () => void;

/**
 * Handles observation of dynamically added video content
 */
class DynamicContentObserver {
    /** Callback for when video elements are added */
    private onVideoElementsAdded: VideoElementsAddedCallback;
    
    /** DOM mutation observer */
    private observer: MutationObserver | null;

    /**
     * Create a dynamic content observer
     * @param onVideoElementsAdded - Callback when video elements are added
     */
    constructor(onVideoElementsAdded: VideoElementsAddedCallback) {
        this.onVideoElementsAdded = onVideoElementsAdded;
        this.observer = null;
    }

    /**
     * Initialize observation of dynamic content
     */
    initialize(): void {
        this.observer = new MutationObserver((mutations: MutationRecord[]) => {
            let shouldApplyVisibility = false;
            
            mutations.forEach((mutation: MutationRecord) => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    const addedVideoElements = Array.from(mutation.addedNodes).some((node: Node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            const element = node as Element;
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
    private observeContainers(): void {
        if (!this.observer) return;

        const thumbnailContainers = document.querySelectorAll('.thumbnails');
        thumbnailContainers.forEach((container: Element) => {
            this.observer!.observe(container, {
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
    disconnect(): void {
        if (this.observer) {
            this.observer.disconnect();
        }
    }
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
class WatchedVideoToggleController {
    /** Toggle input element */
    private toggleElement: HTMLInputElement | null;
    
    /** Visibility manager instance */
    private visibilityManager: WatchedVideoVisibilityManager;
    
    /** Dynamic content observer instance */
    private contentObserver: DynamicContentObserver | null;

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
    initialize(): void {
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
    private setupEventListeners(): void {
        if (!this.toggleElement) return;

        this.toggleElement.addEventListener('change', () => {
            this.handleToggleChange();
        });
    }

    /**
     * Handle toggle state changes
     */
    private handleToggleChange(): void {
        if (!this.toggleElement) return;

        const isChecked = this.toggleElement.checked;
        
        this.saveToggleState(isChecked);
        this.applyToggleState(isChecked);
        this.dispatchToggleEvent(isChecked);
    }

    /**
     * Apply toggle state to DOM and visibility
     * @param isChecked - Whether toggle is checked
     */
    private applyToggleState(isChecked: boolean): void {
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
     * @param isChecked - Whether toggle is checked
     */
    private saveToggleState(isChecked: boolean): void {
        localStorage.setItem(WatchedToggleConfig.STORAGE_KEY, isChecked.toString());
    }

    /**
     * Load saved toggle state from localStorage
     */
    private loadSavedState(): void {
        if (!this.toggleElement) return;

        const savedState = localStorage.getItem(WatchedToggleConfig.STORAGE_KEY);
        if (savedState === 'true') {
            this.toggleElement.checked = true;
            this.applyToggleState(true);
        }
    }

    /**
     * Initialize dynamic content observer
     */
    private initializeDynamicContentObserver(): void {
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
    private applyInitialVisibility(): void {
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
    private dispatchToggleEvent(isChecked: boolean): void {
        const toggleEvent = new CustomEvent<WatchedToggleEventDetail>('watchedToggleChanged', {
            detail: { hideWatched: isChecked }
        });
        document.dispatchEvent(toggleEvent);
    }

    /**
     * Get current toggle state
     * @returns Current toggle state
     */
    getToggleState(): boolean {
        return this.toggleElement?.checked || false;
    }

    /**
     * Set toggle state programmatically
     * @param state - New toggle state
     */
    setToggleState(state: boolean): void {
        if (!this.toggleElement) return;

        this.toggleElement.checked = state;
        this.handleToggleChange();
    }

    /**
     * Cleanup and destroy the controller
     */
    destroy(): void {
        if (this.contentObserver) {
            this.contentObserver.disconnect();
        }
    }
}

// Global instance
let watchedToggleController: WatchedVideoToggleController | undefined;

/**
 * Initialize watched video toggle functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    watchedToggleController = new WatchedVideoToggleController();
    watchedToggleController.initialize();
});
