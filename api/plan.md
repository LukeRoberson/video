

# Plan

1. Clone main DB classes into the API folder
    * [x] sql_db.py
2. Migrate Admin endpoints
    * [x] Add metadata
    * [x] Add a scripture
3. Clone user DB classes into the API folder
    * [x] local_db.py
4. Migrate user profile management
    * [x] Add profile
    * [x] Delete profile
    * [x] Update profile
    * [x] Clear watch history
    * [x] Get active profile
    * [x] Set active profile
5. Migrate video endpoints
    * [x] Load videos (title, thumbnail) into categories
    * [x] Update in progress status
    * [x] Mark a video as watched
    * [x] Mark a video as unwatched
6. Additional pages
    * [ ] Scriptures
    * [ ] Speakers
    * [ ] Characters
    * [ ] Tags
7. Search
    * [ ] Normal search
    * [ ] Advanced search
    * [ ] Reindex
    * [ ] Status
8. Other
    * [ ] Avatar list in profile management; API or frontend?



* Some pages, eg scriptures, do not use an API; They read the DB directly
    * Will need to add an endpoint in these cases


</br></br>


---
# Endpoints

## Frontend Usage


| File                  | File Usage                       | Endpoint                                     | Description                          |
| --------------------- | -------------------------------- | -------------------------------------------- | ------------------------------------ |
| videoAdd.ts           | Admin page                       | /api/videos/csv                              | Read CSV file                        |
| videoAdd.ts           | Admin page                       | /api/videos/add                              | Add video                            |
| profileEdit.ts        | Editing user profiles            | /api/profile/pictures                        | Get a list of avatars                |

</br></br>



## Backend Mapping

| Endpoint                                       | File           | Blueprint      | Function             |
| ---------------------------------------------- | -------------- | -------------- | -------------------- |
| /api/profile/pictures                          | api_profile.py | profile_api_bp | get_profile_pictures |


| Endpoint                                       | File           | Blueprint      | Function             |
| ---------------------------------------------- | -------------- | -------------- | -------------------- |
| /api/search                                    | api_search.py  | search_bp      | search_videos        |
| /api/search/reindex                            | api_search.py  | search_bp      | reindex_all_videos   |
| /api/search/status                             | api_search.py  | search_bp      | search_status        |
| /api/search/advanced                           | api_search.py  | search_bp      | advanced_search      |


| Endpoint                                       | File           | Blueprint      | Function             |
| ---------------------------------------------- | -------------- | -------------- | -------------------- |
| /api/videos/csv                                | api.py         | api_bp         | get_videos_csv       |
| /api/videos/add                                | api.py         | api_bp         | add_videos           |
| /api/search/videos                             | api.py         | api_bp         | search_videos        |
| /api/search/advanced                           | api.py         | api_bp         | advanced_search      |

</br></br>



# Cleanup

* profileMgmt.ts
    * Base URLs in ProfileMgmtConfig
    * URL selection in setActiveProfile
* profileEdit.ts
    * Base URLs in ProfileEditConfig
* populateCategories.ts
    * Base URLs in CategoryConfig



---
# Notes

* Why do we need profileEdit.ts and profileMgmt.ts?
    * Overlapping functionality?
    * Consolidate them?
* Duplicate endpoints?
    * /api/profile/update/{id}
    * /edit_profile/{id}
* videoPlayer.ts
    * Move API endpoints to a variable
* Delete profile Endpoint
    * Used in both profileMgmt.ts and profileEdit.ts
    * profileMgmt - Delete profile from the profile selection screen
    * profileEdit - Delete profile from the Edit profile screen
    * These could be consolidated
* Updating profiles
    * When saving a name change, it's not immediately reflected in the edit screen
* Enpoints to mark as watched/unwatched
    * This uses stateful information; Gets the active user
    * Would be better to pass the active user in the request
* Active user
    * Should this be tracked by the API?
    * Would frontend be better, and it passes the ID to the API?
* videoPlayer.ts
    * Does not have API paths as constants as other files do
* in progress endpoint
    * Uses active profile within the API
    * Better to pass active profile ID from frontend?




</br></br>
