#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Creator: Alexander O. Smith (2024-present), aosmith@syr.edu
# Current Maintainer: Alexander O. Smith, aosmith@syr.edu
# Last Update: July 7, 2024
# Program Goal:
# This file is the main executable Python file of "GRAVITYbot"
#####################################################################################################
#####################################################################################################
# DEPENDENCIES ######################################################################################
# Package Dependencies
import os, sys, pytz, re, csv, openai
from datetime import datetime
import pandas as pd
# API Imports
from openai import OpenAI
from panoptes_client import Panoptes
# Local enviornment imports and path appends
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import find_dotenv, load_dotenv
#import _test_alog as alog # This file needs to be fixed before I use it.
import prompts
# Example of how to import a prompt from prompts py file.
#####################################################################################################
# Load the Talk CSV file
# !!! Eventually set this up so it runs dynamically within the same project
talk_file = './_data/project-1104-comments_2024-07-07.csv'
#####################################################################################################
# Functions #########################################################################################
# 1. load_text          :   loads talk data
# 2. segment_by_time    :   limits talk data to those within particular dates
# 3. chat_with_gpt3     :   calls chatGPT3 bot (less expensive, lower input rate limit)
# 4. chat_with_gpt4     :   calls chatGPT4 bot (more expensive, higher input rate limit)
# 5. main               :   initiates above functions, and loads prompt file info
#####################################################################################################
# Function: loads data and gets comments which contain text
def load_text(file_path):
    talk_url = 'https://www.zooniverse.org/projects/zooniverse/gravity-spy/talk/'

    with open(file_path, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # Define the Universal timezone
        utc = pytz.UTC

        # Set up lists for dataframe return
        txt         =   []
        times       =   []
        comment_urls=   []

        for row in reader:
            # Text cleaning (saves money and makes it easier to not rate limit)
            text = row['comment_body']  
            text = re.sub('[^A-Za-z0-9\>\s\'\"\?\.\!]', ' ', text)
            text = re.sub('\.+', ' ', text)
            text = re.sub('projects zooniverse gravity spy talk subjects', ' ', text)
            text = re.sub('zooniverse gravity spy talk comment page', ' ', text)
            text = re.sub('\s[b-z][\.\s]', ' ', text)
            text = re.sub('[\n]', ' ', text)
            text = re.sub('[0-9]+\s', ' ', text)
            text = re.sub('[a-z][0-9]+', ' ', text)
            text = re.sub('\s+', ' ', text)
            txt.append(text)
            # Building Comment URLs to "cite" when GRAVITYbot needs to reference a comment
            board = str(row['board_id'])+'/'
            disc_id = str(row['discussion_id'])+'/'
            comment_url = talk_url+board+disc_id
            comment_urls.append(comment_url)
            # Define time formats with and without microseconds
            fmt_dot_ms = '%Y-%m-%d %H:%M:%S.%f%z'
            fmt_wo_ms = '%Y-%m-%d %H:%M:%S%z'
            
            # Timestamp Data Clean
            timestamp = row['comment_created_at']

            for fmt in (fmt_dot_ms, fmt_wo_ms):
                try:
                # Parse the timestamp
                    time = datetime.strptime(timestamp, fmt).astimezone(utc)
                    times.append(time)
                    break
                except: 
                    if fmt == fmt_wo_ms:
                        print(f'Datetime Conversion Warning')
                        times.append('datetime_conversion_issue')
                        break
        # Generate DataFrame of data necessary for GRAVITYbot interpretation
        text_dat = pd.DataFrame({
            'timestamp'     : times,
            'comment'       : txt,
            'comment_url'   : comment_urls,
        })

    return text_dat

# Function: transforms dates to segment questions
def segment_by_time(text_dat, start_date, end_date):
    # Parse and localize start_date and end_date to UTC
    utc = pytz.UTC
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    start_dt = utc.localize(start_dt)
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    end_dt = utc.localize(end_dt)

    # Get the comments and URLs between the date range start_date & end_date
    talk_dat = text_dat[(text_dat['timestamp'] >= start_dt) & (text_dat['timestamp'] <= end_dt)]
    
    gpt_talk_reduce = talk_dat[['comment', 'comment_url']]
    # To-Do: Learn how to get chatGPT to read a dataframe object, and update the prompts accordingly
    gpt_talk_str = gpt_talk_reduce.to_string(header = False, index = False)
    gpt_talk_str = re.sub('\s+', ' ', gpt_talk_str)
    
    return gpt_talk_str

def chat_with_gpt4(user_prompt, sys_prompt):
    _ = load_dotenv(find_dotenv())
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) 
    
    response = client.chat.completions.create(
        # Messages: priming the model for a response
        messages = [
            
            {'role' : 'system', 'content' : sys_prompt},# System "role" in which openAI responds
            {'role': 'user', 'content': user_prompt}    # What "I" am asking/telling the model
            ],
        model="gpt-4-turbo",                            # The openAI model for the project
        temperature=    0.8,                            # Lower = more flexibility, Higher = more accurate
        max_tokens=     4000                            # NOTICE: higher tokens, more money.
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
    # Validate openAPI key stored in .env
    # _ = load_dotenv(find_dotenv())
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))   

    # Call load_text function
    txt = load_text(talk_file)

    # Call segment_by_time function
    # To-Do: Find a way to automate these dates
    talk_dat0 = segment_by_time(txt, '2024-06-24', '2024-06-29')
    talk_dat1 = segment_by_time(txt, '2024-06-30', '2024-07-07') 

    # Call ex_func_prompt_gen from prompts.py 
    prompt_func = prompts.ligo_prompt(talk_dat0, talk_dat1)

    # Call chatGPT function
    #gsBot = chat_with_gpt3(prompt_func[0], prompt_func[1])
    gsBot = chat_with_gpt4(prompt_func[0], prompt_func[1])
    print(gsBot)
    
    return gsBot

gsBotResponse = main()