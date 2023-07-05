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
Answer:
"""