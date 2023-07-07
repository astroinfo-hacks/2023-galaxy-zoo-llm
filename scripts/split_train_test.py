import os
import argparse
from gz_datasets import GZDataset


def main(args):
    # Load the data from the file
    dataset = GZDataset().from_file(args.input_file)

    # Split the data into training and test datasets
    train_dataset, test_dataset = dataset.split_data(args.ratio)

    # Extract the base file name without extension
    base_name, _ = os.path.splitext(os.path.basename(args.input_file))

    # Make sure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Save the training and test datasets with the original file name included in the specified directory
    train_dataset.write_dataset(os.path.join(args.output_dir, f'{base_name}_train.json'))
    test_dataset.write_dataset(os.path.join(args.output_dir, f'{base_name}_test.json'))


if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description='Split a JSON file into training and test datasets.')
    parser.add_argument('--input-file', required=True, help='Path to the input JSON file.')
    parser.add_argument('--ratio', type=float, default=0.8, help='Ratio for splitting data into training and test sets.')
    parser.add_argument('--output-dir', default='.', help='Directory to save the split files.')
    args = parser.parse_args()

    main(args)
