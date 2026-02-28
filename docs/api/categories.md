# Overview

API endpoints that relate to video categories.
</br></br>


**Implementation**

`api_category.py`.

</br></br>


**Base URL**

TBA
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /{{category_name}}                  | Resolve a name to an ID                      |
| /{{category_id}}/{{subcategory_id}} | Get videos in a main/subcategory combination |
| /video/{{video_id}}                 | Get categories associated with a video       |
</br></br>


----
# Endpoints

## /api/category/{{category_name}}

**Description**

Resolve a category name to its ID.

Include the category name (string) in the URL.
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

`404 NOT FOUND` if the category is not found
</br></br>


**Response Body**

A single entry, representing the category.
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
| category_id | integer | The category ID |
</br></br>


```json
{
    "category_id": 1
}
```
</br></br>





----
## /api/categories/{{category_id}}/{{subcategory_id}}

**Description**

Fetch all videos that belong to BOTH the major category and subcategory.

Include the main category ID (integer) and the subcategory ID (integer) in the URL.
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

A list of entries, with each item in the list containing details about a video.
</br></br>


| Field       | Type    | Description                                       |
| ----------- | ------- | ------------------------------------------------- |
| id          | integer | The ID of the video                               |
| name        | string  | The name of the video                             |
| description | string  | A multi line description. Uses '\n' for new lines |
| duration    | integer | Duration of the video in seconds                  |
| date_added  | string  | Date the video was added (YYYY-MM-DD HH:MM:SS)    |
| thumbnail   | string  | URL to the video thumbnail                        |
| url         | string  | URL to the video on jw.org                        |
| url_1080    | string  | Video file URL                                    |
| url_720     | string  | Video file URL                                    |
| url_480     | string  | Video file URL                                    |
| url_360     | string  | Video file URL                                    |
| url_240     | string  | Video file URL                                    |
</br></br>


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
</br></br>





----
## /api/categories/video/{{video_id}}

**Description**

Get a list of categories that a video belongs to.

Include the video ID (integer) in the URL.
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

A list of categories that a video belongs to.
</br></br>


| Field       | Type    | Description          |
| ----------- | ------- | -------------------- |
| id          | integer | ID of the category   |
| name        | string  | Name of the category |
</br></br>


```json
[
    {
        "id": 1,
        "name": "Monthly Programs"
    },
    {
        "id": 1340,
        "name": "JW Broadcasting"
    }
]
```
</br></br>

