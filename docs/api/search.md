# Overview

API endpoints that relate to searching and the elasticsearch service.
</br></br>


**Implementation**

`api_search.py`.
</br></br>


**Base URL**

/api/search
</br></br>


**Endpoint Summary**

| Endpoint                            | Description                                  |
| ----------------------------------- | -------------------------------------------- |
| /                                   | Search through videos                        |
| /status                             | Check search service status                  |
| /advanced                           | Perform an advanced search                   |
| /reindex                            | Reindex videos                               |
</br></br>


> [!NOTE]
> If the ElasticSearch service is not available, search will fall back to a simple database search.
</br></br>



----
# Endpoints

## /api/search/status

**Description**

Check the search service status.

This checks if ElasticSearch is available.
</br></br>


**Method**

GET
</br></br>


**Parameters**

None
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success
</br></br>


**Response Body**

Returns 'data', 'message' and 'success' fields.

The 'data' field contains information about the search results.
</br></br>


| Field                   | Type    | Description                                                 |
| ----------------------- | ------- | ----------------------------------------------------------- |
| elasticsearch_available | boolean | Whether the ES service is available                         |
| fallback_active         | boolean | If the search service has fallen back to simple DB searches |
| index_exists            | boolean | Whether a valid search index exists                         |
| timestamp               | string  | The time of the status check                                |
</br></br>


```json
{
    "data": {
        "elasticsearch_available": true,
        "fallback_active": false,
        "index_exists": true,
        "timestamp": "2026-03-13T23:19:48.940795+00:00"
    },
    "message": "Search service status retrieved",
    "success": true
}
```
</br></br>




----
## /api/search/advanced

**Description**

Perform a search of all videos. Supports using advanced parameters.

Searches specific fields (such as tags) for specific values, rather than a general search of all available information.

See also `/api/search` for general guidance.
</br></br>


**Method**

GET
</br></br>


**Parameters**

All parameters are optional.

| Field       | Type    | Default | Description                     |
| ----------- | ------- | ------- | ------------------------------- |
| query       | string  | N/A     | The general search query        |
| speakers    | list    | N/A     | Speaker names to filter by      |
| characters  | list    | N/A     | Character names to filter by    |
| locations   | list    | N/A     | Location names to filter by     |
| tags        | list    | N/A     | Tag names to filter by          |
| page        | integer | 1       | The result page (chunk) number  |
| per_page    | integer | 20      | The results per page (Max. 100) |
</br></br>


> [!NOTE]
> To search for more than one of each type, just include that parameter more than once.
> For example, `?speakers=Stephen Lett&speakers=Burt Mann`
</br></br>


> [!NOTE]
> An advanced search with no parameters will return *everything*
</br></br>



**Body**

None
</br></br>


**Response Code**

`200 OK` on success

`500 INTERNAL SERVER ERROR` If there was an error with the search.
</br></br>


**Response Body**

Returns 'data', 'message' and 'success' fields.

The 'data' field contains some metadata about the search, such as search terms and filters.

It also contains a list of results, with each entry containing information about the video.
</br></br>


General information returned:

| Field               | Type    | Description                               |
| ------------------- | ------- | ----------------------------------------- |
| total               | integer | The total number of results               |
| page                | integer | The current returned page number          |
| pages               | integer | The total number of pages of results      |
| per_page            | integer | The number of results returned per page   |
| using_elasticsearch | boolean | Whether ES was used to return the results |
| filters             | object  | The filters used in the search            |
| query               | string  | The general query used                    |
| results             | list    | A list of results                         |
</br></br>


Filters:

| Field      | Type    | Description                               |
| ---------- | ------- | ----------------------------------------- |
| characters | list    | A list of characters to filter by         |
| locations  | list    | A list of locations to filter by          |
| speakers   | list    | A list of speakers to filter by           |
| tags       | list    | A list of tags to filter by               |
</br></br>


> [!NOTE]
> Searching with filters but no search term will search for those criteria in all videos.
</br></br>


Results:

*See the `/api/search` endpoint for information on these fields*
</br></br>


