#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Author: Alexander O. Smith, aosmith@syr.edu
# Current Maintainer: Alexander O. Smith, aosmith@syr.edu
# Last Update: April 24, 2024
# Program Goal:
# This file is dedicated to creating prompt variables and functions for chatGPT
#####################################################################################################
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# IMPORTANT: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Beginning Here: Do Not Edit !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#####################################################################################################
# Format all prompt variables as follows:
#####################################################################################################
# Define a variable which dynamically interprets a data string
#ex_user_prompt = f"""
#In the given text data
#{talk_dat}, 
#provide a list of primary topics of the data.
#"""
# Use Case: You might want to do this if all you need is a user prompt, however this will be rare.
#####################################################################################################
# Format all prompt function as follows:
#####################################################################################################
# Provide a name that makes sense based on a user story
# Provide at least one argument: a string of text data to evaluate
def ex_func_prompt_gen(talk_dat):
    # Required: provide a user prompt variable which takes the text data
    user_prompt = f"""
    For the following text data, provide a list of primary topics of the data:
    {talk_dat}
    """

    # Optional: provide a system prompt which tells the bot the context it is responding to.
    sys_prompt = f"""
    You are a helpful interpreter who translates forum conversations for physicists and engineers.
    """

    # Required: return user_prompt and all other variables created as inputs for the bot.
    return user_prompt, sys_prompt
# Use Case: You might need to do this if you need more dynamic calls with multiple variables that
#           are predefined here such that you don't have really long strings of text in the main
#           functions of the GravityBot_main.py file. You can add additional variables and objects
#           within each of these such that they may do more complicated tasks, such as tune model
#           temperature, or provide logical operators depending on text data, etc.
#####################################################################################################
#####################################################################################################
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# End of 'Do Not Edit' Section !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#####################################################################################################
# Make all functions and variables below using the above versions as template text.
#####################################################################################################
# Backlog Tasks:
# 3. Consider hashtags in the prompt (Carsten)
# 4. The following response might be valuable for the GravitySpy prompt  
#       **Additional Considerations and Observations**: The community is actively engaging in the use of tools like GWpy for analyzing glitches, prompting discussions on the effectiveness and limitations of these tools in providing accurate representations of glitches, especially in higher dimensions (3D).There is an ongoing dialogue about the need for improved navigation and management tools within the Zooniverse platform to handle large datasets more efficiently, particularly for sorting and identifying duplicates in glitch classifications. This includes suggestions for enhancements that would allow easier deletion or categorization of glitches directly from the user interface.
# 4. Consider multiple prompts for multiple purposes, and whether they should be automated
#####################################################################################################
def ligo_prompt(talk_dat0, talk_dat1):
    # Required: provide a user prompt variable which takes the text data
    user_prompt = f"""
    The following data are citizen scientist forum conversations. They identify and categorize glitches based on their unique characteristics. The data originally were in a dataframe of two columns. The first column was the "comment" text and the second was the "URL" affiliated with the comment. After each comment has been formatted such that it is followed by its URL. 
    
    Citizen scientists also attempt to identify underlying causes of each glitch. The forum data captures the evolving nature of glitch classification, the needs for new classifications, and novel exploration of glitch origins and characteristics by citizen scientists and researchers. The forum data emerges as a part of significant curiosity and engagement with the data, with the need for a clear summary.

These are the glitch classes we know about. These are not new, however there might be important conversations about their underlying causes:
    - 1080 Line 
    - 1400 Ripple 
    - 70 Hz Line 
    - Air Compressor (50 Hz)
    - Blip 
    - Chirp 
    - Crown 
    - Extremely Loud #nltk.download('punkt_tab') #May need to do this for a fresh nltk install
    - Helix 
    - Koi Fish 
    - Low-Frequency Line 
    - No Glitch 
    - Paired Doves 
    - Pizzicato 
    - Power Line (60 Hz) 
    - Repeating Blips 
    - Scattered Light 
    - Scratchy 
    - Tomte 
    - Uncategorized_Glitches 
    - Violin Mode Harmonic 
    - Wandering Line 
    - Whistle

    Consider "last week's" forum data:
    {talk_dat0}

    Now consider "this week's" forum data:
    {talk_dat1}

    Using these two sets of data, please provide at least three bullet points to answer the following questions. Each bullet point requires a couple of sentences of response. Under each bullet point, please provide the relevant URLs that played a part in your response for that bullet.
    
    I want a list of novel things which occur in "this week's" forum data realative to "last week's."
    
    1. Citizen scientists identify new glitch classifications based on their unique characteristics. What new glitch classes are proposed this week. If this week's forum data proposes a new glitch class realtive to last week, what is the glitch class? How is this glitch class described? Provide a bullet point for each new glitch class with two sentences describing the glitch. Provide the relevant URLs under each bullet point.

    2. Citizen scientists sometimes suggest there are problems with existing glitch classes: those previously listed. Are there any concerns regarding the glitch classes according to the citizen scientists? Do these persist in this week, or across both week's of Talk data? Provide two sentences describing each concern raised. Provide the relevant URLs under each bullet point.

    3. Citizen scientists learn by exploring classifications and technical aspects of glitches. Are there emerging questions related to the glitch classes, sensors, or gravitational wave science in this week's data? Describe each question and the reasoning for the question. Provide at two or three sentences describing these emerging questions. Provide the relevant URLs under each bullet point.

    4. Glitches are often related to ecological factors near the sensors or errors in the sensors themselves. Citizen scientists often attempt to analytically explain glitch occurrences with hypothetical origins of glitches, suggesting gained knowledge of the mechanisms of glitch occurances. If this week has more specific hypotheses about where glitch origins, what are these hypotheses and the reasons provided? Provide at two or three sentences describing each hypothesis. Provide the relevant URLs under each bullet point.

    5. Citizen scientists often question if issues are related to particular sensors or channels. Are there any emerging concerns about particular glitches' connections to sensors or channels this week relative to last week? If so, what specifically do they describe? Provide at least two sentences for these questions or thoughts. Provide the relevant URLs under each bullet point.
    """

    # Optional: provide a system prompt which tells the bot the context it is responding to.
    sys_prompt = f"""
    You are a technical interpreter who translates citizen science forum conversations for physicists and engineers. You are to describe particulars of where this ambiguity appears to come from.
    """

    # Required: return user_prompt and all other variables created as inputs for the bot.
    return user_prompt, sys_prompt


