from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
import urllib
import os

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("input", 'talk_urls.csv', "File containing the urls of the talk pages")
flags.DEFINE_string("output_path", "talks_dset", "Path to save the outputed data in a format hugginface will understand")


def retrieve_conversation(driver, unique_id, url):
    # Opening the page with the driver
    driver.get(url)
    
    # Find the first image
    elements = driver.find_elements(By.CLASS_NAME, "polaroid-image")
    image = elements[0].find_element(By.TAG_NAME, "img")
    # download the image using urllib and save it with name made from unique_id
    image_name = FLAGS.output_path+"/%d.png"%unique_id
    urllib.request.urlretrieve(image.get_attribute("src"), image_name)

    # Retrieve the conversation
    elements = driver.find_elements(By.CLASS_NAME, "talk-comment-content")
    # For each comment get the text associated with it and print it
    convo = ""
    for e in elements:
        t = e.find_elements(By.CLASS_NAME, "markdown")
        t = " ".join([x.text for x in t])
        # Remove usernames starting with @ from t 
        t = " ".join([x for x in t.split(" ") if not x.startswith("@")])
        convo += "User: " + t + "\n\n"

    return {'unique_id': unique_id, 'conversation': convo, 'file_name': image_name}

# Build executable main function that will be called from the command line 
def main(argv):
    del argv

    # Check if the output path exists, if not create it
    if not os.path.exists(FLAGS.output_path):
        os.makedirs(FLAGS.output_path)

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(20);

    # Load the csv of urls from file into a pandas db
    df = pd.read_csv(FLAGS.input)
    # For each url retrieve the conversation and put it in a pandas dataframe with a for loop
    conversations = []
    for i in tqdm(range(len(df))):
        try:
            conversations.append(retrieve_conversation(driver, df.loc[i, "unique_id"], df.loc[i, "url"]))
        except:
            print("Error with %d"%df.loc[i, "unique_id"])
            continue
    # Save the dataframe
    convo_df = pd.DataFrame(conversations)

    # merge the dataframes and save it
    df = pd.merge(df, convo_df, on="unique_id")
    df.to_csv(FLAGS.output_path+"/metadata.csv", index=False)
    
    # Close the driver
    driver.close()

if __name__ == "__main__":
    app.run(main)
