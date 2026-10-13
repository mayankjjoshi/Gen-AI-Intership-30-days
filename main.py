import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

response = client.chat.complete(
    model="mistral-small-latest",   
    messages=[
        {
            "role":"user",
            "content":"who virat kohil?"
        }
    ],
)

print(response)
print(response.choices[0].message.content)