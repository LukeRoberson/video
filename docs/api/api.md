# API

## Endpoint Types

Endpoints are categorised into these types:

| Type             | Doc File      |
| ---------------- | ------------- |
| Categories       | categories.md |
| Bible Characters | characters.md |
| Profiles         | profiles.md   |
| Scriptures       | scriptures.md |
| Search           | search.md     |
| Similarity       | similarity.md |
| Speakers         | speakers.md   |
| Tags             | tags.md       |
| Videos           | videos.md     |
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



----
## Endpoints

### Admin

These are endpoints used during admin functions only. These are typically available on the 'Admin' page.

</br></br>


### Profiles


#### /api/profile

**Method**:
GET


**Description**:
Get a list of all profiles and their details


Returns:

200 OK

```json
{
    "data": [
        {
            "admin": 1,
            "created_at": "2025-06-30 01:24:03",
            "id": 2,
            "image": "amos_1.png",
            "name": "Luke"
        },
        {
            "admin": null,
            "created_at": "2025-07-03 04:35:22",
            "id": 3,
            "image": "girl_1.png",
            "name": "Bec"
        }
    ],
    "success": true
}
```

#### /api/profile/{id}

**Method**:
GET


**Description**:
Get the details for a specific profile


Returns:

200 OK

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


#### /api/profile/create

**Method**:
POST


**Description**:
Create a new profile.

Create a profile with a name, ID, and an avatar image.

Saves to the user database.


**Payload**:

| Field      | Type    | Mandatory | Notes                          |
| ---------- | ------- | --------- | ------------------------------ |
| name       | string  | Yes       | The user's name                |
| image      | string  | Yes       | Filename of the avatar's image |


Notes:
* The avatar filename represents one of the avatars on the web server, not a custom image


```json
{
    "name": "test2",
    "image": "ruth_1.png"
}
```


**returns**

200 OK

```json
{
    "message": "Created profile with ID: 9",
    "success": true
}
```


Notes:
* Success message includes the profile ID number




#### /api/profile/delete/{id}

**Method**:
DELETE


**Description**:
Delete an existing profile.

Removes entry from the user database.


Notes:
* No payload is required, just the profile ID in the URL



**returns**

200 OK

```json
{
    "message": "Profile with ID 7 deleted successfully.",
    "success": true
}
```


Notes:
* Success message includes the profile ID number that was deleted




#### /api/profile/update/{id}

**Method**:
POST


**Description**:

Updates an existing user's profile.



**Payload**:

| Field      | Type    | Mandatory | Notes                       |
| ---------- | ------- | --------- | --------------------------- |
| name       | string  | Yes       | The new name of the profile |
| icon       | string  | Yes       | Filename of the avatar      |


Notes:
* Profile matching is based on the ID in the URL, not the name in the payload
* The name in the payload is a new name to set in the database



```json
{
    "name": "Tim2",
    "icon": "man_4.png"
}
```


**returns**

200 OK

```json
{
    "message": "Profile with ID 5 updated successfully.",
    "success": true
}
```


#### /api/profile/clear_history/{id}

**Method**:
POST


**Description**:

Clears a users watch history.

If there is a JSON body, only the specific video will be cleared from history.

If there is no JSON body, clear the entire watch history.



**Payload**:

| Field      | Type    | Mandatory | Notes                                      |
| ---------- | ------- | --------- | ------------------------------------------ |
| video_id   | integer | Yes       | The ID of the video to remove from history |





```json
{
    "video_id": 1030
}
```


**returns**

200 OK

```json
{
    "message": "Cleared video 1030 from watch history of profile 2.",
    "success": true
}
```

Or, for entire history:

```json
{
    "message": "Cleared watch history for profile 2.",
    "success": true
}
```




#### /api/profile/set_active

**Method**:
POST


**Description**:
Set the active user profile in the current session.


**Payload**:

| Field      | Type    | Mandatory | Notes                         |
| ---------- | ------- | --------- | ----------------------------- |
| profile_id | integer | Yes       | The ID of the new active user |



```json
{
    "profile_id": 1
}
```


**returns**

200 OK

```json
{
    "data": {
        "active_profile": 1
    },
    "success": true
}
```


</br></br>



#### /api/profile/get_active

**Method**:
GET


**Description**:
Get the active user profile in the current session.


Returns:

200 OK

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



#### /api/profile/mark_watched (GET)

**Method**:
GET


**Description**:
Find if a video has been marked as watched.

Checks a single video only.


**Parameters**:

| Parameter  | Type    | Mandatory | Notes                    |
| ---------- | ------- | --------- | ------------------------ |
| video_id   | integer | Yes       | ID of the video to check |


Notes:
* Uses the active profile ID


```json
{
    "video_id": 123
}
```


**returns**

200 OK

```json
{
    "data": {
        "video_id": 3011,
        "watched": true
    },
    "success": true
}
```



#### /api/profile/mark_watched (POST)

**Method**:
POST


**Description**:
Marks a video as watched for a user


**Payload**:

