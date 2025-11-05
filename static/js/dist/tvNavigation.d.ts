/**
 * @fileoverview TV Remote Navigation Enhancement
 * Provides native app-like navigation using arrow keys/remote control for Smart TVs.
 * Supports Samsung Tizen, Fire TV, LG WebOS, and other TV platforms.
 */
/**
 * Configuration constants for TV navigation
 */
declare const TVNavigationConfig: {
    /** Delay before starting TV navigation */
    readonly STARTUP_DELAY: 1000;
    /** Delay for slide navigation */
    readonly SLIDE_NAVIGATION_DELAY: 300;
    /** Element update debounce delay */
    readonly UPDATE_DEBOUNCE_DELAY: 100;
    /** Debug mode keyboard shortcut delay */
    readonly DEBUG_DELAY: 500;
    /** Vertical threshold for same row detection */
    readonly SAME_ROW_THRESHOLD: 50;
    /** Small horizontal movement threshold */
    readonly SMALL_HORIZONTAL_THRESHOLD: 10;
    /** Vertical element spacing threshold */
    readonly VERTICAL_SPACING_THRESHOLD: 30;
};
/**
 * TV remote control key mappings for different platforms
 */
declare const TVKeyMappings: {
    /** Standard keyboard codes */
    readonly STANDARD: {
        readonly 37: "ArrowLeft";
        readonly 38: "ArrowUp";
        readonly 39: "ArrowRight";
        readonly 40: "ArrowDown";
        readonly 13: "Enter";
        readonly 27: "Escape";
        readonly 32: " ";
    };
    /** Samsung TV (Tizen) remote codes */
    readonly SAMSUNG: {
        readonly 4: "Escape";
        readonly 10009: "Escape";
        readonly 10252: " ";
        readonly 415: " ";
        readonly 10182: "Enter";
    };
    /** Fire TV / Amazon remote codes */
    readonly FIRE_TV: {
        readonly 21: "ArrowLeft";
        readonly 19: "ArrowUp";
        readonly 22: "ArrowRight";
        readonly 20: "ArrowDown";
        readonly 23: "Enter";
    };
    /** WebOS (LG TV) remote codes */
    readonly WEBOS: {
        readonly 461: "Escape";
        readonly 13: "Enter";
    };
    /** Additional TV remote codes */
    readonly ADDITIONAL: {
        readonly 166: "Escape";
        readonly 8: "Escape";
    };
};
/**
 * Navigation direction types
 */
type NavigationDirection = 'up' | 'down' | 'left' | 'right';
/**
 * Element section types
 */
type ElementSection = 'navbar' | 'profile' | 'carousel' | 'news' | 'program' | 'content' | 'other';
/**
 * Navigation result interface
 */
interface NavigationResult {
    isValid: boolean;
    distance: number;
}
/**
 * Bootstrap carousel instance type
 */
interface BootstrapCarousel {
    next(): void;
    prev(): void;
}
/**
 * Debug interface for TV navigation
 */
interface DebugTVNavigation {
    start(): void;
    stop(): void;
    showElements(): void;
    focusElement(index: number): void;
}
/**
 * Handles TV device detection and status management
 */
declare class TVDetectionManager {
    /**
     * Current TV detection status
     */
    private isTV;
    /**
     * Update TV detection status using multiple detection methods
     * @returns True if device is detected as TV
     */
    updateTVStatus(): boolean;
    /**
     * Perform enhanced TV detection based on user agent
     * @returns True if TV is detected
     */
    private performEnhancedDetection;
    /**
     * Get current TV status
     * @returns Current TV detection status
     */
    getTVStatus(): boolean;
}
/**
 * Handles remote control key input and normalization
 */
declare class TVKeyHandler {
    /**
     * Normalize key input from various TV remote controls
     * @param event - Keyboard event from remote
     * @returns Normalized key name or null if not recognized
     */
    normalizeKey(event: KeyboardEvent): string | null;
}
/**
 * Manages focusable elements and their organization
 */
declare class FocusableElementManager {
    /**
     * Array of currently focusable elements
     */
    private focusableElements;
    /**
     * Update the list of focusable elements on the page
     */
    updateFocusableElements(): void;
    /**
     * Check if an element is actually focusable
     * @param element - Element to check
     * @returns True if element is focusable
     */
    private isElementFocusable;
    /**
     * Check if thumbnail element is valid (not nested)
     * @param element - Thumbnail element to check
     * @returns True if valid thumbnail
     */
    private isValidThumbnailElement;
    /**
     * Sort elements by position with section awareness
     */
    private sortElementsByPosition;
    /**
     * Get section priority for sorting
     * @param element - Element to get priority for
     * @returns Priority number (lower = higher priority)
     */
    private getSectionPriority;
    /**
     * Prepare elements for TV navigation
     */
    private prepareElementsForNavigation;
    /**
     * Get all focusable elements
     * @returns Array of focusable elements
     */
    getFocusableElements(): HTMLElement[];
    /**
     * Get element by index
     * @param index - Element index
     * @returns Element at index or null
     */
    getElementByIndex(index: number): HTMLElement | null;
    /**
     * Get element index
     * @param element - Element to find index for
     * @returns Element index or -1 if not found
     */
    getElementIndex(element: HTMLElement): number;
}
/**
 * Manages focus state and visual indicators
 */
