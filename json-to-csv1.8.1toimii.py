import os
import pandas as pd
import json
import datetime

# Directory containing the JSON files
directory = 'C:/Users/laurikau/Documents/'  # Replace with your own directory

# Get a list of all JSON files
json_files = [pos_json for pos_json in os.listdir(directory) if pos_json.endswith('.json')]

# Loop over JSON files
for js in json_files:
    # Load JSON file with the correct encoding (e.g., utf-8)
    with open(os.path.join(directory, js), encoding='utf-8') as f:
        data_json = json.load(f)

    # Extract 'transcript' and 'resultEndOffset' from the JSON structure
    results = data_json.get('results', [])
    
    transcripts = []
    result_end_offsets = []

    previous_duration_end = datetime.timedelta(seconds=-1)

    for result in results:
        alternatives = result.get('alternatives', [])
        if alternatives:
            transcript = alternatives[0].get('transcript', '')
            result_end_offset = result.get('resultEndOffset', '')
            transcripts.append(transcript)

            # Convert duration string to "- hh.mm.ss" format
            if result_end_offset:
                duration_str = result_end_offset[:-1]  # Remove 's'
                seconds = round(float(duration_str))
                # Round seconds to the nearest multiple of 30
                seconds = round(seconds / 30) * 30
                duration_start = max(previous_duration_end + datetime.timedelta(seconds=1), datetime.timedelta(seconds=0))
                duration_end = duration_start + datetime.timedelta(seconds=seconds - 1)
                formatted_duration = f"{duration_start} - {duration_end}"
                result_end_offsets.append(formatted_duration)
                previous_duration_end = duration_end
            else:
                result_end_offsets.append('')

    # Create a DataFrame with 'resultEndOffset' and 'transcript' columns in reversed order
    data_df = pd.DataFrame({'Kesto': result_end_offsets, 'Transkripti': transcripts})

    # Save the data to a CSV file with renamed columns
    csv_file_name = js.replace('.json', '.csv')
    data_df.to_csv(os.path.join(directory, csv_file_name), index=False, encoding='utf-8-sig')