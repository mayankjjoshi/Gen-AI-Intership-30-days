import os 
import streamlit as st
from pypdf import PdfReader
import chromadb
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+chunk_size])
        start += chunk_size - overlap
    return chunks

st.title("Documents Q&A (RAG)")

files = st.file_uploader("Upload Pdfs", type="pdf", accept_multiple_files=True)

if files and st.button("Process Documents"):
    chroma = chromadb.Client()
    collection = chroma.get_or_create_collection("rag_pdf")

    documents = []
    metadatas = []
    ids = []
    chunk_id = 0
    for f in files:
        reader = PdfReader(f)
        text = "".join(page.extract_text() for page in reader.pages)
        for chunk in chunk_text(text):
            documents.append(chunk)
            metadatas.append({"source":f.name})
            ids.append(str(chunk_id))
            chunk_id += 1
    
    collection.add(
        documents = documents,
        metadatas = metadatas,
        ids = ids
    )

    st.session_state.collection = collection
    st.success(f"Indexed {len(documents)} chunks from {len(files)} files")

question = st.text_input("Ask a Question :")
if question and "collection" in st.session_state:
    results = st.session_state.collection.query(
        query_texts=[question],
        n_results=4
    ) 
    chunks = results["documents"][0]
    sources = results["metadatas"][0]

    context = "\n\n".join(chunks)
    prompt = f"""Answer using only the context below. If not there, say "I don't Know."
    Context :{context}
    
    Question : {question}
    """
    with st.spinner("Thinking ..."):
        response = client.chat.complete(
            model = "mistral-small-latest",
            temperature = 0.2,
            messages = [
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )
    
    st.write(response.choices[0].message.content)

    st.caption("Sources : " + ", ".join(set(s["source"] for s in sources)))