"""
Module: scraper.py

Checks for new videos and categories.

Classes:
    CategoryScraper:
        Scrapes data from JW.org using Selenium.
        This includes major categories, sub-categories, and videos.

    JwScraper:
        Scrapes video metadata from a specific JW.org video URL.

    BuildDb: Builds a DataFrame of categories and videos, and saves them.
        Stores data within the instance of the class; Collates data.
        Can build a dataframe of missing items.
        Can save the data to CSV files.

Usage:
    To get major video categories, use the `fetch_major_categories` method
    of CategoryScraper.
        This supports headless mode, but this is not recommended

    To get sub-categories from a major category, use the `fetch_sub_categories`
        method of CategoryScraper with the category URL.

    To get videos from a sub-category, use the `fetch_videos` method from
        CategoryScraper with the category URL and sub-category name.

    To get video metadata, use the JwScraper class with a specific
        video URL. This will return a dictionary with the video URL, thumbnail,
        duration, and other details.

    The CategoryScraper class is used to get items, but doesn't collate them.
        For this, use the `build_categories` and `build_videos` methods of
        the BuildDb class.

    To save the data to CSV files, use the `save_csv` method of the BuildDb
        class. Optionally use these when instantiating the class to load
        existing data from CSV files, skipping the fetch step.

    Use the `missing` method of BuildDb to check for missing categories
        and videos.

Dependencies:
    - BeautifulSoup: For parsing HTML content.
    - selenium: For interactive web scraping.
    - pandas: For storing data in DataFrames.

Custom dependencies:
    - app.sql_db: For database context management and video/category
        management.

Note:
    Selenium requires a web driver to be installed
        (e.g., ChromeDriver for Chrome).
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup, Tag
import pandas as pd
import yaml

from types import TracebackType
import traceback as tb
import time
from colorama import Fore, Style
from tqdm import tqdm
import os
import sys

# Add the parent directory of 'app' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.sql_db import (    # noqa: E402
    DatabaseContext,
    CategoryManager,
    VideoManager,
)

# Handle script and CSV directory paths
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = os.path.join(script_dir, "csv")
os.makedirs(csv_folder, exist_ok=True)

# The main URL for JW.org videos
MAIN_URL = "https://www.jw.org/en/library/videos/#en/home"

# Path to the Chrome WebDriver executable
# DRIVER_PATH = r"D:\python\video\scripts\chrome\chromedriver.exe"
DRIVER_PATH = r"scripts\chrome\chromedriver.exe"

# Load ignore lists from ignore.yaml if it exists
IGNORE_YAML_PATH = os.path.join(os.path.dirname(__file__), "ignore.yaml")
if os.path.exists(IGNORE_YAML_PATH):
    with open(IGNORE_YAML_PATH, "r", encoding="utf-8") as f:
        ignore_data = yaml.safe_load(f)
        if isinstance(ignore_data, dict):
            IGNORE_CATEGORIES = ignore_data.get("categories", [])
            IGNORE_SUB_CATEGORIES = ignore_data.get("subcategories", [])
            IGNORE_VIDEOS = ignore_data.get("videos", [])


class CategoryScraper:
    """
    A class to scrape major video categories from JW.org using Selenium.

    Args:
        url (str): The URL of the JW.org videos page.
        headless (bool): Whether to run the browser in headless mode.
    """

    def __init__(
        self,
        url=MAIN_URL,
        headless: bool = False,
        suppress_warnings: bool = True
    ) -> None:
        """
        Initialize the CategoryScraper with a URL.
        This is the main video page of JW.org.

        Args:
            url (str): The URL to scrape categories from.
            headless (bool): Whether to run the browser in headless mode.
            suppress_warnings (bool): Whether to suppress Selenium warnings.

        Returns:
            None
        """

        self.url = url
        self.headless = headless
        self.suppress_warnings = suppress_warnings

    def __enter__(
        self
    ) -> 'CategoryScraper':
        """
        Initialize the scraper by setting up the Selenium driver.
        """

        options = Options()

        # This enables the use of Chrome in headless mode (no GUI)
        if self.headless:
            options.add_argument("--headless")

        # This suppresses warnings from Selenium
        if self.suppress_warnings:
            options.add_argument("--log-level=3")

        try:
            self.driver = webdriver.Chrome(options=options)

        except Exception as e:
            if (
                "This version of ChromeDriver only supports Chrome version"
                in str(e)
            ):
                print(
                    f"{Fore.RED}ChromeDriver version mismatch detected!\n"
                    f"{Fore.YELLOW}Please update ChromeDriver to match your "
                    f"Chrome browser version.\n"
                    f"You can download the correct version from:\n"
                    f"https://googlechromelabs.github.io/chrome-for-testing/",
                    Style.RESET_ALL,
                    f"\n\nError details: {str(e)}"
                )
            else:
                print(
                    Fore.RED,
                    f"Failed to initialize Chrome WebDriver: {str(e)}",
                    Style.RESET_ALL
                )

            # Exit the script gracefully
            sys.exit(1)

            # Exit the script gracefully
            sys.exit(1)

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        """
        Clean up the Selenium driver.
        """
        if exc_type is not None:
            print("Exception occurred in CategoryScraper context manager:")
            tb.print_exception(exc_type, exc_value, traceback)

        self.driver.quit()

    def fetch_major_categories(
        self
    ) -> pd.DataFrame:
        """
        Fetch major categories from the main JW.org videos page using Selenium.
            1. Loads the main video page with Selenium.
            2. Waits for the JavaScript to load the content.
            3. Parses the page source with BeautifulSoup.
            4. Finds the "Video Categories" section (h2 tag).
            5. Collects all categories listed under this section (h3 tags).

        Returns:
            pd.DataFrame: A DataFrame containing the major categories.
                Each row contains:
                    - 'name': The name of the category.
                    - 'url': The URL of the category.
                    - 'exist':
                        A boolean indicating if the category exists in the DB
        """

        # Load the URL, wait for JavaScript to load content, parse
        self.driver.get(MAIN_URL)
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Find the <h2> tag for "Video Categories"
        video_cat_h2 = soup.find(
            'h2',
            class_='sectSynHdg',
            string='Video Categories'
        )
        if not video_cat_h2:
            print("Could not find the 'Video Categories' heading.")
            return pd.DataFrame()

        # Use a pandas dataframe
        df = pd.DataFrame(columns=['name', 'url', 'exist'])

        # Collect all <a class="jsNoScroll"> inside <h3> after this <h2>
        for tag in video_cat_h2.find_all_next():
            if isinstance(tag, Tag) and tag.name == 'h3':
                a = tag.find('a', class_='jsNoScroll')
                if a:
                    name = a.get_text(strip=True)
                else:
                    continue
                if name in IGNORE_CATEGORIES:
                    continue

                # Create a dataframe row for the category
                if isinstance(a, Tag) and a.has_attr('href'):
                    with DatabaseContext() as db:
                        category_manager = CategoryManager(db)
                        exists = category_manager.name_to_id(name)

                    df.loc[len(df)] = [
                        name,
                        a['href'],
                        True if exists else False,
                    ]

            # Optionally, stop if you reach another <h2> (end of section)
            if isinstance(tag, Tag) and tag.name == 'h2':
                if tag.name == 'h2' and tag is not video_cat_h2:
                    break

        return df

    def fetch_sub_categories(
        self,
        category_url: str,
        category_name: str,
    ) -> pd.DataFrame:
        """
        Fetch sub-categories from a given category URL.

        Args:
            category_url (str): The URL of the category to scrape.
            category_name (str): The name of the category.

        Returns:
            pd.DataFrame: A DataFrame containing sub-categories.
                Each row contains:
                    - 'name': The name of the sub-category.
                    - 'main_category': The name of the main category.
                    - 'main_cat_url': The URL of the main category.
                    - 'exist':
                        A boolean showing if the sub-category exists in the DB
        """

        # Load the URL, wait for JavaScript to load content, parse
        self.driver.get(category_url)
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Dataframe to store sub-categories (no URL for sub-categories)
        df = pd.DataFrame(
            columns=['name', 'main_category', 'main_cat_url', 'exist']
        )

        for tag in soup.find_all('h2', class_='sectSynHdg'):
            if isinstance(tag, Tag):
                # Get the sub-category name
                name = tag.get_text(strip=True)
                if name in IGNORE_SUB_CATEGORIES:
                    continue

                # Check if it exists in the database
                with DatabaseContext() as db:
                    category_manager = CategoryManager(db)

                    # Check if the sub-category exists in the database
                    exists = category_manager.name_to_id(name)

                # Add the sub-category to the DataFrame
                df.loc[len(df)] = [
                    name,
                    category_name,
                    category_url,
                    True if exists else False,
                ]

        return df

    def fetch_videos(
        self,
        main_cat_url: str,
        sub_cat_name: str,
        main_cat_name: str,
        ignore_cats: bool = False,
    ) -> pd.DataFrame:
        """
        Fetch videos from within a subcategory

        Args:
            main_cat_url (str): The URL of the major category.
                This contains the sub-categories, and videos as a carousel.
            sub_cat_name (str): The name of the sub category.
                This is on the page in an <h2> tag.
            main_cat_name (str): The name of the main category.
            ignore_cats (bool): If True, ignore video category check.
                Needed to find videos in 'latest videos' category.

        Returns:
            pd.DataFrame: A DataFrame containing video information.
                Each row contains:
                    - 'video_name': The name of the video.
                    - 'video_url': The URL of the video.
                    - 'exist': A boolean showing if the video exists in the DB
        """

        try:
            # Load the URL, wait for JavaScript to load content, parse
            self.driver.get(main_cat_url)
            time.sleep(5)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Find the <h2> tag for the sub-category
            sub_cat = soup.find(
                'h2',
                class_='sectSynHdg',
                string=sub_cat_name
            )
        except Exception as e:
            print(
                Fore.RED,
                f"Error fetching videos for {sub_cat_name}: {e}",
                Style.RESET_ALL
            )
            return pd.DataFrame()

        # Create a DataFrame to store video information
        df = pd.DataFrame(
            columns=[
                'video_name',
                'video_url',
                'main_cat_name',
                'sub_cat_name',
                'exist'
            ]
        )

        # Iterate over elements after the subcategory <h2>
        if isinstance(sub_cat, Tag):
            for tag in sub_cat.find_all_next():
                # Stop if we reach another <h2> (next subcategory)
                if isinstance(tag, Tag) and tag.name == 'h2':
                    break

                # Look for <h3> tags with <a>
                if isinstance(tag, Tag) and tag.name == 'h3':
                    a = tag.find('a', class_='jsNoScroll')
                    if isinstance(a, Tag) and a.has_attr('href'):
                        video_name = a.get_text(strip=True)

                        if 'categories' in a['href']:
                            # Skip if the link is to a category, not a video
                            continue

                        # Check if the video exists in the database
                        with DatabaseContext() as db:
                            cat_mgr = CategoryManager(db)
                            video_manager = VideoManager(db)
                            exists = video_manager.name_to_id(
                                video_name
                            )

                            # Get the categories for the video
                            if exists and ignore_cats is False:
                                categories = cat_mgr.get_from_video(
                                    video_id=exists
                                )

                                # Check if the main and sub categories exist
                                #   on this video (video may exist, but be in
                                #   new categories)
                                if categories:
                                    if main_cat_name not in [
                                        cat['name'] for cat in categories
                                    ]:
                                        exists = False
                                    elif sub_cat_name not in [
                                        cat['name'] for cat in categories
                                    ]:
                                        exists = False

                        df.loc[len(df)] = [
                            video_name,
                            a['href'],
                            main_cat_name,
                            sub_cat_name,
                            True if exists else False,
                        ]

        return df


class JwScraper:
    """
    A class to scrape a video URL from JW.org using Selenium.

    Gets the video URL, thumbnail, duration, and other details.

    Args:
        url (str): The URL of the JW.org video page to scrape.
    """

    def __init__(
        self,
        url: str,
        driver_path: str = DRIVER_PATH,
    ) -> None:
        """
        Initializes the JwScraper with a WebDriver and a list of URLs.

        args:
            driver_path (str): Path to the Chrome WebDriver executable.
            url (str): A single URL to scrape
        """

        self.url = url
        self.driver_path = driver_path
        self.details = {}

    def __enter__(
        self
    ) -> "JwScraper":
        """
        Initializes the WebDriver when entering the context.

        Args:
            None

        Returns:
            JwScraper: The instance of the JwScraper class.
        """

        # Setup the Chrome WebDriver
        try:
            self.service = Service(self.driver_path)
            self.driver = webdriver.Chrome(service=self.service)

        except Exception as e:
            if (
                "This version of ChromeDriver only supports Chrome version"
                in str(e)
            ):
                print(
                    f"{Fore.RED}ChromeDriver version mismatch detected!\n"
                    f"{Fore.YELLOW}Please update ChromeDriver to match your "
                    f"Chrome browser version.\n"
                    f"You can download the correct version from:\n"
                    f"https://googlechromelabs.github.io/chrome-for-testing/",
                    Style.RESET_ALL,
                    f"\n\nError details: {str(e)}"
                )
            else:
                print(
                    Fore.RED,
                    f"Failed to initialize Chrome WebDriver: {str(e)}",
                    Style.RESET_ALL
                )

            # Exit the script gracefully
            sys.exit(1)

        return self

    def __exit__(
        self,
        exc_type: type,
        exc_value: Exception,
        traceback: TracebackType | None
    ) -> None:
        """
        Closes the WebDriver when exiting the context.

        Args:
            exc_type (type): The type of the exception raised, if any.
            exc_value (Exception): The exception instance, if any.
            traceback (object): The traceback object, if any.

        Returns:
            None
        """

        if hasattr(self, 'driver'):
            self.driver.quit()

        if exc_type is not None:
            print("Exception occurred in JwScraper context manager:")
            tb.print_exception(exc_type, exc_value, traceback)

    def scrape_vids(
        self,
    ) -> None:
        """
        Scrapes the video page for URLs, thumbnail, and duration.

        This method performs the following steps:
            1. Opens the video URL.
            2. Waits for the dropdown menu to be present.
            3. Clicks the dropdown to expand it.
            4. Waits for the dropdown body to load.
            5. Parses the page source with BeautifulSoup.
            6. Finds the dropdown body and extracts all <a> tags with
                the class 'secondaryButton'.
            7. Extracts the href attributes from these <a> tags.
            8. Adds the URLs to the details dictionary based on resolution.
            9. Scrapes the video thumbnail (background-image URL).
            10. Scrapes the video duration.
            11. Scrapes the div with id="regionMain" for an <article> tag.
            12. Searches the article for an <h1> tag and adds its text to
                the details dictionary.

        Args:
            None

        Returns:
            None
        """

        # Open the URL
        self.driver.get(self.url)

        # Get the final URL after any redirects
        final_url = self.driver.current_url
        self.details["url"] = final_url

        # Wait for the dropdown to be present
        wait = WebDriverWait(self.driver, 10)
        try:
            dropdown = wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "jsDropdownMenu")
                )
            )
        except Exception as e:
            print(f"Error locating dropdown menu: {e}")
            return

        # Scroll the element into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", dropdown
        )

        # Click the dropdown to expand it
        dropdown.click()

        # Wait for the dropdownBody to load
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "dropdownBody"))
        )

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # Find the dropdownBody div
        dropdown_body = soup.find("div", class_="dropdownBody")
        if not isinstance(dropdown_body, Tag):
            print("No valid dropdownBody found.")
            return

        # Find all <a> tags with the class 'secondaryButton'
        links = dropdown_body.find_all("a", class_="secondaryButton")

        # Extract the href attributes
        urls = [
            link["href"]
            for link in links
            if isinstance(link, Tag) and "href" in link.attrs
        ]

        # Add to dictionary
        for url in urls:
            if "1080P" in url:
                self.details["url_1080"] = url
            elif "720P" in url:
                self.details["url_720"] = url
            elif "480P" in url:
                self.details["url_480"] = url
            elif "360P" in url:
                self.details["url_360"] = url
            elif "240P" in url:
                self.details["url_240"] = url

        # Scrape the video thumbnail (background-image URL)
        try:
            video_poster = self.driver.find_element(
                By.CSS_SELECTOR,
                "#videoPlayerInstance .vjs-poster"
            )
            style_attribute = video_poster.get_attribute("style")
            if style_attribute and "background-image" in style_attribute:
                # Extract the URL from the style attribute
                start = style_attribute.find("url(") + 4
                end = style_attribute.find(")", start)
                thumbnail_url = (
                    style_attribute[start:end].strip('"').strip("'")
                )
                self.details["thumbnail"] = thumbnail_url

        except Exception as e:
            print(f"Error scraping thumbnail: {e}")

        # Scrape the video duration
        try:
            duration_element = self.driver.find_element(
                By.CSS_SELECTOR,
                ".mediaItemTitleContainer .mediaItemDuration"
            )
            print(f"Duration element found: {duration_element}")
            self.details["duration"] = (
                duration_element.text.strip().replace("Duration: ", "")
            )

        except Exception as e:
            print(f"Error scraping duration: {e}")

        # Scrape the div with id="regionMain"
        try:
            region_main = self.driver.find_element(By.ID, "regionMain")
        except Exception as e:
            print(f"Error scraping regionMain: {e}")

        # Search region_main for an <article> tag with id="article"
        region_main = None
        article_element = None
        try:
            if region_main:
                article_element = region_main.find_element(
                    By.CSS_SELECTOR,
                    "article#article"
                )
        except Exception as e:
            print(f"Error finding article tag: {e}")

        # Search article_element for an <h1> tag
        h1_element = None
        try:
            if article_element:
                h1_element = article_element.find_element(By.TAG_NAME, "h1")
            if h1_element:
                print(f"Found <h1> tag: {h1_element.text}")
                self.details["name"] = h1_element.text
        except Exception as e:
            print(f"Error finding <h1> tag in article: {e}")


class BuildDb:
    """
    Build a dataframe of categories and videos
    """

    def __init__(
        self,
        major_cat_filename: str = "",
        sub_cat_filename: str = "",
        videos_filename: str = ""
    ) -> None:
        """
        Initialize the BuildDb class.

        Optionally takes a filename to load existing data from a CSV file.

        Args:
            filename (str): The name of the CSV file to load data from.

        Returns:
            None
        """

        # Load existing data from CSV files if provided
        if major_cat_filename != "":
            self.major_categories = pd.read_csv(
                os.path.join(csv_folder, major_cat_filename)
            )
            self.major_loaded = True
        else:
            self.major_categories = pd.DataFrame()
            self.major_loaded = False

        if sub_cat_filename != "":
            self.sub_categories = pd.read_csv(
                os.path.join(csv_folder, sub_cat_filename)
            )
            self.sub_loaded = True
        else:
            self.sub_categories = pd.DataFrame()
            self.sub_loaded = False

        if videos_filename != "":
            self.videos = pd.read_csv(
                os.path.join(csv_folder, videos_filename)
            )
            self.video_loaded = True
        else:
            self.videos = pd.DataFrame()
            self.video_loaded = False

    def build_categories(
        self,
    ) -> None:
        """
        Build the DataFrame of categories.

        Args:
            None

        Returns:
            None
        """

        if not self.major_categories.empty:
            print(
                Fore.GREEN,
                "Major categories loaded from file, skipping fetch.",
                Style.RESET_ALL
            )

        else:
            # Get the major categories from JW.org
            print(
                Fore.YELLOW,
                "Fetching major categories from JW.org...",
                Style.RESET_ALL
            )
            with CategoryScraper(headless=False) as scraper:
                self.major_categories = scraper.fetch_major_categories()
                print(
                    Fore.GREEN,
                    f"{len(self.major_categories)} major categories found.",
                    Style.RESET_ALL
                )

        if not self.sub_categories.empty:
            print(
                Fore.GREEN,
                "Subcategories loaded from file, skipping fetch.",
                Style.RESET_ALL
            )
            return

        # Get sub-categories from a specific category
        for _, row in (tqdm(
            self.major_categories.iterrows(),
            desc="Fetching sub-categories",
            total=len(self.major_categories),
            colour='blue',
            leave=True,
            dynamic_ncols=True,
        )):
            print(
                Fore.YELLOW,
                f"Fetching sub categories for {row['name']}...",
                Style.RESET_ALL
            )
            with CategoryScraper(headless=False) as scraper:
                sub_category = scraper.fetch_sub_categories(
                    row['url'],
                    row['name']
                )

            self.sub_categories = pd.concat(
                [self.sub_categories, sub_category],
                ignore_index=True
            )

    def build_videos(
        self,
    ) -> None:
        """
        Build the DataFrame of videos.

        Args:
            None

        Returns:
            None
        """

        if not self.videos.empty:
            print(
                Fore.YELLOW,
                "Videos loaded from file, checking for new videos...",
                Style.RESET_ALL
            )

        # Get videos from a specific sub-category
        for _, row in tqdm(
            self.sub_categories.iterrows(),
            desc="Fetching videos",
            total=len(self.sub_categories),
            colour='green',
            leave=True,
            dynamic_ncols=True,
        ):
            print(
                Fore.YELLOW,
                f"Fetching videos for {row['name']}...",
                Style.RESET_ALL
            )
            with CategoryScraper(headless=False) as scraper:
                videos = scraper.fetch_videos(
                    main_cat_url=row['main_cat_url'],
                    sub_cat_name=row['name'],
                    main_cat_name=row['main_category'],
                )

            # Only add videos that don't already exist in the DataFrame
            if not self.videos.empty:
                # Filter out videos that already exist
                new_videos = videos[
                    ~videos['video_url'].isin(self.videos['video_url'])
                ]
                if not new_videos.empty:
                    print(
                        Fore.GREEN,
                        f"Found {len(new_videos)} new videos in {row['name']}",
                        Style.RESET_ALL
                    )
                    self.videos = pd.concat(
                        [self.videos, new_videos],
                        ignore_index=True
                    )
            else:
                self.videos = pd.concat(
                    [self.videos, videos],
                    ignore_index=True
                )

    def build_latest(
        self,
        filename: str,
    ) -> None:
        """
        Build a DataFrame and CSV of latest videos only.

        This looks at the 'latest videos' category.

        Args:
            filename (str): The name of the CSV file to save the latest videos.

        Returns:
            None
        """

        with CategoryScraper(headless=False) as scraper:
            videos = scraper.fetch_videos(
                main_cat_url=MAIN_URL,
                sub_cat_name="Latest Videos",
                main_cat_name="Latest Videos",
                ignore_cats=True,
            )

            self.videos = pd.concat(
                [self.videos, videos],
                ignore_index=True
            )

            video_path = os.path.join(csv_folder, filename)
            videos.to_csv(
                video_path,
                index=False,
                encoding='utf-8'
            )
            print(
                Fore.GREEN,
                f"Saving {len(videos)} videos to {video_path}...",
                Style.RESET_ALL
            )

    def save_csv(
        self,
        major_cat_filename: str = "major_categories.csv",
        sub_cat_filename: str = "sub_categories.csv",
        videos_filename: str = "videos.csv",
    ) -> None:
        """
        Save the videos DataFrame to a CSV file.

        Args:
            major_cat_filename (str): The filename for major categories.
            sub_cat_filename (str): The filename for sub-categories.
            videos_filename (str): The filename for videos.

        Returns:
            None
        """

        # Handle major categories
        if self.major_loaded:
            print(
                Fore.YELLOW,
                "Major categories already loaded, skipping save.",
                Style.RESET_ALL
            )

        elif self.major_categories.empty:
            print(
                Fore.RED,
                "No major categories to save.",
                Style.RESET_ALL
            )

        else:
            major_cat_path = os.path.join(csv_folder, major_cat_filename)
            self.major_categories.to_csv(
                major_cat_path,
                index=False,
                encoding='utf-8'
            )
            print(
                Fore.GREEN,
                f"Major categories saved to: {major_cat_filename}",
                Style.RESET_ALL
            )

        # Handle sub-categories
        if self.sub_loaded:
            print(
                Fore.YELLOW,
                "Sub-categories already loaded, skipping save.",
                Style.RESET_ALL
            )

        elif self.sub_categories.empty:
            print(
                Fore.RED,
                "No sub-categories to save.",
                Style.RESET_ALL
            )

        else:
            sub_cat_path = os.path.join(csv_folder, sub_cat_filename)
            self.sub_categories.to_csv(
                sub_cat_path,
                index=False,
                encoding='utf-8'
            )
            print(
                Fore.GREEN,
                f"Sub-categories saved to: {sub_cat_filename}",
                Style.RESET_ALL
            )

        # Handle videos
        if self.video_loaded:
            print(
                Fore.YELLOW,
                "Videos already loaded, skipping save.",
                Style.RESET_ALL
            )

        elif self.videos.empty:
            print(
                Fore.RED,
                "No videos to save.",
                Style.RESET_ALL
            )

        else:
            video_path = os.path.join(csv_folder, videos_filename)
            self.videos.to_csv(
                video_path,
                index=False,
                encoding='utf-8'
            )
            print(
                Fore.GREEN,
                f"Saving {len(self.videos)} videos to {videos_filename}...",
                Style.RESET_ALL
            )

    def missing(
        self,
    ) -> None:
        """
        Check for missing categories and videos.

        Args:
            None

        Returns:
            None
        """

        print(
            Fore.YELLOW,
            "Checking for missing categories and videos...",
            Style.RESET_ALL
        )

        # Validate videos in DB
        with DatabaseContext() as db:
            video_manager = VideoManager(db)
            update = False

            for idx, row in self.videos.iterrows():
                if not row['exist']:
                    exists = video_manager.name_to_id(row['video_name'])
                    if exists:
                        update = True
                        self.videos.at[idx, 'exist'] = True
                        print(
                            Fore.GREEN,
                            f"Video found in DB: {row['video_name']}",
                            Style.RESET_ALL)

                    else:
                        print(
                            Fore.RED,
                            f"Missing video: {row['video_name']}",
                            Style.RESET_ALL
                        )

            # Save the videos DataFrame to CSV after updating 'exist' status
        if update:
            video_path = os.path.join(csv_folder, "videos.csv")
            self.videos.to_csv(
                video_path,
                index=False,
                encoding='utf-8'
            )
            print(
                Fore.GREEN,
                f"Updated videos saved to: {video_path}",
                Style.RESET_ALL
            )

        # Collate information about missing items into DataFrames
        missing_major = self.major_categories[~self.major_categories['exist']]
        missing_sub = self.sub_categories[~self.sub_categories['exist']]
        missing_videos = self.videos[~self.videos['exist']]

        print("Total videos:", len(self.videos))
        print(
            "Videos with exist=True:",
            len(self.videos[self.videos['exist']])
        )
        print("Videos with exist=False:", len(missing_videos))

        # Remove videos in IGNORE_VIDEOS from missing_videos
        missing_videos = missing_videos[
            ~missing_videos['video_name'].isin(IGNORE_VIDEOS)
        ]

        # Print missing categories
        if not missing_major.empty:
            print(
                Fore.RED,
                "Missing major categories:",
                Style.RESET_ALL
            )
            print(missing_major)
        else:
            print(
                Fore.GREEN,
                "All major categories are present.",
                Style.RESET_ALL
            )

        # Print missing sub-categories
        if not missing_sub.empty:
            print(
                Fore.RED,
                "Missing sub-categories:",
                Style.RESET_ALL
            )
            print(missing_sub)
        else:
            print(
                Fore.GREEN,
                "All sub-categories are present.",
                Style.RESET_ALL
            )

        # Print missing videos
        if not missing_videos.empty:
            print(
                Fore.RED,
                "Missing videos:",
                Style.RESET_ALL
            )
            print(missing_videos)
        else:
            print(
                Fore.GREEN,
                "All videos are present.",
                Style.RESET_ALL
            )

        # Save missing items to the instance variables
        missing_videos = missing_videos.drop(columns=['exist'])
        self.missing_videos = missing_videos

    def metadata(
        self,
    ) -> None:
        """
        Collect additional metadata about the videos.

        Args:
            None

        Returns:
            None
        """

        # Add a new columns to the dataframe
        self.missing_videos['url_1080'] = None
        self.missing_videos['url_720'] = None
        self.missing_videos['url_480'] = None
        self.missing_videos['url_360'] = None
        self.missing_videos['url_240'] = None
        self.missing_videos['thumbnail'] = None
        self.missing_videos['duration'] = None

        # Iterate over the missing videos and scrape metadata
        for video in tqdm(
            self.missing_videos.iterrows(),
            desc="Scraping video metadata",
            total=len(self.missing_videos),
            colour='magenta',
            leave=True,
            dynamic_ncols=True,
        ):
            _, row = video
            video_url = row['video_url']
            with JwScraper(video_url) as scraper:
                scraper.scrape_vids()
                url_1080 = scraper.details.get('url_1080', None)
                url_720 = scraper.details.get('url_720', None)
                url_480 = scraper.details.get('url_480', None)
                url_360 = scraper.details.get('url_360', None)
                url_240 = scraper.details.get('url_240', None)
                thumbnail = scraper.details.get('thumbnail', None)
                duration = scraper.details.get('duration', None)

                # Update the missing_videos DataFrame with the scraped data
                self.missing_videos.loc[
                    self.missing_videos['video_url'] == video_url,
                    ['url_1080', 'url_720', 'url_480', 'url_360', 'url_240',
                     'thumbnail', 'duration']
                ] = [
                    url_1080, url_720, url_480, url_360, url_240,
                    thumbnail, duration
                ]

        try:
            meta_path = os.path.join(csv_folder, "missing_videos.csv")
            self.missing_videos.to_csv(
                meta_path,
                index=False,
                encoding='utf-8'
            )
            print(
                Fore.GREEN,
                "Missing videos metadata saved to: missing_videos.csv",
                Style.RESET_ALL
            )

        except Exception as e:
            print(
                Fore.RED,
                f"Error saving missing videos to CSV: {e}",
                Style.RESET_ALL
            )


if __name__ == "__main__":
    """
    This script finds new videos and categories on JW.org.

    1. Find if the CSV files already exist.
    2. Instantiate the BuildDb class with the filenames
        Providing filenames will load existing data, skipping the fetch
        which is time consuming.
    3. Build the categories and videos DataFrames.
        Will be skipped if the DataFrames already exist.
        Also checks if these items are already in the database.
    4. Save the DataFrames to CSV files.
        For optional later use
    5. Check for missing categories and videos.
        Collate information about missing items into DataFrames.
    6. Collect metadata for missing videos.
        Scrape the video URLs, thumbnail, duration, etc.
        Saves this to a CSV file named "missing_videos.csv".

    If 'latest_only' is set to True, it will only fetch the latest videos
        from the "Latest Videos" category, skipping the full categories
        and videos.
    Note, this will not check for the categories these videos are in,
        so there is some manual intervention needed to add these
        videos to the database.
    """

    # Set to true to fetch only the latest videos
    latest_only = True

    # Check if the CSV files already exist
    major_cat_filename = "major_categories.csv" if os.path.exists(
        os.path.join(csv_folder, 'major_categories.csv')
    ) else ""

    sub_cat_filename = "sub_categories.csv" if os.path.exists(
        os.path.join(csv_folder, 'sub_categories.csv')
    ) else ""

    videos_filename = "videos.csv" if os.path.exists(
        os.path.join(csv_folder, 'videos.csv')
    ) else ""

    # Instantiate the BuildDb class with the filenames
    db = BuildDb(
        major_cat_filename=major_cat_filename,
        sub_cat_filename=sub_cat_filename,
        videos_filename=videos_filename,
    )

    if latest_only:
        print(
            Fore.YELLOW,
            "Fetching latest videos only...",
            Style.RESET_ALL
        )

        # Build latest videos only
        db.build_latest(
            filename="latest_videos.csv",
        )

    else:
        print(
            Fore.YELLOW,
            "Fetching all videos...",
            Style.RESET_ALL
        )

        # Get full categories and videos
        db.build_categories()
        db.build_videos()
        db.save_csv()

    # Collate information about missing items
    db.missing()

    # Collect metadata for missing videos
    db.metadata()
