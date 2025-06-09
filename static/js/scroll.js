/**
 * scroll.js
 * 
 * Handles horizontal scrolling and dynamic visibility of left/right navigation arrows
 * for horizontally scrollable thumbnail carousels in the video manager web app.
 * 
 * - Arrows are only visible if there is more content to scroll in that direction.
 * - Clicking an arrow scrolls the carousel by one visible "page" (the width of the container).
 */


/**
 * Scrolls the thumbnails container horizontally by one page in the given direction.
 * @param {string} wrapperId - The ID of the thumbnails wrapper element.
 * @param {number} direction - Direction to scroll: -1 for left, 1 for right.
 */
function scrollThumbnails(wrapperId, direction) {
    const thumbnails = document.getElementById(wrapperId).querySelector('.thumbnails');
    const scrollAmount = thumbnails.clientWidth; // Scroll by visible width
    thumbnails.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
}


/**
 * Updates the visibility of left and right scroll arrows based on scroll position.
 * @param {string} wrapperId - The ID of the thumbnails wrapper element.
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
 * Should be called once after the DOM is loaded.
 */
function setupScrollArrows() {
    document.querySelectorAll('.thumbnails-wrapper').forEach(wrapper => {
        const thumbnails = wrapper.querySelector('.thumbnails');
        thumbnails.addEventListener('scroll', () => updateArrows(wrapper.id));
        window.addEventListener('resize', () => updateArrows(wrapper.id));
        updateArrows(wrapper.id);
    });
}


// Initialize scroll arrows when the DOM is ready
document.addEventListener('DOMContentLoaded', setupScrollArrows);
