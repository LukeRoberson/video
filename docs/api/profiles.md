# Overview

API endpoints that relate to profile management
</br></br>


**Implementation**

`api_profile.py`.
</br></br>


**Base URL**

/api/profile
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  | Swagger UI |
| ----------------------------------- | -------------------------------------------- | ---------- |
| /                                   | Get all profiles                             | Done       |
| /{{profile_id}}                     | Get a specific profile                       | Done       |
| /create                             | Create a profile                             |            |
| /delete{{profile_id}}               | Delete a profile                             |            |
| /update/{{profile_id}}              | Update a profile                             |            |
| clear_history/{{profile_id}}        | Clear a user's watch history                 |            |
| mark_watched_bulk                   | Check watch status on multiple videos        | Done       |
| mark_watched                        | Mark a video as watched                      | Done       |
| mark_unwatched                      | Mark a video as unwatched                    | Done       |
| watch_history                       | Check watch history for a profile*           | Done       |
| in_progress                         | Manage in-progress status for a video        | GET, POST* |
</br></br>



----
# Endpoints

## /api/profile

**Description**

Get a list of all user profiles
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/profile/{{profile_id}}

**Description**

Get a specific user profile by its ID
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/profile/create

**Description**

Create a new user profile.

Adds a name, and selects an avatar filename.

The avatar filenames exist on the server itself, not locally. Uploading new avatar images is not supported.
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

```json
{
    "name": "<Profile Name>",
    "image": "<image file name>",
}
```
</br></br>


**Response Code**

`200 OK` on success

`400 BAD REQUEST` if the body is not included, or fields are missing

`500 INTERNAL SERVER ERROR` if the create operation was unsuccessful
</br></br>


**Response Body**

A simple response to determine if this was successful.
</br></br>


| Field       | Type    | Description                                     |
| ----------- | ------- | ----------------------------------------------- |
| message     | string  | A successor fail message                        |
| success     | boolean | True means the profile was created successfully |
</br></br>


```json
{
    "message": "Created profile with ID: 10",
    "success": true
}
```
</br></br>


When fields are missing:

```json
{
    "error": "Missing required fields: name and image",
    "success": false
}
```
</br></br>




----
## /api/profile/delete/{{profile_id}}

**Description**

Delete a profile, identified by its ID.
</br></br>


**Method**

DELETE
</br></br>


**Parameters**

None
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success

`404 NOT FOUND` if the profile ID does not exist

`500 INTERNAL SERVER ERROR` if the delete operation failed
</br></br>


**Response Body**

A simple response to determine if this was successful.
</br></br>


| Field       | Type    | Description                                     |
| ----------- | ------- | ----------------------------------------------- |
| message     | string  | A successor fail message                        |
| success     | boolean | True means the profile was created successfully |
</br></br>


```json
{
    "message": "Profile with ID 10 deleted successfully.",
    "success": true
}
```
</br></br>


If the profile is not found:

```json
{
    "error": "Profile with ID 99999 not found",
    "success": false
}
```
</br></br>





----
## /api/profile/update/{{profile_id}}

**Description**

Update the name or avatar filename for a profile.
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

| Field       | Type    | Description                   |
| ----------- | ------- | ----------------------------- |
| name        | string  | The profile name              |
| icon        | string  | The filename for their avatar |

```json
{
    "name": "<new profile name>",
    "icon": "<new profile icon>"
}
```
</br></br>


**Response Code**

`200 OK` on success

`400 BAD REQUEST` if fields are missing

`404 NOT FOUND` if the profile does not exist

`500 INTERNAL SERVER ERROR` if the operation was unsuccessful
</br></br>


**Response Body**

A simple response to determine if this was successful.
</br></br>


| Field       | Type    | Description                                     |
| ----------- | ------- | ----------------------------------------------- |
| message     | string  | A successor fail message                        |
| success     | boolean | True means the profile was created successfully |
</br></br>


```json
{
    "message": "Profile with ID 5 updated successfully.",
    "success": true
}
```
</br></br>


If bad fields are provided in the request body:

```json
{
    "error": "Failed to update profile with ID 5",
    "success": false
}
```
</br></br>


If the profile does not exist:

```json
{
    "error": "Profile with ID 99999 not found",
    "success": false
}
```
</br></br>




----
## /api/profile/watch_history

**Description**

Gets the watch history for the current active profile.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/profile/clear_history/{{profile_id}}

**Description**

Clears the watch history in a user's profile.
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

The body of the request contains the ID of the video to remove from the watch history.

This is an optional field. If it is not present, all history is cleared.
</br></br>


| Field       | Type    | Description                            |
| ----------- | ------- | -------------------------------------- |
| video_id    | integer | The video to remove from watch history |
</br></br>


```json
{
    "video_id": "{{int}}"
}
```
</br></br>


**Response Code**

`200 OK` on success

`404 NOT FOUND` If the profile is not found

`500 INTERNAL SERVER ERROR` if there was a problem with clearing the video
</br></br>


**Response Body**

The response is simply 'message' and 'success' fields.
</br></br>


