import pandas as pd
import json
import random
import os
import tiktoken
from urllib import request
import time
from tqdm import tqdm
from copy import deepcopy
import logging


class GZDataset:

    def __init__(self, dataset: list = []) -> None:
        self.dataset = dataset
        
    def append(self, data: dict):
        self.dataset.append(data)

    def from_file(self, input_file: str, n_inputs: int = -1) -> None:
        try:
            with open(input_file, 'r') as file:
                dataset = json.load(file)
            if 0 < n_inputs < len(dataset):
                dataset = random.sample(dataset, n_inputs)
            return GZDataset(dataset)
        except Exception as e:
            raise ValueError(f"Error loading dataset from file: {input_file}. {str(e)}")
        
    def from_list(self, dataset: list) -> None:
        assert isinstance(dataset, list)
        return GZDataset(deepcopy(dataset))
    
    def from_dataframe(self, dataset: pd.DataFrame) -> None:
        assert isinstance(dataset, pd.DataFrame)

        self.dataset = [{'id': dataset.iloc[i]['id'], 'image': dataset.iloc[i]['image'], 'conversations': dataset.iloc[i]['conversations']} for i in range(len(dataset))]

    def write_dataset(self, output_file: str) -> None:
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

    def get_num_tokens_from_string(self, string: str, encoding_name: str = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
    def scan_image_folder(self, image_folder: str) -> tuple:
        is_contained, is_not_contained = [], []

        # Iterate over the entries in the dataset
        progress_bar = tqdm(total=len(self.dataset), desc="Scanning image folder")

        for entry in self.dataset:
            # Get the image path
            id = entry['id']
            url = entry["image"]
            extension = os.path.splitext(url)[1]
            image_path = os.path.join(image_folder, id + extension)
            
            # Check if the file exists
            try:
                open(image_path, 'rb')
                is_contained.append(entry)
            except FileNotFoundError:
                # Add the entry to the list of entries to be removed
                is_not_contained.append(entry)

            progress_bar.update(1)

        progress_bar.close()

        return GZDataset().from_list(is_contained), GZDataset().from_list(is_not_contained)
    
    def convert_to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.dataset)
    
    def remove_union(self, dataset) -> None:
        self_df = self.convert_to_dataframe()
        df = dataset.convert_to_dataframe()
        self.from_dataframe(self_df[~self_df['id'].isin(df['id'])])
        logging.debug('Number of entries left:', len(self.dataset))
    
    def add_intersection(self, dataset) -> None:
        self_df = self.convert_to_dataframe()
        df = dataset.convert_to_dataframe()
        self.from_dataframe(pd.concat([self_df, df]).drop_duplicates(subset=['id']))
        logging.debug('Number of entries:', len(self.dataset))


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

    def __init__(self, input_folder: str) -> None:
        self.image_folder = input_folder
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
