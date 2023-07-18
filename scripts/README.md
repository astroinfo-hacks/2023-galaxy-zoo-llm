# Dataset pre-processing scripts


## Requirements

```
pip install selenium tqdm openai
```

## Dataset Download and Preparation 

### Option 1: Using exported and anonymized Galaxy Zoo talk data (preferred)

This option should be preferred, but relies on having access to the `GZ_talk_comments_notes_urls_AISSAI.csv` file obtained specifically for this hackathon. 

The first step is to process this input csv file to produce a simpler representation of the conversations, with comments groupped by image, as well as to download all associated images.
```bash
$ python convert_gz_csv_to_json.py  --input-file=path/to/GZ_talk_comments_notes_urls_AISSAI.csv \
                                    --output-file=galaxyzoo_dataset
$ python download_image_dataset.py  --input-file=path/to/GZ_talk_comments_notes_urls_AISSAI.json \
                                    --output-dir=galaxyzoo_images \
                                    --recover-images=False
```
This will create a folder named `galaxyzoo_dataset` containing the `GZ_talk_comments_notes_urls_AISSAI.json` file with the conversations, and a `galaxyzoo_images` containing all the images. Set the --recover-images parameter to True if images are missing.


### Option 2: Web Scraping

Hummm maybe don't use this one, as it's better to discuss with the Galaxy Zoo team about how to access the data, and how to handle it in a safe and responsible way. 

But, if you must, here is how you can get the data by yourself, directly by scraping the Galaxy Zoo talk website. 

We first generate a list of all the URLs of the images we want to download. This is done by running the following command:

```bash
$ python scrap_urls.py -n 1000
```
where -n is the number of pages to scrap. Each page contains 10 conversations. The URLs will be stored in a file called `talks_urls.csv`. Then, we download the images using the following command:

```bash
$ python scrap_notes.py 
```
This will generate a new directory called `talks_dset` containing all the images, as well as a `metadata.json` file containing  the conversations.

## Generating Q&A data

To generate a dataset of Q&A pairs, you need to have an OpenAI API key. Assuming you have downloaded and prepared the data in the recommended way, you can run the following script:

```bash
$ python generate_qa.py --input-file=galaxyzoo_dataset/GZ_talk_comments_notes_urls_AISSAI.json \
                        --output-file=galaxyzoo_dataset/qa.json \
                        --prompt-file=prompt.py \
                        --mode=desc
```
The --mode parameter can be set to desc or conv depending on whether you want to generate a description or pairs of Q&A. To generate a subset, you can set the --n-inputs parameter to an integer value. You can specify the OpenAI API key using the --openai-api-key paramter. If the script stopped abruptly, you can recover from an existing qa.json file using the --recover-from parameter.
