# Search

> [!NOTE]
> This is still in progress


## Elastic Search

### Version

Version is 8.19.2, the latest in the 8.x train.

Couldn't get 9.x to work (it's new).


### Container

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


### API Status

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


