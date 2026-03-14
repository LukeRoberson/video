# Overview

API endpoints that relate to Bible characters.
</br></br>


**Implementation**

`api_character.py`.
</br></br>


**Base URL**

/api/characters
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /                                   | Get a list of all characters                 |
| /{{character_id}}                   | Get a specific character                     |
| /video/{{video_id}}                 | Get characters in a video                    |
</br></br>



----
# Endpoints

## /api/characters

**Description**

Get a list of all Bible characters in the database.

The list is sorted alphabetically by name.
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

Contains 'data', 'message', and 'success' fields.

The 'data' field contains a list of all Bible characters, with each entry describing the character.
</br></br>


| Field       | Type    | Description                                             |
| ----------- | ------- | ------------------------------------------------------- |
| id          | integer | The character's ID                                      |
| name        | string  | The character's name                                    |
| description | string  | A multi-line description of the character               |
| date_range  | string  | An approximate date range when the character was active |
| profile_pic | string  | The filename of the characters avatar                   |
</br></br>


```json
{
    "data": [
        {
            "date_range": "1597-1474 B.C.E.",
            "description": "Aaron was the courageous spokesman for his brother, Moses, when they appeared before Pharaoh.\nJehovah later appointed Aaron to be Israel’s ﬁrst high priest.\nAlthough he served God loyally for many years, Aaron did not honor God at Meribah.\nTherefore, he was not allowed to enter the Promised Land.",
            "id": 230,
            "name": "Aaron",
            "profile_pic": "230-Aaron.png"
        }
    ],
    "message": "Retrieved 205 characters",
    "success": true
} 
```
</br></br>




----
## /api/characters/{{character_id}}

**Description**

Get a specific character by their ID.
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

`404 NOT FOUND` if the character does not exist.
</br></br>


**Response Body**

Returns 'data', 'message', and 'success' fields.

The 'data' field contains a single entry, containing details for the character
</br></br>


| Field       | Type    | Description                                             |
| ----------- | ------- | ------------------------------------------------------- |
| id          | integer | The character's ID                                      |
| name        | string  | The character's name                                    |
| description | string  | A multi-line description of the character               |
| date_range  | string  | An approximate date range when the character was active |
| profile_pic | string  | The filename of the characters avatar                   |
</br></br>


```json
{
    "data": {
        "date_range": "About 1000 B.C.E.",
        "description": "Son of Jesse, and the second King of Israel.\nA skilled poet and musician, David wrote more than 73 of the psalms.\nHe humbly sought Jehovah’s direction in his life.\nJehovah called David “a man agreeable to my heart.”",
        "id": 1,
        "name": "David",
        "profile_pic": "1-David.png"
    },
    "message": "Retrieved character with ID 1",
    "success": true
}
```
</br></br>


If a character is not found, this JSON is returned:

```json
{
    "error": "Character with ID 5 not found",
    "success": false
}
```
</br></br>




----
## /api/characters/video/{{video_id}}

**Description**

Get the characters associated with a specific video.
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

`404 NOT FOUND` if the video does not exist.
</br></br>


**Response Body**

Returns 'data', 'message', and 'success' fields.

The 'data' field contains a list of entries. Each entry contains character details
</br></br>


| Field       | Type    | Description                                             |
| ----------- | ------- | ------------------------------------------------------- |
| id          | integer | The character's ID                                      |
| name        | string  | The character's name                                    |
| description | string  | A multi-line description of the character               |
| date_range  | string  | An approximate date range when the character was active |
| profile_pic | string  | The filename of the characters avatar                   |
</br></br>


```json
{
    "data": [
        {
            "date_range": "About 1000 B.C.E.",
            "description": "Son of Jesse, and the second King of Israel.\nA skilled poet and musician, David wrote more than 73 of the psalms.\nHe humbly sought Jehovah’s direction in his life.\nJehovah called David “a man agreeable to my heart.”",
            "id": 1,
            "name": "David",
            "profile_pic": "1-David.png"
        }
    ],
    "message": "Retrieved characters for video ID 1",
    "success": true
}
```
</br></br>


If the video is not found, this is returned:

```json
{
    "error": "Video with ID 6 not found",
    "success": false
}
```