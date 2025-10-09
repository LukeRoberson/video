# Version 1.2.0

# Bugs

- [x] Profile edit not working
  * broken in live, working in devel (containers)
- [x] Snippets not working
  * broken in live, working in devel (containers)
- [x] Issue #4
  - [x] Video categories missing
    * Good news according to Jesus (ep, 2 & 3)
  - [x] Progress bar is wrong on some video categories
    * Children>Dramas has two videos, progress bar says 70
    * Series > The Bible Changes Lives: 14 videos shown, progress bar says 16
    * Series > Viewpoints on the Origin of Life: Videos (10), bar (11)
- [x] Admin page can't add categories to videos
- [ ] About page does not load (fine locally, bad in container)
- [ ] Captions button missing (fine locally, bad in container)
- [ ] Some errors in Chrome console

</br></br>


# Scraper

- [x] Issue #8 - Add date to new videos

</br></br>


# Video Player

- [x] Issue #7
  - [x] When in theatre mode, click outside of the player to close theatre mode
- [x] Touch Screen; Tap the video to pause/play
  * Currently this does nothing, need to use play/pause buttons
- [x] Add subtitle button when vtt files exist

</br></br>


# UI

- [x] Issue #6
  - [x] Add badge to tags to show how many times they are used
  - [x] Sort tags (on tag page) alphabetically or by count
- [x] Nav bar: slider to hide watched videos
- [x] Use Jinja to convert newline to HTML breaks for descriptions
  - [x] Character profiles
  - [x] Scriptures
- [x] Scriptures page organization
    * It's too complicated right now with so many scriptures
- [x] Theme template update
  - [x] Display an image, like a banner
  - [x] Subheadings
  - [x] Strong title for a video
  - [x] Videos in a grid
- [x] Add change log to about page

</br></br>


# Other

- [x] Refactor JS to use classes
- [x] Add JSDoc to all JS files
- [x] Refactor CSS to use BEM format
- [x] Refactor HTML to match CSS BEM
- [x] Refactor to use TypeScript

</br></br>



----
# Future Versions

## Architecture

- [ ] Use consistent logging, not just print statements
- [ ] Investigate accessibility for template files (e.g., 'alt' tags for images)
- [ ] Speakers/Characters: Loads all PNGs for the page; Can we load a minimal one to save bandwidth?
- [ ] Add a helper function to get similar videos
- [ ] Create a testing script to try each URL and check the response is 200 OK

</br></br>


## Database
- [ ] DB entry for video type (talk, interview, dramatization, etc)
    * Talk
    * Interview
    * Experience
    * Dramatization
    * Collection (monthly program, Gilead graduations, annual meetings, full convention programs)
- [ ] Search Method: Support searching based on duration
- [ ] Convert 'speakers' into 'people' (so references to people that aren't speakers can be included)
- [ ] Fields for extra links, such as links to WT articles
- [ ] Link some verses to bible characters (more for the less common ones)
    * So when we look at a scripture, we can see the character's profile listed
    * When we look at a character, we can see key scriptures
- [ ] Locations
  - [ ] Add classifications to locations
    * Modern/Ancient
    * Country/City

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
- [ ] Admin, add videos
  - [ ] Make scriptures field resizable (like description is)
  - [ ] Make tags field resizable
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


## Search and Filtering
- [ ] Advanced Search
  - [ ] Before/after a particular date
  - [ ] Longer than / shorter than (duration)
  - [ ] Add scriptures to the search (book, chapter, verse, or all at once?)
- [ ] Add an elasticsearch container for better searching
- [ ] Search results: checkbox to show unwatched only

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
  - [ ] Model to transcribe to captions
  - [ ] Model to summarize content (for searching)
  - [ ] Video2vec
    - [ ] Build a vector database representing each video
    * Similar to word2vec
- [ ] Track bible reading progress
- [ ] Bible Characters: Links to website articles that are useful
- [ ] Improved scripture management
  - [ ] Primary scriptures: Key scriptures that relate closely to the topic
  - [ ] Secondary: Scriptures that were cited and add value, but not key
- [ ] Audio descriptions
  - [ ] Add secondary links to videos that have audio descriptions
  - [ ] Add an icon to the thumbnail to show that video has this feature
  - [ ] Click a slider to turn this on or off
  - [ ] In reality, just plays a different video

</br></br>

