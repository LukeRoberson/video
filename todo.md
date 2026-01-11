# Version 1.3.1

## Bugs and Improvements

- [x] [Theatre Mode in a Theme is not working](https://github.com/LukeRoberson/video/issues/18)
- [x] [Copying video URL at current time in theatre mode](https://github.com/LukeRoberson/video/issues/20)
- [x] [Improve performance of the similarity script](https://github.com/LukeRoberson/video/issues/14)

</br></br>


## Architecture

- [ ] Separate API and frontend into separate services
  - [x] Create a new directory with basic API framework
  - [ ] Migrate API endpoints (api.py)
  - [ ] Migrate profile management (api_profile.py)
  - [ ] Migrate search (api_search.py)
- [x] Migrate database classes (videos and local)
- [ ] Migrate theme management
- [x] Dockerignore file: Ignore documentation
- [x] Don't wait for Elasticsearch on startup (local mode with no ES)

</br></br>


---
# Version 1.3.2

## Database

- [ ] Move database code into a separate module
- [ ] Extend database fields
  - [ ] Closed captions file
  - [ ] Doc ID
- [ ] Update documentation

</br></br>


## API

- [ ] Catalogue Updates
  - [ ] Get the recent catalog
  - [ ] Check for new videos
- [ ] Create Transcript (for videos that don't have them)
- [ ] Update ElasticSearch indexes


## Indexes

- [ ] Update indexes button in admin page
- [ ] Update indexes when videos added
- [ ] Update indexes when API starts up



---

# Version 1.3.3

## GitHub Issues

### Bugs

- [ ] [Video chapters not displaying correctly on a small screen](https://github.com/LukeRoberson/video/issues/11)
- [ ] [In-progress conflict with snippet](https://github.com/LukeRoberson/video/issues/15)
- [ ] [Snippet - Theatre Mode problems](https://github.com/LukeRoberson/video/issues/17)

</br></br>


### Improvements

- [ ] [Investigate non-interactive scraper](https://github.com/LukeRoberson/video/issues/2)
- [ ] [Search UI improvements](https://github.com/LukeRoberson/video/issues/12)
- [ ] [Feature: Transcript](https://github.com/LukeRoberson/video/issues/19)
- [ ] Dates are in different formats on some videos
    * This cases the 'Latest Videos' in the home screen to get confused

</br></br>


## Searching

- [ ] Search
  - [ ] Filter search results by unwatched
  - [ ] Button to hide extra elasticsearch info on results page
  - [ ] Add a indexing buttons to admin page (create, delete, reindex)
  - [ ] Filter search by disabling certain parts (eg, don't search title, transcript, etc)
- [ ] In dev, absense of elastic search container slows app startup and searching
  * Maybe a CLI arg to start without it
- [ ] Fuzzy match is a little too loose
  * 'Isaiah' returns results for 'Sarah'
  * 'Sprout' > 'proud', 'shout', 'shroud', 'sport', 'spot'
  * 'twig' > twin
- [ ] Encase in double quotes to search for the exact phrase

</br></br>


## Logging

- [ ] Logging
  - [ ] Create a logger instance with stream and file logging
  - [ ] Expose the file log in the compose file
  - [ ] Convert print statements to logs
  - [ ] Some form of log-rotate, so it doesn't get too big

- [ ] Customise Flask logging
  - [ ] Include colours for log types
  - [ ] Suppress unneeded messages

</br></br>


## Testing

- [ ] Testing
  - [ ] Create a basic testing structure/plan; Expand on it later
  - [ ] Script to check that all pages return a 200 OK

</br></br>


## UI

- [ ] Speakers page
  - [ ] Lazy loading of profile images
- [ ] Bible Characters
  - [ ] Lazy loading of profile images
- [ ] Admin page
  - [ ] Add video section: Make scriptures field resizable (like description is)
  - [ ] Add video section: Make tags field resizable

</br></br>


----
# Future Versions

## Architecture

- [ ] Investigate accessibility for template files (e.g., 'alt' tags for images)
- [ ] Add a helper function to get similar videos

</br></br>


## Database
- [ ] DB entry for video type (talk, interview, dramatization, etc)
    * Talk
    * Interview
    * Experience
    * Dramatization
    * Collection (monthly program, Gilead graduations, annual meetings, full convention programs)
- [ ] Convert 'speakers' into 'people' (so references to people that aren't speakers can be included)
- [ ] Fields for extra links, such as links to WT articles
- [ ] Link some verses to bible characters (more for the less common ones)
    * So when we look at a scripture, we can see the character's profile listed
    * When we look at a character, we can see key scriptures
- [ ] Locations
  - [ ] Add classifications to locations
    * Modern/Ancient
    * Country/City
- [ ] Audio Descriptions
    * Add a field for audio descriptions videos
    * Can use this later to switch to the audio description version

</br></br>


## UI

- [ ] Investigate React for a better UI
- [ ] Video details pages:
  - [ ] Share Links
  - [ ] Organise scriptures by book first
  - [ ] Option to show the transcript (from subtitles)
- [ ] Scriptures page: Book can link to the book overview video
- [ ] Homepage:
  - [ ] Random (unwatched) morning worship for the day
- [ ] TV
  - [ ] Find which of the current features are actually needed
  - [ ] Roll back anything not needed
    * Not developing for TV browser as an app
    * Will include just enough to make it 'nice'
  - [ ] Build a sample Native app for Tizen (Samsung TV OS)
    * IDE is VSCode + extension
      * https://developer.samsung.com/smarttv/develop/tools/additional-tools/vscode-extension.html
    * Use React native for the UI
- [ ] Stats page
  * After TypeScript and React are evaluated
  - [ ] Total videos watched / total videos
  - [ ] Video watch time / total watch time
- [ ] Admin option to download the local.db database file for backups

</br></br>


## Tags

- [ ] Aliases, so different tags can mean the same thing
  * eg, 'rto' and 'remote translation office'
- [ ] Tag categories
  * To group tags into
  * Not too many
  * Separate people out from tags first
  * Categories:
    * conflict; wars, etc
    * culture; Languages, cultural groups, political groups, greek words
    * creation; Animals, science
    * history/dates; 1914, 539 bce, 'snare and a racket'
    * qualities/traits; Wisdom, polite, pride, guilt, etc
    * JW terms; Book names, departments, JW library
    * Bible terms; fruitage of the spirit, faithful and discrete slave, etc
- [ ] Add sorting tags by category
- [ ] Colour code tags by category
- [ ] See if some of the rarer tags are actually needed
- [ ] Add a tag count to the top of the tags page
- [ ] Filter 'gilead_*' out of tags page
    * Same as with 'bcast_*'

</br></br>


## General Improvements
- [ ] Profiles
  - [ ] 'Watch later' feature
  - [ ] Options for a PIN on profiles
  - [ ] Include profile's watch history in recommended video calculation
  - [ ] Simplified mode (slider) to hide some details
- [ ] Video Player
  - [ ] Hover mouse over time bar thing: Show thumbnail of that position in the video
  - [ ] Marks on the progress bar to show chapters
  - [ ] Show chapters to the side (on larger screens); Like on Youtube
  - [ ] Tiny icon on thumbnails to show that a video has chapters
- [ ] Speaker Details
  - [ ] DB: Add field for life story, interview, etc
  - [ ] Add lifestory/interview (if there is one) to their page
- [ ] Video details page
  - [ ] Show a speaker's profile pic next to their name
  - [ ] Tooltip for scriptures: Show the scripture on hover
- [ ] Scripts
  - [ ] Script to find videos with no subtitles (so we can create them)
- [ ] Advanced search page (these were difficult to implement previouisly)
  - [ ] Add support to search based on video duration
  - [ ] Add support for date

</br></br>


## Other Ideas
- [ ] Custom import assembly programs from jw stream
- [ ] Music service, like spotify, for JW music
- [ ] A timeline of characters
- [ ] Locations: Links to maps / 'see the good land'
- [ ] AI
  - [ ] Video2vec
    - [ ] Build a vector database representing each video
      * Similar to word2vec
      * Summarises content in a vector format
    - [ ] Integrate into search
    - [ ] Integrate into similarity
  - [ ] Search based on concept (return videos, not its own ideas)
    * eg, 'In what ways did Jesus fulfill prophecies about the Messiah?'
- [ ] Track bible reading progress
- [ ] Bible Characters: Links to website articles that are useful
- [ ] Improved scripture management
  - [ ] Primary scriptures: Key scriptures that relate closely to the topic
  - [ ] Secondary: Scriptures that were cited and add value, but not key
- [ ] Audio description videos
  - [ ] Add secondary links to videos that have audio descriptions
  - [ ] Add an icon to the thumbnail to show that video has this feature
  - [ ] Click a slider to turn this on or off
  - [ ] In reality, just plays a different video
- [ ] Link bible characters to each other
  * eg, Jonathan links to Saul and David
  * Include scriptures that show this link
  * Build a visual map of character links
  * More scriptures, the stronger the link

</br></br>

