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

    # Read university mapping with cost of living data
    try:
        uni_data = pd.read_csv('data/top200_universities.csv')
        # Extract university name from input filename
        uni_name = os.path.basename(input_file).replace('_reddit_posts.csv', '')
        
        # Try different matching strategies
        cost_of_living = None
        
        # Clean the names for comparison using the same function as scrapedata.py
        def clean_for_comparison(name):
            # Remove special characters and spaces, convert to lowercase
            clean = ''.join(c for c in name if c.isalnum() or c in ' -_')
            return clean.strip().replace(' ', '_').lower()
        
        # Add cleaned versions of names to the dataframe
        uni_data['clean_name'] = uni_data['name'].apply(clean_for_comparison)
        uni_data['clean_subreddit'] = uni_data['subreddit'].apply(clean_for_comparison)
        
        # Try matching on cleaned names
        match = uni_data[uni_data['clean_name'] == clean_for_comparison(uni_name)]
        if not match.empty:
            cost_of_living = match['cost_of_living'].iloc[0]
        else:
            # Try matching by subreddit
            match = uni_data[uni_data['clean_subreddit'] == clean_for_comparison(uni_name)]
            if not match.empty:
                cost_of_living = match['cost_of_living'].iloc[0]
            else:
                print(f"Warning: No matching university found for {uni_name}")
                
    except Exception as e:
        print(f"Warning: Could not get cost of living data: {e}")
        cost_of_living = None

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
    
    # Add target word count (modified to binary)
    def count_target_words(text):
        if not text or pd.isna(text):
            return 0
        return 1 if any(word.lower() in text.lower() for word in target_words) else 0
    
    df['target_word_count'] = df['Title'].apply(count_target_words)
    
    # Add cost of living column
    df['cost_of_living'] = cost_of_living
    
    # Generate output filename based on input filename
    output_file = input_file.replace('.csv', '_analyzed.csv')
    # Save to new CSV file
    
    return df
