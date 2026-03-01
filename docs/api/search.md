# Overview

API endpoints that relate to searching and the elasticsearch service.
</br></br>


**Implementation**

`api_search.py`.
</br></br>


**Base URL**

/api/search
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /                                   | Search through videos                        |
| /reindex                            | Reindex videos                               |
| /status                             | Check search service status                  |
| /advanced                           | Perform an advanced search                   |
</br></br>



----
# Endpoints

## /api/search

**Description**

Search through all videos using query parameters.
</br></br>


**Method**

GET
</br></br>


**Parameters**

| Parameter | Type    | Mandatory | Default | Range | Description                      |
| --------- | ------- | --------- | ------- | ----- | -------------------------------- |
| q         | string  | Yes       | N/A     | N/A   | The search query                 |
| page      | integer | No        | 1       | N/A   | Page number for pagination       |
| per_page  | integer | No        | 20      | 1-100 | Results per page in the response |
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success

`400 BAD REQUEST` if the query parameter is not included.

`400 BAD REQUEST` if invalid pagination parameters are given.

`500 INTERNAL SERVER ERROR` If there was a problem performing the search.
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
## /api/search/reindex

**Description**

Request Elasticsearch to reindex all videos.
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
## /api/search/status

**Description**

Check the search service status.
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
## /api/search/advanced

**Description**

Perform an advanced search of all videos using advanced parameters.
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
