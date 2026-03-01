# Overview

API endpoints that relate to scriptures mentions in videos.
</br></br>


**Implementation**

`api_scripture.py`.
</br></br>


**Base URL**

/api/scriptures
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /                                   | Get all scriptures                           |
| /{{scripture_id}}                   | Get a scripture                              |
| /video/{{video_id}}                 | Get scriptures for a video                   |
| /                                   | Add text to a scripture                      |
</br></br>



----
# Endpoints

## /api/scriptures

**Description**

Get a list of all scriptures.
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

A list of scripture entries.
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
| id          | integer | Scripture's ID  |
| book        | string  | Book name       |
| chapter     | integer | Chapter number  |
| verse       | integer | Verse number    |
| verse_text  | string  | Verse text      |
</br></br>


```json
[
    {
        "book": "Matthew",
        "chapter": 19,
        "id": 2,
        "verse": 13,
        "verse_text": "Then young children were brought to him for him to place his hands on them and offer prayer, but the disciples reprimanded them."
    }
]
```
</br></br>




----
## /api/scriptures/{{scripture_id}}

**Description**

Get a single scripture by its ID
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

`404 NOUT FOUND` if the scripture does not exist.
</br></br>


**Response Body**

Returns the details for an individual scripture
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
| id          | integer | Scripture's ID  |
| book        | string  | Book name       |
| chapter     | integer | Chapter number  |
| verse       | integer | Verse number    |
| verse_text  | string  | Verse text      |
</br></br>


```json
{
    "book": "Matthew",
    "chapter": 19,
    "id": 2,
    "verse": 13,
    "verse_text": "Then young children were brought to him for him to place his hands on them and offer prayer, but the disciples reprimanded them."
}
```
</br></br>



If the scripture is not found:

```json
{
    "error": "Scripture with ID 1 not found",
    "success": false
}
```
</br></br>






----
## /api/scriptures/video/{{video_id}}

**Description**

Get all scriptures associated with a specific video.
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

`404 NOT FOUND` if the video is not found
</br></br>


**Response Body**

A list of entries, where each entry is a scripture.
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
| id          | integer | Scripture's ID  |
| book        | string  | Book name       |
| chapter     | integer | Chapter number  |
| verse       | integer | Verse number    |
| verse_text  | string  | Verse text      |
</br></br>


```json
[
    {
        "book": "Matthew",
        "chapter": 19,
        "id": 2,
        "verse": 13,
        "verse_text": "Then young children were brought to him for him to place his hands on them and offer prayer, but the disciples reprimanded them."
    }
]
```
</br></br>


If the video is not found:

```json
{
    "error": "Video with ID 6 not found",
    "success": false
}
```





----
## /api/scripture

**Description**

Add text to a scripture.

The scripture must already exist in the database. This endpoint adds or updates the text in the scripture only.
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

JSON containing the verse to be updated, and the text belonging to the verse.
</br></br>


| Field       | Type    | Description                                    |
| ----------- | ------- | ---------------------------------------------- |
| scr_name    | string  | The name of the scripture (format: `John 1:1`) |
| scr_text    | string  | The text to accompany the verse                |
</br></br>


```json
{
    "scr_name": "John 1:1",
    "scr_text": "In the beginning was the Word, and the Word was with God, and the Word was a god."
}
```
</br></br>


**Response Code**

`200 OK` on success

`415 UNSUPPORTED MEDIA TYPE` if the JSON body is not included

`400 BAD REQUEST` if the fields in the JSON body are incorrect

`500 INTERNAL SERVER ERROR` if the scripture does not yet exist in the database.
</br></br>


**Response Body**

A standard success or failure message.
</br></br>


```json
{
    "message": "Added scripture text for 'John 1:1'",
    "success": true
}
```
</br></br>


If the body is incorrectly formatted:

```json
{
    "error": "Missing 'scr_name' or 'scr_text' in request data",
    "success": false
}
```
</br></br>


If the scripture does not exist in the database:

```json
{
    "error": "Failed to add scripture text: John 999:88",
    "success": false
}
```
