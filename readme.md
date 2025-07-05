# JW Video Streaming Service

A modern web-based video streaming interface for accessing educational content from jw.org and JW Library. This application provides a Netflix-like experience for browsing and watching videos with enhanced search functionality and user profiles.
</br></br>


## ⚠️ Disclaimer

All videos in this application are publicly available on jw.org. This app does not distribute these videos - it serves as an interface to access them in a streaming service format with enhanced search and categorization features.
</br></br>


----
# ✨ Features

### 🎯 Core Functionality
- **Video Streaming**: Stream videos directly from jw.org
- **Advanced Search**: Search by categories, speakers, Bible characters, scriptures, and tags
- **User Profiles**: Create and manage multiple user profiles with custom avatars
- **Responsive Design**: Modern, mobile-friendly interface
</br></br>

### 📚 Content Organization
- **Categories**: Organized by major categories (JW Broadcasting, Bible Studies, etc.)
- **Speakers**: Browse content by specific speakers
- **Bible Characters**: Find videos featuring specific Bible characters
- **Scriptures**: Videos organized by Bible verses and references
- **Tags**: Additional metadata for enhanced discoverability
</br></br>

### 👤 Profile Management
- **Multiple Profiles**: Support for multiple user profiles
- **Custom Avatars**: Choose from a variety of profile pictures
- **Personalized Experience**: Each profile maintains its own viewing preferences
</br></br>


----
# 🚀 Quick Start

There are two ways to run this application: using Docker or running it directly with Python.

Running as a Docker container is the recommended method, however it relies on you having a Docker environment set up.

Below are the instructions for both methods.
</br></br>


## Using Docker

Note: This assumes you have a Docker environment set up and ready to use.

Basic steps are:
1. Get the latest image from Docker Hub
2. Run the Docker container
3. Access the application in your web browser (port 5000 by default)

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
   ```bash
   pip install -r requirements.txt
   ```
</br></br>


3. **Run the application**
   ```bash
   python -m app.main
   ```
</br></br>


4. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`
</br></br>


----
# 📚 Documentation

Additional documentation can be found in the `docs/` directory:
- `project.md` - General project structure information
- `global_database.md` - Schema of the global database
- `local_database.md` - Schema of the local database
- `db_management.md` - The database management classes
- `routes.md` - Web routes documentation
- `similar_videos.md` - The methods of finding similar videos
- `todo.md` - Development roadmap
</br></br>
