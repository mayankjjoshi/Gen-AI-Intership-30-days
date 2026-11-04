import os
from mistralai.client import Mistral
from dotenv import load_dotenv


load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def run_agent(role,content):
    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.5,
        messages=[
            {
                "role":"system",
                "content":role,
            },
            {
                "role":"user",
                "content":content
            }
        ]
    )

    return response.choices[0].message.content


topic = input("Enter a Topic : ")

print("Single Agents Start Working ...")

result = run_agent(
    """You are a Senior Article Researcher, Writer, and Editor responsible for the complete article creation process. Research topics thoroughly, verify facts using credible sources, and write original, engaging, SEO-friendly, high-quality articles., Edit and proofread every article for accuracy,grammar, clarity, readability, and structure before delivering publication-ready content. Here is topic to generate article : """,
    f"write a article in short on this topic :{topic}"
)

print(result)