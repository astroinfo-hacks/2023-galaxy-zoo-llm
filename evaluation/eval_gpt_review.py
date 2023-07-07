import argparse
import json
import os
import time

import openai
import ray

@ray.remote(num_cpus=4)
def get_eval(content, max_tokens, model):
    sleep_time = 1
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': 'You are a helpful and precise assistant for checking the quality of the answer.'},
                    {'role': 'user', 'content': content}
                ],
                temperature=0.2,
                max_tokens=max_tokens
            )
            return response['choices'][0]['message']['content']
        except openai.error.RateLimitError:
            pass
        except Exception as e:
            print(e)
        time.sleep(sleep_time)

class ChatEvaluator:

    def __init__(self, max_tokens=1024, model='gpt-3.5-turbo'):
        self.max_tokens = max_tokens
        self.model = model
        self.sleep_time = 1
        ray.init()

    @staticmethod
    def parse_score(review):
        try:
            score_pair = review.split('\n')[0].replace(',', ' ').split()
            if len(score_pair) == 2:
                return [float(score_pair[0]), float(score_pair[1])]
            else:
                print('error', review)
                return [-1, -1]
        except Exception as e:
            print(e)
            print('error', review)
            return [-1, -1]

    def evaluate(self, question_path, answer_list_paths, context_path, rule_path, output_path):
        with open(os.path.expanduser(rule_path), 'r') as f:
            rule_dict = json.load(f)

        with open(os.path.expanduser(context_path), 'r') as f:
            context_list = [entry["conversations"] for entry in json.load(f)]

        review_file = open(output_path, 'w')

        js_list = []
        handles = []
        idx = 0

        with open(os.path.expanduser(question_path)) as f_q, \
                open(os.path.expanduser(answer_list_paths[0])) as f_ans1, \
                open(os.path.expanduser(answer_list_paths[1])) as f_ans2:

            for ques_js, ans1_js, ans2_js, conv in zip(f_q, f_ans1, f_ans2, context_list):
                ques = json.loads(ques_js)
                ans1 = json.loads(ans1_js)
                ans2 = json.loads(ans2_js)

                category = ques['category']

                if category in rule_dict:
                    print('category', category)
                    rule = rule_dict[category]
                else:
                    assert False, f"Visual QA category not found in rule file: {category}."

                prompt = rule['prompt']
                role = rule['role']
                content = (
                        f'[Context]\n{conv}\n\n'
                        f'[Question]\n{ques["text"]}\n\n'
                        f'[{role} 1]\n{ans1["text"]}\n\n[End of {role} 1]\n\n'
                        f'[{role} 2]\n{ans2["text"]}\n\n[End of {role} 2]\n\n'
                        f'[System]\n{prompt}\n\n')

                js_list.append({
                    'id': idx + 1,
                    'question_id': ques['question_id'],
                    'answer1_id': ans1.get('answer_id', ans1['question_id']),
                    'answer2_id': ans2.get('answer_id', ans2['answer_id']),
                    'category': category})

                idx += 1
                handles.append(get_eval.remote(content, self.max_tokens, self.model))
                time.sleep(self.sleep_time)

        reviews = ray.get(handles)

        for idx, review in enumerate(reviews):
            scores = self.parse_score(review)
            js_list[idx]['content'] = review
            js_list[idx]['tuple'] = scores
            review_file.write(json.dumps(js_list[idx]) + '\n')

        review_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ChatGPT-based QA evaluation.')
    parser.add_argument('-q', '--question', required=True)
    parser.add_argument('-c', '--context', required=True)
    parser.add_argument('-a', '--answer-list', nargs='+', required=True)
    parser.add_argument('-r', '--rule', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('--max-tokens', type=int, default=1024, help='maximum number of tokens produced in the output')

    args = parser.parse_args()

    evaluator = ChatEvaluator(max_tokens=args.max_tokens)
    evaluator.evaluate(args.question, args.answer_list, args.context, args.rule, args.output)
