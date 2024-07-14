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
import os, requests, json, tarfile
from io import BytesIO
from panoptes_client import panoptes, Panoptes, Project, exportable
from dotenv import find_dotenv, load_dotenv
import urllib.request as urllib2
import pandas as pd
#####################################################################################################
# To Do:
# 1. Figure out the order/necessity of describe_export(), generate_export(), get_export()
# 2. Clean up first function. It could probably be simpler. E.g. not a function in a function.
#   a. get_talk_dat() could accept "slug" (the project url extension)
#   b. Then def p_id(slug) could probably be restructured such that it's not a function.
#   c. Add the tar extraction stuff into the function
#   d. Get rid of comments as necessary. This is really comment heavy. 
#   e. Document more for future.
# 3. Generate a main function that decides if a new data download is necessary?   
def get_talk_dat():
    
    # Make sure your Panoptes log-in credentials are added to the .env file 
    # If you do not have proper credentials, ask the project owner for them. 
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
    #######
    # TO-DO! I need to figure out which of these functions actually returns the URL such that talk_describe() reads it.
    # Order of testing! (DON'T FORGET TO DO THIS IN THIS ORDER TO SAVE TIME)
    # 1. First run talk_describe and print the results. If URL is not there, then that doesn't generate the URL.
    # 2. Run talk_generate and then talk_describe. If URL is not in talk_describe, then give it a few minutes, and try again.
    # 3. If 1 and 2 don't work, then try talk_export, then talk_describe. 
    # 4. If none of these work then we are very confused. 
    #######
    # Returns an Email with Project ID associated Talk forum data as JSON
    talk_describe = Project(proj_id).describe_export('talk_comments')
    #talk_generate = Project(proj_id).generate_export('talk_comments')
    #talk_export = Project(proj_id).get_export(export_type='talk_comments', generate=False,  wait=True)
    return talk_describe

print(get_talk_dat())
talk_dat = get_talk_dat()
talk_url = talk_dat['data_requests'][0]['url']
talk_req = urllib2.urlopen(talk_url).read()
file = BytesIO(talk_req)

with tarfile.open(fileobj=file, mode='r:gz') as tar:
    # This extracts the file
    tar.extractall(path="./_data")
#contents = tarfile.open(fileobj=talk_req, mode='r:*')

# 'https://zooniverse-static.s3.amazonaws.com/talk-exports.zooniverse.org/project-1104-comments_2024-07-13.tar.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIHHVKYCIG4GRJ4KQ%2F20240713%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240713T185906Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=a69ffc5bf3651a0a8417e95ef3f8ae270b65b5f7becc8dcc6bddafa36f596367'

### NOTES FOR FUTURE UPDATES: ########################################################################
#
#####################################################################################################
# Import JSON as DataFrame, and save as CSV using Pandas:
talk_dat = pd.read_json('./_data/project-1104-comments_2024-07-08.json')
talk_dat.to_csv('./_data/project-1104-comments_2024-07-08.csv')


# Comparing Updated Talk Data with historical Talk Data
ex_talk_dat = pd.read_csv('./_data/ex_GS_TalkComments_2024-07-08.csv')
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

