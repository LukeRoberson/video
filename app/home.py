"""
Module: home.py

Define flask route for the home page.

Functions:
    TBA

Routes:
    - /
        The home page

Flask Dependencies:
    - Blueprint
    - Response
    - make_response
    - render_template
    - url_for
    - redirect
    - session
    - request

Dependencies:
    - typing: For type annotations
    - concurrent.futures: For threaded API calls
    - os: For building file paths
    - yaml: For parsing theme YAML files
    - requests: For making API calls to the backend

Custom Imports:
    - app.cache: For accessing cached data like category IDs
"""


# Standard Library Imports
from flask import (
    Blueprint,
    Response,
    make_response,
    render_template,
    url_for,
    redirect,
    session,
    request
)
from typing import (
    Dict,
    Any,
)
import os
import yaml
import requests


# Custom Imports
from app.cache import app_cache


home_bp = Blueprint(
    'home',
    __name__,
)


@home_bp.before_app_request
def ensure_profile_selected() -> None | Response:
    """
    Ensure that a profile is selected before accessing any web pages.

    This function checks if a profile is selected in the session.
    If no profile is selected, redirects user to the profile selection page.

    Args:
        None

    Returns:
        None | Response: Returns None if the profile is selected,
            otherwise returns a redirect response
            to the profile selection page.
    """

    # Allow static and profile API routes
    if request.endpoint in ('static',):
        return
    if request.blueprint == 'profile_bp':
        return

    # Allow the profile selection/creation pages
    if request.endpoint in (
        'web_pages.select_profile',
        'web_pages.create_profile',
    ):
        return

    # Only redirect on normal page loads that expect HTML
    if (
        request.method in ('GET', 'HEAD') and
        request.accept_mimetypes.accept_html
    ):
        # Get the active profile from the session
        active = session.get('active_profile', None)

        # If no profile yet, send them to selector
        if active is None:
            next_url = request.url or url_for('home.home')
            return make_response(
                redirect(
                    url_for(
                        'web_pages.select_profile',
                        next=next_url
                    )
                )
            )


@home_bp.app_context_processor
def inject_admin_status() -> Dict[str, Any]:
    """
    Injects the admin status into the template context.

    Checks if the selected user is an admin, which is stored in the session.

    Args:
        None

    Returns:
        Dict[str, Any]: A dictionary containing the admin status.
    """

    return {
        'is_admin': session.get('profile_admin', False)
    }


@home_bp.route(
    "/",
    methods=["GET"],
)
def home() -> Response:
    """
    A very simple home page that renders the main HTML template.

    Returns:
        Response: A rendered HTML 'welcome' page
    """

    def fetch_in_progress() -> list:
        """
        API Call: Get the in-progress videos for the active profile.

        Returns:
            list: A list of in-progress videos for the active profile.
        """

        if profile_id is None:
            return []

        response = requests.get(
            url='http://localhost:5010/api/profile/in_progress',
            params={'profile': profile_id},
        )

        return response.json().get('data', [])

    def fetch_monthly() -> list:
        """
        API Call: Get the latest monthly programs.

        Returns:
            list: A list of the latest monthly programs.
        """

        return requests.get(
            url='http://localhost:5010/api/videos/filter',
            params={
                'cat': categories.get('Monthly Programs', None),
                'latest': 1,
            },
        ).json().get('data', [])

    def fetch_news() -> list:
        """
        API Call: Get the latest news and announcements.

        Returns:
            list: A list of the latest news and announcements.
        """

        return requests.get(
            url='http://localhost:5010/api/videos/filter',
            params={
                'cat': categories.get('News and Announcements', None),
                'latest': 1,
            },
        ).json().get('data', [])

    def fetch_latest() -> list:
        """
        API Call: Get the latest videos.

        Returns:
            list: A list of the latest videos.
        """

        return requests.get(
            url='http://localhost:5010/api/videos/filter',
            params={'latest': 9},
        ).json().get('data', [])

    # Get a list of files in the themes directory
    themes_dir = os.path.join('static', 'themes')
    themes = []
    if os.path.exists(themes_dir):
        themes = [
            f for f in os.listdir(themes_dir)
            if (
                os.path.isfile(os.path.join(themes_dir, f)) and
                f.lower() != 'sample.yaml'
            )
        ]

    # Get banners and titles from each theme file
    banners = []
    for theme in themes:
        with open(os.path.join(themes_dir, theme), 'r', encoding='utf-8') as f:
            try:
                theme_data = list(yaml.safe_load_all(f))
                banner = {
                    'image': theme_data[0].get('banner', None),
                    'title': theme_data[0].get('title', 'No Title'),
                    'path': theme[:-5],  # Remove .yaml extension
                }
                banners.append(banner)
            except yaml.YAMLError as e:
                print(f"Error loading theme file {theme}: {e}")
                themes.remove(theme)

    # Get the session profile ID from the request context
    in_progress_videos = []
    profile_id = session.get('active_profile', None)

    # API: Get in progress videos
    in_progress_videos = fetch_in_progress()

    # API: Get the details for each in-progress video
    response = requests.post(
        url='http://localhost:5010/api/videos/get_bulk',
        json={'video_ids': [v['video_id'] for v in in_progress_videos]}
    )
    data = response.json().get('data', [])

    # Merge the in-progress video data with the API video details
    updated_list = []
    for video in in_progress_videos:
        entry = {}
        entry['current_time'] = video['current_time']
        entry['profile_id'] = video['profile_id']
        entry['updated_at'] = video['updated_at']
        entry['video_id'] = video['video_id']

        for i in data:
            if i['id'] == video['video_id']:
                entry['name'] = i.get('name')
                entry['thumbnail'] = i.get('thumbnail')
                entry['duration'] = i.get('duration')
                break

        updated_list.append(entry)

    # Sort, so the most recently updated videos are first
    updated_list.sort(
        key=lambda v: v.get('updated_at', ''),
        reverse=True
    )

    # Get category IDs from the cache (cached at startup)
    categories = app_cache.get_category_ids()

    # API: Get the latest monthly programs video
    monthly = fetch_monthly()
    # monthly = None
    # monthly = requests.get(
    #     url='http://localhost:5010/api/videos/filter',
    #     params={
    #         'cat': categories.get('Monthly Programs', None),
    #         'latest': 1
    #     }
    # ).json().get('data', [])

    # API: Get the latest news video
    news = fetch_news()
    # news = None
    # news = requests.get(
    #     url='http://localhost:5010/api/videos/filter',
    #     params={
    #         'cat': categories.get('News and Announcements', None),
    #         'latest': 1
    #     }
    # ).json().get('data', [])

    # API: Get the latest videos
    latest = fetch_latest()
    # latest = requests.get(
    #     url='http://localhost:5010/api/videos/filter',
    #     params={
    #         'latest': 9
    #     }
    # ).json().get('data', [])

    return make_response(
        render_template(
            "home.html",
            banners=banners,
            in_progress_videos=updated_list,
            latest_monthly=monthly[0] if monthly else None,
            latest_news=news[0] if news else None,
            latest_videos=latest,
        )
    )
