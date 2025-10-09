# JavaScript Architecture & Documentation Standards

## Overview
This document outlines the JavaScript architecture, coding patterns, and documentation standards implemented across the video application's client-side functionality.

## File Organization

### TypeScript Files
All core files have been migrated to TypeScript for enhanced type safety and developer experience:

#### Video Player & Media Management
- `videoPlayer.ts` - Complete video player implementation with Video.js integration, includes:
  - GlobalPlayerManager - Prevents multiple simultaneous playback
  - VideoPlayerCore - Core player initialization and TV mode detection
  - VideoContextMenu - Right-click context menu for timestamped URL sharing
  - ProgressTracker - Progress tracking and automatic watched status management
  - UrlTimeHandler - URL timestamp parameter handling (t=seconds)
  - CustomControls - Theatre mode button and keyboard controls
  - SubtitleManager - Automatic subtitle loading

#### Admin & Metadata Management
- `metadata.ts` - Video metadata and scripture text form submission handling
- `videoAdd.ts` - Video addition from CSV and management interface

#### UI Components
- `homeThumbs.ts` - Home page thumbnail carousel management with dynamic loading
- `profileCarousel.ts` - Profile image selection carousel with Bootstrap integration
- `populateCategories.ts` - Category population and lazy loading functionality
- `scroll.ts` - Horizontal scrolling controls for thumbnail carousels
- `toggleWatched.ts` - Watched video visibility toggle with localStorage persistence

#### TV Platform Support
- `tvDetection.ts` - Comprehensive TV device detection with type-safe interfaces
- `tvNavigation.ts` - TV navigation system with strict typing for remote control handling

#### Search & Profile Management
- `advancedSearch.ts` - Advanced search interface and autocomplete
- `profileMgmt.ts` - Profile management and selection functionality
- `profileEdit.ts` - Profile editing and creation interfaces

#### Build Output
Compiled JavaScript files are automatically generated in the `dist/` directory:
- All `.ts` files → `dist/*.js` (ES2020 compatible)
- Source maps (`.js.map`) for debugging
- Type declarations (`.d.ts`) for IDE support
- Declaration maps (`.d.ts.map`) for navigation

**Compilation**: Run `npx tsc` to compile all TypeScript files. Compiled files in `dist/` should be referenced in HTML templates.

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

## TypeScript Architecture

### Type Safety Benefits
TypeScript provides compile-time type checking, catching errors before runtime:

```typescript
// Interfaces define data structures
interface Video {
    id: number | string;
    name: string;
    thumbnail: string;
    duration: string;
    watched: boolean;
}

// Type-safe async operations
async fetchCategoryVideos(categoryId: string | number): Promise<Video[]> {
    const response = await fetch(`/api/categories/${categoryId}`);
    return await response.json();
}
```

### Configuration with Type Safety
```typescript
// Readonly configuration with as const
const ScrollConfig = {
    WHEEL_SPEED_FACTOR: 2,
    ARROW_UPDATE_DELAY: 100,
    DIRECTION_LEFT: -1,
    DIRECTION_RIGHT: 1
} as const;

// TypeScript prevents modification
ScrollConfig.WHEEL_SPEED_FACTOR = 5; // Error: Cannot assign to 'WHEEL_SPEED_FACTOR'
```

### Class Structure with Access Modifiers
```typescript
class ThumbnailScrollManager {
    // Private properties (encapsulation)
    private wrapper: HTMLElement;
    private thumbnails: HTMLElement;
    private boundUpdateArrows: () => void;
    
    constructor(wrapperElement: HTMLElement) {
        this.wrapper = wrapperElement;
        this.boundUpdateArrows = this.updateArrows.bind(this);
    }
    
    // Private methods
    private setupEventListeners(): void {
        this.thumbnails.addEventListener('scroll', this.boundUpdateArrows);
    }
    
    // Public methods
    public scrollThumbnails(direction: number): void {
        const scrollAmount = this.thumbnails.clientWidth;
        this.thumbnails.scrollBy({
            left: direction * scrollAmount,
            behavior: 'smooth'
        });
    }
}
```

### Custom Types and Interfaces
```typescript
// Type alias for callbacks
type VideoElementsAddedCallback = () => void;

// Custom event interfaces
interface WatchedToggleEventDetail {
    hideWatched: boolean;
}

interface WatchedToggleEvent extends CustomEvent {
    detail: WatchedToggleEventDetail;
}

// Window extensions for global functions
interface WindowWithScrollFunctions extends Window {
    scrollThumbnails?: (wrapperId: string, direction: number) => void;
    updateArrows?: (wrapperId: string) => void;
}
```

### Null Safety and Type Guards
```typescript
constructor(carouselId: string) {
    // Explicit null checking
    const element = document.getElementById(carouselId);
    if (!element) {
        throw new Error(`Carousel element with ID "${carouselId}" not found`);
    }
    
    // Type guard for HTMLInputElement
    const input = document.getElementById('input');
    if (input && input instanceof HTMLInputElement) {
        this.input = input;
    }
}
```

### TypeScript Compilation
```bash
# Compile all TypeScript files
npx tsc

# Compile in watch mode (auto-recompile on changes)
npx tsc --watch

# Check for errors without emitting files
npx tsc --noEmit
```

