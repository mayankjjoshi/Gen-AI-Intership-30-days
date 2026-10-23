import streamlit as st
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

# st.title("GEN AI Session..")
# st.header("Chapter 7 Token and Cost Control and streaming ...")
# st.write("Every API Costs Money ..")
# st.warning("You hit API Limit...")
# st.success("Congrats you become a father..")

# # input 

# address = st.text_area("Enter your Address")
# gfname = st.text_input("ENter your gf name ")
# age = st.slider("Enter your age",0,100,25)
# mood = st.selectbox("Mood", ["Happy","angry","bad"])


# if st.button("submit"):
#     print(address,gfname, age ,mood )
#     st.success("your data is submiited")


client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

st.title("AI SUMMARIZER")
user_input = st.text_area("Enter your text to summarize")

if st.button("Summarize"):
    if not user_input.strip():
        st.warning("Please enter some text to summarize.")
    else:
        with st.spinner("Loading .."):
            response = client.chat.stream(
                model="mistral-small-latest",
                temperature=0.6,
                messages=[
                    {
                        "role": "system",
                        "content": "you are an AI summarizer, your task to summarize large data in small format make sure not use external other then provided input.. sumamrize in 3 bullet points"
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )

            def token_stream():
                for chunk in response:
                    content = chunk.data.choices[0].delta.content
                    if content:
                        yield content

            st.write_stream(token_stream())