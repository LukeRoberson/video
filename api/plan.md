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
    * [x] After deleting a profile, terminal errors for that profile show
    * [x] Confirm that guests can't have in progress videos, or watched videos
    * [x] Deleting a profile does not remove their in-progress history or watch history
11. Deployment
    * [x] Update npm packages
    * [x] Update python packages
    * [x] Final unit testing
    * [x] Swagger clean up
        * [x] Finish documenting endpoints
        * [x] Schemas for errors
        * [x] Other common schemas
        * [x] Clean up old API docs
    * [x] Sync databases with the master branch
    * [ ] Update container strategy
        * [x] base image version
        * [x] Update elasticsearch
        * [x] Multiple containers (API + frontend)
        * [x] Separate deps in `pyproject.toml` for each container
        * [ ] Consider multistage build
    * [ ] Deploy to Docker server in devel environment
    * [ ] Update `changelog.yaml`
    * [ ] Update `readme.md`

</br></br>


# Python package versions

Major packages, from `pyproject.toml`:
* Flask 3.1.2 > 3.1.3
* Pandas 2.3.2 > 3.0.2
* Requests 2.32.5 > 2.33.1
* PyYAML 6.0.2 > 6.0.3
* elasticsearch 8.19.2 > 8.19.3
* Cerberus 1.3.7 > 1.3.8


(.venv) PS C:\Users\luker\OneDrive\Documents\projects\video-devel> pip list --outdated
Package            Version Latest       Type
------------------ ------- ------------ -----
attrs              25.4.0  26.1.0       wheel
Cerberus           1.3.7   1.3.8        wheel
charset-normalizer 3.4.3   3.4.6        wheel
click              8.3.0   8.3.1        wheel
coverage           7.13.4  7.13.5       wheel
elastic-transport  8.17.1  9.2.1        wheel
elasticsearch      8.19.2  9.3.0        wheel
Flask              3.1.2   3.1.3        wheel
idna               3.10    3.11         wheel
MarkupSafe         3.0.2   3.0.3        wheel
numpy              2.3.3   2.4.4        wheel
pandas             2.3.2   3.0.2        wheel
pytest             7.4.3   9.0.2        wheel
pytest-cov         4.1.0   7.1.0        wheel
pytest-timeout     2.2.0   2.4.0        wheel
pytz               2025.2  2026.1.post1 wheel
PyYAML             6.0.2   6.0.3        wheel
requests           2.31.0  2.33.1       wheel
tzdata             2025.2  2025.3       wheel
Werkzeug           3.1.3   3.1.7        wheel


