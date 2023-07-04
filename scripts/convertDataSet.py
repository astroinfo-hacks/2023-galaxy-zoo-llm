
''''''
import pandas as pd
import json
from tqdm import tqdm

# Read the CSV file into a DataFrame
data = pd.read_csv('GZ_talk_comments_notes_urls_AISSAI.csv')

# Group the data by "subject_id"
grouped_data = data.groupby('subject_id')

# Create a list to store the grouped data as dictionaries
grouped_data_list = []

# Initialize the progress bar
progress_bar = tqdm(total=len(grouped_data), desc="Processing")

# Iterate over the groups and populate the grouped data list
for discussion_id, group in grouped_data:
    sentences = group['comment_body'].tolist()

    # Extract the first entry from the "locations" column
    location_entry = group['locations'].iloc[0]
    #need that because of https://
    image = ((location_entry.split(":")[1])+":"+(location_entry.split(":")[2])).strip('\"').split("jpeg")[0]+"jpeg"

    # Create a dictionary for each group
    group_dict = {
        "id": str(discussion_id).split(".")[0],
        "image": image,
        "conversations": []
    }

    # Add sentences to the conversations list
    for sentence in sentences:
        conversation = {
            "from": "human",
            "value": sentence
        }
        group_dict["conversations"].append(conversation)

    # Append the group dictionary to the list
    grouped_data_list.append(group_dict)

    # Update the progress bar
    progress_bar.update(1)

# Close the progress bar
progress_bar.close()

# Convert the grouped data list to JSON
json_data = json.dumps(grouped_data_list, indent=4)

# Write the JSON data to a file
with open('output.json', 'w') as file:
    file.write(json_data)
