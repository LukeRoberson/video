

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
    * [ ] Add a debug mode when starting the API (flask debug + logging level)
    * [ ] Add better logging to API files
    * [x] Create and organize postman files for API testing
    * [x] Create pytest structure for automated testing
6. Clean up API Calls
    * [x] Set video base URL to /api/videos
    * [x] Set category base URL to /api/category
    * [x] Set scripture base URL to /api/scriptures
    * [ ] TypeScript files (below)
    * [ ] Duplicate API calls (profileEdit vs profileMgmt)
7. Consolidate endpoints
    * [ ] Combine get_video, get_videos_bulk, and filter_videos (api_video.py)
    * [ ] Combine endpoints to get all characters and get one specific character (api_character.py)
    * [ ] Combine 'get all speakers' with 'get specific speaker' (api_speaker.py)
    * [ ] Combine 'get all tags' with 'get specific tag' (api_tags.py)
8. Active user redesign
    * [ ] Get the frontend to track the active user, not the API (eg, mark as watched/unwatched, in progress videos)
        * [ ] `api_category.py` - Category filter
    * [ ] API calls from the frontend should include the active user if needed
    * [ ] Clean up profile.py, as there's some code reuse around active profiles
9. Performance
    * [ ] Home page; 7x separate API calls (get latest videos, get latest news and broadcasting, get watch status for each)
    * [ ] Character; Separate API call for each video to check watch status
    * [ ] Video; About 13 calls (video details, various metadata, similarity, watch status on similar videos, etc)
    * [ ] Themes; It makes many calls to the API instead of just one or two
    * [ ] Tag; Multiple API calls to check which videos have been watched
10. Clean up bugs
    * [ ] In categories, watch status on individual videos is not showing
    * [ ] Terminal errors for one user (500-Marija_Golubiček.png) due to unicode
    * [ ] Searches sometimes throw unicode errors in the terminal
    * [ ] When saving a profile name change, this is not immediately reflected in the edit screen
    * [ ] Categories: Invalid main/sub combinations (eg, Programs and Events/Monthly Programs) still return data
    * [ ] 'Logging Error' at terminal when searching with ElasticSearch


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


# Notes

* Not yet testing endpoints that update the database
    * POST /api/videos/metadata
    * POST /api/videos/add
    * POST /api/profile/create
    * DELETE /api/profile/delete/{{id}}
    * POST /api/profile/update/{{id}}
* The 'set active profile' endpoint happily will set a non-existant profile as active
* `/api/categories/{{category_id}}/{{subcategory_id}}`
    * Contains a 'videos' list in the response, which is unnecessary
* `api_profile.py` still needs to be updated with `api_success` and `api_error`
* Investigate:
    * Should images, such as avatars, be stored in the frontend, or somewhere else?
    * Other test types, such as 'debug' and 'coverage
    * How to mock API tests that are 'destructive'; Eg, add/delete items from the DB
* Investigate:
    * Live version has a bug while showing thumbnail for snippets (noticed on themes)
    * Does the dev version have this too?
* Need to check that we're using `api_error` in all the right places too
    * search for 'make_response', and see where that's used
* Searching
    * `/api/search` doesn't seems to be enforcing the page size limit
    * reindexing: This can take time, so maybe respond with 'starting', and check a URL to find an updated status
