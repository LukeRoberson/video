# JW Video Streaming Service

A modern web-based video streaming interface for accessing educational content from jw.org and JW Library. This application provides a Netflix-like experience for browsing and watching videos with enhanced search functionality and user profiles.
</br></br>


## Disclaimer

All videos in this application are publicly available on jw.org. This app does not distribute these videos - it serves as an interface to access them in a streaming service format with enhanced search and categorization features.
</br></br>


----
# Features

### Core Functionality
- **Video Streaming**: Stream videos directly from jw.org
- **Advanced Search**: Search by categories, speakers, Bible characters, scriptures, and tags
- **User Profiles**: Create and manage multiple user profiles with custom avatars
- **Responsive Design**: Modern, mobile-friendly interface
</br></br>

### Content Organization
- **Categories**: Organized by major categories (JW Broadcasting, Bible Studies, etc.)
- **Speakers**: Browse content by specific speakers
- **Bible Characters**: Find videos featuring specific Bible characters
- **Scriptures**: Videos organized by Bible verses and references
- **Tags**: Additional metadata for enhanced discoverability
</br></br>

### Profile Management
- **Multiple Profiles**: Support for multiple user profiles
- **Custom Avatars**: Choose from a variety of profile pictures
- **Personalized Experience**: Each profile maintains its own viewing preferences
</br></br>


----
# Quick Start

There are two ways to run this application: using Docker or running it directly with Python.

Running as a Docker container is the recommended method, however it relies on you having a Docker environment set up.

Below are the instructions for both methods.

</br></br>


## Portainer

The simplest method is to deploy using **portainer**. This is a simple docker management UI which is deployed as a container.

This assumes that you have deployed portainer in your environment.

</br></br>


1. Open portainer
2. Go to *stacks*
3. Add a stack
4. Select *Repository*
5. Enter a name for the stack
6. Enter *https://github.com/LukeRoberson/video* as the repository URL
7. Enter *refs/heads/master* as the *Repository reference*
7. Enter *docker-compose.yaml* as the compose path
8. Add the six env variables shown below
9. Deploy the stack

</br></br>


There are environment variables which define where certain files are, such as the local database and certificates.

In the examples below, **/path** is used. Update this to whatever path you're using in your docker server.

| Variable Name   | Value             |
| --------------- | ----------------- |
| LOCAL_DB_PATH   | /path/local.db    |
| NGINX_CONF_PATH | /path/nginx.conf  |
| NGINX_KEY_PATH  | /path/nginx.key   |
| NGINX_CRT_PATH  | /path/nginx.crt   |
| DH_PARAM_PATH   | /path/dh-4096.pem |
| NGINX_LOG_PATH  | /path/nginx       |

</br></br>


## Docker Server

Alternatively, you can deploy in docker directly.

Note: This assumes you have a Docker environment set up and ready to use.

Basic steps are:
1. Get the latest image from Docker Hub
2. Run the Docker container
3. Access the application in your web browser (port 5000 by default)

</br></br>


### Note on Local Database

This requires a local database to be mounted as a volume. This is to store user profiles and watch history. The app will create the contents of the file.

For this to work, you need to:
1. Create an empty file named `local.db` in the directory where you will run the Docker command.
2. Mount this file as a volume in the Docker container.

</br></br>


### Docker Scripts

**Linux:**
```bash
if [ ! -f "local.db" ]; then
   touch local.db
fi
docker pull lukerobertson19/1320:latest
docker run -d -p 5000:5000 -v "$(pwd)/local.db:/app/local.db" lukerobertson19/1320:latest
```

</br></br>


**Windows (Powershell):**
```powershell
if (-Not (Test-Path -Path "local.db")) {
   New-Item -ItemType File -Name "local.db"
}
docker pull lukerobertson19/1320:latest
docker run -d -p 5000:5000 -v ${PWD}/local.db:/app/local.db lukerobertson19/1320:latest
```
</br></br>


## Directly with Python

### Prerequisites
- Python 3.10 or higher
- pip package manager
- git (optional, for cloning the repository)
</br></br>


### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LukeRoberson/video.git
   cd video
   ```

   Alternatively, manually download the repository and extract it to your desired location.

   https://github.com/LukeRoberson/video
</br></br>


2. **Install dependencies**
   Optionally, create a venv first, and activate it.
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   Install the dependencies (in `pyproject.toml`)
   ```bash
   pip install .
   ```
</br></br>


3. **Start the ElasticSearch Service**
   This is optional if you want to use ES for advanced searching.

   Create a volume
   ```bash
   docker volume create elasticsearch_data
   ```

   Run the container
   ```bash
   docker run --env=discovery.type=single-node --env=xpack.security.enabled=false --env=ES_JAVA_OPTS=-Xms512m -Xmx512m --env=bootstrap.memory_lock=true --volume=elasticsearch_data:/usr/share/elasticsearch/data -p 9200:9200 elasticsearch/elasticsearch:8.19.2
   ```

4. **Start the API**
   ```bash
   python -m api.main
   ```

   If using ES, reindex by going to http://localhost:5010/api/search/reindex

5. **Start the UI**
   ```bash
   python -m app.main
   ```
</br></br>


6. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`
</br></br>


----
# Development

## TypeScript Development

This project includes TypeScript files for enhanced type safety and developer experience:

```bash
# Build TypeScript files
npm run build

# Watch for changes and auto-compile
npm run watch

# Clean compiled files
npm run clean
```

Compiled JavaScript files are automatically generated in `static/js/dist/` and included in the application.
</br></br>


----
# �📚 Documentation

Additional documentation can be found in the `docs/` directory
</br></br>
