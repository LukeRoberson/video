# Similar Videos

The video details page, where users watch videos, recommends similar videos.

These are based on similarity to the current video only, not based on the user's watch history.
</br></br>


## Metadata

Videos contain this metadata, which can be used for matching:

| Metadata    | Presence  | Description                                    | Source                                |
| ----------- | --------- | ---------------------------------------------- | ------------------------------------- |
| Name        | Mandatory | Video title, matching jw.org                   | jw.org                                |
| Description | Desired   | A description of the video                     | jw.org if available, otherwise custom |
| Tags        | Desired   | Short tags to describe the video               | Custom                                |
| Speaker     | Optional  | Named speakers in the video                    | Custom                                |
| Character   | Optional  | Bible characters in or referenced in the video | Custom                                |
| Scripture   | Optional  | Scriptures in the video                        | Custom                                |
</br></br>

Videos should have descriptions and tags. However, not all do as they haven't all been reviewed yet.

Speaker, character, and scripture, may or may not be present, depending on the type of video format, and the content of the video.
</br></br>


----
# Algorithm
## Weighted Results

Similar videos are found using a weighted scoring system, based on multiple factors.

| Factor    | Weight | Description                             |
| --------- | ------ | --------------------------------------- |
| Tag       | 40%    | More matching tags = higher similarity  |
| Speaker   | 20%    | Higher weight for exact speaker matches |
| Scripture | 15%    | Exact match (high), same book (medium)  |
| Character | 15%    | More matching characters = higher       |
| Text      | 10%    | Word overlap, theme detection           |
</br></br>


## General Principles

All measurements will return a value between 0 and 1, where 0 is completely different, and 1 is identical.

Constraining to this range is a form of normalization.
</br></br>

All similarity functions need to gracefully handle missing data.

This is important, since many videos will not have all types of metadata. For example, a music video will not have a speaker.
</br></br>


## Tag and Character Similarity

Tag similarity uses the _Jaccard similarity coefficient_ to measure overlap.

$J(A,B) = \frac{|A \cap B|}{|A \cup B|}$
</br></br>

A and B represent the datasets being compared (the two sets of tags).

|A ∩ B| is the size (number of elements) of the intersection between A and B. That is, the number of tags that are found in both videos.

|A ∪ B| is the size of the union of sets A and B. That is, the total number of unique tags for _both_ videos.

Dividing intersection by union results in a value between 0 and 1.
</br></br>


## Speaker Similarity

This uses _Max Normalization_ to find the fraction of speakers (of the larger set) that appear in both videos.

$S(A,B) = \frac{|A \cap B|}{\max(|A|, |B|)}$
</br></br>

This gets the intersection (same as with tags), and divides it by the larger of the two sets.
</br></br>


## Scripture Similarity

Scripture similarity is hierarchical:
1. An exact verse match (1.0)
2. A chapter match (0.5) 
3. Book match (0.2)
4. No match at all (0.0)

Each scripture in set A is compared to each scripture in set B, and assigned a score as above.

The results are all added up, and divided by the size of set A times the size of set B.

$ScriptureSim(A,B) = \frac{\sum_{s_a \in A}\sum_{s_b \in B}match_score(s_a, s_b)}{|A| \times |B|}$
</br></br>


## Text Similarity

_Overlap Coefficient_ is used to find text similarity. This is to find the fraction of words from the smaller set that appear in both sets.

First, there is some preprocessing to remove noise:
1. Converts all text to lowercase
2. Remove punctuation
3. Remove stop words

$\text{Overlap}(A,B) = \frac{|A \cap B|}{\min(|A|, |B|)}$
</br></br>

This is nearly the same as speaker similarity, except we divide by the smaller set, not the larger.
</br></br>


## Weighted Score

Finally, create the weighted score by getting a _linear combination_ of the other scores.

$\text{Similarity} = 0.4 \times \text{TagSim} + 0.2 \times \text{SpeakerSim} + 0.15 \times \text{ScriptureSim} + 0.15 \times \text{CharacterSim} + 0.1 \times \text{TextSim}$
</br></br>

