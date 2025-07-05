# Project Structure

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with custom ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Web Scraping**: BeautifulSoup4 for content discovery
- **Testing**: pytest
</br></br>


----
## 📁 Project Structure

```
├── main.py              # Application entry point
├── api.py               # REST API endpoints
├── web.py               # Main web routes
├── web_categories.py    # Category-specific routes
├── web_dynamic.py       # Dynamic content routes
├── local_db.py          # Database management
├── sql_db.py            # SQL database operations
├── static/              # Static assets (CSS, JS, images)
├── templates/           # HTML templates
├── scripts/             # Data management scripts
├── docs/                # Documentation
└── DB Backup/           # Database backups
```
</br></br>


----
## 🗄️ Database Schema

The application uses SQLite with several tables.

A _global database_ contains video information and metadata. The user does not edit this database, only admins do.

A _local database_ contains profile information for users, including watch history and so on.

See **global_database.md** and **local_database.md** for details.
</br></br>


----
## 🔌 API Endpoints

### Profile API
- `POST /api/profile/create` - Create a new user profile
- `POST /api/profile/set_active` - Set the active profile for the session
- `GET /api/profile/get_active` - Get the active profile for the session
- `POST /api/profile/mark_watched` - Mark a video as watched for the active profile
- `POST /api/profile/mark_unwatched` - Mark a video as unwatched for the active profile
- `GET|POST|UPDATE|DELETE /api/profile/in_progress` - Manage in-progress videos for the active profile
</br></br>


### Video API
- `POST /api/videos/add` - Add a new video to the database
- `GET /api/videos/csv` - Get a CSV file of missing videos
- `GET /api/categories/<int:category_id>/<int:subcategory_id>` - Get videos by category and subcategory
- `GET|POST /api/video/metadata` - Add or update metadata for a video
</br></br>


### Search API
- `GET /api/search/videos` - Search for videos by name or description
</br></br>


### Scripture API
- `POST /api/scripture` - Add text to a scripture


