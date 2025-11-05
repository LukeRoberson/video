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
declare const ScrollConfig: {
    /** Mouse wheel scroll speed multiplier */
    readonly WHEEL_SPEED_FACTOR: 2;
    /** Delay for arrow visibility calculation after DOM load */
    readonly ARROW_UPDATE_DELAY: 100;
    /** Scroll direction: left */
    readonly DIRECTION_LEFT: -1;
    /** Scroll direction: right */
    readonly DIRECTION_RIGHT: 1;
};
/**
 * Manages scroll functionality for a single thumbnail container
 */
declare class ThumbnailScrollManager {
    /** The wrapper element containing thumbnails and arrows */
    private wrapper;
    /** The scrollable thumbnails container */
    private thumbnails;
    /** Left scroll arrow element */
    private leftArrow;
    /** Right scroll arrow element */
    private rightArrow;
    /** Wrapper element ID */
    private wrapperId;
    /** Bound update arrows method for event listeners */
    private boundUpdateArrows;
    /**
     * Create a ThumbnailScrollManager instance
     * @param wrapperElement - The thumbnail wrapper element
     */
    constructor(wrapperElement: HTMLElement);
    /**
     * Initialize the scroll manager
     */
    private init;
    /**
     * Validate that required elements exist
     * @returns True if all required elements exist
     */
    private validateElements;
    /**
     * Set up scroll and resize event listeners
     */
    private setupEventListeners;
    /**
     * Set up mouse wheel scrolling functionality
     */
    private setupMouseWheelScrolling;
    /**
     * Scroll thumbnails horizontally by one page width
     * @param direction - Direction to scroll (-1 for left, 1 for right)
     */
    scrollThumbnails(direction: number): void;
    /**
     * Update visibility of scroll arrows based on current scroll position
     */
    updateArrows(): void;
    /**
     * Scroll to the left by one page width
     */
    scrollLeft(): void;
    /**
     * Scroll to the right by one page width
     */
    scrollRight(): void;
    /**
     * Get current scroll position as percentage
     * @returns Scroll position percentage (0-100)
     */
    getScrollPercentage(): number;
    /**
     * Check if container can scroll in either direction
     * @returns True if scrollable
     */
    isScrollable(): boolean;
    /**
     * Destroy the scroll manager and clean up event listeners
     */
    destroy(): void;
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
declare class GlobalScrollManager {
    /** Map of wrapper IDs to their scroll managers */
    private scrollManagers;
    /**
     * Create a GlobalScrollManager instance
     */
    constructor();
    /**
     * Initialize scroll managers for all thumbnail wrappers
     */
    init(): void;
    /**
     * Set up scroll managers for all thumbnail wrappers on the page
     */
    private setupScrollManagers;
    /**
     * Expose global functions for backward compatibility
     */
    private exposeGlobalFunctions;
    /**
     * Get scroll manager for a specific wrapper
     * @param wrapperId - The wrapper ID
     * @returns The scroll manager or null if not found
     */
    getScrollManager(wrapperId: string): ThumbnailScrollManager | null;
    /**
     * Add a new scroll manager for a dynamically created wrapper
     * @param wrapperElement - The new wrapper element
     * @returns The created scroll manager
     */
    addScrollManager(wrapperElement: HTMLElement): ThumbnailScrollManager;
    /**
     * Remove a scroll manager
     * @param wrapperId - The wrapper ID to remove
     */
    removeScrollManager(wrapperId: string): void;
    /**
     * Get all scroll managers
     * @returns Array of all scroll managers
     */
    getAllScrollManagers(): ThumbnailScrollManager[];
    /**
     * Destroy all scroll managers and clean up
     */
    destroy(): void;
}
declare let globalScrollManager: GlobalScrollManager | undefined;
//# sourceMappingURL=scroll.d.ts.map