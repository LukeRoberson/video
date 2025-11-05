"use strict";
/**
 * @fileoverview Category population and lazy loading functionality for video manager.
 * Handles loading videos and thumbnails dynamically for each category with performance optimization.
 * Pages are organized by main category with subcategory carousels using lazy loading via IntersectionObserver API.
 */
/**
 * Configuration constants for category population
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
 */
class VideoThumbnailRenderer {
    /**
     * Create a video thumbnail renderer
     */
    constructor() { }
    /**
     * Render video thumbnails for a category
     * @param videos - Array of video objects
     * @param container - Container element for thumbnails
     */
    renderThumbnails(videos, container) {
        if (!container) {
            console.warn('Thumbnail container not found');
            return;
        }
        const thumbnailsHTML = videos.map((video) => this.createThumbnailHTML(video)).join('');
        container.innerHTML = thumbnailsHTML;
        // Apply current toggle state to newly rendered thumbnails
        this.applyCurrentToggleState(container);
    }
    /**
     * Apply current watched video toggle state to newly rendered thumbnails
     * @param container - Container element for thumbnails
     */
    applyCurrentToggleState(container) {
        // Check if watched videos should be hidden based on current toggle state
        const hideWatched = document.body.classList.contains('hide-watched');
        if (hideWatched) {
            const watchedThumbnails = container.querySelectorAll('.thumbnail--watched, [data-watched="true"]');
            watchedThumbnails.forEach((thumbnail) => {
                const htmlElement = thumbnail;
                htmlElement.style.display = 'none';
                htmlElement.setAttribute('data-hidden-by-toggle', 'true');
            });
        }
    }
    /**
     * Create HTML for a single video thumbnail
     * @param video - Video object with id, name, thumbnail, duration, watched properties
     * @returns HTML string for the thumbnail
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
     * @returns HTML for watched icon
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
 */
class CategoryApiService {
    /**
     * Create a category API service
     */
    constructor() { }
    /**
     * Fetch videos for a specific category and subcategory
     * @param categoryId - The main category ID
     * @param subcategoryId - The subcategory ID
     * @returns Promise resolving to array of video objects
     */
    async fetchCategoryVideos(categoryId, subcategoryId) {
        const endpoint = CategoryConfig.API_ENDPOINT_PATTERN
            .replace('{categoryId}', String(categoryId))
            .replace('{subcategoryId}', String(subcategoryId));
        try {
            const response = await fetch(endpoint);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return await response.json();
        }
        catch (error) {
            console.error(`Error fetching videos for category ${categoryId}/${subcategoryId}:`, error);
            throw error;
        }
    }
}
/**
 * Manages lazy loading of category content using IntersectionObserver
 */
class CategoryLazyLoader {
    /**
     * Create a category lazy loader
     * @param categoryPopulator - The category populator instance
     */
    constructor(categoryPopulator) {
        this.categoryPopulator = categoryPopulator;
        this.observer = this.createObserver();
        this.observedRows = new Set();
    }
    /**
     * Create and configure intersection observer
     * @returns Configured intersection observer
     */
    createObserver() {
        return new IntersectionObserver((entries) => {
            entries.forEach((entry) => this.handleIntersection(entry));
        }, {
            threshold: CategoryConfig.INTERSECTION_THRESHOLD,
            rootMargin: CategoryConfig.INTERSECTION_ROOT_MARGIN
        });
    }
    /**
     * Handle intersection observer callback
     * @param entry - The intersection observer entry
     */
    handleIntersection(entry) {
        if (entry.isIntersecting) {
            const target = entry.target;
            const categoryId = target.dataset.categoryId;
            const subcategoryId = target.dataset.subcategoryId;
            if (categoryId && subcategoryId) {
                this.categoryPopulator.populateCategory(categoryId, subcategoryId);
                this.observer.unobserve(entry.target);
                this.observedRows.delete(target);
            }
        }
    }
    /**
     * Start observing category rows for lazy loading
     */
    observeCategoryRows() {
        const categoryRows = document.querySelectorAll('.category-row');
        categoryRows.forEach((row) => {
            const htmlRow = row;
            if (!this.observedRows.has(htmlRow)) {
                this.observer.observe(htmlRow);
                this.observedRows.add(htmlRow);
            }
        });
    }
    /**
     * Stop observing all category rows and cleanup
     */
    destroy() {
        this.observer.disconnect();
        this.observedRows.clear();
    }
}
/**
 * Handles TV-specific enhancements for category navigation
 */
class TVCategoryEnhancer {
    /**
     * Create a TV category enhancer
     */
    constructor() {
        this.isTV = this.detectTVDevice();
    }
    /**
     * Detect if the current device is a TV
     * @returns True if device is detected as TV
     */
    detectTVDevice() {
        const tvDetection = window.tvDetection;
        return tvDetection?.isTV() || false;
    }
    /**
     * Apply TV-specific enhancements to category navigation
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
     */
    enhanceCategoryRows() {
        const categoryRows = document.querySelectorAll('.category-row');
        categoryRows.forEach((row) => {
            const htmlRow = row;
            htmlRow.style.marginBottom = '3em';
            const title = htmlRow.querySelector('.category-title');
            if (title) {
                const htmlTitle = title;
                htmlTitle.style.fontSize = '1.4em';
                htmlTitle.style.marginBottom = '1em';
            }
        });
    }
    /**
     * Add visual scroll indicators for TV navigation
     */
    addScrollIndicators() {
        const thumbnailContainers = document.querySelectorAll('.thumbnails');
        thumbnailContainers.forEach((container) => {
            const htmlContainer = container;
            if (htmlContainer.scrollWidth > htmlContainer.clientWidth) {
                this.addScrollIndicator(htmlContainer);
            }
        });
    }
    /**
     * Add scroll indicator to a specific container
     * @param container - The thumbnail container
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
 */
class CategoryPopulator {
    /**
     * Create a category populator instance
     */
    constructor() {
        this.thumbnailRenderer = new VideoThumbnailRenderer();
        this.apiService = new CategoryApiService();
        this.lazyLoader = new CategoryLazyLoader(this);
        this.tvEnhancer = new TVCategoryEnhancer();
    }
    /**
     * Initialize the category populator
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
     * @param categoryId - The main category ID
     * @param subcategoryId - The subcategory ID
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
        }
        catch (error) {
            console.error(`Failed to populate category ${categoryId}/${subcategoryId}:`, error);
            this.handlePopulationError(subcategoryId, error);
        }
    }
    /**
     * Get thumbnail container element for a subcategory
     * @param subcategoryId - The subcategory ID
     * @returns The thumbnail container element or null
     */
    getThumbnailContainer(subcategoryId) {
        return document.querySelector(`#category-${subcategoryId} .thumbnails`);
    }
    /**
     * Update arrow visibility for carousel navigation
     * @param subcategoryId - The subcategory ID
     */
    updateArrowVisibility(subcategoryId) {
        const wrapperId = `wrapper-${subcategoryId}`;
        // Call global updateArrows function if it exists
        const updateArrows = window.updateArrows;
        if (typeof updateArrows === 'function') {
            updateArrows(wrapperId);
        }
    }
    /**
     * Handle errors during category population
     * @param subcategoryId - The subcategory ID
     * @param _error - The error that occurred
     */
    handlePopulationError(subcategoryId, _error) {
        const container = this.getThumbnailContainer(subcategoryId);
        if (container) {
            container.innerHTML = `
                <div class="error-message">
                    <p>Failed to load videos for this category.</p>
                    <button onclick="categoryPopulator.populateCategory('${subcategoryId}', '${subcategoryId}')" class="retry-button">
                        Retry
                    </button>
                </div>
            `;
        }
    }
    /**
     * Cleanup resources and observers
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
document.addEventListener('DOMContentLoaded', function () {
    categoryPopulator = new CategoryPopulator();
    categoryPopulator.init();
});
//# sourceMappingURL=populateCategories.js.map