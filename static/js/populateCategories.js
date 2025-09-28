/**
 * @fileoverview Category population and lazy loading functionality for video manager.
 * Handles loading videos and thumbnails dynamically for each category with performance optimization.
 * Pages are organized by main category with subcategory carousels using lazy loading via IntersectionObserver API.
 */

/**
 * Configuration constants for category population
 * @readonly
 * @enum {number|string}
 */
const CategoryConfig = {
    /** API endpoint pattern for category videos */
    API_ENDPOINT_PATTERN: '/api/categories/{categoryId}/{subcategoryId}',
    /** Delay before enhancing TV navigation */
    TV_ENHANCEMENT_DELAY: 500,
    /** Observer threshold for intersection */
    INTERSECTION_THRESHOLD: 0.1,
    /** Observer root margin */
    INTERSECTION_ROOT_MARGIN: '50px'
};

/**
 * Handles video thumbnail rendering and display
 * @class VideoThumbnailRenderer
 */
class VideoThumbnailRenderer {
    /**
     * Create a video thumbnail renderer
     * @memberof VideoThumbnailRenderer
     */
    constructor() {}

    /**
     * Render video thumbnails for a category
     * @param {Array<Object>} videos - Array of video objects
     * @param {HTMLElement} container - Container element for thumbnails
     * @memberof VideoThumbnailRenderer
     */
    renderThumbnails(videos, container) {
        if (!container) {
            console.warn('Thumbnail container not found');
            return;
        }

        const thumbnailsHTML = videos.map(video => this.createThumbnailHTML(video)).join('');
        container.innerHTML = thumbnailsHTML;
        
        // Apply current toggle state to newly rendered thumbnails
        this.applyCurrentToggleState(container);
    }

    /**
     * Apply current watched video toggle state to newly rendered thumbnails
     * @param {HTMLElement} container - Container element for thumbnails
     * @private
     * @memberof VideoThumbnailRenderer
     */
    applyCurrentToggleState(container) {
        // Check if watched videos should be hidden based on current toggle state
        const hideWatched = document.body.classList.contains('hide-watched');
        
        if (hideWatched) {
            const watchedThumbnails = container.querySelectorAll('.thumbnail--watched, [data-watched="true"]');
            watchedThumbnails.forEach(thumbnail => {
                thumbnail.style.display = 'none';
                thumbnail.setAttribute('data-hidden-by-toggle', 'true');
            });
        }
    }
    
    /**
     * Create HTML for a single video thumbnail
     * @param {Object} video - Video object with id, name, thumbnail, duration, watched properties
     * @returns {string} HTML string for the thumbnail
     * @private
     * @memberof VideoThumbnailRenderer
     */
    createThumbnailHTML(video) {
        // Apply BEM naming convention for watched videos
        const watchedClass = video.watched ? ' thumbnail--watched' : '';
        const watchedIcon = video.watched ? this.createWatchedIcon() : '';
        const watchedDataAttribute = video.watched ? ' data-watched="true"' : '';

        return `
            <div class="thumbnail${watchedClass}"${watchedDataAttribute}>
                <a href="/video/${video.id}">
                    ${watchedIcon}
                    <img src="${video.thumbnail}" alt="${video.name}">
                    <div class="thumbnail-title">${video.name}</div>
                    <div class="thumbnail-duration">${video.duration}</div>
                </a>
            </div>
        `;
    }

    /**
     * Create watched icon HTML
     * @returns {string} HTML for watched icon
     * @private
     * @memberof VideoThumbnailRenderer
     */
    createWatchedIcon() {
        return `
            <div class="thumbnail-watched-icon">
                <svg viewBox="0 0 24 24">
                    <path d="M9 16.2l-3.5-3.5 1.4-1.4L9 13.4l7.1-7.1 1.4 1.4z"/>
                </svg>
            </div>
        `;
    }
}

/**
 * Handles API calls for category data
 * @class CategoryApiService
 */
class CategoryApiService {
    /**
     * Create a category API service
     * @memberof CategoryApiService
     */
    constructor() {}

