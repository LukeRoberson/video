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

Get a list of all speakers.

List is sorted alphabetically by speaker name.
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

A list of speakers, with each entry describing the speaker.
</br></br>


| Field       | Type    | Description                                |
| ----------- | ------- | ------------------------------------------ |
| id          | integer | The speaker's ID                           |
| name        | string  | The speaker's name                         |
| profile_pic | string  | The filename for the speaker's profile pic |
| video_count | integer | The number of videos they appear in        |
</br></br>


```json
[
    {
        "id": 321,
        "name": "Adolf Denk",
        "profile_pic": "321-Adolph_Denk.png",
        "video_count": 2
    }
]
```
</br></br>




----
## /api/speakers/{{speaker_id}}

**Description**

Get a specific speaker.
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

`404 NOT FOUND` If the speaker does not exist
</br></br>


**Response Body**

Returns one specific speaker's details.
</br></br>


| Field       | Type    | Description                            |
| ----------- | ------- | -------------------------------------- |
| id          | integer | The speaker's ID                       |
| name        | string  | The speaker's name                     |
| profile_pic | string  | Filename for the speaker's profile pic |
</br></br>


```json
{
    "id": 321,
    "name": "Adolf Denk",
    "profile_pic": "321-Adolph_Denk.png"
}
```
</br></br>


If there is an error:

```json
{
    "error": "Speaker with ID 3 not found",
    "success": false
}
```
</br></br>



----
## /api/speakers/video/{{video_id}}

**Description**

Get all speakers associated with a specific video.
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

Returns a list, where each entry contains a speaker's details
</br></br>


| Field       | Type    | Description                                |
| ----------- | ------- | ------------------------------------------ |
| id          | integer | The speaker's ID                           |
| name        | string  | The speaker's name                         |
| profile_pic | string  | The filename for the speaker's profile pic |
</br></br>


```json
[
    {
        "id": 1,
        "name": "Stephen Lett",
        "profile_pic": "1-Stephen_Lett.png"
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
</br></br>
