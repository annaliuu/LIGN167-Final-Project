import streamlit as st
import base64
import streamlit.config

# Import from your script
from process_materials import QuestionBank, process_lecture_materials

# Initialize the question bank
# Replace with your actual API key
api_key = "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"
lecture_materials = process_lecture_materials()
question_bank = QuestionBank(api_key, lecture_materials)


def main():

    # Function to set the background
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

    if st.button("Generate Question"):
        # Generate a question for the selected topic
        question, summary = question_bank.generate_question(topic)
        st.text_area("Question", value=question, height=100, disabled=True)

    # Answer input
    user_answer = st.text_input("Your answer:")
    question, summary = question_bank.generate_question(topic)

    if user_answer:
        # Assuming generate_answer returns the correct answer for the question
        correct_answer = question_bank.generate_answer(question, summary)

        # Compare user answer with the correct answer
        if user_answer.lower().strip() == correct_answer.lower().strip():
            #question_bank.update_performance(topic, correct=True)
            st.success("Correct!")
        else:
            #question_bank.update_performance(topic, correct=False)
            st.error(f"Incorrect. The correct answer is: {correct_answer}")

    # Check the answer (Placeholder for actual logic)
    # if user_answer:
    #     correct_answer = question_bank.generate_answer(
    #         question, summary)  # Placeholder

    #     st.text_area("test", value=correct_answer)

    #     if user_answer.lower() == correct_answer.lower():
    #         question_bank.update_performance(topic, correct=True)
    #         st.success("Correct!")
    #         st.text_area("Answer", value=correct_answer,
    #                      height=100, disabled=True)
    #     else:
    #         question_bank.update_performance(topic, correct=False)
    #         st.error(f"Incorrect. The correct answer is: {correct_answer}")
    #         st.text_area("Answer", value=correct_answer,
    #                      height=100, disabled=True)


if __name__ == "__main__":
    main()
