# Overview

API endpoints that relate to profile management
</br></br>


**Implementation**

`api_profile.py`.
</br></br>


**Base URL**

/api/profile
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /                                   | Get all profiles                             |
| /{{profile_id}}                     | Get a specific profile                       |
| /create                             | Create a profile                             |
| /delete{{profile_id}}               | Delete a profile                             |
| /update/{{profile_id}}              | Update a profile                             |
| set_active                          | Set the active profile*                      |
| get_active                          | Get the active profile*                      |
| clear_history/{{profile_id}}        | Clear a user's watch history                 |
| mark_watched                        | Checks watch status for a video*             |
| mark_watched_bulk                   | Check watch status on multiple videos*       |
| mark_watched                        | Mark a video as watched*                     |
| mark_unwatched                      | Mark a video as unwatched*                   |
| watch_history                       | Check watch history for a profile*           |
| in_progress                         | Manage in-progress status for a video        |
</br></br>



----
# Endpoints

## /api/profile

**Description**

Get a list of all user profiles
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
## /api/profile/{{profile_id}}

**Description**

Get a specific user profile by its ID
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
## /api/profile/create

**Description**

Create a new user profile.

Adds a name, and selects an avatar filename.
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
## /api/profile/delete/{{profile_id}}

**Description**

Delete a profile, identified by its ID.
</br></br>


**Method**

DELETE
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
## /api/profile/update/{{profile_id}}

**Description**

Update the name or avatar filename for a profile.
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
## /api/profile/set_active

**Description**

Set the active profile for this session.

Note: This will be migrated to the frontend in future.
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
## /api/profile/get_active

**Description**

Get the active profile for the current session.

Note: This will be migrated to the frontend in future.
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
## /api/profile/clear_history/{{profile_id}}

**Description**

Clears the watch history in a user's profile.
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
## /api/profile/mark_watched

**Description**

Check if a video has been marked as watched.

This checks against the active profile for this session.

Note: The active profile will be migrated to the frontend in future.
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
## /api/profile/mark_watched_bulk

**Description**

Check multiple videos to see if they have been marked as watched.

This checks against the active profile for this session.

Note: The active profile will be migrated to the frontend in future.
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
## /api/profile/mark_watched

**Description**

Mark a video as watched.

This is performed on the active profile for this session.

Note: The active profile will be migrated to the frontend in future.
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
## /api/profile/mark_unwatched

**Description**

Mark a video as unwatched.

This is performed on the active profile for this session.

Note: The active profile will be migrated to the frontend in future.
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
## /api/profile/watch_history

**Description**

Gets the watch history for the current active profile.

Note: The active profile will be migrated to the frontend in future.
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
## /api/profile/in_progress

**Description**

Manages in-progress video tracking for user profiles.

This is to track where a video is up to, so it can be resumed there in future.
</br></br>


**Method**

GET, POST, UPDATE, DELETE
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
