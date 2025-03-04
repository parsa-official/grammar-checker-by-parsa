import cohere
import streamlit as st
import json
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Grammar Checker by Parsa",
        page_icon="📕",
    )

    def load_config(file_path="config.json"):
        with open(file_path, "r") as f:
            config = json.load(f)
        return config

    config = load_config()
    api_key = config.get("api_key")

    co = cohere.Client(api_key)

    question = 'Check Grammar (English) of Text and if false, Say **Incorrect** and give a Correction and say why it is incorrect. But if true, Say **Correct** and give another example like that \n Text:'

    with st.form(key="grammar_form"):
        txt = st.text_input(label='Enter a text:')
        submit_button = st.form_submit_button("Check Grammar")

    if submit_button and txt.strip():
        response = co.generate(
            model='command',
            prompt=f'{question} {txt}',
            max_tokens=100,
        )

        if 'Incorrect' in response.generations[0].text:
            st.write(f"<p style='color: red;'>{response.generations[0].text}</p>", unsafe_allow_html=True)
        else:
            st.write(f"<p style='color: green;'>{response.generations[0].text}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    run()
