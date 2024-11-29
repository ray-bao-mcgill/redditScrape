import reddit
import os
from datetime import datetime, timezone, timedelta
import time
import pandas as pd
import json
import sys

# Define the base output directory
output_dir = 'redditScrape/scraped_data'
progress_file = 'redditScrape/data/scraping_progress.json'

# Ensure directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(os.path.dirname(progress_file), exist_ok=True)

def clean_filename(name):
    """Convert university name to a valid filename"""
    # Remove special characters and spaces
    clean = ''.join(c for c in name if c.isalnum() or c in ' -_')
    # Replace spaces with underscores and make lowercase
    return clean.strip().replace(' ', '_').lower()

def load_progress():
    """Load progress from JSON file"""
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading progress file: {e}")
    return {'last_subreddit': 0, 'completed': []}

def save_progress(last_idx, completed):
    """Save progress to JSON file"""
    try:
        with open(progress_file, 'w') as f:
            json.dump({
                'last_subreddit': last_idx,
                'completed': completed
            }, f)
    except Exception as e:
        print(f"Error saving progress: {e}")

def scrape_subreddit(subreddit_name, start_date, end_date, output_file, max_retries=5):
    """Scrape subreddit with retry logic for rate limits"""
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Scrape posts from the subreddit
            posts = reddit.fetch_reddit_posts(subreddit_name, start_date, end_date)
            
            # Save posts to CSV
            reddit.save_posts_to_csv(posts, output_file)
            
            print(f"✓ Scraped and saved data for r/{subreddit_name} to {output_file}")
            return True
            
        except Exception as e:
            if "429" in str(e):  # Rate limit error
                print("\nRate limit reached. Saving progress and exiting...")
                sys.exit(1)
            else:
                print(f"× Error scraping r/{subreddit_name}: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 60 * retry_count
                    print(f"Retrying in {wait_time} seconds... (Attempt {retry_count + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                return False
    
    print(f"× Max retries reached for r/{subreddit_name}")
    return False

def main():
    # Calculate dates for last month
    now = datetime.now(timezone.utc)
    end_date = now
    start_date = end_date - timedelta(days=30)

    print(f"Scraping posts from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    # Load progress
    progress = load_progress()
    last_idx = progress['last_subreddit']
    completed = progress['completed']

    # Read top 100 universities from CSV
    try:
        df = pd.read_csv('redditScrape/data/top100_universities.csv')
        
        subreddits = [
            {
                'name': row['subreddit'],
                'output_file': os.path.join(output_dir, f"{clean_filename(row['name'])}_reddit_posts.csv")
            }
            for _, row in df.iterrows()
        ]
        
        print(f"Loaded {len(subreddits)} subreddits from top 100 universities")
        print(f"Resuming from index {last_idx}")
        
    except Exception as e:
        print(f"Error loading top 100 universities: {e}")
        return

    try:
        # Scrape data for each remaining subreddit
        for idx, subreddit in enumerate(subreddits[last_idx:], last_idx):
            if subreddit['name'] in completed:
                print(f"Skipping completed subreddit: r/{subreddit['name']}")
                continue
                
            print(f"\nProcessing {idx + 1}/{len(subreddits)}: r/{subreddit['name']}")
            success = scrape_subreddit(subreddit['name'], start_date, end_date, subreddit['output_file'])
            
            if success:
                completed.append(subreddit['name'])
                save_progress(idx, completed)
                
                # Delay between successful scrapes
                delay = 100
                print(f"Waiting {delay} seconds before next subreddit...")
                time.sleep(delay)
            else:
                # Save progress but don't mark as completed
                save_progress(idx, completed)

    except KeyboardInterrupt:
        print("\nUser interrupted. Saving progress...")
        save_progress(idx, completed)
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        save_progress(idx, completed)
        sys.exit(1)

    # Clean up progress file when done
    if os.path.exists(progress_file):
        os.remove(progress_file)
        print("\nScraping completed. Progress file cleaned up.")

if __name__ == "__main__":
    main()
