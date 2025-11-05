# Search

> [!NOTE]
> This is still in progress


## Overview

The app uses *Elasticsearch* for advanced searching. This runs as a single-node cluster in a separate container.

If the container isn't available, search functionality will fall back to a basic search.

An API exposes search functions.

</br></br>


## API

The API is defined in `app/api_search.py`.

The **base URL** for the search API is `/api/search/`. Routes below use this as a prefix.

| Route     | Method | Notes                                          |
| --------- | ------ | ---------------------------------------------- |
| /         | GET    | Perform a search based on a simple query       |
| /advanced | GET    | An advanced search using additional parameters |
| /reindex  | POST   | Create indexes or rebuild them                 |
| /status   | GET    | Check the status of the search service         |

</br></br>


## Search Status

URL: `/api/search/status`

Method: `GET`

Query Params: *None*

Response codes:
* `200 OK` When the endpoint is responding

**Responses**:

Returns JSON data like this:

```json
{
  "elasticsearch_available": true,
  "fallback_active": false,
  "index_exists": true,
  "timestamp": "2025-11-04T20:52:50.846649+00:00"
}
```

If the elasticsearch container is not working, a `200 OK` code is still returned, as the endpoint is working. However, the response will be different:

```json
{
  "elasticsearch_available": false,
  "fallback_active": true,
  "index_exists": false,
  "error": "Some error message here",
  "timestamp": "2025-11-04T20:52:50.846649+00:00"
}
```


</br></br>


## Reindex

URL: `/api/search/reindex`

Method: `POST`

Query Params: *None*

Response codes:
* `200 OK` If the indexing process completes successfully.
* `503 Service Unavailable` If ES is not available.
* `500 Internal Server Error` If there was some other problem.

**Responses**:

When successful, this returns a JSON response:

```json
{
    "failed": 0,
    "message": "Reindexing completed",
    "success": 2947,
    "total": 2947
}
```

If unsuccessful, a JSON response with an error will be returned:

```json
{
    "error": "Some error message"
}
```


</br></br>


## Basic Search

This is a simple search that doesn't use any advanced filters.

URL: `/api/search/`

Method: `GET`

Query Params:
* `q` - The search query (required)
* `page` - Page number for pagination. Default is 1
* `per_page` - Results per page. Default is 20, maximum is 100

Response codes:
* `200 OK` Search was successful
* `400 Bad Request` Missing or invalid parameters
* `500 Internal Server Error` If there was some other problem.

**Responses**:

A successful search returns:

```json
{
    "page": "page number",
    "pages": "total pages",
    "per_page": "results per page",
    "query": "original query",
    "results": [
        {
            "result-1": "First result in a list"
        },
    "total": "total results returned",
    "using_elasticsearch": true
}
```

</br></br>


Each result in the list will look like this:

```json
{
    "description": "Video description",
    "duration": "Video duration in seconds",
    "highlights": {
        "title": [
            "The video title"
        ]
    },
    "id": "Video ID",
    "name": "Video Title",
    "score": "Percent",
    "thumbnail": "Thumbnail for the video",
    "title": "Title",
    "video_id": "video ID",
    "watched": false
}
```

</br></br>

Notes on the results:
* Video ID and name are returned in multiple formats to support different ways a frontend may query the results
* The score is a percentage reflecting how well the video matches the search
* Highlights refers to the metadata in the video that matched the query
  * The example above shows that something in the title matched the query
  * This could also be a tag, description, etc.
* Other video metadata, such as watch status, duration, and thumbnail, are returned here to prevent additional queries before rendering on the results page.

</br></br>


If there is an error, JSON will be returned, containing the error message:

```json
{
    "error": "error message"
}
```

</br></br>


## Advanced Search

This is an advanced version of the search, which includes additional filtering parameters.

In this implmentation, the `q` parameter is optional, as other parameters may be used.

URL: `/api/search/advanced`

Method: `GET`

Query Params:
* `q` - The search query (optional)
* `page` - Page number for pagination. Default is 1
* `per_page` - Results per page. Default is 20, maximum is 100
* `speakers` - Speaker IDs to filter by (optional)
* `characters` - Character IDs to filter by (optional)
* `locations` - Location IDs to filter by (optional)
* `tags` - Tag IDs to filter by (optional)

Response codes:
* `200 OK` Search was successful
* `400 Bad Request` Missing or invalid parameters
* `500 Internal Server Error` If there was some other problem.

**Responses**:

All responses are the same as with the simple search.

The only exception to this is the advanced search will also return a `filters` value, containing additional parameters that were used in the search.


</br></br>



---
## Elasticsearch

### Version

Elasticsearch 8.19.2 is used, which is the latest in the 8.x train.

> [!NOTE]
> 9.x is still quite new at this time.

</br></br>


### Container

> [!WARNING]
> This section is still being worked on

```bash
docker run -d --name video_elasticsearch_dev -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" -e "bootstrap.memory_lock=true" --ulimit memlock=-1:-1  -v elasticsearch_data:/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:8.19.2
```

* What are the ports for?
  * 9200 returns JSON
  * 9300 - No idea
* What are the environment variables?


Added a .env file to find the container:

```
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
```

For now it's a development container only.


### Index Settings and Mappings

Settings and mappings are defined in `search/mappings.json`.

The two sections of the JSON file are:
* `settings`
* `mappings`

</br></br>


A custom *analyzer* is created. This is the component that processes text fields during searching and indexing.

