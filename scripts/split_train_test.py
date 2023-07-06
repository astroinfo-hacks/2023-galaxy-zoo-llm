import json
import random
import os
import argparse

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def split_data(data, ratio):
    random.shuffle(data)
    n = len(data)
    train_size = int(n * ratio)
    
    train_data = data[:train_size]
    test_data = data[train_size:]
    
    return train_data, test_data

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description='Split a JSON file into training and test datasets.')
    parser.add_argument('--input-file', required=True, help='Path to the input JSON file.')
    parser.add_argument('--ratio', type=float, default=0.8, help='Ratio for splitting data into training and test sets.')
    parser.add_argument('--output-dir', default='.', help='Directory to save the split files.')

    args = parser.parse_args()

    # Load the data from the file
    file_path = args.input_file
    data = load_json_file(file_path)

    # Split the data into training and test datasets
    train_data, test_data = split_data(data, args.ratio)

    # Extract the base file name without extension
    base_name, _ = os.path.splitext(os.path.basename(file_path))

    # Make sure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Save the training and test datasets with the original file name included in the specified directory
    save_json_file(os.path.join(args.output_dir, f'{base_name}_train.json'), train_data)
    save_json_file(os.path.join(args.output_dir, f'{base_name}_test.json'), test_data)
