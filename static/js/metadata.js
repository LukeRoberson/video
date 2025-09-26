/**
 * @fileoverview Metadata management functionality for videos and scriptures.
 * Handles form submissions for adding video metadata and scripture text.
 */

/**
 * Configuration constants for metadata management
 * @readonly
 * @enum {string}
 */
const MetadataConfig = {
    /** API endpoint for video metadata */
    VIDEO_METADATA_ENDPOINT: '/api/video/metadata',
    /** API endpoint for scripture data */
    SCRIPTURE_ENDPOINT: '/api/scripture',
    /** Content type for JSON requests */
    JSON_CONTENT_TYPE: 'application/json'
};

/**
 * Base class for handling form submissions with common functionality
 * @class BaseFormHandler
 */
class BaseFormHandler {
    /**
     * Create a BaseFormHandler instance
     * @param {string} formId - The ID of the form element
     * @memberof BaseFormHandler
     */
    constructor(formId) {
        /**
         * The form element
         * @type {HTMLFormElement}
         */
        this.form = document.getElementById(formId);
        
        /**
         * Whether the form is currently submitting
         * @type {boolean}
         */
        this.isSubmitting = false;
        
        if (!this.form) {
            console.warn(`Form with ID '${formId}' not found`);
            return;
        }
        
        this.setupEventListener();
    }

    /**
     * Set up form submission event listener
     * @private
     * @memberof BaseFormHandler
     */
    setupEventListener() {
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleSubmit();
        });
    }

    /**
     * Handle form submission - to be implemented by subclasses
     * @abstract
     * @async
     * @memberof BaseFormHandler
     */
    async handleSubmit() {
        throw new Error('handleSubmit method must be implemented by subclass');
    }

    /**
     * Extract form data into an object
     * @param {Array<string>} fieldIds - Array of field IDs to extract
     * @returns {Object} Object containing form field values
     * @protected
     * @memberof BaseFormHandler
     */
    extractFormData(fieldIds) {
        const data = {};
        fieldIds.forEach(fieldId => {
            const element = document.getElementById(fieldId);
            if (element) {
                data[fieldId] = element.value;
            }
        });
        return data;
    }

    /**
     * Send POST request to specified endpoint
     * @param {string} endpoint - API endpoint URL
     * @param {Object} payload - Data to send in request body
     * @returns {Promise<Object>} Response data
     * @protected
     * @async
     * @memberof BaseFormHandler
     */
    async sendRequest(endpoint, payload) {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': MetadataConfig.JSON_CONTENT_TYPE
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    }

    /**
     * Display success message to user
     * @param {string} message - Success message to display
     * @protected
     * @memberof BaseFormHandler
     */
    showSuccess(message) {
        alert(message);
    }

    /**
     * Display error message to user
     * @param {string} message - Error message to display
     * @protected
     * @memberof BaseFormHandler
     */
    showError(message) {
        alert(message);
    }

    /**
     * Reset the form to its initial state
     * @protected
     * @memberof BaseFormHandler
     */
    resetForm() {
        if (this.form) {
            this.form.reset();
        }
    }

    /**
     * Set submitting state to prevent double submissions
     * @param {boolean} submitting - Whether form is currently submitting
     * @protected
     * @memberof BaseFormHandler
     */
    setSubmitting(submitting) {
        this.isSubmitting = submitting;
        const submitButton = this.form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = submitting;
            submitButton.textContent = submitting ? 'Submitting...' : submitButton.dataset.originalText || 'Submit';
            if (!submitButton.dataset.originalText) {
                submitButton.dataset.originalText = submitButton.textContent;
            }
        }
    }
}

/**
 * Handles video metadata form submissions
 * @class VideoMetadataHandler
 * @extends BaseFormHandler
 */
class VideoMetadataHandler extends BaseFormHandler {
    /**
     * Create a VideoMetadataHandler instance
     * @param {string} formId - The ID of the video metadata form
     * @memberof VideoMetadataHandler
     */
    constructor(formId = 'addMetadataForm') {
        super(formId);
        
        /**
         * Field IDs for video metadata form
         * @type {Array<string>}
         * @private
         */
        this.fieldIds = [
            'videoName', 'description', 'url', 'tagName', 'locationName',
            'speakerName', 'characterName', 'scriptureName', 'categoryName', 'dateAdded'
        ];
    }

