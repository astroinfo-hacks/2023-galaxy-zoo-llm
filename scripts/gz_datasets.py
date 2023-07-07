import pandas as pd
import json
import random
import os
import tiktoken
from urllib import request
import copy
import time
from tqdm import tqdm


class GZDataset:

    def __init__(self, dataset: list = []) -> None:
        self.dataset = dataset
        
    def append(self, data: dict):
        self.dataset.append(data)

    def from_file(self, input_file: str, n_inputs: int = -1):
        try:
            with open(input_file, 'r') as file:
                dataset = json.load(file)
            if 0 < n_inputs < len(dataset):
                dataset = random.sample(dataset, n_inputs)
            return GZDataset(dataset)
        except Exception as e:
            raise ValueError(f"Error loading dataset from file: {input_file}. {str(e)}")
        
    def from_list(self, dataset: list):
        assert isinstance(dataset, list)
        return GZDataset(dataset)

    def write_dataset(self, output_file: str):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as file:
            json.dump(self.dataset, file, indent=4)

    def split_data(self, ratio: int = 0.8) -> tuple:
        dataset_copy = self.dataset.copy()
        random.shuffle(dataset_copy)
        train_size = int(len(dataset_copy) * ratio)
        
        train_dataset = GZDataset(dataset_copy[:train_size])
        test_dataset = GZDataset(dataset_copy[train_size:])
    
        return train_dataset, test_dataset

    def get_num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
    def remove_missing_images_from_json(self, image_dir: str) -> list:
        dataset_trimmed = copy.deepcopy(self.dataset)

        # Create a list to store the entries to be removed
        to_be_removed = []

        # Iterate over the entries in the dataset
        for entry in self.dataset:
            # Get the image path
            image_path = os.path.join(image_dir, entry['image'])
            
            # Check if the file exists
            try:
                open(image_path, 'rb')
            except FileNotFoundError:
                # Add the entry to the list of entries to be removed
                to_be_removed.append(entry)

        # Remove the entries from the dataset
        for entry in to_be_removed:
            dataset_trimmed.remove(entry)

        return GZDataset(dataset_trimmed)
    

class RawGZDataset:

    def __init__(self, dataset: pd.DataFrame = pd.DataFrame()) -> None:
        self.dataset = dataset

    def from_file(self, input_file: str):
        try:
            return RawGZDataset(pd.read_csv(input_file))
        except Exception as e:
            raise ValueError(f"Error loading dataset from file: {input_file}. {str(e)}")
        
    def from_df(self, dataset: pd.DataFrame) -> None:
        assert isinstance(dataset, pd.DataFrame)
        return RawGZDataset(dataset.copy())

    def fetch_info_by_group(self, subject_id: float, group: pd.DataFrame) -> dict:
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
    
    def convert_to_gzdataset(self) -> GZDataset:
        # Group the data by "subject_id"
        grouped_data = self.dataset.groupby('subject_id')

        # Create a list to store the grouped data as dictionaries
        grouped_data_list = []

        # Initialize the progress bar
        progress_bar = tqdm(total=len(grouped_data), desc="Processing")

        # Iterate over the groups and populate the grouped data list
        for subject_id, group in grouped_data:
            # Append the group dictionary to the list
            grouped_data_list.append(self.fetch_info_by_group(subject_id, group))

            # Update the progress bar
            progress_bar.update(1)

        # Close the progress bar
        progress_bar.close()

        return GZDataset().from_list(grouped_data_list)


class GZImageDataset:

    def __init__(self, input_folder: str, recover_from: str = None) -> None:
        self.image_folder = input_folder
        self.recover_from = recover_from
        self.missing_items_list = []
        os.makedirs(self.image_folder, exist_ok=True)

    def download_image(self, group_dict: dict) -> None:
        url = group_dict["image"]
        extension = os.path.splitext(url)[1]
        id = group_dict["id"]

        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                request.urlretrieve(url, os.path.join(self.image_folder, id + extension))
                return
            except Exception as e:
                print(f"Error occurred while downloading image for subject ID {group_dict['id']}:", str(e))
                print(f"Retrying ({retries + 1}/{max_retries})...")
                time.sleep(1)  # Wait for 1 second before retrying
                retries += 1

        print(f"Error occurred while downloading image for subject ID {group_dict['id']}")
        print("URL:", url)
        print("Error message:", str(e))
        self.missing_items_list.append(url)

    def write_missing_items_csv(self):
        assert self.missing_items_file is not None
        missing_items_df = pd.DataFrame(self.missing_items_list)
        missing_items_df.to_csv(self.missing_items_file)

    
    def download_missing_items(self, missing_items_file: str):
        pass

