

# Plan

1. General clean up
    * [x] Split out api.py into smaller files
    * [x] Update docstrings in API files
2. Documentation
    * [x] Clean up api.md; Possible split into multiple files
    * [x] Update other documentation files with changes
3. Create standard response formats
    * [x] `api_category.py`
    * [x] `api_character.py`
    * [x] `api_similarity.py`
    * [x] `api_tag.py`
    * [x] `api_scripture.py`
    * [x] `api_location.py`
    * [x] `api_speaker`
    * [x] `api_search.py`
    * [x] `api_video.py`
4. Coding improvements
    * [x] Update blueprints to use a URL prefix (as is done in api_search.py)
5. Logging and Testing
    * [x] Add a debug mode when starting the API (flask debug + logging level)
    * [x] Add better logging to API files
    * [x] Create and organize postman files for API testing
    * [x] Create pytest structure for automated testing
6. Clean up API Calls
    * [x] Set video base URL to /api/videos
    * [x] Set category base URL to /api/category
    * [x] Set scripture base URL to /api/scriptures
    * [x] TypeScript files (below)
    * [x] Duplicate API calls (profileEdit vs profileMgmt)
7. Consolidate endpoints
    * [x] `api_character`: get_character
    * [x] `api_location`: get_location and get_locations
    * [x] `api_scripture`: get_scripture and get_scriptures
    * [x] `api_speaker`: get_speaker and get_speakers
    * [x] `api_tag`: get_tag and get_tags
    * [x] `api_video`: get_video, get_videos_bulk
    * [x] `api_search`: The regular search vs the advanced search
    * [ ] `api_profile`: get_watched and check_watched_bulk
        * Prerequisite: Fix bug where watched status not appearing on thumbnails
8. Active user redesign
    * [x] Get the frontend to track the active user, not the API
        * Currently set in `api_profile.py`, in set_active_profile()
    * [x] API calls from the frontend should include the active user if needed
        * [x] `api_profile.py`: get_watch_history; Still gets profile from local session; Should receive as a parameter
        * [x] `api_profile.py`: mark_watched; Still gets profile from local session; Should receive as a parameter
        * [x] `api_profile.py`: mark_unwatched; Still gets profile from local session; Should receive as a parameter
        * [x] `api_category.py`: category_filter; Still gets profile from local session; Should receive as a parameter
    * [x] Cleanup active user code in the API
        * [x] `api_profile.py`: in_progress_videos; Get's parameter, but falls back to local profile
        * [x] `api_profile.py`: get_watched; Get's parameter, but falls back to local profile
        * [x] `api_profile.py`: check_watched_bulk; Get's parameter, but falls back to local profile
        * [x] `api_profile.py`: set_active_profile; Shouldn't be needed anymore
        * [x] `api_profile.py`: get_active_profile; Shouldn't be needed anymore
9. Performance
    * [x] Home page
    * [x] Character pages
    * [x] Speaker pages
    * [x] Scripture pages
    * [x] Location pages
    * [x] Tag pages
    * [x] Video detail
    * [x] Themes
    * [x] Categories
    * [x] Advanced Search page
10. Clean up bugs
    * [x] In categories, watch status on individual videos is not showing
    * [x] Terminal errors for one user (500-Marija_Golubiček.png) due to unicode
    * [x] 'Logging Error' at terminal when searching with ElasticSearch
    * [x] Cannot mark videos as watched
    * [x] Getting speakers for a video; API displays errors
    * [x] Searches sometimes throw unicode errors in the terminal
    * [x] jinja2.exceptions.TemplateNotFound: 404.html
    * [ ] Profile edits
        * Profile updates work successfully (eg, name, clearing watch history)
        * They do not update on the page immediately
    * [ ] Categories: Invalid main/sub combinations (eg, Programs and Events/Monthly Programs) still return data
    * [ ] After deleting a profile:
        * The profile happened to be ID: 6
        * When loading the profile selection screen, API reports an error
            * DEBUG - Module: api_profile.py, Function: get_profile
            * ERROR - Profile with ID 6 not found.
        * Page loads fine, nothing in console
    * [ ] `/api/search` doesn't seems to be enforcing the page size limit


</br></br>





# Notes

## Improvements

* Searching
    * reindexing: This can take time, so maybe respond with 'starting', and check a URL to find an updated status
* Improve logging in api_profile
    * After other improvements are made
* Create helper functions for reused components:
    * Check if a video exists
    * Logging debugs and warnings during field validation
* Caching
    * Cache theme banners in AppCache (like category IDs); Improve loading the home page
* get_bulk endpoint
    * gets details of several videos in one API call
    * processing is still a synchronous loop of queries
    * Use a single SQL query to get all at once
* Missing similarity scores
    * Not handled well at this time



## Cleanup

* `/api/categories/{{category_id}}/{{subcategory_id}}`
    * Contains a 'videos' list in the response, which is unnecessary
* Speakers endpoint:
    * Query for invalid speaker does not return an empty list like other endpoints do
* Tags endpoint:
    * Query for invalid tag does not return an empty list like other endpoints do
* Video endpoint is still 'get_bulk', which should change
* Profile API
    * `mark_watched` checks if a video has been watched; This is a misleading name
    * `mark_watched_bulk` takes `profile` as a parameter, others take `profile_id`; Update for consistency



## Tests

* Additional tests
    * GET /api/profile/in_progress
        * Need to test passing a video ID as a parameter
        * However, need to be sure that video ID is listed as in progress in the DB first
    * DELETE /api/profile/in_progress
        * Need to test that we can remove an in progress video
        * However, there needs to be one to remove
    * POST /api/profile/mark_watched
        * Test marking a video as watched
* Not yet testing endpoints that update the database
    * POST /api/videos/metadata
    * POST /api/videos/add
* Add tests for api_profile
    * After other improvements are made



## Investigate

* Should images, such as avatars, be stored in the frontend, or somewhere else?
* Other test types, such as 'debug' and 'coverage
* How to mock API tests that are 'destructive'; Eg, add/delete items from the DB
* Live version has a bug while showing thumbnail for snippets (noticed on themes)
    * Does the dev version have this too?
* Do we really need both POST and UPDATE methods for updating in progress videos?
* API batching
    * How can we do batching?
    * Eg, home page has multiple calls to /api/videos/filter
    * Is there a way to run this as a batch?


