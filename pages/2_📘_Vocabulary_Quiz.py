import google.generativeai as genai
from PIL import Image
import streamlit as st
import json
import random


def run():
    st.set_page_config(
        page_title="Vocabulary Quiz by Parsa",
        page_icon="📘",
    )


    ########## API request ##########

    def load_config(file_path="config.json"):
        with open(file_path, "r") as f:
            config = json.load(f)
        return config

    config = load_config()
    api_key = config.get("api_key")
    genai.configure(api_key=api_key)


    ########## Choose (Text or Image) ##########

    def display_text(option):
        if option == 'gemini-pro':
            return "Text (Write or Paste words)"
        elif option == 'gemini-pro-vision':
            return 'Image (Upload a photo with words written inside)'
        else:
            return option  # Handle other cases if needed

    models = st.selectbox('Choose your type input', ['gemini-pro', 'gemini-pro-vision'], format_func=display_text)
    model = genai.GenerativeModel(models)

    # words_list = []
    # random_words = random.sample(words_list, 5)

    question_type = {
        'type of questions': '',
        'Total number of questions': '',
        'level': 'basic',
        'Answers (be end of question)': '',
        "Answers Options" : 'In MCQ questions, The answers (choices) of the questions must be different .(for example, the answers to all questions should not be option "A" or "B" or "C" or "D")',
        'questions orders' : 'The order of the vocabs questions should be random choose (mean The first question should not be from the first word. be random)',
    }

    ########## Question type ##########

    q_type = st.multiselect(label='Questions type:', options=['MCQ', 'Fill in the Blank','True/False','Short Answer','Matching'], default='MCQ')
    question_type['type of questions'] = '+ '.join(q_type)

    ########## Number of questions ##########
    q_num = st.number_input(label='Number of questions:', min_value=1, max_value=10, value=5)

    if q_num > 0:
        question_type['Total number of questions'] = str(q_num)

    ########## Quiz Level ##########

    quiz_level = st.radio(label='Quiz Level',options=['Basic','Normal','Hard','Master'])

    if quiz_level=='Basic':
        question_type['level'] = 'Basic quiz (with Easy Question)'

    elif quiz_level=='Normal':
        question_type['level'] = 'Normal quiz (Not so Easy, Not so hard (HighSchool Level))'    

    elif quiz_level=='Hard':
        question_type['level'] = 'Hard quiz (with hard and challengeable questions (College Level))'
        
    elif quiz_level=='Master':
        question_type['level'] = 'Master quiz (with master and so hard question - like for teachers and masters)'


    ########## Answers Sheet ##########

    answers_sheet = st.toggle("Answers Sheet")

    if answers_sheet:
        question_type['Answers (be end of page)'] = 'Yes, The answer sheet can be seen at the end of page.'
    else:
        question_type['Answers (be end of page)'] = 'Do not need'

    ########## Response Level ##########

    if models == 'gemini-pro':
        words = st.text_area(label='Write your words')
        notic = st.write("Note: Use '-' or ',' for seprate words")
        if st.button('Start Quiz'):
            # Shuffle the list of words before generating the quiz
            vocab_list = [word.strip() for word in words.split('-')]  # Convert to list
            random.shuffle(vocab_list)
            response = model.generate_content([
                f'take Vocabulary Quiz about these vocabs- take random of those (for learning and remembering better)\n\n{json.dumps(question_type)} (Vocabs of quiz be bold text)',
                ' - '.join(vocab_list)  # Join the shuffled list back to string
            ])
            st.write('Level:', question_type['level'])
            st.write(response.text)


    elif models == 'gemini-pro-vision':
        imageupload = st.file_uploader('Upload your photo', type=['jpg', 'jpeg', 'png'])
        notic = st.write("Note: Use high-quality and legible photos. \n Try to make the words legible in the photo. \n formats support: 'jpg', 'jpeg', 'png' ")
        if imageupload:
            if st.button('Start Quiz'):
                img = Image.open(imageupload)
                response = model.generate_content([
                    f'take Vocabulary Quiz about these vocabs- take random of those (for learning and remembering better)\n\n{json.dumps(question_type)}',
                    img
                ])
                st.write(response.text)



if __name__ == "__main__":
    run()