```json
{
    "message": "Cleared video 1871 from watch history of profile 2.",
    "success": true
}
```
</br></br>




----
## GET /api/profile/in_progress

**Description**

Manages in-progress video tracking for user profiles.

This tracks where a video is up to, so it can be resumed there in future.

Specifically, the GET method will either:
* Get a list of in progress videos for a particular profile
* Check if a specific video is in progress for a specific profile

This endpoint also supports POST and DELETE methods.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## POST /api/profile/in_progress

**Description**

Manages in-progress video tracking for user profiles.

This adds a video to the list of in progress videos for the specific profile, and stores the playback location of the video.

This endpoint also supports GET and DELETE methods.
</br></br>


> [!NOTE]
> If a video is already marked as in progress, this endpoint will overwrite it's status.
</br></br>


**Method**

POST
</br></br>


**Parameters**

| Field       | Type    | Mandatory | Description                                                             |
| ----------- | ------- | --------- | ----------------------------------------------------------------------- |
| profile     | integer | Yes       | The profile to check for                                                |
</br></br>

> [!NOTE]
> If the profile ID is not included as a parameter, a 400 error will be returned
</br></br>


**Body**

A body is included with information to update the current playback time of a video.
</br></br>


| Field        | Type    | Description                                         |
| ------------ | ------- | --------------------------------------------------- |
| video_id     | integer | The ID of the video to update                       |
| current_time | integer | The current playback time, in seconds, of the video |
</br></br>


```json
{
    "video_id": "<int>",
    "current_time": "<int>"
}
```
</br></br>


**Response Code**

`201 CREATED` If adding the video was successful

`400 BAD REQUEST` If the profile ID is not provided.

`400 BAD REQUEST` If a JSON body was required, but none provided (eg, POST and UPDATE)

`400 BAD REQUEST` If fields in the body are invalid

`404 NOT FOUND` If an invalid profile is provided

`404 NOT FOUND` If the video ID does not exist

`415 UNSUPPORTED MEDIA TYPE` if the body is missing

`500 INTERNAL SERVER ERROR` If there was a problem updating the database
</br></br>


**Response Body**

The response body contains 'message' and 'success' fields to report on the status of the operation.
</br></br>


```json
{
    "message": "Added in-progress video 1 at position 60",
    "success": true
}
```
</br></br>


If the 'profile' parameter is not included:

```json
{
    "error": "Missing 'profile' parameter in request",
    "success": false
}
```
</br></br>


If an invalid profile is provided:

```json
{
    "error": "Profile not found",
    "success": false
}
```
</br></br>


If required fields are missing from the body:

```json
{
    "error": "Missing 'video_id' or 'current_time' in request data",
    "success": false
}
```
</br></br>


If the required field values have incorrect types:

```json
{
    "error": "Invalid data types. Must be integers",
    "success": false
}
```
</br></br>




----
## DELETE /api/profile/in_progress

**Description**

Manages in-progress video tracking for user profiles.

This is to remove a video as being in progress. This could be when:
* A user manually clears it from their profile
* A video is marked as watched

This endpoint also supports GET and POST methods.
</br></br>


**Method**

DELETE
</br></br>


**Parameters**

| Field       | Type    | Mandatory | Description                                                             |
| ----------- | ------- | --------- | ----------------------------------------------------------------------- |
| profile     | integer | Yes       | The profile to check for                                                |
</br></br>

> [!NOTE]
> If the profile ID is not included as a parameter, a 400 error will be returned
</br></br>


**Body**

For POST and UPDATE methods, a body is included with information to update the current playback time of a video.
</br></br>


| Field        | Type    | Description                                         |
| ------------ | ------- | --------------------------------------------------- |
| video_id     | integer | The ID of the video to update                       |
</br></br>


```json
{
    "video_id": "<int>",
    "current_time": "<int>"
}
```
</br></br>


**Response Code**

`200 OK` on success

`400 BAD REQUEST` If the profile ID is not provided.

`400 BAD REQUEST` If a JSON body was required, but none provided (eg, POST and UPDATE)

`400 BAD REQUEST` If fields in the body are invalid

`404 NOT FOUND` If an invalid profile is provided

`500 INTERNAL SERVER ERROR` If a video could not be processed
</br></br>


**Response Body**

Contains a simple status and message.
</br></br>


```json
{
    "message": "Removed in-progress videos successfully",
    "success": true
}
```
</br></br>


If the 'profile' parameter is not included:

```json
{
    "error": "Missing 'profile' parameter in request",
    "success": false
}
```
</br></br>


If an invalid profile is provided:

```json
{
    "error": "Profile not found",
    "success": false
}
```
</br></br>




----
## /api/profile/mark_watched_bulk

**Description**

Check multiple videos to see if they have been marked as watched.

This checks against a profile ID included in the request
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>




----
## /api/profile/mark_watched

**Description**

Mark a video as watched for a specific profile.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>




----
## /api/profile/mark_unwatched

**Description**

Mark a video as unwatched for a given profile ID.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>

