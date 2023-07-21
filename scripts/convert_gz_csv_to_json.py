import argparse
from gz_datasets import RawGZDataset


def main(args):
    raw_gz_dataset = RawGZDataset().from_file(args.input_file)
    gz_dataset = raw_gz_dataset.convert_to_gzdataset()
    gz_dataset.write_dataset(args.output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", type=str)
    parser.add_argument("--output-file", type=str)
    args = parser.parse_args()

    main(args)