**Configuration**: `tsconfig.json` in project root
- **Target**: ES2020
- **Module**: ES2020
- **Strict Mode**: Enabled (strict type checking)
- **Output**: `static/js/dist/`

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

## TypeScript Migration

### Migration Status
The following JavaScript files have been successfully migrated to TypeScript:

| File | Status | Notes |
|------|--------|-------|
| `homeThumbs.ts` | ✅ Migrated | Thumbnail carousel management |
| `profileCarousel.ts` | ✅ Migrated | Profile picture selection |
| `populateCategories.ts` | ✅ Migrated | Category lazy loading |
| `scroll.ts` | ✅ Migrated | Horizontal scrolling |
| `toggleWatched.ts` | ✅ Migrated | Watched video toggle |
| `tvDetection.ts` | ✅ Migrated | TV platform detection |
| `tvNavigation.ts` | ✅ Migrated | TV remote navigation |
| `advancedSearch.ts` | ✅ Migrated | Advanced search interface |
| `profileMgmt.ts` | ✅ Migrated | Profile management |
| `profileEdit.ts` | ✅ Migrated | Profile editing |
| `videoPlayer.js` | 📋 Pending | Video.js integration |
| `metadata.js` | 📋 Pending | Metadata display |
| `videoAdd.js` | 📋 Pending | Video management |

### Migration Benefits
- **Type Safety**: Catch errors at compile-time instead of runtime
- **Better IDE Support**: IntelliSense, autocomplete, and refactoring
- **Self-Documenting**: Type annotations serve as inline documentation
- **Maintainability**: Easier for team collaboration and onboarding
- **Refactoring Confidence**: Safe refactoring with compiler validation

### Key Improvements from Migration

#### 1. Proper Event Listener Cleanup
```typescript
// Before (JavaScript) - memory leak potential
setupEventListeners() {
    this.element.addEventListener('scroll', () => this.handler());
}

// After (TypeScript) - proper cleanup
private boundHandler: () => void;

constructor() {
    this.boundHandler = this.handler.bind(this);
}

private setupEventListeners(): void {
    this.element.addEventListener('scroll', this.boundHandler);
}

destroy(): void {
    this.element.removeEventListener('scroll', this.boundHandler);
}
```

#### 2. Null Safety
```typescript
// Before (JavaScript) - potential null reference error
const element = document.getElementById('myId');
element.addEventListener('click', handler); // May crash!

// After (TypeScript) - safe with null checking
const element = document.getElementById('myId');
if (!element) {
    throw new Error('Element not found');
}
element.addEventListener('click', handler); // Safe!
```

#### 3. Type-Safe API Calls
```typescript
// Before (JavaScript) - unknown response type
async fetchVideos(categoryId) {
    const response = await fetch(`/api/videos/${categoryId}`);
    return response.json(); // What type is this?
}

// After (TypeScript) - explicit types
async fetchVideos(categoryId: number): Promise<Video[]> {
    const response = await fetch(`/api/videos/${categoryId}`);
    return await response.json(); // TypeScript knows it's Video[]
}
```

### Migration Resources
- **Documentation**: See `docs/typescript_refactoring.md` for detailed migration guide
- **Comparison**: See `docs/typescript_refactoring_comparison.md` for before/after examples
- **Build Process**: Run `npx tsc` to compile, or `npx tsc --watch` for development

## Maintenance Guidelines

### Code Review Checklist
- [ ] **JSDoc/TSDoc Documentation** - All classes and methods documented
- [ ] **TypeScript Types** - Proper interfaces and type annotations (for .ts files)
- [ ] **Null Safety** - Proper null checks and optional chaining
- [ ] **Error Handling** - Proper try/catch and error reporting
- [ ] **Performance** - Efficient DOM manipulation and API usage
- [ ] **Accessibility** - ARIA attributes and keyboard support
- [ ] **Browser Compatibility** - Feature detection and fallbacks
- [ ] **TV Support** - Remote control navigation tested
- [ ] **Security** - Input validation and XSS prevention
- [ ] **Testing** - Unit tests for critical functionality
- [ ] **Type Compilation** - TypeScript files compile without errors

### Deployment Process
1. **TypeScript Compilation** - Run `npx tsc` to compile .ts files
2. **Linting** - ESLint validation with project configuration
3. **Testing** - Unit and integration test execution
4. **Minification** - Production build with source maps
5. **TV Testing** - Validation on target Smart TV platforms
6. **Performance Audit** - Lighthouse and performance testing
7. **Documentation** - Update JSDoc/TSDoc and README files

### Update Guidelines
1. **Backward Compatibility** - Maintain API compatibility
2. **Feature Detection** - Progressive enhancement for new features  
3. **Error Logging** - Comprehensive error tracking and reporting
4. **Performance Monitoring** - Track performance metrics
5. **User Feedback** - Monitor user experience and error reports

---

**Maintained by**: Video Development Team  
**Last Updated**: October 8, 2025  
**JavaScript Standards**: ES2022+  
**TypeScript Version**: 5.x  
**Documentation**: JSDoc 3.6+ / TSDoc