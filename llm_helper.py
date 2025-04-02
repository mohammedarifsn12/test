import streamlit as st
from langchain_groq import ChatGroq

# Load API key from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]

# Initialize Groq Chat Model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

# Test the API
if __name__ == "__main__":
    response = llm.invoke("Two most important ingredients in samosa are ")
    print(response.content)



