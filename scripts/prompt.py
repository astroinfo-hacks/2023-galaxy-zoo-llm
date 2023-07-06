PROMPT_DESC = """
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

PROMPT_CONV = """
You are an AI assistant specialising in astronomical topics. 
You are provided with the following conversation between galaxy zoo users 
that comment on an astronomical image. Unfortunately, you do not have access 
to the actual image.
Conversation:
------
%s
------
End of conversation.
Design a conversation between you and a person asking about this photo. 
The answers should be in a tone that a visual AI assistant is seeing the 
image and answering the question. Ask diverse questions and give corresponding answers.

Below are the requirements for generating the questions:
1. You can get inspiration from the Galaxy Zoo Decision tree for asking the questions about 
morphology of the galaxy.\
2. Do not ask the redshift of the galaxy, as you can not measure the redshift of the galaxy 
just from the image.\ 
3. Focus on the visual aspects of the image such as size, 
position of the galaxy in the image, special features, morphology, artifacts
that can be inferred without the text information. \

Below are the requirements for generating the answers:
1. Avoid quoting or referring to specific facts, terms, abbreviations, dates, numbers, or
names. 
2. Do not use phrases like "mentioned", "caption", "context", "text" in the conversation. Instead,
refer to the information as being "in the image." \
3. Avoid referring to "based on the conversation" in answers. \
4. Avoid giving answers when there is not enough information. \


Please come up with a set four of user questions and assistant answers about that image.

Here is one example of questions and answers: 

human: What do you see in the image? \
gpt:  This image shows a spiral galaxy.\
human: How tightly wound the spiral arm appears? \
gpt: Arms appear to be mediumly bound. \
human: How many spiral arms are there? \
gpt: There are four arms. \
human: How prominent is the central buldge, compared to rest of the galaxy?
gpt: Obvious. \
human: Is there anything odd? \
gpt: It appears to be disturbed. \

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
"""

QUESTIONS_V0 = [
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
