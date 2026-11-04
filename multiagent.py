import os 
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def run_agent(role,content):
    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.4,
        messages=[
            {
                "role":"system",
                "content":role
            },
            {
                "role":"user",
                "content":content
            }
        ]
    )

    return response.choices[0].message.content


topic = input("Enter a Topic :")

# AGent 1 - Research Agent

print(f"Research Work Start on this topic {topic}")
research_content = run_agent(
    "You are a Professional Research Agent responsible for conducting in-depth research on given topics using credible and reliable sources. Gather, verify, and analyze relevant facts, statistics, and insights, ensuring accurate, well-structured, and evidence-based research.generate every article in approximately 200 words.Keep the content concise, informative, engaging, and grammatically correct.",
    f"Research topic is {topic}"
)
print("Research Agent Task is Complete ....")

# print ("Research Outcomes : ", research_content)

# AGent 2 - writer Agent
print(f"Writing Work Start on this topic {topic}")

draft_article = run_agent(
    "You are a Professional Content Writer Agent responsible for creating original, engaging, informative, and SEO-friendly articles based on research and provided topics. Write clear, well-structured, reader-friendly content with compelling headlines, meaningful sections, and practical insights. Generate every article in approximately 200 words.Keep the content concise, informative, engaging, and grammatically correct.",
    f"here is research content :{research_content}"
)

# print(f"Write Agent Outcomes (Draft Article): , {draft_article}")
print("Writing Agent Task is Complete ....")


# AGent 3 - editor Agent
print(f"Editing Work Start on this topic {topic}")

final = run_agent(
    "You are a Professional Article Editor responsible for reviewing, refining, and formatting articles into a polished, professional, publication-ready format. Correct grammar, spelling, punctuation, sentence structure, and readability while improving headings, paragraphs, flow, and consistency without changing the original meaning. Ensure the final article looks professional, engaging, well-organized, and SEO-friendly.generate every article in approximately 200 words.Keep the content concise, informative, engaging, and grammatically correct.",
    f"here is draft article article : {draft_article}"
)

print(f"Here Final Article : ", final)