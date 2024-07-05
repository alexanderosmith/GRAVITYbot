import csv
from datetime import datetime
import re
from openai import OpenAI

client = OpenAI(api_key='OPENAI_API_KEY')


file_path = 'C:/Users/gabri/Downloads/Downloads/Research Team/gravity-spy-comments-processed06-May-2021 11.05.csv'

def load_and_identify_questions(file_path):
    questions = []
    with open(file_path, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row['comment_body_control']  # Replace 'YourColumnNameHere' with the actual column name containing the questions
            timestamp = row['comment_created_at']  # Replace with the actual column name for timestamp
            if re.search(r'\?\s*$', text):  # Regex to find questions
                questions.append({'timestamp': timestamp, 'text': text})
    return questions


def segment_questions_by_time(questions, start_date, end_date):
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    segmented_questions = [q for q in questions if start_dt <= datetime.strptime(q['timestamp'], '%Y-%m-%d %H:%M:%S') <= end_dt]
    return segmented_questions

def interpret_and_respond(questions):
    responses = []
    for question in questions:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question['text']}
        ])
        responses.append({'question': question['text'], 'response': response.choices[0].message.content})
    return responses


def main():
    questions = load_and_identify_questions(file_path)
    # Example: Analyze questions between '2021-01-01' and '2021-12-31'
    segmented_questions = segment_questions_by_time(questions, '2021-01-01', '2021-12-31')
    responses = interpret_and_respond(segmented_questions)
    for response in responses:
        print(f"Q: {response.question}\nA: {response.response}\n")

if __name__ == '__main__':
    main()