declare class FocusManager {
    /**
     * Element manager reference
     */
    private readonly elementManager;
    /**
     * Current focus index
     */
    private currentFocusIndex;
    /**
     * Create a FocusManager instance
     * @param elementManager - Element manager instance
     */
    constructor(elementManager: FocusableElementManager);
    /**
     * Set focus on a specific element by index
     * @param index - Index of element to focus
     */
    setFocus(index: number): void;
    /**
     * Clear focus from all elements
     * @param elements - Elements to clear focus from
     */
    private clearAllFocus;
    /**
     * Apply focus styles to element
     * @param element - Element to apply styles to
     */
    private applyFocusStyles;
    /**
     * Scroll element into view
     * @param element - Element to scroll into view
     */
    private scrollIntoView;
    /**
     * Get current focus index
     * @returns Current focus index
     */
    getCurrentFocusIndex(): number;
    /**
     * Get currently focused element
     * @returns Currently focused element
     */
    getCurrentElement(): HTMLElement | null;
}
/**
 * Handles directional navigation logic
 */
declare class DirectionalNavigator {
    /**
     * Element manager reference
     */
    private readonly elementManager;
    /**
     * Focus manager reference
     */
    private readonly focusManager;
    /**
     * Create a DirectionalNavigator instance
     * @param elementManager - Element manager instance
     * @param focusManager - Focus manager instance
     */
    constructor(elementManager: FocusableElementManager, focusManager: FocusManager);
    /**
     * Find the next focusable element in a direction
     * @param direction - Direction to navigate
     * @returns Index of next element or -1 if not found
     */
    findNextInDirection(direction: NavigationDirection): number;
    /**
     * Get element section identifier
     * @param element - Element to get section for
     * @returns Section identifier
     */
    getElementSection(element: HTMLElement): ElementSection;
    /**
     * Calculate navigation distance and validity for direction
     * @param direction - Navigation direction
     * @param currentY - Current element Y position
     * @param currentX - Current element X position
     * @param elY - Target element Y position
     * @param elX - Target element X position
     * @param currentSection - Current element section
     * @param elSection - Target element section
     * @param currentCarousel - Current carousel element
     * @param elCarousel - Target carousel element
     * @param el - Target element
     * @returns Navigation result with isValid and distance properties
     */
    private calculateNavigationDistance;
    /**
     * Apply preferences for downward navigation
     * @param distance - Base distance
     * @param currentSection - Current section
     * @param elSection - Target section
     * @param currentCarousel - Current carousel
     * @param elCarousel - Target carousel
     * @returns Modified distance
     */
    private applyDownNavigationPreferences;
    /**
     * Apply preferences for upward navigation
     * @param distance - Base distance
     * @param currentSection - Current section
     * @param elSection - Target section
     * @param currentCarousel - Current carousel
     * @param elCarousel - Target carousel
     * @param el - Target element
     * @returns Modified distance
     */
    private applyUpNavigationPreferences;
    /**
     * Calculate horizontal navigation result
     * @param direction - 'left' or 'right'
     * @param currentX - Current X position
     * @param elX - Target X position
     * @param currentY - Current Y position
     * @param elY - Target Y position
     * @param currentSection - Current section
     * @param elSection - Target section
     * @param currentCarousel - Current carousel
     * @param elCarousel - Target carousel
     * @returns Result with isValid and distance properties
     */
    private calculateHorizontalNavigation;
}
/**
 * Handles carousel-specific navigation logic
 */
declare class CarouselNavigator {
    /**
     * Element manager reference
     */
    private readonly elementManager;
    /**
     * Focus manager reference
     */
    private readonly focusManager;
    /**
     * Create a CarouselNavigator instance
     * @param elementManager - Element manager instance
     * @param focusManager - Focus manager instance
     */
    constructor(elementManager: FocusableElementManager, focusManager: FocusManager);
    /**
     * Navigate to next/previous carousel slide when reaching the edge
     * @param direction - 'right' or 'left'
     * @returns True if slide navigation occurred
     */
    navigateCarouselSlide(direction: 'left' | 'right'): boolean;
    /**
     * Handle slide navigation logic
     * @param direction - Navigation direction
     * @param currentIndex - Current thumbnail index
     * @param visibleThumbnails - Visible thumbnails in current slide
     * @param carouselInstance - Bootstrap carousel instance
     * @param currentCarousel - Current carousel element
     * @returns True if navigation occurred
     */
    private handleSlideNavigation;
    /**
     * Move to next carousel slide
     * @param activeIndex - Current active slide index
     * @param totalSlides - Total number of slides
     * @param carouselInstance - Bootstrap carousel instance
     * @param currentCarousel - Current carousel element
     * @returns True if moved to next slide
     */
    private moveToNextSlide;
    /**
     * Move to previous carousel slide
     * @param activeIndex - Current active slide index
     * @param carouselInstance - Bootstrap carousel instance
     * @param currentCarousel - Current carousel element
     * @returns True if moved to previous slide
     */
    private moveToPreviousSlide;
    /**
     * Focus first thumbnail in new slide
     * @param currentCarousel - Current carousel element
     */
    private focusFirstThumbnailInNewSlide;
    /**
     * Focus last thumbnail in new slide
     * @param currentCarousel - Current carousel element
     */
    private focusLastThumbnailInNewSlide;
    /**
     * Update carousel visual indicators
     */
    updateCarouselIndicators(): void;
}
/**
 * Handles dropdown menu interactions in TV mode
 */
