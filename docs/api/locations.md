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

Get a list of all locations, or one specific location when including the location ID.

When all locations are resturned, they are sorted alphabetically by location name.
</br></br>


**Method**

GET
</br></br>


**Parameters**

Optionally include a location ID to get one specific location.
</br></br>


| Field       | Type    | Mandatory | Description                 |
| ----------- | ------- | --------- | --------------------------- |
| loc_id      | integer | No        | A location ID to search for |
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

Returns 'data', 'message', and 'success' fields.

The 'data' field contains a list of location entries.
</br></br>


| Field       | Type    | Description            |
| ----------- | ------- | ---------------------- |
| id          | integer | The ID of the location |
| name        | string  | The location name      |
</br></br>


```json
{
    "data": [
        {
            "id": 13,
            "name": "Philippines"
        }
    ],
    "message": "Locations retrieved successfully",
    "success": true
}
```
</br></br>


If a specific location is searched for, but it does not exist:

```json
{
    "data": [],
    "message": "Retrieved 0 locations",
    "success": true
}
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


</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

Returns 'data', 'message', and 'success' fields.

The 'data' field contains a single location entry.
</br></br>


| Field       | Type    | Description            |
| ----------- | ------- | ---------------------- |
| id          | integer | The ID of the location |
| name        | string  | The location name      |

</br></br>


```json
{
    "data": {
        "id": 1,
        "name": "Samaria"
    },
    "message": "Location retrieved successfully",
    "success": true
}
```
</br></br>


If the location does not exist:

```json
{
    "data": [],
    "message": "Retrieved 0 locations",
    "success": true
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

Returns 'data', 'message', and 'success' fields.

The 'data' field contains a list of location entries.
</br></br>


| Field       | Type    | Description            |
| ----------- | ------- | ---------------------- |
| id          | integer | The ID of the location |
| name        | string  | The location name      |

</br></br>


```json
{
    "data": [
        {
            "id": 13,
            "name": "Philippines"
        }
    ],
    "message": "Locations retrieved successfully",
    "success": true
}
```
</br></br>


If the video does not exist:

```json
{
    "error": "Video with ID 6 not found",
    "success": false
}
```

