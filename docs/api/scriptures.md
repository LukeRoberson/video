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
| /                                   | Add text to a scripture                      |
| /video/{{video_id}}                 | Get scriptures for a video                   |
</br></br>



----
# Endpoints

## /api/scriptures

**Description**

Get a list of all scriptures.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>




----
## /api/scriptures/video/{{video_id}}

**Description**

Get all scriptures associated with a specific video.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/scriptures

**Description**

Add text to a scripture.

The scripture must already exist in the database. This endpoint adds or updates the text in the scripture only.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>
