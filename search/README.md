# Elasticsearch Integration Setup

This document provides instructions for setting up and using Elasticsearch in the video streaming application.

## Overview

The application uses Elasticsearch for advanced search functionality with the following features:
- Fuzzy matching for handling spelling mistakes
- Multi-field search with prioritization
- Search across video metadata and transcripts
- Automatic fallback to database search if Elasticsearch is unavailable

## Development Setup

### 1. Start Elasticsearch

Using Docker Desktop (recommended):

```bash
cd docker/elasticsearch
docker-compose -f docker-compose.elasticsearch.yml up -d
```

### 2. Verify Elasticsearch is Running

```bash
curl http://localhost:9200
```

You should see a JSON response with cluster information.

### 3. Configure Environment

Copy `.env.example` to `.env` and configure:

```env
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
VTT_DIRECTORY=./vtt
```

### 4. Create Index and Initial Indexing

```bash
# Using Python
python
>>> from search import ElasticsearchIndexer
>>> from app import get_db_connection
>>> indexer = ElasticsearchIndexer()
>>> indexer.create_index()
>>> indexer.reindex_all(get_db_connection())
```

Or use the API endpoint:

```bash
curl -X POST http://localhost:5000/api/search/reindex
```

## Production Deployment

### 1. Update docker-compose.yml

The main `docker-compose.yml` already includes Elasticsearch configuration.

### 2. Deploy

```bash
docker-compose up -d
```

The application will automatically connect to Elasticsearch and fall back to database search if unavailable.

## API Endpoints

### Search Videos

```http
GET /api/search/?q=<query>&page=1&per_page=20
```

Query Parameters:
- `q` (required): Search query string
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Results per page (default: 20, max: 100)
- `speaker` (optional): Filter by speaker name
- `tags` (optional): Comma-separated tags to filter

Response:
```json
{
  "results": [...],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "pages": 8,
  "using_elasticsearch": true,
  "query": "sermon",
  "filters": {}
}
```

### Check Search Status

```http
GET /api/search/status
```

Response:
```json
{
  "elasticsearch_available": true,
  "index_exists": true,
  "fallback_active": false,
  "timestamp": "2025-10-13T10:30:00"
}
```

### Reindex All Videos

```http
POST /api/search/reindex
```

Response:
```json
{
  "success": 1450,
  "failed": 2,
  "total": 1452,
  "message": "Reindexing completed"
}
```

## Search Features

### Field Prioritization

Search results are ranked by relevance with the following field weights:
1. Title (highest priority, 5x boost)
2. Speaker (4x boost)
3. Tags (3x boost)
4. Bible Character (3x boost)
5. Location (2x boost)
6. Scriptures (2x boost)
7. Transcript (base priority)

### Fuzzy Matching

Elasticsearch automatically handles spelling mistakes:
- "sermin" will match "sermon"
- "Jonh" will match "John"
- Requires first 2 characters to match exactly

### Transcript Search

VTT subtitle files are parsed and indexed with timestamps, allowing:
- Full-text search through video transcripts
- Highlighted matching sections
- Timestamp information for matched segments

## Maintenance

### Reindexing

Reindex all videos when:
- Adding new videos to the database
- Updating video metadata
- Changing Elasticsearch mappings

```bash
curl -X POST http://localhost:5000/api/search/reindex
```

### Monitoring

Check Elasticsearch health:

```bash
curl http://localhost:9200/_cluster/health
```

View index statistics:

```bash
curl http://localhost:9200/videos/_stats
```

### Troubleshooting

#### Elasticsearch Not Available

The application automatically falls back to database search. Check:
1. Elasticsearch container is running: `docker ps`
2. Port 9200 is accessible: `curl http://localhost:9200`
3. Application logs for connection errors

#### Poor Search Results

1. Ensure index is up to date: Run reindex
2. Check field mappings: `curl http://localhost:9200/videos/_mapping`
3. Verify VTT files are being parsed correctly

#### Out of Memory

Adjust Java heap size in docker-compose:
```yaml
environment:
  - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
```

## Fallback Behavior

When Elasticsearch is unavailable:
- Application automatically uses database search
- Search functionality continues to work
- `using_elasticsearch` field in response indicates search method
- No application restart required when Elasticsearch becomes available


# Docker

## Docker Run Command (Development)

```bash
docker run -d --name video_elasticsearch_dev -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" -e "bootstrap.memory_lock=true" --ulimit memlock=-1:-1 -v elasticsearch_data:/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:8.11.0
```

* Exposes ports 9200 and 9300
  * 9200 - HTTP API
  * 9300 - node-to-node communication
* Allocates 512MB of memory


### Testing

Test this is working, by browsing to http://localhost:9200

This will return some JSON:

```json
{
  "name" : "...",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "...",
  "version" : { ... },
  "tagline" : "You Know, for Search"
}
```

Check health status: http://localhost:9200/_cluster/health

View indices: http://localhost:9200/_cat/indices?v


## Sample Compose File (Production)

```yaml
version: '3.8'

services:
  # ...existing services...
  
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: video_elasticsearch_prod
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
      - bootstrap.memory_lock=true
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - video_network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped

  app:
    # ...existing app configuration...
    environment:
      # ...existing environment variables...
      - ELASTICSEARCH_HOST=elasticsearch
      - ELASTICSEARCH_PORT=9200
      - VTT_DIRECTORY=/app/vtt
    depends_on:
      elasticsearch:
        condition: service_healthy
    # ...existing app configuration...

volumes:
  # ...existing volumes...
  elasticsearch_data:
    driver: local

networks:
  video_network:
    driver: bridge
```
