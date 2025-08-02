/**
 * TV Remote Navigation Enhancement
 * Provides native app-like navigation using arrow keys/remote control
 */

document.addEventListener('DOMContentLoaded', function() {
    let isTV = false;
    let currentFocusIndex = 0;
    let focusableElements = [];
    let navigationActive = false;
    
    // Detect TV browsers:
    function updateTVStatus() {
        if (window.tvDetection && typeof window.tvDetection.isTV === 'function') {
            isTV = window.tvDetection.isTV();
        } else {
            // Enhanced TV detection based on user agent
            const userAgent = navigator.userAgent.toLowerCase();
            const isSamsungTV = userAgent.includes('tizen') || userAgent.includes('samsung');
            const isFireTV = userAgent.includes('silk') || userAgent.includes('afts');
            const isLGTV = userAgent.includes('webos') || userAgent.includes('netcast');

            isTV = isSamsungTV || isFireTV || isLGTV ||
                userAgent.includes('smart-tv') ||
                userAgent.includes('smarttv') ||
                userAgent.includes('roku') ||
                userAgent.includes('googletv') ||
                userAgent.includes('operatv') ||
                (window.navigator.maxTouchPoints === 0 && window.screen.width >= 1920);
        }

        console.log('Enhanced TV Detection:', {
            isTV: isTV,
            userAgent: navigator.userAgent,
            isSamsung: navigator.userAgent.toLowerCase().includes('tizen'),
            isFireTV: navigator.userAgent.toLowerCase().includes('silk'),
            isLG: navigator.userAgent.toLowerCase().includes('webos')
        });
        
        // Force start TV navigation if detected
        if (isTV) {
            setTimeout(() => {
                startTVNavigation();
            }, 1000);
        }

        return isTV;
    }    
    // Initial TV status check
    updateTVStatus();
    
    // Remove any existing listeners first
    document.removeEventListener('keydown', handleKeydown);

    // Add multiple event types for better TV compatibility
    document.addEventListener('keydown', handleKeydown, true);
    document.addEventListener('keyup', handleKeydown, true);
    document.addEventListener('keypress', handleKeydown, true);

    /**
     * Updates the list of focusable elements on the page
     */
    function updateFocusableElements() {
        // Get all potential focusable elements - REMOVED carousel controls
        const allElements = Array.from(document.querySelectorAll(
            'a[href], button:not([disabled]), .thumbnail, .thumbnail-home, .video-js, input:not([disabled]), [tabindex]:not([tabindex="-1"])'
        ));
        
        // Filter out elements that are not actually focusable or are nested
        focusableElements = allElements.filter(el => {
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            
            // Basic visibility checks
            if (rect.width <= 0 || rect.height <= 0 || 
                style.visibility === 'hidden' || 
                style.display === 'none' ||
                el.hasAttribute('disabled')) {
                return false;
            }
            
            // Exclude carousel controls completely
            if (el.classList.contains('carousel-control-prev') || 
                el.classList.contains('carousel-control-next')) {
                return false;
            }
            
            // Prevent nested thumbnail elements (only keep the outermost one)
            if (el.classList.contains('thumbnail') || el.classList.contains('thumbnail-home')) {
                // Check if this element has a parent that's also a thumbnail
                const parentThumbnail = el.parentElement?.closest('.thumbnail, .thumbnail-home');
                if (parentThumbnail && parentThumbnail !== el) {
                    return false; // Skip nested thumbnail
                }
                
                // Also check if this element contains other thumbnails (keep the container)
                const childThumbnails = el.querySelectorAll('.thumbnail, .thumbnail-home');
                if (childThumbnails.length > 0) {
                    return false; // Skip containers, we'll get the actual thumbnails
                }
            }
            
            return true;
        });
        
        // Custom sorting that handles navbar, carousels, and profile correctly
        focusableElements.sort((a, b) => {
            const rectA = a.getBoundingClientRect();
            const rectB = b.getBoundingClientRect();
            
            // Define sections with priorities
            const getSectionPriority = (el) => {
                if (el.closest('.navbar')) return 1;
                if (el.closest('[id*="profile"]') || el.getAttribute('href')?.includes('profile')) return 2;
                if (el.closest('.carousel')) return 3;
                return 4; // Other elements (including non-carousel sections)
            };
            
            const priorityA = getSectionPriority(a);
            const priorityB = getSectionPriority(b);
            
            // Sort by section priority first
            if (priorityA !== priorityB) {
                return priorityA - priorityB;
            }
            
            // Within same section, sort by position
            const verticalDiff = rectA.top - rectB.top;
            if (Math.abs(verticalDiff) > 50) { // 50px threshold for "same row"
                return verticalDiff;
            }
            
            // If roughly same row, sort by horizontal position
            return rectA.left - rectB.left;
        });
        
        // Debug: Log elements to see what we found
        focusableElements.forEach((el, index) => {
            const rect = el.getBoundingClientRect();
            const section = el.closest('.navbar') ? 'navbar' : 
                           el.closest('.carousel') ? 'carousel' : 
                           el.closest('[id*="profile"]') ? 'profile' : 'other';
        });
        
        // Add visual focus indicators and make everything tabbable
        focusableElements.forEach((el, index) => {
            el.setAttribute('data-tv-index', index);
            el.setAttribute('tabindex', '0');
            el.style.outline = 'none';
        });
    }


    /**
     * Sets focus on a specific element by index
     */
    function setFocus(index) {
        if (!isTV || !navigationActive) return;
        
        // Remove previous focus
        focusableElements.forEach(el => {
            el.classList.remove('tv-focused');
            el.style.border = '';
            el.style.boxShadow = '';
        });
        
        // Set new focus
        if (focusableElements[index]) {
            const element = focusableElements[index];
            currentFocusIndex = index;
            
            // Add strong visual focus
            element.classList.add('tv-focused');
            element.style.border = '4px solid #ff6b35';
            element.style.boxShadow = '0 0 20px rgba(255, 107, 53, 0.8)';
            element.style.transition = 'all 0.2s ease';
            element.style.zIndex = '1000';
            
            // Scroll into view
            element.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center',
                inline: 'center'
            });
            
            // Give it actual focus for screen readers
            element.focus();
            
            // Update carousel indicators
            updateCarouselIndicators();
        }
    }


    /**
     * Find the next focusable element in a direction with section awareness
     */
    function findNextInDirection(direction) {
        if (focusableElements.length === 0) return -1;
        
        const current = focusableElements[currentFocusIndex];
        if (!current) return 0;
        
        const currentRect = current.getBoundingClientRect();
        const currentY = currentRect.top + currentRect.height / 2;
        const currentX = currentRect.left + currentRect.width / 2;
        
        // Improved section detection
        function getElementSection(el) {
            if (el.closest('.navbar')) return 'navbar';
            if (el.closest('[id*="profile"]') || el.getAttribute('href')?.includes('profile')) return 'profile';
            if (el.closest('.carousel')) return 'carousel';
            
            // Check for specific content sections
            if (el.closest('[class*="news"]') || el.closest('[id*="news"]')) return 'news';
            if (el.closest('[class*="program"]') || el.closest('[id*="program"]')) return 'program';
            if (el.closest('.container') || el.closest('.row') || el.closest('.col')) return 'content';
            
            return 'other';
        }
        
        const currentSection = getElementSection(current);
        const currentCarousel = current.closest('.carousel');
        
        let bestMatch = -1;
        let bestDistance = Infinity;
        
        focusableElements.forEach((el, index) => {
            if (index === currentFocusIndex) return;
            
            const rect = el.getBoundingClientRect();
            const elY = rect.top + rect.height / 2;
            const elX = rect.left + rect.width / 2;
            
            const elSection = getElementSection(el);
            const elCarousel = el.closest('.carousel');
            
            let isInDirection = false;
            let distance = 0;
            
            switch(direction) {
                case 'down':
                    // Down should move to next section or next row in same section
                    isInDirection = elY > currentY + 30;
                    distance = Math.abs(elY - currentY) + Math.abs(elX - currentX) * 0.2;
                    
                    // Prefer moving to different sections when going down
                    if (currentSection === 'navbar' && elSection !== 'navbar') {
                        distance *= 0.3; // Strong preference for leaving navbar
                    } else if (currentSection === elSection && currentCarousel && elCarousel && currentCarousel === elCarousel) {
                        distance *= 2; // Discourage staying in same carousel
                    }
                    break;
                    
                case 'up':
                    // Up should move to previous section or previous row in same section
                    isInDirection = elY < currentY - 30;
                    distance = Math.abs(elY - currentY) + Math.abs(elX - currentX) * 0.2;
                    
                    // Improved section preference logic for upward navigation
                    if (currentSection === 'content' || currentSection === 'news' || currentSection === 'program') {
                        // From content areas, prefer moving to other content first, then navbar
                        if (elSection === currentSection) {
                            distance *= 0.8; // Prefer same content section
                        } else if (elSection === 'carousel') {
                            distance *= 0.9; // Then prefer carousels
                        } else if (elSection === 'navbar') {
                            distance *= 1.5; // Navbar is lower priority unless nothing else works
                        }
                    } else if (currentSection === 'carousel') {
                        // From carousel, prefer moving to content areas above, not directly to navbar
                        if (elSection === 'content' || elSection === 'news' || elSection === 'program') {
                            distance *= 0.7; // Strong preference for content areas
                        } else if (elSection === 'carousel') {
                            // If we're in same carousel, prefer elements that are actually above
                            if (currentCarousel === elCarousel) {
                                distance *= 1; // Normal preference for same carousel
                            } else {
                                distance *= 2; // Discourage different carousel unless closer
                            }
                        } else if (elSection === 'navbar') {
                            distance *= 3; // Discourage jumping directly to navbar from carousel
                        }
                    } else if (currentSection === 'navbar') {
                        // From navbar, stay in navbar if possible
                        if (elSection === 'navbar') {
                            distance *= 0.5; // Strong preference for staying in navbar
                        }
                    }
                    
                    // Special handling to avoid jumping to specific buttons unless they're the best option
                    if (el.textContent?.toLowerCase().includes('tv mode') || 
                        el.textContent?.toLowerCase().includes('toggle') ||
                        el.classList.contains('btn-outline-secondary')) {
                        distance *= 5; // Make these buttons much less preferred unless nothing else
                    }
                    break;

                case 'right':
                    // Right should ONLY move within the same logical section/carousel
                    if (currentSection === 'navbar' && elSection !== 'navbar') {
                        return; // Don't leave navbar on horizontal movement
                    }
                    
                    if (currentSection === 'carousel') {
                        // For carousel, must be EXACT same carousel instance
                        if (elSection !== 'carousel' || currentCarousel !== elCarousel) {
                            return; // Don't leave current carousel on horizontal movement
                        }
                        
                        // Additional check: must be roughly same horizontal row within carousel
                        if (Math.abs(elY - currentY) > 30) {
                            return; // Don't jump to different rows within same carousel
                        }
                    }
                    
                    // For other content areas, be very strict about staying in same row
                    if (currentSection === 'content' || currentSection === 'news' || currentSection === 'program') {
                        // Must be same section AND roughly same vertical position
                        if (elSection !== currentSection || Math.abs(elY - currentY) > 50) {
                            return; // Don't jump to different sections or rows horizontally
                        }
                    }
                    
                    isInDirection = elX > currentX + 10;
                    distance = Math.abs(elX - currentX) + Math.abs(elY - currentY) * 0.1;
                    break;

                case 'left':
                    // Left should ONLY move within the same logical section/carousel
                    if (currentSection === 'navbar' && elSection !== 'navbar') {
                        return; // Don't leave navbar on horizontal movement
                    }
                    
                    if (currentSection === 'carousel') {
                        // For carousel, must be EXACT same carousel instance
                        if (elSection !== 'carousel' || currentCarousel !== elCarousel) {
                            return; // Don't leave current carousel on horizontal movement
                        }
                        
                        // Additional check: must be roughly same horizontal row within carousel
                        if (Math.abs(elY - currentY) > 30) {
                            return; // Don't jump to different rows within same carousel
                        }
                    }
                
                    // For other content areas, be very strict about staying in same row
                    if (currentSection === 'content' || currentSection === 'news' || currentSection === 'program') {
                        // Must be same section AND roughly same vertical position
                        if (elSection !== currentSection || Math.abs(elY - currentY) > 50) {
                            return; // Don't jump to different sections or rows horizontally
                        }
                    }
                    
                    isInDirection = elX < currentX - 10;
                    distance = Math.abs(elX - currentX) + Math.abs(elY - currentY) * 0.1;
                    break;
            }
            
            if (isInDirection && distance < bestDistance) {
                bestDistance = distance;
                bestMatch = index;
            }
        });
        
        return bestMatch;
    }

    /**
     * Start TV navigation
     */
    function startTVNavigation() {
        if (!isTV) return;
        
        navigationActive = true;
        document.body.style.cursor = 'none';
        
        updateFocusableElements();
        if (focusableElements.length > 0) {
            setFocus(0);
        }
            
        // Initialize carousel indicators
        updateCarouselIndicators();
    }
    
    /**
     * Stop TV navigation
     */
    function stopTVNavigation() {
        navigationActive = false;
        document.body.style.cursor = 'auto';
        
        // Remove all focus indicators
        focusableElements.forEach(el => {
            el.classList.remove('tv-focused');
            el.style.border = '';
            el.style.boxShadow = '';
            el.style.zIndex = '';
        });
    }
    

    /**
     * Keyboard event handler
     */
    function handleKeydown(e) {
        // Only handle navigation if we're in TV mode and navigation is active
        if (!isTV || !navigationActive) return;
        
        // Don't interfere with video player controls when it has focus
        if (document.activeElement && document.activeElement.closest('.video-js')) {
            return;
        }

        // For TV remotes, we want to handle keydown events, but prevent default behavior
        if (e.type !== 'keydown') return;

        let nextIndex = -1;
        const currentElement = focusableElements[currentFocusIndex];

        // Enhanced key mapping for TV remotes
        let normalizedKey = null;

        console.log('Raw key event:', {
            type: e.type,
            key: e.key,
            keyCode: e.keyCode,
            which: e.which,
            code: e.code,
            userAgent: navigator.userAgent.substring(0, 100)
        });

        // Standard keyboard codes
        if (e.keyCode === 37 || e.code === 'ArrowLeft' || e.key === 'ArrowLeft') normalizedKey = 'ArrowLeft';
        if (e.keyCode === 38 || e.code === 'ArrowUp' || e.key === 'ArrowUp') normalizedKey = 'ArrowUp';
        if (e.keyCode === 39 || e.code === 'ArrowRight' || e.key === 'ArrowRight') normalizedKey = 'ArrowRight';
        if (e.keyCode === 40 || e.code === 'ArrowDown' || e.key === 'ArrowDown') normalizedKey = 'ArrowDown';
        if (e.keyCode === 13 || e.code === 'Enter' || e.key === 'Enter') normalizedKey = 'Enter';
        if (e.keyCode === 27 || e.code === 'Escape' || e.key === 'Escape') normalizedKey = 'Escape';
        if (e.keyCode === 32 || e.code === 'Space' || e.key === ' ') normalizedKey = ' ';
        
        // Samsung TV remote key mappings (Tizen)
        if (e.keyCode === 4 || e.keyCode === 10009) normalizedKey = 'Escape';     // Back/Return
        if (e.keyCode === 10252 || e.keyCode === 415) normalizedKey = ' ';        // Play/Pause
        if (e.keyCode === 10182) normalizedKey = 'Enter';                         // OK/Select
        
        // Fire TV / Amazon remote key mappings
        if (e.keyCode === 21) normalizedKey = 'ArrowLeft';    // DPAD_LEFT
        if (e.keyCode === 19) normalizedKey = 'ArrowUp';      // DPAD_UP  
        if (e.keyCode === 22) normalizedKey = 'ArrowRight';   // DPAD_RIGHT
        if (e.keyCode === 20) normalizedKey = 'ArrowDown';    // DPAD_DOWN
        if (e.keyCode === 23) normalizedKey = 'Enter';        // DPAD_CENTER
        
        // WebOS (LG TV) key mappings
        if (e.keyCode === 461) normalizedKey = 'Escape';      // BACK
        if (e.keyCode === 13) normalizedKey = 'Enter';        // OK
        
        // Additional TV remote codes from various manufacturers
        if (e.keyCode === 166) normalizedKey = 'Escape';      // Back (some TVs)
        if (e.keyCode === 8) normalizedKey = 'Escape';        // Backspace (sometimes used as back)
        
        console.log('Normalized key:', normalizedKey);

        // If we don't recognize the key, ignore it
        if (!normalizedKey) return;

        // Always prevent default for recognized TV remote keys
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();

        // Check if current element is a dropdown toggle
        const isDropdownToggle = currentElement && (
            currentElement.hasAttribute('data-bs-toggle') && currentElement.getAttribute('data-bs-toggle') === 'dropdown' ||
            currentElement.classList.contains('dropdown-toggle') ||
            currentElement.getAttribute('role') === 'button' && currentElement.getAttribute('aria-haspopup') === 'true'
        );
        
        // Check if a dropdown is currently open
        const openDropdown = currentElement?.nextElementSibling?.classList.contains('tv-dropdown-open');
        
        switch(e.key) {
            case 'ArrowDown':
                // Only prevent dropdown expansion if dropdown is CLOSED
                if (isDropdownToggle && !openDropdown) {
                    // e.preventDefault();
                    // e.stopPropagation();
                    // e.stopImmediatePropagation();
                    
                    // Force close any dropdown that might be opening
                    const dropdownMenu = currentElement.nextElementSibling;
                    if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
                        dropdownMenu.classList.remove('show', 'tv-dropdown-open');
                    }
                    
                    // Navigate normally instead of opening dropdown
                    nextIndex = findNextInDirection('down');
                    
                    // If no directional match, try next element that's in a different section
                    if (nextIndex === -1) {
                        for (let i = currentFocusIndex + 1; i < focusableElements.length; i++) {
                            const candidate = focusableElements[i];
                            const candidateSection = candidate.closest('.navbar') ? 'navbar' : 
                                                   candidate.closest('.carousel') ? 'carousel' : 
                                                   candidate.closest('[id*="profile"]') ? 'profile' : 'other';
                            const currentSection = currentElement?.closest('.navbar') ? 'navbar' : 
                                                 currentElement?.closest('.carousel') ? 'carousel' : 
                                                 currentElement?.closest('[id*="profile"]') ? 'profile' : 'other';
                            
                            if (candidateSection !== currentSection) {
                                nextIndex = i;
                                break;
                            }
                        }
                    }
                    break;
                }
                
                // If dropdown is open, navigate to first dropdown item
                if (isDropdownToggle && openDropdown) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const dropdownMenu = currentElement.nextElementSibling;
                    if (dropdownMenu) {
                        const firstDropdownItem = dropdownMenu.querySelector('.dropdown-item, a[href]');
                        if (firstDropdownItem) {
                            // Add the dropdown item to focusable elements temporarily
                            const dropdownItems = Array.from(dropdownMenu.querySelectorAll('.dropdown-item, a[href]'));
                            dropdownItems.forEach(item => {
                                if (!focusableElements.includes(item)) {
                                    // Insert dropdown items right after the toggle
                                    const toggleIndex = focusableElements.indexOf(currentElement);
                                    focusableElements.splice(toggleIndex + 1, 0, item);
                                    item.setAttribute('data-tv-index', toggleIndex + 1);
                                    item.setAttribute('tabindex', '0');
                                    item.style.outline = 'none';
                                }
                            });
                            
                            // Focus the first dropdown item
                            const firstItemIndex = focusableElements.indexOf(firstDropdownItem);
                            if (firstItemIndex !== -1) {
                                nextIndex = firstItemIndex;
                            }
                        }
                    }
                    break;
                }
                
                // Normal down navigation
                e.preventDefault();
                e.stopPropagation();
                
                nextIndex = findNextInDirection('down');
                
                // If no directional match, try next element that's in a different section
                if (nextIndex === -1) {
                    for (let i = currentFocusIndex + 1; i < focusableElements.length; i++) {
                        const candidate = focusableElements[i];
                        const candidateSection = candidate.closest('.navbar') ? 'navbar' : 
                                               candidate.closest('.carousel') ? 'carousel' : 
                                               candidate.closest('[id*="profile"]') ? 'profile' : 'other';
                        const currentSection = currentElement?.closest('.navbar') ? 'navbar' : 
                                             currentElement?.closest('.carousel') ? 'carousel' : 
                                             currentElement?.closest('[id*="profile"]') ? 'profile' : 'other';
                        
                        if (candidateSection !== currentSection) {
                            nextIndex = i;
                            break;
                        }
                    }
                }
                break;
                
            case 'ArrowUp':
                // If we're on a dropdown item, allow moving up within dropdown or back to toggle
                if (currentElement?.closest('.dropdown-menu')) {
                    // e.preventDefault();
                    // e.stopPropagation();
                    
                    // Find previous dropdown item or go back to toggle
                    nextIndex = findNextInDirection('up');
                    
                    // If no previous dropdown item, go back to the dropdown toggle
                    if (nextIndex === -1) {
                        const dropdownMenu = currentElement.closest('.dropdown-menu');
                        const dropdownToggle = dropdownMenu?.previousElementSibling;
                        if (dropdownToggle && focusableElements.includes(dropdownToggle)) {
                            nextIndex = focusableElements.indexOf(dropdownToggle);
                        }
                    }
                    break;
                }
                
                // Only prevent dropdown expansion if dropdown is CLOSED
                if (isDropdownToggle && !openDropdown) {
                    e.preventDefault();
                    e.stopPropagation();
                    e.stopImmediatePropagation();
                    
                    // Force close any dropdown that might be opening
                    const dropdownMenu = currentElement.nextElementSibling;
                    if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
                        dropdownMenu.classList.remove('show', 'tv-dropdown-open');
                    }
                    
                    // Navigate normally
                    nextIndex = findNextInDirection('up');
                    
                    // If no directional match, try previous element that's in a different section
                    if (nextIndex === -1) {
                        for (let i = currentFocusIndex - 1; i >= 0; i--) {
                            const candidate = focusableElements[i];
                            const candidateSection = candidate.closest('.navbar') ? 'navbar' : 
                                                   candidate.closest('.carousel') ? 'carousel' : 
                                                   candidate.closest('[id*="profile"]') ? 'profile' : 'other';
                            const currentSection = currentElement?.closest('.navbar') ? 'navbar' : 
                                                 currentElement?.closest('.carousel') ? 'carousel' : 
                                                 currentElement?.closest('[id*="profile"]') ? 'profile' : 'other';
                            
                            if (candidateSection !== currentSection) {
                                nextIndex = i;
                                break;
                            }
                        }
                    }
                    break;
                }
                
                // Normal up navigation
                e.preventDefault();
                e.stopPropagation();
                
                nextIndex = findNextInDirection('up');
                
                // If no directional match, try previous element that's in a different section
                if (nextIndex === -1) {
                    for (let i = currentFocusIndex - 1; i >= 0; i--) {
                        const candidate = focusableElements[i];
                        const candidateSection = candidate.closest('.navbar') ? 'navbar' : 
                                               candidate.closest('.carousel') ? 'carousel' : 
                                               candidate.closest('[id*="profile"]') ? 'profile' : 'other';
                        const currentSection = currentElement?.closest('.navbar') ? 'navbar' : 
                                             currentElement?.closest('.carousel') ? 'carousel' : 
                                             currentElement?.closest('[id*="profile"]') ? 'profile' : 'other';
                        
                        if (candidateSection !== currentSection) {
                            nextIndex = i;
                            break;
                        }
                    }
                }
                break;
                
            case 'ArrowRight':
            case 'ArrowLeft':
                // Close dropdown if moving horizontally
                if (isDropdownToggle && openDropdown) {
                    const dropdownMenu = currentElement.nextElementSibling;
                    if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
                        dropdownMenu.classList.remove('tv-dropdown-open', 'show');
                        
                        // Remove dropdown items from focusable elements
                        const dropdownItems = Array.from(dropdownMenu.querySelectorAll('.dropdown-item, a[href]'));
                        dropdownItems.forEach(item => {
                            const index = focusableElements.indexOf(item);
                            if (index !== -1) {
                                focusableElements.splice(index, 1);
                            }
                        });
                    }
                }
                
                // Normal horizontal navigation
                // e.preventDefault();
                // e.stopPropagation();
                
                const direction = e.key === 'ArrowRight' ? 'right' : 'left';
                console.log('Horizontal navigation:', direction);
                
                // FIRST: Try normal directional navigation within current slide/section
                nextIndex = findNextInDirection(direction);
                console.log('Normal navigation result:', nextIndex);
                
                // ONLY if normal navigation fails AND we're in a carousel, try slide navigation
                if (nextIndex === -1 && currentElement?.closest('.carousel')) {
                    console.log('Normal navigation failed, trying slide navigation');
                    const slideChanged = navigateCarouselSlide(direction);
                    console.log('Slide changed:', slideChanged);
                    if (slideChanged) {
                        // Carousel handled it (either moved slide or stayed at edge)
                        console.log('Carousel handled, exiting');
                        return; // Exit completely, don't try any other navigation
                    }
                }
                
                // If normal navigation found something, use it
                // If it didn't find anything and we're not in a carousel, nextIndex stays -1
                break;

            case 'Enter':
            case ' ':
                // e.preventDefault();
                // e.stopPropagation();
                if (currentElement) {
                    // For dropdown toggles, manually control dropdown
                    if (isDropdownToggle) {
                        const dropdownMenu = currentElement.nextElementSibling;
                        if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
                            // Toggle our custom TV dropdown class
                            if (dropdownMenu.classList.contains('tv-dropdown-open')) {
                                dropdownMenu.classList.remove('tv-dropdown-open', 'show');
                                
                                // Remove dropdown items from focusable elements
                                const dropdownItems = Array.from(dropdownMenu.querySelectorAll('.dropdown-item, a[href]'));
                                dropdownItems.forEach(item => {
                                    const index = focusableElements.indexOf(item);
                                    if (index !== -1) {
                                        focusableElements.splice(index, 1);
                                    }
                                });
                            } else {
                                // Close any other open dropdowns first
                                document.querySelectorAll('.dropdown-menu.tv-dropdown-open').forEach(menu => {
                                    menu.classList.remove('tv-dropdown-open', 'show');
                                });
                                
                                // Open this dropdown
                                dropdownMenu.classList.add('tv-dropdown-open', 'show');
                            }
                        }
                    } else {
                        // Enhanced click handling for carousel items
                        console.log('Enter pressed on element:', currentElement);
                        
                        // Check if this is a carousel thumbnail
                        if (currentElement.classList.contains('thumbnail') || 
                            currentElement.classList.contains('thumbnail-home')) {
                            
                            // Try to find a link within the thumbnail
                            let linkElement = currentElement.querySelector('a[href]');
                            
                            // If no link inside, check if the thumbnail itself is a link
                            if (!linkElement && currentElement.tagName === 'A') {
                                linkElement = currentElement;
                            }
                            
                            // If no direct link, check if parent is a link
                            if (!linkElement) {
                                linkElement = currentElement.closest('a[href]');
                            }
                            
                            // If still no link, try to find any clickable element inside
                            if (!linkElement) {
                                linkElement = currentElement.querySelector('[onclick], [data-bs-toggle], button');
                            }
                            
                            console.log('Found link element:', linkElement);
                            
                            if (linkElement) {
                                // If it's a link, navigate to it
                                if (linkElement.href) {
                                    console.log('Navigating to:', linkElement.href);
                                    window.location.href = linkElement.href;
                                } else {
                                    // If it's a button or has onclick, click it
                                    console.log('Clicking element:', linkElement);
                                    linkElement.click();
                                }
                            } else {
                                // Fallback: try clicking the thumbnail itself
                                console.log('No link found, clicking thumbnail directly');
                                currentElement.click();
                            }
                        } else {
                            // For non-carousel items, use normal click
                            console.log('Normal click on:', currentElement);
                            currentElement.click();
                        }
                    }
                }
                break;

            case 'Escape':
                // e.preventDefault();
                // e.stopPropagation();
                
                // Close any open TV dropdowns first
                const openTVDropdowns = document.querySelectorAll('.dropdown-menu.tv-dropdown-open');
                if (openTVDropdowns.length > 0) {
                    openTVDropdowns.forEach(dropdown => {
                        dropdown.classList.remove('tv-dropdown-open', 'show');
                        
                        // Remove dropdown items from focusable elements
                        const dropdownItems = Array.from(dropdown.querySelectorAll('.dropdown-item, a[href]'));
                        dropdownItems.forEach(item => {
                            const index = focusableElements.indexOf(item);
                            if (index !== -1) {
                                focusableElements.splice(index, 1);
                            }
                        });
                    });
                    
                    // Focus back to the dropdown toggle
                    const dropdownToggle = document.querySelector('.dropdown-toggle.tv-focused');
                    if (dropdownToggle) {
                        const toggleIndex = focusableElements.indexOf(dropdownToggle);
                        if (toggleIndex !== -1) {
                            setFocus(toggleIndex);
                        }
                    }
                } else {
                    window.history.back();
                }
                break;
        }
        
        if (nextIndex !== -1) {
            setFocus(nextIndex);
        }
    }


    /**
     * Navigate to next/previous carousel slide when reaching the edge
     * @param {string} direction - 'right' or 'left'
     */
    function navigateCarouselSlide(direction) {
        const currentElement = focusableElements[currentFocusIndex];
        const currentCarousel = currentElement?.closest('.carousel');
        
        if (!currentCarousel) {
            console.log('navigateCarouselSlide: Not in carousel');
            return false;
        }
        
        console.log('navigateCarouselSlide: Direction =', direction, 'from element:', currentElement);
        
        // Get carousel instance
        const carouselInstance = bootstrap.Carousel.getInstance(currentCarousel) || new bootstrap.Carousel(currentCarousel);
        
        // Get current slide and ALL visible thumbnails in that slide
        const currentSlide = currentCarousel.querySelector('.carousel-item.active');
        const visibleThumbnails = Array.from(currentSlide.querySelectorAll('.thumbnail, .thumbnail-home'));
        const currentIndex = visibleThumbnails.indexOf(currentElement);
        
        console.log('navigateCarouselSlide: Found', visibleThumbnails.length, 'thumbnails, current at index:', currentIndex);
        
        if (direction === 'right') {
            // Only advance slide if we're at the actual LAST visible item
            if (currentIndex === visibleThumbnails.length - 1) {
                const slides = currentCarousel.querySelectorAll('.carousel-item');
                const activeSlide = currentCarousel.querySelector('.carousel-item.active');
                const activeIndex = Array.from(slides).indexOf(activeSlide);
                
                console.log('navigateCarouselSlide: At last item. Slide', activeIndex + 1, 'of', slides.length);
                
                if (activeIndex < slides.length - 1) {
                    console.log('navigateCarouselSlide: Moving to next slide');
                    carouselInstance.next();
                    
                    setTimeout(() => {
                        updateFocusableElements();
                        const newSlide = currentCarousel.querySelector('.carousel-item.active');
                        const firstThumbnail = newSlide.querySelector('.thumbnail, .thumbnail-home');
                        if (firstThumbnail) {
                            const newIndex = focusableElements.indexOf(firstThumbnail);
                            if (newIndex !== -1) {
                                setFocus(newIndex);
                                updateCarouselIndicators();
                            }
                        }
                    }, 300);
                    return true;
                } else {
                    console.log('navigateCarouselSlide: No more slides, staying put');
                    return true; // We handled it (stayed put)
                }
            }
        } else if (direction === 'left') {
            // Only go to previous slide if we're at the actual FIRST visible item
            if (currentIndex === 0) {
                const slides = currentCarousel.querySelectorAll('.carousel-item');
                const activeSlide = currentCarousel.querySelector('.carousel-item.active');
                const activeIndex = Array.from(slides).indexOf(activeSlide);
                
                console.log('navigateCarouselSlide: At first item. Slide', activeIndex + 1, 'of', slides.length);
                
                if (activeIndex > 0) {
                    console.log('navigateCarouselSlide: Moving to previous slide');
                    carouselInstance.prev();
                    
                    setTimeout(() => {
                        updateFocusableElements();
                        const newSlide = currentCarousel.querySelector('.carousel-item.active');
                        const thumbnails = Array.from(newSlide.querySelectorAll('.thumbnail, .thumbnail-home'));
                        const lastThumbnail = thumbnails[thumbnails.length - 1];
                        if (lastThumbnail) {
                            const newIndex = focusableElements.indexOf(lastThumbnail);
                            if (newIndex !== -1) {
                                setFocus(newIndex);
                                updateCarouselIndicators();
                            }
                        }
                    }, 300);
                    return true;
                } else {
                    console.log('navigateCarouselSlide: No previous slides, staying put');
                    return true; // We handled it (stayed put)
                }
            }
        }
        
        console.log('navigateCarouselSlide: Not at edge, normal navigation should handle');
        return false; // Not at edge, let normal navigation handle it
    }

    
    /**
     * Update carousel visual indicators
     */
    function updateCarouselIndicators() {
        document.querySelectorAll('.carousel').forEach(carousel => {
            const slides = carousel.querySelectorAll('.carousel-item');
            const activeSlide = carousel.querySelector('.carousel-item.active');
            const activeIndex = Array.from(slides).indexOf(activeSlide);
            
            // Check if there are previous/next slides
            const hasPrev = activeIndex > 0;
            const hasNext = activeIndex < slides.length - 1;
            
            // Set data attributes for CSS
            carousel.setAttribute('data-has-prev', hasPrev);
            carousel.setAttribute('data-has-next', hasNext);
            
            // Check if focused element is at edge of current slide
            const currentElement = focusableElements[currentFocusIndex];
            if (currentElement && currentElement.closest('.carousel') === carousel) {
                const visibleThumbnails = Array.from(activeSlide.querySelectorAll('.thumbnail:not([style*="display: none"])'));
                const currentIndex = visibleThumbnails.indexOf(currentElement);
                
                // Set edge indicators
                carousel.setAttribute('data-at-start', currentIndex === 0 && hasPrev);
                carousel.setAttribute('data-at-end', currentIndex === visibleThumbnails.length - 1 && hasNext);
            } else {
                // Remove edge indicators if not focused in this carousel
                carousel.setAttribute('data-at-start', false);
                carousel.setAttribute('data-at-end', false);
            }
        });
    }


    // Add keyboard event listener
    // document.addEventListener('keydown', handleKeydown, true);
    
    // Listen for TV mode changes
    window.addEventListener('tvModeChanged', (e) => {
        isTV = e.detail.isTV;
        if (isTV) {
            startTVNavigation();
        } else {
            stopTVNavigation();
        }
    });
    
    // Listen for when tvDetection becomes available
    window.addEventListener('tvDetectionReady', () => {
        updateTVStatus();
        if (isTV) {
            startTVNavigation();
        }
    });
    
    // Initial setup
    if (updateTVStatus() && isTV) {
        // Small delay to ensure page is fully loaded
        setTimeout(startTVNavigation, 500);
    }
    
    // Debug helper for workstation testing
    window.debugTVNavigation = {
        start: () => {
            isTV = true;
            navigationActive = true;
            startTVNavigation();
        },
        
        stop: () => {
            isTV = false;
            stopTVNavigation();
        },
        
        showElements: () => {
            updateFocusableElements();
            focusableElements.forEach((el, index) => {
                const rect = el.getBoundingClientRect();
                const section = el.closest('.navbar') ? 'navbar' : 
                               el.closest('.carousel') ? 'carousel' : 
                               el.closest('[id*="profile"]') ? 'profile' : 'other';
            });
        },
        
        focusElement: (index) => {
            if (index >= 0 && index < focusableElements.length) {
                setFocus(index);
            }
        }
    };

    // Keyboard shortcut for debug mode
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.altKey && e.key === 't') {
            if (navigationActive) {
                window.debugTVNavigation.stop();
            } else {
                window.debugTVNavigation.start();
            }
        }
    });

   
    // Override Bootstrap dropdown behavior in TV mode
    document.addEventListener('click', function(e) {
        if (!isTV || !navigationActive) return;
        
        const dropdownToggle = e.target.closest('.dropdown-toggle');
        if (dropdownToggle) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            return false;
        }
    }, true);
    
    // Prevent Bootstrap from handling dropdown events in TV mode
    document.addEventListener('keydown', function(e) {
        if (!isTV || !navigationActive) return;
        
        const dropdownToggle = e.target.closest('.dropdown-toggle');
        if (dropdownToggle && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            return false;
        }
    }, true);
    
    // Replace the two separate observers with this single combined one:
    
    // Watch for content changes AND force close Bootstrap dropdowns
    const observer = new MutationObserver((mutations) => {
        if (!isTV || !navigationActive) return;
        
        mutations.forEach((mutation) => {
            // Handle content changes (original first observer functionality)
            if (mutation.type === 'childList' || mutation.type === 'attributes') {
                // Debounce the element update to avoid excessive calls
                clearTimeout(observer.updateTimeout);
                observer.updateTimeout = setTimeout(() => {
                    updateFocusableElements();
                    // Keep focus on current element if it still exists
                    if (currentFocusIndex < focusableElements.length) {
                        setFocus(currentFocusIndex);
                    } else if (focusableElements.length > 0) {
                        setFocus(0);
                    }
                }, 100);
            }
            
            // Handle Bootstrap dropdown prevention (original second observer functionality)
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1 && node.classList?.contains('dropdown-menu') && node.classList?.contains('show')) {
                    // If a Bootstrap dropdown opens and we're in TV mode, close it unless it's our TV dropdown
                    if (!node.classList.contains('tv-dropdown-open')) {
                        node.classList.remove('show');
                    }
                }
            });
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class']
    });
});
