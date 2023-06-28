from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_integer("n", 1, "Number of pages to scrap")

# Accessing the page from GalaxyZoo
base_url = "https://www.zooniverse.org"
home = "/projects/zookeeper/galaxy-zoo/talk/1267"


def retrieve_talk_urls(driver, page_id):
    # Opening the page with the driver
    driver.get(base_url+home+"?page="+str(page_id))
    # Find all elemnts 
    elements = driver.find_elements(By.CLASS_NAME, "talk-discussion-preview")
    # Extract the urls, number of participants, and number of comments
    for e in elements:
        url = e.find_element(By.TAG_NAME, "h1").find_element(By.TAG_NAME, "a").get_attribute("href")
        unique_id = url.split("/")[-1]
        comments = int(e.text.split("\n")[-1].split(" ")[0])
        participants = int(e.text.split("\n")[-2].split(" ")[0])
        yield unique_id, url, comments, participants


def build_talk_database(driver, n_pages):
    df = pd.DataFrame(retrieve_talk_urls(driver, 1), columns=["unique_id", "url", "comments", "participants"])
    # Do a for loop aggregating the dataframes 
    for i in tqdm(range(2, n_pages+1)):
        # Append the pandas dataframe from generator or urls
        try:
            df = pd.concat([df, pd.DataFrame(retrieve_talk_urls(driver, i), columns=["unique_id", "url", "comments", "participants"])])
        except:
            print("Error with page %d"%i)
            continue
    return df


# Build executable main function that will be called from the command line 
def main(argv):
    del argv
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(20);
    # Build the dataframe
    df = build_talk_database(driver, FLAGS.n)
    # Save the dataframe
    df.to_csv("talk_urls.csv", index=False)
    # Close the driver
    driver.close()

if __name__ == "__main__":
    app.run(main)
