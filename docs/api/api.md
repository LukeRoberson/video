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


#### /api/video/metadata

**Method**:
POST


**Description**:
Add metadata to videos, including:
* Description
* URL
* Tag
* Location
* Speaker
* Character
* Scripture
* Category
* Date

The video must already exist in the database before metadata can be added.

If fields already contain metadata, the behavour will vary:
* Description, URL, and Date will be overwritten by the new value
* Other fields are lists, and will have new metadata appended


**Payload**:

| Field          | Type   | Mandatory | Notes                                                    |
| -------------- | ------ | --------- | -------------------------------------------------------- |
| video_name     | string | Yes       | Used to match a video in the database                    |
| description    | string | No        | Video description                                        |
| url            | string | No        | URL to the video location on the jw.org website          |
| tag_name       | string | No        | List of tags, comma separated                            |
| location_name  | string | No        | List of locations, comma separated                       |
| speaker_name   | string | No        | List of speakers, comma separated                        |
| character_name | string | No        | List of characters, comma separated                      |
| scripture_name | string | No        | List of scriptures, comma separated                      |
| category_name  | string | No        | List of categories, comma separated                      |
| date_added     | string | No        | A date, formatted as "2000-01-01T00:00:00.000Z"          |


Notes:
* Video name cannot be set or changed here; It is for identifying the video to update
* At least one other field must be set
* Any scriptures must be formatted in standard notation, such as "John 1:1". Other formats will be rejected.
* Categories must already exist in the database
* List fields, such as tags, do not need to exist in the database; They will automatically be added


```json
{
    "video_name": "Video name",
    "description": "Video description",
    "url": "URL",
    "tag_name": "list of tags",
    "location_name": "list of locations",
    "speaker_name": "list of speakers",
    "character_name": "list of characters",
    "scripture_name": "John 1:1",
    "category_name": "Programs and Events",
    "date_added": "date"
}
```


</br></br>


#### /api/videos/csv

**Method**:
GET


**Description**:

Load videos from a CSV file in preparation to enter them into the database.

CSV is not selectable, it is set in code using a constant.


**returns**

200 OK

Returns the contents of the CSV file.

Each entry includes an index, starting at zero.


```json
{
    "0": {
        "video_name": "JW Broadcasting—January 2026: Annual Meeting 2025, Part 1",
        "video_url": "https://www.jw.org/en/library/videos/#en/mediaitems/StudioMonthlyPrograms/pub-jwb-134_1_VIDEO",
        "main_cat_name": "JW Broadcasting",
        "sub_cat_name": "Monthly Programs",
        "url_1080": null,
        "url_720": "https://akdd1.jw-cdn.org/sg2/p/360c2c/1/o/jwb-134_E_01_r720P.mp4",
        "url_480": "https://akdd1.jw-cdn.org/sg2/p/99bdbd/1/o/jwb-134_E_01_r480P.mp4",
        "url_360": "https://akdd1.jw-cdn.org/sg2/p/fcc2dd/1/o/jwb-134_E_01_r360P.mp4",
        "url_240": "https://akamd1.jw-cdn.org/sg2/p/485b9ed/1/o/jwb-134_E_01_r240P.mp4",
        "thumbnail": "https://cms-imgp.jw-cdn.org/img/p/jwb-134/univ/art/jwb-134_univ_wss_01_lg.jpg",
        "duration": "1:43:33"
    }
}
```


#### /api/videos/add

**Method**:
POST


**Description**:

Add videos to the database. Used on the admin page.



**Payload**:

| Field          | Type   | Mandatory | Notes                                                    |
| -------------- | ------ | --------- | -------------------------------------------------------- |
| video_name     | String | Yes       | The name of the video to add                             |
| video_url      | String | Yes       | The URL on jw.org                                        |
| main_cat_name  | String | Yes       | The video's main category                                |
| sub_cat_name   | String | Yes       | The video's subcategory                                  |
| url_1080       | String | Yes       | URL to 1080p video                                       |
| url_720        | String | Yes       | URL to 720p video                                        |
| url_480        | String | Yes       | URL to 480p video                                        |
| url_360        | String | Yes       | URL to 360p video                                        |
| url_240        | String | Yes       | URL to 240p video                                        |
| thumbnail      | String | Yes       | URL to the thumbnail's image                             |
| duration       | String | Yes       | Duration in the format HH:MM:SS                          |




