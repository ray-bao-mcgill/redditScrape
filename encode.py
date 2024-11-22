import pandas as pd
import glob
import os

def combine_csv_files():
    # Get all CSV files in the analyzed_data directory
    csv_files = glob.glob('analyzed_data/*_reddit_posts_analyzed.csv')
    
    if not csv_files:
        print("No CSV files found in analyzed_data directory")
        return
    
    # Initialize list to store DataFrames
    dfs = []
    
    # Process each CSV file
    for file in csv_files:
        # Extract university name from filename (e.g., "ASU_reddit_posts_analyzed.csv" -> "ASU")
        uni_name = os.path.basename(file).split('_')[0]
        
        # Read CSV
        df = pd.read_csv(file)
        
        # Create new DataFrame with desired structure
        new_df = pd.DataFrame({
            'uni': uni_name,
            'psample': df['Title'],
            'date': df['Date'],
            'sentiment': df['sentiment'],
            't_count': df['target_word_count']
        })
        
        dfs.append(new_df)
    
    # Combine all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Create coded directory if it doesn't exist
    os.makedirs('coded', exist_ok=True)
    
    # Save combined data
    output_path = 'coded/uncleaned_data.csv'
    combined_df.to_csv(output_path, index=False)
    print(f"Combined CSV files saved to {output_path}")
    
    # Clean and encode the data
    # Create a mapping of universities to numeric indices
    universities = combined_df['uni'].unique()
    uni_mapping = {uni: idx + 1 for idx, uni in enumerate(universities)}
    
    # Create a new DataFrame with encoded values
    cleaned_df = pd.DataFrame({
        'uni': combined_df['uni'].map(uni_mapping),
        'psample': range(1, len(combined_df) + 1),  # Generate sequential numbers from 1 to n
        'date': combined_df['date'],
        'sentiment': combined_df['sentiment'],
        't_count': combined_df['t_count']
    })
    
    # Save the mapping for reference
    mapping_df = pd.DataFrame({
        'uni_id': uni_mapping.values(),
        'university': uni_mapping.keys()
    }).sort_values('uni_id')
    
    # Save the cleaned data and mapping
    cleaned_df.to_csv('coded/cleaned_data.csv', index=False)
    mapping_df.to_csv('coded/university_mapping.csv', index=False)
    
    print(f"Cleaned data saved to coded/cleaned_data.csv")
    print(f"University mapping saved to coded/university_mapping.csv")

if __name__ == "__main__":
    combine_csv_files()
