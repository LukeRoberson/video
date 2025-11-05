/**
 * @fileoverview TV Remote Navigation Enhancement
 * Provides native app-like navigation using arrow keys/remote control for Smart TVs.
 * Supports Samsung Tizen, Fire TV, LG WebOS, and other TV platforms.
 */
/**
 * Configuration constants for TV navigation
 */
const TVNavigationConfig = {
    /** Delay before starting TV navigation */
    STARTUP_DELAY: 1000,
    /** Delay for slide navigation */
    SLIDE_NAVIGATION_DELAY: 300,
    /** Element update debounce delay */
    UPDATE_DEBOUNCE_DELAY: 100,
    /** Debug mode keyboard shortcut delay */
    DEBUG_DELAY: 500,
    /** Vertical threshold for same row detection */
    SAME_ROW_THRESHOLD: 50,
    /** Small horizontal movement threshold */
    SMALL_HORIZONTAL_THRESHOLD: 10,
    /** Vertical element spacing threshold */
    VERTICAL_SPACING_THRESHOLD: 30
};
/**
 * TV remote control key mappings for different platforms
 */
const TVKeyMappings = {
    /** Standard keyboard codes */
    STANDARD: {
        37: 'ArrowLeft', 38: 'ArrowUp', 39: 'ArrowRight', 40: 'ArrowDown',
        13: 'Enter', 27: 'Escape', 32: ' '
    },
    /** Samsung TV (Tizen) remote codes */
    SAMSUNG: {
        4: 'Escape', 10009: 'Escape', 10252: ' ', 415: ' ', 10182: 'Enter'
    },
    /** Fire TV / Amazon remote codes */
    FIRE_TV: {
        21: 'ArrowLeft', 19: 'ArrowUp', 22: 'ArrowRight', 20: 'ArrowDown', 23: 'Enter'
    },
    /** WebOS (LG TV) remote codes */
    WEBOS: {
        461: 'Escape', 13: 'Enter'
    },
    /** Additional TV remote codes */
    ADDITIONAL: {
        166: 'Escape', 8: 'Escape'
    }
};
/**
 * Handles TV device detection and status management
 */
class TVDetectionManager {
    constructor() {
        /**
         * Current TV detection status
         */
        this.isTV = false;
    }
    /**
     * Update TV detection status using multiple detection methods
     * @returns True if device is detected as TV
     */
    updateTVStatus() {
        const externalTVDetection = window.tvDetection;
        if (externalTVDetection && typeof externalTVDetection.isTV === 'function') {
            this.isTV = externalTVDetection.isTV();
        }
        else {
            this.isTV = this.performEnhancedDetection();
        }
        console.log('Enhanced TV Detection:', {
            isTV: this.isTV,
            userAgent: navigator.userAgent,
            isSamsung: navigator.userAgent.toLowerCase().includes('tizen'),
            isFireTV: navigator.userAgent.toLowerCase().includes('silk'),
            isLG: navigator.userAgent.toLowerCase().includes('webos')
        });
        return this.isTV;
    }
    /**
     * Perform enhanced TV detection based on user agent
     * @returns True if TV is detected
     */
    performEnhancedDetection() {
        const userAgent = navigator.userAgent.toLowerCase();
        const isSamsungTV = userAgent.includes('tizen') || userAgent.includes('samsung');
        const isFireTV = userAgent.includes('silk') || userAgent.includes('afts');
        const isLGTV = userAgent.includes('webos') || userAgent.includes('netcast');
        return isSamsungTV || isFireTV || isLGTV ||
            userAgent.includes('smart-tv') ||
            userAgent.includes('smarttv') ||
            userAgent.includes('roku') ||
            userAgent.includes('googletv') ||
            userAgent.includes('operatv') ||
            (navigator.maxTouchPoints === 0 && window.screen.width >= 1920);
    }
    /**
     * Get current TV status
     * @returns Current TV detection status
     */
    getTVStatus() {
        return this.isTV;
    }
}
/**
 * Handles remote control key input and normalization
 */
class TVKeyHandler {
    /**
     * Normalize key input from various TV remote controls
     * @param event - Keyboard event from remote
     * @returns Normalized key name or null if not recognized
     */
    normalizeKey(event) {
        console.log('Raw key event:', {
            type: event.type,
            key: event.key,
            keyCode: event.keyCode,
            which: event.which,
            code: event.code,
            userAgent: navigator.userAgent.substring(0, 100)
        });
        // Check all key mapping categories
        const allMappings = [
            TVKeyMappings.STANDARD,
            TVKeyMappings.SAMSUNG,
            TVKeyMappings.FIRE_TV,
            TVKeyMappings.WEBOS,
            TVKeyMappings.ADDITIONAL
        ];
        for (const mappings of allMappings) {
            const mapping = mappings;
            if (mapping[event.keyCode]) {
                return mapping[event.keyCode];
            }
        }
        // Standard key/code mapping
        if (event.code && event.code.startsWith('Arrow')) {
            return event.key;
        }
        console.log('Unrecognized key:', event.keyCode);
        return null;
    }
}
/**
 * Manages focusable elements and their organization
 */
