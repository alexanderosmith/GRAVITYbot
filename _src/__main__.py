#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Creator: Alexander O. Smith (2024-present), aosmith@syr.edu
# Current Maintainer: Alexander O. Smith, aosmith@syr.edu
# Last Update: August 06, 2024
# Program Goal:
# This file is the main executable Python file of "GRAVITYbot"
#####################################################################################################
#####################################################################################################
# DEPENDENCIES ######################################################################################
# Package Dependencies
import os, sys, pytz, re, csv, openai
from datetime import datetime, date, timedelta
import pandas as pd
# API Imports
from openai import OpenAI
from panoptes_client import Panoptes
# Local enviornment imports and path appends
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import find_dotenv, load_dotenv
#import _alog as alog # This file needs to be fixed before I use it.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../_data')))
import prompts, talk_data, alog
# Example of how to import a prompt from prompts py file.
#####################################################################################################
# Functions #########################################################################################
# 0. start_end_dates    :   produces dates that span two adjacent weeks dynamic to most recent talk 
#                           data
# 1. load_text          :   loads talk data
# 2. segment_by_time    :   limits talk data to those within particular dates
# 3. chat_with_gpt4     :   calls chatGPT4 bot (more expensive, higher input rate limit)
# 4. main               :   initiates above functions, and loads prompt file info
# POSSIBLE FUTURE FUNCTIONS
# 1. Perhaps we could add an opensource LLM to make a "free" version of the summarizer
#####################################################################################################
# Produces start and end dates for the most recent two weeks of Talk data.
def start_end_dates():
    print('Finding most recent Talk data file...\n')
    # Today's date
    current_date = datetime.utcnow()
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
        #print(f'Attempting to find a file for date {current_date}')
    return {
        'talk_file'         :   talk_file, 
        'talk_dat1_start'   :   talk_dat1_start, 
        'talk_dat1_end'     :   talk_dat1_end, 
        'talk_dat0_start'   :   talk_dat0_start, 
        'talk_dat0_end'     :   talk_dat0_end 
    }

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

    # Retrieve most updated talk data (will only work once per 24 hours)
    talkdata = talk_data.main()
    # NOTICE: talk_data.main() function requires more clear comms with panoptes API warnings
    # To-Do: Update the talk_data's main function to do this better for future warnings.

    # Get the most recent csv name, and the start and end dates for the most recen two weeks.     
    time_deltas = start_end_dates()
    talk_dat = f"_data/{time_deltas['talk_file']}"

    # Load talk data file
    txt = load_text(talk_dat)

    # Call segment_by_time function using the automated start-end days.
    talk_dat0 = segment_by_time(txt, time_deltas['talk_dat0_start'], time_deltas['talk_dat0_end']) # Older week
    talk_dat1 = segment_by_time(txt, time_deltas['talk_dat1_start'], time_deltas['talk_dat1_end']) # Newer week

    # Call ex_func_prompt_gen from prompts.py 
    prompt_func = prompts.ligo_prompt(talk_dat0, talk_dat1)

    # Call chatGPT function
    gsBot = chat_with_gpt4(prompt_func[0], prompt_func[1])
    current_day = datetime.utcnow().strftime('%Y-%m-%d')
    with open(f'./_output/ZooniverseTalkSummary_{current_day}.md', 'w') as gsBotResp:
        gsBotResp.write(gsBot)
        gsBotResp.close()
    print(gsBot)
    
    return gsBot
     

gsBotResponse = main()