    /**
     * Fetch videos for a specific category and subcategory
     * @param {string|number} categoryId - The main category ID
     * @param {string|number} subcategoryId - The subcategory ID
     * @returns {Promise<Array<Object>>} Promise resolving to array of video objects
     * @async
     * @memberof CategoryApiService
     */
    async fetchCategoryVideos(categoryId, subcategoryId) {
        const endpoint = CategoryConfig.API_ENDPOINT_PATTERN
            .replace('{categoryId}', categoryId)
            .replace('{subcategoryId}', subcategoryId);

        try {
            const response = await fetch(endpoint);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`Error fetching videos for category ${categoryId}/${subcategoryId}:`, error);
            throw error;
        }
    }
}

/**
 * Manages lazy loading of category content using IntersectionObserver
 * @class CategoryLazyLoader
 */
class CategoryLazyLoader {
    /**
     * Create a category lazy loader
     * @param {CategoryPopulator} categoryPopulator - The category populator instance
     * @memberof CategoryLazyLoader
     */
    constructor(categoryPopulator) {
        /**
         * Category populator instance
         * @type {CategoryPopulator}
         */
        this.categoryPopulator = categoryPopulator;
        
        /**
         * Intersection observer instance
         * @type {IntersectionObserver}
         */
        this.observer = this.createObserver();
        
        /**
         * Set of observed category rows
         * @type {Set<HTMLElement>}
         */
        this.observedRows = new Set();
    }

    /**
     * Create and configure intersection observer
     * @returns {IntersectionObserver} Configured intersection observer
     * @private
     * @memberof CategoryLazyLoader
     */
    createObserver() {
        return new IntersectionObserver((entries) => {
            entries.forEach(entry => this.handleIntersection(entry));
        }, {
            threshold: CategoryConfig.INTERSECTION_THRESHOLD,
            rootMargin: CategoryConfig.INTERSECTION_ROOT_MARGIN
        });
    }

    /**
     * Handle intersection observer callback
     * @param {IntersectionObserverEntry} entry - The intersection observer entry
     * @private
     * @memberof CategoryLazyLoader
     */
    handleIntersection(entry) {
        if (entry.isIntersecting) {
            const categoryId = entry.target.dataset.categoryId;
            const subcategoryId = entry.target.dataset.subcategoryId;
            
            this.categoryPopulator.populateCategory(categoryId, subcategoryId);
            this.observer.unobserve(entry.target);
            this.observedRows.delete(entry.target);
        }
    }

    /**
     * Start observing category rows for lazy loading
     * @memberof CategoryLazyLoader
     */
    observeCategoryRows() {
        const categoryRows = document.querySelectorAll('.category-row');
        
        categoryRows.forEach(row => {
            if (!this.observedRows.has(row)) {
                this.observer.observe(row);
                this.observedRows.add(row);
            }
        });
    }

    /**
     * Stop observing all category rows and cleanup
     * @memberof CategoryLazyLoader
     */
    destroy() {
        this.observer.disconnect();
        this.observedRows.clear();
    }
}

/**
 * Handles TV-specific enhancements for category navigation
 * @class TVCategoryEnhancer
 */
class TVCategoryEnhancer {
    /**
     * Create a TV category enhancer
     * @memberof TVCategoryEnhancer
     */
    constructor() {
        /**
         * Whether the current device is a TV
         * @type {boolean}
         */
        this.isTV = this.detectTVDevice();
    }

    /**
     * Detect if the current device is a TV
     * @returns {boolean} True if device is detected as TV
     * @private
     * @memberof TVCategoryEnhancer
     */
    detectTVDevice() {
        return window.tvDetection?.isTV() || false;
    }

    /**
     * Apply TV-specific enhancements to category navigation
     * @memberof TVCategoryEnhancer
     */
    enhanceForTV() {
        if (!this.isTV) {
            return;
        }

        this.enhanceCategoryRows();
        this.addScrollIndicators();
    }

    /**
     * Enhance category rows for TV viewing
     * @private
     * @memberof TVCategoryEnhancer
     */
    enhanceCategoryRows() {
        const categoryRows = document.querySelectorAll('.category-row');
        
        categoryRows.forEach(row => {
            row.style.marginBottom = '3em';
            
            const title = row.querySelector('.category-title');
            if (title) {
                title.style.fontSize = '1.4em';
                title.style.marginBottom = '1em';
            }
        });
    }

    /**
     * Add visual scroll indicators for TV navigation
     * @private
     * @memberof TVCategoryEnhancer
     */
    addScrollIndicators() {
        const thumbnailContainers = document.querySelectorAll('.thumbnails');
        
        thumbnailContainers.forEach(container => {
            if (container.scrollWidth > container.clientWidth) {
                this.addScrollIndicator(container);
            }
        });
    }

