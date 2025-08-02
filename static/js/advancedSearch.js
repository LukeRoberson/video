/**
 * advancedSearch.js
 * 
 * Manages advanced search functionality.
 * This is where we search based on metadata like tags.
 */


/**
 * MultiSelectManager
 * 
 * Handles multi-select dropdowns for speakers, characters, locations, and tags.
 * Allows users to search and select multiple items, displaying them as badges.
 * 
 * This is instantiated for each type of data (speaker, character, location, tag).
 */
class MultiSelectManager {
    /**
     * Initializes the MultiSelectManager with the necessary elements.
     * @param {string} containerId - The ID of the container element.
     * @param {string} inputId - The ID of the search input element.
     * @param {string} dropdownId - The ID of the dropdown element.
     * @param {string} selectedId - The ID of the selected items container.
     * @param {string} hiddenInputsId - The ID of the hidden inputs container.
     * @param {string} dataKey - The key used to identify the type of data (e.g., 'speaker', 'character').
     */
    constructor(containerId, inputId, dropdownId, selectedId, hiddenInputsId, dataKey) {
        this.container = document.getElementById(containerId);
        this.searchInput = document.getElementById(inputId);
        this.dropdown = document.getElementById(dropdownId);
        this.selectedContainer = document.getElementById(selectedId);
        this.hiddenInputsContainer = document.getElementById(hiddenInputsId);
        this.dataKey = dataKey;
        this.data = [];
        this.selectedItems = new Map();
        
        this.setupEventListeners();
    }
    
    /**
     * Sets the data for the multi-select manager.
     * @param {Array} data - The array of items to display in the dropdown.
     */
    setData(data) {
        this.data = data;
        this.renderDropdown(data);
    }
    
    /**
     * Sets up event listeners for the search input and dropdown.
     */
    setupEventListeners() {
        // Hide dropdown initially
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
        
        // Hide dropdown on defocus
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.hideDropdown();
            }
        });
    }
    
    /**
     * Adds items to the dropdown.
     * @param {*} items 
     */
    renderDropdown(items) {
        this.dropdown.innerHTML = '';
        items.slice(0, 50).forEach(item => { // Limit to 50 for performance
            if (!this.selectedItems.has(item.id)) {
                const div = document.createElement('div');
                div.className = 'dropdown-item p-2 cursor-pointer';
                div.style.cursor = 'pointer';
                div.textContent = item.name;
                div.addEventListener('click', () => this.selectItem(item));
                this.dropdown.appendChild(div);
            }
        });
        
        if (items.length === 0) {
            const div = document.createElement('div');
            div.className = 'dropdown-item p-2 text-muted';
            div.textContent = 'No items found';
            this.dropdown.appendChild(div);
        }
    }
    
    /**
     * Selects an item and adds it to the selected items.
     * @param {Object} item - The item to select.
     */
    selectItem(item) {
        this.selectedItems.set(item.id, item);
        this.renderSelected();
        this.searchInput.value = '';
        this.hideDropdown();
    }
    
    /**
     * Removes an item from the selected items.
     * @param {string} itemId - The ID of the item to remove.
     */
    removeItem(itemId) {
        this.selectedItems.delete(itemId);
        this.renderSelected();
    }
    
    /**
     * Renders the selected items as badges and updates hidden inputs.
     */
    renderSelected() {
        // Render selected badges
        this.selectedContainer.innerHTML = '';

        // Create badges for each selected item
        this.selectedItems.forEach(item => {
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
            
            // Add event listener to the close button
            const closeButton = badge.querySelector('.btn-close');
            closeButton.addEventListener('click', () => this.removeItem(item.id));
            
            this.selectedContainer.appendChild(badge);
        });
        
        // Update hidden inputs
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
     * Shows the dropdown menu.
     */
    showDropdown() {
        this.dropdown.style.display = 'block';
    }
    
    /**
     * Hides the dropdown menu.
     */
    hideDropdown() {
        this.dropdown.style.display = 'none';
    }
    
    /**
     * Clears the selected items and resets the search input.
     */
    clear() {
        this.selectedItems.clear();
        this.renderSelected();
        this.searchInput.value = '';
    }
}

// Initialize managers
let speakerManager, characterManager, locationManager, tagManager;

