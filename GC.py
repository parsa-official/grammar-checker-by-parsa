import google.generativeai as genai
from PIL import Image
import streamlit as st
import json

# API = "AIzaSyC6trLcXtcQWDhGca-l7QVDZPWh19fIYDs"
# genai.configure(api_key=API)


def load_config(file_path="config.json"):
    with open(file_path, "r") as f:
        config = json.load(f)
    return config

config = load_config()
api_key = config.get("api_key")

genai.configure(api_key=api_key)



model = genai.GenerativeModel('gemini-pro')

# img = Image.open('photo_2023-12-30_15-14-26.jpg')
txt = st.text_input(label='Enter a text:')
question = 'Check Grammar (English) of Text and if false, Say **Incorrect** and give a Correction and say why it is incorrect. But if true, Say **Correct** and give another example like that \n Text:'
button_clicked = st.button("Check Grammer")
response = model.generate_content([question, txt])


# for word in response:
if 'Incorrect' in response.text:
    st.write(f"<p style='color: red;'>{response.text}</p>", unsafe_allow_html=True)
else:
    st.write(f"<p style='color: green;'>{response.text}</p>", unsafe_allow_html=True)