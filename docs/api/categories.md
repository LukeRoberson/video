# Overview

API endpoints that relate to video categories.
</br></br>


**Implementation**

`api_category.py`.

</br></br>


**Base URL**

/api/categories
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /{{category_name}}                  | Resolve a name to an ID                      |
| /{{category_id}}/{{subcategory_id}} | Get videos in a main/subcategory combination |
| /video/{{video_id}}                 | Get categories associated with a video       |
</br></br>


----
# Endpoints

## /api/categories

**Description**

Get all categories at once, including name and ID.

Or, get specific categories using a filter.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/categories/{{category_name}}

**Description**

Resolve a category name to its ID.

Include the category name (string) in the URL.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/categories/{{category_id}}/{{subcategory_id}}

**Description**

Fetch all videos that belong to BOTH the major category and subcategory.

Include the main category ID (integer) and the subcategory ID (integer) in the URL.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>



----
## /api/categories/video/{{video_id}}

**Description**

Get a list of categories that a video belongs to.

Include the video ID (integer) in the URL.
</br></br>


> [!NOTE]
> Documentation has been migrated to Swagger UI
> http://localhost:5010
</br></br>
