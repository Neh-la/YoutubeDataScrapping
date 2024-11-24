from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
from bs4 import BeautifulSoup

def format_duration(duration_str):
    # Split the duration string by ":" to extract parts
    parts = duration_str.split(':')
    total_seconds = 0

    # Calculate total seconds based on the number of parts
    if len(parts) == 2:  # MM:SS format
        minutes = int(parts[0])
        seconds = int(parts[1])
        total_seconds = minutes * 60 + seconds
    elif len(parts) == 3:  # HH:MM:SS format
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds

def categorize_duration(seconds):
    if seconds <= 180:
        return "SHORTS"
    elif seconds <= 900:
        return "Mini-Videos"
    elif seconds <= 3600:
        return "Long-Videos"
    else:
        return "Very-Long-Videos"

def format_views(views_str):
    # Remove the word "views" and special characters
    views_str = re.sub(r'views', '', views_str, flags=re.IGNORECASE).strip()
    
    # Check for 'k' or 'M' at the end and convert accordingly
    if views_str.lower().endswith('k'):  # Handle thousands
        return str(int(float(views_str[:-1].replace(',', '')) * 1000))
    elif views_str.lower().endswith('m'):  # Handle millions
        return str(int(float(views_str[:-1].replace(',', '')) * 1000000))
    else:
        # Remove commas and return as is for plain numbers
        return views_str.replace(',', '').strip()

def scroll_to_load_all_videos(driver, timeout=10):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait for new videos to load
        time.sleep(2)

        # Calculate new scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        # Break if no more new content
        if new_height == last_height:
            break

        last_height = new_height

def extract_youtube_data(channel_url):
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize the driver
    driver = webdriver.Chrome(options=options)

    try:
        # Load the channel page
        driver.get(channel_url)

        # Wait for videos to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "ytd-rich-grid-media"))
        )

        # Scroll to load all videos
        scroll_to_load_all_videos(driver)

        # Get the page source after all videos are loaded
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Initialize lists to store data
        videos_data = []

        # Find all video elements
        video_elements = soup.find_all('ytd-rich-grid-media')

        for video in video_elements:
            try:
                # Extract title
                title = video.find('a', id='video-title-link').get('title')

                # Extract duration
                duration = video.find('span', {'class': 'ytd-thumbnail-overlay-time-status-renderer'}).text.strip()

                # Extract views
                views_text = video.find('span', {'class': 'inline-metadata-item style-scope ytd-video-meta-block'}).text.strip()

                # Format the data
                formatted_duration_seconds = format_duration(duration)
                video_category = categorize_duration(formatted_duration_seconds)
                formatted_views = format_views(views_text)

                videos_data.append({
                    'Title': title,
                    'Views': formatted_views,
                    'Duration (Category)': video_category
                })

            except AttributeError as e:
                continue

        return videos_data

    finally:
        driver.quit()

def main():
    channel_url = 'https://www.youtube.com/@meghnerd/videos'

    print("Extracting data from YouTube channel...")
    videos_data = extract_youtube_data(channel_url)

    # Create DataFrame
    df = pd.DataFrame(videos_data)

    # Save to Excel
    output_file = 'Meghnerd_channel_data.xlsx'
    df.to_excel(output_file, index=False)

    # Print the data
    print("\nChannel Video Data:")
    print(df.to_string())
    print(f"\nData has been saved to {output_file}")

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
print("Created files:", ["Meghnerd_channel_data.xlsx"])
