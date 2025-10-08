# Subtitles

## Overview

Videos support the addition of subtitles. These are _vtt_ files, which are stored in `static/subtitles`.

> [!WARNING]
> Only WebVTT format is supported. SRT is not supported.

</br></br>


## Creating Subtitles

Subtitles can be created manually, following the WebVTT format. But don't do that to yourself.

Instead, use the [Voice to Text](https://github.com/LukeRoberson/Voice-to-Text) project on GitHub.

This uses the OpenAI Whisper model to transcribe the subtitles automatically.

This is a fast process with a GPU. However, CPU is also supported.

</br></br>


## Project Setup

The **readme** file in the project explains how to generate the subtitles in detail. However, as an overview:

1. Pull the respository
    `git pull https://github.com/LukeRoberson/Voice-to-Text.git`
2. Create a virtual environment, and activate it
    `python -m venv venv`
    `venv\Scripts\activate`
3. Install the dependencies
    `pip install -r requirements.txt`
4. [Download ffmpeg](ffmpeg.org)
5. If you have a GPU, there's a few extra steps (skip for CPU only)
   1. Install the latest NVIDIA driver
   2. Install CUDA (12.8 for example)
   3. Install pytorch with CUDA support that matches your CUDA version
        `pip3 install torch --index-url https://download.pytorch.org/whl/cu128`
6. Validate the environment
    `python validate_setup.py`

</br></br>


## Transcribe Videos

Transcribe one video at a time:
`python main.py path\to\your\video.mp4 -f vtt`

</br></br>

> [!NOTE]
> This changes the format to WebVTT. The default is SRT.

</br></br>

> [!TIP]
> The video file can also be a url. This will download the mp4, transcribe it, then delete it.

</br></br>


Alternatively, you can use a CSV file to batch transcribe videos.

The CSV needs to have these fields:
* name - The video name (determines how the subtitle file will be named)
* file - The video filename or URL
</br></br>

> [!TIP]
> You can add other fields to the CSV if you want. These will be ignored
> You could have a field for the _friendly name_ of the video, while the _name_ of the video can be an ID number.

</br></br>


To work with a CSV file:
`python main.py -c csv_file.csv -f vtt`