```json
{
    "data": {
        "filters": {
            "characters": [
                "David"
            ],
            "locations": [
                "Samaria"
            ],
            "speakers": [
                "Stephen Lett"
            ],
            "tags": [
                "prayer"
            ]
        },
        "page": 1,
        "pages": 1,
        "per_page": 20,
        "query": "generosity",
        "results": [
            {
                "bible_character": "David, Jesus, Daniel, Mephibosheth, Hosea, Gomer (Wife of Hosea), Jeroboam II, Zechariah (King of Israel), Shallum (King of Israel), Pekahiah, Pekah",
                "chapter_markers": "Introduction Imitate Jehovah’s Generosity Hospitality—An Opportunity to Build Deep Friendships The Otalora Sisters: Build Faith That Endures Tragedy See Yourself in Paradise Dig for Treasures - Hosea Jehovah Focuses on the Good You Do Music Video - We See You, Sister Conclusion",
                "description": "Theme: Imitate Jehovah’s Generosity\nLessons From the Watchtower - The Delightful Course of Hospitality-So Needed!\nMaythe, Jacky, and Marcela, three sisters, discuss their experiences with unexpected tragedy with the sudden and violent loss of their father.\nInterviews - Children talk about what they look forward to about paradise.\nDig for Treasures - Hosea\nJohn Ekrann: Morning Worship (Pr 15:3)\nMusic Video - Our sisters are an example of faith\n\nVideo post card from French Guiana in South America. 90% of the land is covered by forests.\nThere is great diversity in the people and the languages they speak.\nIt is even the site for the European Space Agency.\nThe kingdom message first arrived when Olga Laland, from Guadaloup, arrived in 1945. He shared the good news in villages, gold mines, and trading posts, over the next two years.\nXavier and Sarah Knoll arrived after graduating from Gilead in 1978, by supporting a group in Cayenne.\nToday there is an average of 3000 publishers, including a peak of 700 regular pioneers, and 11500 at the memorial.\nPublishers often travel by boat to distant territories, as there’s no other way to get to many areas.",
                "duration": 3673,
                "highlights": {
                    "bible_character": [
                        "<em>David</em>, Jesus, Daniel, Mephibosheth, Hosea, Gomer (Wife of Hosea), Jeroboam II, Zechariah (King of Israel), Shallum (King of Israel), Pekahiah, Pekah"
                    ],
                    "chapter_markers": [
                        "Introduction Imitate Jehovah’s <em>Generosity</em> Hospitality—An Opportunity to Build Deep Friendships The Otalora Sisters: Build Faith That Endures Tragedy See"
                    ],
                    "description": [
                        "Theme: Imitate Jehovah’s <em>Generosity</em>\nLessons From the Watchtower - The Delightful Course of Hospitality-So Needed!"
                    ],
                    "location": [
                        "<em>Samaria</em>, Philippines, Japan, Israel, Austria, Switzerland, Croatia, Columbia, Bangladesh, French Guiana, South America, Guadaloup, Cayenne"
                    ],
                    "speaker": [
                        "<em>Stephen</em> <em>Lett</em>, John Ekrann, Stefanie Karapatsios, Barbara Ilg, Sergio Ilg, Marija Golubiček, Maythe Otalora, Jacky Otalora, Marcela Lagno, Prithibi, Nanato"
                    ],
                    "tags": [
                        "<em>prayer</em>, language, translation, construction, friends, preaching, encouragement, volunteer, prison, disaster relief, children, hospitality, peace, love,",
                        "family, prophecy, bible, kingdom, donation, happiness, creator, comfort, <em>generosity</em>, commendation, motive, caleb, sophia, meeting, personal study, sign"
                    ],
                    "transcript": [
                        "We'll discuss the theme, imitate Jehovah's <em>generosity</em>. <em>Generosity</em> is an aspect of Jehovah's love.",
                        "Because of Jehovah's voluminous <em>generosity</em>. But now we ask, how can we imitate Jehovah's <em>generosity</em> in giving physical gifts?",
                        "That is the ultimate example of <em>generosity</em>. But now we ask, how can we imitate Jehovah's <em>generosity</em> in giving spiritual gifts?"
                    ]
                },
                "id": 2687,
                "location": "Samaria, Philippines, Japan, Israel, Austria, Switzerland, Croatia, Columbia, Bangladesh, French Guiana, South America, Guadaloup, Cayenne",
                "name": "JW Broadcasting—August 2025",
                "score": 11.7441025,
                "scriptures": "Proverbs 3:27 - Do not withhold good from those to whom you should give it\nIf it is within your power to help., Ephesians 5:1 - Therefore, become imitators of God, as beloved children,, Proverbs 15:23 - A man rejoices in giving the right answer,\nAnd a word spoken at the right time—how good it is!, Proverbs 15:3 - The eyes of Jehovah are everywhere,\nWatching both the bad and the good., Psalms 139:14 - I praise you because in an awe-inspiring way I am wonderfully made.\nYour works are wonderful,\nI know this very well., James 1:17 - Every good gift and every perfect present is from above, coming down from the Father of the celestial lights, who does not vary or change like the shifting shadows., 1 Peter 4:9 - Be hospitable to one another without grumbling., Genesis 8:21 - And Jehovah began to smell a pleasing aroma. So Jehovah said in his heart: “Never again will I curse the ground on man’s account, for the inclination of the heart of man is bad from his youth up; and never again will I strike down every living thing as I have done., James 2:15 - If any brothers or sisters are lacking clothing and enough food for the day,, James 2:16 - yet one of you says to them, “Go in peace; keep warm and well fed,” but you do not give them what they need for their body, of what benefit is it?, 1 Corinthians 16:2 - On the first day of every week, each of you should set something aside according to his own means, so that collections will not take place when I arrive., John 14:26 - But the helper, the holy spirit, which the Father will send in my name, that one will teach you all things and bring back to your minds all the things I told you., Proverbs 18:21 - Death and life are in the power of the tongue;\nThose who love to use it will eat its fruitage., Colossians 3:13 - Continue putting up with one another and forgiving one another freely even if anyone has a cause for complaint against another. Just as Jehovah freely forgave you, you must also do the same., Psalms 37:11 - But the meek will possess the earth,\nAnd they will find exquisite delight in the abundance of peace., Romans 12:12 - Rejoice in the hope. Endure under tribulation. Persevere in prayer., Hosea 1:2 - When Jehovah started to speak his word through Ho·seʹa, Jehovah said to Ho·seʹa: “Go, marry a woman of prostitution and have children of prostitution, because by prostitution the land has turned completely away from following Jehovah.”, Hosea 3:1 - Then Jehovah said to me: “Go once again, love the woman who is loved by another man and is committing adultery, just as Jehovah loves the people of Israel while they turn to other gods and love raisin cakes.”, John 8:29 - And the One who sent me is with me; he did not abandon me to myself, because I always do the things pleasing to him.”, Luke 18:9 - He also told this illustration to some who trusted in their own righteousness and who considered others as nothing:, Luke 18:10 - “Two men went up into the temple to pray, the one a Pharisee and the other a tax collector., Luke 18:11 - The Pharisee stood and began to pray these things to himself, ‘O God, I thank you that I am not like everyone else—extortioners, unrighteous, adulterers—or even like this tax collector., Luke 18:12 - I fast twice a week; I give the tenth of all things I acquire.’, Luke 18:13 - But the tax collector, standing at a distance, was not willing even to raise his eyes heavenward but kept beating his chest, saying, ‘O God, be gracious to me, a sinner.’, Luke 18:14 - I tell you, this man went down to his home and was proved more righteous than that Pharisee. Because everyone who exalts himself will be humiliated, but whoever humbles himself will be exalted.”",
                "speaker": null,
                "tags": null,
                "thumbnail": "https://cms-imgp.jw-cdn.org/img/p/jwb-129/univ/art/jwb-129_univ_wss_01_lg.jpg",
                "title": "JW Broadcasting—August 2025",
                "video_id": 2687,
                "watched": false
            }
        ],
        "total": 1,
        "using_elasticsearch": true
    },
    "message": "Advanced search completed",
    "success": true
}
```
</br></br>





----
## /api/search/reindex

**Description**

Request Elasticsearch to reindex all videos.

This can take a few seconds to complete.
</br></br>


**Method**

POST
</br></br>


**Parameters**

None
</br></br>


**Body**

None
</br></br>


**Response Code**

`200 OK` on success

`503 SERVICE UNAVAILABLE` if there is a problem with the search service
</br></br>


**Response Body**

Returns 'data', 'message' and 'success' fields.
</br></br>


| Field       | Type    | Description               |
| ----------- | ------- | ------------------------- |
| message     | string  | The result of the request |
| success     | integer | Number of indexes created |
| failed      | integer | Number of failed indexes  |
| total       | integer | Total number of indexes   |
</br></br>


```json
{
    "data": {
        "failed": 0,
        "success": 2992,
        "total": 2992
    },
    "message": "Reindexing completed",
    "success": true
}
```
</br></br>


If there is a problem with the ElasticSearch service:

```json
{
    "error": "Elasticsearch is not available"
}
```
</br></br>



