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
        summary = openai.Completion.create(
            model="text-davinci-003",
            prompt="""Given the following conversation between galaxy zoo users that comment on an 
            astronomical image, answer the following question about this image making sure to include 
            as much information as possible.
            Conversation:
            ---
            %s
            ---
            Question: What do we see in this image?
            Answer:""" % dataset[i]['conversations'],
            max_tokens=256
        ).choices[0].text

        question_and_answer = [{"from": "human", "value": "What do we see in this image?"}, {"from": "gpt", "value": summary}]
        obj = {
            "id": dataset[i]['id'],
            "image": f"{dataset[i]['id']}.png",
            "conversations": question_and_answer
        }

        data.append(obj)
        print("Success")

    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate summaries for dataset')
    parser.add_argument('n', type=int, help='Number of summaries to generate')
    parser.add_argument('--input', type=str, default='../data/zoo_convos.json', help='Path to input dataset')
    parser.add_argument('--output', type=str, default='../data/first_results.json', help='Path to save output JSON')

    args = parser.parse_args()

    api_key = load_api_key()
    dataset = load_dataset(args.input)
    summaries = generate_summaries(api_key, dataset, args.n)
    write_to_json(summaries, args.output)
