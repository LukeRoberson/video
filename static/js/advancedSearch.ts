/**
 * @fileoverview Advanced search functionality for video metadata.
 * Manages multi-select dropdowns for speakers, characters, locations, and tags.
 * Handles search form submission and result display.
 */

/**
 * Configuration constants for the advanced search functionality
 */
const SearchConfig = {
    /** Maximum items to display in dropdown for performance */
    MAX_DROPDOWN_ITEMS: 50,
    /** Maximum description length for result cards */
    MAX_DESCRIPTION_LENGTH: 100
} as const;

/**
 * Interface for multi-select item data
 */
interface MultiSelectItem {
    id: string;
    name: string;
}

/**
 * Interface for video search result
 */
interface VideoResult {
    id: string;
    name: string;
    thumbnail?: string;
    description?: string;
    duration?: string;
    watched?: boolean;
}

/**
 * Interface for multi-select data structure
 */
interface MultiSelectData {
    speakers: MultiSelectItem[];
    characters: MultiSelectItem[];
    locations: MultiSelectItem[];
    tags: MultiSelectItem[];
}

/**
 * Interface for search API response
 */
interface SearchApiResponse {
    success: boolean;
    data?: VideoResult[];
    error?: string;
}

/**
 * Interface for all selected items
 */
interface AllSelectedItems {
    speakers: MultiSelectItem[];
    characters: MultiSelectItem[];
    locations: MultiSelectItem[];
    tags: MultiSelectItem[];
}

/**
 * Manages multi-select dropdowns for speakers, characters, locations, and tags.
 * Allows users to search and select multiple items, displaying them as badges.
 */
class MultiSelectManager {
    private container: HTMLElement;
    private searchInput: HTMLInputElement;
    private dropdown: HTMLElement;
    private selectedContainer: HTMLElement;
    private hiddenInputsContainer: HTMLElement;
    private dataKey: string;
    private data: MultiSelectItem[];
    private selectedItems: Map<string, MultiSelectItem>;

    /**
     * Create a MultiSelectManager instance
     * @param containerId - The ID of the container element
     * @param inputId - The ID of the search input element
     * @param dropdownId - The ID of the dropdown element
     * @param selectedId - The ID of the selected items container
     * @param hiddenInputsId - The ID of the hidden inputs container
     * @param dataKey - The key used to identify the type of data (e.g., 'speaker', 'character')
     */
    constructor(
        containerId: string,
        inputId: string,
        dropdownId: string,
        selectedId: string,
        hiddenInputsId: string,
        dataKey: string
    ) {
        this.container = document.getElementById(containerId) as HTMLElement;
        this.searchInput = document.getElementById(inputId) as HTMLInputElement;
        this.dropdown = document.getElementById(dropdownId) as HTMLElement;
        this.selectedContainer = document.getElementById(selectedId) as HTMLElement;
        this.hiddenInputsContainer = document.getElementById(hiddenInputsId) as HTMLElement;
        this.dataKey = dataKey;
        this.data = [];
        this.selectedItems = new Map<string, MultiSelectItem>();
        
        this.setupEventListeners();
    }

    /**
     * Set the data array for this multi-select manager
     * @param data - Array of items with id and name properties
     */
    setData(data: MultiSelectItem[]): void {
        this.data = data;
        this.renderDropdown(data);
    }

