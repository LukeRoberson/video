# Web Routes

The web routes are provided by Flask.

There are pages to reflect major categories, as seen on jw.org, such as 'JW Broadcasting' and so on.
</br></br>


----
# Categories
## Category Types

Categories come from jw.org. For the purpose of this app, we consider them to be either a:
* Major category
* A sub category of a major category

Major categories can be found here:
https://www.jw.org/en/library/videos/#en/home
</br></br>


Each major category has sub categories. For example, the 'JW Broadcasting' category has sub categories:
* Monthly Programs
* Talks
* News and Announcements

These can be found here:
https://www.jw.org/en/library/videos/#en/categories/VODStudio
</br></br>


There is nothing explicit in the database to identify a category as major or a sub category.
</br></br>


## Video Categories

All videos have at least two categories associated with them. At the very least, they will have a major category and a subcategory.

Most videos will have more categories assigned.
</br></br>


## Web Pages

Web pages are based on the major category. Within each of these pages, a _carousel_ of sub categories is shown, each containing videos that have both the major category and sub category applied.
</br></br>

