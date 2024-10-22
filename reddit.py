import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import time
import csv

def fetch_reddit_posts(subreddit, start_date, end_date):
    """
    Scrapes Reddit post titles from a specific subreddit that were posted between the start_date and end_date,
    navigating through pages and stopping when posts are older than start_date or newer than end_date.

    :param subreddit: str, name of the subreddit
    :param start_date: datetime, the earliest date for scraping posts (offset-aware)
    :param end_date: datetime, the latest date for scraping posts (offset-aware)
    :return: List of post titles within the date range
    """
    base_url = f"https://old.reddit.com/r/{subreddit}/new"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    post_titles = []
    next_button_url = None  # URL to store the "next" button link for pagination

    while True:
        # If there is a next button URL, use it, otherwise, start with the base URL
        url = next_button_url if next_button_url else base_url
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve posts. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the posts on the current page
        posts = soup.find_all('div', class_='thing')

        # Get the timestamp of the first post (top post)
        if posts:
            first_post_time_tag = posts[0].find('time')
            if first_post_time_tag:
                # Parse the datetime and make sure it is offset-aware
                first_post_time = datetime.strptime(first_post_time_tag['datetime'], '%Y-%m-%dT%H:%M:%S%z')

                # If the first post is newer than the end_date, skip this page
                if first_post_time > end_date:
                    print(f"Skipping page, posts are newer than end date: {first_post_time}")
                    next_button = soup.find('span', class_='next-button')
                    if next_button:
                        next_button_url = next_button.find('a')['href']
                        continue
                    else:
                        break  # No more pages, so stop scraping
                
                # If the first post is older than the start_date, stop scraping
                if first_post_time < start_date:
                    print(f"Stopping, posts are older than start date: {first_post_time}")
                    break

        # Iterate over the posts and extract title and timestamp
        for post in posts:
            title_tag = post.find('a', class_='title may-blank')
            if not title_tag:
                continue
            
            title = title_tag.text

            # Extract the post's timestamp
            time_tag = post.find('time')
            if time_tag:
                post_time = datetime.strptime(time_tag['datetime'], '%Y-%m-%dT%H:%M:%S%z')

                # Only collect posts within the date range
                if start_date <= post_time <= end_date:
                    post_titles.append(title)

        # Check if there is a "next" button to navigate to the next page
        next_button = soup.find('span', class_='next-button')
        if next_button:
            next_button_url = next_button.find('a')['href']
        else:
            # No more pages to navigate through
            break

        # Pause to avoid hitting rate limits
        time.sleep(2)

    return post_titles

def save_posts_to_csv(posts, file_name):
    """
    Saves a list of post titles to a CSV file with an additional 'sentiment' column.

    :param posts: list of str, each containing a post title
    :param file_name: str, name of the CSV file
    """
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'sentiment'])  # Write the header

        # Write each post title with an empty sentiment field
        for title in posts:
            writer.writerow([title, ''])


    