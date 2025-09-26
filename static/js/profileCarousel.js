/**
 * @fileoverview Profile picture carousel functionality.
 * Manages selection and navigation of profile pictures in a Bootstrap carousel.
 */

/**
 * Configuration constants for the profile carousel
 * @readonly
 * @enum {string}
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
 * @class ProfileCarouselManager
 */
class ProfileCarouselManager {
    /**
     * Create a ProfileCarouselManager instance
     * @param {string} [carouselId='profilePicCarousel'] - ID of the carousel element
     * @param {string} [hiddenInputId='profile_pic'] - ID of the hidden input element
     * @memberof ProfileCarouselManager
     */
    constructor(carouselId = ProfileCarouselConfig.DEFAULT_CAROUSEL_ID, hiddenInputId = ProfileCarouselConfig.DEFAULT_HIDDEN_INPUT_ID) {
        /**
         * The carousel DOM element
         * @type {HTMLElement}
         */
        this.carousel = document.getElementById(carouselId);
        
        /**
         * Array of carousel item elements
         * @type {NodeList}
         */
        this.items = null;
        
        /**
         * Hidden input element to store selected profile picture value
         * @type {HTMLInputElement}
         */
        this.hiddenInput = document.getElementById(hiddenInputId);
        
        /**
         * Bootstrap carousel instance
         * @type {Object}
         */
        this.carouselInstance = null;
        
        /**
         * Currently selected item index
         * @type {number}
         */
        this.selectedIndex = 0;

        this.init();
    }

    /**
     * Initialize the profile carousel manager
     * @memberof ProfileCarouselManager
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
     * @returns {boolean} True if all required elements exist
     * @private
     * @memberof ProfileCarouselManager
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
     * @returns {Object} Bootstrap carousel instance
     * @private
     * @memberof ProfileCarouselManager
     */
    getBootstrapCarouselInstance() {
        if (typeof bootstrap === 'undefined' || !bootstrap.Carousel) {
            console.warn('Bootstrap Carousel not available');
            return null;
        }

        return bootstrap.Carousel.getOrCreateInstance(this.carousel);
    }

    /**
     * Set up event listeners for carousel interactions
     * @private
     * @memberof ProfileCarouselManager
     */
    setupEventListeners() {
        this.setupClickListeners();
        this.setupSlideListener();
    }

    /**
     * Set up click event listeners on carousel items
     * @private
     * @memberof ProfileCarouselManager
     */
    setupClickListeners() {
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
     * @private
     * @memberof ProfileCarouselManager
     */
    setupSlideListener() {
        this.carousel.addEventListener('slid.bs.carousel', (e) => {
            this.selectItem(e.to);
        });
    }

    /**
     * Handle click on carousel item
     * @param {number} index - Index of clicked item
     * @private
     * @memberof ProfileCarouselManager
     */
    handleItemClick(index) {
        this.selectItem(index);
        this.navigateToItem(index);
    }

    /**
     * Select a carousel item by index
     * @param {number} index - Index of item to select
     * @memberof ProfileCarouselManager
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
     * @param {number} index - Index to validate
     * @returns {boolean} True if index is valid
     * @private
     * @memberof ProfileCarouselManager
     */
    isValidIndex(index) {
        return index >= 0 && index < this.items.length;
    }

    /**
     * Clear selection from all carousel items
     * @private
     * @memberof ProfileCarouselManager
     */
    clearAllSelections() {
        this.items.forEach(item => {
            item.classList.remove(ProfileCarouselConfig.SELECTED_CLASS);
        });
    }

    /**
     * Mark specific item as selected
     * @param {number} index - Index of item to mark as selected
     * @private
     * @memberof ProfileCarouselManager
     */
    setSelectedItem(index) {
        this.items[index].classList.add(ProfileCarouselConfig.SELECTED_CLASS);
    }

    /**
     * Update hidden input with selected profile picture value
     * @param {number} index - Index of selected item
     * @private
     * @memberof ProfileCarouselManager
     */
    updateHiddenInput(index) {
        const selectedItem = this.items[index];
        const picValue = selectedItem.getAttribute(ProfileCarouselConfig.DATA_PIC_ATTRIBUTE);
        
        if (picValue) {
            this.hiddenInput.value = picValue;
        } else {
            console.warn(`No ${ProfileCarouselConfig.DATA_PIC_ATTRIBUTE} attribute found on item ${index}`);
        }
    }

    /**
     * Navigate carousel to specific item
     * @param {number} index - Index of item to navigate to
     * @memberof ProfileCarouselManager
     */
    navigateToItem(index) {
        if (this.carouselInstance && this.isValidIndex(index)) {
            this.carouselInstance.to(index);
        }
    }

    /**
     * Get currently selected item index
     * @returns {number} Currently selected index
     * @memberof ProfileCarouselManager
     */
    getSelectedIndex() {
        return this.selectedIndex;
    }

    /**
     * Get currently selected profile picture value
     * @returns {string} Currently selected profile picture value
     * @memberof ProfileCarouselManager
     */
    getSelectedValue() {
        return this.hiddenInput.value;
    }

    /**
     * Get total number of carousel items
     * @returns {number} Number of carousel items
     * @memberof ProfileCarouselManager
     */
    getItemCount() {
        return this.items.length;
    }

    /**
     * Programmatically select next item
     * @memberof ProfileCarouselManager
     */
    selectNext() {
        const nextIndex = (this.selectedIndex + 1) % this.items.length;
        this.selectItem(nextIndex);
        this.navigateToItem(nextIndex);
    }

    /**
     * Programmatically select previous item
     * @memberof ProfileCarouselManager
     */
    selectPrevious() {
        const prevIndex = (this.selectedIndex - 1 + this.items.length) % this.items.length;
        this.selectItem(prevIndex);
        this.navigateToItem(prevIndex);
    }

    /**
     * Destroy the carousel manager and clean up event listeners
     * @memberof ProfileCarouselManager
     */
    destroy() {
        // Remove click listeners
        this.items.forEach(item => {
            const img = item.querySelector('img');
            if (img) {
                img.removeEventListener('click', this.handleItemClick);
            }
        });

        // Remove carousel listener
        this.carousel.removeEventListener('slid.bs.carousel', this.selectItem);
    }
}

// Global instance
let profileCarouselManager;

/**
 * Initialize profile carousel functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    profileCarouselManager = new ProfileCarouselManager();
});