```json
{
    "video_name": "Jehovah Is a Real Person",
    "video_url": "https://www.jw.org/en/library/videos/#en/mediaitems/BJF/pub-pk_59_VIDEO",
    "main_cat_name": "Children",
    "sub_cat_name": "Video Lessons",
    "url_1080": null,
    "url_720": "https://akdd1.jw-cdn.org/sg2/p/bf8814/1/o/pk_E_059_r720P.mp4",
    "url_480": "https://akamd1.jw-cdn.org/sg2/p/0fc60b/1/o/pk_E_059_r480P.mp4",
    "url_360": "https://akamd1.jw-cdn.org/sg2/p/1bfe852/1/o/pk_E_059_r360P.mp4",
    "url_240": "https://akamd1.jw-cdn.org/sg2/p/513517a/1/o/pk_E_059_r240P.mp4",
    "thumbnail": "https://cms-imgp.jw-cdn.org/img/p/501600168/univ/art/501600168_univ_wss_lg.jpg",
    "duration": "10:35",
    "date_added": "2026-01-17 19:40:48"
}
```


**returns**

200 OK


```json
{
}
```




**Method**:
POST


**Description**:
Add scripture text to a scripture.

The scripture must already exist in the database before text can be added.

If a scripture already has text, the new text will overwrite the old.


**Payload**:

| Field    | Type   | Mandatory | Notes                                                    |
| -------- | ------ | --------- | -------------------------------------------------------- |
| scr_name | string | Yes       | Name of the scripture in standard format; Eg, 'John 1:1' |
| scr_text | string | Yes       | Scripture text                                           |


```json
{
    "scr_name": "Scripture",
    "scr_text": "Text"
}
```



</br></br>



---
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
### Videos


#### /api/videos/{video_id}


**Method**:
GET


**Description**:
Get a video by it's ID, and return details of the video.


**Returns**:

200 OK


```json
{
    "date_added": "2025-11-04 00:00:00",
    "description": "A description",
    "duration": 3476,
    "id": 3011,
    "name": "JW Broadcasting—November 2025",
    "thumbnail": "https://cms-imgp.jw-cdn.org/img/p/jwb-132/univ/art/jwb-132_univ_wss_01_lg.jpg",
    "url": "https://www.jw.org/en/library/videos/#en/mediaitems/LatestVideos/pub-jwb-132_1_VIDEO",
    "url_1080": null,
    "url_240": "https://akamd1.jw-cdn.org/sg2/p/d7ad66/1/o/jwb-132_E_01_r240P.mp4",
    "url_360": "https://akdd1.jw-cdn.org/sg2/p/30a4cf1/1/o/jwb-132_E_01_r360P.mp4",
    "url_480": "https://akdd1.jw-cdn.org/sg2/p/d320c0/1/o/jwb-132_E_01_r480P.mp4",
    "url_720": "https://akdd1.jw-cdn.org/sg2/p/781121/1/o/jwb-132_E_01_r720P.mp4"
}
```


#### /api/videos/get_bulk


**Method**:
POST


**Description**:
Get the details for a list of videos, all in one request.


**Payload**:

| Field      | Type    | Mandatory | Notes                         |
| ---------- | ------- | --------- | ----------------------------- |
| video_ids  | list    | Yes       | A list of video ID's to check |


```json
{
    "video_ids": [123, 124, 125]
}
```


**Returns**:

200 OK


