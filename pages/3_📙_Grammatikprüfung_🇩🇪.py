import google.generativeai as genai
from PIL import Image
import streamlit as st
import json
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Grammer Checker by Parsa",
        page_icon="📕",
    )

    def load_config(file_path="config.json"):
        with open(file_path, "r") as f:
            config = json.load(f)
        return config

    config = load_config()
    api_key = config.get("api_key")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    txt = st.text_input(label='Enter a text:')
    question = 'Check Grammar (Germany) of Text and if false, Say **Incorrect** and give a Correction and say why it is incorrect. But if true, Say **Correct** and give another example like that \n Text:'
    button_clicked = st.button("Check Grammer")
    response = model.generate_content([question, txt])


    # for word in response:
    if 'Incorrect' in response.text:
        st.write(f"<p style='color: red;'>{response.text}</p>", unsafe_allow_html=True)
    else:
        st.write(f"<p style='color: green;'>{response.text}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    run()    