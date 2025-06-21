"""
Module: category_scraper.py

This module provides a class to scrape major video categories
    from JW.org using Selenium.

Classes:
    CategoryScraper: A class to scrape major video categories from JW.org.

Usage:
    with CategoryScraper() as scraper:
        categories = scraper.fetch_major_categories()

Dependencies:
    - selenium: For web scraping with a browser.
    - bs4 (BeautifulSoup): For parsing HTML content.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, Tag
import time
import traceback as tb
import os
import sys
from colorama import Fore, Style
from tqdm import tqdm
import pandas as pd

# Import custom database classes
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)


MAIN_URL = "https://www.jw.org/en/library/videos/#en/home"


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

        self.driver = webdriver.Chrome(options=options)

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
    ) -> list[dict]:
        """
        Fetch major categories from the main JW.org videos page using Selenium.
            1. Loads the main video page with Selenium.
            2. Waits for the JavaScript to load the content.
            3. Parses the page source with BeautifulSoup.
            4. Finds the "Video Categories" section (h2 tag).
            5. Collects all categories listed under this section (h3 tags).

        Returns:
            list: A list of dictionaries representing video categories.
                {
                    'name': str,  # Category name
                    'url': str    # Category URL
                }
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
            return []

        # Collect all <a class="jsNoScroll"> inside <h3> after this <h2>
        categories = []
        for tag in video_cat_h2.find_all_next():
            if isinstance(tag, Tag) and tag.name == 'h3':
                a = tag.find('a', class_='jsNoScroll')
                if isinstance(a, Tag) and a.has_attr('href'):
                    entry = {
                        'name': a.get_text(strip=True),
                        'url': a['href']
                    }
                    categories.append(entry)

            # Optionally, stop if you reach another <h2> (end of section)
            if isinstance(tag, Tag) and tag.name == 'h2':
                if tag.name == 'h2' and tag is not video_cat_h2:
                    break

        return categories

    def fetch_sub_categories(
        self,
        category_url: str
    ) -> list[str]:
        """
        Fetch sub-categories from a given category URL.

        Args:
            category_url (str): The URL of the category to scrape.

        Returns:
            list: A list of subcategory names found on the page.
        """

        # Load the URL, wait for JavaScript to load content, parse
        self.driver.get(category_url)
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        sub_categories = []
        for tag in soup.find_all('h2', class_='sectSynHdg'):
            if isinstance(tag, Tag):
                sub_cat_name = tag.get_text(strip=True)
                sub_categories.append(sub_cat_name)

        return sub_categories

    def fetch_videos(
        self,
        category_url: str,
        category_name: str
    ) -> list[dict]:
        """
        Fetch videos from within a subcategory

        Args:
            category_url (str): The URL of the major category.
                This contains the sub-categories, and videos as a carousel.
            category_name (str): The name of the sub category.
                This is on the page in an <h2> tag.

        Returns:
            list: A list of dictionaries representing sub-categories.
                {
                    'name': str,  # Video name
                    'url': str    # Video URL
                }
        """

        # Load the URL, wait for JavaScript to load content, parse
        self.driver.get(category_url)
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Find the <h2> tag for the sub-category
        sub_cat = soup.find(
            'h2',
            class_='sectSynHdg',
            string=category_name
        )

        videos = []
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
                        videos.append({
                            'name': a.get_text(strip=True),
                            'url': a['href']
                        })

        return videos


if __name__ == "__main__":
    # Store all entries in a list, will be converted to a DataFrame later
    all_rows = []

    # Get the major categories from JW.org
    with CategoryScraper() as scraper:
        print(
            Fore.YELLOW,
            "Fetching major video categories from JW.org...",
            Style.RESET_ALL
        )
        categories = scraper.fetch_major_categories()
        print(
            Fore.YELLOW,
            f"\t{len(categories)} major categories Found.",
            Style.RESET_ALL
        )

    with CategoryScraper() as scraper:
        # Loop through the major categories
        for category in tqdm(categories, desc="Processing categories"):
            try:
                sub_categories = scraper.fetch_sub_categories(category['url'])
                print(
                    Fore.BLUE,
                    f"Major Category: {category['name']}\n",
                    f"{len(sub_categories)} Sub-Categories Found.\n",
                    "-" * 40,
                    Style.RESET_ALL
                )
            except Exception as e:
                print(
                    Fore.RED,
                    f"Error fetching sub-categories for {category['name']}: "
                    f"{e}",
                    Style.RESET_ALL
                )
                continue

            # Loop through the sub-categories to get videos
            for sub_category in tqdm(
                sub_categories,
                desc=f"  Sub-categories of {category['name']}",
                leave=False
            ):
                try:
                    print(
                        Fore.GREEN,
                        f"Sub-Category: {sub_category}",
                        Style.RESET_ALL
                    )
                    video_list = scraper.fetch_videos(
                        category_url=category['url'],
                        category_name=sub_category
                    )

                except Exception as e:
                    print(
                        Fore.RED,
                        f"Error fetching videos for {sub_category}: {e}",
                        Style.RESET_ALL
                    )
                    continue

                # If videos are found, add them to the dictionary
                if video_list:
                    print(
                        Fore.CYAN,
                        f"{len(video_list)} Videos Found in {sub_category}.",
                        Style.RESET_ALL
                    )

                    for video in video_list:
                        all_rows.append(
                            {
                                "major_category": category['name'],
                                "sub_category": sub_category,
                                "video_name": video['name'],
                                "url": video['url']
                            },
                        )

                else:
                    print(
                        Fore.RED,
                        f"No videos found in {sub_category}.",
                        Style.RESET_ALL
                    )

    df = pd.DataFrame(all_rows)
    df.to_csv(
        "jw_videos.csv",
        index=False,
        encoding='utf-8-sig'
    )