This factors in the weights, and adds the results to get the final value.
</br></br>


----
# Pre-Calculation

When there's 2000 or more videos, it's not efficient to calculate similarity at runtime (when the video details page loads).

Instead, this process is used:
1. A server side process runs the algorithm
2. The top matches for each video are found
3. These matches are stored in the database

When the results are _baked in_ to the global database, there are some advantages and disadvantages:
* Fast lookup when the user watches a video
* Needs to be rerun when videos are added and metadata changes
* Less scalability to include customised recommendations in future
</br></br>


## Database

A table in the global database (see **global_database.md**) has records which store:
* Video ID
* Similar video ID
* Similarity score

This can contain just the top _n_ results. It doesn't need to store a full matrix linking all 2000 videos to all other 2000 videos.

For example, the top 10 similar videos could be stored in the database. Queries could pull the top three, or three random videos from the top 10.
</br></br>


## Calculation

On demand, and Admin can run a process to calculate scores for each video.

This would generally be done when new videos are added to the database.

Adding new metadata to existing videos may also require this process to be run.

This can be comutationally difficult, so it shouldn't be done too often.
</br></br>


----
# Implementation

This is implemented as a class, which is called in a context handler.
</br></br>


## Similarity Calculation
### Values

Inputs:
* Video #1 ID
* Video #2 ID

Output:
* A score (value between 0.0 and 1.0)
</br></br>


### Method: *Collect Data*

1. Validates both videos exist
2. Get name and description for both videos
3. Get tags for both videos
4. Get scriptures for both videos
5. Get speakers for both videos
6. Get characters for both videos

All these values are stored in the instance of the class.
</br></br>


### Method: *Jaccard Similarity*

Used with tags and characters.

1. Convert both lists of tags or characters to sets.
2. Calculate the intersection
3. Calculate the union
4. Divide the intersection by the union
</br></br>

The Python _intersection_ and _union_ properties can be used in this case.
</br></br>


### Method: *Max Normalization*

Used with speaker similarity.

1. Convert lists to sets
2. Get the intersection
3. Get the size of the larger set
4. Divide intersection by size of larger set
</br></br>

Use Python's _len_ to get the size of a set, and _max_ to find the larger of the two.
</br></br>


### Method: *Hierarchical Similarity*

Used with scriptures.

Scriptures are already in a dictionary format, with separate keys for book, chapter, and verse.

1. Calculate the max possible score (size of dataset 1 * size of dataset 2)
    * That would be if every scripture was a perfect match
2. Loop over each scripture combination:
    * Get the score for each pair (as defined earlier)
    * Add the score to a running total
3. Divide the total score by the max possible score
</br></br>


### Method: *Overlap Coefficient*

Used with descriptions.

1. Combine the name and the description for each of the two videos
2. Preprocess: Convert text to lowercase
3. Preprocess: Remove punctuation
4. Preprocess: Remove stop words (Bag of Words)
5. Create a set of words in the text for each video
6. Calculate the intersection
7. Calculate the size of the smaller set
8. Divide the intersection by the size of the smaller set
</br></br>

The Python _min_ function can find the smaller set.
</br></br>



### Method: *Weighted Sum*

Calculate the final weighted sum and return it.

1. Multiply each similarity score by its weight
2. Add up all the resulting values
3. Return the final similarity score
</br></br>


## Pre-Calculation

This is the classes and functions used to get similarity scores, and store in the database for retrieval later.

1. Make sure the new table is created in the **global database**
2. Create a class in **sql_db.py** to manage CRUD operations for this table
3. Create a script to calculate and store the scores:
    * Collect a list of all videos and loop over them
    * Create similarity scores for each pair
    * Store the top 10 in the table
</br></br>


Optional Improvements:

Find ways to improve performance of the script
* Threading or asynchronous processing
* Batching
* Don't rerun pairs that have been done already

Optionally, run only on a specific list of videos
* Ones that have been recently added
* Ones that have had their metadata updated
</br></br>


----
# Potential Future Improvements

* Use the watch history of the user to influence the results
* Use Spacy or a similar library to better compare text
* Use Spacy to normalise similar tags
