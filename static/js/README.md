# JavaScript Architecture & Documentation Standards

## Overview
This document outlines the JavaScript architecture, coding patterns, and documentation standards implemented across the video application's client-side functionality.

## File Organization

### Core Files
- `videoPlayer.js` - Complete video player implementation with Video.js integration
- `populateCategories.js` - Category population and lazy loading functionality
- `tvNavigation.ts` - TV remote control navigation for Smart TV platforms (TypeScript)
- `tvDetection.ts` - TV platform detection and mode switching (TypeScript)
- `scroll.js` - Horizontal scrolling controls for thumbnail carousels
- `advancedSearch.js` - Advanced search interface and autocomplete
- `profileMgmt.js` - Profile management and selection functionality
- `profileEdit.js` - Profile editing and creation interfaces
- `profileCarousel.js` - Profile image selection carousel
- `homeThumbs.js` - Home page thumbnail management
- `metadata.js` - Video metadata display and interaction
- `videoAdd.js` - Video addition and management interface

### TypeScript Files
The following files have been migrated to TypeScript for enhanced type safety and developer experience:
- `tvDetection.ts` - Comprehensive TV device detection with type-safe interfaces
- `tvNavigation.ts` - TV navigation system with strict typing for remote control handling

Compiled JavaScript files are automatically generated in the `dist/` directory and included in templates.

## Architecture Patterns

### Class-Based Architecture
All JavaScript modules follow a modern class-based architecture pattern:

```javascript
/**
 * @fileoverview Brief description of the module's purpose
 * Additional context and usage information
 */

/**
 * Configuration constants for the module
 * @readonly
 * @enum {number|string}
 */
const ModuleConfig = {
    /** Constant description */
    CONSTANT_NAME: 'value',
    /** Numeric constant */
    DELAY_MS: 500
};

/**
 * Main class description
 * @class ClassName
 */
class ClassName {
    /**
     * Create a new instance
     * @param {Object} options - Configuration options
     * @memberof ClassName
     */
    constructor(options = {}) {
        this.config = { ...ModuleConfig, ...options };
        this.init();
    }

    /**
     * Initialize the component
     * @private
     */
    init() {
        // Implementation
    }
}
```

### Module Patterns
- **Singleton Classes** - For global functionality (TV Navigation, Video Player)
- **Factory Classes** - For creating multiple instances (Thumbnail Renderers)
- **Utility Classes** - For shared functionality (URL handlers, API clients)
- **Configuration Objects** - For module constants and settings

## Documentation Standards

### File Header Format
```javascript
/**
 * @fileoverview Brief description of file purpose
 * Extended description explaining the module's functionality,
 * use cases, and any important implementation details.
 * 
 * @requires dependency1 - Description of external dependency
 * @requires dependency2 - Another dependency
 * 
 * @example
 * // Basic usage example
 * const instance = new ClassName(options);
 * instance.methodName();
 * 
 * @see {@link RelatedClass} - Link to related functionality
 * @see {@link OtherModule} - Another related module
 */
```

### Class Documentation
```javascript
/**
 * Class description explaining purpose and usage
 * 
 * @class ClassName
 * @implements {InterfaceName} - If implementing an interface
 * @extends {BaseClass} - If extending another class
 */
class ClassName {
    /**
     * Constructor description
     * 
     * @param {Object} options - Configuration object
     * @param {string} options.property - Description of property
     * @param {number} [options.optionalProperty=100] - Optional property with default
     * @memberof ClassName
     */
    constructor(options = {}) {}

    /**
     * Method description
     * 
     * @param {string} param1 - Description of parameter
     * @param {Object} [param2] - Optional parameter
     * @returns {Promise<Object>} Description of return value
     * @throws {Error} When specific error conditions occur
     * @example
     * const result = await instance.methodName('value', options);
     */
    async methodName(param1, param2) {}
}
```

### Function Documentation
```javascript
/**
 * Function description
 * 
 * @param {HTMLElement} element - DOM element to process
 * @param {Object} config - Configuration object
 * @param {boolean} [config.immediate=false] - Execute immediately
 * @returns {void}
 * @since 1.0.0
 */
function functionName(element, config = {}) {}
```

## Code Style Standards

### ES6+ Modern JavaScript
- **Classes** over prototypal inheritance
- **Arrow functions** for callbacks and short functions
- **Async/await** over Promise chains
- **Destructuring** for object and array access
- **Template literals** for string interpolation
- **Const/let** instead of var

### Example Modern Patterns
```javascript
// Destructuring and default parameters
const { width = 100, height = 200 } = dimensions;

// Template literals
const message = `Video ${videoId} loaded successfully at ${timestamp}`;

// Async/await
async function loadVideo(videoId) {
    try {
        const response = await fetch(`/api/videos/${videoId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to load video:', error);
        throw error;
    }
}

