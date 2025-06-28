# UI

## Main Page:

Create a favicon
</br></br>

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
* Have several, and selecct five at random on load
</br></br>


## Category Pages:

Adjust the text in the thumbnails
* Does not fit very well
* Investigate better ways to handle long video names
</br></br>

Sort videos in the carousels so the newest is first.
</br></br>

Scrolling carousels with the mouse wheel is slow. See how this can be improved.
</br></br>


## Special Pages:

**Dynamic Pages**
* Base pages for characters, tags, speakers, scriptures
* To browse through these items
</br></br>


## Additional Pages

An 'about' page
* Explain that this is not a JW app
* Explain this does not distribute videos
* Show data for the most recent DB update
</br></br>

A settings page
* This may be part of the profile
* Clear watch history
* Check for DB updates
</br></br>

Admin Tools

_Page has been created, but there's no functionality there yet_

* Meant for me only, so find a way to hide it from regular users; Special profile name maybe?
* Form to add metadata to existing videos
* Form to add a new video
* Button to run a scrape, to check for new videos and categories from the website
</br></br>


----
# Local Data
## Profiles:

* Mark videos as watched (manually)
* Auto mark as watched if a video finishes
* Mark as unwatched
* Track resume time on video

</br></br>


----
# Backend
## Database

**Filtering**
* Before a particular date
* After a particular date
* Shorter than (duration)
* Longer than (duration)
* List of tags (AND/OR)
</br></br>

**Bible Character table**
* Add a profile pic
* Add a date range
* Description field
</br></br>

**Scripture table**
* Add a field to include the text
* Unless this can be retrieved straight from the website?
</br></br>

**Speaker Table**
* Add a field for a picture
</br></br>

**Data**
* Add URLs for videos
* Get date stamps for remaining videos
</br></br>


## Correlation

Find similar videos
* Look at similar tags, speakers, characters, description
* Need to do research on how to do this best

</br></br>


## Search:

* Add basic search functionality
* Page to show videos by topic
* Show by speaker
* Show by bible character
* Show by scripture

</br></br>


----
# Other Things (Bizzare Ideas)
* Stats page (fun stats globally and for the user)
* Profiles of suggested categories on the main page (topics for the main carousel)
* Goal watch time per week (like LinkedIn learning)
* Character pictures (for bible characters)
* Add DB fields for 'chapters' based on timestamp (good for long videos like monthly programs and graduations)
</br></br>

Theme based on scripture
* See on the main page as banners
* A theme like 'Sermon on the mount'
* Include videos related to the theme
* Lay out nicely, not just videos based on a category
