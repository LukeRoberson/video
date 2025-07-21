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