# THIS PROMPT IS STILL A BETA DESIGN, DO NOT RUN YET.

def alog_prompt(alog_dat0, alog_dat1):
    # Required: provide a user prompt variable which takes the text data
    user_prompt = f"""
    The following forum data are from LIGO affiliated scientists and engineers. LIGO affiliates often use LIGO's LVC Abbreviations and Acronyms, and so you will need to use them to interpret the discussions. The data involve discussions surrounding LIGO laboratory equiptment. The data originally were in a dataframe of two columns. The first column was the "comment" text and the second was the "URL" affiliated with the comment. After each comment has been formatted such that it is followed by its URL.

    Many of the acronyms relate to channels in LIGO sensors or other processes surrounding LIGO.

    Consider ALOG Dataset 1:
    {alog_dat0}

    Now consider ALOG Dataset 2:
    {alog_dat1}

    Provide responses for some the specific kinds of activities that are different for ALOG Dataset 2 relative to Dataset 1.
    
    1. Are there unresolved issues related to particular sensors? What are they? For each unresolved issue, provide a bullet. Also provide a sentence or two explaining each issue in pedestrian language. Please provide the URL that references back to the relevant ALOG conversation.

    2. Were there alterations to particular sensors? For each unresolved issue, provide a bullet and a sentence or two explaining each issue in pedestrian language. Provide the URLs that reference back ot the relevant ALOG conversation.
    """

    # Optional: provide a system prompt which tells the bot the context it is responding to.
    sys_prompt = f"""
    You are a interpreting engineers and physicists conversations surrounding the LIGO laboratories. You are helping a group of citizen scientists understand what is happening at the laboratory such that they can interpret Gravity Spy Glitch issues as quickly as possible. You are providing a summary in plain language that a citizen scientist might understand.
    """

    # Required: return user_prompt and all other variables created as inputs for the bot.
    return user_prompt, sys_prompt