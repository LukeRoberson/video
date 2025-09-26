/**
 * @fileoverview Advanced search functionality for video metadata.
 * Manages multi-select dropdowns for speakers, characters, locations, and tags.
 * Handles search form submission and result display.
 */

/**
 * Configuration constants for the advanced search functionality
 * @readonly
 * @enum {number}
 */
const SearchConfig = {
    /** Maximum items to display in dropdown for performance */
    MAX_DROPDOWN_ITEMS: 50,
    /** Maximum description length for result cards */
    MAX_DESCRIPTION_LENGTH: 100
};

/**
 * Manages multi-select dropdowns for speakers, characters, locations, and tags.
 * Allows users to search and select multiple items, displaying them as badges.
 * 
 * @class MultiSelectManager
 */
class MultiSelectManager {
    /**
     * Create a MultiSelectManager instance
     * @param {string} containerId - The ID of the container element
     * @param {string} inputId - The ID of the search input element
     * @param {string} dropdownId - The ID of the dropdown element
     * @param {string} selectedId - The ID of the selected items container
     * @param {string} hiddenInputsId - The ID of the hidden inputs container
     * @param {string} dataKey - The key used to identify the type of data (e.g., 'speaker', 'character')
     * @memberof MultiSelectManager
     */
    constructor(containerId, inputId, dropdownId, selectedId, hiddenInputsId, dataKey) {
        /**
         * Main container element
         * @type {HTMLElement}
         */
        this.container = document.getElementById(containerId);
        
        /**
         * Search input element
         * @type {HTMLInputElement}
         */
        this.searchInput = document.getElementById(inputId);
        
        /**
         * Dropdown container element
         * @type {HTMLElement}
         */
        this.dropdown = document.getElementById(dropdownId);
        
        /**
         * Container for selected item badges
         * @type {HTMLElement}
         */
        this.selectedContainer = document.getElementById(selectedId);
        
        /**
         * Container for hidden form inputs
         * @type {HTMLElement}
         */
        this.hiddenInputsContainer = document.getElementById(hiddenInputsId);
        
        /**
         * Data key identifier for this manager type
         * @type {string}
         */
        this.dataKey = dataKey;
        
        /**
         * Array of available items for selection
         * @type {Array<Object>}
         */
        this.data = [];
        
        /**
         * Map of currently selected items (id -> item)
         * @type {Map<string, Object>}
         */
        this.selectedItems = new Map();
        
        this.setupEventListeners();
    }
    
    /**
     * Set the data array for this multi-select manager
     * @param {Array<Object>} data - Array of items with id and name properties
     * @memberof MultiSelectManager
     */
    setData(data) {
        this.data = data;
        this.renderDropdown(data);
    }
    
