"use strict";
/**
 * @fileoverview Profile picture carousel functionality.
 * Manages selection and navigation of profile pictures in a Bootstrap carousel.
 */
/**
 * Configuration constants for the profile carousel
 */
const ProfileCarouselConfig = {
    /** Default carousel element ID */
    DEFAULT_CAROUSEL_ID: 'profilePicCarousel',
    /** Default hidden input element ID */
    DEFAULT_HIDDEN_INPUT_ID: 'profile_pic',
    /** CSS class for selected items */
    SELECTED_CLASS: 'selected',
    /** Data attribute for profile picture value */
    DATA_PIC_ATTRIBUTE: 'data-pic'
};
/**
 * Manages profile picture selection and carousel navigation
 */
class ProfileCarouselManager {
    /**
     * Create a ProfileCarouselManager instance
     * @param carouselId - ID of the carousel element
     * @param hiddenInputId - ID of the hidden input element
     */
    constructor(carouselId = ProfileCarouselConfig.DEFAULT_CAROUSEL_ID, hiddenInputId = ProfileCarouselConfig.DEFAULT_HIDDEN_INPUT_ID) {
        const carouselElement = document.getElementById(carouselId);
        if (!carouselElement) {
            throw new Error(`Carousel element with ID "${carouselId}" not found`);
        }
        this.carousel = carouselElement;
        this.items = null;
        const inputElement = document.getElementById(hiddenInputId);
        if (!inputElement || !(inputElement instanceof HTMLInputElement)) {
            throw new Error(`Hidden input element with ID "${hiddenInputId}" not found`);
        }
        this.hiddenInput = inputElement;
        this.carouselInstance = null;
        this.selectedIndex = 0;
        this.init();
    }
    /**
     * Initialize the profile carousel manager
     */
    init() {
        if (!this.validateElements()) {
            return;
        }
        this.items = this.carousel.querySelectorAll('.carousel-item');
        this.carouselInstance = this.getBootstrapCarouselInstance();
        this.setupEventListeners();
        this.selectItem(0); // Set initial selection
    }
    /**
     * Validate that required DOM elements exist
     * @returns True if all required elements exist
     */
    validateElements() {
        if (!this.carousel) {
            console.error('Profile carousel element not found');
            return false;
        }
        if (!this.hiddenInput) {
            console.error('Profile picture hidden input not found');
            return false;
        }
        return true;
    }
    /**
     * Get or create Bootstrap carousel instance
     * @returns Bootstrap carousel instance or null if Bootstrap is not available
     */
    getBootstrapCarouselInstance() {
        const bootstrap = window.bootstrap;
        if (typeof bootstrap === 'undefined' || !bootstrap.Carousel) {
            console.warn('Bootstrap Carousel not available');
            return null;
        }
        return bootstrap.Carousel.getOrCreateInstance(this.carousel);
    }
    /**
     * Set up event listeners for carousel interactions
     */
    setupEventListeners() {
        this.setupClickListeners();
        this.setupSlideListener();
    }
    /**
     * Set up click event listeners on carousel items
     */
    setupClickListeners() {
        if (!this.items)
            return;
        this.items.forEach((item, index) => {
            const img = item.querySelector('img');
            if (img) {
                img.addEventListener('click', () => this.handleItemClick(index));
                img.style.cursor = 'pointer'; // Add visual feedback
            }
        });
    }
    /**
     * Set up slide event listener for carousel
     */
    setupSlideListener() {
        this.carousel.addEventListener('slid.bs.carousel', (e) => {
            const slideEvent = e;
            if (typeof slideEvent.to === 'number') {
                this.selectItem(slideEvent.to);
            }
        });
    }
    /**
     * Handle click on carousel item
     * @param index - Index of clicked item
     */
    handleItemClick(index) {
        this.selectItem(index);
        this.navigateToItem(index);
    }
    /**
     * Select a carousel item by index
     * @param index - Index of item to select
     */
    selectItem(index) {
        if (!this.isValidIndex(index)) {
            console.warn(`Invalid item index: ${index}`);
            return;
        }
        this.clearAllSelections();
        this.setSelectedItem(index);
        this.updateHiddenInput(index);
        this.selectedIndex = index;
    }
    /**
     * Check if index is valid for current items
     * @param index - Index to validate
     * @returns True if index is valid
     */
    isValidIndex(index) {
        return this.items !== null && index >= 0 && index < this.items.length;
    }
    /**
     * Clear selection from all carousel items
     */
    clearAllSelections() {
        if (!this.items)
            return;
        this.items.forEach((item) => {
            item.classList.remove(ProfileCarouselConfig.SELECTED_CLASS);
        });
    }
    /**
     * Mark specific item as selected
     * @param index - Index of item to mark as selected
     */
    setSelectedItem(index) {
        if (!this.items)
            return;
        this.items[index].classList.add(ProfileCarouselConfig.SELECTED_CLASS);
    }
    /**
     * Update hidden input with selected profile picture value
     * @param index - Index of selected item
     */
    updateHiddenInput(index) {
        if (!this.items)
            return;
        const selectedItem = this.items[index];
        const picValue = selectedItem.getAttribute(ProfileCarouselConfig.DATA_PIC_ATTRIBUTE);
        if (picValue) {
            this.hiddenInput.value = picValue;
        }
        else {
            console.warn(`No ${ProfileCarouselConfig.DATA_PIC_ATTRIBUTE} attribute found on item ${index}`);
        }
    }
    /**
     * Navigate carousel to specific item
     * @param index - Index of item to navigate to
     */
    navigateToItem(index) {
        if (this.carouselInstance && this.isValidIndex(index)) {
            this.carouselInstance.to(index);
        }
    }
    /**
     * Get currently selected item index
     * @returns Currently selected index
     */
    getSelectedIndex() {
        return this.selectedIndex;
    }
    /**
     * Get currently selected profile picture value
     * @returns Currently selected profile picture value
     */
    getSelectedValue() {
        return this.hiddenInput.value;
    }
    /**
     * Get total number of carousel items
     * @returns Number of carousel items
     */
    getItemCount() {
        return this.items ? this.items.length : 0;
    }
    /**
     * Programmatically select next item
     */
    selectNext() {
        if (!this.items)
            return;
        const nextIndex = (this.selectedIndex + 1) % this.items.length;
        this.selectItem(nextIndex);
        this.navigateToItem(nextIndex);
    }
    /**
     * Programmatically select previous item
     */
    selectPrevious() {
        if (!this.items)
            return;
        const prevIndex = (this.selectedIndex - 1 + this.items.length) % this.items.length;
        this.selectItem(prevIndex);
        this.navigateToItem(prevIndex);
    }
    /**
     * Destroy the carousel manager and clean up event listeners
     */
    destroy() {
        if (!this.items)
            return;
        // Remove click listeners
        this.items.forEach((item) => {
            const img = item.querySelector('img');
            if (img) {
                const newImg = img.cloneNode(true);
                img.parentNode?.replaceChild(newImg, img);
            }
        });
        // Bootstrap handles its own cleanup
        if (this.carouselInstance) {
            this.carouselInstance.dispose();
        }
    }
}
// Global instance
let profileCarouselManager;
/**
 * Initialize profile carousel functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function () {
    try {
        profileCarouselManager = new ProfileCarouselManager();
    }
    catch (error) {
        console.error('Failed to initialize profile carousel:', error);
    }
});
//# sourceMappingURL=profileCarousel.js.map