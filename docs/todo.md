# UI

## Main Page:

Current month's broadcasting video
* Before 'continue watching'
* Only display one from the last 30 days
* If two, within 30 days, show the latest
* If marked as read, don't show at all
</br></br>

Latest GB update (up to 1 month old)
* Between monthly program and continue watching
* Only one within the last 30 days
* Hide when marked as watched
</br></br>

Category for newest videos
* As a carousel, below 'continue watching'
</br></br>

Category for a random tag
* Another carousel below
</br></br>

Carousel Banners
* Rotating banners at the top of the page
* For now, a nice theme scripture or annotation
* Have several, and select five at random on load
</br></br>


----
# Local Data
## Profiles:

* Auto mark as watched if a video finishes
* Track resume time on video
* Show as watched on thumbnail
* Show as in progress on thumbnail
</br></br>

Steps:
1. Create a new table for in progress videos
2. Update local_db.py with new methods for this table
3. API to save the playback position for a video
4. API to get a list of in progress videos
5. Get video.js to track the video time, and update the database through the API
6. Add a 'resume playback' button to video details page
7. Update 'mark as watched' to clear any in-progress entries
8. Update local_database.md


----
# Backend
## Database

**Filtering**
* Before a particular date
* After a particular date
* Shorter than (duration)
* Longer than (duration)
* Search page: check box to show unwatched only
</br></br>

**Data**
* Add URLs for videos
* Get date stamps for remaining videos
* Get profile pics for speakers
* Get profile pics for characters
</br></br>

**Scraper**
* Add a YAML file for ignore categories and videos
* Remove static lists in the script


## Correlation

Find similar videos
* Look at similar tags, speakers, characters, description
* Need to do research on how to do this best

</br></br>


## Search:

* Page to show videos by topic
* Show by speaker
* Show by bible character
* Show by scripture

</br></br>


----
# Other Things (Bizzare Ideas)
* Stats page (fun stats globally and for the user)
* Profiles of suggested categories on the main page (topics for the main carousel)
* Cache thumbnails to make loading faster
</br></br>

UI:
* Simplified mode (slider) to hide some details
* Button to hide watched videos
</br></br>

Theme based on scripture
* See on the main page as banners
* A theme like 'Sermon on the mount'
* Include videos related to the theme
* Lay out nicely, not just videos based on a category
</br></br>

Profiles
* Settings page
    * Clear watch history
    * Check for DB updates
* Goal watch time per week (like LinkedIn learning)
</br></br>

Video Controls
* Skip ahead/back 5s/15s
* Theatre mode (like in youtube)
* Time range, to play a specific part of a video
* Chapters in longer videos (like in youtube)
</br></br>

AI
* AI model to transcribe to captions
* AI model to summarise content
</br></br>

Project
* Break into two project
    * Interface, that users will access
    * Tools, that I will use
* Get working as a phone/tablet app
* Chromecast or Amazon Fire app
