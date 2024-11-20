import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime, timezone
import time
import csv
import random
from datetime import timedelta

def fetch_reddit_posts(subreddit, start_date, end_date):
    """
    Scrapes Reddit post titles from a specific subreddit that were posted between the start_date and end_date,
    navigating through pages and stopping when posts are older than start_date or newer than end_date.

    :param subreddit: str, name of the subreddit
    :param start_date: datetime, the earliest date for scraping posts (offset-aware)
    :param end_date: datetime, the latest date for scraping posts (offset-aware)
    :return: List of post titles within the date range
    """
    print(f"Starting to scrape r/{subreddit} from {start_date} to {end_date}")
    
    base_url = f"https://old.reddit.com/r/{subreddit}/new"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    post_data = []  # Changed from post_titles to post_data to store both title and date
    next_button_url = None  # URL to store the "next" button link for pagination

    while True:
        # Add a delay before each page request
        time.sleep(random.uniform(0, 1))  # Random delay between 3 to 5 seconds

        # If there is a next button URL, use it, otherwise, start with the base URL
        url = next_button_url if next_button_url else base_url
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
        except requests.RequestException as e:
            print(f"An error occurred while fetching the page: {e}")
            break

        # Check if we've been rate limited
        if response.status_code == 429:
            print("Rate limited. Waiting for 60 seconds before retrying...")
            time.sleep(60)
            continue

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
                        next_link = next_button.find('a')
                        if next_link and isinstance(next_link, Tag):
                            href = next_link.get('href')
                            if isinstance(href, str):
                                next_button_url = href
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
            print(f"Scraping post: {title[:50]}...")  # Added print statement showing first 50 chars of title

            # Extract the post's timestamp
            time_tag = post.find('time')
            if time_tag:
                post_time = datetime.strptime(time_tag['datetime'], '%Y-%m-%dT%H:%M:%S%z')

                # Check if the post is older than the start_date
                if post_time < start_date:
                    print(f"Stopping, found post older than start date: {post_time}")
                    return post_data  # Stop scraping and return collected data

                # Only collect posts within the date range
                if post_time <= end_date:
                    post_data.append((title, post_time))  # Store both title and date

                # Add a small delay after processing each post
                time.sleep(random.uniform(0, 0.2))  # Random delay between 0.5 to 1 second

        # Check if there is a "next" button to navigate to the next page
        next_button = soup.find('span', class_='next-button')
        next_button_url = None
        if next_button:
            next_link = next_button.find('a')
            if next_link and isinstance(next_link, Tag):
                href = next_link.get('href')
                if isinstance(href, str):
                    next_button_url = href
        
        if not next_button_url:
            # If we couldn't find a valid next URL, stop scraping
            break

        # Add a longer delay before moving to the next page
        print(f"Scraping next page... ({url})")  # Added print statement
        time.sleep(random.uniform(0,1))  # Random delay between 5 to 8 seconds

    return post_data

def save_posts_to_csv(posts, output_file):
    """
    Save the scraped posts to a CSV file.

    :param posts: List of tuples containing (title, datetime) of posts
    :param output_file: str, path to the output CSV file
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Date'])  # Write header
        for post in posts:
            writer.writerow([post[0], post[1].isoformat()])

    print(f"Saved {len(posts)} posts to {output_file}")

def parse_date(date_str):
    """
    Parse the date string from Reddit posts.
    """
    now = datetime.now(timezone.utc)
    if 'just now' in date_str:
        return now
    elif 'minute' in date_str or 'hour' in date_str:
        return now.replace(microsecond=0)
    elif 'day' in date_str:
        days = int(date_str.split()[0])
        return (now - timedelta(days=days)).replace(microsecond=0)
    elif 'month' in date_str:
        months = int(date_str.split()[0])
        return (now - timedelta(days=months*30)).replace(microsecond=0)
    elif 'year' in date_str:
        years = int(date_str.split()[0])
        return (now - timedelta(days=years*365)).replace(microsecond=0)
    else:
        return datetime.strptime(date_str, '%b %d %Y').replace(tzinfo=timezone.utc)