// Arrow functions and array methods
const activeVideos = videos
    .filter(video => video.isActive)
    .map(video => ({ ...video, displayName: video.title.toUpperCase() }));
```

### Error Handling
```javascript
// Comprehensive error handling
class VideoPlayer {
    async loadVideo(videoId) {
        try {
            if (!videoId) {
                throw new Error('Video ID is required');
            }

            const video = await this.apiClient.fetchVideo(videoId);
            
            if (!video) {
                throw new Error(`Video ${videoId} not found`);
            }

            return this.initializePlayer(video);
        } catch (error) {
            this.handleError('Failed to load video', error);
            throw error; // Re-throw for caller handling
        }
    }

    handleError(message, error) {
        console.error(`${message}:`, error);
        this.showUserError(message);
        // Optional: Send to error reporting service
    }
}
```

## API Integration Patterns

### Fetch API Usage
```javascript
/**
 * API client for video operations
 * @class ApiClient
 */
class ApiClient {
    /**
     * Base API request method
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Fetch options
     * @returns {Promise<Object>} API response data
     */
    async request(endpoint, options = {}) {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            ...options
        };

        const response = await fetch(endpoint, config);
        
        if (!response.ok) {
            throw new Error(`API request failed: ${response.status}`);
        }

        return response.json();
    }

    /**
     * Get category videos
     * @param {number} categoryId - Category identifier
     * @param {number} subcategoryId - Subcategory identifier
     * @returns {Promise<Array>} Video list
     */
    async getCategoryVideos(categoryId, subcategoryId) {
        const endpoint = `/api/categories/${categoryId}/${subcategoryId}`;
        return this.request(endpoint);
    }
}
```

### Form Handling
```javascript
/**
 * Form submission handler
 * @class FormHandler
 */
class FormHandler {
    /**
     * Submit form with validation
     * @param {HTMLFormElement} form - Form element
     * @param {Object} options - Submission options
     */
    async submitForm(form, options = {}) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Validate form data
        const validation = this.validateForm(data);
        if (!validation.isValid) {
            this.showValidationErrors(validation.errors);
            return;
        }

        try {
            const response = await this.apiClient.request(form.action, {
                method: form.method || 'POST',
                body: JSON.stringify(data)
            });

            this.handleSuccess(response);
        } catch (error) {
            this.handleError('Form submission failed', error);
        }
    }
}
```

## Performance Optimization

### Lazy Loading
```javascript
/**
 * Intersection Observer for lazy loading
 * @class LazyLoader
 */
class LazyLoader {
    constructor() {
        this.observer = new IntersectionObserver(
            this.handleIntersection.bind(this),
            {
                threshold: 0.1,
                rootMargin: '50px'
            }
        );
    }

    /**
     * Handle element intersection
     * @param {Array<IntersectionObserverEntry>} entries
     */
    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                this.loadContent(entry.target);
                this.observer.unobserve(entry.target);
            }
        });
    }
}
```

### Debouncing and Throttling
```javascript
/**
 * Utility functions for performance optimization
 */
class PerformanceUtils {
    /**
     * Debounce function calls
     * @param {Function} func - Function to debounce
     * @param {number} delay - Delay in milliseconds
     * @returns {Function} Debounced function
     */
    static debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }

    /**
     * Throttle function calls
     * @param {Function} func - Function to throttle
     * @param {number} limit - Time limit in milliseconds
     * @returns {Function} Throttled function
     */
    static throttle(func, limit) {
        let inThrottle;
        return function (...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => (inThrottle = false), limit);
            }
        };
    }
}
```

## TV/Smart TV Support

### Platform Detection
```javascript
/**
 * TV platform detection and optimization
 * @class TVDetection
 */
class TVDetection {
    /**
     * Detect TV platform
     * @returns {Object} Platform information
     */
    detectPlatform() {
        const userAgent = navigator.userAgent.toLowerCase();
        
        return {
            isTizen: userAgent.includes('tizen'),
            isWebOS: userAgent.includes('webos'),
            isFireTV: userAgent.includes('afts'),
            isAndroidTV: userAgent.includes('android') && userAgent.includes('tv'),
            isSmartTV: this.isAnySmartTV(),
            screenSize: this.getScreenSize()
        };
    }
}
```

### Remote Control Navigation
```javascript
/**
 * Remote control navigation handler
 * @class RemoteNavigation
 */
class RemoteNavigation {
    /**
     * Key mappings for different TV platforms
     */
    static KEY_MAPPINGS = {
        ArrowUp: 'up',
        ArrowDown: 'down',
        ArrowLeft: 'left',
        ArrowRight: 'right',
        Enter: 'select',
        Escape: 'back'
    };

    /**
     * Handle remote control input
     * @param {KeyboardEvent} event - Keyboard event
     */
    handleKeyPress(event) {
        const action = RemoteNavigation.KEY_MAPPINGS[event.key];
        if (action) {
            event.preventDefault();
            this.navigate(action);
        }
    }
}
```

## Testing Guidelines

### Unit Testing Structure
```javascript
/**
 * Example test structure using modern testing framework
 */
