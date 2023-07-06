import json
import argparse
import os

def main(args):
    # Read the qa.json file
    dataset = json.load(open(args.input_file_json, 'r'))

    # Create a list to store the entries to be removed
    to_be_removed = []

    # Iterate over the entries in the dataset
    for entry in dataset:
        # Get the image path
        image_path = os.path.join(args.input_dir_images, entry['image'])
        
        # Check if the file exists
        try:
            open(image_path, 'rb')
        except FileNotFoundError:
            # Add the entry to the list of entries to be removed
            to_be_removed.append(entry)

    # Remove the entries from the dataset
    for entry in to_be_removed:
        dataset.remove(entry)

    # Write the dataset to the qa.json file
    with open(args.output_file, 'w') as file:
        json.dump(dataset, file, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file-json", type=str)
    parser.add_argument("--input-dir-images", type=str)
    parser.add_argument("--output-file", type=str)
    args = parser.parse_args()

    main(args)