class FocusableElementManager {
    constructor() {
        /**
         * Array of currently focusable elements
         */
        this.focusableElements = [];
    }
    /**
     * Update the list of focusable elements on the page
     */
    updateFocusableElements() {
        const allElements = Array.from(document.querySelectorAll('a[href], button:not([disabled]), .thumbnail, .thumbnail-home, .video-js, input:not([disabled]), [tabindex]:not([tabindex="-1"])'));
        this.focusableElements = allElements.filter(el => this.isElementFocusable(el));
        this.sortElementsByPosition();
        this.prepareElementsForNavigation();
    }
    /**
     * Check if an element is actually focusable
     * @param element - Element to check
     * @returns True if element is focusable
     */
    isElementFocusable(element) {
        const rect = element.getBoundingClientRect();
        const style = window.getComputedStyle(element);
        // Basic visibility checks
        if (rect.width <= 0 || rect.height <= 0 ||
            style.visibility === 'hidden' ||
            style.display === 'none' ||
            element.hasAttribute('disabled')) {
            return false;
        }
        // Exclude carousel controls completely
        if (element.classList.contains('carousel-control-prev') ||
            element.classList.contains('carousel-control-next')) {
            return false;
        }
        // Prevent nested thumbnail elements
        if (element.classList.contains('thumbnail') || element.classList.contains('thumbnail-home')) {
            return this.isValidThumbnailElement(element);
        }
        return true;
    }
    /**
     * Check if thumbnail element is valid (not nested)
     * @param element - Thumbnail element to check
     * @returns True if valid thumbnail
     */
    isValidThumbnailElement(element) {
        // Check if this element has a parent that's also a thumbnail
        const parentThumbnail = element.parentElement?.closest('.thumbnail, .thumbnail-home');
        if (parentThumbnail && parentThumbnail !== element) {
            return false; // Skip nested thumbnail
        }
        // Also check if this element contains other thumbnails (keep the container)
        const childThumbnails = element.querySelectorAll('.thumbnail, .thumbnail-home');
        if (childThumbnails.length > 0) {
            return false; // Skip containers, we'll get the actual thumbnails
        }
        return true;
    }
    /**
     * Sort elements by position with section awareness
     */
    sortElementsByPosition() {
        this.focusableElements.sort((a, b) => {
            const rectA = a.getBoundingClientRect();
            const rectB = b.getBoundingClientRect();
            const priorityA = this.getSectionPriority(a);
            const priorityB = this.getSectionPriority(b);
            // Sort by section priority first
            if (priorityA !== priorityB) {
                return priorityA - priorityB;
            }
            // Within same section, sort by position
            const verticalDiff = rectA.top - rectB.top;
            if (Math.abs(verticalDiff) > TVNavigationConfig.SAME_ROW_THRESHOLD) {
                return verticalDiff;
            }
            // If roughly same row, sort by horizontal position
            return rectA.left - rectB.left;
        });
    }
    /**
     * Get section priority for sorting
     * @param element - Element to get priority for
     * @returns Priority number (lower = higher priority)
     */
    getSectionPriority(element) {
        if (element.closest('.navbar'))
            return 1;
        if (element.closest('[id*="profile"]') || element.getAttribute('href')?.includes('profile'))
            return 2;
        if (element.closest('.carousel'))
            return 3;
        return 4; // Other elements
    }
    /**
     * Prepare elements for TV navigation
     */
    prepareElementsForNavigation() {
        this.focusableElements.forEach((el, index) => {
            el.setAttribute('data-tv-index', index.toString());
            el.setAttribute('tabindex', '0');
            el.style.outline = 'none';
        });
    }
    /**
     * Get all focusable elements
     * @returns Array of focusable elements
     */
    getFocusableElements() {
        return this.focusableElements;
    }
    /**
     * Get element by index
     * @param index - Element index
     * @returns Element at index or null
     */
    getElementByIndex(index) {
        return this.focusableElements[index] || null;
    }
    /**
     * Get element index
     * @param element - Element to find index for
     * @returns Element index or -1 if not found
     */
    getElementIndex(element) {
        return this.focusableElements.indexOf(element);
    }
}
/**
 * Manages focus state and visual indicators
 */
class FocusManager {
    /**
     * Create a FocusManager instance
     * @param elementManager - Element manager instance
     */
    constructor(elementManager) {
        /**
         * Current focus index
         */
        this.currentFocusIndex = 0;
        this.elementManager = elementManager;
    }
    /**
     * Set focus on a specific element by index
     * @param index - Index of element to focus
     */
    setFocus(index) {
        const focusableElements = this.elementManager.getFocusableElements();
        // Remove previous focus
        this.clearAllFocus(focusableElements);
        // Set new focus
        if (focusableElements[index]) {
            const element = focusableElements[index];
            this.currentFocusIndex = index;
            this.applyFocusStyles(element);
            this.scrollIntoView(element);
            element.focus();
        }
    }
    /**
     * Clear focus from all elements
     * @param elements - Elements to clear focus from
     */
    clearAllFocus(elements) {
        elements.forEach(el => {
            el.classList.remove('tv-focused');
            el.style.border = '';
            el.style.boxShadow = '';
            el.style.zIndex = '';
        });
    }
    /**
     * Apply focus styles to element
     * @param element - Element to apply styles to
     */
    applyFocusStyles(element) {
        element.classList.add('tv-focused');
        element.style.border = '4px solid #ff6b35';
        element.style.boxShadow = '0 0 20px rgba(255, 107, 53, 0.8)';
        element.style.transition = 'all 0.2s ease';
        element.style.zIndex = '1000';
    }
    /**
     * Scroll element into view
     * @param element - Element to scroll into view
     */
    scrollIntoView(element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'center'
        });
    }
    /**
     * Get current focus index
     * @returns Current focus index
     */
    getCurrentFocusIndex() {
        return this.currentFocusIndex;
    }
    /**
     * Get currently focused element
     * @returns Currently focused element
     */
    getCurrentElement() {
        return this.elementManager.getElementByIndex(this.currentFocusIndex);
    }
}
/**
 * Handles directional navigation logic
 */
