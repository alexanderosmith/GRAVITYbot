import numpy as np
import pandas as pd
from datetime import datetime
from dateutil import parser
import os, re, csv

# To load the data dynamically with functions below
talk_file_path = '/home/aosmith/Documents/Scripts/Projects/GravitySpy/Data/GS_TalkComments_2024-01-29.csv'

# Load data for investigating the file outside of functions.
talk_data = pd.read_csv('/home/aosmith/Documents/Scripts/Projects/GravitySpy/Data/GS_TalkComments_2024-01-29.csv')

#cols = talk_data2.columns
#print(cols)
# Talk Column Names, and Definitions:
# 'Unnamed: 0'              ID assigned to each row in dataframe ??? (maybe useless)
# 'document.id',            Uniform 1... meaningless?
# 'array.index',            Same as 'Unnamed: 0'
# 'board_id',               Board/Forum Thread ID #
# 'board_title',            Board Name/Forum Thread Topic (visible on website)
# 'board_description',      Board/Forum Thread description
# 'discussion_id',          ?
# 'discussion_title',       Either something like 'Subject 5736418' or user provided text  
# 'comment_id',             Comment ID
# 'comment_body',           The full text of the comment
# 'comment_focus_type',     nan or 'Subject' ???
# 'comment_user_id',        User ID of comment
# 'comment_user_login',     User Login Name
# 'comment_created_at'      Comment Time (In YYYY-MM-DDTHH:MM:SS.???Z Format)

#set(talk_data2['discussion_title'])

# Columns that seem relatively important columns for topic modeling:
# board_title, board_description, comment_body, comment_created_at

###############################################################################################
# Modified from Gabe's script: Analyzing_tool2.py
# Comments added for clarity

# A function using regex to find questions in comments 
def load_and_id_qs(file_path):
    questions = []
    with open(file_path, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row['comment_body']  
            # Replace 'YourColumnNameHere' with the actual column name containing the questions
            timestamp = row['comment_created_at']  
            # Replace with the actual column name for timestamp
            if re.search(r'.\?', text):  # Regex to find questions
                questions.append({'timestamp': timestamp, 'text': text})
    return questions


# A function to segement questions by time frame and transform dates
def segment_by_time(questions, start_date, end_date):
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    segmented_questions = [q for q in questions if start_dt <= datetime.strptime(
        q['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ') <= end_dt]
    return segmented_questions
###############################################################################################

# Rewritten Main Function

def main():

    # Call load_and_id_qs
    questions = load_and_id_qs(talk_file_path)
    # Example: Analyze questions between '2021-01-01' and '2021-12-31'
    segmented_questions = segment_by_time(questions, '2024-01-01', '2024-12-31')

    #Return 
    for qs in segmented_questions[:-2]:
        print(f"Q: {qs['text']}\n")

    #for q in questions:
    #    print(q)

main()
#################################################################################################
# Explore Talk Data

talk_data.comment_body[-2:-1]

url_comment = "More probably a closely spaced row of narrow little arches, thus a form of fast scattering - similar to the old Scratchy from O1 and O2, but the vibrating reflecting item that had caused the original Scratchies was removed at both observatories after O2, so something else must be involved here. There haven't yet been enough of them to justify a glitch class proposal, but we've seen a handful of [similar subjects from Hanford](+tab+/projects/zooniverse/gravity-spy/talk/762/2961842?comment=5058342) on at least three occasions during ER15 and O4."

if re.search(r'.\?'+'^?.*=', url_comment):
    print(url_comment)

if re.search(r'^=.*\s', url_comment):
    print(url_comment)



talk_text = talk_data.comment_body
quests = []
for t in talk_text:
    t = str(t)
    t = t.lower()
    t = re.sub('\n', ' ', t)
    t = re.sub('\'|\"', '', t)
    if re.search(r'.\?', t):  # Regex to find questions
        quests.append(t)
    

quests[0:10]
talk_data.comment_body[24]
len(quests)

#################################################################################################
# From Corey:
# 
# 1. Generative AI Talk digests: Requires no cleaning (at the moment) and would use the .csv of comments to pass a subset of data to a genAI that will summarize the data in some meaningful way via a weekly digest or open prompts. 
# 
# A tool using RShiny which filters date filter and an input field for a question/prompt and then passing the data to the API and returning the summary. 
# 
# This might involve passing templates to format the responses from the tool. Here's an example: https://shiny.posit.co/r/gallery/education/radiant/

# 2. Cleaning comment data / analyzing Talk dynamics? 
# 
# Gabrielle's goal was to have GenAI summarize Talk data (which we’ve done in several papers). Some level of data cleaning might be useful before passing to the summarization tool, be probably content coding and not extraction since genAI can already read # and identify URLs.


# Restructured Order of Operations:
# 1. Use the structure above to filter dates
# 2.a. Use the date filter on comments to generate an automated weekly summary.
# 3.a Use the R code or translate that code to Python if easier.
# 2.b. Use the date filter for an Rshiny prompt (e.g. learn Rshiny)

# To Do:
# 1. Figure out how to automate weekly input dates for the date function.
# 2. Convert Corey's R code to Python begin automating reports with existing CSV. 
# 3. Figure out how to automate the download the new Talk or how to get it regularly. 
# 4. 