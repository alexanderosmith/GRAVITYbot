#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Creator: Alexander O. Smith (2025-present), aosmith@syr.edu
# Current Maintainer: Alexander O. Smith, aosmith@syr.edu
# Last Update: April 2, 2025
# Program Goal:
# This file posts the aLOG summary "GRAVITYbot"
#####################################################################################################
#####################################################################################################
# DEPENDENCIES ######################################################################################
# Package Dependencies
import os, sys, requests
from dotenv import find_dotenv, load_dotenv
from panoptes_client.panoptes import Talk, Panoptes
#####################################################################################################
# Getting dotenv credentials necessary to send the message.
_ = load_dotenv(find_dotenv())
username = os.environ.get("PANOPTES_USER")
password = os.environ.get("PANOPTES_PASS")
Panoptes.connect(username=username, password=password)
user_id = os.environ.get("PANOPTES_ID") #os.environ.get("PANOPTES_USER")
#####################################################################################################
# Build the message 
talk = Talk()
# This needs to be generated and updated to whatever the discussion ID is, 
# It is at the end of the URL of the discussion post
discussion_id = 3633195

# Message to post
body = "This is an aLOG hello world"

payload = { 'comments': {
                         'user_id': user_id, 'discussion_id': discussion_id, 'body': body
               }}

# Posting the message
talk.http_post('comments', json=payload)


#####################################################################################################
# From Laura and Cliff:
#
# from panoptes_client.panoptes import Talk
# talk = Talk()
# user_id = USER_ID_TO_POST_COMMENT
# discussion_id = ID_OF_DISCUSSION_THREAD
# body = POST CONTENT
# payload = { 'comments': {
#                        'user_id': user_id, 'discussion_id': discussion_id, 'body': body
#                }}
# 
# talk.http_post('comments', json=payload)
# 
# Notice your user_id =/= your username. 
# You can map a login to a user_id using the User.where() function:
# from panoptes_client import User
# user = next(User.where(login='your-user-name'))
# print(user.id)
#
# You need to login so that the Client can pass along the appropriate API token as part of the request. Following the Client documentation (see https://panoptes-python-client.readthedocs.io/en/latest/user_guide.html#usage-examples), add the following login command at the beginning of the script:
#
# Note: to keep credentials out of script and logs, you could use the following alternatives:
#a) Panoptes.connect(login='interactive') # command will prompt for username and/or password
#b) Set PANOPTES_USERNAME and PANOPTES_PASSWORD environment variables that would be accessible via os.environ.get() call.