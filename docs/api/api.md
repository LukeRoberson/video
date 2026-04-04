# API

## Endpoints

Endpoints are categorised into these types:

| Type             | Endpoint                                           | Description                                  |
| ---------------- | -------------------------------------------------- | -------------------------------------------- |
| Categories       | /api/categories/{{category_name}}                  | Resolve a name to an ID                      |
| Categories       | /api/categories/{{category_id}}/{{subcategory_id}} | Get videos in a main/subcategory combination |
| Categories       | /api/categories/video/{{video_id}}                 | Get categories associated with a video       |
| Bible Characters | /api/characters/                                   | Get a list of all characters                 |
| Bible Characters | /api/characters/video/{{video_id}}                 | Get characters in a video                    |
| Profiles         | /api/profile/                                      | Get all profiles                             |
| Profiles         | /api/profile/{{profile_id}}                        | Get a specific profile                       |
| Profiles         | /api/profile/create                                | Create a profile                             |
| Profiles         | /api/profile/delete{{profile_id}}                  | Delete a profile                             |
| Profiles         | /api/profile/update/{{profile_id}}                 | Update a profile                             |
| Profiles         | /api/profile/clear_history/{{profile_id}}          | Clear a user's watch history                 |
| Profiles         | /api/profile/mark_watched_bulk                     | Check watch status on multiple videos        |
| Profiles         | /api/profile/mark_watched                          | Mark a video as watched                      |
| Profiles         | /api/profile/mark_unwatched                        | Mark a video as unwatched                    |
| Profiles         | /api/profile/watch_history                         | Check watch history for a profile            |
| Profiles         | /api/profile/in_progress                           | Manage in-progress status for a video        |
| Scriptures       | /api/scriptures/                                   | Get all scriptures, or update scripture text |
| Scriptures       | /api/scriptures/video/{{video_id}}                 | Get scriptures for a video                   |
| Search           | /api/search/                                       | Search through videos                        |
| Search           | /api/search/status                                 | Check search service status                  |
| Search           | /api/search/advanced                               | Perform an advanced search                   |
| Search           | /api/search/reindex                                | Reindex videos                               |
| Similarity       | /api/similarity/{{video_id}}                       | Get similar videos for a given video         |
| Speakers         | /api/speakers/                                     | Get all speakers                             |
| Speakers         | /api/speakers/{{speaker_id}}                       | Get one speaker                              | 
| Speakers         | /api/speakers/video/{{video_id}}                   | Get speakers on a video                      |
| Locations        | /api/locations/                                    | Get all locations                            |
| Locations        | /api/locations/{{location_id}}                     | Get a location                               |
| Locations        | /api/locations/video/{{video_id}}                  | Get locations by video                       |
| Tags             | /api/tags/                                         | Get all tags                                 |
| Tags             | /api/tags/video/{{video_id}}                       | Get tags on a video                          |
| Videos           | /api/videos/{{video_id}}                           | Get details for a video                      |
| Videos           | /api/videos/get_bulk                               | Get details for multiple videos              |
| Videos           | /api/videos/filter                                 | Get a filtered list of videos                |
| Videos           | /api/videos/metadata                               | Get, add, or update metadata on a video      |
| Videos           | /api/videos/csv                                    | Read a CSV file of videos                    |
| Videos           | /api/videos/add                                    | Add a new video to the database              |
</br></br>



----
## Swagger UI

These endpoints are now documented in Swagger. This is the primary source of API documentation.

This is defined in `/api/static/swagger.yaml`, and is accessible at http://localhost:5010.
</br></br>


----
## Postman

A postman collection has been exported, and is stored in `/docs/api/postman_collection.json`
</br></br>


----
## Standard Responses

### Success

On success, an API call will typically respond with a `200 OK` message.

It will also include a JSON body with a format like this:
</br></br>


```json
{
    "data": [],
    "message": "success message",
    "success": true
}
```
</br></br>


The `data` field will contain whatever information was requested from this endpoint. This will vary for each endpoint.

The `message` field is a simple user-friendly message indicating the success of the API call.

The `success` field is a boolean, indicating success or failure.
</br></br>



### Failure

On failure, the API will respond with a `4xx` or `5xx` error code. `404 NOT FOUND` is common when querying something (such as a video) that does not exist.

This will also include a JSON body in this format:
</br></br>


```json
{
    "error": "An error message describing the problem",
    "success": false
}
```
</br></br>



### Invalid Method

If an invalid method is used, a `405 METHOD NOT ALLOWED` code is returned.

