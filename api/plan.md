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
    * [x] `api_profile`: get_watched and check_watched_bulk
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
    * [x] Profile Edit: Can't mark videos as watched
    * [x] Profile Edit: Marking a video as watched can result in duplicates
    * [x] Profile edits: UI doesn't reflect changes straight away
    * [x] After deleting a profile:
    * [ ] Confirm that guests can't have in progress videos, or watched videos
    * [ ] Confirm that deleting a profile will remove their watch history and in progress videos
    * [ ] Categories: Invalid main/sub combinations (eg, Programs and Events/Monthly Programs) still return data
    * [ ] `/api/search` doesn't seems to be enforcing the page size limit


</br></br>

