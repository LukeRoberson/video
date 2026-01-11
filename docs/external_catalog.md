# External API

## Overview

New publications and media are made available on jw.org regularly.

When this happens, apps like JW Library are able to find this new content and add it. This appears to be done through a CDN and API.

> [!NOTE] Only publically accessible API information is included here.
> Do not try to access anything beyond this.

</br></br>


## Manifest

A manifest includes all publications in a SQLite3 database.

> [WARNING] The manifest includes publications, but not video or audio.

The manifest has an ID as a string. A change in ID means there's a change in manifest (ie, there are new publications).

</br></br>


### Manifest ID

Get the manifest ID from this URL:

https://app.jw-cdn.org/catalogs/publications/v4/manifest.json

</br></br>


This will return something in in this format:

```json
{
    "version": 1,
    "current": "1c502dfc-9096-4377-93ed-912416609c87"
}
```

</br></br>


### Manifest DB

Get the Manifest database using the ID from the previous step.

https://app.jw-cdn.org/catalogs/publications/v4/<<MANIFEST_ID>>/catalog.db.gz

</br></br>


This will automatically download a compressed copy of the database.

</br></br>


## Media Catalog

Video and audio are not included in the standard manifest.

Instead, there is a separate JSON formatted catalog file containing a media list. Details on each item can be obtained from the API.

</br></br>


### Media List

Get the media list (in English) from here: https://app.jw-cdn.org/catalogs/media/E.json.gz

</br></br>


This will download a compressed JSON file, containing multiple JSON entries. Each entry will contain a _type_ and an _o_ field. The _o_ field contains further information for the type.

Types are:
* catalogSchemaVersion - Describes the schema of the file
* language - Information about the language in the file
* category - Organise information into a category
* media-item - Describes a particular audio or video item

</br></br>


In each *category* entry, there will be a _key_ field to describe the type of category being described. These appear to be containers, containing the minimum information for media in the JW lirary app.

These include:
* TeachingToolbox - Items belonging to the JW library app
* ConvReleases - Convention releases
* VideoOnDemand - A list of all video and audio items
* LatestAudioVideo - A list of the latest audio and video releases

</br></br>


A *media-item* type contains information about each piece of media. This does not include _all_ information on the media however.

Below is a sample entry for the video titled "The Front Seats in the Synagogue":

```json
{
    "type": "media-item",
    "o": {
        "languageAgnosticNaturalKey": "docid-1001072063_1_VIDEO",
        "naturalKey": "docid-1001072063_E_1_VIDEO",
        "keyParts": {
            "docID": 1001072063,
            "languageCode": "E",
            "track": 1,
            "formatCode": "VIDEO"
        },
        "primaryCategory": "VODBibleMedia",
        "title": "The Front Seats in the Synagogue",
        "firstPublished": "2022-01-03T18:56:44.176Z",
        "duration": 93.27,
        "checksums": [
            "53870fd48f248fbdc2bf1754dd64b1e8",
            "aa08d7241e1bc870f9ebbd68a7237e3e",
            "69802210b1a92cfc0d12c2bcf64ef37d",
            "d3c27096c58cd4fb5a1c284559ac7d2e"
        ],
        "images": {
            "sqr": {
                "sm": "https://cms-imgp.jw-cdn.org/img/p/1001072063/univ/art/1001072063_univ_sqr_sm.jpg",
                "xs": "https://cms-imgp.jw-cdn.org/img/p/1001072063/univ/art/1001072063_univ_sqr_xs.jpg",
                "lg": "https://cms-imgp.jw-cdn.org/img/p/1001072063/univ/art/1001072063_univ_sqr_lg.jpg",
                "xl": "https://cms-imgp.jw-cdn.org/img/p/1001072063/univ/art/1001072063_univ_sqr_xl.jpg",
                "md": "https://cms-imgp.jw-cdn.org/img/p/1001072063/univ/art/1001072063_univ_sqr_md.jpg"
            },
            "lsr": {
                "sm": "https://cms-imgp.jw-cdn.org/img/p/1001072063/univ/art/1001072063_univ_lsr_sm.jpg",
                "xs": "https://cms-imgp.jw-cdn.org/img/p/1001072063/univ/art/1001072063_univ_lsr_xs.jpg",
                "lg": "https://cms-imgp.jw-cdn.org/img/p/1001072063/univ/art/1001072063_univ_lsr_lg.jpg",
                "xl": "https://cms-imgp.jw-cdn.org/img/p/1001072063/univ/art/1001072063_univ_lsr_xl.jpg",
                "md": "https://cms-imgp.jw-cdn.org/img/p/1001072063/univ/art/1001072063_univ_lsr_md.jpg"
            }
        }
    }
}
```

