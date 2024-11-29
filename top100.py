import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import sys

def get_top_universities():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Read the university mapping from CSV
    try:
        print("Reading university mapping from CSV...")
        uni_df = pd.read_csv('data/university_map.csv')
        print(f"Found {len(uni_df)} universities in mapping file")
    except Exception as e:
        print(f"Error reading university map CSV: {e}")
        return []
    
    # Check for progress file and load existing results
    progress_file = 'data/subreddit_progress.csv'
    try:
        if os.path.exists(progress_file) and os.path.getsize(progress_file) > 0:
            print("Found existing progress, loading...")
            progress_df = pd.read_csv(progress_file)
            subreddits = progress_df.to_dict('records')
            last_processed = len(subreddits)
            print(f"Resuming from university {last_processed + 1}")
        else:
            subreddits = []
            last_processed = 0
            print("Starting from beginning...")
    except Exception as e:
        print(f"Error reading progress file: {e}")
        subreddits = []
        last_processed = 0
        print("Starting from beginning...")
    
    total = len(uni_df)
    
    for idx, row in uni_df.iloc[last_processed:].iterrows():
        name = row['name']
        location = row['location']
        subreddit = row['subreddit']
        print(f"\nChecking {idx + 1}/{total}: {name} (r/{subreddit})")
        
        url = f"https://old.reddit.com/r/{subreddit}"
        print(f"  Requesting {url}...")
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 429:  # Rate limited
                print("\nRate limit reached. Saving progress and exiting...")
                # Save current progress
                progress_df = pd.DataFrame(subreddits)
                progress_df.to_csv(progress_file, index=False)
                sys.exit(1)
                
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                subscribers_div = soup.find('span', {'class': 'number'})
                
                if subscribers_div:
                    subscriber_text = subscribers_div.text
                    subscribers = int(re.sub(r'[^\d]', '', subscriber_text))
                    
                    subreddits.append({
                        'name': name,
                        'location': location,
                        'subreddit': subreddit,
                        'subscribers': subscribers,
                        'cost_of_living': row.get('cost_of_living', None)
                    })
                    print(f"  ✓ Success: {subscribers:,} subscribers")
                    
                    # Save progress after each successful request
                    progress_df = pd.DataFrame(subreddits)
                    progress_df.to_csv(progress_file, index=False)
            else:
                print(f"  × Error: HTTP {response.status_code}")
            
            print("  Waiting 0.2 seconds before next request...")
            time.sleep(0.2)
            
        except Exception as e:
            print(f"  × Error processing: {str(e)}")
            continue
    
    print("\nSorting universities by subscriber count...")
    subreddits.sort(key=lambda x: x['subscribers'], reverse=True)
    
    # Get top 200 and save to CSV
    top_200 = subreddits[:200]
    
    try:
        # Convert to DataFrame and save
        df = pd.DataFrame(top_200)
        output_path = 'data/top200_universities.csv'
        df.to_csv(output_path, index=False)
        print(f"\nSaved top 200 universities to {output_path}")
        
        # Print top 10 for quick verification
        print("\nTop 10 universities by subscriber count:")
        for i, uni in enumerate(top_200[:10], 1):
            print(f"{i}. r/{uni['subreddit']}: {uni['subscribers']:,} subscribers - {uni['name']}")
        
        # Clean up progress file if successful
        if os.path.exists(progress_file):
            os.remove(progress_file)
            
    except Exception as e:
        print(f"\nError saving top 200 CSV: {e}")
    
    return top_200

if __name__ == "__main__":
    get_top_universities()
