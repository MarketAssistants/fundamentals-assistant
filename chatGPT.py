import os
import openai
#key: sk-dpxZijUs4TYour6O1eluT3BlbkFJh63j60HVnXO6qkxY1y72
#reference docs: https://platform.openai.com/docs/api-reference/authentication

openai.organization = "org-yg98NTQ2h1KWEJW6WALSfHkC"
os.environ["OPENAI_API_KEY"] = "sk-dpxZijUs4TYour6O1eluT3BlbkFJh63j60HVnXO6qkxY1y72"
openai.api_key = os.getenv("OPENAI_API_KEY")
models = openai.Model.list()
# print(models[0])
models_id = [model['id'] for model in models['data']]

# print(models_id)

# conversation = []
# initial_prompt = "You: Hello, ChatGPT! How can you assist me today?\nChatGPT:"
# conversation.append(initial_prompt)

response = openai.ChatCompletion.create(
    model="davinci",  # Choose the appropriate model
    messages=[
        {"role": "system", "content": "You are a helpful assistant for text classification."},
        {"role": "user", "content": "Classify the sentiment of this text: 'I love this product!'"},
        {"role": "assistant", "content": ""}
    ]
)

# Extract the assistant's reply
assistant_reply = response['choices'][0]['message']['content']

print("Assistant's reply:", assistant_reply)

##Good attemps but it is not free
##getting this error: openai.error.RateLimitError: You exceeded your current quota, please check your plan and billing details.