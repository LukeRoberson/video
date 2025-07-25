/**
 * loadvideos.js
 * 
 * Handles loading videos and thumbnails dynamically for each category in the video manager web app.
 * For lazy loading, it uses the IntersectionObserver API to load videos only when the category row is in view.
 * This improves performance by reducing the initial load time and only fetching data as needed.
 */


/**
 * Loads videos for a given category and populates the thumbnails section.
 * @param {*} categoryId - The ID of the category to load videos for.
 */
function populateCategory(categoryId) {
    fetch(`/videos/${categoryId}`)
        .then(response => response.json())
        .then(videos => {
            const thumbnailsDiv = document.querySelector(`#category-${categoryId} .thumbnails`);
            thumbnailsDiv.innerHTML = videos.map(video => `
                <div class="thumbnail">
                    <a href="/video/${video.id}">
                        <img src="${video.thumbnail}" alt="${video.name}">
                        <div class="thumbnail-title">${video.name}</div>
                        <div class="thumbnail-duration">${video.duration}</div>
                    </a>
                </div>
            `).join('');
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
                populateCategory(categoryId);
                observer.unobserve(entry.target); // Stop observing once loaded
            }
        });
    });

    // Observe each category row
    document.querySelectorAll(".category-row").forEach(row => {
        observer.observe(row);
    });
});
