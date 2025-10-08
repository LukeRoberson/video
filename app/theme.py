"""
Module: theme.py

Manages 'themes', which are collections of special web pages.
    Themes are web pages with information in a particular topic.
    These are defined in YAML files in the static/themes folder.

NOTE: Pylance has issues with Cerberus. For example, it does not
    recognize the 'error' and 'validate' attributes of the Validator class.
    It also does not recognise passing a schema to the validate method.
    For this reason, type: ignore comments are used in several places.

Classes:
    ThemeManager: Manages loading and validating theme files.

Dependancies:
    Cerberus: Data validation library for Python.

Custom Dependencies:
    app.sql_db:
        DatabaseContext: Context manager for database operations.
        VideoManager: Manages videos.
"""

# Standard dependencies
from cerberus import Validator
import yaml
import os
from typing import Tuple
import logging

# Custom dependencies
from app.sql_db import (
    DatabaseContext,
    VideoManager
)


class ThemeManager:
    """
    Manages a theme:
        Loads the theme file (YAML).
        Validates the structure and content.

    Theme files contain multiple documents.
        The first document contains the main metadata (title, heading).
        Subsequent documents contain sections of content.
    """

    def __init__(
        self
    ) -> None:
        """
        Initializes the class with predefined schemas.

        The main schema validates the first document (main metadata).
        The section schema validates each section document.
        """

        self.main_schema = {
            # This is the HTML title of the page
            'title': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            # This is the main heading of the page
            'heading': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            # Banner image (URL)
            'banner': {
                'type': 'string',
                'required': True,
                'empty': False,
                'regex': r'^https?://.+'
            }
        }

        self.section_schema = {
            'section': {
                'type': 'list',
                'required': True,
                'schema': {
                    'type': 'dict',
                    'oneof': [
                        # Section Heading
                        {
                            'schema': {
                                'heading': {
                                    'type': 'string',
                                    'required': True,
                                    'empty': False,
                                }
                            }
                        },
                        # Paragraph
                        {
                            'schema': {
                                'paragraph': {
                                    'type': 'string',
                                    'required': True,
                                    'empty': False,
                                }
                            }
                        },
                        # List
                        {
                            'schema': {
                                'list': {
                                    'type': 'list',
                                    'required': True,
                                    'schema': {
                                        'type': 'string',
                                        'empty': False,
                                    }
                                }
                            }
                        },
                        # Video snippet
                        {
                            'schema': {
                                'video': {
                                    'type': 'dict',
                                    'required': True,
                                    'schema': {
                                        'id': {
                                            'type': 'integer',
                                            'required': True,
                                            'min': 1,
                                        },
                                        'start': {
                                            'type': 'integer',
                                            'required': False,
                                            'min': 0,
                                        },
                                        'end': {
                                            'type': 'integer',
                                            'required': False,
                                            'min': 1,
                                        }
                                    }
                                }
                            }
                        },
                        # Quote
                        {
                            'schema': {
                                'quote': {
                                    'type': 'string',
                                    'required': True,
                                    'empty': False,
                                }
                            }
                        },
                        {
                            'schema': {
                                'link': {
                                    'type': 'dict',
                                    'required': True,
                                    'schema': {
                                        'url': {
                                            'type': 'string',
                                            'required': True,
                                            'empty': False,
                                            'regex': r'^https?://.+'
                                        },
                                        'text': {
                                            'type': 'string',
                                            'required': True,
                                            'empty': False,
                                        }
                                    }
                                }
                            }
                        }
                    ]
                },
            }
        }

        # Initialize Cerberus validator
        self.main_validator = Validator(self.main_schema)  # type: ignore
        self.section_validator = Validator(self.section_schema)  # type: ignore

    def _validate_document(
        self
    ) -> Tuple[bool, str]:
        """
        Validates the loaded theme documents against the predefined schemas.

        Args:
            None

        Returns:
            Tuple: (bool, List[str])
                bool: True if all documents are valid, False otherwise.
                List[str]: List of error messages if any document is invalid.
        """

        # Check if documents exist
        if not hasattr(self, 'theme_documents') or not self.theme_documents:
            return (
                False,
                "No theme documents loaded"
            )

        # Validate the main document
        main_doc = self.theme_documents[0]
        if not self.main_validator.validate(main_doc):  # type: ignore
            logging.error(
                f"Main document validation errors: "
                f"{self.main_validator.errors}"  # type: ignore
            )
            return (
                False,
                f"Main document errors: "
                f"{self.main_validator.errors}"  # type: ignore
            )

        # Validate section documents (if any)
        for i, section_doc in enumerate(self.theme_documents[1:], 1):
            if not self.section_validator.validate(  # type: ignore
                section_doc,
                self.section_schema
            ):
                logging.error(
                    f"Section {i} validation errors: "
                    f"{self.section_validator.errors}"  # type: ignore
                )
                return (
                    False,
                    f"Section {i} errors: "
                    f"{self.section_validator.errors}"  # type: ignore
                )

        return (
            True,
            "Documents are valid"
        )

    def _get_video_details(
        self,
    ) -> None:
        """
        Search each section document for videos.
            For each video found, fetch additional details from the database.
            Update the document with these details.
        """

        # Loop through each section document (skipping the main document)
        for section in self.theme_documents[1:]:
            for item in section.get('section', []):
                if 'video' in item:
                    video_id = item['video'].get('id')

                    # Get video details from the database
                    with DatabaseContext() as db:
                        video_mgr = VideoManager(db)
                        details = video_mgr.get(video_id)

                        if not details:
                            logging.warning(
                                f"Video ID {video_id} not found in database."
                            )
                            continue

                        # Update the video info with fetched details
                        details = details[0]
                        item['video'].update(details)

    def load_theme(
        self,
        filepath: str
    ) -> Tuple[bool, str]:
        """
        Loads and validates a theme file.
            Documents are stored in the class instance.

        Args:
            filepath (str): Path to the theme YAML file.

        Returns:
            Tuple: (bool, message)
                bool: True if successful, False otherwise.
                message: Error message if unsuccessful, else success message.
        """

        # Check if the file exists
        if not os.path.exists(filepath):
            logging.error(f"Theme file does not exist: {filepath}")
            return (
                False,
                "File does not exist."
            )

        # Load the theme data from the YAML file
        try:
            # Read all documents from the YAML file
            with open(filepath, "r", encoding="utf-8") as f:
                self.theme_documents = list(yaml.safe_load_all(f))

                # Filter out empty documents
                self.theme_documents = [
                    doc for doc in self.theme_documents
                    if doc is not None
                ]

                # Ensure there is at least one document
                if not self.theme_documents:
                    logging.error(
                        f"No valid documents found in theme file: {filepath}"
                    )
                    return (
                        False,
                        "No valid documents found in YAML file"
                    )

        except Exception as e:
            logging.error(f"Exception reading theme file: {e}")
            return (
                False,
                "Error reading theme file"
            )

        # Validate the documents
        is_valid = self._validate_document()
        if not is_valid[0]:
            return (
                False,
                f"YAML Validation errors: {is_valid[1]}"
            )

        # Fetch additional video details from the database
        self._get_video_details()

        # Separate main document and sections
        self.main = self.theme_documents[0]
        self.sections = self.theme_documents[1:]

        return (
            True,
            "Theme loaded successfully"
        )
