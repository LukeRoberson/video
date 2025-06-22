from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from tqdm import tqdm
from colorama import Fore, Style


CSV_FILE = "difficult_vids.csv"

df = pd.read_csv(CSV_FILE)

errors = []
for idx, row in tqdm(
    df.iterrows(),
    total=len(df),
    desc="Processing videos",
    colour="green"
):
    video_url = row['url']

    # Set up Selenium
    driver = webdriver.Chrome()

    driver.get(video_url)

    # Wait for the video player to load
    wait = WebDriverWait(driver, 10)
    video_div = wait.until(
        EC.presence_of_element_located((By.ID, "vjs_video_3"))
    )

    # Find the play button inside the video player and click it
    play_button = video_div.find_element(By.CLASS_NAME, "vjs-big-play-button")

    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView(true);", play_button)
    time.sleep(1)

    try:
        play_button.click()
    except Exception:
        # Fallback to JS click if normal click fails
        driver.execute_script("arguments[0].click();", play_button)
    # Wait a moment for controls to update
    time.sleep(2)

    # Now find the vjs-progress-holder inside the video player
    progress_holder = video_div.find_element(
        By.CLASS_NAME,
        "vjs-progress-holder"
    )

    # Wait for aria-valuetext to appear (max 10 seconds)
    try:
        wait.until(
            lambda d: (
                progress_holder.get_attribute("aria-valuetext")
                is not None
            )
        )
    except Exception:
        errors.append(video_url)
        print(
            Fore.RED,
            f"Timeout waiting for aria-valuetext on video {video_url}",
            Style.RESET_ALL
        )
        driver.quit()
        continue

    # Get the updated outerHTML and aria-valuetext
    duration = None
    if progress_holder:
        aria_valuetext = progress_holder.get_attribute("aria-valuetext")
        if aria_valuetext is not None:
            duration = aria_valuetext.split(" ")[-1]

    # Get the poster (thumbnail) URL from the video tag
    video_tag = driver.find_element(By.TAG_NAME, "video")
    poster_url = video_tag.get_attribute("poster")

    driver.quit()

    # Update the DataFrame with the duration and thumbnail URL
    df.at[idx, 'duration'] = duration
    df.at[idx, 'thumbnail'] = poster_url

# Save the updated DataFrame back to CSV
if len(errors) > 0:
    print(Fore.YELLOW, "Some videos encountered errors:", Style.RESET_ALL)
df.to_csv(CSV_FILE, index=False)
print(Fore.GREEN, "Processing complete. Updated CSV saved.", Style.RESET_ALL)
