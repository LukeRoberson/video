# Overview

API endpoints that relate to videos.
</br></br>


**Implementation**

`api_video.py`.
</br></br>


**Base URL**

TBA
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /{{video_id}}                       | Get details for a video                      |
| /get_bulk                           | Get details for multiple videos              |
| /filter                             | Get a filtered list of videos                |
| /metadata                           | Get metadata for a video                     |
| /metadata                           | Add or update metadata on a video            |
| /csv                                | Read a CSV file of videos                    |
| /add                                | Add a new video to the database              |
</br></br>



----
# Endpoints

## /api/videos/get_bulk

**Description**

Get details for multiple videos at once.

This is more efficient than getting a single video at a time
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

| Field       | Type    | Description                                   |
| ----------- | ------- | --------------------------------------------- |
| video_ids   | list    | A list of video ID's to retrieve, as integers |
</br></br>


```json
{
    "video_ids": [1, 2, 3]
}
```
</br></br>


**Response Code**

`200 OK` on success

`400 BAD REQUEST` if video IDs are missing, or are not integers.

`415 UNSUPPORTED MEDIA TYPE` If a body is not present.
</br></br>


**Response Body**

'data', 'message', and 'success' fields.

The 'data' field contains a list of entries, where each entry represents a video.
</br></br>


| Field       | Type    | Description                                       |
| ----------- | ------- | ------------------------------------------------- |
| id          | integer | The video's ID                                    |
| name        | string  | The video's name                                  |
| description | string  | The video's description                           |
| duration    | integer | The duration of the video in seconds              |
| date_added  | string  | The date the video was added (YYY-MM-DD HH:MM:SS) |
| thumbnail   | string  | URL of the video's thumbnail                      |
| url         | string  | URL to the original video on jw.org               |
| url_1080    | string  | URL to the video (1080p)                          |
| url_720     | string  | URL to the video (720p)                           |
| url_480     | string  | URL to the video (480p)                           |
| url_360     | string  | URL to the video (360p)                           |
| url_240     | string  | URL to the video (240p)                           |
</br></br>


```json
{
    "data": [
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
        }
    ],
    "message": "Videos retrieved successfully for IDs: [1, 2, 3]",
    "success": true
}
```
</br></br>


If the video IDs are not integers as expected:

```json
{
    "error": "'video_ids' must be a list of integers",
    "success": false
}
```
</br></br>




----
## /api/videos/filter

**Description**

Get a filtered list of videos, based on query parameters such as tag.

This can be used to return the 'x' number of latest videos.
</br></br>


**Method**

GET
</br></br>


**Parameters**

| Field  | Type    | Description                           |
| ------ | ------- | ------------------------------------- |
| cat    | integer | The ID of the category to filter by   |
| tag    | integer | The ID of the tag to filter by        |
| loc    | integer | The ID of the location to filter by   |
| speak  | integer | The ID of the speaker to filter by    |
| char   | integer | The ID of the character to filter by  |
| scrip  | integer | The ID of the scripture to filter by  |
| latest | integer | The number of latest videos to return |
</br></br>


> [!NOTE]
> All the parameters are optional, but at least one must be provided.
</br></br>


> [!NOTE]
> Multiple of each parameter may be provided to create a list of that type.
</br></br>



**Body**

None
</br></br>


**Response Code**

`200 OK` on success

`400 BAD REQUEST` if there isn't at least one parameter included
</br></br>


**Response Body**

'data', 'message', and 'success' fields.

The 'data' field contains a list of video entries that match the query.
</br></br>


| Field       | Type    | Description                                       |
| ----------- | ------- | ------------------------------------------------- |
| id          | integer | The video's ID                                    |
| name        | string  | The video's name                                  |
| description | string  | The video's description                           |
| duration    | integer | The duration of the video in seconds              |
| date_added  | string  | The date the video was added (YYY-MM-DD HH:MM:SS) |
| thumbnail   | string  | URL of the video's thumbnail                      |
| url         | string  | URL to the original video on jw.org               |
| url_1080    | string  | URL to the video (1080p)                          |
| url_720     | string  | URL to the video (720p)                           |
| url_480     | string  | URL to the video (480p)                           |
| url_360     | string  | URL to the video (360p)                           |
| url_240     | string  | URL to the video (240p)                           |
</br></br>


```json
{
    "data": [
        {
            "date_added": "2026-03-11",
            "description": "",
            "duration": 60,
            "id": 3015,
            "name": "Test Video",
            "thumbnail": "http://localhost/test.png",
            "url": "http://localhost/test",
            "url_1080": "http://localhost/test1080.mp4",
            "url_240": "http://localhost/test240.mp4",
            "url_360": "http://localhost/test360.mp4",
            "url_480": "http://localhost/test480.mp4",
            "url_720": "http://localhost/test720.mp4"
        }
    ],
    "message": "Videos retrieved successfully",
    "success": true
}
```
</br></br>


If no parameters are included:

```json
{
    "error": "At least one filter query parameter is required",
    "success": false
}
```
</br></br>


If parameters are invalid (not integers):

```json
{
    "error": "Invalid value for category_id: \"one\". Must be an integer.",
    "success": false
}
```
</br></br>




----
## /api/videos/metadata

**Description**

Resolve metadata names to IDs. For example, a location name to a location ID.

Other endpoints also do this, but this one allows multiple resolutions to happen in a single request.

Resolvable information is:
* Video
* Tag
* Location
* Speaker
* Character

Not all fields need to be included in the request.
</br></br>


**Method**

GET
</br></br>


**Parameters**

| Field          | Type    | Description             |
| -------------- | ------- | ----------------------- |
| video_name     | string  | The name of a video     |
| tag_name       | string  | The name of a tag       |
| location_name  | string  | The name of a location  |
| speaker_name   | string  | the name of a speaker   |
| character_name | string  | the name of a character |
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

