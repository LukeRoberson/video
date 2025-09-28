/**
 * @fileoverview Handles horizontal scrolling and dynamic visibility of navigation arrows
 * for horizontally scrollable thumbnail carousels in the video manager web app.
 * 
 * Features:
 * - Dynamically shows/hides left and right arrows based on scroll position
 * - Allows horizontal scrolling using mouse wheel or arrow buttons
 * - Smooth scrolling behavior for better user experience
 * 
 * Usage:
 * - Include this script on pages with `.thumbnails-wrapper` elements
 * - Ensure each `.thumbnails-wrapper` has a unique `id` and contains:
 *   - `.thumbnails` (scrollable container for thumbnails)
 *   - `.scroll-arrow.left` (left arrow button)
 *   - `.scroll-arrow.right` (right arrow button)
 * 
 * Dependencies: None (Vanilla JavaScript)
 */

/**
 * Configuration constants for scroll functionality
 * @readonly
 * @enum {number}
 */
const ScrollConfig = {
    /** Mouse wheel scroll speed multiplier */
    WHEEL_SPEED_FACTOR: 2,
    /** Delay for arrow visibility calculation after DOM load */
    ARROW_UPDATE_DELAY: 100,
    /** Scroll direction: left */
    DIRECTION_LEFT: -1,
    /** Scroll direction: right */
    DIRECTION_RIGHT: 1
};

/**
 * Manages scroll functionality for a single thumbnail container
 * @class ThumbnailScrollManager
 */
class ThumbnailScrollManager {
    /**
     * Create a ThumbnailScrollManager instance
     * @param {HTMLElement} wrapperElement - The thumbnail wrapper element
     * @memberof ThumbnailScrollManager
     */
    constructor(wrapperElement) {
        /**
         * The wrapper element containing thumbnails and arrows
         * @type {HTMLElement}
         */
        this.wrapper = wrapperElement;
        
        /**
         * The scrollable thumbnails container
         * @type {HTMLElement}
         */
        this.thumbnails = wrapperElement.querySelector('.thumbnails');
        
        /**
         * Left scroll arrow element
         * @type {HTMLElement}
         */
        this.leftArrow = wrapperElement.querySelector('.carousel-scroll-arrow--left');
        
        /**
         * Right scroll arrow element
         * @type {HTMLElement}
         */
        this.rightArrow = wrapperElement.querySelector('.carousel-scroll-arrow--right');
        
        /**
         * Wrapper element ID
         * @type {string}
         */
        this.wrapperId = wrapperElement.id;

        this.init();
    }

    /**
     * Initialize the scroll manager
     * @memberof ThumbnailScrollManager
     */
    init() {
        if (!this.validateElements()) {
            return;
        }

        this.setupEventListeners();
        this.setupMouseWheelScrolling();
        
        // Initial arrow visibility update with delay
        setTimeout(() => this.updateArrows(), ScrollConfig.ARROW_UPDATE_DELAY);
    }

    /**
     * Validate that required elements exist
     * @returns {boolean} True if all required elements exist
     * @private
     * @memberof ThumbnailScrollManager
     */
    validateElements() {
        if (!this.thumbnails) {
            console.warn(`Thumbnails container not found in wrapper ${this.wrapperId}`);
            return false;
        }

        return true;
    }

    /**
     * Set up scroll and resize event listeners
     * @private
     * @memberof ThumbnailScrollManager
     */
    setupEventListeners() {
        this.thumbnails.addEventListener('scroll', () => this.updateArrows());
        window.addEventListener('resize', () => this.updateArrows());
    }

    /**
     * Set up mouse wheel scrolling functionality
     * @private
     * @memberof ThumbnailScrollManager
     */
    setupMouseWheelScrolling() {
        this.thumbnails.addEventListener('wheel', (event) => {
            event.preventDefault();
            
            const scrollAmount = event.deltaY * ScrollConfig.WHEEL_SPEED_FACTOR;
            this.thumbnails.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
        });
    }

    /**
     * Scroll thumbnails horizontally by one page width
     * @param {number} direction - Direction to scroll (-1 for left, 1 for right)
     * @memberof ThumbnailScrollManager
     */
    scrollThumbnails(direction) {
        const scrollAmount = this.thumbnails.clientWidth;
        this.thumbnails.scrollBy({
            left: direction * scrollAmount,
            behavior: 'smooth'
        });
    }

    /**
     * Update visibility of scroll arrows based on current scroll position
     * @memberof ThumbnailScrollManager
     */
    updateArrows() {
        // Re-query arrows each time in case they were created dynamically
        this.leftArrow = this.wrapper.querySelector('.carousel-scroll-arrow--left');
        this.rightArrow = this.wrapper.querySelector('.carousel-scroll-arrow--right');
        
        // If arrows don't exist, skip updating them
        if (!this.leftArrow || !this.rightArrow) {
            console.log(`Scroll arrows not yet available for wrapper ${this.wrapperId}`);
            return;
        }

        const canScrollLeft = this.thumbnails.scrollLeft > 0;
        const canScrollRight = (this.thumbnails.scrollLeft + this.thumbnails.clientWidth) < this.thumbnails.scrollWidth;
        
        this.leftArrow.style.display = canScrollLeft ? 'flex' : 'none';
        this.rightArrow.style.display = canScrollRight ? 'flex' : 'none';
    }

    /**
     * Scroll to the left by one page width
     * @memberof ThumbnailScrollManager
     */
    scrollLeft() {
        this.scrollThumbnails(ScrollConfig.DIRECTION_LEFT);
    }

