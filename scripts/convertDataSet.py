""" Convert the GZ talk comments CSV file to a JSON file for the ZooConvo dataset.
"""
import pandas as pd
import json
from tqdm import tqdm
import urllib.request
import os
from absl import app, flags
from absl.flags import FLAGS
from multiprocessing import Pool

# Define the command line arguments
flags.DEFINE_string('input_csv', 'GZ_talk_comments_notes_urls_AISSAI.csv', 'Path to the input CSV file')
flags.DEFINE_string('output_folder', 'galaxyzoo_dataset', 'Path to the output folder')
# Add a flag to download images
flags.DEFINE_bool('download_images', False, 'Download images from the URLs in the CSV file')

FLAGS = flags.FLAGS

# Define the main function
def main(_argv):

    # Create the output folder if it does not exist
    if not os.path.exists(FLAGS.output_folder):
        os.makedirs(FLAGS.output_folder)

    # Read the CSV file into a DataFrame
    data = pd.read_csv(FLAGS.input_csv)

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
    
    # Use multiprocessing to download all the images in grouped_data_list
    if FLAGS.download_images:
        def download_image(group_dict):
            try:
                urllib.request.urlretrieve(group_dict["image"], FLAGS.output_folder + "/" + group_dict["id"] + ".jpeg")
            except:
                print("Could not download image for subject ID " + group_dict["id"])
        with Pool() as pool:
            pool.map(download_image, grouped_data_list)

    # Convert the grouped data list to JSON and save it to a file
    json_data = json.dumps(grouped_data_list, indent=4)
    with open( FLAGS.output_folder + "/metadata.json", 'w') as file:
        file.write(json_data)

# Call the main function
if __name__ == '__main__':
    app.run(main)