'data', 'message', and 'success' fields.

The 'data' field contains the resolved IDs.

Each field will be 'null' if resolution was not requested for that field. If no fields were included in the request, each entry in the response will be 'null'.
</br></br>


| Field        | Type    | Description               |
| ------------ | ------- | ------------------------- |
| character_id | integer | The resolved character ID |
| location_id  | integer | The resolved location ID  |
| speaker_id   | integer | The resolved speaker ID   |
| tag_id       | integer | The resolved tag ID       |
| video_id     | integer | The resolved video ID     |
</br></br>


```json
{
    "data": {
        "character_id": 31,
        "location_id": 15,
        "speaker_id": 1,
        "tag_id": 1,
        "video_id": 1254
    },
    "message": "Metadata resolved successfully",
    "success": true
}
```
</br></br>


When no entries are included in the reqest:

```json
{
    "data": {
        "character_id": null,
        "location_id": null,
        "speaker_id": null,
        "tag_id": null,
        "video_id": null
    },
    "success": true
}
```
</br></br>




----
## /api/videos/metadata

**Description**

Add metadata to a video, or update existing metadata.
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

Includes a JSON body with information to update.
</br></br>


| Field          | Type    | Description                                                               |
| -------------- | ------- | ------------------------------------------------------------------------- |
| video_name     | string  | The name of the video to update                                           |
| description    | string  | The description of the video                                              |
| url            | string  | The URL to the video's location on jw.org                                 |
| tag_name       | string  | A comma separated list of tag names                                       |
| location_name  | string  | A comma separated list of location names                                  |
| speaker_name   | string  | A comma separated list of speaker names                                   |
| character_name | string  | A comma separated list of character names                                 |
| scripture_name | string  | A comma separated list of scriptures, in standard format (eg, 'John 1:1') |
| category_name  | string  | A comma separated list of category names                                  |
| date_added     | string  | A datetime string (YYYY-MM-DD HH:MM:SS)                                   |
</br></br>


```json
{
    "video_name": "David Schafer: Why We Have Faith in . . . God’s Existence",
    "description": "Video description",
    "url": "URL",
    "tag_name": "tag-1, tag-2",
    "location_name": "Israel",
    "speaker_name": "David Schafer",
    "character_name": "Abraham",
    "scripture_name": "John 1:1",
    "category_name": "Programs and Events",
    "date_added": "2000-01-01T00:00:00.000Z"
}
```
</br></br>


**Response Code**

`200 OK` on success

`400 BAD REQUEST` if fields in the request's body are invalid.

`404 NOT FOUND` if the video was not found
</br></br>


**Response Body**

Sends a 'success' field, with true or false.
</br></br>


```json
{
    "success": true
}
```
</br></br>


If there is a problem, such as the video not existing:

```json
{
    "error": "Video 'Fake Video' not found",
    "success": false
}
```
</br></br>


Or if the date in formatted badly:

```json
{
    "error": "Invalid date format for 'date_added'. Expect ISO format.",
    "success": false
}
```
</br></br>


----
## /api/videos/csv

**Description**

Read a CSV file containing a list of videos that need to be added to the database.

NOTE: This endpoint just reads this information, it does not modify the database.

The CSV file is assumed to be named `missing_videos.csv`, and is stored in `../scripts/csv`.
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

`404 NOT FOUND` if the CSV file is not present

`500 INTERNAL SERVER ERROR` if the CSV file could not be loaded
</br></br>


**Response Body**

Returns videos as numberical indexes (starting at 0).

Video information contains all the usual metadata.
</br></br>


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
</br></br>




----
## /api/videos/add

**Description**

Add a new video to the database.
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

Information about a single video to add to the database.
</br></br>


| Field         | Type    | Description                            |
| ------------- | ------- | -------------------------------------- |
| video_name    | string  | The name of the video                  |
| video_url     | string  | The video's URL on jw.org              |
| main_cat_name | string  | The main category the video belongs to |
| sub_cat_name  | string  | The subcategory the video belongs to   |
| url_1080      | string  | Video URL                              |
| url_720       | string  | Video URL                              |
| url_480       | string  | Video URL                              |
| url_360       | string  | Video URL                              |
| url_240       | string  | Video URL                              |
| thumbnail     | string  | URL to the video's thumbnail           |
| duration      | string  | Duration of the video, in HH:MM:SS     |
</br></br>


```json
{
    "video_name": "<video name>",
    "video_url": "<video URL>",
    "main_cat_name": "<main category name>",
    "sub_cat_name": "<subcategory name>",
    "url_1080": "<1080p video URL>",
    "url_720": "<720p video URL>",
    "url_480": "<480p video URL>",
    "url_360": "<360p video URL>",
    "url_240": "<240p video URL>",
    "thumbnail": "<thumbnail image URL>",
    "duration": "<video duration in HH:MM:SS>",
}
```
</br></br>


**Response Code**

`200 OK` on success

`400 BAD REQUEST` If the video name is not present, or if the duration is not formatted correctly.

`404 NOT FOUND` if the categories don't exist in the database

`500 INTERNAL SERVER ERROR` if the video could not be added to the database
</br></br>


**Response Body**

A simple success or failure message.
</br></br>


Success:

```json
{
    "message": "video added",
    "success": true
}
```
</br></br>


Failure:

```json
{
    "error": "Missing 'video_name' in request data",
    "success": false
}
```
</br></br>


```json
{
    "error": "Main category 'None' not found",
    "success": false
}
```
</br></br>


```json
{
    "error": "Failed to add video 'Test Video'",
    "success": false
}
```
</br></br>
