import argparse
import os
import pandas as pd
import json
from tqdm import tqdm
from urllib import request
from multiprocessing import Pool
from functools import partial


def download_image(group_dict: dict, output_folder_image: str):
    url = group_dict["image"]
    extension = os.path.splitext(url)[1]
    id = group_dict["id"]
    try:
        request.urlretrieve(url, os.path.join(output_folder_image, id + extension))
    except:
        print("Could not download image for subject ID " + group_dict["id"])
        print("URL:", url)


def fetch_info_by_group(subject_id: float, group: pd.DataFrame) -> dict:
    # Get the conversations of the group as a list
    comment_body = group['comment_body'].tolist()
    # Get the url of the image
    location_entry = group['locations'].iloc[0]
    image = json.loads(location_entry)["0"]
    # Cast the subject_id as an int
    id = str(int(subject_id))
    # Create the conversations as a dict with the training-friendly format
    conversations = [{
            "from": "human",
            "value": sentence
        } for sentence in comment_body]

    return {
        "id": id,
        "image": image,
        "conversations": conversations,
    }


def main(args):
    assert os.path.exists(args.input_path), "{input_path} does not exist.".format(input_path=args.input_path)
    
    # Load data
    data = pd.read_csv(args.input_path)

    # Group the data by "subject_id"
    grouped_data = data.groupby('subject_id')

    # Create a list to store the grouped data as dictionaries
    grouped_data_list = []

    # Initialize the progress bar
    progress_bar = tqdm(total=len(grouped_data), desc="Processing")

    # Iterate over the groups and populate the grouped data list
    for subject_id, group in data.groupby('subject_id'):
        # Append the group dictionary to the list
        grouped_data_list.append(fetch_info_by_group(subject_id, group))

        # Update the progress bar
        progress_bar.update(1)

    # Close the progress bar
    progress_bar.close()

    # Use multiprocessing to download all the images in grouped_data_list
    if args.download_images:
        os.makedirs(args.output_path_images, exist_ok=True)
        print('Start downloading the images....')
        download_image_partial = partial(download_image, output_folder_image=args.output_path_images)
        with Pool() as pool:
            pool.map(download_image_partial, grouped_data_list)
        print('Done!')

    # Convert the grouped data list to JSON
    json_data = json.dumps(grouped_data_list, indent=4)

    # Write the JSON data to a file
    os.makedirs(os.path.dirname(args.output_path_json), exist_ok=True)
    with open(args.output_path_json, 'w') as file:
        file.write(json_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str, default="./")
    parser.add_argument("--output-path-json", type=str, default="./")
    parser.add_argument("--output-path-images", type=str, default="./")
    parser.add_argument("--download-images", type=bool, default=False)
    args = parser.parse_args()

    main(args)
