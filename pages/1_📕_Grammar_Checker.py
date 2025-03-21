import streamlit as st
import json
import openai

def run():
    st.set_page_config(
        page_title="Grammar Checker by Parsa",
        page_icon="📕",
    )

    st.title("📕 Grammar Checker by Parsa")
    st.markdown("Check grammar in English or German, with explanations in your preferred language!")

    # Load API key from config
    def load_config(file_path="config.json"):
        with open(file_path, "r") as f:
            return json.load(f)

    config = load_config()
    api_key = config.get("api_key")

    # ✅ OpenRouter-compatible setup
    openai.api_key = api_key
    openai.base_url = "https://openrouter.ai/api/v1"

    # AI Model Selection
    model_options = {
        "🧠 Qwen2.5 VL 72B": "qwen/qwen2.5-vl-72b-instruct:free",
        "🔍 Google Gemma 3 12B": "google/gemma-3-12b-it:free",
        "💬 OpenChat 7B": "openchat/openchat-7b:free",
        "🔥 OlympicCoder 32B": "open-r1/olympiccoder-32b:free",
        "⚡ Mistral 24B Instruct": "mistralai/mistral-small-3.1-24b-instruct:free",
        "🚀 Reka Flash 3": "rekaai/reka-flash-3:free"
    }

    col1, col2 = st.columns(2)

    with col1:
        selected_model_name = st.selectbox("🤖 Choose AI Model", list(model_options.keys()))
        selected_model = model_options[selected_model_name]

    with col2:
        chat_language = st.selectbox("🗣️ Response Language", ["Persian", "English", "German"])

    # Set grammar-checking prompt based on chat language
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

    # Input form
    with st.form(key="grammar_form"):
        txt = st.text_input("✍️ Enter your sentence (English or German):")
        submit_button = st.form_submit_button("Check Grammar")

    if submit_button and txt.strip():
        prompt = f"{instruction} {txt}"

        try:
            response = openai.ChatCompletion.create(
                model=selected_model,
                messages=[{"role": "user", "content": prompt}]
            )

            result = response['choices'][0]['message']['content']

            # Display based on language markers
            if any(word in result.lower() for word in ["incorrect", "falsch", "نادرست"]):
                st.write(f"<p style='color: red;'>{result}</p>", unsafe_allow_html=True)
            elif any(word in result.lower() for word in ["correct", "richtig", "درست"]):
                st.write(f"<p style='color: green;'>{result}</p>", unsafe_allow_html=True)
            else:
                st.write(result)

        except Exception as e:
            st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    run()
