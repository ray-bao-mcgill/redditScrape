import pandas as pd

def compress_data():
    try:
        # Read the cleaned data
        df = pd.read_csv('coded/cleaned_data.csv')
        
        # Convert date column to datetime for proper min/max operations
        df['date'] = pd.to_datetime(df['date'])
        
        # Group by university and calculate means/first/last dates
        compressed_df = df.groupby('uni').agg({
            'sentiment': 'mean',
            't_count': 'mean',
            'cost_of_living': 'first',  # Take first value since it's the same for all rows of same uni
            'date': ['min', 'max']  # Get both first and last dates
        }).reset_index()
        
        # Flatten the multi-level columns created by agg
        compressed_df.columns = ['uni', 'sentiment', 't_count', 'cost_of_living', 'first_date', 'last_date']
        
        # Round the averaged values
        compressed_df['sentiment'] = compressed_df['sentiment'].round(4)
        compressed_df['t_count'] = compressed_df['t_count'].round(4)
        
        # Save compressed data
        compressed_df.to_csv('coded/cleaned_data_compressed.csv', index=False)
        print("Successfully compressed data and saved to coded/cleaned_data_compressed.csv")
        
        # Print summary statistics
        print(f"\nOriginal number of rows: {len(df)}")
        print(f"Compressed number of rows: {len(compressed_df)}")
        print("\nSentiment range:")
        print(f"Min: {compressed_df['sentiment'].min():.4f}")
        print(f"Max: {compressed_df['sentiment'].max():.4f}")
        print(f"Mean: {compressed_df['sentiment'].mean():.4f}")
        
        # Print date range
        print("\nDate ranges:")
        print(f"Earliest: {compressed_df['first_date'].min()}")
        print(f"Latest: {compressed_df['last_date'].max()}")
        
    except FileNotFoundError:
        print("Error: cleaned_data.csv not found in coded directory")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    compress_data()
