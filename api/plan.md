

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
    * [x] Home page; Down to 5s loading time
    * [ ] Character pages; 24s to load the 'Aaron' profile (http://localhost:5000/character/230)
    * [ ] Speaker pages; 67s to load 'Anthony Morris' (http://localhost:5000/speaker/284)
    * [ ] Scripture pages; 38s to load Heb 11:6 (http://localhost:5000/scripture/1679)
    * [ ] Location pages; 26s to load 'Africa' (http://localhost:5000/location/15)
    * [ ] Tag pages; 4:26 to load 'faith' (http://localhost:5000/tag/971)
    * [ ] Video detail; 22s to load '2026 GB update #1' (http://localhost:5000/video/3083)
    * [ ] Themes; 93s to load 'Powerful by Faith' (http://localhost:5000/theme/2021_powerful_by_faith)
    * [ ] Categories; 22s to load 'Broadcasting' (http://localhost:5000/broadcasting)
    * [ ] Advanced Search page; 10s to load (http://localhost:5000/search/advanced)
    * [ ] Advanced Search; 13s to search 'With Eyes of Faith' (http://localhost:5000/search/advanced?q=With+Eyes+of+Faith)
10. Clean up bugs
    * [x] In categories, watch status on individual videos is not showing
    * [x] Terminal errors for one user (500-Marija_Golubiček.png) due to unicode
    * [x] 'Logging Error' at terminal when searching with ElasticSearch
    * [x] Cannot mark videos as watched
    * [ ] Searches sometimes throw unicode errors in the terminal
    * [ ] Profile edits
        * Profile updates work successfully (eg, name, clearing watch history)
        * They do not update on the page immediately
    * [ ] Categories: Invalid main/sub combinations (eg, Programs and Events/Monthly Programs) still return data
    * [ ] Getting speakers for a video; API displays errors
        * Error retrieving speakers for video 1: Cannot operate on a closed database.
        * DEBUG - Module api_speaker: Function get_video_speakers
    * [ ] After deleting a profile:
        * The profile happened to be ID: 6
        * When loading the profile selection screen, API reports an error
            * DEBUG - Module: api_profile.py, Function: get_profile
            * ERROR - Profile with ID 6 not found.
        * Page loads fine, nothing in console
    * [ ] `/api/search` doesn't seems to be enforcing the page size limit


</br></br>





# Notes

## Performance

* Home page
    * `web.py`
    * `home()`
* API calls:
    * GET /api/profile/in_progress?profile={ID}
    * POST /api/videos/get_bulk
    * /api/videos/filter?cat=1&latest=1
    * /api/videos/filter?cat=3&latest=1
    * /api/videos/filter?latest=9
* Updated (5s loading time)
    * REMOVED: GET /api/categories
        * Now uses a cache to improve performance
    * GET /api/profile/4
        * This is being called as part of the base template
        * This is client-side, so not really an issue
    * Added workers to handle API calls
    * Added 'as_complete' for better worker efficiency

* Character details page
    * `web_dynamic`
    * `character_details()`
* API calls:
    * GET /api/characters
        * Gets details for a specific character
    * GET /api/videos/filter
        * Gets a list of videos for this character
    * GET /api/profile/mark_watched
        * Checks if videos have been watched by the current profile
        * One call for each video, means many calls
* Updated:
    * Loads in 7s for 'Aaron'
    * Bulk check of watched videos, rather than one at a time

* Speaker details page
    * `web_dynamic`
    * `speaker_details()`
* API calls:
    * /api/speakers
        * Gets details for the specific speaker
    * /api/videos/filter
        * Gets videos associated with the speaker
    * /api/profile/mark_watched
        * Checks if each video has been watched by the current profile
* Updates:
    * Loads in 8s for 'Anthony Morris'
    * Bulk check of watched videos, rather than one at a time

* Scripture details page
    * `web_dynamic`
    * `scripture_details()`
* API calls:
    * /api/scriptures
        * Gets details for the specific scripture
    * /api/videos/filter
        * Gets videos associated with the scripture
    * /api/profile/mark_watched
        * Checks if each video has been watched by the current profile
* Updates:
    * Loads in 7s for Heb 11:6
    * Bulk check of watched videos, rather than one at a time

* Location detail page
    * `web_dynamic`
    * `location_details()`
* API calls:
    * /api/locations
        * Gets details for the specific location
    * /api/videos/filter
        * Gets videos associated with the location
    * /api/profile/mark_watched
        * Checks if each video has been watched by the current profile
* Updates:
    * Loads in 7s for 'Africa'
    * Bulk check of watched videos, rather than one at a time

* Tag detail page
    * `web_dynamic`
    * `tag_details()`
* API calls:
    * /api/tags
        * Gets details for the specific tag
    * /api/videos/filter
        * Gets videos associated with the tag
    * /api/profile/mark_watched
        * Checks if each video has been watched by the current profile
* Updates:
    * Loads in 8s for 'faith'
    * Bulk check of watched videos, rather than one at a time

* Video details
    * `web_dynamic`
    * `video_details()`
    * Bug: Error retrieving speakers for video 3083: Cannot operate on a closed database.
    * Bug: An error occurred while retrieving similar videos for video ID 3083
* API calls:
    * /api/videos/get_bulk
        * Gets the details for the video
    * /api/categories/video/{video_id}
        * Gets categories the video belongs to
    * /api/tags/video/{video_id}
        * Gets tags associated with a video
    * /api/locations/video/{video_id}
        * Gets locations associated with a video
    * /api/speakers/video/{video_id}
        * Gets speakers associated with the video
    * /api/characters/video/{video_id}
        * Gets characters associated with a video
    * /api/scriptures/video/{video_id}
        * Gets scriptures associated with a video
    * /api/profile/mark_watched
        * Check if the video has been watched on this profile
    * /api/profile/in_progress
        * Check if the video is in progress for the profile
    * /api/similarity/{video_id}
        * Get a list of similar videos
    * /api/videos/get_bulk
        * x3
        * Get details for each similar video

* Themes pages
    * `web_dynamic`
    * `theme()`
* API calls:
    * /api/videos/get_bulk
        * Gets video details
        * This is a synchronous loop for every video in the file

* Categories
    * `web_categories.py`
    * `render_category_page()`
* API calls:
    * /api/categories/{category}
        * Resolve the main category name to ID
        * Can make use of the cache now
    * /api/categories/{category}
        * Resolve each subcategory name to an ID
        * Called several times synchronously
        * Can make use of the cache now
    * /api/categories/{main_id}/{sub_cat_id}
        * Get a list of videos in each main/sub category combo
    * /api/profile/mark_watched_bulk
        * Check watch status of videos
        * Run for each main/sub category combo
        * Already checks all videos in a single request



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


