/**
 * @fileoverview Metadata management functionality for videos and scriptures.
 * Handles form submissions for adding video metadata and scripture text.
 * Used with the 'admin' page.
 */
/**
 * Configuration constants for metadata management
 */
declare const MetadataConfig: {
    /** API base URL */
    readonly API_BASE_URL: "http://localhost:5010";
    /** API endpoint for video metadata */
    readonly VIDEO_METADATA_ENDPOINT: "/api/video/metadata";
    /** API endpoint for scripture data */
    readonly SCRIPTURE_ENDPOINT: "/api/scripture";
    /** Content type for JSON requests */
    readonly JSON_CONTENT_TYPE: "application/json";
};
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
declare abstract class BaseFormHandler {
    /** The form element */
    protected form: HTMLFormElement | null;
    /** Whether the form is currently submitting */
    protected isSubmitting: boolean;
    /**
     * Create a BaseFormHandler instance
     * @param formId - The ID of the form element
     */
    constructor(formId: string);
    /**
     * Set up form submission event listener
     */
    private setupEventListener;
    /**
     * Handle form submission - to be implemented by subclasses
     */
    protected abstract handleSubmit(): Promise<void>;
    /**
     * Extract form data into an object
     * @param fieldIds - Array of field IDs to extract
     * @returns Object containing form field values
     */
    protected extractFormData<T extends Record<string, string>>(fieldIds: readonly string[]): T;
    /**
     * Send POST request to specified endpoint
     * @param endpoint - API endpoint URL
     * @param payload - Data to send in request body
     * @returns Response data
     */
    protected sendRequest<T extends ApiResponse>(endpoint: string, payload: unknown): Promise<T>;
    /**
     * Display success message to user
     * @param message - Success message to display
     */
    protected showSuccess(message: string): void;
    /**
     * Display error message to user
     * @param message - Error message to display
     */
    protected showError(message: string): void;
    /**
     * Reset the form to its initial state
     */
    protected resetForm(): void;
    /**
     * Set submitting state to prevent double submissions
     * @param submitting - Whether form is currently submitting
     */
    protected setSubmitting(submitting: boolean): void;
}
/**
 * Handles video metadata form submissions
 */
declare class VideoMetadataHandler extends BaseFormHandler {
    /** Field IDs for video metadata form */
    private readonly fieldIds;
    /**
     * Create a VideoMetadataHandler instance
     * @param formId - The ID of the video metadata form
     */
    constructor(formId?: string);
    /**
     * Handle video metadata form submission
     */
    protected handleSubmit(): Promise<void>;
    /**
     * Build the payload object for video metadata API
     * @param formData - Raw form data
     * @returns Formatted payload for API
     */
    private buildMetadataPayload;
}
/**
 * Handles scripture text form submissions
 */
declare class ScriptureTextHandler extends BaseFormHandler {
    /** Field IDs for scripture form */
    private readonly fieldIds;
    /**
     * Create a ScriptureTextHandler instance
     * @param formId - The ID of the scripture form
     */
    constructor(formId?: string);
    /**
     * Handle scripture text form submission
     */
    protected handleSubmit(): Promise<void>;
    /**
     * Build the payload object for scripture API
     * @param formData - Raw form data
     * @returns Formatted payload for API
     */
    private buildScripturePayload;
    /**
     * Clear only the scripture text field (keeping the name field)
     */
    private clearScriptureText;
}
/**
 * Main controller for metadata management functionality
 */
declare class MetadataController {
    /** Video metadata form handler */
    private videoHandler;
    /** Scripture text form handler */
    private scriptureHandler;
    /**
     * Create a MetadataController instance
     */
    constructor();
    /**
     * Initialize the metadata controller
     */
    private init;
    /**
     * Initialize form handlers
     */
    private initializeHandlers;
    /**
     * Set up global error handling for unhandled promise rejections
     */
    private setupGlobalErrorHandling;
    /**
     * Get the video metadata handler instance
     * @returns Video handler instance
     */
    getVideoHandler(): VideoMetadataHandler | null;
    /**
     * Get the scripture text handler instance
     * @returns Scripture handler instance
     */
    getScriptureHandler(): ScriptureTextHandler | null;
}
declare let metadataController: MetadataController;
//# sourceMappingURL=metadata.d.ts.map