    /**
     * Add scroll indicator to a specific container
     * @param {HTMLElement} container - The thumbnail container
     * @private
     * @memberof TVCategoryEnhancer
     */
    addScrollIndicator(container) {
        container.style.position = 'relative';
        
        const scrollIndicator = document.createElement('div');
        scrollIndicator.innerHTML = '→';
        scrollIndicator.style.cssText = `
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 5px 10px;
            border-radius: 50%;
            font-size: 1.2em;
            z-index: 10;
        `;
        
        container.appendChild(scrollIndicator);
    }
}

/**
 * Main controller for category population functionality
 * @class CategoryPopulator
 */
class CategoryPopulator {
    /**
     * Create a category populator instance
     * @memberof CategoryPopulator
     */
    constructor() {
        /**
         * Video thumbnail renderer instance
         * @type {VideoThumbnailRenderer}
         */
        this.thumbnailRenderer = new VideoThumbnailRenderer();
        
        /**
         * Category API service instance
         * @type {CategoryApiService}
         */
        this.apiService = new CategoryApiService();
        
        /**
         * Lazy loader instance
         * @type {CategoryLazyLoader}
         */
        this.lazyLoader = new CategoryLazyLoader(this);
        
        /**
         * TV enhancement instance
         * @type {TVCategoryEnhancer}
         */
        this.tvEnhancer = new TVCategoryEnhancer();
    }

    /**
     * Initialize the category populator
     * @memberof CategoryPopulator
     */
    init() {
        this.lazyLoader.observeCategoryRows();
        
        // Delay TV enhancements to allow categories to load
        setTimeout(() => {
            this.tvEnhancer.enhanceForTV();
        }, CategoryConfig.TV_ENHANCEMENT_DELAY);
    }

    /**
     * Populate a specific category with videos
     * @param {string|number} categoryId - The main category ID
     * @param {string|number} subcategoryId - The subcategory ID
     * @async
     * @memberof CategoryPopulator
     */
    async populateCategory(categoryId, subcategoryId) {
        try {
            const videos = await this.apiService.fetchCategoryVideos(categoryId, subcategoryId);
            const container = this.getThumbnailContainer(subcategoryId);
            
            if (!container) {
                console.warn(`Thumbnail container not found for subcategory ${subcategoryId}`);
                return;
            }

            this.thumbnailRenderer.renderThumbnails(videos, container);
            this.updateArrowVisibility(subcategoryId);
            
        } catch (error) {
            console.error(`Failed to populate category ${categoryId}/${subcategoryId}:`, error);
            this.handlePopulationError(subcategoryId, error);
        }
    }

    /**
     * Get thumbnail container element for a subcategory
     * @param {string|number} subcategoryId - The subcategory ID
     * @returns {HTMLElement|null} The thumbnail container element
     * @private
     * @memberof CategoryPopulator
     */
    getThumbnailContainer(subcategoryId) {
        return document.querySelector(`#category-${subcategoryId} .thumbnails`);
    }

    /**
     * Update arrow visibility for carousel navigation
     * @param {string|number} subcategoryId - The subcategory ID
     * @private
     * @memberof CategoryPopulator
     */
    updateArrowVisibility(subcategoryId) {
        const wrapperId = `wrapper-${subcategoryId}`;
        
        // Call global updateArrows function if it exists
        if (typeof updateArrows === 'function') {
            updateArrows(wrapperId);
        }
    }

    /**
     * Handle errors during category population
     * @param {string|number} subcategoryId - The subcategory ID
     * @param {Error} error - The error that occurred
     * @private
     * @memberof CategoryPopulator
     */
    handlePopulationError(subcategoryId, error) {
        const container = this.getThumbnailContainer(subcategoryId);
        
        if (container) {
            container.innerHTML = `
                <div class="error-message">
                    <p>Failed to load videos for this category.</p>
                    <button onclick="categoryPopulator.populateCategory('${subcategoryId}')" class="retry-button">
                        Retry
                    </button>
                </div>
            `;
        }
    }

    /**
     * Cleanup resources and observers
     * @memberof CategoryPopulator
     */
    destroy() {
        this.lazyLoader.destroy();
    }
}

// Global instance
let categoryPopulator;

/**
 * Initialize category population functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    categoryPopulator = new CategoryPopulator();
    categoryPopulator.init();
});