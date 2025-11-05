/**
 * @fileoverview Advanced search functionality for video metadata.
 * Manages multi-select dropdowns for speakers, characters, locations, and tags.
 * Handles search form submission and result display.
 */
/**
 * Configuration constants for the advanced search functionality
 */
declare const SearchConfig: {
    /** Maximum items to display in dropdown for performance */
    readonly MAX_DROPDOWN_ITEMS: 50;
    /** Maximum description length for result cards */
    readonly MAX_DESCRIPTION_LENGTH: 100;
};
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
declare class MultiSelectManager {
    private container;
    private searchInput;
    private dropdown;
    private selectedContainer;
    private hiddenInputsContainer;
    private dataKey;
    private data;
    private selectedItems;
    /**
     * Create a MultiSelectManager instance
     * @param containerId - The ID of the container element
     * @param inputId - The ID of the search input element
     * @param dropdownId - The ID of the dropdown element
     * @param selectedId - The ID of the selected items container
     * @param hiddenInputsId - The ID of the hidden inputs container
     * @param dataKey - The key used to identify the type of data (e.g., 'speaker', 'character')
     */
    constructor(containerId: string, inputId: string, dropdownId: string, selectedId: string, hiddenInputsId: string, dataKey: string);
    /**
     * Set the data array for this multi-select manager
     * @param data - Array of items with id and name properties
     */
    setData(data: MultiSelectItem[]): void;
    /**
     * Set up event listeners for user interactions
     */
    private setupEventListeners;
    /**
     * Render dropdown items based on filtered data
     * @param items - Filtered items to display
     */
    private renderDropdown;
    /**
     * Create a single dropdown item element
     * @param item - Item data with id and name
     * @returns Dropdown item element
     */
    private createDropdownItem;
    /**
     * Create "no items found" message element
     * @returns No items message element
     */
    private createNoItemsMessage;
    /**
     * Select an item and add it to selected items
     * @param item - Item to select with id and name properties
     */
    selectItem(item: MultiSelectItem): void;
    /**
     * Remove an item from selected items
     * @param itemId - ID of the item to remove
     */
    removeItem(itemId: string): void;
    /**
     * Render selected items as badges and update hidden form inputs
     */
    private renderSelected;
    /**
     * Render selected items as removable badges
     */
    private renderSelectedBadges;
    /**
     * Create a badge element for a selected item
     * @param item - Selected item data
     * @returns Badge element
     */
    private createSelectedBadge;
    /**
     * Update hidden form inputs for selected items
     */
    private updateHiddenInputs;
    /**
     * Show the dropdown menu
     */
    showDropdown(): void;
    /**
     * Hide the dropdown menu
     */
    hideDropdown(): void;
    /**
     * Clear all selected items and reset the search input
     */
    clear(): void;
    /**
     * Get array of selected item IDs
     * @returns Array of selected item IDs
     */
    getSelectedIds(): string[];
    /**
     * Get array of selected items
     * @returns Array of selected item objects
     */
    getSelectedItems(): MultiSelectItem[];
}
/**
 * Manages search result display and formatting
 */
declare class SearchResultRenderer {
    private resultsContainer;
    /**
     * Create a SearchResultRenderer instance
     * @param resultsContainerId - ID of the results container element
     */
    constructor(resultsContainerId: string);
    /**
     * Display loading state in results container
     */
    showLoading(): void;
    /**
     * Display error message in results container
     * @param error - Error message to display
     */
    showError(error: string): void;
    /**
     * Display search results or no results message
     * @param videos - Array of video objects from search
     */
    displayResults(videos: VideoResult[]): void;
    /**
     * Show no results found message
     */
    private showNoResults;
    /**
     * Build HTML for search results
     * @param videos - Array of video objects
     * @returns HTML string for results
     */
    private buildResultsHTML;
    /**
     * Build HTML for a single video card
     * @param video - Video object with properties like id, name, thumbnail, etc.
     * @returns HTML string for video card
     */
    private buildVideoCard;
    /**
     * Build watched icon HTML
     * @returns HTML for watched icon
     */
    private buildWatchedIcon;
    /**
     * Build thumbnail HTML with watched state styling
     * @param video - Video object
     * @param watchedIcon - HTML for watched icon
     * @returns HTML for thumbnail
     */
    private buildThumbnailHTML;
    /**
     * Build description HTML with length limit
     * @param description - Video description
     * @returns HTML for description
     */
    private buildDescriptionHTML;
}
/**
 * Main controller for advanced search functionality
 */
declare class AdvancedSearchController {
    private speakerManager;
    private characterManager;
    private locationManager;
    private tagManager;
    private searchForm;
    /**
     * Create an AdvancedSearchController instance
     */
    constructor();
    /**
     * Initialize the advanced search controller
     */
    init(): void;
    /**
     * Initialize all multi-select managers
     */
    private initializeManagers;
    /**
     * Set up event listeners for form interactions
     */
    private setupEventListeners;
    /**
     * Load data for all multi-select dropdowns
     */
    private loadMultiSelectData;
    /**
     * Restore selected items from URL query parameters
     * @param data - Available data for all multi-select managers
     */
    private restoreSelectedItems;
    /**
     * Clear all form inputs and selected items
     */
    clearForm(): void;
    /**
     * Get all selected items from all managers
     * @returns Object containing arrays of selected items by type
     */
    getAllSelectedItems(): AllSelectedItems;
}
declare let advancedSearchController: AdvancedSearchController;
//# sourceMappingURL=advancedSearch.d.ts.map