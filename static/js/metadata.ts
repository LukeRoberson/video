/**
 * @fileoverview Metadata management functionality for videos and scriptures.
 * Handles form submissions for adding video metadata and scripture text.
 * Used with the 'admin' page.
 */

/**
 * Configuration constants for metadata management
 */
const MetadataConfig = {
    /** API endpoint for video metadata */
    VIDEO_METADATA_ENDPOINT: '/api/video/metadata',
    /** API endpoint for scripture data */
    SCRIPTURE_ENDPOINT: '/api/scripture',
    /** Content type for JSON requests */
    JSON_CONTENT_TYPE: 'application/json'
} as const;

/**
 * Interface for API response structure
 */
interface ApiResponse {
    success: boolean;
    error?: string;
    message?: string;
}

/**
 * Interface for video metadata form data
 */
interface VideoMetadataFormData extends Record<string, string> {
    videoName: string;
    description: string;
    url: string;
    tagName: string;
    locationName: string;
    speakerName: string;
    characterName: string;
    scriptureName: string;
    categoryName: string;
    dateAdded: string;
}

/**
 * Interface for video metadata API payload
 */
interface VideoMetadataPayload {
    video_name: string;
    description: string;
    url: string;
    tag_name: string;
    location_name: string;
    speaker_name: string;
    character_name: string;
    scripture_name: string;
    category_name: string;
    date_added: string | null;
}

/**
 * Interface for scripture form data
 */
interface ScriptureFormData extends Record<string, string> {
    scrName: string;
    scrText: string;
}

/**
 * Interface for scripture API payload
 */
interface ScripturePayload {
    scr_name: string;
    scr_text: string;
}

/**
 * Base class for handling form submissions with common functionality
 */
abstract class BaseFormHandler {
    /** The form element */
    protected form: HTMLFormElement | null;
    
    /** Whether the form is currently submitting */
    protected isSubmitting: boolean = false;

    /**
     * Create a BaseFormHandler instance
     * @param formId - The ID of the form element
     */
    constructor(formId: string) {
        this.form = document.getElementById(formId) as HTMLFormElement;
        
        if (!this.form) {
            console.warn(`Form with ID '${formId}' not found`);
            return;
        }
        
        this.setupEventListener();
    }

    /**
     * Set up form submission event listener
     */
    private setupEventListener(): void {
        if (!this.form) return;
        
        this.form.addEventListener('submit', async (e: Event) => {
            e.preventDefault();
            await this.handleSubmit();
        });
    }

    /**
     * Handle form submission - to be implemented by subclasses
     */
    protected abstract handleSubmit(): Promise<void>;

    /**
     * Extract form data into an object
     * @param fieldIds - Array of field IDs to extract
     * @returns Object containing form field values
     */
    protected extractFormData<T extends Record<string, string>>(fieldIds: readonly string[]): T {
        const data: Record<string, string> = {};
        
        fieldIds.forEach(fieldId => {
            const element = document.getElementById(fieldId) as HTMLInputElement | HTMLTextAreaElement;
            if (element) {
                data[fieldId] = element.value;
            }
        });
        
        return data as T;
    }

    /**
     * Send POST request to specified endpoint
     * @param endpoint - API endpoint URL
     * @param payload - Data to send in request body
     * @returns Response data
     */
    protected async sendRequest<T extends ApiResponse>(endpoint: string, payload: unknown): Promise<T> {
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
        
        return await response.json() as T;
    }

    /**
     * Display success message to user
     * @param message - Success message to display
     */
    protected showSuccess(message: string): void {
        alert(message);
    }

    /**
     * Display error message to user
     * @param message - Error message to display
     */
    protected showError(message: string): void {
        alert(message);
    }

    /**
     * Reset the form to its initial state
     */
    protected resetForm(): void {
        if (this.form) {
            this.form.reset();
        }
    }