describe('VideoPlayer', () => {
    let videoPlayer;
    
    beforeEach(() => {
        // Setup before each test
        videoPlayer = new VideoPlayer({
            containerId: 'test-container'
        });
    });

    describe('initialization', () => {
        test('should initialize with default config', () => {
            expect(videoPlayer.config).toBeDefined();
            expect(videoPlayer.config.autoplay).toBe(false);
        });

        test('should merge custom config', () => {
            const customPlayer = new VideoPlayer({
                autoplay: true,
                volume: 0.8
            });
            
            expect(customPlayer.config.autoplay).toBe(true);
            expect(customPlayer.config.volume).toBe(0.8);
        });
    });

    describe('video loading', () => {
        test('should load video successfully', async () => {
            const mockVideo = { id: 1, title: 'Test Video' };
            jest.spyOn(videoPlayer.apiClient, 'fetchVideo')
                .mockResolvedValue(mockVideo);

            const result = await videoPlayer.loadVideo(1);
            
            expect(result).toBeDefined();
            expect(videoPlayer.currentVideo).toEqual(mockVideo);
        });
    });
});
```

## Browser Support

### Target Browsers
- **Chrome** (latest 2 versions) - Primary development browser
- **Firefox** (latest 2 versions) - Standard web support
- **Safari** (latest 2 versions) - macOS and iOS support
- **Edge** (latest 2 versions) - Windows support
- **Smart TV Browsers** - Tizen, WebOS, Fire TV, Android TV

### Progressive Enhancement
```javascript
/**
 * Feature detection and progressive enhancement
 */
class FeatureDetection {
    static hasIntersectionObserver() {
        return 'IntersectionObserver' in window;
    }

    static hasCustomElements() {
        return 'customElements' in window;
    }

    static hasAsyncAwait() {
        try {
            return (async () => {})() instanceof Promise;
        } catch (e) {
            return false;
        }
    }

    /**
     * Initialize features based on browser support
     */
    static initializeFeatures() {
        if (this.hasIntersectionObserver()) {
            // Use modern lazy loading
            new LazyLoader().init();
        } else {
            // Fallback to immediate loading
            this.loadAllContent();
        }
    }
}
```

## Accessibility Standards

### ARIA Implementation
```javascript
/**
 * Accessibility enhancements
 * @class AccessibilityManager
 */
class AccessibilityManager {
    /**
     * Enhance element accessibility
     * @param {HTMLElement} element - Element to enhance
     * @param {Object} options - Accessibility options
     */
    enhanceElement(element, options = {}) {
        const {
            role,
            label,
            describedBy,
            expanded,
            controls
        } = options;

        if (role) element.setAttribute('role', role);
        if (label) element.setAttribute('aria-label', label);
        if (describedBy) element.setAttribute('aria-describedby', describedBy);
        if (expanded !== undefined) {
            element.setAttribute('aria-expanded', expanded.toString());
        }
        if (controls) element.setAttribute('aria-controls', controls);

        // Ensure keyboard accessibility
        if (!element.tabIndex && element.onclick) {
            element.tabIndex = 0;
            this.addKeyboardSupport(element);
        }
    }

    /**
     * Add keyboard support to clickable elements
     * @param {HTMLElement} element - Element to enhance
     */
    addKeyboardSupport(element) {
        element.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                element.click();
            }
        });
    }
}
```

## Maintenance Guidelines

### Code Review Checklist
- [ ] **JSDoc Documentation** - All classes and methods documented
- [ ] **Error Handling** - Proper try/catch and error reporting
- [ ] **Performance** - Efficient DOM manipulation and API usage
- [ ] **Accessibility** - ARIA attributes and keyboard support
- [ ] **Browser Compatibility** - Feature detection and fallbacks
- [ ] **TV Support** - Remote control navigation tested
- [ ] **Security** - Input validation and XSS prevention
- [ ] **Testing** - Unit tests for critical functionality

### Deployment Process
1. **Linting** - ESLint validation with project configuration
2. **Testing** - Unit and integration test execution
3. **Minification** - Production build with source maps
4. **TV Testing** - Validation on target Smart TV platforms
5. **Performance Audit** - Lighthouse and performance testing
6. **Documentation** - Update JSDoc and README files

### Update Guidelines
1. **Backward Compatibility** - Maintain API compatibility
2. **Feature Detection** - Progressive enhancement for new features  
3. **Error Logging** - Comprehensive error tracking and reporting
4. **Performance Monitoring** - Track performance metrics
5. **User Feedback** - Monitor user experience and error reports

---

**Maintained by**: Video Development Team  
**Last Updated**: September 26, 2025  
**JavaScript Standards**: ES2022+  
**Documentation**: JSDoc 3.6+