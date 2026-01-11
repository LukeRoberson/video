"use strict";
/**
 * @fileoverview Metadata management functionality for videos and scriptures.
 * Handles form submissions for adding video metadata and scripture text.
 * Used with the 'admin' page.
 */
/**
 * Configuration constants for metadata management
 */
const MetadataConfig = {
    /** API base URL for legacy endpoints (still on main server) */
    LEGACY_API_BASE_URL: 'http://localhost:5000',
    /** API base URL for migrated endpoints (on separate service) */
    API_BASE_URL: 'http://localhost:5010',
    /** API endpoint for video metadata */
    VIDEO_METADATA_ENDPOINT: '/api/video/metadata',
    /** API endpoint for scripture data */
    SCRIPTURE_ENDPOINT: '/api/scripture',
    /** Content type for JSON requests */
    JSON_CONTENT_TYPE: 'application/json'
};
/**
 * Base class for handling form submissions with common functionality
 */
class BaseFormHandler {
    /**
     * Create a BaseFormHandler instance
     * @param formId - The ID of the form element
     */
    constructor(formId) {
        /** Whether the form is currently submitting */
        this.isSubmitting = false;
        this.form = document.getElementById(formId);
        if (!this.form) {
            console.warn(`Form with ID '${formId}' not found`);
            return;
        }
        this.setupEventListener();
    }
    /**
     * Set up form submission event listener
     */
    setupEventListener() {
        if (!this.form)
            return;
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleSubmit();
        });
    }
    /**
     * Extract form data into an object
     * @param fieldIds - Array of field IDs to extract
     * @returns Object containing form field values
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
     * @param endpoint - API endpoint URL
     * @param payload - Data to send in request body
     * @returns Response data
     */
    async sendRequest(endpoint, payload, usesMigratedApi = false) {
        const baseUrl = usesMigratedApi ? MetadataConfig.API_BASE_URL : MetadataConfig.LEGACY_API_BASE_URL;
        const url = `${baseUrl}${endpoint}`;
        console.log(`New API: ${usesMigratedApi}, URL: ${url}, Payload:`, payload);
        const response = await fetch(url, {
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
     * @param message - Success message to display
     */
    showSuccess(message) {
        alert(message);
    }
    /**
     * Display error message to user
     * @param message - Error message to display
     */
    showError(message) {
        alert(message);
    }
    /**
     * Reset the form to its initial state
     */
    resetForm() {
        if (this.form) {
            this.form.reset();
        }
    }
    /**
     * Set submitting state to prevent double submissions
     * @param submitting - Whether form is currently submitting
     */
    setSubmitting(submitting) {
        this.isSubmitting = submitting;
        if (!this.form)
            return;
        const submitButton = this.form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = submitting;
            if (!submitButton.dataset.originalText) {
                submitButton.dataset.originalText = submitButton.textContent || 'Submit';
            }
            submitButton.textContent = submitting ? 'Submitting...' : submitButton.dataset.originalText;
        }
    }
}
/**
 * Handles video metadata form submissions
 */
class VideoMetadataHandler extends BaseFormHandler {
    /**
     * Create a VideoMetadataHandler instance
     * @param formId - The ID of the video metadata form
     */
    constructor(formId = 'addMetadataForm') {
        super(formId);
        this.fieldIds = [
            'videoName', 'description', 'url', 'tagName', 'locationName',
            'speakerName', 'characterName', 'scriptureName', 'categoryName', 'dateAdded'
        ];
    }
    /**
     * Handle video metadata form submission
     */
    async handleSubmit() {
        if (this.isSubmitting)
            return;
        try {
            this.setSubmitting(true);
            const formData = this.extractFormData(this.fieldIds);
            const payload = this.buildMetadataPayload(formData);
            const result = await this.sendRequest(MetadataConfig.VIDEO_METADATA_ENDPOINT, payload);
            if (result.success) {
                this.showSuccess('Metadata added successfully!');
                this.resetForm();
            }
            else {
                this.showError('Failed to add metadata: ' + (result.error || 'Unknown error'));
            }
        }
        catch (error) {
            console.error('Video metadata submission error:', error);
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            this.showError('Error: ' + errorMessage);
        }
        finally {
            this.setSubmitting(false);
        }
    }
    /**
     * Build the payload object for video metadata API
     * @param formData - Raw form data
     * @returns Formatted payload for API
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
 */
class ScriptureTextHandler extends BaseFormHandler {
    /**
     * Create a ScriptureTextHandler instance
     * @param formId - The ID of the scripture form
     */
    constructor(formId = 'addScrForm') {
        super(formId);
        this.fieldIds = ['scrName', 'scrText'];
    }
    /**
     * Handle scripture text form submission
     */
    async handleSubmit() {
        if (this.isSubmitting)
            return;
        try {
            this.setSubmitting(true);
            const formData = this.extractFormData(this.fieldIds);
            const payload = this.buildScripturePayload(formData);
            const result = await this.sendRequest(MetadataConfig.SCRIPTURE_ENDPOINT, payload, true // Uses migrated API
            );
            if (result.success) {
                this.showSuccess('Scripture text added successfully!');
                this.clearScriptureText();
            }
            else {
                this.showError('Failed to add scripture text: ' + (result.error || 'Unknown error'));
            }
        }
        catch (error) {
            console.error('Scripture submission error:', error);
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            this.showError('Error: ' + errorMessage);
        }
        finally {
            this.setSubmitting(false);
        }
    }
    /**
     * Build the payload object for scripture API
     * @param formData - Raw form data
     * @returns Formatted payload for API
     */
    buildScripturePayload(formData) {
        return {
            scr_name: formData.scrName,
            scr_text: formData.scrText
        };
    }
    /**
     * Clear only the scripture text field (keeping the name field)
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
 */
class MetadataController {
    /**
     * Create a MetadataController instance
     */
    constructor() {
        /** Video metadata form handler */
        this.videoHandler = null;
        /** Scripture text form handler */
        this.scriptureHandler = null;
        this.init();
    }
    /**
     * Initialize the metadata controller
     */
    init() {
        this.initializeHandlers();
        this.setupGlobalErrorHandling();
    }
    /**
     * Initialize form handlers
     */
    initializeHandlers() {
        this.videoHandler = new VideoMetadataHandler();
        this.scriptureHandler = new ScriptureTextHandler();
    }
    /**
     * Set up global error handling for unhandled promise rejections
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
     * @returns Video handler instance
     */
    getVideoHandler() {
        return this.videoHandler;
    }
    /**
     * Get the scripture text handler instance
     * @returns Scripture handler instance
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
document.addEventListener('DOMContentLoaded', function () {
    metadataController = new MetadataController();
});
//# sourceMappingURL=metadata.js.map