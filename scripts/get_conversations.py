import os
import json
import openai
import argparse

def load_api_key():
    return os.getenv("OPENAI_API_KEY")

def load_dataset(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_to_json(data, output_path):
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

def generate_summaries(api_key, dataset, n):
    openai.api_key = api_key
    data = []

    for i in range(n):
        
        prompt = """You are an AI assistant specialising in astronomical topics. 
            You are provided with the following conversation between galaxy zoo users 
            that comment on an astronomical image. Unfortunately, you do not have access 
            to the actual image.
            You are provided with the following conversation between galaxy zoo users 
            that comment on an astronomical image. Unfortunately, you do not have access to the actual image.
            Conversation:
            ------
            %s
            ------
            End of conversation.
            Design a conversation between you and a person asking about this photo. 
            The answers should be in a tone that a visual AI assistant is seeing the 
            image and answering the question. Ask diverse questions and give corresponding answers.

            Below are the requirements for generating the questions and answers in the conversation:
            1. Avoid quoting or referring to specific facts, terms, abbreviations, dates, numbers, or
            names, as these may reveal the conversation is based on the text information, rather than
            the image itself. Focus on the visual aspects of the image that can be inferred without
            the text information. \
            2. Do not use phrases like "mentioned", "caption", "context" in the conversation. Instead,
            refer to the information as being "in the image." \
            3. Ensure that questions are diverse and cover a range of visual aspects of the image.
            The conversation must include 2 questions and 2 answers about thevisual aspects of the image. \
            4. Do not use your knowledge to interpret the image and keep the questions and answers short. \
            5. Please come up with a set of 2 user questions and assistant answers about that image.

            For example, you have this User-Assistant set of questions.
            human: What can you see in this image? \
            gpt: There are two galaxies merging. \
            human: Is one of the galaxies a smaller galaxy? \
            gpt: It appears so.

            Please respond with a json file format like this:
            [
                {
                    "from": "human",
                    "value": human question,
                },
                {
                    "from": "gpt",
                    "value": gpt response,
                }
            ]

            where human question and gpt response are the question and answer generated.
            """ % dataset[i]['conversations']

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0,
        )


        obj = {
            "id": "{}".format(dataset[i]['id']),
            "image": "{}.png".format(dataset[i]['id']),
            "conversations": json.loads(response['choices'][0]['message'].content)
        }
        data.append(obj)
        print("Success")

    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate summaries for dataset')
    parser.add_argument('n', type=int, help='Number of summaries to generate')
    parser.add_argument('--input', type=str, default='../data/zoo_convos.json', help='Path to input dataset')
    parser.add_argument('--output', type=str, default='../data/first_results_convos.json', help='Path to save output JSON')

    args = parser.parse_args()

    api_key = load_api_key()
    dataset = load_dataset(args.input)
    summaries = generate_summaries(api_key, dataset, args.n)
    write_to_json(summaries, args.output)