declare class DropdownManager {
    /**
     * Element manager reference
     */
    private readonly elementManager;
    /**
     * Create a DropdownManager instance
     * @param elementManager - Element manager instance
     */
    constructor(elementManager: FocusableElementManager);
    /**
     * Check if element is a dropdown toggle
     * @param element - Element to check
     * @returns True if element is dropdown toggle
     */
    isDropdownToggle(element: HTMLElement | null): boolean;
    /**
     * Check if dropdown is currently open
     * @param toggleElement - Dropdown toggle element
     * @returns True if dropdown is open
     */
    isDropdownOpen(toggleElement: HTMLElement): boolean;
    /**
     * Handle dropdown toggle interaction
     * @param toggleElement - Dropdown toggle element
     */
    toggleDropdown(toggleElement: HTMLElement): void;
    /**
     * Open dropdown menu
     * @param dropdownMenu - Dropdown menu element
     */
    private openDropdown;
    /**
     * Close dropdown menu
     * @param dropdownMenu - Dropdown menu element
     */
    private closeDropdown;
    /**
     * Close all open dropdowns
     */
    closeAllDropdowns(): void;
}
/**
 * Main TV Navigation controller class
 */
declare class TVNavigationController {
    /**
     * TV detection manager
     */
    private readonly tvDetection;
    /**
     * Key handler for remote input
     */
    private readonly keyHandler;
    /**
     * Focusable element manager
     */
    private readonly elementManager;
    /**
     * Focus state manager
     */
    private readonly focusManager;
    /**
     * Directional navigation handler
     */
    private readonly directionalNav;
    /**
     * Carousel navigation handler
     */
    private readonly carouselNav;
    /**
     * Dropdown interaction manager
     */
    private readonly dropdownManager;
    /**
     * Whether TV navigation is currently active
     */
    private navigationActive;
    /**
     * Mutation observer for DOM changes
     */
    private observer;
    /**
     * Create a TVNavigationController instance
     */
    constructor();
    /**
     * Initialize TV navigation system
     */
    init(): void;
    /**
     * Set up event listeners
     */
    private setupEventListeners;
    /**
     * Set up dropdown behavior overrides
     */
    private setupDropdownOverrides;
    /**
     * Set up mutation observer for DOM changes
     */
    private setupMutationObserver;
    /**
     * Start TV navigation mode
     */
    startTVNavigation(): void;
    /**
     * Stop TV navigation mode
     */
    stopTVNavigation(): void;
    /**
     * Handle keyboard input from TV remote
     * @param event - Keyboard event
     */
    private handleKeydown;
    /**
     * Process navigation command based on normalized key
     * @param key - Normalized key command
     */
    private processNavigationCommand;
    /**
     * Handle downward navigation
     * @param currentElement - Currently focused element
     */
    private handleDownNavigation;
    /**
     * Handle upward navigation
     * @param currentElement - Currently focused element
     */
    private handleUpNavigation;
    /**
     * Handle horizontal navigation
     * @param direction - 'ArrowLeft' or 'ArrowRight'
     * @param currentElement - Currently focused element
     */
    private handleHorizontalNavigation;
    /**
     * Handle activation (Enter/Space)
     * @param currentElement - Currently focused element
     */
    private handleActivation;
    /**
     * Handle escape key
     */
    private handleEscape;
    /**
     * Activate an element (click it)
     * @param element - Element to activate
     */
    private activateElement;
    /**
     * Find clickable element within a thumbnail
     * @param thumbnailElement - Thumbnail element to search
     * @returns Clickable element or null
     */
    private findClickableElement;
    /**
     * Find alternative navigation for dropdown scenarios
     * @returns Next element index or -1
     */
    private findAlternativeDownNavigation;
    /**
     * Expose debug functions for development
     */
    exposeDebugInterface(): void;
}
declare global {
    interface Window {
        debugTVNavigation: DebugTVNavigation;
    }
}
export { TVNavigationController, TVDetectionManager, TVKeyHandler, FocusableElementManager, FocusManager, DirectionalNavigator, CarouselNavigator, DropdownManager, TVNavigationConfig, TVKeyMappings, type NavigationDirection, type ElementSection, type NavigationResult, type BootstrapCarousel, type DebugTVNavigation };
//# sourceMappingURL=tvNavigation.d.ts.map