</br></br>


Notice that this is generic information that can apply to audio and video items. It does not include paths to the media itself.

</br></br>


### API

To get more information about a specific media item, the API is needed.

To use the API, the following information must first be obtained:
* docid - Get this from the catalog
* track - Usually set to '1'; Check in the catalog
* langwritten - A code matching the language, such as 'E' for English
* fileformat - 'MP4' for video

</br></br>


With that information, we can make a request to the API in this format:

https://b.jw-cdn.org/apis/pub-media/GETPUBMEDIALINKS?docid=<DOCID>&track=<TRACK>&langwritten=<LANG>&fileformat=<FORMAT>

</br></br>


Below is a sample entry for the video titled "The Front Seats in the Synagogue", mentioned earlier:
* docid - '1001072063'
* track - '1'
* langwritten - 'E'
* fileformat - 'MP4'

URL:

https://b.jw-cdn.org/apis/pub-media/GETPUBMEDIALINKS?docid=1001072063&track=1&langwritten=E&fileformat=MP4

</br></br>


This will return a JSON result like this:

```json
{
    "pubName": "Download a Video",
    "parentPubName": "",
    "booknum": null,
    "pub": "",
    "issue": "",
    "formattedDate": "",
    "fileformat": [
        "MP4"
    ],
    "track": 1,
    "specialty": "",
    "pubImage": {
        "url": "",
        "modifiedDatetime": "",
        "checksum": null
    },
    "languages": {
        "E": {
            "name": "English",
            "direction": "ltr",
            "locale": "en",
            "script": "ROMAN"
        }
    },
    "files": {
        "E": {
            "MP4": [
                {
                    "title": "The Front Seats in the Synagogue",
                    "file": {
                        "url": "https://akamd1.jw-cdn.org/sg2/p/195c25a/3/o/1001072063_E_cnt_1_r240P.mp4",
                        "stream": "https://jw.org",
                        "modifiedDatetime": "2023-12-20 21:32:15",
                        "checksum": "53870fd48f248fbdc2bf1754dd64b1e8"
                    },
                    "filesize": 2467676,
                    "trackImage": {
                        "url": "",
                        "modifiedDatetime": "",
                        "checksum": null
                    },
                    "markers": null,
                    "label": "240p",
                    "track": 1,
                    "hasTrack": true,
                    "pub": "",
                    "docid": 1001072063,
                    "booknum": 0,
                    "mimetype": "video/mp4",
                    "edition": "",
                    "editionDescr": "Regular",
                    "format": "",
                    "formatDescr": "Regular",
                    "specialty": "",
                    "specialtyDescr": "",
                    "subtitled": false,
                    "frameWidth": 416,
                    "frameHeight": 234,
                    "frameRate": 24,
                    "duration": 93.269333,
                    "bitRate": 206.69943838882176
                },
                {
                    "title": "The Front Seats in the Synagogue",
                    "file": {
                        "url": "https://akamd1.jw-cdn.org/sg2/p/5b9309/3/o/1001072063_E_cnt_1_r360P.mp4",
                        "stream": "https://jw.org",
                        "modifiedDatetime": "2023-12-20 22:46:05",
                        "checksum": "aa08d7241e1bc870f9ebbd68a7237e3e"
                    },
                    "filesize": 3840235,
                    "trackImage": {
                        "url": "",
                        "modifiedDatetime": "",
                        "checksum": null
                    },
                    "markers": null,
                    "label": "360p",
                    "track": 1,
                    "hasTrack": true,
                    "pub": "",
                    "docid": 1001072063,
                    "booknum": 0,
                    "mimetype": "video/mp4",
                    "edition": "",
                    "editionDescr": "Regular",
                    "format": "",
                    "formatDescr": "Regular",
                    "specialty": "",
                    "specialtyDescr": "",
                    "subtitled": false,
                    "frameWidth": 640,
                    "frameHeight": 360,
                    "frameRate": 24,
                    "duration": 93.269333,
                    "bitRate": 321.668816238881
                },
                {
                    "title": "The Front Seats in the Synagogue",
                    "file": {
                        "url": "https://akamd1.jw-cdn.org/sg2/p/c45e16/3/o/1001072063_E_cnt_1_r480P.mp4",
                        "stream": "https://jw.org",
                        "modifiedDatetime": "2023-12-20 22:16:57",
                        "checksum": "69802210b1a92cfc0d12c2bcf64ef37d"
                    },
                    "filesize": 6528148,
                    "trackImage": {
                        "url": "",
                        "modifiedDatetime": "",
                        "checksum": null
                    },
                    "markers": null,
                    "label": "480p",
                    "track": 1,
                    "hasTrack": true,
                    "pub": "",
                    "docid": 1001072063,
                    "booknum": 0,
                    "mimetype": "video/mp4",
                    "edition": "",
                    "editionDescr": "Regular",
                    "format": "",
                    "formatDescr": "Regular",
                    "specialty": "",
                    "specialtyDescr": "",
                    "subtitled": false,
                    "frameWidth": 960,
                    "frameHeight": 540,
                    "frameRate": 24,
                    "duration": 93.269333,
                    "bitRate": 546.81592126320879
                },
                {
                    "title": "The Front Seats in the Synagogue",
                    "file": {
                        "url": "https://akamd1.jw-cdn.org/sg2/p/4e8d85/3/o/1001072063_E_cnt_1_r720P.mp4",
                        "stream": "https://jw.org",
                        "modifiedDatetime": "2023-12-20 22:09:06",
                        "checksum": "d3c27096c58cd4fb5a1c284559ac7d2e"
                    },
                    "filesize": 9912928,
                    "trackImage": {
                        "url": "",
                        "modifiedDatetime": "",
                        "checksum": null
                    },
                    "markers": null,
                    "label": "720p",
                    "track": 1,
                    "hasTrack": true,
                    "pub": "",
                    "docid": 1001072063,
                    "booknum": 0,
                    "mimetype": "video/mp4",
                    "edition": "",
                    "editionDescr": "Regular",
                    "format": "",
                    "formatDescr": "Regular",
                    "specialty": "",
                    "specialtyDescr": "",
                    "subtitled": false,
                    "frameWidth": 1280,
                    "frameHeight": 720,
                    "frameRate": 24,
                    "duration": 93.269333,
                    "bitRate": 830.33455380237353
                }
            ]
        }
    }
}
```

</br></br>


The key field is _files_. This contains the actual media information.

For video, there is an entry in _files_ for each resolution the video is in (240, 360, 480, 720, 1080)

</br></br>


Within each of these entries, the key fields are:
* title - The title of the video item
* file/url - The URL to the media for this resolution
* file/modifiedDatetime - The time this was modified (different to the catalog time)
* label - Represents the resolution, eg '720p'

</br></br>


Some entries will include _subtitles_ under each of these entries as well. For example:

```json
"subtitles": {
    "url": "https://akamd1.jw-cdn.org/sg2/p/4bd2a1d/1/o/1112024041_E_cnt_1.vtt",
    "modifiedDatetime": "2025-12-17 13:45:32",
    "checksum": "0de737f7b346632bad63b588135a7f61"
}
```


