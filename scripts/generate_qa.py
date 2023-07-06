import os
import json
import time
import openai
from multiprocessing import Pool
from tqdm import tqdm
import importlib
import random
import copy
import argparse


MAX_TOKENS = 2048


class QAGenerator:

    def __init__(self, input_path: str, output_path: str, prompt_path: str, mode: str, n_inputs: int = -1, n_processes: int = 4) -> None:
        self.dataset = self.load_dataset(input_path, n_inputs)
        self.output_path = output_path
        self.n_processes = n_processes
        module = self.load_module(prompt_path)
        assert mode in ['conv', 'desc', 'both'], "Mode must be either 'conv' or 'desc' or 'both but received {mode}".format(mode=mode)
        self.mode = mode
        if mode == 'desc':
            self.prompt = module.PROMPT_DESC
            self.questions = module.QUESTIONS_V0
        elif mode == 'conv':
            self.prompt = module.PROMPT_CONV
            self.questions = None
        #elif mode == 'both':

    def load_module(self, path: str):
        """
        Allows to load variables from questions.py and prompt.py.
        """
        spec = importlib.util.spec_from_file_location("settings", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def load_dataset(self, input_path: str, n_inputs: int = -1) -> list[dict]:
        """
        Load the galaxy-zoo json dataset. If specified, a random subset of the dataset is returned.
        """
        with open(input_path, 'r') as file:
            dataset = json.load(file)
        if 0 < n_inputs < len(dataset):
            return random.sample(dataset, n_inputs)
        else:
            return dataset

    def write_to_json(self, data: list, output_path: str):
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)

    def concat_conversation(self, entry: dict) -> str:
        """
        Convert the conversation into a single string. Each user is separated with '\n\nUser:'.
        If the conversation is not a string or is too long, respectectively discard or crop the conversation.
        """
        conversation = ""
        for j in range(len(entry['conversations'])):
            conversation += "User: " + entry['conversations'][j]['value'] + "\n\n"

        # If conversation is a string
        if not isinstance(conversation, str):
            conversation = ""

        # Maximum number of tokens you can send to this model is 2,048 tokens per request.
        # TODO: check the size of the conversation

        return conversation
    
    def get_question(self) -> str:
        if self.mode == 'desc':  # V0
            return self.questions[random.randint(0, len(self.questions) - 1)]
        elif self.mode == 'conv':  # V1
            return None

    def get_answer_from_gpt(self, entry: dict) -> list[dict]:
        """
        Send the content to GPT and return the answer into a question/answer format.
        """
        conversation = self.concat_conversation(entry)
        question = self.get_question()
        if self.mode == "desc":
            content = copy.deepcopy(self.prompt) % (conversation, question)
        elif self.mode == "conv":
            content = copy.deepcopy(self.prompt) % conversation

        while True and len(conversation) > 0:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{'role': 'user', 'content': content}],
                    temperature=0,
                )

                answer = response['choices'][0]['message'].content

                if self.mode == "desc":  # V0
                    question_and_answer = [{"from": "human", "value": question}, {"from": "gpt", "value": answer}]
                elif self.mode == "conv":  # V1
                    question_and_answer = json.loads(answer)
                    

                obj = {
                    "id": "{}".format(entry['id']),
                    "image": "{}.png".format(entry['id']),
                    "conversations": question_and_answer
                }

                return obj
            
            except openai.error.RateLimitError:
                # While GPT is not responding due to rate limit...
                pass
            except Exception as e:
                print(e)
                conversations = conversations[:-2]
            
            time.sleep(1)
        
        return None

    def generate(self) -> list[dict]:
        """
        Run the generation of questions and answers.
        Use multiprocessing to parallelize the generation of summaries by calling call_api over a list of prompts.
        """
        data = []
        with Pool(self.n_processes) as pool:
            for result in tqdm(pool.imap(self.get_answer_from_gpt, self.dataset), total=len(self.dataset), desc="Generating QA"):
                if result is not None:
                    data.append(result)
                # Write to json every 100 answers
                if len(data) % 100 == 0:
                    self.write_to_json(data, self.output_path)
        self.write_to_json(data, self.output_path)

        return data


# Define the main function
def main(args):
    # Load the API key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    qa_generator = QAGenerator(args.input_path, args.output_path, args.prompt_path, args.mode, args.n_inputs, args.n_processes)
    qa_generator.generate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str, default="./")
    parser.add_argument("--output-path", type=str, default="./")
    parser.add_argument("--prompt-path", type=str, default="./")
    parser.add_argument("--mode", type=str, default="conv")
    parser.add_argument("--n-inputs", type=int, default=-1)
    parser.add_argument("--n-processes", type=str, default=4)
    args = parser.parse_args()

    main(args)