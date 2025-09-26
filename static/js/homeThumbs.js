/**
 * homeThumbs.js
 * 
 * Manages the sizing and dynamic loading of thumbnail carousels on the home page.
 * Thumbnails are loaded as batches for a nice scrolling experience.
 * The number of thumbnails per batch is determined by the screen width.
 * The width of each thumbnail is adjusted based on the parent container's width.
 */

/**
 * Configuration class for carousel display settings
 * @class CarouselConfig
 */
class CarouselConfig {
    /**
     * Get screen configuration based on screen width and device type
     * @static
     * @param {number} screenWidth - The current screen width in pixels
     * @param {boolean} [isTV=false] - Whether the device is a TV
     * @returns {Object} Configuration object with batchSize, padding, and optional thumbnailWidth
     * @memberof CarouselConfig
     */
    static getScreenConfig(screenWidth, isTV = false) {
        if (isTV) {
            if (screenWidth >= 3840) {
                return { batchSize: 6, thumbnailWidth: 350, padding: 35 };
            }
            return { batchSize: 4, thumbnailWidth: 320, padding: 35 };
        }

        // Regular screen configurations
        if (screenWidth <= 400) {
            return { batchSize: 2, padding: 17 };
        } else if (screenWidth <= 576) {
            return { batchSize: 2, padding: 20 };
        } else if (screenWidth <= 820) {
            return { batchSize: 3, padding: 35 };
        } else {
            return { batchSize: 3, padding: 35 };
        }
    }
}

/**
 * Manages individual thumbnail carousel behavior and layout
 * @class ThumbnailCarousel
 */
class ThumbnailCarousel {
    /**
     * Create a thumbnail carousel instance
     * @param {HTMLElement} carouselElement - The carousel DOM element
     * @memberof ThumbnailCarousel
     */
    constructor(carouselElement) {
        /**
         * The main carousel DOM element
         * @type {HTMLElement}
         */
        this.carousel = carouselElement;
        
        /**
         * The carousel inner container element
         * @type {HTMLElement}
         */
        this.carouselInner = carouselElement.querySelector('.carousel-inner');
        
        /**
         * Array of video thumbnail elements
         * @type {HTMLElement[]}
         */
        this.videos = Array.from(this.carouselInner.querySelectorAll('.thumbnail-home'));
        
        /**
         * Auto-advance interval ID
         * @type {?number}
         */
        this.autoAdvanceInterval = null;
    }

    /**
     * Update the carousel layout based on configuration
     * @param {Object} config - Configuration object from CarouselConfig
     * @param {number} config.batchSize - Number of thumbnails per batch
     * @param {number} config.padding - Padding value for calculations
     * @param {number} [config.thumbnailWidth] - Fixed thumbnail width for TV mode
     * @memberof ThumbnailCarousel
     */
    updateLayout(config) {
        this.clearCarousel();
        
        const parentWidth = this.carousel.offsetWidth || window.innerWidth;
        const thumbnailWidth = this.calculateThumbnailWidth(parentWidth, config);
        
        this.applyThumbnailStyles(thumbnailWidth);
        this.createBatches(config.batchSize);
        this.showCarousel();
    }

    /**
     * Calculate the appropriate thumbnail width based on parent container and configuration
     * @param {number} parentWidth - Width of the parent container
     * @param {Object} config - Configuration object
     * @param {number} [config.thumbnailWidth] - Fixed width for TV mode
     * @param {number} config.batchSize - Number of thumbnails per batch
     * @param {number} config.padding - Padding value
     * @returns {number} Calculated thumbnail width in pixels
     * @memberof ThumbnailCarousel
     */
    calculateThumbnailWidth(parentWidth, config) {
        if (config.thumbnailWidth) {
            return config.thumbnailWidth; // TV mode has fixed width
        }
        
        let width = (parentWidth - config.padding) / config.batchSize;
        return Math.min(width, 330); // Maximum thumbnail width is 330px
    }

    /**
     * Apply width and height styles to all thumbnail elements
     * @param {number} thumbnailWidth - Width to apply to thumbnails
     * @memberof ThumbnailCarousel
     */
    applyThumbnailStyles(thumbnailWidth) {
        this.videos.forEach(thumbnail => {
            thumbnail.style.width = `${thumbnailWidth}px`;
            // Apply height for TV mode to maintain aspect ratio
            if (window.tvDetection?.isTV()) {
                thumbnail.style.height = `${thumbnailWidth * 0.75}px`;
            }
        });
    }

    /**
     * Create carousel batches from video thumbnails
     * @param {number} batchSize - Number of thumbnails per batch
     * @memberof ThumbnailCarousel
     */
    createBatches(batchSize) {
        for (let i = 0; i < this.videos.length; i += batchSize) {
            const batch = this.videos.slice(i, i + batchSize);
            const carouselItem = this.createCarouselItem(batch, i === 0);
            this.carouselInner.appendChild(carouselItem);
        }
    }

