import os
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set the OpenAI API key

# Verify the API key is correctly fetched
if not openai.api_key:
    raise ValueError("The OpenAI API key is not set. Please check your environment variables.")

# Load your CSV data
csv_file_path = r'C:\Users\gabri\Downloads\Downloads\Research Team\gravity-spy-comments-processed06-May-2021 11.05.csv'
df = pd.read_csv(csv_file_path)
print("First few rows of the DataFrame:")
print(df.head())

# Generate a prompt and fetch a response from ChatGPT
prompt = f"Here's a summary of the data: {df.head().to_string(index=False)}\n\nProvide a brief analysis of this data."

response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
])

print("\nChatGPT's Response:")
print(response.choices[0].message.content)
