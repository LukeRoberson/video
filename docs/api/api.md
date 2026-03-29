# API

## Endpoint Types

Endpoints are categorised into these types:

| Type             | Doc File      |
| ---------------- | ------------- |
| Categories       | categories.md |
| Bible Characters | characters.md |
| Profiles         | profiles.md   |
| Scriptures       | scriptures.md |
| Search           | search.md     |
| Similarity       | similarity.md |
| Speakers         | speakers.md   |
| Tags             | tags.md       |
| Videos           | videos.md     |
</br></br>



----
## Swagger UI

Some of these endpoints are now documented in Swagger.

This is accessible at http://localhost:5010.

> [!NOTE]
> Not all endpoints have been migrated to swagger yet.
</br></br>



----
## Standard Responses

### Success

On success, an API call will typically respond with a `200 OK` message.

It will also include a JSON body with a format like this:
</br></br>


```json
{
    "data": [],
    "message": "success message",
    "success": true
}
```
</br></br>


The `data` field will contain whatever information was requested from this endpoint. This will vary for each endpoint.

The `message` field is a simple user-friendly message indicating the success of the API call.

The `success` field is a boolean, indicating success or failure.
</br></br>



### Failure

On failure, the API will respond with a `4xx` or `5xx` error code. `404 NOT FOUND` is common when querying something (such as a video) that does not exist.

This will also include a JSON body in this format:
</br></br>


```json
{
    "error": "An error message describing the problem",
    "success": false
}
```
</br></br>



### Invalid Method

If an invalid method is used, a `405 METHOD NOT ALLOWED` code is returned.

