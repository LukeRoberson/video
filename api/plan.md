

# Plan

1. General clean up
    * [x] Split out api.py into smaller files
    * [x] Update docstrings in API files
2. Documentation
    * [ ] Clean up api.md; Possible split into multiple files
    * [ ] Update other documentation files with changes
3. Create standard response formats
    * Some include 'data' and 'message', others don't
    * [ ] `api_category.py`: 3x endpoints
    * [ ] `api_character.py`: 3x endpoints
    * [ ] `api_similarity.py`: 1x endpoint
    * [ ] `api_tag.py`: 3x endpoints
    * [ ] `api_scripture.py`: 3x endpoints
    * [ ] `api_location.py`: 3x endpoints
4. Logging and Testing
    * [ ] Add better logging to API files
    * [ ] Add a debug mode when starting the API (flask debug + logging level)
    * [ ] Create and organize postman files for API testing
    * [ ] Create pytest structure for automated testing
5. Clean up API Calls
    * [ ] Set video base URL to /api/videos
    * [x] Set category base URL to /api/category
    * [x] Set scripture base URL to /api/scriptures
    * [ ] TypeScript files (below)
    * [ ] Duplicate API calls (profileEdit vs profileMgmt)
6. Consolidate endpoints
    * [ ] Combine get_video, get_videos_bulk, and filter_videos (api_video.py)
    * [ ] Combine endpoints to get all characters and get one specific character (api_character.py)
    * [ ] Combine 'get all speakers' with 'get specific speaker' (api_speaker.py)
    * [ ] Combine 'get all tags' with 'get specific tag' (api_tags.py)
7. Clean up bugs
    * [ ] In categories, watch status on individual videos is not showing
    * [ ] Terminal errors for one user (500-Marija_Golubiček.png) due to unicode
    * [ ] Searches sometimes throw unicode errors in the terminal
    * [ ] When saving a profile name change, this is not immediately reflected in the edit screen
    * [ ] Categories: Invalid main/sub combinations (eg, Programs and Events/Monthly Programs) still return data
8. Coding improvements
    * [ ] Investigate using 'MethodView' in Flask
    * [ ] Update blueprints to use a URL prefix (as is done in api_search.py)
    * [ ] Investigate whether avatars should be stored in the frontend or backend
9. Performance
    * [ ] Some endpoints should have a filter, so they don't return all information if it's not needed (minimal payload size)
    * [ ] Fix themes.py - It makes many calls to the API instead of just one or two
10. Active user redesign
    * [ ] Get the frontend to track the active user, not the API (eg, mark as watched/unwatched, in progress videos)
        * [ ] `api_category.py` - Category filter
    * [ ] API calls from the frontend should include the active user if needed
    * [ ] Clean up profile.py, as there's some code reuse around active profiles


</br></br>





# Cleanup

## TypeScript Files

* profileMgmt.ts
    * Base URLs in ProfileMgmtConfig
    * URL selection in setActiveProfile
* profileEdit.ts
    * Base URLs in ProfileEditConfig
* populateCategories.ts
    * Base URLs in CategoryConfig
* videoAdd.ts
    * Base URLs in VideoAddConfig
* videoPlayer.ts
    * Move API endpoints to a variable


## Overlapping API calls and endpoints

* profileEdit.ts and profileMgmt.ts
    * These appear to do the same thing
    * Can they be consolidated?
* Duplicate endpoints
    * /api/profile/update/{id} and /edit_profile/{id} appear to be the same thing

