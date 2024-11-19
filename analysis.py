import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
import re

def analyze_reddit_posts(input_file):
    # Initialize VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Read the CSV file
    df = pd.read_csv(input_file)
    
    def preprocess_text(text):
        # Handle None or empty text
        if not text or pd.isna(text):
            return ""
        
        # Convert emojis to their text description
        text = emoji.demojize(text)
        
        # Academic stress indicators
        text = re.sub(r"(?i)help+[p]*", "need assistance", text)  # Strengthen help requests
        text = re.sub(r"(?i)anyone (know|have|taking)", "seeking information about", text)
        text = re.sub(r"(?i)burnt? out", "completely exhausted and overwhelmed", text)
        text = re.sub(r"(?i)struggling with", "having severe difficulty with", text)
        
        # Question neutralizing
        text = re.sub(r"(?i)what (is|are) the best", "what are some", text)  # Reduce false positives
        text = re.sub(r"(?i)how (to|do I|can I) get", "what is the process for", text)
        
        # UofT specific terms
        text = re.sub(r"(?i)bird course", "easy course", text)
        text = re.sub(r"(?i)cooked", "doomed", text)
        
        # Common abbreviations
        text = text.replace("pls", "please")
        text = text.replace("rn", "right now")
        text = text.replace("gc", "group chat")

        # Stress indicators
        text = re.sub(r"(?i)can'?t (handle|manage|do)", "completely unable to handle", text)
        
        return text.strip()
    
    def get_sentiment_score(text):
        # Missing error handling for None or empty text
        if not text or pd.isna(text):
            return 0
        processed_text = preprocess_text(text)
        
        # Handle case where preprocessing returns empty string
        if not processed_text:
            return 0
            
        return analyzer.polarity_scores(processed_text)['compound']

    # Apply sentiment analysis to titles
    df['sentiment'] = df['title'].apply(get_sentiment_score)
    
    # Generate output filename based on input filename
    output_file = input_file.replace('.csv', '_with_sentiment.csv')
    
    # Save to new CSV file
    df.to_csv(output_file, index=False)
    
    return df

# Example usage
if __name__ == "__main__":
    # You can easily analyze multiple files by calling the function multiple times
    df_uoft = analyze_reddit_posts('uoft_reddit_posts.csv')
    # For future use with other universities:
    # df_other = analyze_reddit_posts('other_university_posts.csv')
