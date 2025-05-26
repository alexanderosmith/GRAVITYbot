#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Creator: Alexander O. Smith (2024-present), aosmith@syr.edu
# Current Maintainer: Alexander O. Smith, aosmith@syr.edu
# Last Update: May 25, 2025
# Program Goal:
# This file is the main talk summary executable Python file of "GRAVITYbot"
#####################################################################################################
#####################################################################################################
# DEPENDENCIES ######################################################################################
# Package Dependencies
import os, sys, re, csv, openai, pytz, smtplib, ssl
from datetime import datetime, timezone, date, timedelta
import pandas as pd

# API Imports
from openai import OpenAI
from panoptes_client import Panoptes

# Local environment imports and path appends
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import find_dotenv, load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../_data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../_output')))
import prompts, talk_data, emails
#####################################################################################################
# Functions #########################################################################################
# 0. start_end_dates    :   produces two adjacent weeks spans
# 1. clean_comments     :   adds all regex cleaning for talk data into one function
# 2. load_talk          :   loads talk data and cleans it
# 3. segment_by_time    :   limits talk data to those within particular dates


# Produces start and end dates for the most recent two weeks of Talk data.
def start_end_dates():
    print('Loading the most recent Talk forum data...')
    # Today's date
    current_date = datetime.now(timezone.utc)
    # Set talk_file to a 0 length string for the while loop
    talk_file = ''
    count = 1
    # While loop searches until length of talk_file >= 1 OR
    # it will stop after 1000 iterations (= 10000 days prior current date)
    while len(talk_file) < 1:
        # Set all dates relative to "current_time"
        talk_dat1_start = current_date - timedelta(days=7)
        talk_dat0_end = talk_dat1_start - timedelta(days=1)
        talk_dat0_start = talk_dat0_end - timedelta(days=7)
        
        # Convert all the dates to strings formatted as the Talk file name conventions.
        talk_dat1_start = talk_dat1_start.strftime('%Y-%m-%d')
        talk_dat0_end = talk_dat0_end.strftime('%Y-%m-%d')
        talk_dat0_start = talk_dat0_start.strftime('%Y-%m-%d')
        talk_dat1_end = current_date.strftime('%Y-%m-%d')
        print(f'Checking for file date: {talk_dat1_end}')

        # Search _data directory for the most recent file, based on "current_date"
        file_search = os.listdir('_data/')
        for f in file_search:
            if re.match(f'project-1104-comments_{talk_dat1_end}.csv', f):
                talk_file = f
                print(
                f"""
NOTICE: Talk file "{talk_file}" found! 
    Generating date range for summary...\n
                """
                )

        # If the earliest date searched in Talk data is older than Zooniverse, stop.
        if talk_dat0_start == '2009-12-12':
            print("""
DATA ISSUE: It appears current Talk Data needs to be imported to the _data directory.\n
TROUBLESHOOTING SUGGESTIONS:
    1. Make sure __main__.main() is running load_text(file_path) with the expected talk data file path.
    2. Make sure the proper panoptes credentials are configured in the .env file.
    3. Ask the Zooniverse project owner for proper panoptes credentials rights to download data.
    4. Check whether the Zooniverse "slug" in dotenv is correct.
    5. Troubleshoot talk_data.py.
            """)
            break

        current_date -= timedelta(days=1)

    return {
        'talk_file'         :   talk_file, 
        'talk_dat1_start'   :   talk_dat1_start, 
        'talk_dat1_end'     :   talk_dat1_end, 
        'talk_dat0_start'   :   talk_dat0_start, 
        'talk_dat0_end'     :   talk_dat0_end 
    }