```json
[
    {
        "date_added": "2025-11-04 00:00:00",
        "description": "A description",
        "duration": 3476,
        "id": 3011,
        "name": "JW Broadcasting—November 2025",
        "thumbnail": "https://cms-imgp.jw-cdn.org/img/p/jwb-132/univ/art/jwb-132_univ_wss_01_lg.jpg",
        "url": "https://www.jw.org/en/library/videos/#en/mediaitems/LatestVideos/pub-jwb-132_1_VIDEO",
        "url_1080": null,
        "url_240": "https://akamd1.jw-cdn.org/sg2/p/d7ad66/1/o/jwb-132_E_01_r240P.mp4",
        "url_360": "https://akdd1.jw-cdn.org/sg2/p/30a4cf1/1/o/jwb-132_E_01_r360P.mp4",
        "url_480": "https://akdd1.jw-cdn.org/sg2/p/d320c0/1/o/jwb-132_E_01_r480P.mp4",
        "url_720": "https://akdd1.jw-cdn.org/sg2/p/781121/1/o/jwb-132_E_01_r720P.mp4"
    }
]
```


#### /api/videos/filter


**Method**:
GET


**Description**:
Get a list of videos, but filter by given parameters.

Returns details of each video.


**Parameters**

| Parameter  | Type    | Mandatory | Notes                              |
| ---------- | ------- | --------- | ---------------------------------- |
| cat        | integer | No        | Category ID                        |
| tag        | integer | No        | Tag ID                             |
| loc        | integer | No        | Location ID                        |
| speak      | integer | No        | Speaker ID                         |
| char       | integer | No        | Character ID                       |
| scrip      | integer | No        | Scripture ID                       |
| latest     | integer | No        | Number of latest entries to return |


**Returns**

200 OK


```json
[
    {
        "date_added": "2014-10-01 00:00:00",
        "description": "Behind the scenes look at the design and construction of the JW Broadcasting set.\nA race for everlasting life, where the runners are not in competition with each other.\nHow principles in the Bible can help face bullies.\nAn archived interview with Theodore Jaracz, as he talks about the challenges he faced as a young man.\nThe role the legal department plays in establishing the good news\nThe experience of Burt Mann, who became a witness in his 90s\nA music video: The Best Life Ever",
        "duration": 3305,
        "id": 1,
        "name": "JW Broadcasting—October 2014",
        "thumbnail": "https://assetsnffrgf-a.akamaihd.net/assets/m/jwb/univ/201410/art/jwb_univ_201410_lss_01_lg.jpg",
        "url": null,
        "url_1080": "",
        "url_240": "https://akdd1.jw-cdn.org/sg2/p/1cf913/1/o/jwb_E_201410_01_r240p.mp4",
        "url_360": "https://akdd1.jw-cdn.org/sg2/p/ed9f24/1/o/jwb_E_201410_01_r360P.mp4",
        "url_480": "https://akdd1.jw-cdn.org/sg2/p/1ff4d1a/1/o/jwb_E_201410_01_r480P.mp4",
        "url_720": "https://akdd1.jw-cdn.org/sg2/p/8fa715/1/o/jwb_E_201410_01_r720p.mp4"
    },
    {
        "date_added": "2014-11-01 00:00:00",
        "description": "A tour of the new SKE school in Florida\nA look at why publications are translated into so many languages\nTake a tour of the correspondence department\nHear from Lloyd Barry, as he talks about his early days as a missionary in Japan\nThe Gournon's tell about their 40+ years of service\nMorning worship; Curbing wrongful desire before it becomes a problem\nKeep improving your family worship\nMusic video - We won't forget you",
        "duration": 3553,
        "id": 2,
        "name": "JW Broadcasting​—November 2014",
        "thumbnail": "https://assetsnffrgf-a.akamaihd.net/assets/m/jwb/univ/201411/art/jwb_univ_201411_lss_01_lg.jpg",
        "url": null,
        "url_1080": "",
        "url_240": "https://akamd1.jw-cdn.org/sg2/p/c907e6/1/o/jwb_E_201411_01_r240P.mp4",
        "url_360": "https://akdd1.jw-cdn.org/sg2/p/fcc6f84/1/o/jwb_E_201411_01_r360P.mp4",
        "url_480": "https://akdd1.jw-cdn.org/sg2/p/85baf5f/1/o/jwb_E_201411_01_r480P.mp4",
        "url_720": "https://akdd1.jw-cdn.org/sg2/p/722c72/1/o/jwb_E_201411_01_r720P.mp4"
    }
]
```

</br></br>



----


----
