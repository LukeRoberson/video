/**
 * @fileoverview Category population and lazy loading functionality for video manager.
 * Handles loading videos and thumbnails dynamically for each category with performance optimization.
 * Pages are organized by main category with subcategory carousels using lazy loading via IntersectionObserver API.
 */
/**
 * Configuration constants for category population
 */
declare const CategoryConfig: {
    /** API base URL for new endpoints (separate server) */
    readonly API_BASE_URL: "http://localhost:5010";
    /** API base URL for legacy endpoints */
    readonly LEGACY_API_BASE_URL: "http://localhost:5000";
    /** API endpoint pattern for category videos */
    readonly API_ENDPOINT_PATTERN: "/api/categories/{categoryId}/{subcategoryId}";
    /** Delay before enhancing TV navigation */
    readonly TV_ENHANCEMENT_DELAY: 500;
    /** Observer threshold for intersection */
    readonly INTERSECTION_THRESHOLD: 0.1;
    /** Observer root margin */
    readonly INTERSECTION_ROOT_MARGIN: "50px";
};
/**
 * Video data object structure
 */
interface Video {
    /** Video ID */
    id: number | string;
    /** Video name/title */
    name: string;
    /** Thumbnail URL */
    thumbnail: string;
    /** Video duration string */
    duration: string;
    /** Whether the video has been watched */
    watched: boolean;
}
/**
 * TV detection interface
 */
interface TVDetection {
    isTV(): boolean;
}
/**
 * Handles video thumbnail rendering and display
 */
declare class VideoThumbnailRenderer {
    /**
     * Create a video thumbnail renderer
     */
    constructor();
    /**
     * Render video thumbnails for a category
     * @param videos - Array of video objects
     * @param container - Container element for thumbnails
     */
    renderThumbnails(videos: Video[], container: HTMLElement | null): void;
    /**
     * Apply current watched video toggle state to newly rendered thumbnails
     * @param container - Container element for thumbnails
     */
    private applyCurrentToggleState;
    /**
     * Create HTML for a single video thumbnail
     * @param video - Video object with id, name, thumbnail, duration, watched properties
     * @returns HTML string for the thumbnail
     */
    private createThumbnailHTML;
    /**
     * Create watched icon HTML
     * @returns HTML for watched icon
     */
    private createWatchedIcon;
}
/**
 * Handles API calls for category data
 */
declare class CategoryApiService {
    /**
     * Create a category API service
     */
    constructor();
    /**
     * Fetch videos for a specific category and subcategory
     * @param categoryId - The main category ID
     * @param subcategoryId - The subcategory ID
     * @returns Promise resolving to array of video objects
     */
    fetchCategoryVideos(categoryId: string | number, subcategoryId: string | number): Promise<Video[]>;
}
/**
 * Manages lazy loading of category content using IntersectionObserver
 */
declare class CategoryLazyLoader {
    /** Category populator instance */
    private categoryPopulator;
    /** Intersection observer instance */
    private observer;
    /** Set of observed category rows */
    private observedRows;
    /**
     * Create a category lazy loader
     * @param categoryPopulator - The category populator instance
     */
    constructor(categoryPopulator: CategoryPopulator);
    /**
     * Create and configure intersection observer
     * @returns Configured intersection observer
     */
    private createObserver;
    /**
     * Handle intersection observer callback
     * @param entry - The intersection observer entry
     */
    private handleIntersection;
    /**
     * Start observing category rows for lazy loading
     */
    observeCategoryRows(): void;
    /**
     * Stop observing all category rows and cleanup
     */
    destroy(): void;
}
/**
 * Handles TV-specific enhancements for category navigation
 */
declare class TVCategoryEnhancer {
    /** Whether the current device is a TV */
    private isTV;
    /**
     * Create a TV category enhancer
     */
    constructor();
    /**
     * Detect if the current device is a TV
     * @returns True if device is detected as TV
     */
    private detectTVDevice;
    /**
     * Apply TV-specific enhancements to category navigation
     */
    enhanceForTV(): void;
    /**
     * Enhance category rows for TV viewing
     */
    private enhanceCategoryRows;
    /**
     * Add visual scroll indicators for TV navigation
     */
    private addScrollIndicators;
    /**
     * Add scroll indicator to a specific container
     * @param container - The thumbnail container
     */
    private addScrollIndicator;
}
/**
 * Main controller for category population functionality
 */
declare class CategoryPopulator {
    /** Video thumbnail renderer instance */
    private thumbnailRenderer;
    /** Category API service instance */
    private apiService;
    /** Lazy loader instance */
    private lazyLoader;
    /** TV enhancement instance */
    private tvEnhancer;
    /**
     * Create a category populator instance
     */
    constructor();
    /**
     * Initialize the category populator
     */
    init(): void;
    /**
     * Populate a specific category with videos
     * @param categoryId - The main category ID
     * @param subcategoryId - The subcategory ID
     */
    populateCategory(categoryId: string | number, subcategoryId: string | number): Promise<void>;
    /**
     * Get thumbnail container element for a subcategory
     * @param subcategoryId - The subcategory ID
     * @returns The thumbnail container element or null
     */
    private getThumbnailContainer;
    /**
     * Update arrow visibility for carousel navigation
     * @param subcategoryId - The subcategory ID
     */
    private updateArrowVisibility;
    /**
     * Handle errors during category population
     * @param subcategoryId - The subcategory ID
     * @param _error - The error that occurred
     */
    private handlePopulationError;
    /**
     * Cleanup resources and observers
     */
    destroy(): void;
}
declare let categoryPopulator: CategoryPopulator | undefined;
//# sourceMappingURL=populateCategories.d.ts.map