    /**
     * Set up event listeners for user interactions
     * @private
     * @memberof MultiSelectManager
     */
    setupEventListeners() {
        // Filter dropdown based on input
        this.searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const filtered = this.data.filter(item => 
                item.name.toLowerCase().includes(query)
            );
            this.renderDropdown(filtered);
            this.showDropdown();
        });
        
        // Show dropdown on focus
        this.searchInput.addEventListener('focus', () => {
            this.renderDropdown(this.data);
            this.showDropdown();
        });
        
        // Hide dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.hideDropdown();
            }
        });
    }
    
    /**
     * Render dropdown items based on filtered data
     * @param {Array<Object>} items - Filtered items to display
     * @private
     * @memberof MultiSelectManager
     */
    renderDropdown(items) {
        this.dropdown.innerHTML = '';
        
        // Limit items for performance
        const limitedItems = items.slice(0, SearchConfig.MAX_DROPDOWN_ITEMS);
        
        limitedItems.forEach(item => {
            if (!this.selectedItems.has(item.id)) {
                const dropdownItem = this.createDropdownItem(item);
                this.dropdown.appendChild(dropdownItem);
            }
        });
        
        // Show "no items found" message if needed
        if (limitedItems.length === 0) {
            this.dropdown.appendChild(this.createNoItemsMessage());
        }
    }
    
    /**
     * Create a single dropdown item element
     * @param {Object} item - Item data with id and name
     * @returns {HTMLElement} Dropdown item element
     * @private
     * @memberof MultiSelectManager
     */
    createDropdownItem(item) {
        const div = document.createElement('div');
        div.className = 'dropdown-item p-2 cursor-pointer';
        div.style.cursor = 'pointer';
        div.textContent = item.name;
        div.addEventListener('click', () => this.selectItem(item));
        return div;
    }
    
    /**
     * Create "no items found" message element
     * @returns {HTMLElement} No items message element
     * @private
     * @memberof MultiSelectManager
     */
    createNoItemsMessage() {
        const div = document.createElement('div');
        div.className = 'dropdown-item p-2 text-muted';
        div.textContent = 'No items found';
        return div;
    }
    
    /**
     * Select an item and add it to selected items
     * @param {Object} item - Item to select with id and name properties
     * @memberof MultiSelectManager
     */
    selectItem(item) {
        this.selectedItems.set(item.id, item);
        this.renderSelected();
        this.searchInput.value = '';
        this.hideDropdown();
    }
    
    /**
     * Remove an item from selected items
     * @param {string} itemId - ID of the item to remove
     * @memberof MultiSelectManager
     */
    removeItem(itemId) {
        this.selectedItems.delete(itemId);
        this.renderSelected();
    }
    
    /**
     * Render selected items as badges and update hidden form inputs
     * @private
     * @memberof MultiSelectManager
     */
    renderSelected() {
        this.renderSelectedBadges();
        this.updateHiddenInputs();
    }
    
    /**
     * Render selected items as removable badges
     * @private
     * @memberof MultiSelectManager
     */
    renderSelectedBadges() {
        this.selectedContainer.innerHTML = '';

        this.selectedItems.forEach(item => {
            const badge = this.createSelectedBadge(item);
            this.selectedContainer.appendChild(badge);
        });
    }
    
    /**
     * Create a badge element for a selected item
     * @param {Object} item - Selected item data
     * @returns {HTMLElement} Badge element
     * @private
     * @memberof MultiSelectManager
     */
    createSelectedBadge(item) {
        const badge = document.createElement('span');
        badge.className = 'badge bg-primary me-1 mb-1';
        badge.innerHTML = `
            ${item.name} 
            <button type="button"
                    class="btn-close btn-close-white ms-1" 
                    style="font-size: 0.7em;" 
                    data-item-id="${item.id}" 
                    data-manager="${this.dataKey}">
            </button>
        `;
        
        const closeButton = badge.querySelector('.btn-close');
        closeButton.addEventListener('click', () => this.removeItem(item.id));
        
        return badge;
    }
    
    /**
     * Update hidden form inputs for selected items
     * @private
     * @memberof MultiSelectManager
     */
    updateHiddenInputs() {
        this.hiddenInputsContainer.innerHTML = '';
        
        this.selectedItems.forEach(item => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = `${this.dataKey}_ids`;
            input.value = item.id;
            this.hiddenInputsContainer.appendChild(input);
        });
    }

    /**
     * Show the dropdown menu
     * @memberof MultiSelectManager
     */
    showDropdown() {
        this.dropdown.style.display = 'block';
    }
    
    /**
     * Hide the dropdown menu
     * @memberof MultiSelectManager
     */
    hideDropdown() {
        this.dropdown.style.display = 'none';
    }
    
    /**
     * Clear all selected items and reset the search input
     * @memberof MultiSelectManager
     */
    clear() {
        this.selectedItems.clear();
        this.renderSelected();
        this.searchInput.value = '';
    }

    /**
     * Get array of selected item IDs
     * @returns {Array<string>} Array of selected item IDs
     * @memberof MultiSelectManager
     */
    getSelectedIds() {
        return Array.from(this.selectedItems.keys());
    }

    /**
     * Get array of selected items
     * @returns {Array<Object>} Array of selected item objects
     * @memberof MultiSelectManager
     */
    getSelectedItems() {
        return Array.from(this.selectedItems.values());
    }
}

/**
 * Manages search result display and formatting
 * @class SearchResultRenderer
 */
class SearchResultRenderer {
    /**
     * Create a SearchResultRenderer instance
     * @param {string} resultsContainerId - ID of the results container element
     * @memberof SearchResultRenderer
     */
    constructor(resultsContainerId) {
        /**
         * Results container element
         * @type {HTMLElement}
         */
        this.resultsContainer = document.getElementById(resultsContainerId);
    }

    /**
     * Display loading state in results container
     * @memberof SearchResultRenderer
     */
    showLoading() {
        this.resultsContainer.style.display = 'block';
        this.resultsContainer.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    }

    /**
     * Display error message in results container
     * @param {string} error - Error message to display
     * @memberof SearchResultRenderer
     */
    showError(error) {
        this.resultsContainer.innerHTML = `<div class="alert alert-danger">Search failed: ${error}</div>`;
    }

    /**
     * Display search results or no results message
     * @param {Array<Object>} videos - Array of video objects from search
     * @memberof SearchResultRenderer
     */
    displayResults(videos) {
        if (!videos || videos.length === 0) {
            this.showNoResults();
            return;
        }

        const html = this.buildResultsHTML(videos);
        this.resultsContainer.innerHTML = html;
    }

