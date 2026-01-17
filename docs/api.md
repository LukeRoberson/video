# API



---
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


#### /api/scripture

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



#### /api/profile/mark_watched

**Method**:
POST


**Description**:
Marks a video as watched for a user


**Payload**:

| Field      | Type    | Mandatory | Notes                              |
| ---------- | ------- | --------- | ---------------------------------- |
| video_id   | integer | Yes       | ID of the video to mark as watched |


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



**returns**

200 OK

```json
{

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


#### /api/categories/{category_id}/{subcategory_id}


**Method**:
GET


**Description**:
Get a list of videos in a particular category/subcategory combination.


Returns:

200 OK


Notes:
* Returns a list of entries


```json
[
    {
        "date_added": "2025-11-04 00:00:00",
        "description": "A talk about taking in spiritual food, by Geoffrey Jackson.\nHighlights from the dedication of the new Britain branch.\nThe experience of Nigel Baker.\nMorning worship with John Ekrann.\nDig for Treasures - Obadiah.\nThe experience of Domenic Alessia.\nMusic Video - Hearer of Prayer.\nVideo Postcard from Brussels.",
        "duration": "57:56",
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



