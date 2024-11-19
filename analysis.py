import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji

def analyze_reddit_posts(input_file):
    # Initialize VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Read the CSV file
    df = pd.read_csv(input_file)
    
    def preprocess_text(text):
        # Convert emojis to text description which VADER can better understand
        text = emoji.demojize(str(text))
        # Replace Reddit's /s with text that VADER understands as sarcasm
        text = text.replace(" /s", " [SARCASM]")
        return text
    
    def get_sentiment_score(text):
        # Preprocess the text first
        processed_text = preprocess_text(text)
        # Get just the compound score
        return analyzer.polarity_scores(processed_text)['compound']

    # Apply sentiment analysis to titles
    df['sentiment'] = df['title'].apply(get_sentiment_score)
    
    # Generate output filename based on input filename
    output_file = input_file.replace('.csv', '_with_sentiment.csv')
    
    # Save to new CSV file
    df.to_csv(output_file, index=False)
    print(f"Sentiment analysis complete! Results saved to '{output_file}'")
    
    return df

# Example usage
if __name__ == "__main__":
    # You can easily analyze multiple files by calling the function multiple times
    df_uoft = analyze_reddit_posts('uoft_reddit_posts.csv')
    # For future use with other universities:
    # df_other = analyze_reddit_posts('other_university_posts.csv')
