# Overview

API endpoints that relate to video speakers and interviewees.
</br></br>


**Implementation**

`api_speaker.py`.
</br></br>


**Base URL**

/api/speakers
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /                                   | Get all speakers                             |
| /{{speaker_id}}                     | Get one speaker                              |
| /video/{{video_id}}                 | Get speakers on a video                      |
</br></br>



----
# Endpoints

## /api/speakers

**Description**

Get a list of all speakers, or just one specific speaker.

List is sorted alphabetically by speaker name.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/speakers/{{speaker_id}}

**Description**

Get a specific speaker.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/speakers/video/{{video_id}}

**Description**

Get all speakers associated with a specific video.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>
