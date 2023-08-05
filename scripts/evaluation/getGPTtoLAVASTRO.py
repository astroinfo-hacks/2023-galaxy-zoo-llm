import json

# Read in file (1)
with open('llavastro.jsonl', 'r') as file1:
    data1 = file1.readlines()

# Read in file (2)
with open('qa.json', 'r') as file2:
    data2 = json.load(file2)

# Create an empty list to store the matching entries
output = []

# Iterate over entries in file (1)
for line in data1:
    entry = json.loads(line)
    question_id = entry['image_id']
    
    # Search for matching entry in file (2)
    for item in data2:
        if item['id'] == str(question_id):
            entry2 = item.copy()
            entry2['answer'] = entry
            output.append(entry2)
            break

# Write the output to a JSON file
with open('ABCOUT.json', 'w') as outfile:
    json.dump(output, outfile)

# Create a set of all image_ids from qa.json
image_ids = {item['id'] for item in data2}

# Filter out entries in data1 that don't have a corresponding image_id in data2
filtered_data1 = [line for line in data1 if json.loads(line)['image_id'] in image_ids]

# Write the filtered data to a new file
with open('llavastro_cleared.jsonl', 'w') as outfile:
    outfile.writelines(filtered_data1)