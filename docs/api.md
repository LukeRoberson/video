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


</br></br>
