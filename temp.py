import pandas as pd
import difflib

def clean_uni_name(name):
    """Clean university name for more flexible matching"""
    # Convert to lowercase and strip whitespace
    name = str(name).lower().strip()
    
    # Remove common words and punctuation
    replacements = {
        'university': 'uni',
        'college': '',
        'of': '',
        'and': '',
        '&': '',
        ',': '',
        '-': ' ',
        '.': '',
    }
    
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    # Remove extra whitespace
    return ' '.join(name.split())

def compare_university_lists():
    try:
        # Read both CSV files
        top100_df = pd.read_csv('data/university_map.csv')
        recovery_df = pd.read_csv('recovery/recovery_report.csv')
        
        # Extract and clean university names from both files
        top100_unis = {clean_uni_name(name): name for name in top100_df['name']}
        recovery_unis = {clean_uni_name(name): name for name in recovery_df['Matched_University']}
        
        # Find matches using fuzzy matching
        matches = []
        potential_matches = []
        
        for clean_top_uni, original_top_uni in top100_unis.items():
            # Look for exact matches first (with cleaned names)
            if clean_top_uni in recovery_unis:
                matches.append((original_top_uni, recovery_unis[clean_top_uni]))
            else:
                # Try fuzzy matching with a higher threshold
                close_matches = difflib.get_close_matches(clean_top_uni, recovery_unis.keys(), n=1, cutoff=0.75)
                if close_matches:
                    potential_matches.append((original_top_uni, recovery_unis[close_matches[0]]))
        
        # Print results
        print(f"\nTotal universities in top100: {len(top100_unis)}")
        print(f"Total universities in recovery: {len(recovery_unis)}")
        print(f"\nExact matches found: {len(matches)}")
        print(f"Potential fuzzy matches found: {len(potential_matches)}")
        
        if matches:
            print("\nExact matches (top100 <-> recovery):")
            for top_uni, recovery_uni in matches[:10]:  # Show first 10
                print(f"  {top_uni} <-> {recovery_uni}")
            if len(matches) > 10:
                print(f"  ... and {len(matches) - 10} more")
        
        if potential_matches:
            print("\nPotential matches (top100 -> recovery):")
            for top_uni, recovery_uni in potential_matches:
                print(f"  {top_uni} -> {recovery_uni}")
        
        # Find universities unique to each file (using cleaned names)
        unique_to_top100 = set(top100_unis.values()) - {m[0] for m in matches} - {m[0] for m in potential_matches}
        unique_to_recovery = set(recovery_unis.values()) - {m[1] for m in matches} - {m[1] for m in potential_matches}
        
        if unique_to_top100:
            print("\nUniversities only in top100:")
            for uni in sorted(unique_to_top100):
                print(f"  {uni}")
                
        if unique_to_recovery:
            print("\nUniversities only in recovery (first 10):")
            for uni in sorted(list(unique_to_recovery)[:10]):
                print(f"  {uni}")
            if len(unique_to_recovery) > 10:
                print(f"  ... and {len(unique_to_recovery) - 10} more")
                
    except FileNotFoundError as e:
        print(f"Error: Could not find one of the required files - {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    compare_university_lists()
