# Final

* Update project to restrict access to admin tasks
* Git to update videos_db


----
# Future Versions

UI:
* Home page needs to be responsive
* Navbar needs to be responsive
* Stats page (fun stats globally and for the user)
* Profiles of suggested categories on the main page (topics for the main carousel)
* Cache thumbnails to make loading faster
* Simplified mode (slider) to hide some details
* Button to hide watched videos
* Investigate accessibility for template files (eg, 'alt' tags for images)
* Watch history page (see videos watched in order, and when)
</br></br>


Theme based on scripture
* See on the main page as banners
* A theme like 'Sermon on the mount'
* Include videos related to the theme
* Lay out nicely, not just videos based on a category
</br></br>


General Improvements:
* Organise api.py better
* Use consistent logging, not just print statements
* Add a helper function to get similar videos
* Add error handler pages for 500, 400, etc (like 404)
* The code to check for watch status is duplicated over many routes (eg, tag_details, speaker_details, etc)


Regular tasks (a continuing process):
* Add URLs for videos
* Get date stamps for remaining videos
* Get profile pics for speakers
* Get profile pics for characters
* A simpler scraper for new items (avoid scanning the entire site)
</br></br>


Profiles
* Settings page
    * Clear watch history
    * Check for DB updates
* Goal watch time per week (like LinkedIn learning)
* Include watch history in recommended video calculation
* Edit/delete profile
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
* Get working as a phone/tablet app
* Chromecast or Amazon Fire app
* Add unit testing
</br></br>


Filtering
* Before a particular date
* After a particular date
* Shorter than (duration)
* Longer than (duration)
* Search page: check box to show unwatched only
* Consider adding location metadata
</br></br>

