import os
import json
import openai
from absl import app, flags
from tqdm import tqdm
from multiprocessing import Pool
import random
import time

# Define the command line arguments
flags.DEFINE_string('input', 'galaxyzoo_dataset/metadata.json', 'Path to the input JSON file')
flags.DEFINE_string('output', 'galaxyzoo_dataset/qa.json', 'Path to the output JSON file')


FLAGS = flags.FLAGS

detail_describe_instructions = [
    "Describe the following image in detail.",
    "Provide a detailed description of the given image.",
    "Give an elaborate explanation of the image you see.",
    "Share a comprehensive rundown of the presented image.",
    "Offer a thorough analysis of the image.",
    "Explain the various aspects of the image before you.",
    "Clarify the contents of the displayed image with great detail.",
    "Characterize the image using a well-detailed description.",
    "Break down the elements of the image in a detailed manner.",
    "Walk through the important details of the image.",
    "Portray the image with a rich, descriptive narrative.",
    "Narrate the contents of the image with precision.",
    "Analyze the image in a comprehensive and detailed manner.",
    "Illustrate the image through a descriptive explanation.",
    "Examine the image closely and share its details.",
    "Write an exhaustive depiction of the given image.",
]

concise_describe_instructions = [
    "Describe the following image concisely.",
    "Provide a brief description of the given image.",
    "Offer a succinct explanation of the picture presented.",
    "Summarize the visual content of the following image.",
    "Give a short and clear explanation of the subsequent image.",
    "Share a concise interpretation of the image provided.",
    "Present a compact description of the photo's key features.",
    "Relay a brief, clear account of the picture shown.",
    "Render a clear and concise summary of the photo below.",
    "Write a terse but informative summary of the following picture.",
    "Create a compact narrative representing the image presented.",
]

prompt_pool = detail_describe_instructions + concise_describe_instructions


def load_dataset(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_to_json(data, output_path):
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_answer(entry):
    conversation = ""
    for j in range(len(entry['conversations'])):
        conversation += "User: " + entry['conversations'][j]['value'] + "\n\n"

    # Extract a random question from prompt pool
    question = prompt_pool[random.randint(0, len(prompt_pool) - 1)]


    prompt = """
You are an AI assistant specialising in astronomical topics. 
You are provided with the following conversation between galaxy zoo users 
that comment on an astronomical image. Unfortunately, you do not have access to the actual image.
Conversation:
------
%s
------
End of conversation.
Answer the question asked below between you and a person asking about this photo. 
The answers should be in a tone that a visual AI assistant is seeing the 
image and answering the question. 

Below are the requirements for generating the answer:
1. Avoid quoting or referring to specific facts, terms, abbreviations, dates, numbers, or
names, as these may reveal the conversation is based on the text information, rather than
the image itself. Focus on the visual aspects of the image that can be inferred without
the text information. \
2. Do not use phrases like "mentioned", "caption", "context" in the conversation. Instead,
refer to the information as being "in the image." \
3. Do not use your knowledge to interpret the image and keep the answers short. \

Now, please respond to the question below as if you were describing the image in the style of a professional astronomer.

Question: %s
Answer:""" % (conversation,question)

    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{'role': 'user', 'content': prompt}],
                temperature=0,
           )
            question_and_answer = [{"from": "human", "value": question}, {"from": "gpt", "value": response['choices'][0]['message'].content}]

            obj = {
                "id": "{}".format(entry['id']),
                "image": "{}.png".format(entry['id']),
                "conversations": question_and_answer
            }

            return obj
        except openai.error.RateLimitError:
            pass
        except Exception as e:
            print(e)
        time.sleep(1)
        
def generate_summaries(dataset):
    
    data = []

    # Use multiprocessing to parallelize the generation of summaries by calling call_api over a list of prompts
    with Pool(4) as pool:
        for result in tqdm(pool.imap(get_answer, dataset), total=len(dataset), desc="Generating QA"):
            data.append(result)
    return data

# Define the main function
def main(_argv):

    # Load the API key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Load input JSON file
    dataset = load_dataset(FLAGS.input)

    # Generate the summaries
    summaries = generate_summaries(dataset)

    # Write the summaries to the output JSON file
    write_to_json(summaries, FLAGS.output)


if __name__ == "__main__":
    app.run(main)