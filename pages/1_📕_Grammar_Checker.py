import streamlit as st
import json
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="Grammar Checker by Parsa",
    page_icon="📕",
)

st.title("📕 Grammar Checker by Parsa")
st.markdown("Check grammar in English or German — with explanations in your chosen language.")

# 🔐 Load API key
def get_api_key():
    try:
        with open("config.json", "r") as f:
            return json.load(f).get("api_key")
    except:
        return None

stored_key = get_api_key()

if not stored_key:
    st.warning("🔐 Please enter your OpenRouter API key to use this app.")
    user_key = st.text_input("Enter your API key (starts with `sk-`)", type="password")
    st.markdown("➡️ [Get your free API key here](https://openrouter.ai/keys)")
    if not user_key:
        st.stop()
    api_key = user_key
else:
    api_key = stored_key

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# ✅ Model choices
model_options = {
    "🎲 Auto Free Router (recommended)": "openrouter/free",
    "🦙 Llama 3.2 3B Instruct": "meta-llama/llama-3.2-3b-instruct:free",
    "🔤 Qwen 2.5 7B Instruct": "qwen/qwen-2.5-7b-instruct:free",
    "🧠 Qwen 2.5 72B Instruct": "qwen/qwen-2.5-72b-instruct:free",
    "💎 Gemma 3 27B Instruct": "google/gemma-3-27b-it:free",
}

# UI - Model & Language
col1, col2 = st.columns(2)

with col1:
    selected_model_name = st.selectbox("🤖 Choose AI Model", list(model_options.keys()))
    selected_model = model_options[selected_model_name]

with col2:
    chat_language = st.selectbox("🗣️ Response Language", ["English","Persian","German"])

# User input
with st.form("grammar_form"):
    txt = st.text_input("✍️ Enter a sentence (English or German):")
    submit_button = st.form_submit_button("Check Grammar")

# Generate the prompt based on chat language
if chat_language == "Persian":
    instruction = """
    بررسی کن که جملهٔ زیر از نظر گرامری درست است یا نه (ممکن است جمله به انگلیسی یا آلمانی باشد).
    اگر اشتباه دارد، بنویس **نادرست**، نسخهٔ اصلاح‌شده را بده و دلیل اشتباه را به زبان فارسی توضیح بده.
    اگر درست است، بنویس **درست** و یک مثال مشابه دیگر به همان زبان ارائه بده.
    متن:"""

elif chat_language == "German":
    instruction = """
    Überprüfen Sie die Grammatik des folgenden Satzes (auf Englisch oder Deutsch).
    Wenn er falsch ist, sagen Sie **Falsch**, geben Sie eine Korrektur an und erklären Sie den Fehler auf Deutsch.
    Wenn er korrekt ist, sagen Sie **Richtig** und geben Sie ein ähnliches Beispiel.
    Text:"""

else:  # English
    instruction = """
    Check the grammar of the following sentence (can be in English or German).
    If incorrect, say **Incorrect**, provide the correction, and explain the error in English.
    If correct, say **Correct** and provide a similar example in the same language.
    Text:"""

# Handle grammar check
if submit_button and txt.strip():
    prompt = f"{instruction} {txt}"

    try:
        completion = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = completion.choices[0].message.content

        # Color-coded output
        if any(word in response_text.lower() for word in ["incorrect", "falsch", "نادرست"]):
            st.write(f"<p style='color: red;'>{response_text}</p>", unsafe_allow_html=True)
        elif any(word in response_text.lower() for word in ["correct", "richtig", "درست"]):
            st.write(f"<p style='color: green;'>{response_text}</p>", unsafe_allow_html=True)
        else:
            st.write(response_text)

    except Exception as e:
        st.error(f"❌ Error: {e}")