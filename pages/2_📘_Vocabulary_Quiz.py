import streamlit as st
import json
import random
import openai

def run():
    st.set_page_config(
        page_title="Vocabulary Quiz by Parsa",
        page_icon="📘",
    )

    st.title("📘 Vocabulary Quiz by Parsa")
    st.markdown("Create smart vocabulary quizzes using your word list and AI! 🧠")

    # Load config
    def load_config(file_path="config.json"):
        with open(file_path, "r") as f:
            return json.load(f)

    config = load_config()
    api_key = config.get("api_key")

    # ✅ OpenRouter-compatible setup
    openai.api_key = api_key
    openai.base_url = "https://openrouter.ai/api/v1"

    # 🔽 Model selection
    model_options = {
        "⚡ Mistral 24B Instruct": "mistralai/mistral-small-3.1-24b-instruct:free",
        "🔍 Google Gemma 3 12B": "google/gemma-3-27b-it:free",
        "💬 OpenChat 7B": "openchat/openchat-7b:free",
        "🧠 Qwen2.5 VL 72B": "qwen/qwen2.5-vl-72b-instruct:free",
        # "🚀 Reka Flash 3": "rekaai/reka-flash-3:free"
    }

    col1, col2 = st.columns(2)
    with col1:
        selected_model_name = st.selectbox("🤖 Choose AI Model", list(model_options.keys()))
        selected_model = model_options[selected_model_name]

    with col2:
        quiz_level = st.radio("🎯 Quiz Level", ['Basic', 'Normal', 'Hard', 'Master'])

    # Quiz Settings
    question_type = {
        'type of questions': '',
        'Total number of questions': '',
        'level': '',
        'Answers (be end of question)': '',
        "Answers Options": "In MCQ questions, the answer choices must vary (avoid repeating A/B/C/D).",
        'questions orders': 'Randomize vocab question order.',
    }

    # Question types
    q_type = st.multiselect("❓ Question Types", 
                            ['MCQ', 'Fill in the Blank', 'True/False', 'Short Answer', 'Matching'], 
                            default=['MCQ'])
    question_type['type of questions'] = '+ '.join(q_type)

    # Number of questions
    q_num = st.number_input("🔢 Number of Questions", min_value=1, max_value=10, value=5)
    question_type['Total number of questions'] = str(q_num)

    # Quiz difficulty
    levels = {
        'Basic': 'Basic quiz (easy questions)',
        'Normal': 'Normal quiz (high school level)',
        'Hard': 'Hard quiz (college level)',
        'Master': 'Master quiz (very difficult – for experts)'
    }
    question_type['level'] = levels.get(quiz_level, 'Normal')

    # Answer Sheet
    show_answers = st.toggle("🧾 Show Answer Sheet at the End")
    question_type['Answers (be end of page)'] = 'Yes' if show_answers else 'No'

    # Word input
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
At the end, if answer sheet is requested, include the answers in a clearly labeled section.
Words:\n{', '.join(vocab_list)}
"""

            try:
                response = openai.ChatCompletion.create(
                    model=selected_model,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = response['choices'][0]['message']['content']

                # If answer sheet is included, split and show it at the bottom
                if show_answers and "**Answers:**" in response_text:
                    quiz_part, answer_part = response_text.split("**Answers:**", 1)
                    st.markdown(f"**🧠 Quiz Level:** {question_type['level']}")
                    st.markdown(quiz_part.strip())
                    st.markdown("---")
                    st.markdown("### 🧾 Answer Sheet")
                    st.markdown(answer_part.strip())
                else:
                    st.markdown(f"**🧠 Quiz Level:** {question_type['level']}")
                    st.write(response_text)

            except Exception as e:
                st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    run()