class DirectionalNavigator {
    /**
     * Create a DirectionalNavigator instance
     * @param elementManager - Element manager instance
     * @param focusManager - Focus manager instance
     */
    constructor(elementManager, focusManager) {
        this.elementManager = elementManager;
        this.focusManager = focusManager;
    }
    /**
     * Find the next focusable element in a direction
     * @param direction - Direction to navigate
     * @returns Index of next element or -1 if not found
     */
    findNextInDirection(direction) {
        const focusableElements = this.elementManager.getFocusableElements();
        const currentFocusIndex = this.focusManager.getCurrentFocusIndex();
        if (focusableElements.length === 0)
            return -1;
        const current = focusableElements[currentFocusIndex];
        if (!current)
            return 0;
        const currentRect = current.getBoundingClientRect();
        const currentY = currentRect.top + currentRect.height / 2;
        const currentX = currentRect.left + currentRect.width / 2;
        const currentSection = this.getElementSection(current);
        const currentCarousel = current.closest('.carousel');
        let bestMatch = -1;
        let bestDistance = Infinity;
        focusableElements.forEach((el, index) => {
            if (index === currentFocusIndex)
                return;
            const rect = el.getBoundingClientRect();
            const elY = rect.top + rect.height / 2;
            const elX = rect.left + rect.width / 2;
            const elSection = this.getElementSection(el);
            const elCarousel = el.closest('.carousel');
            const navigationResult = this.calculateNavigationDistance(direction, currentY, currentX, elY, elX, currentSection, elSection, currentCarousel, elCarousel, el);
            if (navigationResult.isValid && navigationResult.distance < bestDistance) {
                bestDistance = navigationResult.distance;
                bestMatch = index;
            }
        });
        return bestMatch;
    }
    /**
     * Get element section identifier
     * @param element - Element to get section for
     * @returns Section identifier
     */
    getElementSection(element) {
        if (element.closest('.navbar'))
            return 'navbar';
        if (element.closest('[id*="profile"]') || element.getAttribute('href')?.includes('profile'))
            return 'profile';
        if (element.closest('.carousel'))
            return 'carousel';
        if (element.closest('[class*="news"]') || element.closest('[id*="news"]'))
            return 'news';
        if (element.closest('[class*="program"]') || element.closest('[id*="program"]'))
            return 'program';
        if (element.closest('.container') || element.closest('.row') || element.closest('.col'))
            return 'content';
        return 'other';
    }
    /**
     * Calculate navigation distance and validity for direction
     * @param direction - Navigation direction
     * @param currentY - Current element Y position
     * @param currentX - Current element X position
     * @param elY - Target element Y position
     * @param elX - Target element X position
     * @param currentSection - Current element section
     * @param elSection - Target element section
     * @param currentCarousel - Current carousel element
     * @param elCarousel - Target carousel element
     * @param el - Target element
     * @returns Navigation result with isValid and distance properties
     */
    calculateNavigationDistance(direction, currentY, currentX, elY, elX, currentSection, elSection, currentCarousel, elCarousel, el) {
        let isValid = false;
        let distance = 0;
        switch (direction) {
            case 'down':
                isValid = elY > currentY + TVNavigationConfig.VERTICAL_SPACING_THRESHOLD;
                distance = Math.abs(elY - currentY) + Math.abs(elX - currentX) * 0.2;
                distance = this.applyDownNavigationPreferences(distance, currentSection, elSection, currentCarousel, elCarousel);
                break;
            case 'up':
                isValid = elY < currentY - TVNavigationConfig.VERTICAL_SPACING_THRESHOLD;
                distance = Math.abs(elY - currentY) + Math.abs(elX - currentX) * 0.2;
                distance = this.applyUpNavigationPreferences(distance, currentSection, elSection, currentCarousel, elCarousel, el);
                break;
            case 'right':
                const rightResult = this.calculateHorizontalNavigation('right', currentX, elX, currentY, elY, currentSection, elSection, currentCarousel, elCarousel);
                isValid = rightResult.isValid;
                distance = rightResult.distance;
                break;
            case 'left':
                const leftResult = this.calculateHorizontalNavigation('left', currentX, elX, currentY, elY, currentSection, elSection, currentCarousel, elCarousel);
                isValid = leftResult.isValid;
                distance = leftResult.distance;
                break;
        }
        return { isValid, distance };
    }
    /**
     * Apply preferences for downward navigation
     * @param distance - Base distance
     * @param currentSection - Current section
     * @param elSection - Target section
     * @param currentCarousel - Current carousel
     * @param elCarousel - Target carousel
     * @returns Modified distance
     */
    applyDownNavigationPreferences(distance, currentSection, elSection, currentCarousel, elCarousel) {
        // Prefer moving to different sections when going down
        if (currentSection === 'navbar' && elSection !== 'navbar') {
            distance *= 0.3; // Strong preference for leaving navbar
        }
        else if (currentSection === elSection && currentCarousel && elCarousel && currentCarousel === elCarousel) {
            distance *= 2; // Discourage staying in same carousel
        }
        return distance;
    }
    /**
     * Apply preferences for upward navigation
     * @param distance - Base distance
     * @param currentSection - Current section
     * @param elSection - Target section
     * @param currentCarousel - Current carousel
     * @param elCarousel - Target carousel
     * @param el - Target element
     * @returns Modified distance
     */
    applyUpNavigationPreferences(distance, currentSection, elSection, currentCarousel, elCarousel, el) {
        // Complex upward navigation preferences
        if (currentSection === 'content' || currentSection === 'news' || currentSection === 'program') {
            if (elSection === currentSection) {
                distance *= 0.8;
            }
            else if (elSection === 'carousel') {
                distance *= 0.9;
            }
            else if (elSection === 'navbar') {
                distance *= 1.5;
            }
        }
        else if (currentSection === 'carousel') {
            if (elSection === 'content' || elSection === 'news' || elSection === 'program') {
                distance *= 0.7;
            }
            else if (elSection === 'carousel') {
                distance *= currentCarousel === elCarousel ? 1 : 2;
            }
            else if (elSection === 'navbar') {
                distance *= 3;
            }
        }
        else if (currentSection === 'navbar' && elSection === 'navbar') {
            distance *= 0.5;
        }
        // Avoid specific buttons unless they're the best option
        if (el.textContent?.toLowerCase().includes('tv mode') ||
            el.textContent?.toLowerCase().includes('toggle') ||
            el.classList.contains('btn-outline-secondary')) {
            distance *= 5;
        }
        return distance;
    }
    /**
     * Calculate horizontal navigation result
     * @param direction - 'left' or 'right'
     * @param currentX - Current X position
     * @param elX - Target X position
     * @param currentY - Current Y position
     * @param elY - Target Y position
     * @param currentSection - Current section
     * @param elSection - Target section
     * @param currentCarousel - Current carousel
     * @param elCarousel - Target carousel
     * @returns Result with isValid and distance properties
     */
    calculateHorizontalNavigation(direction, currentX, elX, currentY, elY, currentSection, elSection, currentCarousel, elCarousel) {
        // Strict horizontal navigation rules
        if (currentSection === 'navbar' && elSection !== 'navbar') {
            return { isValid: false, distance: Infinity };
        }
        if (currentSection === 'carousel') {
            if (elSection !== 'carousel' || currentCarousel !== elCarousel) {
                return { isValid: false, distance: Infinity };
            }
            if (Math.abs(elY - currentY) > TVNavigationConfig.VERTICAL_SPACING_THRESHOLD) {
                return { isValid: false, distance: Infinity };
            }
        }
        if (currentSection === 'content' || currentSection === 'news' || currentSection === 'program') {
            if (elSection !== currentSection || Math.abs(elY - currentY) > TVNavigationConfig.SAME_ROW_THRESHOLD) {
                return { isValid: false, distance: Infinity };
            }
        }
        const isInDirection = direction === 'right' ?
            elX > currentX + TVNavigationConfig.SMALL_HORIZONTAL_THRESHOLD :
            elX < currentX - TVNavigationConfig.SMALL_HORIZONTAL_THRESHOLD;
        if (!isInDirection) {
            return { isValid: false, distance: Infinity };
        }
        const distance = Math.abs(elX - currentX) + Math.abs(elY - currentY) * 0.1;
        return { isValid: true, distance };
    }
}
/**
 * Handles carousel-specific navigation logic
 */
