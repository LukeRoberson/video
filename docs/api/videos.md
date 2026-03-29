# Overview

API endpoints that relate to videos.
</br></br>


**Implementation**

`api_video.py`.
</br></br>


**Base URL**

/api/videos
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


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>




----
## /api/videos/filter

**Description**

Get a filtered list of videos, based on query parameters such as tag.

This can be used to return the 'x' number of latest videos.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
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


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
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
