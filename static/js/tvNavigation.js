/**
 * TV Remote Navigation Enhancement
 * Provides native app-like navigation using arrow keys/remote control
 * 
 * Used in the base template
 */



/**
 * Enhances navigation for TV-like devices by allowing users to navigate
 * through focusable elements using arrow keys or a remote control.
 * 
 * Includes extra functions
 */
document.addEventListener('DOMContentLoaded', function() {
    // Detect if we're likely on a TV
    const isTV = window.innerWidth >= 1920 || 
                 (window.innerWidth >= 1200 && !('ontouchstart' in window));
    
    // If not a TV, just exit this script
    if (!isTV) return;
    
    let currentFocusIndex = 0;
    let focusableElements = [];
    
    /**
     * Updates the list of focusable elements on the page (buttons, thumbnails, etc).
     * This function is called initially and whenever the content changes.
     */
    function updateFocusableElements() {
        // Get all focusable elements in order
        focusableElements = Array.from(document.querySelectorAll(
            'a, button, .thumbnail, .video-js, [tabindex]:not([tabindex="-1"])'
        )).filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0; // Only visible elements
        });
        
        // Add visual focus indicators
        focusableElements.forEach((el, index) => {
            el.setAttribute('data-tv-index', index);
            el.style.outline = 'none'; // Remove default outline
            
            // Make video player focusable
            if (el.classList.contains('video-js')) {
                el.setAttribute('tabindex', '0');
            }
        });
    }
    

    /**
     * Sets focus on a specific element by index.
     * Highlights the element and scrolls it into view.
     * 
     * @param {number} index - The index of the element to focus.
     */
    function setFocus(index) {
        // Remove previous focus
        focusableElements.forEach(el => {
            el.classList.remove('tv-focused');
            el.style.border = '';
        });
        
        // Set new focus
        if (focusableElements[index]) {
            const element = focusableElements[index];
            element.classList.add('tv-focused');
            element.style.border = '3px solid #007bff';
            element.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
            currentFocusIndex = index;
        }
    }
    
    /**
     * Initial setup: find all focusable elements and set the first one as focused.
     * This is called when the page loads.
     */
    updateFocusableElements();
    if (focusableElements.length > 0) {
        setFocus(0);
    }
    
    
    /**
     * Listens for keydown events to handle navigation.
     * Supports arrow keys for navigation, Enter/Space for selection,
     * and Escape for going back.
     * 
     * The remote control is effectively arrow keys on a keyboard.
     */
    document.addEventListener('keydown', function(e) {
        // When a keypress is detected, find which key, and handle it
        switch(e.key) {
            // Handle arrow keys for navigation
            case 'ArrowDown':
                e.preventDefault();
                const nextRowIndex = findNextInDirection('down');
                if (nextRowIndex !== -1) setFocus(nextRowIndex);
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                const prevRowIndex = findNextInDirection('up');
                if (prevRowIndex !== -1) setFocus(prevRowIndex);
                break;
                
            case 'ArrowRight':
                e.preventDefault();
                if (currentFocusIndex < focusableElements.length - 1) {
                    setFocus(currentFocusIndex + 1);
                }
                break;
                
            case 'ArrowLeft':
                e.preventDefault();
                if (currentFocusIndex > 0) {
                    setFocus(currentFocusIndex - 1);
                }
                break;
                
            // Enter and spacebar are for selections and actions
            case 'Enter':
            case ' ':
                e.preventDefault();
                focusableElements[currentFocusIndex]?.click();
                break;
                
            // The escape key is the back button, and cancels things like open modals
            case 'Escape':
                window.history.back();
                break;
        }
    });
    

    /**
     * Finds the next focusable element in the specified direction.
     * 
     * @param {*} direction 
     * @returns 
     */
    function findNextInDirection(direction) {
        // Ensure we have focusable elements
        const current = focusableElements[currentFocusIndex];
        if (!current) return -1;
        
        // Get the current element's position
        const currentRect = current.getBoundingClientRect();
        const currentY = currentRect.top + currentRect.height / 2;
        const currentX = currentRect.left + currentRect.width / 2;
        
        // Find the best match in the specified direction
        let bestMatch = -1;
        let bestDistance = Infinity;
        
        // Loop through all focusable elements to find the best match
        focusableElements.forEach((el, index) => {
            // Skip the current element
            if (index === currentFocusIndex) return;
            
            // Get the element's position
            const rect = el.getBoundingClientRect();
            const elY = rect.top + rect.height / 2;
            const elX = rect.left + rect.width / 2;
            
            // Check if the element is in the specified direction
            let isInDirection = false;
            let distance = 0;
            
            // Calculate distance based on direction
            if (direction === 'down') {
                isInDirection = elY > currentY + 20; // 20px threshold
                distance = Math.abs(elY - currentY) + Math.abs(elX - currentX) * 0.1; // Prefer same column
            } else if (direction === 'up') {
                isInDirection = elY < currentY - 20; // 20px threshold  
                distance = Math.abs(elY - currentY) + Math.abs(elX - currentX) * 0.1; // Prefer same column
            }
            
            // If the element is in the direction and closer than the best match, update
            // the best match
            if (isInDirection && distance < bestDistance) {
                bestDistance = distance;
                bestMatch = index;
            }
        });
        
        // Return the best match index
        return bestMatch;
    }
    

    /**
     * Updates the focusable elements when the content changes.
     */
    const observer = new MutationObserver(updateFocusableElements);
    observer.observe(document.body, { 
        childList: true, 
        subtree: true 
    });
});