# Overview

API endpoints that relate to past or modern locations.
</br></br>


**Implementation**

Implemented in `api_location.py`.
</br></br>


**Base URL**

/api/locations
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /                                   | Get all locations                            |
| /{{location_id}}                    | Get a location                               |
| /video/{{video_id}}                 | Get locations by video                       |
</br></br>




# Endpoints

## /api/locations

**Description**

Get a list of all locations.

Response entries are sorted alphabetically by location name.
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


** Response Body**

Returns a list of location entries.
</br></br>


| Field       | Type    | Description            |
| ----------- | ------- | ---------------------- |
| id          | integer | The ID of the location |
| name        | string  | The location name      |
</br></br>


```json
[
    {
        "id": 260,
        "name": "Addis Ababa"
    }
]
```
</br></br>




----
## /api/locations/{{location_id}}

**Description**

Get a single location by its ID.
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

`404 NOT FOUND` if the location does not exist
</br></br>


**Response Body**

A single location entry
</br></br>


| Field       | Type    | Description            |
| ----------- | ------- | ---------------------- |
| id          | integer | The ID of the location |
| name        | string  | The location name      |

</br></br>


```json
{
    "id": 1,
    "name": "Samaria"
}
```
</br></br>


If the location does not exist:

```json
{
    "error": "Location with ID 9999 not found",
    "success": false
}
```




----
## /api/locations/video/{{video_id}}

**Description**

Get locations associated with a particular video.
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

A list of location entries.

An empty list if there are no locations for this video.
</br></br>


| Field       | Type    | Description            |
| ----------- | ------- | ---------------------- |
| id          | integer | The ID of the location |
| name        | string  | The location name      |

</br></br>


```json
[
    {
        "id": 13,
        "name": "Philippines"
    }
]
```
</br></br>


If the video does not exist:

```json
{
    "error": "Video with ID 6 not found",
    "success": false
}
```

