# Version 2

## Responsive Design
- [x] Phone
- [x] Tablet
- [ ] TV

</br></br>

Responsive issues (phone screen):
* Home page/Latest videos: Look a bit funny on profiles other than mine

</br></br>


## Platform
- [x] Bugs
  - [x] Videos in the 'latest' category on home pade do not load (404)
  - [x] Scripture chapters are displayed out of order
  - [x] Theatre mode doesn't quite fit into the screen correctly
  - [ ] Link to a time broken in prod; Works locally
- [x] Chromecast support
- [x] General cleanup
  - [x] Split api.py into separate blueprints
  - [x] Split api.py into smaller files based on blueprints
  - [x] Refactor duplicated code for watch status checks (e.g., `tag_details`, `speaker_details`, etc.)
  - [x] Scraper for the latest videos only
  - [x] Add categories to the metadata section of admin page
  - [x] There are some duplicate categories in the database
- [x] Limit access
  - [x] Limit to known URL paths only
  - [x] Block scrapers


## Video Controls
- [x] Skip ahead/back 5s/15s
- [x] Theatre mode (like in YouTube)
- [x] Chapters in longer videos (like in YouTube)
- [x] If in theatre mode and the video ends, wait 1 sec, then close theatre mode

</br></br>


## Search and Filtering
- [ ] Update general search to use description, tags, etc, not just title (elasticsearch container)
- [ ] Class method: Find videos shorter or longer than a certain duration
- [ ] Create an advanced search/filter page (speaker, category, duration, etc.)

</br></br>


## Location
- [x] Add DB table for location
- [x] Add DB table to link videos to locaiton
- [x] Document the new tables
- [x] Add a LocationManager class with methods
- [x] Add a filter to get videos based on location
- [x] Add to admin tools page
- [x] Add locations to video details page
- [x] Dynamic locations page
- [x] Add a 'dig deeper' page for locations
- [x] Add page to navbar
- [ ] Migrate location tags to the new field
- [ ] Update similarity algorithm to use location

</br></br>


## Profiles
- [ ] Option to edit profile
- [ ] Option to delete profile
- [ ] Profile selection screen when opening the app


----
# Future Versions

## UI
- [ ] Stats page (fun stats globally and for the user)
- [ ] Cache thumbnails to make loading faster
- [ ] Simplified mode (slider) to hide some details
- [ ] Button to hide watched videos
- [ ] Investigate accessibility for template files (e.g., 'alt' tags for images)
- [ ] Watch history page (see videos watched in order, and when)
- [ ] Track bible reading progress
- [ ] Share Links
- [ ] Tags page: Add video count to tag label
- [ ] Tags page: Sort alphabetically, or by video count
- [ ] Video details: Organise scriptures by book first
- [ ] Speakers/Characters: Loads all PNGs for the page; Can we load a minimal one to save bandwidth?
- [ ] Can NGINX cache images? Or pre-cache?
- [ ] Scriptures page: Book can link to the book overview video
- [ ] Show chapters to the side (on larger screens); Like on Youtube
- [ ] Tiny icon on thumbnails to show that a video has chapters

## Theme Based on Scripture
- [ ] See on the main page as banners
- [ ] A theme like 'Sermon on the mount'
- [ ] Include videos related to the theme
- [ ] Lay out nicely, not just videos based on a category
- [ ] Profiles of suggested categories on the main page (topics for the main carousel)

## General Improvements
- [ ] Use consistent logging, not just print statements
- [ ] Add a helper function to get similar videos
- [ ] Add error handler pages for 500, 400, etc. (like 404)
- [ ] Support to add custom videos (eg, local assemblies); Think about this a bit though

## Regular Tasks (Ongoing)
- [ ] Add URLs for videos
- [ ] Get date stamps for remaining videos
- [ ] Get profile pics for speakers
- [ ] Get profile pics for characters
- [ ] Create a simpler scraper for new items (avoid scanning the entire site)

## Profiles
- [ ] Settings page
  - [ ] Clear watch history
  - [ ] Check for DB updates
- [ ] Goal watch time per week (like LinkedIn Learning)
- [ ] Include watch history in recommended video calculation
- [ ] Edit/delete profile
- [ ] Options for a PIN on profiles

## AI
- [ ] AI model to transcribe to captions
- [ ] AI model to summarize content

## Project
- [ ] Chromecast or Amazon Fire app
- [ ] Add unit testing
- [ ] Add DB entries for illustrations
- [ ] Add DB entries for ministry ideas (group topics)
- [ ] DDB entry for video type (talk, interview, dramatization, etc)

## Search and Filtering
- [ ] Before a particular date
- [ ] After a particular date
- [ ] Search page: checkbox to show unwatched only
- [ ] Consider adding location metadata

## Video Player
- [ ] Time range to play a specific part of a video
- [ ] Share video link at a particular time
- [ ] Hover mouse over time bar thing: Show thumbnail of that position in the video
- [ ] Marks on the progress bar to show chapters

## Other Ideas
- [ ] Add a 'watch later' feature
- [ ] Custom import assembly programs from jw stream
- [ ] Music service, like spotify, for JW music
- [ ] Convert 'speakers' into 'people' (so references to people can be included)
- [ ] A timeline of characters
