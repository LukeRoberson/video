# Version 1.3.0

## GitHub Issues

- [ ] [Investigate non-interactive scraper](https://github.com/LukeRoberson/video/issues/2)
- [ ] [Video chapters not displaying correctly on a small screen](https://github.com/LukeRoberson/video/issues/11)
- [ ] [Search UI improvements](https://github.com/LukeRoberson/video/issues/12)
- [ ] [Improve performance of the similarity script](https://github.com/LukeRoberson/video/issues/14)
- [ ] [In-progress conflict with snippet](https://github.com/LukeRoberson/video/issues/15)

</br></br>


## Architecture

- [ ] Search
  - [ ] Add an elasticsearch container
  - [ ] Integrate elasticsearch with the app
    * Video titles
    * Speakers
    * Locations
    * Tags
    * Bible characters
    * Transcripts (subtitles)
    * Chapters
  - [ ] Fallback to basic search if container is unavailable
  - [ ] Add support to search based on video duration
  - [ ] Add support for date
  - [ ] Add support to search by scriptures

- [ ] Logging
  - [ ] Create a logger instance with stream and file logging
  - [ ] Expose the file log in the compose file
  - [ ] Convert print statements to logs
  - [ ] Some form of log-rotate, so it doesn't get too big

- [ ] Testing
  - [ ] Create a basic testing structure/plan; Expand on it later
  - [ ] Script to check that all pages return a 200 OK

</br></br>


## UI

- [ ] About Page
  - [ ] Disclaimer: Subtitles are machine generated
  - [ ] Disclaimer: Descriptions, tags, locations, etc are custom, not from jw.org
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
  - [ ] Capture remote control input (for navigation)
  - [ ] Menu should not be collapsed (as seen on Amazon Fire)
- [ ] Stats page
  * After TypeScript and React are evaluated
  - [ ] Total videos watched / total videos
  - [ ] Video watch time / total watch time

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

</br></br>


## Other Ideas
- [ ] Custom import assembly programs from jw stream
- [ ] Music service, like spotify, for JW music
- [ ] A timeline of characters
- [ ] Locations: Links to maps / 'see the good land'
- [ ] AI
  - [ ] Model to summarize content (for searching)
  - [ ] Video2vec
    - [ ] Build a vector database representing each video
    * Similar to word2vec
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