    /**
     * Scroll to the right by one page width
     * @memberof ThumbnailScrollManager
     */
    scrollRight() {
        this.scrollThumbnails(ScrollConfig.DIRECTION_RIGHT);
    }

    /**
     * Get current scroll position as percentage
     * @returns {number} Scroll position percentage (0-100)
     * @memberof ThumbnailScrollManager
     */
    getScrollPercentage() {
        const maxScroll = this.thumbnails.scrollWidth - this.thumbnails.clientWidth;
        if (maxScroll <= 0) return 0;
        
        return (this.thumbnails.scrollLeft / maxScroll) * 100;
    }

    /**
     * Check if container can scroll in either direction
     * @returns {boolean} True if scrollable
     * @memberof ThumbnailScrollManager
     */
    isScrollable() {
        return this.thumbnails.scrollWidth > this.thumbnails.clientWidth;
    }

    /**
     * Destroy the scroll manager and clean up event listeners
     * @memberof ThumbnailScrollManager
     */
    destroy() {
        this.thumbnails.removeEventListener('scroll', this.updateArrows);
        window.removeEventListener('resize', this.updateArrows);
        this.thumbnails.removeEventListener('wheel', this.setupMouseWheelScrolling);
    }
}

/**
 * Global manager for all thumbnail scroll functionality
 * @class GlobalScrollManager
 */
class GlobalScrollManager {
    /**
     * Create a GlobalScrollManager instance
     * @memberof GlobalScrollManager
     */
    constructor() {
        /**
         * Map of wrapper IDs to their scroll managers
         * @type {Map<string, ThumbnailScrollManager>}
         */
        this.scrollManagers = new Map();
    }

    /**
     * Initialize scroll managers for all thumbnail wrappers
     * @memberof GlobalScrollManager
     */
    init() {
        this.setupScrollManagers();
        this.exposeGlobalFunctions();
    }

    /**
     * Set up scroll managers for all thumbnail wrappers on the page
     * @private
     * @memberof GlobalScrollManager
     */
    setupScrollManagers() {
        const wrappers = document.querySelectorAll('.thumbnail-wrapper');
        
        wrappers.forEach(wrapper => {
            if (!wrapper.id) {
                console.warn('Thumbnail wrapper found without ID, skipping');
                return;
            }

            const manager = new ThumbnailScrollManager(wrapper);
            this.scrollManagers.set(wrapper.id, manager);
        });
    }

    /**
     * Expose global functions for backward compatibility
     * @private
     * @memberof GlobalScrollManager
     */
    exposeGlobalFunctions() {
        /**
         * Global function to scroll thumbnails (for backward compatibility)
         * @global
         * @param {string} wrapperId - The ID of the thumbnails wrapper
         * @param {number} direction - Direction to scroll (-1 for left, 1 for right)
         */
        window.scrollThumbnails = (wrapperId, direction) => {
            const manager = this.scrollManagers.get(wrapperId);
            if (manager) {
                manager.scrollThumbnails(direction);
            } else {
                console.warn(`No scroll manager found for wrapper ${wrapperId}`);
            }
        };

        /**
         * Global function to update arrows (for backward compatibility)
         * @global
         * @param {string} wrapperId - The ID of the thumbnails wrapper
         */
        window.updateArrows = (wrapperId) => {
            const manager = this.scrollManagers.get(wrapperId);
            if (manager) {
                manager.updateArrows();
            } else {
                console.warn(`No scroll manager found for wrapper ${wrapperId}`);
            }
        };
    }

    /**
     * Get scroll manager for a specific wrapper
     * @param {string} wrapperId - The wrapper ID
     * @returns {ThumbnailScrollManager|null} The scroll manager or null if not found
     * @memberof GlobalScrollManager
     */
    getScrollManager(wrapperId) {
        return this.scrollManagers.get(wrapperId) || null;
    }

    /**
     * Add a new scroll manager for a dynamically created wrapper
     * @param {HTMLElement} wrapperElement - The new wrapper element
     * @returns {ThumbnailScrollManager} The created scroll manager
     * @memberof GlobalScrollManager
     */
    addScrollManager(wrapperElement) {
        if (!wrapperElement.id) {
            throw new Error('Wrapper element must have an ID');
        }

        const manager = new ThumbnailScrollManager(wrapperElement);
        this.scrollManagers.set(wrapperElement.id, manager);
        
        return manager;
    }

    /**
     * Remove a scroll manager
     * @param {string} wrapperId - The wrapper ID to remove
     * @memberof GlobalScrollManager
     */
    removeScrollManager(wrapperId) {
        const manager = this.scrollManagers.get(wrapperId);
        if (manager) {
            manager.destroy();
            this.scrollManagers.delete(wrapperId);
        }
    }

    /**
     * Get all scroll managers
     * @returns {Array<ThumbnailScrollManager>} Array of all scroll managers
     * @memberof GlobalScrollManager
     */
    getAllScrollManagers() {
        return Array.from(this.scrollManagers.values());
    }

    /**
     * Destroy all scroll managers and clean up
     * @memberof GlobalScrollManager
     */
    destroy() {
        this.scrollManagers.forEach(manager => manager.destroy());
        this.scrollManagers.clear();
        
        // Clean up global functions
        delete window.scrollThumbnails;
        delete window.updateArrows;
    }
}

// Global instance
let globalScrollManager;

/**
 * Initialize scroll functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    globalScrollManager = new GlobalScrollManager();
    globalScrollManager.init();
});