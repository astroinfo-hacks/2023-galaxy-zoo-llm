import argparse
from multiprocessing import Pool
from gz_datasets import RawGZDataset, GZImageDataset


def main(args):
    raw_gz_dataset = RawGZDataset().from_file(args.input_file)
    gz_dataset = raw_gz_dataset.convert_to_gzdataset()
    gz_dataset.write_dataset(args.output_file_json)

    # Use multiprocessing to download all the images in grouped_data_list
    if args.download_images:
        dataset_images = GZImageDataset(args.output_dir_images, args.output_file_missing_items)
        print('Start downloading the images....')
        with Pool() as pool:
            pool.map(dataset_images.download_image, gz_dataset.dataset)
        print('Done!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", type=str)
    parser.add_argument("--output-file-json", type=str)
    parser.add_argument("--output-dir-images", type=str)
    parser.add_argument("--download-images", type=bool, default=False)
    parser.add_argument("--output-file-missing-items", type=str, default=None)
    args = parser.parse_args()

    main(args)
