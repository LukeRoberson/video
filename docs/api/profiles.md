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

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /                                   | Get all profiles                             |
| /{{profile_id}}                     | Get a specific profile                       |
| /create                             | Create a profile                             |
| /delete{{profile_id}}               | Delete a profile                             |
| /update/{{profile_id}}              | Update a profile                             |
| set_active                          | Set the active profile*                      |
| get_active                          | Get the active profile*                      |
| clear_history/{{profile_id}}        | Clear a user's watch history                 |
| mark_watched                        | Checks watch status for a video*             |
| mark_watched_bulk                   | Check watch status on multiple videos*       |
| mark_watched                        | Mark a video as watched*                     |
| mark_unwatched                      | Mark a video as unwatched*                   |
| watch_history                       | Check watch history for a profile*           |
| in_progress                         | Manage in-progress status for a video        |
</br></br>



----
# Endpoints

## /api/profile

**Description**

Get a list of all user profiles
</br></br>


**Method**

GET
</br></br>


**Parameters**

None
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

Returns in 'data' and 'success' format.

'data' include a list of profiles, each describing that profile.
</br></br>


| Field      | Type    | Description                                           |
| ---------- | ------- | ----------------------------------------------------- |
| id         | integer | The profile ID                                        |
| name       | string  | The profile name                                      |
| image      | string  | A filename for the profile's avatar                   |
| admin      | integer | Whether the user is an admin (1 for yes, null for no) |
| created_at | string  | When the profile was created                          |
</br></br>


```json
{
    "data": [
        {
            "admin": 1,
            "created_at": "2025-06-30 01:24:03",
            "id": 2,
            "image": "amos_1.png",
            "name": "Luke"
        }
    ],
    "success": true
}
```
</br></br>





----
## /api/profile/{{profile_id}}

**Description**

Get a specific user profile by its ID
</br></br>


**Method**

GET
</br></br>


**Parameters**

None
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success

`404 NOT FOUND` if the profile does not exist.
</br></br>


**Response Body**

Response in 'data' and 'success' format.

The single entry in 'data' describes the profile.

This is effectively returning one single entry from the entire list (as found in `/api/profile`)
</br></br>


| Field      | Type    | Description                                           |
| ---------- | ------- | ----------------------------------------------------- |
| id         | integer | The profile ID                                        |
| name       | string  | The profile name                                      |
| image      | string  | A filename for the profile's avatar                   |
| admin      | integer | Whether the user is an admin (1 for yes, null for no) |
| created_at | string  | When the profile was created                          |
</br></br>


```json
{
    "data": {
        "admin": 1,
        "created_at": "2025-06-30 01:24:03",
        "id": 2,
        "image": "amos_1.png",
        "name": "Luke"
    },
    "success": true
}
```
</br></br>


If a profile is not found:

```json
{
    "error": "Profile with ID 1 not found",
    "success": false
}
```
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
## /api/profile/set_active

**Description**

Set the active profile for this session.

This can be an existing profile, identified by the profile ID, or "guest" for guest access.

> [!NOTE]
> This will be migrated to the frontend in future.

Also sets the profile as an admin or regular user, depending on the value of the profile's 'admin' field.
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

| Field       | Type    | Description                           |
| ----------- | ------- | ------------------------------------- |
| profile_id  | integer | The profile to set active, or "guest" |
</br></br>


```json
{
    "profile_id": "{{int}} or {{guest}}"
}
```
</br></br>


**Response Code**

`200 OK` on success

`400 INVALID REQUEST` if the body is missing or invalid.
</br></br>


**Response Body**

Standard 'data'/'success' response.

The 'data' field contains the active profile.
</br></br>


| Field          | Type    | Description              |
| -------------- | ------- | ------------------------ |
| active_profile | integer | The profile that was set |
</br></br>


```json
{
    "data": {
        "active_profile": 2
    },
    "success": true
}
```
</br></br>


If fields are missing from the request:

```json
{
    "error": "Missing 'profile_id' in request data",
    "success": false
}
```
</br></br>





----
## /api/profile/get_active

**Description**

Get the active profile for the current session.

If there is no active profile, this will return "guest".

> [!NOTE]
> This will be migrated to the frontend in future.
</br></br>


**Method**

GET
</br></br>


**Parameters**

None
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

A data/success message, where 'data/active_profile' describes the active profile
</br></br>


| Field       | Type    | Description                                  |
| ----------- | ------- | -------------------------------------------- |
| id          | integer | The profile's ID                             |
| name        | string  | The profile's name                           |
| image       | string  | The filename for the avatar                  |
| admin       | integer | Admin status ('1' for admin, null otherwise) |
| created_at  | string  | Date/time this profile was created           |
</br></br>


```json
{
    "data": {
        "active_profile": {
            "admin": 1,
            "created_at": "2025-06-30 01:24:03",
            "id": 2,
            "image": "amos_1.png",
            "name": "Luke"
        }
    },
    "success": true
}
```
</br></br>


If the guest profile is returned:

```json
{
    "data": {
        "active_profile": {
            "id": null,
            "image": "guest.png",
            "name": "Guest"
        }
    },
    "success": true
}
```
</br></br>





----

## /api/profile/watch_history

**Description**

Gets the watch history for the current active profile.

Note: The active profile will be migrated to the frontend in future.
</br></br>


**Method**

GET
</br></br>


**Parameters**

Pass the active profile to the endpoint.

