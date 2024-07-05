#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Creator:         Alexander O. Smith, aosmith@syr.edu
# Current Maintainer:   Alexander O. Smith, aosmith@syr.edu
# Past Maintainers:     Alexander O. Smith (6/05/2024-present)
# Last Update:          June 18, 2024
# Program Goal:
# This file is primarily designed to access "Talk" comments from through the Zooniverse API
#####################################################################################################
# IMPORTANT REFERENCES/GUIDES: ######################################################################
# Zooniverse/Panoptes API Guides:
# Zooniverse API Authentication Info:       https://zooniverse.github.io/panoptes/#authentication
# Zooniverse Panoptes Python Client Info:   https://github.com/zooniverse/panoptes-python-client 
# Zooniverse Panoptes Command Client Info:  https://github.com/zooniverse/panoptes-cli 
# Zooniverse/Panoptes Contact Info:    
# Contact Laura Trouille (Avoid Emailing):  trouille@zooniverse.org
# Contact for API Questions (Main Contact): contact@zooniverse.org 
#   Notice, Laura claims emails to this contact cannot handle major debugging until at least
#   September of 2024. However, this email will reach her and the whole team for responses.    
#####################################################################################################
#####################################################################################################
# DEPENDENCIES ######################################################################################
import os, requests, json
from panoptes_client import panoptes, Panoptes, Project, exportable
from dotenv import find_dotenv, load_dotenv
import pandas as pd
#####################################################################################################
# Verify Panoptes credentials (make sure your credentials are added to the .env file) 
#   Notice: you must have proper role credentials to download data. 
#   If you do not have proper credentials, ask the project owner for them. 
_ = load_dotenv(find_dotenv())
p_user = os.environ.get("PANOPTES_USER")
p_pass = os.environ.get("PANOPTES_PASS")
client = Panoptes.connect(username = p_user , password = p_pass)

# Get Project ID via the project slug:
# The project slug is a part of the URL of your project. E.G.
#   Project url: https://www.zooniverse.org/projects/zooniverse/gravity-spy
#   Project slug: 'zooniverse/gravity-spy' 
def p_id(slug):
    project = Project.find(slug=str(slug))
    proj_id = int(str(project).split(' ')[1].split('>')[0])
    return proj_id
# Getting Project ID for Gravity Spy
proj_id = p_id('zooniverse/gravity-spy')

# Returns an Email with Project ID associated Talk forum data as JSON
talk_export = Project(proj_id).get_export(export_type='talk_comments', generate=True,  wait=True)
### NOTES FOR FUTURE UPDATES: ########################################################################
# When I run this for the second time, I get this error:
# panoptes_client.panoptes.PanoptesAPIException: Validation failed: Kind has already been created
# However, this exception does not seem to be documented, so I do not know how to address this.
# Although, I suppose I could follow the traceback to learn something: line 128 in json_request
# This resulted in a deadend for two reasons:
# 1. The source code isn't enumerated, and 2. where it appears the error occurred is calling "self"
# I'm going to call it quits for here, and move on... 
### DOCUMENTED STEPS FOR WORK AROUND UNTIL AUTOMATION IS SOLVED #####################################
# Current workaround from moderation requires a few steps:
# 1. Manually download the tar file from the p_user email to the data directory and untar it;
# 2. Import and deseriealize the JSON file;
# 3. Create the required dataframe from the JSON.
#####################################################################################################
# Import JSON as DataFrame, and save as CSV using Pandas:
talk_dat = pd.read_json('./_data/project-1104-comments_2024-06-18.json')
talk_dat.to_csv('./_data/project-1104-comments_2024-06-18.csv')


# Comparing Updated Talk Data with historical Talk Data
ex_talk_dat = pd.read_csv('./_data/ex_GS_TalkComments_2024-01-29.csv')
len(list(talk_dat))
len(list(ex_talk_dat))
#####################################################################################################
# TO-DO:
# Make function to save talk_dat as CSV file
#   Automate the naming convention of the JSON object
# Use the automated name for the import for the rest of the project
#####################################################################################################
# NOTES From Laura Trouille @ Zooniverse
# INSTRUCTIONS:
# You can query the Talk API directly to generate and get the status of both tag and comment exports. 
# To begin, you need to generate a valid Panoptes authentication token. This process is detailed here:
# https://zooniverse.github.io/panoptes/#authentication
#
# Once you have a valid token, you can make a request to the API to generate an export, like this:
#
# POST https://talk.zooniverse.org/data_requests
#
# {
#   "data_requests": {
#     "section": "project-6676",
#     "kind": "comments"
#   }
# }
# with the same Authentication, Content-Type, and Accept headers detailed in the docs linked above and 
# replacing the project ID with your own. The above will generate a Comment export, the only other 
# valid kind is tags. The response will indicate that the export now has a 'pending' status. You can 
# check on the status of the export by querying Talk for it:
#
# GET https://talk.zooniverse.org/data_requests?section=project-6676&kind=comments
# 
# The kind=comments parameter is optional, providing only the section will return both if they exist. 
# If the export is finished, the response will include the URL that it can be downloaded from. These 
# exports (as well as the download links) are valid for 24 hours from when they're created before 
# they're removed and need to be generated again. 
# 
# A potentially easier route would be to use https://github.com/zooniverse/panoptes-cli. Scroll down 
# on that page and you'll see the command line for generating Talk exports for a project. (And/or you 
# can use https://github.com/zooniverse/panoptes-python-client). 
#
# Note: as with any project-wide data export, you'll be grabbing all data from all time every time and 
# so the exports can get large in size. 
#####################################################################################################