    /**
     * Set submitting state to prevent double submissions
     * @param submitting - Whether form is currently submitting
     */
    protected setSubmitting(submitting: boolean): void {
        this.isSubmitting = submitting;
        
        if (!this.form) return;
        
        const submitButton = this.form.querySelector('button[type="submit"]') as HTMLButtonElement;
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
    /** Field IDs for video metadata form */
    private readonly fieldIds: string[];

    /**
     * Create a VideoMetadataHandler instance
     * @param formId - The ID of the video metadata form
     */
    constructor(formId: string = 'addMetadataForm') {
        super(formId);
        
        this.fieldIds = [
            'videoName', 'description', 'url', 'tagName', 'locationName',
            'speakerName', 'characterName', 'scriptureName', 'categoryName', 'dateAdded'
        ];
    }

    /**
     * Handle video metadata form submission
     */
    protected async handleSubmit(): Promise<void> {
        if (this.isSubmitting) return;
        
        try {
            this.setSubmitting(true);
            
            const formData = this.extractFormData<VideoMetadataFormData>(this.fieldIds);
            const payload = this.buildMetadataPayload(formData);
            
            const result = await this.sendRequest<ApiResponse>(
                MetadataConfig.VIDEO_METADATA_ENDPOINT,
                payload
            );
            
            if (result.success) {
                this.showSuccess('Metadata added successfully!');
                this.resetForm();
            } else {
                this.showError('Failed to add metadata: ' + (result.error || 'Unknown error'));
            }
            
        } catch (error) {
            console.error('Video metadata submission error:', error);
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            this.showError('Error: ' + errorMessage);
        } finally {
            this.setSubmitting(false);
        }
    }

    /**
     * Build the payload object for video metadata API
     * @param formData - Raw form data
     * @returns Formatted payload for API
     */
    private buildMetadataPayload(formData: VideoMetadataFormData): VideoMetadataPayload {
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
    /** Field IDs for scripture form */
    private readonly fieldIds: string[];

    /**
     * Create a ScriptureTextHandler instance
     * @param formId - The ID of the scripture form
     */
    constructor(formId: string = 'addScrForm') {
        super(formId);
        
        this.fieldIds = ['scrName', 'scrText'];
    }

    /**
     * Handle scripture text form submission
     */
    protected async handleSubmit(): Promise<void> {
        if (this.isSubmitting) return;
        
        try {
            this.setSubmitting(true);
            
            const formData = this.extractFormData<ScriptureFormData>(this.fieldIds);
            const payload = this.buildScripturePayload(formData);
            
            const result = await this.sendRequest<ApiResponse>(
                MetadataConfig.SCRIPTURE_ENDPOINT,
                payload
            );
            
            if (result.success) {
                this.showSuccess('Scripture text added successfully!');
                this.clearScriptureText();
            } else {
                this.showError('Failed to add scripture text: ' + (result.error || 'Unknown error'));
            }
            
        } catch (error) {
            console.error('Scripture submission error:', error);
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            this.showError('Error: ' + errorMessage);
        } finally {
            this.setSubmitting(false);
        }
    }

    /**
     * Build the payload object for scripture API
     * @param formData - Raw form data
     * @returns Formatted payload for API
     */
    private buildScripturePayload(formData: ScriptureFormData): ScripturePayload {
        return {
            scr_name: formData.scrName,
            scr_text: formData.scrText
        };
    }

    /**
     * Clear only the scripture text field (keeping the name field)
     */
    private clearScriptureText(): void {
        const textField = document.getElementById('scrText') as HTMLTextAreaElement;
        if (textField) {
            textField.value = '';
        }
    }
}

/**
 * Main controller for metadata management functionality
 */
class MetadataController {
    /** Video metadata form handler */
    private videoHandler: VideoMetadataHandler | null = null;
    
    /** Scripture text form handler */
    private scriptureHandler: ScriptureTextHandler | null = null;

    /**
     * Create a MetadataController instance
     */
    constructor() {
        this.init();
    }

    /**
     * Initialize the metadata controller
     */
    private init(): void {
        this.initializeHandlers();
        this.setupGlobalErrorHandling();
    }

    /**
     * Initialize form handlers
     */
    private initializeHandlers(): void {
        this.videoHandler = new VideoMetadataHandler();
        this.scriptureHandler = new ScriptureTextHandler();
    }

    /**
     * Set up global error handling for unhandled promise rejections
     */
    private setupGlobalErrorHandling(): void {
        window.addEventListener('unhandledrejection', (event: PromiseRejectionEvent) => {
            console.error('Unhandled promise rejection:', event.reason);
            // Prevent the default behavior of logging to console
            event.preventDefault();
        });
    }

    /**
     * Get the video metadata handler instance
     * @returns Video handler instance
     */
    public getVideoHandler(): VideoMetadataHandler | null {
        return this.videoHandler;
    }

    /**
     * Get the scripture text handler instance
     * @returns Scripture handler instance
     */
    public getScriptureHandler(): ScriptureTextHandler | null {
        return this.scriptureHandler;
    }
}

// Global controller instance
let metadataController: MetadataController;

/**
 * Initialize metadata functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    metadataController = new MetadataController();
});