    /**
     * Create a single carousel item containing a batch of thumbnails
     * @param {HTMLElement[]} batch - Array of thumbnail elements for this batch
     * @param {boolean} [isActive=false] - Whether this should be the active carousel item
     * @returns {HTMLElement} The created carousel item element
     * @memberof ThumbnailCarousel
     */
    createCarouselItem(batch, isActive = false) {
        const carouselItem = document.createElement('div');
        carouselItem.classList.add('carousel-item');
        if (isActive) carouselItem.classList.add('active');

        const batchContainer = document.createElement('div');
        batchContainer.classList.add('d-flex', 'gap-3', 'justify-content-center');
        batch.forEach(video => batchContainer.appendChild(video));

        carouselItem.appendChild(batchContainer);
        return carouselItem;
    }

    /**
     * Clear all content from the carousel inner container
     * @memberof ThumbnailCarousel
     */
    clearCarousel() {
        this.carouselInner.innerHTML = '';
    }

    /**
     * Make the carousel visible by setting visibility and opacity
     * @memberof ThumbnailCarousel
     */
    showCarousel() {
        this.carousel.style.visibility = 'visible';
        this.carousel.style.opacity = '1';
    }

    /**
     * Start auto-advance functionality for the carousel
     * Automatically advances to the next slide every 10 seconds
     * @memberof ThumbnailCarousel
     */
    startAutoAdvance() {
        this.stopAutoAdvance(); // Clear any existing interval
        
        this.autoAdvanceInterval = setInterval(() => {
            const nextButton = this.carousel.querySelector('.carousel-control-next');
            if (nextButton && !document.querySelector('.tv-focused')) {
                nextButton.click();
            }
        }, 10000);
    }

    /**
     * Stop auto-advance functionality
     * @memberof ThumbnailCarousel
     */
    stopAutoAdvance() {
        if (this.autoAdvanceInterval) {
            clearInterval(this.autoAdvanceInterval);
            this.autoAdvanceInterval = null;
        }
    }
}

/**
 * Main manager class that orchestrates all thumbnail carousels on the home page
 * @class HomeThumbnailManager
 */
class HomeThumbnailManager {
    /**
     * Create the thumbnail manager and initialize all carousels
     * @memberof HomeThumbnailManager
     */
    constructor() {
        /**
         * Array of ThumbnailCarousel instances
         * @type {ThumbnailCarousel[]}
         */
        this.carousels = [];
        
        /**
         * Whether the current device is a TV
         * @type {boolean}
         */
        this.isTV = window.tvDetection?.isTV() || false;
        
        this.init();
    }

    /**
     * Initialize the thumbnail manager
     * @memberof HomeThumbnailManager
     */
    init() {
        this.initializeCarousels();
        this.setupEventListeners();
        this.updateAllCarousels();
        
        if (this.isTV) {
            this.setupTVMode();
        }
    }

    /**
     * Find and initialize all dynamic carousels on the page
     * @memberof HomeThumbnailManager
     */
    initializeCarousels() {
        const carouselElements = document.querySelectorAll('.carousel[data-dynamic="true"]');
        carouselElements.forEach(element => {
            this.carousels.push(new ThumbnailCarousel(element));
        });
    }

    /**
     * Set up event listeners for resize and TV mode changes
     * @memberof HomeThumbnailManager
     */
    setupEventListeners() {
        window.addEventListener('resize', () => this.updateAllCarousels());
        
        if (window.tvDetection) {
            window.addEventListener('tvModeChanged', (e) => {
                this.isTV = e.detail.isTV;
                if (this.isTV) {
                    this.setupTVMode();
                } else {
                    this.resetToNormalMode();
                }
            });
        }
    }

    /**
     * Update the layout of all carousels based on current screen size
     * @memberof HomeThumbnailManager
     */
    updateAllCarousels() {
        const screenWidth = window.innerWidth;
        const config = CarouselConfig.getScreenConfig(screenWidth, this.isTV);

        this.carousels.forEach(carousel => {
            carousel.updateLayout(config);
        });
    }

    /**
     * Configure carousels for TV mode operation
     * @memberof HomeThumbnailManager
     */
    setupTVMode() {
        this.updateAllCarousels();
        
        // Start auto-advance for TV mode
        this.carousels.forEach(carousel => {
            carousel.startAutoAdvance();
        });
    }

    /**
     * Reset carousels from TV mode to normal mode
     * @memberof HomeThumbnailManager
     */
    resetToNormalMode() {
        this.carousels.forEach(carousel => {
            carousel.stopAutoAdvance();
        });
        
        // Simple approach to reset - could be improved
        location.reload();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new HomeThumbnailManager();
});