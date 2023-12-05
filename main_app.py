import streamlit as st
import base64
import streamlit.config

# Import from your script
from process_materials import QuestionBank, process_lecture_materials

# Initialize the question bank
api_key = "insert_api_key"
lecture_materials = process_lecture_materials()
question_bank = QuestionBank(api_key, lecture_materials)


def main():

    # Function to set custom background
    def set_bg_img(image_file):
        with open(image_file, "rb") as file:
            base64_img = base64.b64encode(file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{base64_img}");
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # Call the function to set the background
    set_bg_img('gradient.png')

    st.title("LIGN 101 Dynamic Question Bank")

    # Select a topic
    topic = st.selectbox("Choose a topic:", list(lecture_materials.keys()))

    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
        st.session_state.summary = None
        st.session_state.correct_answer = None
        st.session_state.question_counter = 0  # Initialize the counter

    if st.button("Generate Question"):
        # Generate a question for the selected topic
        st.session_state.current_question, st.session_state.summary = question_bank.generate_question(topic)
        st.session_state.correct_answer = None
        st.session_state.question_counter += 1  # Increment the counter

    if st.session_state.current_question:
        st.text_area("Question", value=st.session_state.current_question, height=100, disabled=True)

    # Answer input with counter as the key
    user_answer = st.text_input("Your answer:", key=f"answer_input_{st.session_state.question_counter}")

    if user_answer and not st.session_state.correct_answer:
        # Generate answer only once
        st.session_state.correct_answer = question_bank.generate_answer(st.session_state.current_question, st.session_state.summary)

    if user_answer and st.session_state.correct_answer:
        # Compare user answer with the correct answer
        if user_answer.lower().strip() == st.session_state.correct_answer[0].lower().strip():
            st.success("Correct!")
        else:
            st.error(f"Incorrect. The correct answer is: {st.session_state.correct_answer}")


    # if 'current_question' not in st.session_state:
    #     st.session_state.current_question = None
    #     st.session_state.summary = None
    #     st.session_state.correct_answer = None

    # if st.button("Generate Question"):
    #     # Generate a question for the selected topic
    #     st.session_state.current_question, st.session_state.summary = question_bank.generate_question(topic)
    #     st.session_state.correct_answer = None  # Reset correct answer

    # if st.session_state.current_question:
    #     st.text_area("Question", value=st.session_state.current_question, height=100, disabled=True)

    # # Answer input
    # user_answer = st.text_input("Your answer:")

    # if user_answer and not st.session_state.correct_answer:
    #     # Generate answer only once
    #     st.session_state.correct_answer = question_bank.generate_answer(st.session_state.current_question, st.session_state.summary)

    # if user_answer and st.session_state.correct_answer:
    #     # Compare user answer with the correct answer
    #     if user_answer.lower().strip() == st.session_state.correct_answer.lower().strip():
    #         st.success("Correct!")
    #     else:
    #         st.error(f"Incorrect. The correct answer is: {st.session_state.correct_answer}")

if __name__ == "__main__":
    main()
