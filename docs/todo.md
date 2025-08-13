# Version 3

## Project
- [x] Create a new branch in github
- [x] Build a beta container for this version, add to stack
- [x] Simplify NGINX config
- [x] Add NGINX config to point some traffic to beta container
- [x] Add records in CloudFlare
- [x] Change nav bar colour for devel
- [x] Find a method to backup local.db on Docker
- [ ] Setup Github actions to build the docker container and push to the hub

</br></br>


## Profiles
- [ ] Profile selection screen when opening the app
- [ ] Settings page
  - [ ] Edit profile name
  - [ ] Edit profile icon
  - [ ] Delete profile
  - [ ] Clear watch history

</br></br>


## Video Player
- [ ] Time range to play a specific part of a video
- [ ] Share video link at a particular time
- [ ] Hover over the bar to show the time index at that point
- [ ] Video bar: Show time passed, not just remaining

</br></br>


## Themes / Banners
- [ ] Create YAML files (or similar) to contain information on a topic
  - [ ] Contains some basic information on the topic
  - [ ] Includes videos (or parts of videos) about that topic
- [ ] Load these (or a selection of them) as banners on the home page
- [ ] Clicking a banner loads a page on that theme

</br></br>



----
# Future Versions

## Performance and Code

- [ ] Cache thumbnails to make loading faster
- [ ] Can NGINX cache images? Or pre-cache?
- [ ] Use consistent logging, not just print statements
- [ ] Investigate accessibility for template files (e.g., 'alt' tags for images)
- [ ] Speakers/Characters: Loads all PNGs for the page; Can we load a minimal one to save bandwidth?
- [ ] Log IP addresses that access the site

</br></br>


## UI
- [ ] Nav bar: Button to hide watched videos
- [ ] Video details pages:
  - [ ] Share Links
  - [ ] Organise scriptures by book first
- [ ] Scriptures page: Book can link to the book overview video

</br></br>


## TV
- [ ] Capture remote control input (for navigation)
- [ ] Menu should not be collapsed (as seen on Amazon Fire)

</br></br>


## Theme Based on Scripture
- [ ] See on the main page as banners
- [ ] A theme like 'Sermon on the mount'
- [ ] Include videos related to the theme
- [ ] Lay out nicely, not just videos based on a category
- [ ] Suggested categories on the main page (topics for the main carousel)

</br></br>


## Database
- [ ] Add DB entries for illustrations
- [ ] Add DB entries for ministry ideas (group topics)
- [ ] DB entry for video type (talk, interview, dramatization, etc)
- [ ] Search Method: Support searching based on duration
- [ ] Convert 'speakers' into 'people' (so references to people that aren't speakers can be included)
- [ ] Get dates for all bible characters
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
  - [ ] Add error handler pages for 500, 400, etc. (like 404)
- [ ] Profiles
  - [ ] Watch history page for each profile
  - [ ] 'Watch later' feature
  - [ ] Goal watch time per week (like LinkedIn Learning)
  - [ ] Options for a PIN on profiles
  - [ ] Include profile's watch history in recommended video calculation
  - [ ] Simplified mode (slider) to hide some details
- [ ] Video Player
  - [ ] Hover mouse over time bar thing: Show thumbnail of that position in the video
  - [ ] Marks on the progress bar to show chapters
  - [ ] Show chapters to the side (on larger screens); Like on Youtube
  - [ ] Tiny icon on thumbnails to show that a video has chapters

</br></br>


## Other Ideas
- [ ] Custom import assembly programs from jw stream
- [ ] Music service, like spotify, for JW music
- [ ] A timeline of characters
- [ ] Locations: Links to maps / 'see the good land'
- [ ] AI
  - [ ] Model to transcribe to captions
  - [ ] Model to summarize content (for searching)
- [ ] Stats page (fun stats globally and for the user)
- [ ] Track bible reading progress
- [ ] Bible Characters: Links to website articles that are useful

</br></br>

