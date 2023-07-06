import json

# Read the first JSON file
with open('abcout.json') as file:
    data = json.load(file)

# Initialize empty lists
ids = []
questions = []
responses = []

# Iterate over the data
for item in data:
    # Extract ID
    id = item['id']
    ids.append(id)

    # Extract conversations
    conversations = item['conversations']

    # Extract question and response from each conversation
    for conversation in conversations:
        if conversation['from'] == 'human':
            question = conversation['value']
        elif conversation['from'] == 'gpt':
            response = conversation['value']

    questions.append(question)
    responses.append(response)

# Read the second JSON file
with open('questionsl.json') as file:
    question_data = file.readlines()

# Initialize empty list
question_ids = []

# Extract question IDs from the second JSON file
for question in questions:
    question_id = None
    for line in question_data:
        data = json.loads(line)
        if data['text'] == question:
            question_id = data['question_id']
            question_ids.append(question_id)
            break

print(question_id)
# Print the first 10 questions and question IDs
print("First 10 Questions:")
for question in questions[:10]:
    print(question)

print("\nFirst 10 Question IDs:")
print(question_ids[:10])


# Create a list to hold the formatted data
formatted_data = []

# Iterate over the arrays and format the data
for i in range(len(ids)):
    data = {
        "answer_id": ids[i],
        "model_id": "gpt-3.5-turbo:20230327",
        "question_id": question_ids[i],
        "text": responses[i],
        "metadata": {}
    }
    formatted_data.append(data)

# Convert the formatted data to a JSON string with line breaks
json_data = "\n".join(json.dumps(entry) for entry in formatted_data)

# Write the formatted data to a JSON file
with open('formatted_data.json', 'w') as file:
    file.write(json_data)