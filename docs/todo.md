# Version 2

## Responsive Design
- [ ] Phone
- [ ] Tablet
- [ ] TV

| Viewport | Size      | Orientation | Notes         |
|----------|-----------|-------------|---------------|
| Desktop  | 1920x1080 | N/A         | Full HD       |
| Desktop  | 1633x768  | N/A         |               |
| Desktop  | 1280x720  | N/A         | Laptop        |
| Tablet   | 768x1024  | Portrait    |               |
| Tablet   | 1280x800  | Landscape   |               |
| Phone    | 360x800   | Portrait    | Android       |
| Phone    | 375x667   | Portrait    | iPhones       |
| Phone    | 390x844   | Portrait    | iPhone 12/13  |
| Phone    | 412x915   | Portrait    | Bigger phones |

</br></br>


## Platform
- [ ] Chromecast support
  - [ ] Add Chromecast JS library script
  - [ ] Add Google cast launcher button
  - [ ] Add JS function to launch the video on Chromecast
- [ ] General cleanup
  - [ ] Split api.py into separate blueprints
  - [ ] Split api.py into smaller files based on blueprints
  - [ ] Refactor duplicated code for watch status checks (e.g., `tag_details`, `speaker_details`, etc.)
  - [ ] Scripture chapters are displayed out of order


## Video Controls
- [ ] Skip ahead/back 5s/15s
- [ ] Theatre mode (like in YouTube)
- [ ] Time range to play a specific part of a video
- [ ] Chapters in longer videos (like in YouTube)

</br></br>


## Search and Filtering
- [ ] Update general search to use description, tags, etc, not just title
- [ ] Class method: Find videos shorter or longer than a certain duration
- [ ] Create an advanced search page (speaker, category, duration, etc.)

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

## Other Ideas
- [ ] Add a 'watch later' feature
- [ ] Custom import assembly programs from jw stream
- [ ] Music service, like spotify, for JW music
