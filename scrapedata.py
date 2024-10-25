import reddit
from datetime import datetime, timezone

def scrape_subreddit(subreddit_name, start_date, end_date, output_file):
    # Scrape posts from the subreddit
    posts = reddit.fetch_reddit_posts(subreddit_name, start_date, end_date)
    
    # Save posts to CSV
    reddit.save_posts_to_csv(posts, output_file)
    
    print(f"Scraped and saved data for r/{subreddit_name} to {output_file}")

# Define the subreddits and their respective date ranges
subreddits = [
    {
        'name': 'uoft',
        'start_date': datetime(2024, 10, 1, tzinfo=timezone.utc),
        'end_date': datetime(2024, 10, 15, tzinfo=timezone.utc),
        'output_file': 'uoft_reddit_posts.csv'
    },
    {
        'name': 'McGill',
        'start_date': datetime(2024, 9, 15, tzinfo=timezone.utc),
        'end_date': datetime(2024, 10, 1, tzinfo=timezone.utc),
        'output_file': 'mcgill_reddit_posts.csv'
    }
]

# Scrape data for each subreddit
for subreddit in subreddits:
    scrape_subreddit(subreddit['name'], subreddit['start_date'], subreddit['end_date'], subreddit['output_file'])
