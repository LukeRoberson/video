# Chapters

Longer videos can be divided into chapters.

If a video has chapters, a button will appear on the control bar. Hover over it to see the chapters and jump to them.

</br></br>


## WebVTT

WebVTT files are used to define chapters. These are stored in static/vtt.

There is one file for each video that has chapters. The filename is the video's ID with the '.vtt' extension.

If there is no VTT file for a video, then the video has no chapters defined.
</br></br>


## File Format

The file format looks like this:

```vtt
WEBVTT

00:00:00.000 --> 00:01:00.000
Introduction

00:01:00.000 --> 00:02:00.000
Chapter 1

00:02:00.000--> 00:03:00.000
Chapter 2

00:03:00.000 --> 00:04:00.000
Conclusion
```
</br></br>


# Snippets

A snippet of a video can be played. This has a defined start and end time.
</br></br>


## UI

When in snippet mode, an overlay appears in the top left of the video player, and shows the time range that is being played.

There is a close button to close snippet mode. This does not just hide the overlay, it exits snippet mode completely.

The progress bar displays an overlay showing the time range that the snippet covers.
</br></br>


## Parameters

To enter snippet mode, use URL parameters:
* The 't' parameter specifies the time to start the video, in seconds
* the 'end' parameter specifies when the snippet ends (also in seconds)

The 't' parameter can be used to start a video at a time, and does not require an 'end' parameter.

For example, this will start a video at 1 minute:

```http://url/video/1682?t=60```
</br></br>


When both the start and end parameters are included, snippet mode is used.

For example, this plays a snippet of a video, from 1 minute to 2 minutes:

```http://url/video/1682?t=60&end=120```
</br></br>
