# Overview

API endpoints for finding video similarity.
</br></br>


**Implementation**

`api_similarity.py`.
</br></br>


**Base URL**

/api/similarity
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /{{video_id}}                       | Get similar videos for a given video         |
</br></br>



----
# Endpoints

## /api/similarity/{{video_id}}

**Description**

Get a top-10 list of similar videos, using a pre-calculated score.

This gets the top-10 for a single video.
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

Returns a list of similarity scores for a video.

Each entry contains the IDs for two videos, and a numerical score showing how similar they are
</br></br>


| Field       | Type    | Description                               |
| ----------- | ------- | ----------------------------------------- |
| video_1_id  | integer | The requested video ID                    |
| video_2_id  | float   | The video ID that it is being compared to |
| score       | float   | A score (between 0-1)                     |
</br></br>


```json
[
    {
        "score": 0.23379166666666665,
        "video_1_id": 1,
        "video_2_id": 16
    }
]
```
</br></br>


On error:

```json
{
    "error": "Video with ID 6 not found",
    "success": false
}
```
