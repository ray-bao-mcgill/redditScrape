import reddit
import os
from datetime import datetime, timezone, timedelta
import time

# Define the base output directory
output_dir = 'redditScrape/data'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def scrape_subreddit(subreddit_name, start_date, end_date, output_file):
    # Scrape posts from the subreddit
    posts = reddit.fetch_reddit_posts(subreddit_name, start_date, end_date)
    
    # Save posts to CSV
    reddit.save_posts_to_csv(posts, output_file)
    
    print(f"Scraped and saved data for r/{subreddit_name} to {output_file}")

# Calculate dates for the past 2 months
current_date = datetime.now(timezone.utc)
two_months_ago = current_date - timedelta(days=60)

# Define the subreddits and their respective date ranges
subreddits = [

    {
        'name': 'McGill',
        'start_date': two_months_ago,
        'end_date': current_date,
        'output_file': os.path.join(output_dir, 'mcgill_reddit_posts.csv')
    },
    {
        'name': 'UBC',
        'start_date': two_months_ago,
        'end_date': current_date,
        'output_file': os.path.join(output_dir, 'UBC_reddit_posts.csv')
    },
    {
        'name': 'uwaterloo',
        'start_date': two_months_ago,
        'end_date': current_date,
        'output_file': os.path.join(output_dir, 'uwaterloo_reddit_posts.csv')
    },
    {
        'name': 'McMaster',
        'start_date': two_months_ago,
        'end_date': current_date,
        'output_file': os.path.join(output_dir, 'McMaster_reddit_posts.csv')
    },
    {
        'name': 'YorkU',
        'start_date': two_months_ago,
        'end_date': current_date,
        'output_file': os.path.join(output_dir, 'YorkU_reddit_posts.csv')
    },
    {
        'name': 'uAlberta',
        'start_date': two_months_ago,
        'end_date': current_date,
        'output_file': os.path.join(output_dir, 'uAlberta_reddit_posts.csv')
    },
    {
        'name': 'UCalgary',
        'start_date': two_months_ago,
        'end_date': current_date,
        'output_file': os.path.join(output_dir, 'UCalgary_reddit_posts.csv')
    },
    {
        'name': 'uwo',
        'start_date': two_months_ago,
        'end_date': current_date,
        'output_file': os.path.join(output_dir, 'uwo_reddit_posts.csv')
    }
]

# Scrape data for each subreddit
for subreddit in subreddits:
    scrape_subreddit(subreddit['name'], subreddit['start_date'], subreddit['end_date'], subreddit['output_file'])
    time.sleep(100)
