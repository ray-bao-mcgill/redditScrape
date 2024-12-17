import pandas as pd
import os
import re
import csv

def find_matching_universities(target_df, reference_df, tolerance=0.001):
    """
    Find universities in reference_df that match the STUFACR and UGDS values from target_df
    
    Args:
        target_df: DataFrame with unknown universities
        reference_df: DataFrame with known university names
        tolerance: Percentage difference allowed for matching (default 0.1%)
    """
    matches = []
    
    for _, target_row in target_df.iterrows():
        target_stufacr = target_row['STUFACR']
        target_ugds = target_row['UGDS']
        
        # Find exact/near-exact matches
        matches_mask = (
            (reference_df['STUFACR'].between(
                target_stufacr * (1-tolerance), 
                target_stufacr * (1+tolerance)
            )) &
            (reference_df['UGDS'].between(
                target_ugds * (1-tolerance), 
                target_ugds * (1+tolerance)
            ))
        )
        
        matching_unis = reference_df[matches_mask].copy()
        
        if not matching_unis.empty:
            matches.append({
                'original_row': target_row,
                'matches': matching_unis
            })
    
    return matches

def recover_data():
    """Recover lost data from FINALDATA2.csv using americanunidata.csv"""
    recovery_dir = 'recovery'
    os.makedirs(recovery_dir, exist_ok=True)
    
    try:
        # Load the data files
        target_data = pd.read_csv('recovery/FINALDATA2.csv')
        reference_data = pd.read_csv('recovery/americanunidata.csv')
        
        # Find matches
        matches = find_matching_universities(target_data, reference_data)
        
        # Create recovery report
        report_rows = []
        uni_counter = 1  # Counter for university numbering
        seen_universities = {}  # Track universities we've seen
        
        # First pass: collect all rows for each university
        university_rows = {}
        for match in matches:
            original = match['original_row']
            for _, potential_match in match['matches'].iterrows():
                uni_name = potential_match['INSTNM']
                if uni_name not in university_rows:
                    university_rows[uni_name] = []
                
                # Create row data
                row_data = {col: original[col] for col in target_data.columns}
                row_data.update({
                    'Matched_University': uni_name,
                    'Matched_STUFACR': potential_match['STUFACR'],
                    'Matched_UGDS': potential_match['UGDS']
                })
                university_rows[uni_name].append(row_data)
        
        # Second pass: combine rows and assign numbers
        for uni_name, rows in sorted(university_rows.items()):
            # Average the sentiment and t_count if multiple rows exist
            if len(rows) > 1:
                combined_row = rows[0].copy()
                sentiments = [row.get('sentiment', 0) for row in rows]
                t_counts = [row.get('t_count', 0) for row in rows]
                combined_row['sentiment'] = sum(sentiments) / len(sentiments)
                combined_row['t_count'] = sum(t_counts) / len(t_counts)
                rows = [combined_row]
            
            # Assign university number
            for row in rows:
                if uni_name not in seen_universities:
                    seen_universities[uni_name] = uni_counter
                    uni_counter += 1
                
                row_data = {col: row[col] for col in target_data.columns}
                row_data.update({
                    'uni': seen_universities[uni_name],
                    'Matched_University': uni_name,
                    'Matched_STUFACR': row['Matched_STUFACR'],
                    'Matched_UGDS': row['Matched_UGDS']
                })
                report_rows.append(row_data)
        
        # Create and save the recovery report
        report_df = pd.DataFrame(report_rows)
        report_df = report_df.sort_values('uni')
        report_df.to_csv(f'{recovery_dir}/recovery_report.csv', index=False)
        
        # Read the saved report to ensure consistent ordering
        saved_report = pd.read_csv(f'{recovery_dir}/recovery_report.csv')
        
        # Create the university mapping in codebook format
        mapping_rows = [['Format_name', 'Value (numeric code)', 'Value label']]
        
        # Process universities from the report
        for _, row in saved_report.drop_duplicates('Matched_University').iterrows():
            uni_name = row['Matched_University']
            uni_id = row['uni']
            
            # First row includes "unisub", others are empty
            format_name = 'unisub' if len(mapping_rows) == 1 else ''
            mapping_rows.append([format_name, str(uni_id), uni_name])
        
        # Save the mapping file
        with open(f'{recovery_dir}/recovered_map.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(mapping_rows)
        
        print(f"Recovery report saved to {recovery_dir}/recovery_report.csv")
        print(f"University mapping saved to {recovery_dir}/recovered_map.csv")
        
    except FileNotFoundError as e:
        print(f"Error: Required file not found - {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    recover_data()

