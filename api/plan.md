

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
    * [ ] Home page; 7x separate API calls (get latest videos, get latest news and broadcasting, get watch status for each)
    * [ ] Character; Separate API call for each video to check watch status
    * [ ] Video; About 13 calls (video details, various metadata, similarity, watch status on similar videos, etc)
    * [ ] Themes; It makes many calls to the API instead of just one or two
    * [ ] Tag; Multiple API calls to check which videos have been watched
    * [ ] Check if a video has been watched: Check multiple videos in a single call
    * [ ] One endpoint to get characters, tags, etc from a given video (currently one per type)
10. Clean up bugs
    * [ ] In categories, watch status on individual videos is not showing
    * [x] Terminal errors for one user (500-Marija_Golubiček.png) due to unicode
    * [ ] Searches sometimes throw unicode errors in the terminal
    * [ ] When saving a profile name change, this is not immediately reflected in the edit screen
    * [ ] Categories: Invalid main/sub combinations (eg, Programs and Events/Monthly Programs) still return data
    * [x] 'Logging Error' at terminal when searching with ElasticSearch


</br></br>





# Notes

* Not yet testing endpoints that update the database
    * POST /api/videos/metadata
    * POST /api/videos/add
* `/api/categories/{{category_id}}/{{subcategory_id}}`
    * Contains a 'videos' list in the response, which is unnecessary
* Investigate:
    * Should images, such as avatars, be stored in the frontend, or somewhere else?
    * Other test types, such as 'debug' and 'coverage
    * How to mock API tests that are 'destructive'; Eg, add/delete items from the DB
    * Live version has a bug while showing thumbnail for snippets (noticed on themes)
        * Does the dev version have this too?
    * Do we really need both POST and UPDATE methods for updating in progress videos?
* Searching
    * `/api/search` doesn't seems to be enforcing the page size limit
    * reindexing: This can take time, so maybe respond with 'starting', and check a URL to find an updated status
* Speakers endpoint:
    * Query for invalid speaker does not return an empty list like other endpoints do
* Tags endpoint:
    * Query for invalid tag does not return an empty list like other endpoints do
* Video endpoint is still 'get_bulk', which should change

* Improve logging in api_profile
    * After other improvements are made
* Add tests for api_profile
    * After other improvements are made
* Create helper functions for reused components:
    * Check if a video exists
    * Logging debugs and warnings during field validation
* Get active profile
    * This is used as an API call, as well as to verify that a profile exists
    * Would be better as a helper function
* Checking if a video exists
    * Used in many places, should be a helper function

* Additional tests
    * GET /api/profile/in_progress
        * Need to test passing a video ID as a parameter
        * However, need to be sure that video ID is listed as in progress in the DB first
    * DELETE /api/profile/in_progress
        * Need to test that we can remove an in progress video
        * However, there needs to be one to remove

* Bug:
    * The 'set active profile' endpoint happily will set a non-existant profile as active
    * Error retrieving speakers for video 1036: Cannot operate on a closed database.
        * DEBUG - Module api_speaker: Function get_video_speakers
        * INFO - No speakers found for video ID 1036
    * After deleting a profile:
        * The profile happened to be ID: 6
        * When loading the profile selection screen, API reports an error
            * DEBUG - Module: api_profile.py, Function: get_profile
            * ERROR - Profile with ID 6 not found.
        * Page loads fine, nothing in console
    * Mark as watched
        * Failing from the profile page
        * Haven't tested from a video page
    * Clearing watch history
        * This works, but does not update the page in real time