    /**
     * Set up event listeners for user interactions
     */
    private setupEventListeners(): void {
        // Filter dropdown based on input
        this.searchInput.addEventListener('input', (e: Event) => {
            const target = e.target as HTMLInputElement;
            const query = target.value.toLowerCase();
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
        document.addEventListener('click', (e: Event) => {
            const target = e.target as Node;
            if (!this.container.contains(target)) {
                this.hideDropdown();
            }
        });
    }

    /**
     * Render dropdown items based on filtered data
     * @param items - Filtered items to display
     */
    private renderDropdown(items: MultiSelectItem[]): void {
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
     * @param item - Item data with id and name
     * @returns Dropdown item element
     */
    private createDropdownItem(item: MultiSelectItem): HTMLElement {
        const div = document.createElement('div');
        div.className = 'dropdown-item p-2 cursor-pointer';
        div.style.cursor = 'pointer';
        div.textContent = item.name;
        div.addEventListener('click', () => this.selectItem(item));
        return div;
    }

    /**
     * Create "no items found" message element
     * @returns No items message element
     */
    private createNoItemsMessage(): HTMLElement {
        const div = document.createElement('div');
        div.className = 'dropdown-item p-2 text-muted';
        div.textContent = 'No items found';
        return div;
    }

    /**
     * Select an item and add it to selected items
     * @param item - Item to select with id and name properties
     */
    selectItem(item: MultiSelectItem): void {
        this.selectedItems.set(item.id, item);
        this.renderSelected();
        this.searchInput.value = '';
        this.hideDropdown();
    }

    /**
     * Remove an item from selected items
     * @param itemId - ID of the item to remove
     */
    removeItem(itemId: string): void {
        this.selectedItems.delete(itemId);
        this.renderSelected();
    }

    /**
     * Render selected items as badges and update hidden form inputs
     */
    private renderSelected(): void {
        this.renderSelectedBadges();
        this.updateHiddenInputs();
    }

    /**
     * Render selected items as removable badges
     */
    private renderSelectedBadges(): void {
        this.selectedContainer.innerHTML = '';

        this.selectedItems.forEach(item => {
            const badge = this.createSelectedBadge(item);
            this.selectedContainer.appendChild(badge);
        });
    }

    /**
     * Create a badge element for a selected item
     * @param item - Selected item data
     * @returns Badge element
     */
    private createSelectedBadge(item: MultiSelectItem): HTMLElement {
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

        const closeButton = badge.querySelector('.btn-close') as HTMLButtonElement;
        closeButton.addEventListener('click', () => this.removeItem(item.id));

        return badge;
    }

    /**
     * Update hidden form inputs for selected items
     */
    private updateHiddenInputs(): void {
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
     */
    showDropdown(): void {
        this.dropdown.style.display = 'block';
    }

    /**
     * Hide the dropdown menu
     */
    hideDropdown(): void {
        this.dropdown.style.display = 'none';
    }

    /**
     * Clear all selected items and reset the search input
     */
    clear(): void {
        this.selectedItems.clear();
        this.renderSelected();
        this.searchInput.value = '';
    }

    /**
     * Get array of selected item IDs
     * @returns Array of selected item IDs
     */
    getSelectedIds(): string[] {
        return Array.from(this.selectedItems.keys());
    }

    /**
     * Get array of selected items
     * @returns Array of selected item objects
     */
    getSelectedItems(): MultiSelectItem[] {
        return Array.from(this.selectedItems.values());
    }
}

/**
 * Manages search result display and formatting
 */
class SearchResultRenderer {
    private resultsContainer: HTMLElement;

    /**
     * Create a SearchResultRenderer instance
     * @param resultsContainerId - ID of the results container element
     */
    constructor(resultsContainerId: string) {
        this.resultsContainer = document.getElementById(resultsContainerId) as HTMLElement;
    }

    /**
     * Display loading state in results container
     */
    showLoading(): void {
        this.resultsContainer.style.display = 'block';
        this.resultsContainer.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    }

    /**
     * Display error message in results container
     * @param error - Error message to display
     */
    showError(error: string): void {
        this.resultsContainer.innerHTML = `<div class="alert alert-danger">Search failed: ${error}</div>`;
    }

    /**
     * Display search results or no results message
     * @param videos - Array of video objects from search
     */
    displayResults(videos: VideoResult[]): void {
        if (!videos || videos.length === 0) {
            this.showNoResults();
            return;
        }

        const html = this.buildResultsHTML(videos);
        this.resultsContainer.innerHTML = html;
    }

    /**
     * Show no results found message
     */
    private showNoResults(): void {
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
     * @param videos - Array of video objects
     * @returns HTML string for results
     */
    private buildResultsHTML(videos: VideoResult[]): string {
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
     * @param video - Video object with properties like id, name, thumbnail, etc.
     * @returns HTML string for video card
     */
    private buildVideoCard(video: VideoResult): string {
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
     * @returns HTML for watched icon
     */
    private buildWatchedIcon(): string {
        return '<div class="thumbnail-watched-icon" style="position: absolute; top: 10px; left: 10px; z-index: 2;"><svg viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="10" fill="rgba(0,255,0,0.8)"/><path d="m9 12 2 2 4-4" stroke="white" stroke-width="2" fill="none"/></svg></div>';
    }

    /**
     * Build thumbnail HTML with watched state styling
     * @param video - Video object
     * @param watchedIcon - HTML for watched icon
     * @returns HTML for thumbnail
     */
    private buildThumbnailHTML(video: VideoResult, watchedIcon: string): string {
        const opacity = video.watched ? 'opacity: 0.6;' : '';
        return `
            ${watchedIcon}
            <img src="${video.thumbnail}" class="card-img-top" alt="${video.name}" style="${opacity}">
        `;
    }

    /**
     * Build description HTML with length limit
     * @param description - Video description
     * @returns HTML for description
     */
    private buildDescriptionHTML(description?: string): string {
        if (!description) return '';

        const truncated = description.length > SearchConfig.MAX_DESCRIPTION_LENGTH 
            ? description.substring(0, SearchConfig.MAX_DESCRIPTION_LENGTH) + '...' 
            : description;

        return `<p class="card-text">${truncated}</p>`;
    }
}

/**
 * Main controller for advanced search functionality
 */
class AdvancedSearchController {
    private speakerManager: MultiSelectManager;
    private characterManager: MultiSelectManager;
    private locationManager: MultiSelectManager;
    private tagManager: MultiSelectManager;
    private resultRenderer: SearchResultRenderer;
    private searchForm: HTMLFormElement | null;

    /**
     * Create an AdvancedSearchController instance
     */
    constructor() {
        this.speakerManager = null!;
        this.characterManager = null!;
        this.locationManager = null!;
        this.tagManager = null!;
        this.resultRenderer = new SearchResultRenderer('search-results');
        this.searchForm = null;
    }

    /**
     * Initialize the advanced search controller
     */
    init(): void {
        this.initializeManagers();
        this.setupEventListeners();
        this.loadMultiSelectData();
    }

    /**
     * Initialize all multi-select managers
     */
    private initializeManagers(): void {
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
     */
    private setupEventListeners(): void {
        this.searchForm = document.getElementById('advanced-search-form') as HTMLFormElement | null;

        // Clear form handler
        const clearButton = document.getElementById('clear-form');
        if (clearButton) {
            clearButton.addEventListener('click', () => this.clearForm());
        }

        // Form submission handler
        if (this.searchForm) {
            this.searchForm.addEventListener('submit', (e: Event) => {
                e.preventDefault();
                this.performAdvancedSearch();
            });
        }
    }

    /**
     * Load data for all multi-select dropdowns
     */
    private loadMultiSelectData(): void {
        try {
            const dataElement = document.getElementById('multi-select-data');
            if (!dataElement) {
                throw new Error('Multi-select data element not found');
            }

            const data: MultiSelectData = JSON.parse(dataElement.textContent || '{}');

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
     */
    clearForm(): void {
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
     */
    async performAdvancedSearch(): Promise<void> {
        if (!this.searchForm) {
            console.error('Search form not found');
            return;
        }

        const formData = new FormData(this.searchForm);
        const params = this.buildSearchParams(formData);

        try {
            this.resultRenderer.showLoading();
            const data = await this.executeSearch(params);

            if (data.success && data.data) {
                this.resultRenderer.displayResults(data.data);
            } else {
                this.resultRenderer.showError(data.error || 'Unknown error');
            }
        } catch (error) {
            console.error('Search error:', error);
            this.resultRenderer.showError('An error occurred during search.');
        }
    }

    /**
     * Build URL search parameters from form data
     * @param formData - Form data to process
     * @returns URL search parameters
     */
    private buildSearchParams(formData: FormData): URLSearchParams {
        const params = new URLSearchParams();

        for (const [key, value] of formData.entries()) {
            const stringValue = value.toString();
            if (stringValue.trim()) {
                params.append(key, stringValue);
            }
        }

        return params;
    }

    /**
     * Execute the search API call
     * @param params - Search parameters
     * @returns Search response data
     */
    private async executeSearch(params: URLSearchParams): Promise<SearchApiResponse> {
        const response = await fetch(`/api/search/advanced?${params.toString()}`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Get all selected items from all managers
     * @returns Object containing arrays of selected items by type
     */
    getAllSelectedItems(): AllSelectedItems {
        return {
            speakers: this.speakerManager.getSelectedItems(),
            characters: this.characterManager.getSelectedItems(),
            locations: this.locationManager.getSelectedItems(),
            tags: this.tagManager.getSelectedItems()
        };
    }
}

// Global controller instance
let advancedSearchController: AdvancedSearchController;

/**
 * Initialize advanced search functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    advancedSearchController = new AdvancedSearchController();
    advancedSearchController.init();
});
