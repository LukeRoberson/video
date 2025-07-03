# UI

## Main Page:

Big items:
* place right after 'continue watching'
* Two videos only'
    * Latest monthly program
    * Latest news
</br></br>

Category for newest videos
* As a carousel, below the big items
</br></br>

Carousel Banners
* Rotating banners at the top of the page
* For now, a nice theme scripture or annotation
* Have several, and select five at random on load
</br></br>


----
# Backend

## Cleanup

* API: Use helper functions for returning success and error (partially implemented)
* Make API paths consistent (eg, 'video' or 'videos', but not both)
* Consolidate functions/routes for APIs, and base them on method
</br></br>

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


## Correlation

Find similar videos
* Look at similar tags, speakers, characters, description
* Need to do research on how to do this best

</br></br>


## Search

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
