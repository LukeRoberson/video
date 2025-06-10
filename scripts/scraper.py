"""
This script uses Selenium to scrape video URLs from a specific webpage.

Collects:
    - The final URL, after redirects
    - A list of downloadable video URLs from a dropdown menu on the page.

Requirements:
    - Selenium
    - BeautifulSoup
    - Chrome WebDriver

Chrome WebDriver enables interaction with the Chrome browser.
    Check the current chrome version: chrome://version//settings/help
    Download the appropriate version of ChromeDriver:
        https://googlechromelabs.github.io/chrome-for-testing/#stable
    Extract to a location and set the DRIVER_PATH variable accordingly.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

DRIVER_PATH = r"D:\python\video\scripts\chrome\chromedriver.exe"

urls = [
    "https://www.jw.org/finder?srcid=jwlshare&wtlocale=E&lank=pub-jwb_201503_1_VIDEO",
    "https://www.jw.org/finder?srcid=jwlshare&wtlocale=E&lank=pub-jwb_201504_1_VIDEO"
]


class JwScraper:
    """
    A class to scrape video URLs from JW.org using Selenium.
    """

    def __init__(
        self,
        driver_path: str = DRIVER_PATH,
        url: list = None,
    ) -> None:
        """
        Initializes the JwScraper with a WebDriver and a list of URLs.

        args:
            driver_path (str): Path to the Chrome WebDriver executable.
            url (str): A single URL to scrape
        """

        # Check we have a URL
        if urls is None:
            raise ValueError("You must provide a URL to scrape.")

        self.url = url

        # Set the driver path
        self.driver_path = driver_path

        # A dictionary to hold the details
        self.details = {
            "final_url": "",
            "1080p": "",
            "720p": "",
            "480p": "",
            "360p": "",
            "240p": ""
        }

    def __enter__(
        self
    ) -> "JwScraper":
        """
        Initializes the WebDriver when entering the context.
        """

        # Setup the Chrome WebDriver
        self.service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=self.service)

        return self

    def __exit__(
        self,
        exc_type: type,
        exc_value: Exception,
        traceback: object
    ) -> None:
        """
        Closes the WebDriver when exiting the context.
        """

        if hasattr(self, 'driver'):
            self.driver.quit()

    def scrape_videos(
        self,
    ) -> list:
        # Open the URL
        self.driver.get(self.url)

        # Get the final URL after any redirects
        final_url = self.driver.current_url
        self.details["url"] = final_url

        # Wait for the dropdown to be present
        wait = WebDriverWait(self.driver, 10)
        dropdown = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "jsDropdownMenu"))
        )

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
        if not dropdown_body:
            print("No dropdownBody found.")
            return []

        # Find all <a> tags with the class 'secondaryButton'
        links = dropdown_body.find_all("a", class_="secondaryButton")

        # Extract the href attributes
        urls = [link["href"] for link in links if "href" in link.attrs]

        # Add to dictionary
        for url in urls:
            if "1080P" in url:
                self.details["url_1080p"] = url
            elif "720P" in url:
                self.details["url_720p"] = url
            elif "480P" in url:
                self.details["url_480p"] = url
            elif "360P" in url:
                self.details["url_360p"] = url
            elif "240P" in url:
                self.details["url_240p"] = url

        # Scrape the video thumbnail (background-image URL)
        try:
            video_poster = self.driver.find_element(
                By.CSS_SELECTOR,
                "#videoPlayerInstance .vjs-poster"
            )
            style_attribute = video_poster.get_attribute("style")
            if "background-image" in style_attribute:
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
            self.details["duration"] = (
                duration_element.text.strip().replace("Duration: ", "")
            )

        except Exception as e:
            print(f"Error scraping duration: {e}")

        # Scrape the video title
        try:
            title_element = self.driver.find_element(
                By.CSS_SELECTOR,
                ".mediaItemTitleContainer .mediaItemTitle"
            )
            self.details["name"] = (
                title_element.text.strip().replace("—", " - ")
            )

        except Exception as e:
            print(f"Error scraping title: {e}")


class CreateCsv:
    """
    A class to create a CSV file from the scraped video details.

    Instantiate, then add details as many times as needed.
    Finally, call `write_to_csv` to save the details to a CSV file.
    """

    def __init__(
        self,
        filename: str = "video_details.csv"
    ) -> None:
        """
        Initializes the CreateCsv class with a filename.
        """

        self.filename = filename
        self.detail_list = []

    def add_details(
        self,
        details: dict
    ) -> None:
        """
        Adds scraped details to the object

        args:
            details (dict): A dictionary containing video details.

        Dictionary keys should include:
            - final_url
            - At least one video URL: 1080p, 720p, 480p, 360p, or 240p
            - thumbnail
            - duration
            - title
        """

        # Check that we have a dictionary
        if not isinstance(details, dict):
            raise ValueError("Details must be a dictionary.")

        # Check that we have the required keys
        required_keys = ['url', 'thumbnail', 'duration', 'name']
        for key in required_keys:
            if (
                key not in details or
                not isinstance(details[key], str) or
                not details[key].strip()
            ):
                raise ValueError(
                    f"Missing or invalid value for '{key}' in details."
                )

        # Check that at least one video URL is present
        video_keys = [
            'url_1080p', 'url_720p', 'url_480p', 'url_360p', 'url_240p'
        ]
        if not any(
            key in details and isinstance(details[key], str) and
            details[key].strip() for key in video_keys
        ):
            raise ValueError(
                "At least one video URL must be provided."
            )

        self.detail_list.append(details)

    def write_to_csv(
        self,
    ) -> None:
        """
        Create a dataframe from the details and write to a CSV file.
        """

        if not self.detail_list:
            raise ValueError("No details to write to CSV.")

        # Create a DataFrame from the list of details
        df = pd.DataFrame(self.detail_list)

        # Add extra columns if they don't exist
        extra_columns = ["category_name", "description", "date_added"]
        for col in extra_columns:
            if col not in df.columns:
                df[col] = ""

        # Update the column order
        column_order = [
            "name", "duration", "category_name", "description", "date_added",
            "url", "thumbnail", "url_1080p", "url_720p", "url_480p",
            "url_360p", "url_240p"
        ]
        column_order = [col for col in column_order if col in df.columns]
        df = df[column_order]

        # Write the DataFrame to a CSV file
        df.to_csv(self.filename, index=False)


full_details = CreateCsv()
for url in urls:
    with JwScraper(url=url) as scraper:
        print(f"Scraping {url}...")
        scraper.scrape_videos()

        full_details.add_details(scraper.details)

print("Writing details to CSV...")
full_details.write_to_csv()
