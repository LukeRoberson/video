

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
    * [ ] Update profile
    * [ ] Clear watch history
    * [ ] Mark video as watched
    * [x] Get active profile
    * [x] Set active profile
    * [ ] List avatars
5. Migrate video endpoints
    * [ ] Load videos (title, thumbnail) into categories
    * [ ] Update in progress status
    * [ ] Mark a video as watched
    * [ ] Mark a video as unwatched
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


* Some pages, eg scriptures, do not use an API; They read the DB directly
    * Will need to add an endpoint in these cases
* Where is the port set?
    * Using tcp/5010 for the new API

</br></br>


---
# Endpoints

## Frontend Usage


| File                  | File Usage                       | Endpoint                                     | Description                          |
| --------------------- | -------------------------------- | -------------------------------------------- | ------------------------------------ |
| metadata.ts           | Admin page                       | /api/video/metadata                          | Add metadata to videos               |
| metadata.ts           | Admin page                       | /api/scripture                               | Add a scripture                      |
| videoAdd.ts           | Admin page                       | /api/videos/csv                              | Read CSV file                        |
| videoAdd.ts           | Admin page                       | /api/videos/add                              | Add video                            |
| populateCategories.ts | Load videos into categories page | /api/categories/{categoryId}/{subcategoryId} | Get a list of videos                 |
| profileEdit.ts        | Editing user profiles            | /api/profile/pictures                        | Get a list of avatars                |
| profileEdit.ts        | Editing user profiles            | /api/profile/delete/{id}                     | Delete a profile                     |
| profileEdit.ts        | Editing user profiles            | /api/profile/update/{id}                     | Update a profile                     |
| profileEdit.ts        | Editing user profiles            | /api/profile/clear_history/{id}              | Clear profile watch history          |
| profileEdit.ts        | Editing user profiles            | /api/profile/mark_watched                    | Mark a video as watched              |
| profileMgmt.ts        | Profile management               | /api/profile/create                          | Create a profile                     |
| profileMgmt.ts        | Profile management               | /api/profile/get_active                      | Get the active profile               |
| profileMgmt.ts        | Profile management               | /api/profile/set_active                      | Set the active profile               |
| profileMgmt.ts        | Profile management               | /api/profile/delete/{id}                     | Delete a profile                     |
| profileMgmt.ts        | Profile management               | /edit_profile/{id}                           | Edit a profile                       |
| videoPlayer.ts        | Play videos                      | /api/profile/in_progress                     | Update the time of video in progress |
| videoPlayer.ts        | Play videos                      | /api/profile/mark_watched                    | Mark a video as watched              |
| videoPlayer.ts        | Play videos                      | /api/profile/mark_unwatched                  | Mark a video as unwatched            |

</br></br>



## Backend Mapping

| Endpoint                                       | File           | Blueprint      | Function             |
| ---------------------------------------------- | -------------- | -------------- | -------------------- |
| /api/profile/create                            | api_profile.py | profile_api_bp | create_profile       |
| /api/profile/set_active                        | api_profile.py | profile_api_bp | set_active_profile   |
| /api/profile/get_active                        | api_profile.py | profile_api_bp | get_active_profile   |
| /api/profile/mark_watched                      | api_profile.py | profile_api_bp | mark_watched         |
| /api/profile/mark_unwatched                    | api_profile.py | profile_api_bp | mark_unwatched       |
| /api/profile/in_progress                       | api_profile.py | profile_api_bp | in_progress_videos   |
| /api/profile/delete/<profile_id>               | api_profile.py | profile_api_bp | delete_profile       |
| /api/profile/update/<profile_id>               | api_profile.py | profile_api_bp | update_profile       |
| /api/profile/clear_history/<profile_id>        | api_profile.py | profile_api_bp | clear_watch_history  |
| /api/profile/pictures                          | api_profile.py | profile_api_bp | get_profile_pictures |


| Endpoint                                       | File           | Blueprint      | Function             |
| ---------------------------------------------- | -------------- | -------------- | -------------------- |
| /api/search                                    | api_search.py  | search_bp      | search_videos        |
| /api/search/reindex                            | api_search.py  | search_bp      | reindex_all_videos   |
| /api/search/status                             | api_search.py  | search_bp      | search_status        |
| /api/search/advanced                           | api_search.py  | search_bp      | advanced_search      |


| Endpoint                                       | File           | Blueprint      | Function             |
| ---------------------------------------------- | -------------- | -------------- | -------------------- |
| /api/video/metadata                            | api.py         | api_bp         | add_video_metadata   |
| /api/videos/csv                                | api.py         | api_bp         | get_videos_csv       |
| /api/videos/add                                | api.py         | api_bp         | add_videos           |
| /api/search/videos                             | api.py         | api_bp         | search_videos        |
| /api/search/advanced                           | api.py         | api_bp         | advanced_search      |
| /api/scripture                                 | api.py         | api_bp         | add_scripture_text   |
| /api/categories/<category_id>/<subcategory_id> | api.py         | api_bp         | category_filter      |

</br></br>



# Cleanup

* profileMgmt.ts
    * Base URLs in ProfileMgmtConfig
    * URL selection in setActiveProfile



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



</br></br>
