/**
 * homeThumbs.ts
 *
 * Manages the sizing and dynamic loading of thumbnail carousels on the home page.
 * Thumbnails are loaded as batches for a nice scrolling experience.
 * The number of thumbnails per batch is determined by the screen width.
 * The width of each thumbnail is adjusted based on the parent container's width.
 */
/**
 * Configuration object returned by CarouselConfig.getScreenConfig
 */
interface ScreenConfig {
    /** Number of thumbnails per batch */
    batchSize: number;
    /** Padding value for calculations */
    padding: number;
    /** Fixed thumbnail width for TV mode (optional) */
    thumbnailWidth?: number;
}
/**
 * Configuration class for carousel display settings
 */
declare class CarouselConfig {
    /**
     * Get screen configuration based on screen width and device type
     * @param screenWidth - The current screen width in pixels
     * @param isTV - Whether the device is a TV
     * @returns Configuration object with batchSize, padding, and optional thumbnailWidth
     */
    static getScreenConfig(screenWidth: number, isTV?: boolean): ScreenConfig;
}
/**
 * Manages individual thumbnail carousel behavior and layout
 */
declare class ThumbnailCarousel {
    /** The main carousel DOM element */
    private carousel;
    /** The carousel inner container element */
    private carouselInner;
    /** Array of video thumbnail elements */
    private videos;
    /** Auto-advance interval ID */
    private autoAdvanceInterval;
    /**
     * Create a thumbnail carousel instance
     * @param carouselElement - The carousel DOM element
     */
    constructor(carouselElement: HTMLElement);
    /**
     * Update the carousel layout based on configuration
     * @param config - Configuration object from CarouselConfig
     */
    updateLayout(config: ScreenConfig): void;
    /**
     * Calculate the appropriate thumbnail width based on parent container and configuration
     * @param parentWidth - Width of the parent container
     * @param config - Configuration object
     * @returns Calculated thumbnail width in pixels
     */
    private calculateThumbnailWidth;
    /**
     * Apply width and height styles to all thumbnail elements
     * @param thumbnailWidth - Width to apply to thumbnails
     */
    private applyThumbnailStyles;
    /**
     * Create carousel batches from video thumbnails
     * @param batchSize - Number of thumbnails per batch
     */
    private createBatches;
    /**
     * Create a single carousel item containing a batch of thumbnails
     * @param batch - Array of thumbnail elements for this batch
     * @param isActive - Whether this should be the active carousel item
     * @returns The created carousel item element
     */
    private createCarouselItem;
    /**
     * Clear all content from the carousel inner container
     */
    private clearCarousel;
    /**
     * Make the carousel visible by setting visibility and opacity
     */
    private showCarousel;
    /**
     * Start auto-advance functionality for the carousel
     * Automatically advances to the next slide every 10 seconds
     */
    startAutoAdvance(): void;
    /**
     * Stop auto-advance functionality
     */
    stopAutoAdvance(): void;
}
/**
 * TV detection interface for type safety
 */
interface TVDetection {
    isTV(): boolean;
}
/**
 * Custom event detail for TV mode changes
 */
interface TVModeChangeEvent extends CustomEvent {
    detail: {
        isTV: boolean;
    };
}
/**
 * Main manager class that orchestrates all thumbnail carousels on the home page
 */
declare class HomeThumbnailManager {
    /** Array of ThumbnailCarousel instances */
    private carousels;
    /** Whether the current device is a TV */
    private isTV;
    /**
     * Create the thumbnail manager and initialize all carousels
     */
    constructor();
    /**
     * Initialize the thumbnail manager
     */
    private init;
    /**
     * Find and initialize all dynamic carousels on the page
     */
    private initializeCarousels;
    /**
     * Set up event listeners for resize and TV mode changes
     */
    private setupEventListeners;
    /**
     * Update the layout of all carousels based on current screen size
     */
    private updateAllCarousels;
    /**
     * Configure carousels for TV mode operation
     */
    private setupTVMode;
    /**
     * Reset carousels from TV mode to normal mode
     */
    private resetToNormalMode;
}
//# sourceMappingURL=homeThumbs.d.ts.map