class CarouselNavigator {
    /**
     * Create a CarouselNavigator instance
     * @param elementManager - Element manager instance
     * @param focusManager - Focus manager instance
     */
    constructor(elementManager, focusManager) {
        this.elementManager = elementManager;
        this.focusManager = focusManager;
    }
    /**
     * Navigate to next/previous carousel slide when reaching the edge
     * @param direction - 'right' or 'left'
     * @returns True if slide navigation occurred
     */
    navigateCarouselSlide(direction) {
        const currentElement = this.focusManager.getCurrentElement();
        const currentCarousel = currentElement?.closest('.carousel');
        if (!currentCarousel) {
            console.log('navigateCarouselSlide: Not in carousel');
            return false;
        }
        console.log('navigateCarouselSlide: Direction =', direction, 'from element:', currentElement);
        const bootstrapCarousel = window.bootstrap?.Carousel;
        if (!bootstrapCarousel) {
            console.log('Bootstrap carousel not available');
            return false;
        }
        const carouselInstance = bootstrapCarousel.getInstance(currentCarousel) || new bootstrapCarousel(currentCarousel);
        const currentSlide = currentCarousel.querySelector('.carousel-item.active');
        const visibleThumbnails = Array.from(currentSlide.querySelectorAll('.thumbnail, .thumbnail-home'));
        const currentIndex = visibleThumbnails.indexOf(currentElement);
        console.log('navigateCarouselSlide: Found', visibleThumbnails.length, 'thumbnails, current at index:', currentIndex);
        return this.handleSlideNavigation(direction, currentIndex, visibleThumbnails, carouselInstance, currentCarousel);
    }
    /**
     * Handle slide navigation logic
     * @param direction - Navigation direction
     * @param currentIndex - Current thumbnail index
     * @param visibleThumbnails - Visible thumbnails in current slide
     * @param carouselInstance - Bootstrap carousel instance
     * @param currentCarousel - Current carousel element
     * @returns True if navigation occurred
     */
    handleSlideNavigation(direction, currentIndex, visibleThumbnails, carouselInstance, currentCarousel) {
        const slides = currentCarousel.querySelectorAll('.carousel-item');
        const activeSlide = currentCarousel.querySelector('.carousel-item.active');
        const activeIndex = Array.from(slides).indexOf(activeSlide);
        if (direction === 'right' && currentIndex === visibleThumbnails.length - 1) {
            return this.moveToNextSlide(activeIndex, slides.length, carouselInstance, currentCarousel);
        }
        else if (direction === 'left' && currentIndex === 0) {
            return this.moveToPreviousSlide(activeIndex, carouselInstance, currentCarousel);
        }
        console.log('navigateCarouselSlide: Not at edge, normal navigation should handle');
        return false;
    }
    /**
     * Move to next carousel slide
     * @param activeIndex - Current active slide index
     * @param totalSlides - Total number of slides
     * @param carouselInstance - Bootstrap carousel instance
     * @param currentCarousel - Current carousel element
     * @returns True if moved to next slide
     */
    moveToNextSlide(activeIndex, totalSlides, carouselInstance, currentCarousel) {
        console.log('navigateCarouselSlide: At last item. Slide', activeIndex + 1, 'of', totalSlides);
        if (activeIndex < totalSlides - 1) {
            console.log('navigateCarouselSlide: Moving to next slide');
            carouselInstance.next();
            setTimeout(() => {
                this.focusFirstThumbnailInNewSlide(currentCarousel);
            }, TVNavigationConfig.SLIDE_NAVIGATION_DELAY);
            return true;
        }
        else {
            console.log('navigateCarouselSlide: No more slides, staying put');
            return true;
        }
    }
    /**
     * Move to previous carousel slide
     * @param activeIndex - Current active slide index
     * @param carouselInstance - Bootstrap carousel instance
     * @param currentCarousel - Current carousel element
     * @returns True if moved to previous slide
     */
    moveToPreviousSlide(activeIndex, carouselInstance, currentCarousel) {
        console.log('navigateCarouselSlide: At first item. Slide', activeIndex + 1);
        if (activeIndex > 0) {
            console.log('navigateCarouselSlide: Moving to previous slide');
            carouselInstance.prev();
            setTimeout(() => {
                this.focusLastThumbnailInNewSlide(currentCarousel);
            }, TVNavigationConfig.SLIDE_NAVIGATION_DELAY);
            return true;
        }
        else {
            console.log('navigateCarouselSlide: No previous slides, staying put');
            return true;
        }
    }
    /**
     * Focus first thumbnail in new slide
     * @param currentCarousel - Current carousel element
     */
    focusFirstThumbnailInNewSlide(currentCarousel) {
        this.elementManager.updateFocusableElements();
        const newSlide = currentCarousel.querySelector('.carousel-item.active');
        const firstThumbnail = newSlide.querySelector('.thumbnail, .thumbnail-home');
        if (firstThumbnail) {
            const newIndex = this.elementManager.getElementIndex(firstThumbnail);
            if (newIndex !== -1) {
                this.focusManager.setFocus(newIndex);
            }
        }
    }
    /**
     * Focus last thumbnail in new slide
     * @param currentCarousel - Current carousel element
     */
    focusLastThumbnailInNewSlide(currentCarousel) {
        this.elementManager.updateFocusableElements();
        const newSlide = currentCarousel.querySelector('.carousel-item.active');
        const thumbnails = Array.from(newSlide.querySelectorAll('.thumbnail, .thumbnail-home'));
        const lastThumbnail = thumbnails[thumbnails.length - 1];
        if (lastThumbnail) {
            const newIndex = this.elementManager.getElementIndex(lastThumbnail);
            if (newIndex !== -1) {
                this.focusManager.setFocus(newIndex);
            }
        }
    }
    /**
     * Update carousel visual indicators
     */
    updateCarouselIndicators() {
        const currentElement = this.focusManager.getCurrentElement();
        document.querySelectorAll('.carousel').forEach(carousel => {
            const slides = carousel.querySelectorAll('.carousel-item');
            const activeSlide = carousel.querySelector('.carousel-item.active');
            const activeIndex = Array.from(slides).indexOf(activeSlide);
            const hasPrev = activeIndex > 0;
            const hasNext = activeIndex < slides.length - 1;
            carousel.setAttribute('data-has-prev', hasPrev.toString());
            carousel.setAttribute('data-has-next', hasNext.toString());
            if (currentElement && currentElement.closest('.carousel') === carousel) {
                const visibleThumbnails = Array.from(activeSlide.querySelectorAll('.thumbnail:not([style*="display: none"])'));
                const currentIndex = visibleThumbnails.indexOf(currentElement);
                carousel.setAttribute('data-at-start', (currentIndex === 0 && hasPrev).toString());
                carousel.setAttribute('data-at-end', (currentIndex === visibleThumbnails.length - 1 && hasNext).toString());
            }
            else {
                carousel.setAttribute('data-at-start', 'false');
                carousel.setAttribute('data-at-end', 'false');
            }
        });
    }
}
/**
 * Handles dropdown menu interactions in TV mode
 */