# Function: All regex cleaning for Talk Comments added to one function
def clean_comments(text):
    text = re.sub('This comment has been deleted', '', text)
    text = re.sub(r'https.*\s', ' ', text)
    text = re.sub(r'@\w+', ' ', text)
    text = re.sub(r'Hi,\n|Hello,\n', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Thanks|Thank you', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[^A-Za-z0-9\>\s\'\"\?\.\!]', ' ', text)
    text = re.sub(r'\.+', ' ', text)
    text = re.sub('projects zooniverse gravity spy talk subjects', ' ', text)
    text = re.sub('zooniverse gravity spy talk comment page', ' ', text)
    text = re.sub(r'\s[b-z][\.\s]', ' ', text)
    text = re.sub(r'^v$', '', text)
    text = re.sub(r'[\n]', ' ', text)
    text = re.sub(r'[0-9]+\s', ' ', text)
    text = re.sub(r'[a-z][0-9]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Function: loads Talk data and gets comments which contain text
def load_talk(file_path):
    talk_url = 'https://www.zooniverse.org/projects/zooniverse/gravity-spy/talk/'

    # Import CSV of Talk as Pandas DataFrame
    reader = pd.read_csv(file_path, encoding='utf8')
    

    # NOTICE: gb_id is GRAVITYbot's user_id. We remove affiliated rows that match comment_user_id to reduce circularity in summaries
    _ = load_dotenv(find_dotenv())
    gb_id = os.environ.get("PANOPTES_ID")

    # NOTICE: these could be added to the dotenv file to automate them rather than hardcode them
    # Drop rows with board_ids associated with GRAVITYbot: 6872, 6946, 6945
    drop_board = [6872] # This will reduce the risk of circular summaries
    # drop all rows with these board_ids
    reader = reader[reader.board_id.isin(drop_board) == False]
    # Drop GRAVITYbot User_id
    drop_gb = [gb_id]
    reader = reader[reader.comment_user_id.isin(drop_gb) == False]

    # Define the Universal timezone
    utc = pytz.UTC

    timestamp = reader['comment_created_at']
    times = pd.to_datetime(timestamp, utc=True, format='mixed', errors='raise')
    comment_urls =  reader.apply(
        lambda row: f"{talk_url}{row['board_id']}/{row['discussion_id']}", axis=1)
    text = reader['comment_body'].fillna('').apply(clean_comments)

    # Generate DataFrame of data necessary for GRAVITYbot interpretation
    text_dat = pd.DataFrame({
        'timestamp'     : times,
        'comment'       : text,
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
    gpt_talk_str = gpt_talk_reduce.to_string(header = False, index = False)
    gpt_talk_str = re.sub(r'\s+', ' ', gpt_talk_str)
    
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

def main():
    # Get Talk Data from Panoptes API
    #talkdata = talk_data.main()
    print("GravitySpy Talk Forum Data Request Complete")
    
    # Get the most recent csv name, and the start and end dates for the most recent two weeks.     
    time_deltas = start_end_dates()

    # Load Gravity Spy Talk data file
    talkload = load_talk(f"_data/{time_deltas['talk_file']}")

    # Call segment_by_time function using the automated start-end days.
    talk_dat0 = segment_by_time(talkload, time_deltas['talk_dat0_start'], time_deltas['talk_dat0_end']) # Talk Older week
    talk_dat1 = segment_by_time(talkload, time_deltas['talk_dat1_start'], time_deltas['talk_dat1_end']) # Talk Newer week
    
    current_day = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    # Call ex_func_prompt_gen from prompts.py 
    talk_prompt = prompts.ligo_prompt(talk_dat0, talk_dat1)

    # Call chatGPT function for Zooniverse Talk summary
    try:
        gsBot = chat_with_gpt4(talk_prompt[0], talk_prompt[1])
        with open(f'./_output/ZooniverseTalkSummary_{current_day}.md', 'w') as gsBotResp:
            gsBotResp.write(gsBot)
            gsBotResp.close()
    except:
        print("WARNING: No Zooniverse Talk Summary file saved.")

    # Sending Email containing Zooniverse Talk summary
    print("Sending Email...")
    #try:
    email = emails.main(date = current_day, body = gsBot)
    #except:
    #    print("WARNING: Email failed to send.")
     
gsBotResponse = main()