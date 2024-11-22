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

# Calculate dates for Oct 21 - Nov 21, 2024
start_date = datetime(2024, 10, 21, tzinfo=timezone.utc)
end_date = datetime(2024, 11, 21, tzinfo=timezone.utc)

# Define subreddits ranked 10-40
subreddits = [
    {
        'name': 'uoft',
        'output_file': os.path.join(output_dir, 'uoft_reddit_posts.csv')
    },
    {
        'name': 'UBC',
        'output_file': os.path.join(output_dir, 'UBC_reddit_posts.csv')
    },
    {
        'name': 'uwaterloo',
        'output_file': os.path.join(output_dir, 'uwaterloo_reddit_posts.csv')
    },
    {
        'name': 'UIUC',
        'output_file': os.path.join(output_dir, 'UIUC_reddit_posts.csv')
    },
    {
        'name': 'UCSD',
        'output_file': os.path.join(output_dir, 'UCSD_reddit_posts.csv')
    },
    {
        'name': 'OSU',
        'output_file': os.path.join(output_dir, 'OSU_reddit_posts.csv')
    },
    {
        'name': 'ucla',
        'output_file': os.path.join(output_dir, 'ucla_reddit_posts.csv')
    },
    {
        'name': 'UTAustin',
        'output_file': os.path.join(output_dir, 'UTAustin_reddit_posts.csv')
    },
    {
        'name': 'ucf',
        'output_file': os.path.join(output_dir, 'ucf_reddit_posts.csv')
    },
    {
        'name': 'nyu',
        'output_file': os.path.join(output_dir, 'nyu_reddit_posts.csv')
    },
    {
        'name': 'Purdue',
        'output_file': os.path.join(output_dir, 'Purdue_reddit_posts.csv')
    },
    {
        'name': 'rutgers',
        'output_file': os.path.join(output_dir, 'rutgers_reddit_posts.csv')
    },
    {
        'name': 'aggies',
        'output_file': os.path.join(output_dir, 'aggies_reddit_posts.csv')
    },
    {
        'name': 'Cornell',
        'output_file': os.path.join(output_dir, 'Cornell_reddit_posts.csv')
    },
    {
        'name': 'mcgill',
        'output_file': os.path.join(output_dir, 'mcgill_reddit_posts.csv')
    },
    {
        'name': 'ASU',
        'output_file': os.path.join(output_dir, 'ASU_reddit_posts.csv')
    },
    {
        'name': 'uofm',
        'output_file': os.path.join(output_dir, 'uofm_reddit_posts.csv')
    },
    {
        'name': 'udub',
        'output_file': os.path.join(output_dir, 'udub_reddit_posts.csv')
    },
    {
        'name': 'USC',
        'output_file': os.path.join(output_dir, 'USC_reddit_posts.csv')
    },
    {
        'name': 'UMD',
        'output_file': os.path.join(output_dir, 'UMD_reddit_posts.csv')
    },
    {
        'name': 'gmu',
        'output_file': os.path.join(output_dir, 'gmu_reddit_posts.csv')
    },
    {
        'name': 'yorku',
        'output_file': os.path.join(output_dir, 'yorku_reddit_posts.csv')
    },
    {
        'name': 'uAlberta',
        'output_file': os.path.join(output_dir, 'uAlberta_reddit_posts.csv')
    },
    {
        'name': 'UCDavis',
        'output_file': os.path.join(output_dir, 'UCDavis_reddit_posts.csv')
    },
    {
        'name': 'VirginiaTech',
        'output_file': os.path.join(output_dir, 'VirginiaTech_reddit_posts.csv')
    },
    {
        'name': 'ufl',
        'output_file': os.path.join(output_dir, 'ufl_reddit_posts.csv')
    },
    {
        'name': 'PennStateUniversity',
        'output_file': os.path.join(output_dir, 'PennStateUniversity_reddit_posts.csv')
    },
    {
        'name': 'Concordia',
        'output_file': os.path.join(output_dir, 'Concordia_reddit_posts.csv')
    },
    {
        'name': 'stanford',
        'output_file': os.path.join(output_dir, 'stanford_reddit_posts.csv')
    },
    {
        'name': 'Harvard',
        'output_file': os.path.join(output_dir, 'Harvard_reddit_posts.csv')
    }
]

# Scrape data for each subreddit
for subreddit in subreddits:
    scrape_subreddit(subreddit['name'], start_date, end_date, subreddit['output_file'])
    time.sleep(100)  # Reduced delay since we're processing fewer subreddits