    /**
     * Handle video metadata form submission
     * @async
     * @memberof VideoMetadataHandler
     */
    async handleSubmit() {
        if (this.isSubmitting) return;
        
        try {
            this.setSubmitting(true);
            
            const formData = this.extractFormData(this.fieldIds);
            const payload = this.buildMetadataPayload(formData);
            
            const result = await this.sendRequest(MetadataConfig.VIDEO_METADATA_ENDPOINT, payload);
            
            if (result.success) {
                this.showSuccess('Metadata added successfully!');
                this.resetForm();
            } else {
                this.showError('Failed to add metadata: ' + (result.error || 'Unknown error'));
            }
            
        } catch (error) {
            console.error('Video metadata submission error:', error);
            this.showError('Error: ' + error.message);
        } finally {
            this.setSubmitting(false);
        }
    }

    /**
     * Build the payload object for video metadata API
     * @param {Object} formData - Raw form data
     * @returns {Object} Formatted payload for API
     * @private
     * @memberof VideoMetadataHandler
     */
    buildMetadataPayload(formData) {
        return {
            video_name: formData.videoName,
            description: formData.description,
            url: formData.url,
            tag_name: formData.tagName,
            location_name: formData.locationName,
            speaker_name: formData.speakerName,
            character_name: formData.characterName,
            scripture_name: formData.scriptureName,
            category_name: formData.categoryName,
            date_added: formData.dateAdded ? new Date(formData.dateAdded).toISOString() : null
        };
    }
}

/**
 * Handles scripture text form submissions
 * @class ScriptureTextHandler
 * @extends BaseFormHandler
 */
class ScriptureTextHandler extends BaseFormHandler {
    /**
     * Create a ScriptureTextHandler instance
     * @param {string} formId - The ID of the scripture form
     * @memberof ScriptureTextHandler
     */
    constructor(formId = 'addScrForm') {
        super(formId);
        
        /**
         * Field IDs for scripture form
         * @type {Array<string>}
         * @private
         */
        this.fieldIds = ['scrName', 'scrText'];
    }

    /**
     * Handle scripture text form submission
     * @async
     * @memberof ScriptureTextHandler
     */
    async handleSubmit() {
        if (this.isSubmitting) return;
        
        try {
            this.setSubmitting(true);
            
            const formData = this.extractFormData(this.fieldIds);
            const payload = this.buildScripturePayload(formData);
            
            const result = await this.sendRequest(MetadataConfig.SCRIPTURE_ENDPOINT, payload);
            
            if (result.success) {
                this.showSuccess('Scripture text added successfully!');
                this.clearScriptureText();
            } else {
                this.showError('Failed to add scripture text: ' + (result.error || 'Unknown error'));
            }
            
        } catch (error) {
            console.error('Scripture submission error:', error);
            this.showError('Error: ' + error.message);
        } finally {
            this.setSubmitting(false);
        }
    }

    /**
     * Build the payload object for scripture API
     * @param {Object} formData - Raw form data
     * @returns {Object} Formatted payload for API
     * @private
     * @memberof ScriptureTextHandler
     */
    buildScripturePayload(formData) {
        return {
            scr_name: formData.scrName,
            scr_text: formData.scrText
        };
    }

    /**
     * Clear only the scripture text field (keeping the name field)
     * @private
     * @memberof ScriptureTextHandler
     */
    clearScriptureText() {
        const textField = document.getElementById('scrText');
        if (textField) {
            textField.value = '';
        }
    }
}

/**
 * Main controller for metadata management functionality
 * @class MetadataController
 */
class MetadataController {
    /**
     * Create a MetadataController instance
     * @memberof MetadataController
     */
    constructor() {
        /**
         * Video metadata form handler
         * @type {VideoMetadataHandler}
         */
        this.videoHandler = null;
        
        /**
         * Scripture text form handler
         * @type {ScriptureTextHandler}
         */
        this.scriptureHandler = null;
        
        this.init();
    }

    /**
     * Initialize the metadata controller
     * @memberof MetadataController
     */
    init() {
        this.initializeHandlers();
        this.setupGlobalErrorHandling();
    }

    /**
     * Initialize form handlers
     * @private
     * @memberof MetadataController
     */
    initializeHandlers() {
        this.videoHandler = new VideoMetadataHandler();
        this.scriptureHandler = new ScriptureTextHandler();
    }

    /**
     * Set up global error handling for unhandled promise rejections
     * @private
     * @memberof MetadataController
     */
    setupGlobalErrorHandling() {
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            // Prevent the default behavior of logging to console
            event.preventDefault();
        });
    }

    /**
     * Get the video metadata handler instance
     * @returns {VideoMetadataHandler} Video handler instance
     * @memberof MetadataController
     */
    getVideoHandler() {
        return this.videoHandler;
    }

    /**
     * Get the scripture text handler instance
     * @returns {ScriptureTextHandler} Scripture handler instance
     * @memberof MetadataController
     */
    getScriptureHandler() {
        return this.scriptureHandler;
    }
}

// Global controller instance
let metadataController;

/**
 * Initialize metadata functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    metadataController = new MetadataController();
});