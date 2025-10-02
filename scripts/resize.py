"""
Module: resize.py

Description: This loops through images in a directory and resizes
    them to a specified resolution.

Classes:
    ImageHandler: Handles image resizing operations.
"""

import os
from PIL import Image

CHARACTERS = os.path.join(
    os.path.dirname(__file__),
    '..',
    'static',
    'img',
    'characters'
)

SPEAKERS = os.path.join(
    os.path.dirname(__file__),
    '..',
    'static',
    'img',
    'speakers'
)


class ImageHandler:
    """
    Loop through images in a directory and resize them to a
        specified resolution.

    Attributes:
        directory (str): Directory containing images.
        type (str): Image file type (e.g., 'png', 'jpg').
        resolution (tuple): Desired resolution (width, height).

    Methods:
        __init__:
            Initializes the ImageHandler with directory, type, and resolution.
        scan_directory:
            Scans the directory for images to resize.
    """

    def __init__(
        self,
        directory: str = CHARACTERS,
        type: str = 'png',
        resolution: tuple = (320, 320),
    ) -> None:
        """
        Initialize the ImageHandler.

        Args:
            directory (str): Directory containing images.
            type (str): Image file type (e.g., 'png', 'jpg').
            resolution (tuple): Desired resolution (width, height).

        Returns:
            None
        """

        # Config
        self.directory = directory
        self.type = type.lower()
        self.resolution = resolution

        # Track files
        self.file_list = []

    def scan_directory(
        self,
    ) -> None:
        """
        Scan the directory for images to resize.
        This checks for:
            - File type matches the specified type.
            - Images that do not already match the desired resolution.

        Args:
            None

        Returns:
            None
        """

        # Loop through files in the directory
        for filename in os.listdir(self.directory):
            # Only process files with the specified type
            if filename.lower().endswith(f'.{self.type}'):
                # Check the image resolution
                filepath = os.path.join(self.directory, filename)
                with Image.open(filepath) as img:
                    if img.size != self.resolution:
                        self.file_list.append(filepath)

    def resize_image(
        self,
        filename: str,
        overwrite: bool = False,
    ) -> None:
        """
        Resize an image to the specified resolution.

        Args:
            filename (str): Name of the image file to resize.
            overwrite (bool): Whether to overwrite existing files.

        Returns:
            None
        """

        print(f"Resizing {filename}...")
        with Image.open(filename) as img:
            # Resize the image using high-quality resampling
            resized_img = img.resize(self.resolution, Image.Resampling.LANCZOS)

            # Save the resized image
            if overwrite:
                resized_img.save(filename)

            else:
                print("Skipping save (overwrite is False).")


if __name__ == "__main__":
    # Create an ImageHandler instance for the speakers directory
    handler = ImageHandler(
        directory=SPEAKERS,
        type='png',
        resolution=(320, 320),
    )

    # Scan the directory for images to resize
    handler.scan_directory()

    # Resize each image found
    if len(handler.file_list) == 0:
        print("No images to resize.")
    else:
        for image in handler.file_list:
            handler.resize_image(
                filename=image,
                overwrite=True,
            )
