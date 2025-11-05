/**
 * @fileoverview Profile picture carousel functionality.
 * Manages selection and navigation of profile pictures in a Bootstrap carousel.
 */
/**
 * Configuration constants for the profile carousel
 */
declare const ProfileCarouselConfig: {
    /** Default carousel element ID */
    readonly DEFAULT_CAROUSEL_ID: "profilePicCarousel";
    /** Default hidden input element ID */
    readonly DEFAULT_HIDDEN_INPUT_ID: "profile_pic";
    /** CSS class for selected items */
    readonly SELECTED_CLASS: "selected";
    /** Data attribute for profile picture value */
    readonly DATA_PIC_ATTRIBUTE: "data-pic";
};
/**
 * Bootstrap Carousel interface
 */
interface BootstrapCarousel {
    to(index: number): void;
    next(): void;
    prev(): void;
    dispose(): void;
}
/**
 * Bootstrap object interface
 */
interface Bootstrap {
    Carousel: {
        getOrCreateInstance(element: HTMLElement): BootstrapCarousel;
    };
}
/**
 * Manages profile picture selection and carousel navigation
 */
declare class ProfileCarouselManager {
    /** The carousel DOM element */
    private carousel;
    /** Array of carousel item elements */
    private items;
    /** Hidden input element to store selected profile picture value */
    private hiddenInput;
    /** Bootstrap carousel instance */
    private carouselInstance;
    /** Currently selected item index */
    private selectedIndex;
    /**
     * Create a ProfileCarouselManager instance
     * @param carouselId - ID of the carousel element
     * @param hiddenInputId - ID of the hidden input element
     */
    constructor(carouselId?: string, hiddenInputId?: string);
    /**
     * Initialize the profile carousel manager
     */
    private init;
    /**
     * Validate that required DOM elements exist
     * @returns True if all required elements exist
     */
    private validateElements;
    /**
     * Get or create Bootstrap carousel instance
     * @returns Bootstrap carousel instance or null if Bootstrap is not available
     */
    private getBootstrapCarouselInstance;
    /**
     * Set up event listeners for carousel interactions
     */
    private setupEventListeners;
    /**
     * Set up click event listeners on carousel items
     */
    private setupClickListeners;
    /**
     * Set up slide event listener for carousel
     */
    private setupSlideListener;
    /**
     * Handle click on carousel item
     * @param index - Index of clicked item
     */
    private handleItemClick;
    /**
     * Select a carousel item by index
     * @param index - Index of item to select
     */
    selectItem(index: number): void;
    /**
     * Check if index is valid for current items
     * @param index - Index to validate
     * @returns True if index is valid
     */
    private isValidIndex;
    /**
     * Clear selection from all carousel items
     */
    private clearAllSelections;
    /**
     * Mark specific item as selected
     * @param index - Index of item to mark as selected
     */
    private setSelectedItem;
    /**
     * Update hidden input with selected profile picture value
     * @param index - Index of selected item
     */
    private updateHiddenInput;
    /**
     * Navigate carousel to specific item
     * @param index - Index of item to navigate to
     */
    navigateToItem(index: number): void;
    /**
     * Get currently selected item index
     * @returns Currently selected index
     */
    getSelectedIndex(): number;
    /**
     * Get currently selected profile picture value
     * @returns Currently selected profile picture value
     */
    getSelectedValue(): string;
    /**
     * Get total number of carousel items
     * @returns Number of carousel items
     */
    getItemCount(): number;
    /**
     * Programmatically select next item
     */
    selectNext(): void;
    /**
     * Programmatically select previous item
     */
    selectPrevious(): void;
    /**
     * Destroy the carousel manager and clean up event listeners
     */
    destroy(): void;
}
declare let profileCarouselManager: ProfileCarouselManager | undefined;
//# sourceMappingURL=profileCarousel.d.ts.map