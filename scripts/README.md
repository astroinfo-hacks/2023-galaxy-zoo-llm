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
$ python convertDataSet.py  --input_csv=path/to/GZ_talk_comments_notes_urls_AISSAI.csv \
                            --output_folder=galaxyzoo_dataset \
                            --download_images=True
```
This will create a folder named `galaxyzoo_dataset` containing all images, and a `metadata.json` file with the conversations.


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
$ python generate_qa.py --input=galaxyzoo_dataset/metadata.json --output=galaxyzoo_dataset/qa.json
```

