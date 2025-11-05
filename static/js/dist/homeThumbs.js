"use strict";
/**
 * homeThumbs.ts
 *
 * Manages the sizing and dynamic loading of thumbnail carousels on the home page.
 * Thumbnails are loaded as batches for a nice scrolling experience.
 * The number of thumbnails per batch is determined by the screen width.
 * The width of each thumbnail is adjusted based on the parent container's width.
 */
/**
 * Configuration class for carousel display settings
 */
class CarouselConfig {
    /**
     * Get screen configuration based on screen width and device type
     * @param screenWidth - The current screen width in pixels
     * @param isTV - Whether the device is a TV
     * @returns Configuration object with batchSize, padding, and optional thumbnailWidth
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
        }
        else if (screenWidth <= 576) {
            return { batchSize: 2, padding: 20 };
        }
        else if (screenWidth <= 820) {
            return { batchSize: 3, padding: 35 };
        }
        else {
            return { batchSize: 3, padding: 35 };
        }
    }
}
/**
 * Manages individual thumbnail carousel behavior and layout
 */
class ThumbnailCarousel {
    /**
     * Create a thumbnail carousel instance
     * @param carouselElement - The carousel DOM element
     */
    constructor(carouselElement) {
        this.carousel = carouselElement;
        const innerElement = carouselElement.querySelector('.carousel-inner');
        if (!innerElement) {
            throw new Error('Carousel inner element not found');
        }
        this.carouselInner = innerElement;
        this.videos = Array.from(this.carouselInner.querySelectorAll('.thumbnail-home'));
        this.autoAdvanceInterval = null;
    }
    /**
     * Update the carousel layout based on configuration
     * @param config - Configuration object from CarouselConfig
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
     * @param parentWidth - Width of the parent container
     * @param config - Configuration object
     * @returns Calculated thumbnail width in pixels
     */
    calculateThumbnailWidth(parentWidth, config) {
        if (config.thumbnailWidth) {
            return config.thumbnailWidth; // TV mode has fixed width
        }
        const width = (parentWidth - config.padding) / config.batchSize;
        return Math.min(width, 330); // Maximum thumbnail width is 330px
    }
    /**
     * Apply width and height styles to all thumbnail elements
     * @param thumbnailWidth - Width to apply to thumbnails
     */
    applyThumbnailStyles(thumbnailWidth) {
        this.videos.forEach((thumbnail) => {
            thumbnail.style.width = `${thumbnailWidth}px`;
            // Apply height for TV mode to maintain aspect ratio
            const tvDetection = window.tvDetection;
            if (tvDetection?.isTV()) {
                thumbnail.style.height = `${thumbnailWidth * 0.75}px`;
            }
        });
    }
    /**
     * Create carousel batches from video thumbnails
     * @param batchSize - Number of thumbnails per batch
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
     * @param batch - Array of thumbnail elements for this batch
     * @param isActive - Whether this should be the active carousel item
     * @returns The created carousel item element
     */
    createCarouselItem(batch, isActive = false) {
        const carouselItem = document.createElement('div');
        carouselItem.classList.add('carousel-item');
        if (isActive)
            carouselItem.classList.add('active');
        const batchContainer = document.createElement('div');
        batchContainer.classList.add('d-flex', 'gap-3', 'justify-content-center');
        batch.forEach((video) => batchContainer.appendChild(video));
        carouselItem.appendChild(batchContainer);
        return carouselItem;
    }
    /**
     * Clear all content from the carousel inner container
     */
    clearCarousel() {
        this.carouselInner.innerHTML = '';
    }
    /**
     * Make the carousel visible by setting visibility and opacity
     */
    showCarousel() {
        this.carousel.style.visibility = 'visible';
        this.carousel.style.opacity = '1';
    }
    /**
     * Start auto-advance functionality for the carousel
     * Automatically advances to the next slide every 10 seconds
     */
    startAutoAdvance() {
        this.stopAutoAdvance(); // Clear any existing interval
        this.autoAdvanceInterval = window.setInterval(() => {
            const nextButton = this.carousel.querySelector('.carousel-control-next');
            if (nextButton && !document.querySelector('.tv-focused')) {
                nextButton.click();
            }
        }, 10000);
    }
    /**
     * Stop auto-advance functionality
     */
    stopAutoAdvance() {
        if (this.autoAdvanceInterval !== null) {
            clearInterval(this.autoAdvanceInterval);
            this.autoAdvanceInterval = null;
        }
    }
}
/**
 * Main manager class that orchestrates all thumbnail carousels on the home page
 */
class HomeThumbnailManager {
    /**
     * Create the thumbnail manager and initialize all carousels
     */
    constructor() {
        this.carousels = [];
        const tvDetection = window.tvDetection;
        this.isTV = tvDetection?.isTV() || false;
        this.init();
    }
    /**
     * Initialize the thumbnail manager
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
     */
    initializeCarousels() {
        const carouselElements = document.querySelectorAll('.carousel[data-dynamic="true"]');
        carouselElements.forEach((element) => {
            this.carousels.push(new ThumbnailCarousel(element));
        });
    }
    /**
     * Set up event listeners for resize and TV mode changes
     */
    setupEventListeners() {
        window.addEventListener('resize', () => this.updateAllCarousels());
        const tvDetection = window.tvDetection;
        if (tvDetection) {
            window.addEventListener('tvModeChanged', (e) => {
                const tvEvent = e;
                this.isTV = tvEvent.detail.isTV;
                if (this.isTV) {
                    this.setupTVMode();
                }
                else {
                    this.resetToNormalMode();
                }
            });
        }
    }
    /**
     * Update the layout of all carousels based on current screen size
     */
    updateAllCarousels() {
        const screenWidth = window.innerWidth;
        const config = CarouselConfig.getScreenConfig(screenWidth, this.isTV);
        this.carousels.forEach((carousel) => {
            carousel.updateLayout(config);
        });
    }
    /**
     * Configure carousels for TV mode operation
     */
    setupTVMode() {
        this.updateAllCarousels();
        // Start auto-advance for TV mode
        this.carousels.forEach((carousel) => {
            carousel.startAutoAdvance();
        });
    }
    /**
     * Reset carousels from TV mode to normal mode
     */
    resetToNormalMode() {
        this.carousels.forEach((carousel) => {
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
//# sourceMappingURL=homeThumbs.js.map