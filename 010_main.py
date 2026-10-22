import os
import json
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key = os.getenv("MISTRAL_API_KEY"))

response = client.chat.complete(
    model = "mistral-small-latest",
    temperature = 0.4,
    response_format = {"type":"json_object"},
    messages=[
        {
            "role":"system",
            "content":"Make sure u provide response in json format : sentiment(postivite, nageative) , rating score(out of 5), summarize (string)"
        },
        {
            "role":"user",
            "content":"your product quality is good but delivery is late.."
        },
    ]
)

# print(response.choices[0].message.content)
raw = response.choices[0].message.content
print(raw)
try:
    data = json.loads(raw)
    print(data["sentiment"])
    print(data["rating_score"])
    print(data["summarize"])
except json.JSONDecodeError:
    print("Error while parse to json..")