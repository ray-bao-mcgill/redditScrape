import reddit
from datetime import datetime, timezone

#u of t

subreddit_name = 'uoft'

# Define the start and end dates (with timezone awareness, UTC in this case)
start_date = datetime(2024, 9, 15, tzinfo=timezone.utc)  # Earliest date (inclusive, UTC)
end_date = datetime(2024, 10, 1, tzinfo=timezone.utc)   # Latest date (inclusive, UTC)

# Scrape posts from the base URL
posts = reddit.fetch_reddit_posts(subreddit_name, start_date, end_date)

reddit.save_posts_to_csv(posts, 'uoft_reddit_posts.csv')



subreddit_name = 'Mcgill'

# Define the start and end dates (with timezone awareness, UTC in this case)
start_date = datetime(2024, 9, 15, tzinfo=timezone.utc)  # Earliest date (inclusive, UTC)
end_date = datetime(2024, 10, 1, tzinfo=timezone.utc)   # Latest date (inclusive, UTC)

# Scrape posts from the base URL
posts = reddit.fetch_reddit_posts(subreddit_name, start_date, end_date)


reddit.save_posts_to_csv(posts, 'McGill_reddit_posts.csv')