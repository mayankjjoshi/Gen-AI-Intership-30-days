import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

response = client.chat.stream(
    model = "mistral-small-latest",
    temperature = 0.4,
    messages = [
        {
            "role":"user",
            "content":"write an article on AI destruction.."
        },
    ],
)

# print(response.choices[0].message.content)

for chunks in response:
    content = chunks.data.choices[0].delta.content
    if content:
        print(content , end=" ")