import streamlit as st
import json
import random
from openai import OpenAI

def run():
    st.set_page_config(
        page_title="Vocabulary Quiz by Parsa",
        page_icon="📘",
    )

    st.title("📘 Vocabulary Quiz by Parsa")
    st.markdown("Create smart AI-powered vocabulary quizzes from your own word list!")

    # 🔐 Load API key from input or local config.json
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

    # ✅ OpenRouter API client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    model_options = {
        "⚡ Mistral 24B Instruct": "mistralai/mistral-small-3.1-24b-instruct:free",
        "🔍 Google Gemma 3 12B": "google/gemma-3-27b-it:free",
        "💬 OpenChat 7B": "openchat/openchat-7b:free",
        "🧠 Qwen2.5 VL 72B": "qwen/qwen2.5-vl-72b-instruct:free",
        # "🚀 Reka Flash 3": "rekaai/reka-flash-3:free"
    }

    # UI Layout
    col1, col2 = st.columns(2)

    with col1:
        selected_model_name = st.selectbox("🤖 Choose AI Model", list(model_options.keys()))
        selected_model = model_options[selected_model_name]

    with col2:
        quiz_level = st.radio("🎯 Quiz Level", ['Basic', 'Normal', 'Hard', 'Master'])

    # Quiz settings
    question_type = {
        'type of questions': '',
        'Total number of questions': '',
        'level': '',
        'Answers (be end of question)': '',
        "Answers Options": "In MCQ questions, the answer choices must vary (avoid repeating A/B/C/D).",
        'questions orders': 'Randomize vocab question order.',
    }

    q_type = st.multiselect("❓ Question Types", 
                            ['MCQ', 'Fill in the Blank', 'True/False', 'Short Answer', 'Matching'], 
                            default=['MCQ'])
    question_type['type of questions'] = '+ '.join(q_type)

    q_num = st.number_input("🔢 Number of Questions", min_value=1, max_value=10, value=5)
    question_type['Total number of questions'] = str(q_num)

    # Level descriptions
    levels = {
        'Basic': 'Basic quiz (easy questions)',
        'Normal': 'Normal quiz (high school level)',
        'Hard': 'Hard quiz (college level)',
        'Master': 'Master quiz (very difficult – for experts)'
    }
    question_type['level'] = levels.get(quiz_level, 'Normal')

    show_answers = st.toggle("🧾 Show Answer Sheet at the End")
    question_type['Answers (be end of page)'] = 'Yes' if show_answers else 'No'

    # User inputs vocab
    words = st.text_area("✍️ Enter Your Words (separated by - or ,)")
    st.caption("Example: apple - orange - banana")

    if st.button("🚀 Generate Quiz"):
        if not words.strip():
            st.warning("Please enter some words.")
        else:
            vocab_list = [w.strip() for w in words.replace(',', '-').split('-') if w.strip()]
            random.shuffle(vocab_list)

            prompt = f"""
Create a vocabulary quiz using the following words. The quiz should follow this structure:
{json.dumps(question_type, ensure_ascii=False, indent=2)}

Use a random selection of words from the list. Bold the vocabulary word in each question.
At the end, if answer sheet is requested, include the correct answers.
Words:\n{', '.join(vocab_list)}
"""

            try:
                completion = client.chat.completions.create(
                    model=selected_model,
                    messages=[{"role": "user", "content": prompt}]
                )
                response = completion.choices[0].message.content
                st.markdown(f"**🧠 Quiz Level:** {question_type['level']}")

                # Show answer sheet at the bottom
                if show_answers and "**Answers:**" in response:
                    quiz_part, answer_part = response.split("**Answers:**", 1)
                    st.markdown(quiz_part.strip())
                    st.markdown("---")
                    st.markdown("### 🧾 Answer Sheet")
                    st.markdown(answer_part.strip())
                else:
                    st.write(response)

            except Exception as e:
                st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    run()
