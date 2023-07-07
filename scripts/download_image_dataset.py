import argparse
from multiprocessing import Pool
from gz_datasets import GZDataset, GZImageDataset
from tqdm import tqdm


def main(args):
    dataset = GZDataset().from_file(args.input_file)
    print('\n\n', len(dataset.dataset), '\n\n')

    if args.recover_images:
        _, dataset = dataset.scan_image_folder(args.output_dir_images)

    print('\n\n', len(dataset.dataset), '\n\n')
        

    # Use multiprocessing to download all the images in grouped_data_list
    dataset_images = GZImageDataset(args.output_dir_images)
    print('Start downloading the images....')
    with Pool() as pool, tqdm(total=len(dataset.dataset)) as pbar:
        for _ in tqdm(pool.imap_unordered(dataset_images.download_image, dataset.dataset)):
            pbar.update(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", type=str)
    parser.add_argument("--output-dir-images", type=str)
    parser.add_argument("--recover-images", type=bool, default=False)
    args = parser.parse_args()

    main(args)
