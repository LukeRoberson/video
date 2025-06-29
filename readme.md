# JW Video Streaming Service

A modern web-based video streaming interface for accessing educational content from jw.org and JW Library. This application provides a Netflix-like experience for browsing and watching videos with enhanced search functionality and user profiles.

## ⚠️ Disclaimer

All videos in this application are publicly available on jw.org. This app does not distribute these videos - it serves as an interface to access them in a streaming service format with enhanced search and categorization features.

## ✨ Features

### 🎯 Core Functionality
- **Video Streaming**: Stream videos directly from jw.org
- **Advanced Search**: Search by categories, speakers, Bible characters, scriptures, and tags
- **User Profiles**: Create and manage multiple user profiles with custom avatars
- **Responsive Design**: Modern, mobile-friendly interface

### 📚 Content Organization
- **Categories**: Organized by major categories (JW Broadcasting, Bible Studies, etc.)
- **Speakers**: Browse content by specific speakers
- **Bible Characters**: Find videos featuring specific Bible characters
- **Scriptures**: Videos organized by Bible verses and references
- **Tags**: Additional metadata for enhanced discoverability

### 👤 Profile Management
- **Multiple Profiles**: Support for multiple user profiles
- **Custom Avatars**: Choose from a variety of profile pictures
- **Personalized Experience**: Each profile maintains its own viewing preferences

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd video
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with custom ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Web Scraping**: BeautifulSoup4 for content discovery
- **Testing**: pytest

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

## 🗄️ Database Schema

The application uses SQLite with the following main tables:
- **videos**: Video metadata and URLs
- **categories**: Content categories
- **speakers**: Speaker information
- **bible_characters**: Bible character profiles
- **scriptures**: Scripture references
- **tags**: Video tags
- **profiles**: User profiles

## 🔌 API Endpoints

### Video API
- `GET /api/videos` - Get all videos
- `GET /api/videos/<id>` - Get specific video
- `GET /api/videos/category/<category>` - Get videos by category

### Search API
- `GET /api/search/speakers/<speaker>` - Search by speaker
- `GET /api/search/characters/<character>` - Search by Bible character
- `GET /api/search/scriptures/<scripture>` - Search by scripture
- `GET /api/search/tags/<tag>` - Search by tag

## 🎨 User Interface

### Main Pages
- **Home**: Featured videos and categories
- **Categories**: Browse by content categories
- **Profile Selection**: Choose or create user profiles
- **Video Player**: Full-featured video playback
- **Admin Dashboard**: Content management (if enabled)

### Navigation Features
- Category browsing with subcategories
- Advanced filtering options
- Search functionality across all content types
- Profile carousel for easy switching

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile devices

## 🔧 Configuration

### Environment Setup
The application can be configured through:
- Database settings in `local_db.py`
- Flask configuration in `main.py`
- Static file paths in web modules

### Profile Pictures
Profile pictures are stored in `static/img/profiles/` and include various character themes.

## 📊 Data Management

### Scripts
The `scripts/` directory contains utilities for:
- Adding videos (`add_videos.py`)
- Managing categories (`add_categories.py`)
- Content scraping (`scraper.py`, `category_scraper.py`)
- Database maintenance

### Database Backups
Regular database backups are stored in the `DB Backup/` directory.

## 📝 Development

### Code Style
- Follows PEP 8 guidelines
- Comprehensive docstrings for modules and functions

## 📚 Documentation

Additional documentation can be found in the `docs/` directory:
- `database.md` - Database schema and structure
- `routes.md` - Web routes and API documentation
- `todo.md` - Development roadmap

## 🔒 Legal

This application is for educational and personal use only. All video content remains the property of its original creators and is accessed through official jw.org channels.