| Field      | Type    | Mandatory | Notes                              |
| ---------- | ------- | --------- | ---------------------------------- |
| video_id   | integer | Yes       | ID of the video to mark as watched |
| profile    | integer | No        | The profile to check               |


Notes:
* Uses the active profile ID if the profile is not set


```json
{
    "video_id": 123
}
```


**returns**

200 OK

```json
{

}
```




#### /api/profile/mark_watched_bulk (POST)

**Method**:
POST


**Description**:
Check the watch status of a list of videos at once


**Payload**:

| Field      | Type    | Mandatory | Notes                         |
| ---------- | ------- | --------- | ----------------------------- |
| video_ids  | list    | Yes       | A list of video ID's to check |


Notes:
* Uses the active profile ID if the profile is not set


```json
{
    "video_ids": [123, 124, 125]
}
```


**returns**

200 OK

```json
{
    "123": true,
    "124": false,
    "125": true
}
```



#### /api/profile/mark_unwatched

**Method**:
POST


**Description**:
Marks a video as unwatched for a user


**Payload**:

| Field      | Type    | Mandatory | Notes                                |
| ---------- | ------- | --------- | ------------------------------------ |
| video_id   | integer | Yes       | ID of the video to mark as unwatched |



```json
{
    "video_id": 123
}
```


**returns**

200 OK

```json
{

}
```




#### /api/profile/watch_history (GET)

**Method**:
GET


**Description**:
Get the watch history for a given profile


**Parameters**:

| Parameter  | Type    | Mandatory | Notes             |
| ---------- | ------- | --------- | ----------------- |
| profile    | integer | Yes       | ID of the profile |



```json
{
    "profile_id": 1
}
```


**returns**

200 OK

```json
{
    "data": [
        {
            "current_time": 0,
            "id": 476,
            "profile_id": 2,
            "video_id": 1871,
            "watched_at": "2026-01-18 12:51:26.409769"
        },
        {
            "current_time": 0,
            "id": 477,
            "profile_id": 2,
            "video_id": 22,
            "watched_at": "2026-01-18 13:09:47.205452"
        }
    ],
    "message": "Retrieved watch history successfully",
    "success": true
}
```


#### /api/profile/in_progress (GET)

**Method**:
GET


**Description**:

Retrieve in-progress videos for the active profile.

May be filtered by a video_id to get a specific video.

Uses the active profile.



**Parameters**

| Parameter  | Type    | Mandatory | Notes                      |
| ---------- | ------- | --------- | -------------------------- |
| video_id   | integer | No        | Filter results by video ID |
| profile    | integer | No        | Profile to use for search  |


Notes:
* The profile ID is optional, will fall back to checking the local session if it is not present
* Does not check if the profile ID exists
    * If this is not a real ID, then an empty list of videos is returned


**returns**

200 OK


When checking for all videos:

```json
{
    "data": [
        {
            "current_time": 8,
            "profile_id": 2,
            "updated_at": "2026-01-17 07:14:08",
            "video_id": 2834
        },
        {
            "current_time": 900,
            "profile_id": 2,
            "updated_at": "2026-01-18 01:27:07",
            "video_id": 3011
        }
    ],
    "message": "Retrieved in-progress videos successfully",
    "success": true
}
```


When checking a specific video:

```json
{
    "data": [
        {
            "current_time": 900,
            "profile_id": 2,
            "updated_at": "2026-01-18 01:27:07",
            "video_id": 3011
        }
    ],
    "message": "Retrieved in-progress videos successfully",
    "success": true
}
```


If the video is not in progress:

```json
{
    "message": "Retrieved in-progress videos successfully",
    "success": true
}
```



#### /api/profile/in_progress (POST)

**Method**:
POST


**Description**:

Add a video that's in progress to the database.

Uses the active profile.



**Payload**:

| Field        | Type    | Mandatory | Notes                              |
| ------------ | ------- | --------- | ---------------------------------- |
| video_id     | Integer | Yes       | ID of the video that's in progress |
| current_time | integer | Yes       | Video's current time (in seconds)  |



```json
{
    "video_id": 1,
    "current_time": 123
}
```


**returns**

200 OK

```json
{

}
```



#### /api/profile/in_progress (UPDATE)

**Method**:
UPDATE


**Description**:

Updates the time index of a video that's already marked as being in progress.

Uses the active profile.



**Payload**:

| Field        | Type    | Mandatory | Notes                              |
| ------------ | ------- | --------- | ---------------------------------- |
| video_id     | Integer | Yes       | ID of the video that's in progress |
| current_time | integer | Yes       | Video's current time (in seconds)  |



```json
{
    "video_id": 1,
    "current_time": 123
}
```


**returns**

200 OK

```json
{

}
```



#### /api/profile/in_progress (DELETE)

**Method**:
DELETE


**Description**:

Removes an in-progress video from the database.

Uses the active user.



**Parameters**

| Parameter  | Type    | Mandatory | Notes                  |
| ---------- | ------- | --------- | ---------------------- |
| video_id   | integer | Yes       | The video ID to remove |



**returns**

200 OK

```json
{

}
```

</br></br>




---
