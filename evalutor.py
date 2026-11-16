import os
from mistralai.client import Mistral
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

question_input = input("Etner Your Question : ")

response = mistral_client.chat.complete(
    model = "mistral-small-latest",
    temperature = 0.6,
    messages = [
        {
            "role":"user",
            "content":question_input
        }
    ]
)

mistral_outcome = response.choices[0].message.content

print(f"MiSTRAL O?P : {mistral_outcome}")

def evalutor_LLM(question,answer):

    evalutor_prompt = f"""
        You are a Strict Evalutor , 
        rate this question: {question} and 
        answer : {answer}

        after evaluate return response with evaluate score and short summary 
    """

    groq_outcome = groq_client.chat.completions.create(
        model = "openai/gpt-oss-20b",
        messages=[
            {
                "role":"user",
                "content":evalutor_prompt
            }
        ]
    )

    return groq_outcome.choices[0].message.content



evalutor_outcome = evalutor_LLM(question_input,mistral_outcome)


print(f"EValute : {evalutor_outcome}")