class DropdownManager {
    /**
     * Create a DropdownManager instance
     * @param elementManager - Element manager instance
     */
    constructor(elementManager) {
        this.elementManager = elementManager;
    }
    /**
     * Check if element is a dropdown toggle
     * @param element - Element to check
     * @returns True if element is dropdown toggle
     */
    isDropdownToggle(element) {
        return element !== null && ((element.hasAttribute('data-bs-toggle') && element.getAttribute('data-bs-toggle') === 'dropdown') ||
            element.classList.contains('dropdown-toggle') ||
            (element.getAttribute('role') === 'button' && element.getAttribute('aria-haspopup') === 'true'));
    }
    /**
     * Check if dropdown is currently open
     * @param toggleElement - Dropdown toggle element
     * @returns True if dropdown is open
     */
    isDropdownOpen(toggleElement) {
        return toggleElement?.nextElementSibling?.classList.contains('tv-dropdown-open') || false;
    }
    /**
     * Handle dropdown toggle interaction
     * @param toggleElement - Dropdown toggle element
     */
    toggleDropdown(toggleElement) {
        const dropdownMenu = toggleElement.nextElementSibling;
        if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
            if (dropdownMenu.classList.contains('tv-dropdown-open')) {
                this.closeDropdown(dropdownMenu);
            }
            else {
                this.openDropdown(dropdownMenu);
            }
        }
    }
    /**
     * Open dropdown menu
     * @param dropdownMenu - Dropdown menu element
     */
    openDropdown(dropdownMenu) {
        // Close any other open dropdowns first
        document.querySelectorAll('.dropdown-menu.tv-dropdown-open').forEach(menu => {
            this.closeDropdown(menu);
        });
        dropdownMenu.classList.add('tv-dropdown-open', 'show');
    }
    /**
     * Close dropdown menu
     * @param dropdownMenu - Dropdown menu element
     */
    closeDropdown(dropdownMenu) {
        dropdownMenu.classList.remove('tv-dropdown-open', 'show');
        // Remove dropdown items from focusable elements
        const dropdownItems = Array.from(dropdownMenu.querySelectorAll('.dropdown-item, a[href]'));
        const focusableElements = this.elementManager.getFocusableElements();
        dropdownItems.forEach(item => {
            const index = focusableElements.indexOf(item);
            if (index !== -1) {
                focusableElements.splice(index, 1);
            }
        });
    }
    /**
     * Close all open dropdowns
     */
    closeAllDropdowns() {
        const openDropdowns = document.querySelectorAll('.dropdown-menu.tv-dropdown-open');
        openDropdowns.forEach(dropdown => this.closeDropdown(dropdown));
    }
}
/**
 * Main TV Navigation controller class
 */
