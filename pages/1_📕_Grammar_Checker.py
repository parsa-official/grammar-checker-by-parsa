import streamlit as st
import json
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="Grammar Checker by Parsa (ENG/GER)",
    page_icon="📕",
)

# Load API key from config.json
def load_config(file_path="config.json"):
    with open(file_path, "r") as f:
        config = json.load(f)
    return config

config = load_config()
api_key = config.get("api_key")

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# ✅ Available Models
model_options = {
    "⚡ Mistral 24B Instruct": "mistralai/mistral-small-3.1-24b-instruct:free",
    "🔍 Google Gemma 3 12B": "google/gemma-3-27b-it:free",
    "💬 OpenChat 7B": "openchat/openchat-7b:free",
    "🧠 Qwen2.5 VL 72B": "qwen/qwen2.5-vl-72b-instruct:free",
    # "🚀 Reka Flash 3": "rekaai/reka-flash-3:free"
}

# UI Layout
st.markdown("Grammar check for English or German input. Response in your chosen language!")

col1, col2 = st.columns(2)

with col1:
    selected_model_name = st.selectbox("🤖 Choose AI Model", list(model_options.keys()))
    selected_model = model_options[selected_model_name]

with col2:
    chat_language = st.selectbox("🗣️ Choose Response Language", ["English","Persian", "German"])

# Input form
with st.form(key="grammar_form"):
    txt = st.text_input("✍️ Enter a sentence (English or German):")
    submit_button = st.form_submit_button("Check Grammar")

# Instruction prompt based on chat language
if chat_language == "Persian":
    instruction = """
    بررسی کن که جملهٔ زیر از نظر گرامری درست است یا نه (ممکن است جمله به انگلیسی یا آلمانی باشد).
    اگر اشتباه دارد، بنویس **نادرست**، نسخهٔ اصلاح‌شده را بده و دلیل اشتباه را به زبان فارسی توضیح بده.
    اگر درست است، بنویس **درست** و یک مثال مشابه دیگر به همان زبان ارائه بده.
    متن:"""

elif chat_language == "German":
    instruction = """
    Überprüfen Sie die Grammatik des folgenden Satzes (der Satz kann auf Englisch oder Deutsch sein).
    Wenn er falsch ist, sagen Sie **Falsch**, geben Sie eine Korrektur an und erklären Sie den Fehler auf Deutsch.
    Wenn er korrekt ist, sagen Sie **Richtig** und geben Sie ein ähnliches Beispiel.
    Text:"""

else:  # English
    instruction = """
    Check the grammar of the following sentence (can be in English or German).
    If incorrect, say **Incorrect**, provide the correction, and explain the error in English.
    If correct, say **Correct** and provide a similar example in the same language.
    Text:"""

# On form submission
if submit_button and txt.strip():
    full_prompt = f"{instruction} {txt}"

    try:
        completion = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": full_prompt}]
        )

        response_text = completion.choices[0].message.content

        # Highlight result
        if any(word in response_text.lower() for word in ["incorrect", "falsch", "نادرست"]):
            st.write(f"<p style='color: red;'>{response_text}</p>", unsafe_allow_html=True)
        elif any(word in response_text.lower() for word in ["correct", "richtig", "درست"]):
            st.write(f"<p style='color: green;'>{response_text}</p>", unsafe_allow_html=True)
        else:
            st.write(response_text)

    except Exception as e:
        st.error(f"❌ Error: {e}")


# model_options = {
#     "⚡ Mistral 24B Instruct": "mistralai/mistral-small-3.1-24b-instruct:free",
#     "🔍 Google Gemma 3 12B": "google/gemma-3-27b-it:free",
#     "💬 OpenChat 7B": "openchat/openchat-7b:free",
#     "🧠 Qwen2.5 VL 72B": "qwen/qwen2.5-vl-72b-instruct:free",
#     # "🚀 Reka Flash 3": "rekaai/reka-flash-3:free"
# }