This analyzer includes:
* **Tokenizer**: Standard
* **Filters**:
  * `lowercase` - Makes all searches case-insensitive.
  * `asciifolding` - Converts non-ascii characters to ASCII

</br></br>


The mappings are a collection of *properties* which describe fields and their types that can be indexed.

These properties of a video are indexed:
* video_id
* title
* tags
* speaker
* bible_character
* location
* scriptures
* transcript
* transcript_chunks
* created_at
* updated_at

</br></br>




---
## Sample Results

Show current status: http://localhost:5000/api/search/status

If working:

```json
{
  "elasticsearch_available": true,
  "fallback_active": false,
  "index_exists": true,
  "timestamp": "2025-11-04T19:49:50.809215+00:00"
}```


If not working:

```json
{
  "elasticsearch_available": false,
  "error": "Object of type HeadApiResponse is not JSON serializable",
  "fallback_active": true,
  "index_exists": false
}
```


To create or reindex videos, **POST** to http://localhost:5000/api/search/reindex


Run a query through the API: http://localhost:5000/api/search/?q=joy

```json
{
  "filters": {},
  "page": 1,
  "pages": 1,
  "per_page": 20,
  "query": "1914",
  "results": [
    {
      "bible_character": "",
      "description": "The Bible describes events, conditions, and attitudes that would mark \u201cthe last days.\u201d (2 Timothy 3:1) See how these signs have been evident in an unprecedented way since the year 1914.",
      "highlights": {
        "title": [
          "The World Has Changed Since <em>1914</em>"
        ]
      },
      "location": "",
      "score": 35.842556,
      "scriptures": "",
      "speaker": "",
      "tags": "",
      "title": "The World Has Changed Since 1914",
      "transcript": "",
      "transcript_chunks": [],
      "video_id": 1941
    }
  "total": 1,
  "using_elasticsearch": true
}
```


When there are no results, it will look like this:

```json
{
  "filters": {},
  "page": 1,
  "pages": 0,
  "per_page": 20,
  "query": "blue",
  "results": [],
  "total": 0,
  "using_elasticsearch": true
}
```



### Testing

See if the service is running by going to http://localhost:9200.

Returns JSON:

```json
{
  "name" : "2e278dc309b9",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "yiEgGtOFRwS4OWlfqJzsyQ",
  "version" : {
    "number" : "8.19.2",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "c1c00e18ef14acd650768ff01f037eaede0c1f7b",
    "build_date" : "2025-08-11T10:07:54.721189302Z",
    "build_snapshot" : false,
    "lucene_version" : "9.12.2",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```


Cluster health: http://localhost:9200/_cluster/health?pretty

```json
{
  "cluster_name" : "docker-cluster",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 3,
  "active_shards" : 3,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 1,
  "unassigned_primary_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 75.0
}
```

Status 'yellow' is ok for a single node cluster.


See indices: http://localhost:9200/_cat/indices?v


```
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size dataset.size
yellow open   videos P1sVQgtqTaKWTdZlFIqNOw   1   1       2947            0    915.1kb        915.1kb      915.1kb
```

> [!warning]
> This looks like its missing information? or is there only meant to be one?


Check video indices: http://localhost:9200/videos

```json
{
    "videos":{
        "aliases":{},
        "mappings":{
            "properties":{
                "bible_character":{
                    "type":"text",
                    "analyzer":"video_analyzer"
                },
                "created_at":{
                    "type":"date"
                },
                "description":{
                    "type":"text",
                    "fields":{
                        "keyword":{
                            "type":"keyword",
                            "ignore_above":256
                        }
                    }
                },
                "location":{
                    "type":"text",
                    "analyzer":"video_analyzer"
                },
                "scriptures":{
                    "type":"text",
                    "analyzer":"video_analyzer"
                },
                "speaker":{
                    "type":"text",
                    "fields":{
                        "keyword":{
                            "type":"keyword"
                        }
                    },
                    "analyzer":"video_analyzer"
                },
                "tags":{
                    "type":"text",
                    "analyzer":"video_analyzer"
                },
                "title":{
                    "type":"text",
                    "fields":{
                        "keyword":{
                            "type":"keyword"
                        }
                    },
                    "analyzer":"video_analyzer"
                },
                "transcript":{
                    "type":"text",
                    "analyzer":"video_analyzer"
                },
                "transcript_chunks":{
                    "type":"nested",
                    "properties":{
                        "text":{
                            "type":"text",
                            "analyzer":"video_analyzer"
                        },
                        "timestamp":{
                            "type":"keyword"
                        }
                    }
                },
                "updated_at":{
                    "type":"date"
                },
                "video_id":{
                    "type":"integer"
                }
            }
        },
        "settings":{
            "index":{
                "routing":{
                    "allocation":{
                        "include":{
                            "_tier_preference":"data_content"
                        }
                    }
                },
                "number_of_shards":"1",
                "provided_name":"videos",
                "creation_date":"1762284871175",
                "analysis":{
                    "filter":{
                        "video_synonym":{
                            "type":"synonym",
                            "synonyms":[]
                        }
                    },
                    "analyzer":{
                        "video_analyzer":{
                            "filter":["lowercase","asciifolding","video_synonym"],
                            "type":"custom","tokenizer":"standard"
                        }
                    }
                },
                "number_of_replicas":"1",
                "uuid":"wGtd5h2-RnOU06UZuWsisg","version":{
                    "created":"8536000"
                }
            }
        }
    }
}
```


Count documents in the index: http://localhost:9200/videos/_count?pretty

```json
{
  "count" : 2947,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  }
}
```


