from analysis import analyze_reddit_posts

# Add this
if __name__ == "__main__":
    # Analyze UofT posts
    df_uoft = analyze_reddit_posts('redditScrape/uoft_reddit_posts.csv')
    print("Analysis complete!")