If the parameter is missing, the active profile is assumed to be "guest", which doesn't have a watch history.
</br></br>


| Field       | Type    | Description       |
| ----------- | ------- | ----------------- |
| profile     | integer | The profile's ID. |
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

The response contains 'data', 'message', and the 'success' status.

'data' is a list of entries, where each entry describes a video in the watch history.
</br></br>


| Field        | Type    | Description                                                   |
| ------------ | ------- | ------------------------------------------------------------- |
| profile_id   | integer | The ID of the profile used for the request                    |
| video_id     | integer | The ID of the video                                           |
| current_time | integer | The timestamp this profile is up to in the video (in seconds) |
| watched_at   | string  | Date/time the video was watched                               |
</br></br>


```json
{
    "data": [
        {
            "current_time": 0,
            "id": 476,
            "profile_id": 2,
            "video_id": 1871,
            "watched_at": "2026-01-18 12:51:26.409769"
        }
    ],
    "message": "Retrieved watch history successfully",
    "success": true
}
```
</br></br>


If the guest profile is active:

```json
{
    "message": "No watch history for guest profile",
    "success": true
}
```
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


**Method**

GET
</br></br>


**Parameters**

| Field       | Type    | Mandatory | Description                                                             |
| ----------- | ------- | --------- | ----------------------------------------------------------------------- |
| profile     | integer | Yes       | The profile to check for                                                |
| video_id    | integer | No        | Optional video ID to check status for (rather than checking all videos) |
</br></br>

> [!NOTE]
> If the profile ID is not included as a parameter, a 400 error will be returned
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success

`400 BAD REQUEST` If the profile ID is not provided.

`404 NOT FOUND` If an invalid profile is provided
</br></br>


**Response Body**

Includes the usual 'data', 'message', and 'success' fields.

The 'data' field is a list of videos in progress, where each entry describes the status of the video.
</br></br>


| Field        | Type    | Description                                           |
| ------------ | ------- | ----------------------------------------------------- |
| profile_id   | integer | The profile ID that was requested                     |
| video_id     | integer | The ID of the video in progress                       |
| current_time | integer | The playback position, in seconds                     |
| updated_at   | string  | Date/time when the playback position was last updated |
</br></br>


```json
{
    "data": [
        {
            "current_time": 8,
            "profile_id": 2,
            "updated_at": "2026-01-17 07:14:08",
            "video_id": 2834
        }
    ],
    "message": "Retrieved in-progress videos successfully",
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
## GET /api/profile/mark_watched

**Description**

Check if a specific video has been marked as watched for a profile.

This checks against the active profile for this session.

Note: The active profile will be migrated to the frontend in future.
</br></br>


**Method**

GET
</br></br>


**Parameters**

| Field       | Type    | Description                           |
| ----------- | ------- | ------------------------------------- |
| profile     | integer | The profile to check watch status for |
| video_id    | integer | The video to check status for         |
</br></br>


> [!NOTE]
> If the profile is not included as a parameter, the API will get it from the active session.
> This will change in future, as the API shouldn't track the active session.


**Body**

None
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

'data' and 'success' fields, where 'data' describes the watch status of a video.
</br></br>


| Field       | Type    | Description                                       |
| ----------- | ------- | ------------------------------------------------- |
| video_id    | integer | Video that was checked                            |
| watched     | boolean | true or false, to indicate if it has been watched |
</br></br>


```json
{
    "data": {
        "video_id": 1871,
        "watched": false
    },
    "success": true
}
```
</br></br>





----
## /api/profile/mark_watched_bulk

**Description**

Check multiple videos to see if they have been marked as watched.

This checks against the active profile for this session.

Note: The active profile will be migrated to the frontend in future.
</br></br>


**Method**

POST
</br></br>


**Parameters**

| Field       | Type    | Description                           |
| ----------- | ------- | ------------------------------------- |
| profile     | integer | The profile to check watch status for |
</br></br>


> [!NOTE]
> If the profile is not included as a parameter, the API will get it from the active session.
> This will change in future, as the API shouldn't track the active session.
</br></br>


**Body**

| Field       | Type             | Description                  |
| ----------- | ---------------- | ---------------------------- |
| video_ids   | list of integers | A list of video IDs to check |
</br></br>


```json
{
    "video_ids": [1, 2, 3]
}
```
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

Includes 'data' and 'success' fields.

The 'data' field is an object, where each entry represents a video ID and its watch status.
</br></br>


```json
{
    "data": {
        "1": false,
        "2": false,
        "3": false
    },
    "success": true
}
```
</br></br>




----
## /api/profile/mark_watched

**Description**

Mark a video as watched.

This is performed on the active profile for this session.

Note: The active profile will be migrated to the frontend in future.
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

| Field       | Type    | Description                     |
| ----------- | ------- | ------------------------------- |
| video_id    | integer | The video ID to mark as watched |
</br></br>


```json
{
    "video_id": 1
}
```
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

Returns a simple message indicating success or failure.
</br></br>




----
## /api/profile/mark_unwatched

**Description**

Mark a video as unwatched.

This is performed on the active profile for this session.

Note: The active profile will be migrated to the frontend in future.
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

The video to mark as unwatched.
</br></br>


| Field       | Type    | Description                    |
| ----------- | ------- | ------------------------------ |
| video_id    | integer | The video to mark as unwatched |
</br></br>



**Response Code**

`200 OK` on success
</br></br>


**Response Body**

A simple message to indicate the success or failure of the operation.
</br></br>



