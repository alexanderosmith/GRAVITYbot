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
    The following data are from citizen scientists identifying and categorizing new types of glitches based on their unique characteristics. The data originally were in a pandas dataframe of two columns. The first column was the "comment" text and the second was the "URL" affiliated with that comment. After having converted this pandas dataframe to string, each comment is now followed by its URL. 
    
    The citizen scientists investigate underlying causes of various types of glitches observed in the LIGO sensors. I am trying to capture the evolving nature of glitch classification, the needs for new classifications, and novel exploration of glitch origins and characteristics by citizen scientists and researchers. The Talk data emerges as a part of significant curiosity and engagement with the data, with the need for a clear summary.

    Consider Talk Dataset 1:
    {talk_dat0}

    Now consider Talk Dataset 2:
    {talk_dat1}

    Also, importantly, we already know about several glitch classes. So if you see these, they are not new:
    - 1080 Line 
    - 1400 Ripple 
    - 70 Hz Line 
    - Air Compressor (50 Hz)
    - Blip 
    - Chirp 
    - Crown 
    - Extremely Loud 
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

    Below are a list of things I would like an answer for. Also, importantly, if your answer uses a comment, after the end of each answer provide, provide a list of URL variables which played a part in your response.
    
    I want a list of novel things which occur in Talk Dataset 2 realtive to Talk Dataset 1.
    1. Citizen scientists are actively identifying and categorizing new types of glitches based on their unique characteristics. I want to know what new glitch classes are proposed. If Talk data set 2 proposes a new glitch class realtive to Talk data set 1, what is the glitch class? How do they describe this glitch class?

    2. Citizen scientists sometimes question whether there are problems with existing glitch classes: i.e. those listed. I am interested in whether there are any concerns regarding the glitch classes according to the citizen scientists, and whether or not they persist in both  sets of Talk Datasets, or if concerns occur only in Talk Dataset 2. If there are concerns, what problems are they claiming exist with the classifcations?

    3. Additionally, citizen scientists wish to deepen their knowledge by exploring and learning classifications and technical aspects of glitches. I am interested in whether there are emerging questions related to the glitch classes, sensors, or gravitational wave science in Talk data set 2 relative to Talk data set 1. Describe each question and the reasoning for the question. 

    4. The origins of glitches are usually related to enviornemntal factors near the sensors or errors in measurements of sensors themselves. Citizen scientists often attempt to analytically correlate external conditions with glitch occurrences, providing specific hypothetical origins of glitches suggesting potentially gained knowledge in underlying mechanisms of glitch causes or their appearances in spectograms. If Talk data set 2 has more specific hypotheses about where glitch origins, what are these hypotheses? What is each hypothesis' analytical motivation?

    5. Often citizen scientists will question if issues are specifically related to particular sensors or channels. Are there any emerging questions or thoughts concerning the way particular glitches are connected to sensors or channels in Talk Dataset 2 relative to Talk Dataset 1? If these thoughts or questions exist, what specifically do they describe?
    """

    # Optional: provide a system prompt which tells the bot the context it is responding to.
    sys_prompt = f"""
    You are a technical interpreter who translates citizen science forum conversations for physicists and engineers. You are to describe particulars of where this ambiguity appears to come from.
    """

    # Required: return user_prompt and all other variables created as inputs for the bot.
    return user_prompt, sys_prompt


# THIS PROMPT IS STILL A BETA DESIGN, DO NOT RUN YET.

def gs_prompt(talk_dat0, talk_dat1):
    # Required: provide a user prompt variable which takes the text data
    user_prompt = f"""
    The following data are from citizen scientists identifying and categorizing new types of glitches based on their unique characteristics. The data originally were in a pandas dataframe of two columns. The first column was the comment text and the second was the URL affiliated with that comment. After having converted this pandas dataframe to string, each comment is now followed by its URL. 
    
    The citizen scientists investigate underlying causes of various types of glitches observed in the LIGO sensors. I am trying to capture the evolving nature of glitch classification, the needs for new classifications, and novel exploration of glitch origins and characteristics by citizen scientists and researchers. The Talk data emerges as a part of significant curiosity and engagement with the data, with the need for a clear summary.

    Consider Talk Dataset 1:
    {talk_dat0}

    Now consider Talk Dataset 2:
    {talk_dat1}

    2. Citizen scientists sometimes question whether there are problems with existing glitch classes: i.e. those listed. I am interested in whether there are any concerns regarding the glitch classes according to the citizen scientists, and whether or not they persist in both  sets of Talk Datasets, or if concerns occur only in Talk Dataset 2. If there are concerns, what problems are they claiming exist with the classifcations?

    3. Additionally, citizen scientists wish to deepen their knowledge by exploring and learning classifications and technical aspects of glitches. I am interested in whether there are emerging questions related to the glitch classes, sensors, or gravitational wave science in Talk data set 2 relative to Talk data set 1. Describe each question and the reasoning for the question. 

    4. The origins of glitches are usually related to enviornemntal factors near the sensors or errors in measurements of sensors themselves. Citizen scientists often attempt to analytically correlate external conditions with glitch occurrences, providing specific hypothetical origins of glitches suggesting potentially gained knowledge in underlying mechanisms of glitch causes or their appearances in spectograms. If Talk data set 2 has more specific hypotheses about where glitch origins, what are these hypotheses? What is each hypothesis' analytical motivation?

    5. Often citizen scientists will question if issues are specifically related to particular sensors or channels. Are there any emerging questions or thoughts concerning the way particular glitches are connected to sensors or channels in Talk Dataset 2 relative to Talk Dataset 1? If these thoughts or questions exist, what specifically do they describe?
    """

    # Optional: provide a system prompt which tells the bot the context it is responding to.
    sys_prompt = f"""
    You are a design consultant and research collaborator who translates citizen science forum conversations for the designers of the forum and the Citizen Science project. You also suggest possible research topics related to learning occuring through forum activity.
    """

    # Required: return user_prompt and all other variables created as inputs for the bot.
    return user_prompt, sys_prompt