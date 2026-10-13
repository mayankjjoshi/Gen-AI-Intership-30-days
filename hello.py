from mistralai.client import Mistral
from dotenv import load_dotenv
import os

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

response = client.chat.complete(
    model="mistral-small-latest",
    temperature = 0.2,
    messages=[
        {
            "role":"system",
            "content":"""
            You are a customer support chatbot for indian food industry and your hotel name is Kismat Kathiywadi. keep answer short prciese and tone calmness , polite, sweet tone.
            few examples answer based on this pattern :
            input : Services is good , food is bad
            output : neutral
            input : deilvery on time, taste is good
            output : postive
            input : staff is bad, need improvemnet in parking
            output : negative
            input : vibe is good, interior is good
            output : positive

            keep reponse in above format.also append one summarize senetnece based on user input with reponse.
            """
        },
        {
            "role":"user",
            "content":"kaju sabji is delcious but it is very cold and naan is very hard. but price is very low."
        }
    ]
)

print(response.choices[0].message.content)