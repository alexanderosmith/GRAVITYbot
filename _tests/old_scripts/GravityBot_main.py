#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Creator: Alexander O. Smith (2024-present), aosmith@syr.edu
# Current Maintainer: Alexander O. Smith, aosmith@syr.edu
# Last Update: April 7, 2024
# Program Goal:
# This file is the main executable Python file of "GravityBot"
#####################################################################################################
#####################################################################################################
#####################################################################################################
# Backlog Tasks:
# 1. Figure out how to properly build the .env file for security purposes.
# 2. Use RegEx to clean up text data before sending it to ChatGPT (???)
# 3. Figure out how to specify data location as relative file path.
# 4. Make date segmentation function prompt user for dates.
# 5. Automate the format of the "content" such that it needs minimal editing before reporting it.
# Optional Considerations
# 1. Look into automating the talk page download through Zooniverse API
# 2. Maybe use LangChain to simplify talk search
# 3/4 Perhaps figure out a way to summarize Alogs and follow and links as a knowledge base.


# Questions:
# 1. Once I have .env secured, and the directories cleared up, should I push this to GitHub?
# 2. If so, is using an MIT License okay?
# 3. We should probably focus on specifying the prompts and which comments
#      Take a look at gravityBot_output.txt
# 4. How about expenses? (After having run a week's worth of data about 10-15 times, it cost $.09)
# 5. How do we want the output summary structured? How long do we want it to be?
#       This will likely be different for each user story.

# !!! Eventually set a fixed directory for the project to run from

# DEPENDENCIES ######################################################################################
import os, re, csv, openai
os.chdir('/home/aosmith/Documents/Scripts/Projects/GravitySpy/GenAI_Proj/GRAVITYbot')
import pandas as pd
from datetime import datetime
from openai import OpenAI
from panoptes_client import Panoptes
from dotenv import find_dotenv, load_dotenv
import prompts
# Example of how to import a prompt from prompts py file.
#####################################################################################################
# Load the Talk CSV file
# !!! Eventually set this up so it runs dynamically within the same project
talk_file = './_data/ex_GS_TalkComments_2024-01-29.csv'

#####################################################################################################
# Functions #########################################################################################
# 1. load_text          :   loads talk data
# 2. segment_by_time    :   limits talk data to those within particular dates
# 3. chat_with_gpt      :   calls chatGPT bot
# 4. main               :   runs above functions in order, and loads prompt file info
#####################################################################################################
# Function: gets data from Zooniverse using Panoptes client
# def zooniverse_dat_git():
#   
# Function: loads data and gets comments which contain text
def load_text(file_path):
    text_dat = []
    with open(file_path, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row['comment_body']  
            # Comment Data
            timestamp = row['comment_created_at']  
            # Captures only those comments containing text.
            if re.search(r'.', text):  # Regex to find questions
                text_dat.append({'timestamp': timestamp, 'text': text})
    return text_dat

# Function: transforms dates to segment questions
def segment_by_time(text_dat, start_date, end_date):
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    segmented_txt = [t for t in text_dat if start_dt <= datetime.strptime(
        t['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ') <= end_dt]
    
    # Make segmented text a single string.
    talk_dat = ""
    for t in segmented_txt:
        #print(t['text'])
        talk_dat += " "+t['text']
    return talk_dat

# Function: sends prompts to chatGPT
#### NOTICE: Be careful with this function! It costs the money.
_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def chat_with_gpt(user_prompt, sys_prompt):
    
    response = client.chat.completions.create(
        
        # Messages: priming the model for a response
        messages = [
            # System role tells the model a "role" to respond
            {'role' : 'system', 'content' : sys_prompt},
            # User role is what "we" the user are asking/telling the model
            {"role": "user", "content": user_prompt}
            ],
        # Model: The openAI model for the project
        model="gpt-3.5-turbo-0125",

        # Temperature: How accurate do we want it to be?
        temperature=0.6,
        # Maximum token output.
        #### NOTICE: Making this number bigger makes things more expensive.
        max_tokens=500
    )

    # Outfile of Call and Response to GravitySpy
    current_time = f"{datetime.now()}"
    with open("_output/gravityBot_output.txt", "a") as out_file:
        out_file.write(f"GRAVITYBOT PROMPT TIME: {current_time}\n\n")
        out_file.write(f"SYSTEM PROMPT:\n{sys_prompt}\nUser Prompt: {user_prompt}\n")
        out_file.write(f"GRAVITYBOT RESPONSE:\n{str(response)}\n\n")

    return response.choices[0].message.content


# Main Function: Calls all previous functions for a user specified time frame
def main():
    # Call load_text
    txt = load_text(talk_file)

    # Call segment_by_time for correct time span
    talk_dat = segment_by_time(txt, '2023-01-06', '2023-01-07')

    # Validate openAPI key stored in .env
    _ = load_dotenv(find_dotenv())
    client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
    )    

    # Call ex_func_prompt_gen from prompts.py 
    prompt_func = prompts.ex_func_prompt_gen(talk_dat)

    # Call chatGPT function
    gsBot = chat_with_gpt(prompt_func[0], prompt_func[1])

    return gsBot

gsBotResponse = main()