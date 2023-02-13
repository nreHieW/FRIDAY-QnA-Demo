import streamlit as st
from pdf_helpers import *
from models import *
from transformers import pipeline
from streamlit_chat import message as st_message
import requests

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

def query(HF_TOKEN, question, context):

    prompt = f'''
    You are a customer service chatbot. Answer the question with the following context. 
    If the question cannot be answered using the information provided, reply with "no answer".

    Context: {context}

    Question: {question}
    Answer:
    '''
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@st.cache
def create_embeddings(full_text):
    embeddings = EmbeddingModel()
    embeddings.load_data(full_text)
    embeddings.create_mappings(240)
    return embeddings

def get_file():
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file:
        return uploaded_file

def app():
    HF_TOKEN = st.sidebar.text_input("Input AI Token", "")
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    uploaded_file = get_file()
    question = st.text_input("Question", "")
    if uploaded_file is not None:
        rawfile = uploaded_file.read()
        container = displayPDF(rawfile) # Unedited 

        full_text = get_all_text(rawfile)
        embeddings = create_embeddings(full_text)

        if question:
            if not question.endswith("?"):
                question += "?"
            context = embeddings.get_closest(question)
            edited = highlight_pdf(rawfile, context)
            result = query(HF_TOKEN, question, context)
            st.session_state.past.append(question)
            st.session_state.generated.append(result[0]["generated_text"])
            if st.session_state['generated']:
                for i in range(len(st.session_state['generated'])-1, -1, -1):
                    st_message(st.session_state["generated"][i], key=str(i))
                    st_message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            
            displayPDF(edited, container)
    else:       
        for key in st.session_state.keys():
            del st.session_state[key]

if __name__ == "__main__":
    app()