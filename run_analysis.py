import os
from analysis import analyze_reddit_posts

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build paths to data and analyzed_data directories
data_dir = os.path.join(script_dir, 'scraped_data')
analyzed_dir = os.path.join(script_dir, 'analyzed_data')

# Create both directories if they don't exist
os.makedirs(data_dir, exist_ok=True)
os.makedirs(analyzed_dir, exist_ok=True)

analyzed_data = {}

# Loop through all CSV files in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(data_dir, filename)
        output_path = os.path.join(analyzed_dir, filename.replace('.csv', '_analyzed.csv'))
        university_name = filename.replace('_reddit_posts.csv', '')
        
        print(f"Analyzing {university_name}...")
        try:
            # Store the analyzed dataframe in our dictionary and save to file
            df = analyze_reddit_posts(file_path)
            analyzed_data[university_name] = df
            df.to_csv(output_path, index=False)
            print(f"Completed analysis for {university_name}")
        except Exception as e:
            print(f"Error analyzing {university_name}: {e}")

# Now analyzed_data contains all the dataframes, accessed like:
# analyzed_data['uoft'] for University of Toronto data
# analyzed_data['mcgill'] for McGill data, etc.