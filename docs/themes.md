# Themes

Themes are web pages that contain a collection of videos relating to a topic.

These are usually in the form of a snippet, where just the relevant part of the video is shown.

There will also be additional information or comments on the videos, such as links to relevant articles.
</br></br>

Themes appear at the top of the home page as banners.
</br></br>


## Theme Files

Themes are created as YAML theme files. These can be found in the static/themes directory.

There is a particular schema that is required for these to work. The class in __theme.py__ manages loading the YAML file, as well as parsing and validating against the required schema.

A sample file __sample.yaml__ shows how a file may look.
</br></br>


## Format

The theme file is a YAML file made of two or more documents.

The first document is global information, such as:
* The HTML title of the theme
* The top heading for the theme
* The banner image that links to the theme (a URL)
</br></br>

Additional documents are __sections__. Sections are separate parts of the web page, and are rendered as different divs in HTML.

The order of items in the section represent the order that they are rendered to the screen.

This only supports a simple subset of what HTML can do in order to simplify the process of creating and updating theme content.
</br></br>