    /**
     * Show no results found message
     * @private
     * @memberof SearchResultRenderer
     */
    showNoResults() {
        this.resultsContainer.innerHTML = `
            <div class="card bg-dark border-secondary">
                <div class="card-body text-center py-5">
                    <i class="fas fa-search fa-3x text-light mb-3"></i>
                    <h4 class="text-white">No videos found</h4>
                    <p class="text-light">Try adjusting your search criteria</p>
                </div>
            </div>
        `;
    }

    /**
     * Build HTML for search results
     * @param {Array<Object>} videos - Array of video objects
     * @returns {string} HTML string for results
     * @private
     * @memberof SearchResultRenderer
     */
    buildResultsHTML(videos) {
        let html = `
            <h4 class="text-white mb-3">Search Results (${videos.length} videos found)</h4>
            <div class="row">
        `;
        
        videos.forEach(video => {
            html += this.buildVideoCard(video);
        });
        
        html += '</div>';
        return html;
    }

    /**
     * Build HTML for a single video card
     * @param {Object} video - Video object with properties like id, name, thumbnail, etc.
     * @returns {string} HTML string for video card
     * @private
     * @memberof SearchResultRenderer
     */
    buildVideoCard(video) {
        const watchedClass = video.watched ? ' watched' : '';
        const watchedIcon = video.watched ? this.buildWatchedIcon() : '';
        const thumbnail = video.thumbnail ? this.buildThumbnailHTML(video, watchedIcon) : '';
        const description = this.buildDescriptionHTML(video.description);
        const duration = video.duration ? `<small class="text-light"><i class="fas fa-clock"></i> ${video.duration}</small>` : '';

        return `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card bg-dark text-white h-100 border-secondary${watchedClass}" style="position: relative;">
                    <a href="/video/${video.id}" class="text-decoration-none text-white">
                        ${thumbnail}
                        <div class="card-body">
                            <h5 class="card-title">${video.name}</h5>
                            ${description}
                            ${duration}
                        </div>
                    </a>
                </div>
            </div>
        `;
    }

    /**
     * Build watched icon HTML
     * @returns {string} HTML for watched icon
     * @private
     * @memberof SearchResultRenderer
     */
    buildWatchedIcon() {
        return '<div class="thumbnail-watched-icon" style="position: absolute; top: 10px; left: 10px; z-index: 2;"><svg viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="10" fill="rgba(0,255,0,0.8)"/><path d="m9 12 2 2 4-4" stroke="white" stroke-width="2" fill="none"/></svg></div>';
    }

    /**
     * Build thumbnail HTML with watched state styling
     * @param {Object} video - Video object
     * @param {string} watchedIcon - HTML for watched icon
     * @returns {string} HTML for thumbnail
     * @private
     * @memberof SearchResultRenderer
     */
    buildThumbnailHTML(video, watchedIcon) {
        const opacity = video.watched ? 'opacity: 0.6;' : '';
        return `
            ${watchedIcon}
            <img src="${video.thumbnail}" class="card-img-top" alt="${video.name}" style="${opacity}">
        `;
    }

    /**
     * Build description HTML with length limit
     * @param {string} description - Video description
     * @returns {string} HTML for description
     * @private
     * @memberof SearchResultRenderer
     */
    buildDescriptionHTML(description) {
        if (!description) return '';
        
        const truncated = description.length > SearchConfig.MAX_DESCRIPTION_LENGTH 
            ? description.substring(0, SearchConfig.MAX_DESCRIPTION_LENGTH) + '...' 
            : description;
            
        return `<p class="card-text">${truncated}</p>`;
    }
}

/**
 * Main controller for advanced search functionality
 * @class AdvancedSearchController
 */
class AdvancedSearchController {
    /**
     * Create an AdvancedSearchController instance
     * @memberof AdvancedSearchController
     */
    constructor() {
        /**
         * Multi-select manager for speakers
         * @type {MultiSelectManager}
         */
        this.speakerManager = null;
        
        /**
         * Multi-select manager for characters
         * @type {MultiSelectManager}
         */
        this.characterManager = null;
        
        /**
         * Multi-select manager for locations
         * @type {MultiSelectManager}
         */
        this.locationManager = null;
        
        /**
         * Multi-select manager for tags
         * @type {MultiSelectManager}
         */
        this.tagManager = null;

        /**
         * Search result renderer instance
         * @type {SearchResultRenderer}
         */
        this.resultRenderer = new SearchResultRenderer('search-results');

        /**
         * Advanced search form element
         * @type {HTMLFormElement}
         */
        this.searchForm = null;
    }

