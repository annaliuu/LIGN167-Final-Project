import os
import openai
import random

# Part 1: Data Processing


def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


def process_lecture_materials(directory='lectures'):
    topics = {
        "Introducing Language and Dialect": "l101_2_whatislanguage.md",
        # ... other topics and their corresponding filenames
    }

    processed_materials = {}
    for topic, filename in topics.items():
        file_path = os.path.join(directory, filename)
        lecture_content = read_markdown_file(file_path)
        if lecture_content is not None:
            processed_materials[topic] = lecture_content

    return processed_materials

# Part 2: Question Generation


class QuestionBank:
    def __init__(self, api_key, lecture_materials):
        self.api_key = api_key
        self.lecture_materials = lecture_materials
        self.user_performance = {}

    def update_performance(self, topic, correct):
        if topic not in self.user_performance:
            self.user_performance[topic] = {'correct': 0, 'incorrect': 0}

        if correct:
            self.user_performance[topic]['correct'] += 1
        else:
            self.user_performance[topic]['incorrect'] += 1

    def generate_question(self, topic):
        performance = self.user_performance.get(
            topic, {'correct': 0, 'incorrect': 0})
        difficulty = "hard" if performance['correct'] > performance['incorrect'] else "easy"
        prompt = f"Generate a {difficulty} multiple choice question about {topic}"

        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=150,
                api_key=self.api_key
            )
            question = response.choices[0].text.strip()
            return question
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Error generating question"


# Example usage
# Replace with your actual API key
api_key = "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"
lecture_materials = process_lecture_materials()
question_bank = QuestionBank(api_key, lecture_materials)

# Simulate user answering questions
question_bank.update_performance("Syntax is a Life Sentence", correct=False)
question_bank.update_performance("Syntax is a Life Sentence", correct=True)

# Generate a question based on performance
next_question = question_bank.generate_question("Syntax is a Life Sentence")
print(next_question)
