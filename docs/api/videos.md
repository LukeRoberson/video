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


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>


----
## /api/videos/csv

**Description**

Read a CSV file containing a list of videos that need to be added to the database.

NOTE: This endpoint just reads this information, it does not modify the database.

The CSV file is assumed to be named `missing_videos.csv`, and is stored in `../scripts/csv`.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/videos/add

**Description**

Add a new video to the database.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>
