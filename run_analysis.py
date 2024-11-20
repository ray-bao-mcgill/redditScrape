from analysis import analyze_reddit_posts

# Analyze UofT posts
df_uoft = analyze_reddit_posts('data/uoft_reddit_posts.csv') 
df_mcgill = analyze_reddit_posts('data/McGill_reddit_posts.csv') 