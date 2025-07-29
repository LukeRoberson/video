/**
 * populateCategories.js
 * 
 * Handles loading videos and thumbnails dynamically for each category in the video manager web app.
 *  Pages are organized by main category, and will display a carousel for subcategories.
 * 
 * For lazy loading, it uses the IntersectionObserver API to load videos only when the category row is in view.
 *  This improves performance by reducing the initial load time and only fetching data as needed.
 */


/**
 * Calls a Flask route, passing a major category ID and subcategory ID, to get a list of videos.
 * Loads videos into the carousel for the specified category.
 * 
 * @param {*} categoryId - The ID of the category to load videos for.
 */
function populateCategory(categoryId, subcategoryId) {
    fetch(`/api/categories/${categoryId}/${subcategoryId}`)
        .then(response => response.json())
        .then(videos => {
            const wrapperId = `wrapper-${subcategoryId}`;            
            const thumbnailsDiv = document.querySelector(`#category-${subcategoryId} .thumbnails`);
            
            // Add thumbnails to the category row
            thumbnailsDiv.innerHTML = videos.map(video => `
                <div class="thumbnail${video.watched ? ' watched' : ''}">
                    <a href="/video/${video.id}">
                        ${video.watched ? `
                            <div class="thumbnail-watched-icon">
                                <svg viewBox="0 0 24 24">
                                    <path d="M9 16.2l-3.5-3.5 1.4-1.4L9 13.4l7.1-7.1 1.4 1.4z"/>
                                </svg>
                            </div>
                        ` : ''}
                        <img src="${video.thumbnail}" alt="${video.name}">
                        <div class="thumbnail-title">${video.name}</div>
                        <div class="thumbnail-duration">${video.duration}</div>
                    </a>
                </div>
            `).join('');

            // Update arrow visibility after thumbnails are populated
            updateArrows(wrapperId);
        })

        .catch(error => {
            console.error("Error loading videos:", error);
        });
}


/**
 * Sets up an IntersectionObserver to load videos when a category row comes into view.
 * This allows for lazy loading of videos to improve performance.
 */
document.addEventListener("DOMContentLoaded", () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const categoryId = entry.target.dataset.categoryId;
                const subcategoryId = entry.target.dataset.subcategoryId;
                populateCategory(categoryId, subcategoryId);
                observer.unobserve(entry.target); // Stop observing once loaded
            }
        });
    });

    // Observe each category row
    document.querySelectorAll(".category-row").forEach(row => {
        observer.observe(row);
    });
});


/**
 * Enhances the category navigation for TV devices.
 */
function enhanceCategoryNavigationForTV() {
    // Check if the device is a TV based on screen width and touch capability
    const isTV = window.tvDetection.isTV();
    if (!isTV) return;
    
    // Make category rows more prominent
    document.querySelectorAll('.category-row').forEach(row => {
        row.style.marginBottom = '3em';
        
        const title = row.querySelector('.category-title');
        if (title) {
            title.style.fontSize = '1.4em';
            title.style.marginBottom = '1em';
        }
    });
    
    // Add visual indicators for scrollable content
    document.querySelectorAll('.thumbnails').forEach(container => {
        if (container.scrollWidth > container.clientWidth) {
            container.style.position = 'relative';
            
            // Add scroll indicators
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
    });
}

/**
 * Updates visibility after categories are fully loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit for categories to load before enhancing for TV
    setTimeout(enhanceCategoryNavigationForTV, 500);
});
