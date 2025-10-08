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
} as const;

/**
 * Manages scroll functionality for a single thumbnail container
 */
class ThumbnailScrollManager {
    /** The wrapper element containing thumbnails and arrows */
    private wrapper: HTMLElement;
    
    /** The scrollable thumbnails container */
    private thumbnails: HTMLElement;
    
    /** Left scroll arrow element */
    private leftArrow: HTMLElement | null;
    
    /** Right scroll arrow element */
    private rightArrow: HTMLElement | null;
    
    /** Wrapper element ID */
    private wrapperId: string;
    
    /** Bound update arrows method for event listeners */
    private boundUpdateArrows: () => void;

    /**
     * Create a ThumbnailScrollManager instance
     * @param wrapperElement - The thumbnail wrapper element
     */
    constructor(wrapperElement: HTMLElement) {
        this.wrapper = wrapperElement;
        
        const thumbnailsElement = wrapperElement.querySelector('.thumbnails');
        if (!thumbnailsElement) {
            throw new Error('Thumbnails container not found');
        }
        this.thumbnails = thumbnailsElement as HTMLElement;
        
        this.leftArrow = wrapperElement.querySelector('.carousel-scroll-arrow--left');
        this.rightArrow = wrapperElement.querySelector('.carousel-scroll-arrow--right');
        this.wrapperId = wrapperElement.id || 'unknown';
        
        // Bind method for proper 'this' context in event listeners
        this.boundUpdateArrows = this.updateArrows.bind(this);

        this.init();
    }

    /**
     * Initialize the scroll manager
     */
    private init(): void {
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
     * @returns True if all required elements exist
     */
    private validateElements(): boolean {
        if (!this.thumbnails) {
            console.warn(`Thumbnails container not found in wrapper ${this.wrapperId}`);
            return false;
        }

        return true;
    }

    /**
     * Set up scroll and resize event listeners
     */
    private setupEventListeners(): void {
        this.thumbnails.addEventListener('scroll', this.boundUpdateArrows);
        window.addEventListener('resize', this.boundUpdateArrows);
    }

    /**
     * Set up mouse wheel scrolling functionality
     */
    private setupMouseWheelScrolling(): void {
        this.thumbnails.addEventListener('wheel', (event: WheelEvent) => {
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
     * @param direction - Direction to scroll (-1 for left, 1 for right)
     */
    scrollThumbnails(direction: number): void {
        const scrollAmount = this.thumbnails.clientWidth;
        this.thumbnails.scrollBy({
            left: direction * scrollAmount,
            behavior: 'smooth'
        });
    }

    /**
     * Update visibility of scroll arrows based on current scroll position
     */
    updateArrows(): void {
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
     */
    scrollLeft(): void {
        this.scrollThumbnails(ScrollConfig.DIRECTION_LEFT);
    }

    /**
     * Scroll to the right by one page width
     */
    scrollRight(): void {
        this.scrollThumbnails(ScrollConfig.DIRECTION_RIGHT);
    }

    /**
     * Get current scroll position as percentage
     * @returns Scroll position percentage (0-100)
     */
    getScrollPercentage(): number {
        const maxScroll = this.thumbnails.scrollWidth - this.thumbnails.clientWidth;
        if (maxScroll <= 0) return 0;
        
        return (this.thumbnails.scrollLeft / maxScroll) * 100;
    }

    /**
     * Check if container can scroll in either direction
     * @returns True if scrollable
     */
    isScrollable(): boolean {
        return this.thumbnails.scrollWidth > this.thumbnails.clientWidth;
    }

    /**
     * Destroy the scroll manager and clean up event listeners
     */
    destroy(): void {
        this.thumbnails.removeEventListener('scroll', this.boundUpdateArrows);
        window.removeEventListener('resize', this.boundUpdateArrows);
    }
}

/**
 * Global functions interface for backward compatibility
 */
interface WindowWithScrollFunctions extends Window {
    scrollThumbnails?: (wrapperId: string, direction: number) => void;
    updateArrows?: (wrapperId: string) => void;
}

/**
 * Global manager for all thumbnail scroll functionality
 */
class GlobalScrollManager {
    /** Map of wrapper IDs to their scroll managers */
    private scrollManagers: Map<string, ThumbnailScrollManager>;

    /**
     * Create a GlobalScrollManager instance
     */
    constructor() {
        this.scrollManagers = new Map<string, ThumbnailScrollManager>();
    }

    /**
     * Initialize scroll managers for all thumbnail wrappers
     */
    init(): void {
        this.setupScrollManagers();
        this.exposeGlobalFunctions();
    }

    /**
     * Set up scroll managers for all thumbnail wrappers on the page
     */
    private setupScrollManagers(): void {
        const wrappers = document.querySelectorAll('.thumbnail-wrapper');
        
        wrappers.forEach((wrapper: Element) => {
            const htmlWrapper = wrapper as HTMLElement;
            if (!htmlWrapper.id) {
                console.warn('Thumbnail wrapper found without ID, skipping');
                return;
            }

            const manager = new ThumbnailScrollManager(htmlWrapper);
            this.scrollManagers.set(htmlWrapper.id, manager);
        });
    }

    /**
     * Expose global functions for backward compatibility
     */
    private exposeGlobalFunctions(): void {
        const windowObj = window as WindowWithScrollFunctions;
        
        /**
         * Global function to scroll thumbnails (for backward compatibility)
         */
        windowObj.scrollThumbnails = (wrapperId: string, direction: number): void => {
            const manager = this.scrollManagers.get(wrapperId);
            if (manager) {
                manager.scrollThumbnails(direction);
            } else {
                console.warn(`No scroll manager found for wrapper ${wrapperId}`);
            }
        };

        /**
         * Global function to update arrows (for backward compatibility)
         */
        windowObj.updateArrows = (wrapperId: string): void => {
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
     * @param wrapperId - The wrapper ID
     * @returns The scroll manager or null if not found
     */
    getScrollManager(wrapperId: string): ThumbnailScrollManager | null {
        return this.scrollManagers.get(wrapperId) || null;
    }

    /**
     * Add a new scroll manager for a dynamically created wrapper
     * @param wrapperElement - The new wrapper element
     * @returns The created scroll manager
     */
    addScrollManager(wrapperElement: HTMLElement): ThumbnailScrollManager {
        if (!wrapperElement.id) {
            throw new Error('Wrapper element must have an ID');
        }

        const manager = new ThumbnailScrollManager(wrapperElement);
        this.scrollManagers.set(wrapperElement.id, manager);
        
        return manager;
    }

    /**
     * Remove a scroll manager
     * @param wrapperId - The wrapper ID to remove
     */
    removeScrollManager(wrapperId: string): void {
        const manager = this.scrollManagers.get(wrapperId);
        if (manager) {
            manager.destroy();
            this.scrollManagers.delete(wrapperId);
        }
    }

    /**
     * Get all scroll managers
     * @returns Array of all scroll managers
     */
    getAllScrollManagers(): ThumbnailScrollManager[] {
        return Array.from(this.scrollManagers.values());
    }

    /**
     * Destroy all scroll managers and clean up
     */
    destroy(): void {
        this.scrollManagers.forEach((manager: ThumbnailScrollManager) => manager.destroy());
        this.scrollManagers.clear();
        
        // Clean up global functions
        const windowObj = window as WindowWithScrollFunctions;
        delete windowObj.scrollThumbnails;
        delete windowObj.updateArrows;
    }
}

// Global instance
let globalScrollManager: GlobalScrollManager | undefined;

/**
 * Initialize scroll functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    globalScrollManager = new GlobalScrollManager();
    globalScrollManager.init();
});
