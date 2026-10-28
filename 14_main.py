# chat with pdf 

from pypdf import PdfReader
import chromadb
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

# read pdf and extract text

reader = PdfReader("sample.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# chunking 

def chunks_text(text,chunk_size=1000, overlap=200):
    start = 0
    chunks = []
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks

chunks = chunks_text(text)
print(chunks)

# embedding and store in db

chroma_client = chromadb.Client()
collection = chroma_client.create_collection("pdf")

# for i in range(len(chunks)):
#     print(str(i))

collection.add(
    documents = chunks,
    ids=[str(i) for i in range(len(chunks))],
)

# user input 

user_input = input("Ask question to pdf :")

relevant = collection.query(
    query_texts=[user_input],
    n_results = 4
)
print(relevant)
print(relevant["documents"])
# injection + generation

context = relevant["documents"][0]
user_prompt = f"""
provide answer based on user input based on below context only :
{context}
and make sure answer provide only from context if you don't know just replied with "I don't Know"

here is question : {user_input}
"""

client = Mistral(api_key = os.getenv("MISTRAL_API_KEY"))

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.6,
    messages=[
        {
            "role":"user",
            "content":user_prompt,
        },
    ]
)

print(response.choices[0].message.content)