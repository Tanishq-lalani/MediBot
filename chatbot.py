import streamlit as st
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_FAISS_PATH="vectorstore/db_faiss"
@st.cache_resource
def get_vectorstore():
    embedding_model=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db=FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db


def set_custom_prompt(custom_prompt_template):
    prompt=PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt

HF_TOKEN=os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID="Qwen/Qwen2.5-1.5B-Instruct"

def load_llm(huggingface_repo_id):
    llm = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        task="conversational",
        max_new_tokens=512
    )
    chat_llm = ChatHuggingFace(llm=llm)
    return chat_llm

def main():
    st.title("Ask Chatbot! ")
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt = st.chat_input("Pass your Prompt here")
    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({"role":'user', 'content': prompt})
        CUSTOM_PROMPT_TEMPLATE = """
                Use the pieces of information provided in the context to answer user's question.
                If you dont know the answer, just say that you dont know, dont try to make up an answer. 
                Dont provide anything out of the given context

                Context: {context}
                Question: {question}

                Start the answer directly. No small talk please.
                """
        vectorStore = get_vectorstore()
        if vectorStore is None:
                st.error("Failed to load the vector store")
        
        qa_chain=RetrievalQA.from_chain_type(
            llm=load_llm(HUGGINGFACE_REPO_ID),
            chain_type="stuff",
            retriever=vectorStore.as_retriever(search_kwargs={'k':3}),
            return_source_documents=True,
            chain_type_kwargs={'prompt':set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
        )
        response=qa_chain.invoke({'query':prompt})
        result = response["result"]
        result_to_show=result
        st.chat_message("assistant").markdown(result_to_show)
        st.session_state.messages.append({"role":'Assistant', 'content': result_to_show})

if __name__ == "__main__":
    main()

