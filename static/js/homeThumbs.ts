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
class CarouselConfig {
    /**
     * Get screen configuration based on screen width and device type
     * @param screenWidth - The current screen width in pixels
     * @param isTV - Whether the device is a TV
     * @returns Configuration object with batchSize, padding, and optional thumbnailWidth
     */
    static getScreenConfig(screenWidth: number, isTV: boolean = false): ScreenConfig {
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
 */
class ThumbnailCarousel {
    /** The main carousel DOM element */
    private carousel: HTMLElement;
    
    /** The carousel inner container element */
    private carouselInner: HTMLElement;
    
    /** Array of video thumbnail elements */
    private videos: HTMLElement[];
    
    /** Auto-advance interval ID */
    private autoAdvanceInterval: number | null;

    /**
     * Create a thumbnail carousel instance
     * @param carouselElement - The carousel DOM element
     */
    constructor(carouselElement: HTMLElement) {
        this.carousel = carouselElement;
        
        const innerElement = carouselElement.querySelector('.carousel-inner');
        if (!innerElement) {
            throw new Error('Carousel inner element not found');
        }
        this.carouselInner = innerElement as HTMLElement;
        
        this.videos = Array.from(this.carouselInner.querySelectorAll('.thumbnail-home')) as HTMLElement[];
        this.autoAdvanceInterval = null;
    }

    /**
     * Update the carousel layout based on configuration
     * @param config - Configuration object from CarouselConfig
     */
    updateLayout(config: ScreenConfig): void {
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
    private calculateThumbnailWidth(parentWidth: number, config: ScreenConfig): number {
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
    private applyThumbnailStyles(thumbnailWidth: number): void {
        this.videos.forEach((thumbnail: HTMLElement) => {
            thumbnail.style.width = `${thumbnailWidth}px`;
            // Apply height for TV mode to maintain aspect ratio
            const tvDetection = (window as any).tvDetection as TVDetection | undefined;
            if (tvDetection?.isTV()) {
                thumbnail.style.height = `${thumbnailWidth * 0.75}px`;
            }
        });
    }

    /**
     * Create carousel batches from video thumbnails
     * @param batchSize - Number of thumbnails per batch
     */
    private createBatches(batchSize: number): void {
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
    private createCarouselItem(batch: HTMLElement[], isActive: boolean = false): HTMLElement {
        const carouselItem = document.createElement('div');
        carouselItem.classList.add('carousel-item');
        if (isActive) carouselItem.classList.add('active');

        const batchContainer = document.createElement('div');
        batchContainer.classList.add('d-flex', 'gap-3', 'justify-content-center');
        batch.forEach((video: HTMLElement) => batchContainer.appendChild(video));

        carouselItem.appendChild(batchContainer);
        return carouselItem;
    }

    /**
     * Clear all content from the carousel inner container
     */
    private clearCarousel(): void {
        this.carouselInner.innerHTML = '';
    }

    /**
     * Make the carousel visible by setting visibility and opacity
     */
    private showCarousel(): void {
        this.carousel.style.visibility = 'visible';
        this.carousel.style.opacity = '1';
    }

    /**
     * Start auto-advance functionality for the carousel
     * Automatically advances to the next slide every 10 seconds
     */
    startAutoAdvance(): void {
        this.stopAutoAdvance(); // Clear any existing interval
        
        this.autoAdvanceInterval = window.setInterval(() => {
            const nextButton = this.carousel.querySelector('.carousel-control-next');
            if (nextButton && !document.querySelector('.tv-focused')) {
                (nextButton as HTMLElement).click();
            }
        }, 10000);
    }

    /**
     * Stop auto-advance functionality
     */
    stopAutoAdvance(): void {
        if (this.autoAdvanceInterval !== null) {
            clearInterval(this.autoAdvanceInterval);
            this.autoAdvanceInterval = null;
        }
    }
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
class HomeThumbnailManager {
    /** Array of ThumbnailCarousel instances */
    private carousels: ThumbnailCarousel[];
    
    /** Whether the current device is a TV */
    private isTV: boolean;

    /**
     * Create the thumbnail manager and initialize all carousels
     */
    constructor() {
        this.carousels = [];
        const tvDetection = (window as any).tvDetection as TVDetection | undefined;
        this.isTV = tvDetection?.isTV() || false;
        
        this.init();
    }

    /**
     * Initialize the thumbnail manager
     */
    private init(): void {
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
    private initializeCarousels(): void {
        const carouselElements = document.querySelectorAll('.carousel[data-dynamic="true"]');
        carouselElements.forEach((element: Element) => {
            this.carousels.push(new ThumbnailCarousel(element as HTMLElement));
        });
    }

    /**
     * Set up event listeners for resize and TV mode changes
     */
    private setupEventListeners(): void {
        window.addEventListener('resize', () => this.updateAllCarousels());
        
        const tvDetection = (window as any).tvDetection as TVDetection | undefined;
        if (tvDetection) {
            window.addEventListener('tvModeChanged', (e: Event) => {
                const tvEvent = e as TVModeChangeEvent;
                this.isTV = tvEvent.detail.isTV;
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
     */
    private updateAllCarousels(): void {
        const screenWidth = window.innerWidth;
        const config = CarouselConfig.getScreenConfig(screenWidth, this.isTV);

        this.carousels.forEach((carousel: ThumbnailCarousel) => {
            carousel.updateLayout(config);
        });
    }

    /**
     * Configure carousels for TV mode operation
     */
    private setupTVMode(): void {
        this.updateAllCarousels();
        
        // Start auto-advance for TV mode
        this.carousels.forEach((carousel: ThumbnailCarousel) => {
            carousel.startAutoAdvance();
        });
    }

    /**
     * Reset carousels from TV mode to normal mode
     */
    private resetToNormalMode(): void {
        this.carousels.forEach((carousel: ThumbnailCarousel) => {
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