/**
 * Document ready function
 * 
 * Initializes the multi-select managers and sets up event listeners.
 * Handles form submission and clearing.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Create the speaker manager
    speakerManager = new MultiSelectManager(
        'speaker-container', 'speaker-search', 'speaker-dropdown', 
        'selected-speakers', 'speaker-inputs', 'speaker'
    );
    
    // Create the character manager
    characterManager = new MultiSelectManager(
        'character-container', 'character-search', 'character-dropdown', 
        'selected-characters', 'character-inputs', 'character'
    );
    
    // Create the location manager
    locationManager = new MultiSelectManager(
        'location-container', 'location-search', 'location-dropdown', 
        'selected-locations', 'location-inputs', 'location'
    );
    
    // Create the tag manager
    tagManager = new MultiSelectManager(
        'tag-container', 'tag-search', 'tag-dropdown', 
        'selected-tags', 'tag-inputs', 'tag'
    );
    
    // Load data into managers
    loadMultiSelectData();
    
    // Clear form handler
    document.getElementById('clear-form').addEventListener('click', function() {
        document.getElementById('advanced-search-form').reset();
        speakerManager.clear();
        characterManager.clear();
        locationManager.clear();
        tagManager.clear();
    });
    
    // Form submission handler
    document.getElementById('advanced-search-form').addEventListener('submit', function(e) {
        e.preventDefault();
        performAdvancedSearch();
    });
});

/**
 * Loads data for multi-select dropdowns from a JSON script tag.
 * Sets the data for each manager (speakers, characters, locations, tags).
 */
function loadMultiSelectData() {
    try {
        // Get data from the JSON script tag
        const dataElement = document.getElementById('multi-select-data');
        const data = JSON.parse(dataElement.textContent);
        
        speakerManager.setData(data.speakers);
        characterManager.setData(data.characters);
        locationManager.setData(data.locations);
        tagManager.setData(data.tags);
        
    } catch (error) {
        console.error('Error loading data:', error);
        // Fallback to empty arrays
        speakerManager.setData([]);
        characterManager.setData([]);
        locationManager.setData([]);
        tagManager.setData([]);
    }
}

/**
 * Performs the advanced search based on the form data.
 * Collects form inputs, makes an API call, and displays results.
 */
async function performAdvancedSearch() {
    const formData = new FormData(document.getElementById('advanced-search-form'));
    const params = new URLSearchParams();
    
    // Collect form data
    for (let [key, value] of formData.entries()) {
        if (value.trim()) {
            params.append(key, value);
        }
    }
    
    try {
        // Show loading state
        const resultsDiv = document.getElementById('search-results');
        resultsDiv.style.display = 'block';
        resultsDiv.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
        
        // Make API call
        const response = await fetch(`/api/search/advanced?${params.toString()}`);
        const data = await response.json();
        
        if (data.success) {
            displaySearchResults(data.data);
        } else {
            resultsDiv.innerHTML = '<div class="alert alert-danger">Search failed: ' + data.error + '</div>';
        }
    } catch (error) {
        console.error('Search error:', error);
        document.getElementById('search-results').innerHTML = 
            '<div class="alert alert-danger">An error occurred during search.</div>';
    }
}

/**
 * Displays the search results in the results div.
 * 
 * @param {Array} videos - The array of video objects returned from the search.
 */
function displaySearchResults(videos) {
    const resultsDiv = document.getElementById('search-results');
    
    // If no videos found, display a message
    if (!videos || videos.length === 0) {
        resultsDiv.innerHTML = `
            <div class="card bg-dark border-secondary">
                <div class="card-body text-center py-5">
                    <i class="fas fa-search fa-3x text-light mb-3"></i>
                    <h4 class="text-white">No videos found</h4>
                    <p class="text-light">Try adjusting your search criteria</p>
                </div>
            </div>
        `;
        return;
    }
    
    // Show how many videos were found
    let html = `
        <h4 class="text-white mb-3">Search Results (${videos.length} videos found)</h4>
        <div class="row">
    `;
    
    // Loop through videos and create cards
    videos.forEach(video => {
        const watchedClass = video.watched ? ' watched' : '';
        const watchedIcon = video.watched ? 
            '<div class="thumbnail-watched-icon" style="position: absolute; top: 10px; left: 10px; z-index: 2;"><svg viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="10" fill="rgba(0,255,0,0.8)"/><path d="m9 12 2 2 4-4" stroke="white" stroke-width="2" fill="none"/></svg></div>' : '';
        
        html += `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card bg-dark text-white h-100 border-secondary${watchedClass}" style="position: relative;">
                    <a href="/video/${video.id}" class="text-decoration-none text-white">
                        ${video.thumbnail ? `
                            ${watchedIcon}
                            <img src="${video.thumbnail}" class="card-img-top" alt="${video.name}" style="${video.watched ? 'opacity: 0.6;' : ''}">
                        ` : ''}
                        <div class="card-body">
                            <h5 class="card-title">${video.name}</h5>
                            ${video.description ? `<p class="card-text">${video.description.length > 100 ? video.description.substring(0, 100) + '...' : video.description}</p>` : ''}
                            ${video.duration ? `<small class="text-light"><i class="fas fa-clock"></i> ${video.duration}</small>` : ''}
                        </div>
                    </a>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    resultsDiv.innerHTML = html;
}
