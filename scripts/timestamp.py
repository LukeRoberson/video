from pymediainfo import MediaInfo
from datetime import datetime
import requests
from tqdm import tqdm
import os
import sys
import random


# Add parent folder to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from sql_db import (    # noqa: E402
    DatabaseContext,
    VideoManager,
)


URL = "https://akamd1.jw-cdn.org/sg2/p/ac675a/1/o/jwb-081_E_09_r240P.mp4"
LOCAL_PATH = r"C:\Users\lrobertson\Videos\JWLibrary\temp.mp4"


class DateTimeAttribute:
    """
    A Class to find the creation date of a media file on the internet.
    It downloads the file to a temp location and extracts the creation date
    using the pymediainfo library.

    Args:
        url (str):
            The URL of the media file to download.
        temp_path (str):
            The local path where the file will be temporarily stored.
    """

    def __init__(
        self,
        url: str,
        temp_path: str = LOCAL_PATH,
    ) -> None:
        """
        Initializes the DateTimeAttribute class.

        Args:
            url (str):
                The URL of the media file to download.
            temp_path (str):
                The local path where the file will be temporarily stored.
        """

        self.url = url
        self.temp_path = temp_path
        self.dateattribute = None
        self.datestamp = None
        self.datestring = None

    def __enter__(
        self
    ) -> "DateTimeAttribute":
        """
        The context manager's entry point.
        """

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ) -> None:
        """
        The context manager's exit point.
        Cleans up the temporary file if it exists.
        """

        # Remove the temporary file if it exists
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

    def get_attribute(
        self,
    ) -> None:
        """
        Gets the creation date of the media file.
            Required the file to be downloaded first.

        Args:
            None

        Returns:
            None
        """

        media_info = MediaInfo.parse(self.temp_path)
        for track in media_info.tracks:
            if track.track_type == "General":
                self.dateattribute = (
                    track.tagged_date or
                    track.encoded_date
                )

        if self.dateattribute:
            try:
                self.datestamp = datetime.strptime(
                    self.dateattribute,
                    "%Y-%m-%d %H:%M:%S.%f %Z"
                )
            except ValueError:
                # Fallback if there are no microseconds
                self.datestamp = datetime.strptime(
                    self.dateattribute,
                    "%Y-%m-%d %H:%M:%S %Z"
                )

        # Format for SQLite
        if self.datestamp:
            self.datestring = self.datestamp.strftime("%Y-%m-%d %H:%M:%S")

    def download_file(
        self,
    ) -> None:
        """
        Downloads the media file from the URL to the local path.
        """

        # Get the remote file as a stream
        tried_360p = False
        while True:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))

                # Open the local file for writing in binary mode
                try:
                    with open(self.temp_path, 'wb') as f, tqdm(
                        desc="Downloading",
                        total=total,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as bar:
                        # Download the file in chunks
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                bar.update(len(chunk))

                    # Exit the loop if download is successful
                    break

                # If the video is not available, try 360P
                except requests.exceptions.RequestException:
                    if not tried_360p and "240P" in self.url:
                        self.url = self.url.replace("240P", "360P")
                        tried_360p = True
                        print("240P not available, trying 360P...")
                    else:
                        print(f"Failed to download: {self.url}")
                        break


if __name__ == "__main__":
    with DatabaseContext() as db:
        video_mgr = VideoManager(db)

        # Get videos with no date_added
        videos = video_mgr.get_filter(
            missing_date=True,
        )

        if not videos:
            print("No videos found with missing date_added.")
            sys.exit(0)

        print(f"Found {len(videos)} videos with no date_added.")

        # Grab a selection of 100 videos to process
        for video in videos:
            with DateTimeAttribute(video['url_240'], LOCAL_PATH) as dt:
                dt.download_file()
                dt.get_attribute()

            if dt.datestring:
                print(f"{video['name']} creation date: {dt.datestring}")
                id = video_mgr.update(
                    video['id'],
                    date_added=dt.datestring,
                )

            else:
                print("No creation date found.")
                id = video_mgr.update(
                    video['id'],
                    date_added="Unknown",
                )

            if id:
                print(f"Updated video ID {id} with date_added {dt.datestring}")
