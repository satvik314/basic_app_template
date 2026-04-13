# ============================================================
# Tweet Generator - Main Application
# A Streamlit app that generates tweets using Google's Gemini
# AI model, orchestrated through LangChain.
# ============================================================

# --- Imports ---
# LangChain components for LLM interaction and prompt management
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Streamlit for the web UI, os for environment variable management
import streamlit as st
import os

# --- API Key Configuration ---
# Load the Google API key from environment variables.
api_key = os.getenv('GOOGLE_API_KEY', '')

if not api_key:
    st.error("GOOGLE_API_KEY is missing. Set it in your environment variables.")
    st.stop()

os.environ['GOOGLE_API_KEY'] = api_key

# --- Prompt Template ---
# Define the prompt template with placeholders for the number of tweets
# and the topic. LangChain's PromptTemplate handles variable substitution.
tweet_template = "Give me {number} tweets on {topic}"

tweet_prompt = PromptTemplate(template = tweet_template, input_variables = ['number', 'topic'])

# --- Streamlit UI ---
# Page header and description
st.header("🐦 Tweet Generator")

st.subheader("Generate tweets using Generative AI 🤖")

# Text input for the user to specify a tweet topic
topic = st.text_input("Topic")

# Numeric input to select how many tweets to generate (between 1 and 10)
number = st.number_input("Number of tweets", min_value = 1, max_value = 10, value = 1, step = 1)

# Generate button - invokes the LangChain pipeline and displays the results
if st.button("Generate"):
    clean_topic = topic.strip()
    if not clean_topic:
        st.warning("Please enter a topic before generating tweets.")
        st.stop()

    with st.spinner("Generating tweets..."):
        gemini_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")
        tweet_chain = tweet_prompt | gemini_model
        tweets = tweet_chain.invoke({"number": number, "topic": clean_topic})

    generated_text = getattr(tweets, "content", None)
    if not generated_text:
        generated_text = str(tweets)
    st.write(generated_text)
    