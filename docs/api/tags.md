# Overview

API endpoints for tag management.
</br></br>


**Implementation**

`api_tag.py`.
</br></br>


**Base URL**

/api/tags
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /                                   | Get all tags                                 |
| /{{tag_id}}                         | Get a tag                                    |
| /video/{{video_id}}                 | Get tags on a video                          |
</br></br>



----
# Endpoints

## /api/tags

**Description**

Get a list of all tags.

Tags are sorted alphabetically by their name.
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

Returns 'data', 'message', and 'success' fields.

The 'data' field is a list of tag entries. Each entry describes the tag.
</br></br>


| Field       | Type    | Description                              |
| ----------- | ------- | ---------------------------------------- |
| id          | integer | The tag's ID                             |
| name        | string  | The tag's name                           |
| video_count | integer | The number of videos its associated with |
</br></br>


```json
{
    "data": [
        {
            "id": 933,
            "name": "1914",
            "video_count": 8
        }
    ],
    "message": "Tags retrieved successfully",
    "success": true
}
```
</br></br>




----
## /api/tags/{{tag_id}}

**Description**

Get a specific tag by its ID.
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

`404 NOT FOUND` if the tag does not exist.
</br></br>


**Response Body**

Returns 'data', 'message', and 'success' fields.

The 'data' field describes a single tag.
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
| id          | integer | The tag's ID    |
| name        | string  | The tag's name  |
</br></br>


```json
{
    "data": {
        "id": 1,
        "name": "av"
    },
    "message": "Tag retrieved successfully",
    "success": true
}
```
</br></br>


If there's an error:

```json
{
    "error": "Tag with ID 3 not found",
    "success": false
}
```
</br></br>



----
## /api/tags/video/{{video_id}}

**Description**

Get all tags associated with a specific video.
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

`404 NOT FOUND` if the video does not exist
</br></br>


**Response Body**

Returns 'data', 'message', and 'success' fields.

The 'data' field is a list of entries that describe tags.
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
| id          | integer | The tag's ID    |
| name        | string  | The tag's name  |
</br></br>


```json
{
    "data": [
        {
            "id": 1,
            "name": "av"
        }
    ],
    "message": "Tags retrieved successfully",
    "success": true
}
```
</br></br>


When the video is not found:

```json
{
    "error": "Video with ID 6 not found",
    "success": false
}
```