class TVNavigationController {
    /**
     * Create a TVNavigationController instance
     */
    constructor() {
        /**
         * Whether TV navigation is currently active
         */
        this.navigationActive = false;
        /**
         * Mutation observer for DOM changes
         */
        this.observer = null;
        this.tvDetection = new TVDetectionManager();
        this.keyHandler = new TVKeyHandler();
        this.elementManager = new FocusableElementManager();
        this.focusManager = new FocusManager(this.elementManager);
        this.directionalNav = new DirectionalNavigator(this.elementManager, this.focusManager);
        this.carouselNav = new CarouselNavigator(this.elementManager, this.focusManager);
        this.dropdownManager = new DropdownManager(this.elementManager);
        this.init();
    }
    /**
     * Initialize TV navigation system
     */
    init() {
        this.setupEventListeners();
        this.setupMutationObserver();
        // Initial TV status check
        this.tvDetection.updateTVStatus();
        if (this.tvDetection.getTVStatus()) {
            setTimeout(() => {
                this.startTVNavigation();
            }, TVNavigationConfig.STARTUP_DELAY);
        }
    }
    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Remove any existing listeners first
        document.removeEventListener('keydown', this.handleKeydown.bind(this));
        // Add event listeners for TV remote input
        document.addEventListener('keydown', this.handleKeydown.bind(this), true);
        document.addEventListener('keyup', this.handleKeydown.bind(this), true);
        document.addEventListener('keypress', this.handleKeydown.bind(this), true);
        // Listen for TV mode changes
        window.addEventListener('tvModeChanged', (e) => {
            const event = e;
            if (event.detail.isTV) {
                this.startTVNavigation();
            }
            else {
                this.stopTVNavigation();
            }
        });
        // Listen for when tvDetection becomes available
        window.addEventListener('tvDetectionReady', () => {
            this.tvDetection.updateTVStatus();
            if (this.tvDetection.getTVStatus()) {
                this.startTVNavigation();
            }
        });
        // Override Bootstrap dropdown behavior in TV mode
        this.setupDropdownOverrides();
    }
    /**
     * Set up dropdown behavior overrides
     */
    setupDropdownOverrides() {
        // Override Bootstrap dropdown click behavior
        document.addEventListener('click', (e) => {
            if (!this.tvDetection.getTVStatus() || !this.navigationActive)
                return;
            const dropdownToggle = e.target?.closest('.dropdown-toggle');
            if (dropdownToggle) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                return;
            }
        }, true);
        // Prevent Bootstrap dropdown keyboard behavior
        document.addEventListener('keydown', (e) => {
            if (!this.tvDetection.getTVStatus() || !this.navigationActive)
                return;
            const dropdownToggle = e.target?.closest('.dropdown-toggle');
            if (dropdownToggle && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                return;
            }
        }, true);
    }
    /**
     * Set up mutation observer for DOM changes
     */
    setupMutationObserver() {
        this.observer = new MutationObserver((mutations) => {
            if (!this.tvDetection.getTVStatus() || !this.navigationActive)
                return;
            mutations.forEach((mutation) => {
                // Handle content changes
                if (mutation.type === 'childList' || mutation.type === 'attributes') {
                    clearTimeout(this.observer.updateTimeout);
                    this.observer.updateTimeout = window.setTimeout(() => {
                        this.elementManager.updateFocusableElements();
                        const currentIndex = this.focusManager.getCurrentFocusIndex();
                        const focusableElements = this.elementManager.getFocusableElements();
                        if (currentIndex < focusableElements.length) {
                            this.focusManager.setFocus(currentIndex);
                        }
                        else if (focusableElements.length > 0) {
                            this.focusManager.setFocus(0);
                        }
                    }, TVNavigationConfig.UPDATE_DEBOUNCE_DELAY);
                }
                // Handle Bootstrap dropdown prevention
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const element = node;
                        if (element.classList?.contains('dropdown-menu') && element.classList?.contains('show')) {
                            if (!element.classList.contains('tv-dropdown-open')) {
                                element.classList.remove('show');
                            }
                        }
                    }
                });
            });
        });
        this.observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['style', 'class']
        });
    }
    /**
     * Start TV navigation mode
     */
    startTVNavigation() {
        if (!this.tvDetection.getTVStatus())
            return;
        this.navigationActive = true;
        document.body.style.cursor = 'none';
        this.elementManager.updateFocusableElements();
        const focusableElements = this.elementManager.getFocusableElements();
        if (focusableElements.length > 0) {
            this.focusManager.setFocus(0);
        }
        this.carouselNav.updateCarouselIndicators();
    }
    /**
     * Stop TV navigation mode
     */
    stopTVNavigation() {
        this.navigationActive = false;
        document.body.style.cursor = 'auto';
        // Remove all focus indicators
        const focusableElements = this.elementManager.getFocusableElements();
        focusableElements.forEach(el => {
            el.classList.remove('tv-focused');
            el.style.border = '';
            el.style.boxShadow = '';
            el.style.zIndex = '';
        });
    }
    /**
     * Handle keyboard input from TV remote
     * @param event - Keyboard event
     */
    handleKeydown(event) {
        // Only handle navigation if we're in TV mode and navigation is active
        if (!this.tvDetection.getTVStatus() || !this.navigationActive)
            return;
        // Don't interfere with video player controls
        if (document.activeElement && document.activeElement.closest('.video-js')) {
            return;
        }
        // Only handle keydown events
        if (event.type !== 'keydown')
            return;
        const normalizedKey = this.keyHandler.normalizeKey(event);
        if (!normalizedKey)
            return;
        // Prevent default for recognized TV remote keys
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
        this.processNavigationCommand(normalizedKey);
    }
    /**
     * Process navigation command based on normalized key
     * @param key - Normalized key command
     */
    processNavigationCommand(key) {
        const currentElement = this.focusManager.getCurrentElement();
        switch (key) {
            case 'ArrowDown':
                this.handleDownNavigation(currentElement);
                break;
            case 'ArrowUp':
                this.handleUpNavigation(currentElement);
                break;
            case 'ArrowRight':
            case 'ArrowLeft':
                this.handleHorizontalNavigation(key, currentElement);
                break;
            case 'Enter':
            case ' ':
                this.handleActivation(currentElement);
                break;
            case 'Escape':
                this.handleEscape();
                break;
        }
    }
    /**
     * Handle downward navigation
     * @param currentElement - Currently focused element
     */
    handleDownNavigation(currentElement) {
        const isDropdownToggle = this.dropdownManager.isDropdownToggle(currentElement);
        const isDropdownOpen = currentElement ? this.dropdownManager.isDropdownOpen(currentElement) : false;
        if (isDropdownToggle && !isDropdownOpen) {
            // Navigate instead of opening dropdown
            const nextIndex = this.findAlternativeDownNavigation();
            if (nextIndex !== -1) {
                this.focusManager.setFocus(nextIndex);
            }
        }
        else {
            const nextIndex = this.directionalNav.findNextInDirection('down');
            if (nextIndex !== -1) {
                this.focusManager.setFocus(nextIndex);
            }
        }
    }
    /**
     * Handle upward navigation
     * @param currentElement - Currently focused element
     */
    handleUpNavigation(_currentElement) {
        const nextIndex = this.directionalNav.findNextInDirection('up');
        if (nextIndex !== -1) {
            this.focusManager.setFocus(nextIndex);
        }
    }
    /**
     * Handle horizontal navigation
     * @param direction - 'ArrowLeft' or 'ArrowRight'
     * @param currentElement - Currently focused element
     */
    handleHorizontalNavigation(direction, currentElement) {
        // Close dropdown if moving horizontally
        if (currentElement && this.dropdownManager.isDropdownToggle(currentElement) && this.dropdownManager.isDropdownOpen(currentElement)) {
            this.dropdownManager.closeAllDropdowns();
        }
        const navDirection = direction === 'ArrowRight' ? 'right' : 'left';
        let nextIndex = this.directionalNav.findNextInDirection(navDirection);
        // If normal navigation fails and we're in a carousel, try slide navigation
        if (nextIndex === -1 && currentElement?.closest('.carousel')) {
            const slideChanged = this.carouselNav.navigateCarouselSlide(navDirection);
            if (slideChanged) {
                return;
            }
        }
        if (nextIndex !== -1) {
            this.focusManager.setFocus(nextIndex);
        }
    }
    /**
     * Handle activation (Enter/Space)
     * @param currentElement - Currently focused element
     */
    handleActivation(currentElement) {
        if (!currentElement)
            return;
        if (this.dropdownManager.isDropdownToggle(currentElement)) {
            this.dropdownManager.toggleDropdown(currentElement);
        }
        else {
            this.activateElement(currentElement);
        }
    }
    /**
     * Handle escape key
     */
    handleEscape() {
        const openDropdowns = document.querySelectorAll('.dropdown-menu.tv-dropdown-open');
        if (openDropdowns.length > 0) {
            this.dropdownManager.closeAllDropdowns();
        }
        else {
            window.history.back();
        }
    }
    /**
     * Activate an element (click it)
     * @param element - Element to activate
     */
    activateElement(element) {
        console.log('Enter pressed on element:', element);
        // Enhanced click handling for carousel items
        if (element.classList.contains('thumbnail') || element.classList.contains('thumbnail-home')) {
            const linkElement = this.findClickableElement(element);
            if (linkElement) {
                if (linkElement.hasAttribute('href')) {
                    const href = linkElement.getAttribute('href');
                    if (href) {
                        console.log('Navigating to:', href);
                        window.location.href = href;
                    }
                }
                else {
                    console.log('Clicking element:', linkElement);
                    linkElement.click();
                }
            }
            else {
                console.log('No link found, clicking thumbnail directly');
                element.click();
            }
        }
        else {
            console.log('Normal click on:', element);
            element.click();
        }
    }
    /**
     * Find clickable element within a thumbnail
     * @param thumbnailElement - Thumbnail element to search
     * @returns Clickable element or null
     */
    findClickableElement(thumbnailElement) {
        // Try to find a link within the thumbnail
        let linkElement = thumbnailElement.querySelector('a[href]');
        // If no link inside, check if the thumbnail itself is a link
        if (!linkElement && thumbnailElement.tagName === 'A') {
            linkElement = thumbnailElement;
        }
        // If no direct link, check if parent is a link
        if (!linkElement) {
            linkElement = thumbnailElement.closest('a[href]');
        }
        // If still no link, try to find any clickable element inside
        if (!linkElement) {
            linkElement = thumbnailElement.querySelector('[onclick], [data-bs-toggle], button');
        }
        return linkElement;
    }
    /**
     * Find alternative navigation for dropdown scenarios
     * @returns Next element index or -1
     */
    findAlternativeDownNavigation() {
        const currentFocusIndex = this.focusManager.getCurrentFocusIndex();
        const focusableElements = this.elementManager.getFocusableElements();
        const currentElement = focusableElements[currentFocusIndex];
        for (let i = currentFocusIndex + 1; i < focusableElements.length; i++) {
            const candidate = focusableElements[i];
            const candidateSection = this.directionalNav.getElementSection(candidate);
            const currentSection = this.directionalNav.getElementSection(currentElement);
            if (candidateSection !== currentSection) {
                return i;
            }
        }
        return -1;
    }
    /**
     * Expose debug functions for development
     */
    exposeDebugInterface() {
        const debugInterface = {
            start: () => {
                this.tvDetection.isTV = true;
                this.startTVNavigation();
            },
            stop: () => {
                this.tvDetection.isTV = false;
                this.stopTVNavigation();
            },
            showElements: () => {
                this.elementManager.updateFocusableElements();
                const elements = this.elementManager.getFocusableElements();
                elements.forEach((el, index) => {
                    const rect = el.getBoundingClientRect();
                    const section = this.directionalNav.getElementSection(el);
                    console.log(`Element ${index}: ${el.tagName} in ${section} at (${rect.left}, ${rect.top})`);
                });
            },
            focusElement: (index) => {
                const elements = this.elementManager.getFocusableElements();
                if (index >= 0 && index < elements.length) {
                    this.focusManager.setFocus(index);
                }
            }
        };
        window.debugTVNavigation = debugInterface;
        // Keyboard shortcut for debug mode
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.altKey && e.key === 't') {
                if (this.navigationActive) {
                    debugInterface.stop();
                }
                else {
                    debugInterface.start();
                }
            }
        });
    }
}
// Initialize TV Navigation when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    const tvNav = new TVNavigationController();
    tvNav.exposeDebugInterface();
});
export { TVNavigationController, TVDetectionManager, TVKeyHandler, FocusableElementManager, FocusManager, DirectionalNavigator, CarouselNavigator, DropdownManager, TVNavigationConfig, TVKeyMappings };
//# sourceMappingURL=tvNavigation.js.map