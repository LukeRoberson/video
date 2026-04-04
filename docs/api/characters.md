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
| /video/{{video_id}}                 | Get characters in a video                    |
</br></br>



----
# Endpoints

## /api/characters

**Description**

Get a list of all Bible characters in the database, or get a specific character by their ID.

When getting the entire list, it will be sorted alphabetically by name.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/characters/video/{{video_id}}

**Description**

Get the characters associated with a specific video.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>
