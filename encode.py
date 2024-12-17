import pandas as pd
import glob
import os
import compress as comp
import difflib
import re

def combine_csv_files():
    """Combines and cleans CSV files from analyzed_data directory"""
    # Get all CSV files in the analyzed_data directory
    csv_files = glob.glob('analyzed_data/*_reddit_posts_analyzed.csv')
    
    if not csv_files:
        print("No CSV files found in analyzed_data directory")
        return False
    
    # Initialize list to store DataFrames
    dfs = []
    
    # Process each CSV file
    for file in csv_files:
        uni_name = os.path.basename(file).replace('_reddit_posts_analyzed.csv', '')
        df = pd.read_csv(file)
        
        new_df = pd.DataFrame({
            'uni': uni_name,
            'psample': df['Title'],
            'date': df['Date'],
            'sentiment': df['sentiment'],
            't_count': df['target_word_count'],
            'cost_of_living': df['cost_of_living']
        })
        dfs.append(new_df)
    
    # Combine all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)
    os.makedirs('coded', exist_ok=True)
    combined_df.to_csv('coded/uncleaned_data.csv', index=False)
    return True

def process_with_metrics():
    """Process data with metrics after matching is complete"""
    try:
        # Load the data
        uncleaned_data = pd.read_csv('coded/uncleaned_data.csv')
        
        # Get list of valid universities (those with complete metrics)
        valid_unis = uncleaned_data.groupby('uni').first().reset_index()
        valid_unis = valid_unis[valid_unis['STUFACR'].notna() & valid_unis['UGDS'].notna()]['uni']
        
        # Filter data to only include valid universities
        filtered_data = uncleaned_data[uncleaned_data['uni'].isin(valid_unis)]
        
        if len(filtered_data) == 0:
            print("Error: No data remains after filtering for valid metrics")
            return False
            
        # Create cleaned data with new indices
        universities = sorted(filtered_data['uni'].unique())
        uni_mapping = {uni: idx + 1 for idx, uni in enumerate(universities)}
        
        # Group by university and reset psample numbers
        cleaned_rows = []
        for uni in universities:
            uni_data = filtered_data[filtered_data['uni'] == uni].copy()
            if len(uni_data) > 0:  # Only process if there's data
                uni_data = uni_data.sort_values('date', ascending=False)
                uni_data['uni'] = uni_mapping[uni]  # Convert to ID for the cleaned data
                uni_data['psample'] = range(1, len(uni_data) + 1)
                cleaned_rows.append(uni_data)
        
        if not cleaned_rows:
            print("Error: No data to process after cleaning")
            return False
            
        # Combine all university data
        cleaned_df = pd.concat(cleaned_rows, ignore_index=True)
        cleaned_df = cleaned_df[['uni', 'psample', 'date', 'sentiment', 't_count', 'cost_of_living', 'STUFACR', 'UGDS']]
        
        # Save the cleaned data
        cleaned_df.to_csv('coded/cleaned_data.csv', index=False)
        
        print(f"Successfully processed {len(universities)} universities with {len(cleaned_df)} total posts")
        return True
        
    except FileNotFoundError as e:
        print(f"Error: Required file not found - {str(e)}")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def create_codebook():
    """Creates a codebook describing the variables in the cleaned dataset"""
    try:
        # Read the cleaned data and university mapping
        cleaned_data = pd.read_csv('coded/cleaned_data.csv')
        uni_mapping = pd.read_csv('coded/university_mapping.csv')
        
        if len(uni_mapping) == 0:
            print("Warning: No universities found in mapping file")
            return False
            
        # Create initial rows for unisub entries
        rows = []
        # First university row includes "unisub" in Format_name
        first_uni = uni_mapping.iloc[0]
        rows.append({
            'Format_name': 'unisub',
            'Value (numeric code)': first_uni['uni_id'],
            'Value label': f"{str(first_uni['university'])}"
        })
        
        # Remaining universities have empty Format_name
        for _, uni in uni_mapping.iloc[1:].iterrows():
            rows.append({
                'Format_name': '',
                'Value (numeric code)': uni['uni_id'],
                'Value label': f"{str(uni['university'])}"
            })
        
        # Add final psample row
        rows.append({
            'Format_name': 'psample',
            'Value (numeric code)': f'[1, {len(cleaned_data)}]',
            'Value label': 'see sheet 2'
        })
        
        # Create and save codebook
        codebook = pd.DataFrame(rows)
        codebook.to_csv('coded/codebook.csv', index=False)
        print("Codebook saved to coded/codebook.csv")
        return True
        
    except FileNotFoundError as e:
        print(f"Error: Required file not found - {str(e)}")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def create_codebook_sheet2():
    """Creates the second sheet of the codebook mapping psample numbers to post titles"""
    try:
        # Read the cleaned and uncleaned data
        cleaned_data = pd.read_csv('coded/cleaned_data.csv')
        uncleaned_data = pd.read_csv('coded/uncleaned_data.csv')
        
        # Create mapping between psample and titles
        sheet2 = pd.DataFrame({
            'psample': range(1, len(cleaned_data) + 1),
            'title': uncleaned_data['psample']
        })
        
        # Save sheet2
        sheet2.to_csv('coded/codebook_sheet2.csv', index=False)
        print("Codebook sheet 2 saved to coded/codebook_sheet2.csv")
        
    except PermissionError:
        print("Error: Unable to write to file. Please check if the file is open in another program or if you have write permissions.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def create_post_counts():
    """Creates a CSV file showing the number of posts scraped for each university"""
    try:
        # Read the uncleaned data
        uncleaned_data = pd.read_csv('coded/uncleaned_data.csv')
        
        # Count posts per university
        post_counts = uncleaned_data['uni'].value_counts().reset_index()
        post_counts.columns = ['university', 'post_count']
        
        # Sort by university name
        post_counts = post_counts.sort_values('university')
        
        # Save the counts
        post_counts.to_csv('coded/post_counts.csv', index=False)
        print("Post counts saved to coded/post_counts.csv")
        
    except PermissionError:
        print("Error: Unable to write to file. Please check if the file is open in another program or if you have write permissions.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def add_university_metrics():
    """Add UGRADS and STUFACR data from americanunidata.csv to uncleaned_data"""
    try:
        # Load the data files
        uncleaned_data = pd.read_csv('coded/uncleaned_data.csv')
        reference_data = pd.read_csv('recovery/americanunidata.csv')
        
        # Manual matches list
        manual_matches = [
            ("arizona_state_university", "Arizona State University Campus Immersion"),
            ("baruch_college", "CUNY Bernard M Baruch College"),
            ("berklee_college", "Berklee College of Music"),
            ("bowling_green_state_university", "Bowling Green State University-Firelands"),
            ("humboldt_state_university","California State Polytechnic University-Humboldt"),
            ("hunter_college", "CUNY Hunter College"),
            ("ohio_university", "Ohio University-Main Campus"),
            ("purdue_university", "Purdue University-Main Campus"),
            ("rose_hulman_institue", "Rose-Hulman Institute of Technology"),
            ("texas_am", "Texas A & M University-Corpus Christi"),
            ("the_college_of_william_and_mary", "William & Mary"),
            ("university_of_alabama", "The University of Alabama"),
            ("university_of_hawaii", "University of Hawaii at Manoa"),
            ("university_of_minnesota", "University of Minnesota-Twin Cities"),
            ("university_of_missouri","University of Missouri-Columbia"),
            ("university_of_new_mexico", "University of New Mexico-Main Campus"),
            ("university_of_oklahoma", "University of Oklahoma-Norman Campus"),
            ("university_of_pittsburgh", "University of Pittsburgh-Pittsburgh Campus"),
            ("university_of_texas_-_austin", "The University of Texas at Austin"),
            ("university_of_texas_-_dallas", "The University of Texas at Dallas"),
            ("university_of_virgina", "University of Virginia-Main Campus")
        ]
        manual_dict = dict(manual_matches)
        
        # Filter out rows with missing metrics
        reference_data = reference_data.dropna(subset=['STUFACR', 'UGDS'])
        
        # Create reference dictionary with institution names as keys
        reference_name_dict = {name: row for name, row in zip(reference_data['INSTNM'], reference_data.itertuples())}
        
        # Clean university names for matching
        def clean_name(name):
            name = str(name).lower()
            name = re.sub(r'university|college|institute|of|technology|-|_|,|\s+', ' ', name)
            return ' '.join(sorted(set(name.split())))
            
        # Create cleaned name mappings for fuzzy matching
        reference_dict = {clean_name(name): row for name, row in zip(reference_data['INSTNM'], reference_data.itertuples())}
        
        # Add new columns
        uncleaned_data['STUFACR'] = None
        uncleaned_data['UGDS'] = None
        
        matched = 0
        total = len(uncleaned_data['uni'].unique())
        log_entries = []
        
        # Process each unique university
        for uni in uncleaned_data['uni'].unique():
            # First check manual matches
            if uni in manual_dict:
                match_name = manual_dict[uni]
                if match_name in reference_name_dict:
                    match = reference_name_dict[match_name]
                    uncleaned_data.loc[uncleaned_data['uni'] == uni, 'STUFACR'] = match.STUFACR
                    uncleaned_data.loc[uncleaned_data['uni'] == uni, 'UGDS'] = match.UGDS
                    matched += 1
                    log_entry = f"Original: {uni}\nMANUAL MATCH -> {match_name}\n"
                    log_entry += f"STUFACR: {match.STUFACR}, UGDS: {match.UGDS}\n"
                    log_entries.append(log_entry + "-" * 50 + "\n")
                    continue
            
            clean_uni = clean_name(uni)
            log_entry = f"Original: {uni}\nCleaned: {clean_uni}\n"
            
            # Try exact match first
            if clean_uni in reference_dict:
                match = reference_dict[clean_uni]
                uncleaned_data.loc[uncleaned_data['uni'] == uni, 'STUFACR'] = match.STUFACR
                uncleaned_data.loc[uncleaned_data['uni'] == uni, 'UGDS'] = match.UGDS
                matched += 1
                log_entry += f"EXACT MATCH -> {match.INSTNM}\n"
                log_entry += f"STUFACR: {match.STUFACR}, UGDS: {match.UGDS}\n"
            else:
                # Try fuzzy matching
                matches = difflib.get_close_matches(clean_uni, reference_dict.keys(), n=1, cutoff=0.8)
                if matches:
                    match = reference_dict[matches[0]]
                    uncleaned_data.loc[uncleaned_data['uni'] == uni, 'STUFACR'] = match.STUFACR
                    uncleaned_data.loc[uncleaned_data['uni'] == uni, 'UGDS'] = match.UGDS
                    matched += 1
                    log_entry += f"FUZZY MATCH -> {match.INSTNM}\n"
                    log_entry += f"Matched with: {matches[0]}\n"
                    log_entry += f"STUFACR: {match.STUFACR}, UGDS: {match.UGDS}\n"
                else:
                    log_entry += "NO MATCH FOUND\n"
            
            log_entries.append(log_entry + "-" * 50 + "\n")
        
        # Save matching log before filtering
        with open('coded/matching_log.txt', 'w', encoding='utf-8') as f:
            f.write(f"Total universities processed: {total}\n")
            f.write(f"Successfully matched: {matched}\n")
            f.write("=" * 50 + "\n\n")
            f.writelines(log_entries)
        
        # Remove rows with missing metrics
        uncleaned_data = uncleaned_data.dropna(subset=['STUFACR', 'UGDS'])
        
        # Reassign integer codes
        universities = uncleaned_data['uni'].unique()
        uni_mapping = {uni: idx + 1 for idx, uni in enumerate(sorted(universities))}
        uncleaned_data['uni'] = uncleaned_data['uni'].map(uni_mapping)
        
        # Save updated uncleaned data
        uncleaned_data.to_csv('coded/uncleaned_data.csv', index=False)
        
        print(f"Added university metrics to uncleaned_data.csv ({matched}/{total} universities matched)")
        print("Matching details saved to coded/matching_log.txt")
        
        # Update university mapping
        mapping_df = pd.DataFrame({
            'uni_id': uni_mapping.values(),
            'university': uni_mapping.keys()
        }).sort_values('uni_id')
        mapping_df.to_csv('coded/university_mapping.csv', index=False)
        
        return True
        
    except FileNotFoundError as e:
        print(f"Error: Required file not found - {str(e)}")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    combine_csv_files()
    if add_university_metrics():
        if process_with_metrics():
            if create_codebook():
                create_codebook_sheet2()
                create_post_counts()
                comp.compress_data()
