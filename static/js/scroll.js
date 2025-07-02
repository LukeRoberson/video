/**
 * scroll.js
 * 
 * Handles horizontal scrolling and dynamic visibility of left/right navigation arrows
 * for horizontally scrollable thumbnail carousels in the video manager web app.
 * 
 * Features:
 * - Dynamically shows/hides left and right arrows based on scroll position.
 * - Allows horizontal scrolling using mouse wheel or arrow buttons.
 * - Smooth scrolling behavior for better user experience.
 * 
 * Usage:
 * - Include this script on pages with `.thumbnails-wrapper` elements.
 * - Ensure each `.thumbnails-wrapper` has a unique `id` and contains:
 *   - `.thumbnails` (scrollable container for thumbnails)
 *   - `.scroll-arrow.left` (left arrow button)
 *   - `.scroll-arrow.right` (right arrow button)
 * 
 * Dependencies:
 * - None (Vanilla JavaScript)
 * 
 * Event Listeners:
 * - `scroll` on `.thumbnails`: Updates arrow visibility dynamically as the user scrolls.
 * - `resize` on `window`: Recalculates arrow visibility when the window is resized.
 * - `wheel` on `.thumbnails`: Enables horizontal scrolling using the mouse wheel.
 * - `DOMContentLoaded` on `document`: Initializes scroll arrows and event listeners.
 */


/**
 * Scrolls the thumbnails container horizontally by one page in the given direction.
 * 
 * @param {string} wrapperId - The ID of the thumbnails wrapper element.
 * @param {number} direction - Direction to scroll: -1 for left, 1 for right.
 * 
 * Behavior:
 * - Scrolls the `.thumbnails` container inside the specified wrapper.
 * - The scroll amount is equal to the visible width of the container.
 * - Smooth scrolling is applied for better user experience.
 */
function scrollThumbnails(wrapperId, direction) {
    const thumbnails = document.getElementById(wrapperId).querySelector('.thumbnails');
    const scrollAmount = thumbnails.clientWidth; // Scroll by visible width
    thumbnails.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
}


/**
 * Updates the visibility of left and right scroll arrows based on scroll position.
 * 
 * @param {string} wrapperId - The ID of the thumbnails wrapper element.
 * 
 * Behavior:
 * - Shows the left arrow if the container can scroll left.
 * - Shows the right arrow if the container can scroll right.
 * - Hides arrows if scrolling is not possible in the respective direction.
 * 
 * Notes:
 * - This function should be called after the thumbnails are populated.
 * - It is also triggered on scroll and resize events.
 */
function updateArrows(wrapperId) {
    const wrapper = document.getElementById(wrapperId);
    const thumbnails = wrapper.querySelector('.thumbnails');

    const leftArrow = wrapper.querySelector('.scroll-arrow.left');
    const rightArrow = wrapper.querySelector('.scroll-arrow.right');
    
    // Show/hide arrows based on scroll position
    leftArrow.style.display = thumbnails.scrollLeft > 0 ? 'flex' : 'none';
    rightArrow.style.display = (thumbnails.scrollLeft + thumbnails.clientWidth) < thumbnails.scrollWidth ? 'flex' : 'none';
}


/**
 * Sets up scroll arrow visibility and event listeners for all thumbnail wrappers on the page.
 * 
 * Behavior:
 * - Adds `scroll` and `resize` event listeners to update arrow visibility dynamically.
 * - Initializes arrow visibility immediately after the DOM is loaded.
 * 
 * Notes:
 * - This function should be called once after the DOM is fully loaded.
 * - Ensure each `.thumbnails-wrapper` has a unique `id`.
 */
function setupScrollArrows() {
    document.querySelectorAll('.thumbnails-wrapper').forEach(wrapper => {
        const thumbnails = wrapper.querySelector('.thumbnails');

        // Add event listeners for scroll and resize
        thumbnails.addEventListener('scroll', () => updateArrows(wrapper.id));
        window.addEventListener('resize', () => updateArrows(wrapper.id));

        // Delay by 100ms to allow layout calculation
        setTimeout(() => updateArrows(wrapper.id), 100);
    });
}


/**
 * Event listener.
 * Adds mouse wheel scrolling functionality to thumbnail containers.
 */
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.thumbnails').forEach(thumbnails => {
        thumbnails.addEventListener('wheel', (event) => {
            // Prevent vertical scrolling
            event.preventDefault();

            // Scroll horizontally
            const speedFactor = 2; // Adjust this value to control scroll speed
            thumbnails.scrollBy({
                left: event.deltaY * speedFactor, // Use vertical scroll delta for horizontal scrolling
                behavior: 'smooth'
            });
        });
    });
});


/**
 * Event listener.
 * Sets up scroll arrows and event listeners when the DOM is fully loaded.
 */
document.addEventListener('DOMContentLoaded', setupScrollArrows);