    /**
     * Initialize the advanced search controller
     * @memberof AdvancedSearchController
     */
    init() {
        this.initializeManagers();
        this.setupEventListeners();
        this.loadMultiSelectData();
    }

    /**
     * Initialize all multi-select managers
     * @private
     * @memberof AdvancedSearchController
     */
    initializeManagers() {
        this.speakerManager = new MultiSelectManager(
            'speaker-container', 'speaker-search', 'speaker-dropdown', 
            'selected-speakers', 'speaker-inputs', 'speaker'
        );
        
        this.characterManager = new MultiSelectManager(
            'character-container', 'character-search', 'character-dropdown', 
            'selected-characters', 'character-inputs', 'character'
        );
        
        this.locationManager = new MultiSelectManager(
            'location-container', 'location-search', 'location-dropdown', 
            'selected-locations', 'location-inputs', 'location'
        );
        
        this.tagManager = new MultiSelectManager(
            'tag-container', 'tag-search', 'tag-dropdown', 
            'selected-tags', 'tag-inputs', 'tag'
        );
    }

    /**
     * Set up event listeners for form interactions
     * @private
     * @memberof AdvancedSearchController
     */
    setupEventListeners() {
        this.searchForm = document.getElementById('advanced-search-form');
        
        // Clear form handler
        const clearButton = document.getElementById('clear-form');
        if (clearButton) {
            clearButton.addEventListener('click', () => this.clearForm());
        }
        
        // Form submission handler
        if (this.searchForm) {
            this.searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.performAdvancedSearch();
            });
        }
    }

    /**
     * Load data for all multi-select dropdowns
     * @private
     * @memberof AdvancedSearchController
     */
    loadMultiSelectData() {
        try {
            const dataElement = document.getElementById('multi-select-data');
            if (!dataElement) {
                throw new Error('Multi-select data element not found');
            }

            const data = JSON.parse(dataElement.textContent);
            
            this.speakerManager.setData(data.speakers || []);
            this.characterManager.setData(data.characters || []);
            this.locationManager.setData(data.locations || []);
            this.tagManager.setData(data.tags || []);
            
        } catch (error) {
            console.error('Error loading multi-select data:', error);
            // Set empty arrays as fallback
            this.speakerManager.setData([]);
            this.characterManager.setData([]);
            this.locationManager.setData([]);
            this.tagManager.setData([]);
        }
    }

    /**
     * Clear all form inputs and selected items
     * @memberof AdvancedSearchController
     */
    clearForm() {
        if (this.searchForm) {
            this.searchForm.reset();
        }
        
        this.speakerManager.clear();
        this.characterManager.clear();
        this.locationManager.clear();
        this.tagManager.clear();
    }

    /**
     * Perform advanced search based on form data
     * @async
     * @memberof AdvancedSearchController
     */
    async performAdvancedSearch() {
        if (!this.searchForm) {
            console.error('Search form not found');
            return;
        }

        const formData = new FormData(this.searchForm);
        const params = this.buildSearchParams(formData);
        
        try {
            this.resultRenderer.showLoading();
            const data = await this.executeSearch(params);
            
            if (data.success) {
                this.resultRenderer.displayResults(data.data);
            } else {
                this.resultRenderer.showError(data.error);
            }
        } catch (error) {
            console.error('Search error:', error);
            this.resultRenderer.showError('An error occurred during search.');
        }
    }

    /**
     * Build URL search parameters from form data
     * @param {FormData} formData - Form data to process
     * @returns {URLSearchParams} URL search parameters
     * @private
     * @memberof AdvancedSearchController
     */
    buildSearchParams(formData) {
        const params = new URLSearchParams();
        
        for (let [key, value] of formData.entries()) {
            if (value.trim()) {
                params.append(key, value);
            }
        }
        
        return params;
    }

    /**
     * Execute the search API call
     * @param {URLSearchParams} params - Search parameters
     * @returns {Promise<Object>} Search response data
     * @private
     * @memberof AdvancedSearchController
     */
    async executeSearch(params) {
        const response = await fetch(`/api/search/advanced?${params.toString()}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    }

    /**
     * Get all selected items from all managers
     * @returns {Object} Object containing arrays of selected items by type
     * @memberof AdvancedSearchController
     */
    getAllSelectedItems() {
        return {
            speakers: this.speakerManager.getSelectedItems(),
            characters: this.characterManager.getSelectedItems(),
            locations: this.locationManager.getSelectedItems(),
            tags: this.tagManager.getSelectedItems()
        };
    }
}

// Global controller instance
let advancedSearchController;

/**
 * Initialize advanced search functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    advancedSearchController = new AdvancedSearchController();
    advancedSearchController.init();
});