import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

to = input("Enter to Email :")
subject = input("Enter Email Subject :")
reason = input("Enter Vaild Reason :")
tone = input("Enter Tone :")

reponse = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.7,
    max_tokens=300,
    messages=[
        {
            "role":"system",
            "content":"You are an experience Smart Email Writer. your task is generate a email based on user inputs and make sure response generate based on user input not use other word which are not present in user input... don't use extra word.."
        },
        {
            "role":"user",
            "content":f"Write {subject} email to {to} and {reason} and use this tone {tone}."
        },
    ]
)

print(reponse.choices[0].message.content)