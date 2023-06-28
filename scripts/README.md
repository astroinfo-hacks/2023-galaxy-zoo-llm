# Dataset pre-processing scripts


## Requirements

```
pip install selenium tqdm 
```


## Usage

We first generate a list of all the URLs of the images we want to download. This is done by running the following command:

```bash
python scrap_urls.py -n 1000
```

where -n is the number of pages to scrap. Each page contains 10 conversations. The URLs will be stored in a file called `talks_urls.csv`.

Then, we download the images using the following command:

```bash
python scrap_notes.py 
```
This will generate a new directory called `talks_dset` containing all the images.
