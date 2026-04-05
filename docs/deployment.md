# Deployment

For deploying local dev to Docker devel, or devel to prod.
</br></br>



## Deployment Checklist

* Update the nginx config file
    * Confirm it is correct for prod or dev
* Make sure ENV variables are correct for prod or dev
* Make sure local.db is in the correct place
    * Confirm write permissions are present
* Update ES indexes
</br></br>



## UI Test Plan

- [x] Load home page
    - [x] Themes show at the top
    - [x] Latest News and Monthly Program have two videos
    - [x] Nine videos in 'Latest Videos'
- [x] Video Details (test a few different ones)
    - [x] Load the details page for a video
    - [x] Metadata displays (description, date, tags, url)
    - [x] Categories, speakers, scriptures, and bible characters populate
    - [x] Three similar videos are shown
- [x] Play a video
    - [x] Video plays correctly
    - [x] In progress status tracks correctly (appears as in progress on the home page)
    - [x] Resumes at the correct playback location
    - [x] Mark video as watched
    - [x] Mark video as unwatched
    - [x] Theatre mode and full screen work
    - [x] Skip ahead and back work
    - [x] Different resolutions work
    - [x] Transcript works
- [x] About page loads
- [x] Various category pages load
    - [x] Thumbnails load
    - [x] Can access video details from here
    - [x] Some videos are marked as watched
    - [x] 'Hide watched' slider works
- [x] Dig deeper pages load
    - [x] Characters
        - [x] Character details page loads
        - [x] Metadata present (Name, profile pic, video count, dates, profile description)
        - [x] Associated videos are present
    - [x] Speakers
        - [x] Speaker details page loads
        - [x] Video count shows
        - [x] Associated videos are present
    - [x] Scriptures
        - [x] Scripture details page loads
        - [x] Metadata present (Scripture, text)
        - [x] Associated videos are present
    - [x] Locations
        - [x] Location details page loads
        - [x] Metadata present (name, video count)
        - [x] Associated videos are present
    - [x] Tags
        - [x] Tag details page loads
        - [x] Metadata present (name, video count)
        - [x] Associated videos are present
- [x] Simple Search
    - [x] Simple search gets results
    - [x] ElasticSearch is used
    - [x] Matching fields (title, desc, tags, etc) are shown
    - [x] Load video page from here
- [x] Advanced search
    - [x] Search by speaker filter
    - [x] Search by character filter
    - [x] Search by location filter
    - [x] Search by tag filter
- [x] Profiles
    - [x] Select Guest profile
    - [x] Select non-guest profile
    - [x] Delete a profile
    - [x] Rename a profile
    - [x] Change profile avatar image
    - [x] Create a profile
    - [x] Mark an in progress video as watched
    - [x] Clear a video from the watch history
    - [x] Clear the entire watch history
- [x] Themes
    - [x] Various themes load
        - [x] Videos are shown
        - [x] Titles and descriptions are shown
    - [x] Video snippets work
- [x] Swagger page loads

