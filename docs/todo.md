# Version 2

## Responsive Design
- [x] Phone
- [x] Tablet
- [ ] TV

</br></br>


## Platform
- [x] Bugs
  - [x] Videos in the 'latest' category on home pade do not load (404)
  - [x] Scripture chapters are displayed out of order
- [x] Chromecast support
- [ ] General cleanup
  - [ ] Split api.py into separate blueprints
  - [ ] Split api.py into smaller files based on blueprints
  - [ ] Refactor duplicated code for watch status checks (e.g., `tag_details`, `speaker_details`, etc.)
  - [x] Scraper for the latest videos only
  - [ ] Add categories to the metadata section of admin page
- [ ] Limit access
  - [ ] Limit to known URL paths only
  - [ ] Block scrapers


## Video Controls
- [ ] Skip ahead/back 5s/15s
  - Requires 8.2.0 or later
  - https://videojs.com/guides/options/#skipbuttons
- [ ] Theatre mode (like in YouTube)
- [ ] Chapters in longer videos (like in YouTube)

</br></br>


## Search and Filtering
- [ ] Update general search to use description, tags, etc, not just title
- [ ] Class method: Find videos shorter or longer than a certain duration
- [ ] Create an advanced search page (speaker, category, duration, etc.)
- [ ] Extra field
  - [ ] Add a field for location
  - [ ] Migrate location tags to the new field
  - [ ] Add to admin tools page

</br></br>


## Profiles
- [ ] Option to edit profile
- [ ] Option to delete profile


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

## Search and Filtering
- [ ] Before a particular date
- [ ] After a particular date
- [ ] Search page: checkbox to show unwatched only
- [ ] Consider adding location metadata

## Video Player
- [ ] Time range to play a specific part of a video

## Other Ideas
- [ ] Add a 'watch later' feature
- [ ] Custom import assembly programs from jw stream
- [ ] Music service, like spotify, for JW music
