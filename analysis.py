import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
import re
import os

def analyze_reddit_posts(input_file):
    # Initialize VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Read the CSV file
    df = pd.read_csv(input_file)

    target_words = [
        # Academic assessment terms
        'exam', 'exams',
        'midterm', 'midterms',
        'final', 'finals',
        'test', 'tests',
        'deadline', 'deadlines',
        'assignment', 'assignments',
        'project', 'projects',
        'essay', 'essays',
        'report', 'reports',
        'presentation', 'presentations'
    ]    
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
    df['sentiment'] = df['Title'].apply(get_sentiment_score)
    
    # Add target word count
    def count_target_words(text):
        if not text or pd.isna(text):
            return 0
        return sum(1 for word in target_words if word.lower() in text.lower())
    
    df['target_word_count'] = df['Title'].apply(count_target_words)
    
    # Generate output filename based on input filename
    output_file = input_file.replace('.csv', '_analyzed.csv')
    # Save to new CSV file
    
    return df

# Example usage
if __name__ == "__main__":
    # Define target words
    target_words = ['stress', 'anxiety', 'help', 'worried', 'failing']  # example words
    
    # Analyze files
    df_uoft = analyze_reddit_posts('uoft_reddit_posts.csv', target_words)
    # For future use with other universities:
    # df_other = analyze_reddit_posts('other_university_posts.csv', target_words)
