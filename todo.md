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

</br></br>


# Scraper

- [x] Issue #8 - Add date to new videos

</br></br>


# Video Player

- [ ] Issue #7
  - [ ] When in theatre mode, click outside of the player to close theatre mode
- [ ] Touch Screen; Tap the video to pause/play
  * Currently this does nothing, need to use play/pause buttons

</br></br>


# UI

- [ ] Issue #6
  - [ ] Add badge to tags to show how many times they are used
  - [ ] Sort tags (on tag page) alphabetically or by count
- [ ] Nav bar: slider to hide watched videos
- [ ] Stats page
  - [ ] Total videos watched / total videos
  - [ ] Video watch time / total watch time

</br></br>


# Other

- [ ] Refactor JS to use classes
- [ ] Add JSDoc to all JS files
- [ ] Refactor to use TypeScript

</br></br>



----
# Future Versions

## Performance and Code

- [ ] Cache thumbnails to make loading faster
- [ ] Can NGINX cache images? Or pre-cache?
- [ ] Use consistent logging, not just print statements
- [ ] Investigate accessibility for template files (e.g., 'alt' tags for images)
- [ ] Speakers/Characters: Loads all PNGs for the page; Can we load a minimal one to save bandwidth?

</br></br>


## UI
- [ ] Video details pages:
  - [ ] Share Links
  - [ ] Organise scriptures by book first
- [ ] Scriptures page: Book can link to the book overview video
- [ ] Homepage:
  - [ ] Random (unwatched) morning worship for the day

</br></br>


## TV
- [ ] Capture remote control input (for navigation)
- [ ] Menu should not be collapsed (as seen on Amazon Fire)

</br></br>


## Database
- [ ] DB entry for video type (talk, interview, dramatization, etc)
- [ ] Search Method: Support searching based on duration
- [ ] Convert 'speakers' into 'people' (so references to people that aren't speakers can be included)
- [ ] Fields for extra links, such as links to WT articles

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
- [ ] Code Improvement
  - [ ] Add a helper function to get similar videos
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
- [ ] Tags
  - [ ] Aliases, so different tags can mean the same thing

</br></br>


## Other Ideas
- [ ] Custom import assembly programs from jw stream
- [ ] Music service, like spotify, for JW music
- [ ] A timeline of characters
- [ ] Locations: Links to maps / 'see the good land'
- [ ] AI
  - [ ] Model to transcribe to captions
  - [ ] Model to summarize content (for searching)
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
- [ ] Video2vec
  - [ ] Similar to word2vec
  - [ ] Build a vector database representing each video
- [ ] Investigate React

</br></br>

