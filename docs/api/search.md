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
| /status                             | Check search service status                  |
| /advanced                           | Perform an advanced search                   |
| /reindex                            | Reindex videos                               |
</br></br>


> [!NOTE]
> If the ElasticSearch service is not available, search will fall back to a simple database search.
</br></br>



----
# Endpoints

## /api/search/status

**Description**

Check the search service status.

This checks if ElasticSearch is available.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/search/advanced

**Description**

Perform a search of all videos. Supports using advanced parameters.

Searches specific fields (such as tags) for specific values, rather than a general search of all available information.

See also `/api/search` for general guidance.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/search/reindex

**Description**

Request Elasticsearch to reindex all videos.

This can take a few seconds to complete.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>

