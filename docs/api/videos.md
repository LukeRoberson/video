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

## /api/videos/{{video_id}}

**Description**

Get a video by its ID, and return all its details.
</br></br>


**Method**

GET
</br></br>


**Parameters**

TBA
</br></br>


**Body**

TBA
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

TBA
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
|             |         |                 |
</br></br>


```json
```
</br></br>




----
## /api/videos/get_bulk

**Description**

Get details for multiple videos at once.
</br></br>


**Method**

POST
</br></br>


**Parameters**

TBA
</br></br>


**Body**

TBA
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

TBA
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
|             |         |                 |
</br></br>


```json
```
</br></br>




----
## /api/videos/filter

**Description**

Get a filtered list of videos, based on query parameters.
</br></br>


**Method**

GET
</br></br>


**Parameters**

TBA
</br></br>


**Body**

TBA
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

TBA
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
|             |         |                 |
</br></br>


```json
```
</br></br>





----
## /api/video/metadata

**Description**

Get metadata for a video.

This includes tags, categories, etc.
</br></br>


**Method**

GET
</br></br>


**Parameters**

TBA
</br></br>


**Body**

TBA
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

TBA
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
|             |         |                 |
</br></br>


```json
```
</br></br>




----
## /api/video/metadata

**Description**

Add metadata to a video, or update existing metadata.
</br></br>


**Method**

POST
</br></br>


**Parameters**

TBA
</br></br>


**Body**

TBA
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

TBA
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
|             |         |                 |
</br></br>


```json
```
</br></br>




----
## /api/videos/csv

**Description**

Read a CSV file containing a list of videos and metadata.
</br></br>


**Method**

GET
</br></br>


**Parameters**

TBA
</br></br>


**Body**

TBA
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

TBA
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
|             |         |                 |
</br></br>


```json
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

TBA
</br></br>


**Body**

TBA
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

TBA
</br></br>


| Field       | Type    | Description     |
| ----------- | ------- | --------------- |
|             |         |                 |
</br></br>


```json
```
</br></br>
