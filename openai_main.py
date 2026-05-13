from openai import OpenAI
import streamlit as st
import os

# Create prompt template for generating tweets

tweet_template = "Give me {number} tweets on {topic}"

st.header(":bird: AI Tweet Generator")

st.subheader(":heart: Made with Build Fast with AI")

topic = st.text_input("Topic")

number = st.number_input("Number of tweets", min_value = 1, max_value = 10, value = 1, step = 1)

if st.button("Generate"):
    client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
    prompt = tweet_template.format(number=number, topic=topic)
    
    response = client.chat.completions.create(
        model="gpt-5.4-mini", # gpt-5.4-nano
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    st.write(response.choices[0].message.content)