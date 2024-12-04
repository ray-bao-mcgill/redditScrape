import pandas as pd
import os

def save_top_200():
    try:
        # Read the progress file
        df = pd.read_csv('redditScrape/data/subreddit_progress.csv')
        print(f"Found {len(df)} total subreddits")
        
        # Sort by subscriber count in descending order
        df_sorted = df.sort_values('subscribers', ascending=False)
        
        # Take top 200
        top_200 = df_sorted.head(250)
        
        # Save to CSV
        output_path = 'redditScrape/data/top200_universities.csv'
        top_200.to_csv(output_path, index=False)
        
        # Print summary
        print(f"\nSaved top 200 universities to {output_path}")
        print("\nTop 10 universities by subscriber count:")
        for idx, row in top_200.head(10).iterrows():
            print(f"{idx + 1}. r/{row['subreddit']}: {row['subscribers']:,} subscribers - {row['name']}")
            
        print(f"\nSmallest subreddit in top 200: r/{top_200.iloc[-1]['subreddit']} with {top_200.iloc[-1]['subscribers']:,} subscribers")
        
    except FileNotFoundError:
        print("Error: subreddit_progress.csv not found")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    save_top_200()
