#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Creator:         Alexander O. Smith, aosmith@syr.edu
# Current Maintainer:   Alexander O. Smith, aosmith@syr.edu
# Past Maintainers:     Alexander O. Smith (6/05/2024-present)
# Last Update:          July 16, 2024
# Program Goal:
# This file is primarily designed to access "Talk" comments from through the Zooniverse API
#####################################################################################################
# IMPORTANT REFERENCES/GUIDES: ######################################################################
# Zooniverse/Panoptes API Guides:
# Zooniverse API Authentication Info:       https://zooniverse.github.io/panoptes/#authentication
# Zooniverse Panoptes Python Client Info:   https://github.com/zooniverse/panoptes-python-client
# Zooniverse Panoptes Command Client Info:  https://github.com/zooniverse/panoptes-cli
# Zooniverse/Panoptes Contact Info:
# Contact for API Questions: contact@zooniverse.org
#   Notice, Laura Trouille claims emails to this contact cannot handle major debugging until at least
#   September of 2024. However, this email will reach her and the whole team for responses.
#####################################################################################################
#####################################################################################################
# DEPENDENCIES ######################################################################################
import os, requests, json, tarfile, dotenv
from io import BytesIO
from panoptes_client import panoptes, Panoptes, Project, exportable
from dotenv import find_dotenv, load_dotenv
from datetime import date
import urllib.request as urllib2
import pandas as pd
#####################################################################################################
# To Do:
# 1. Make more dynamic to deal with Panoptes API issues and once-per-day downloads
# 2. Figure out how to delete/backup older data
# 3. Decide on whether aLOG data should be integrated into this or distinct. 
#####################################################################################################

def get_talk_dat(slug):
    ### VALIDATING CREDENTIALS FOR DOWNLOADING TALK DATA ###
    # Make sure your Panoptes log-in credentials are added to the .env file
    _ = load_dotenv(find_dotenv())
    p_user = os.environ.get("PANOPTES_USER")
    p_pass = os.environ.get("PANOPTES_PASS")
    client = Panoptes.connect(username = p_user , password = p_pass)

    # Get Project ID via the project slug: make sure slug is in .env file
    project = Project.find(slug=str(slug))
    proj_id = int(str(project).split(' ')[1].split('>')[0])
    ###

    ### RETRIEVES TALK DATA FROM ZOONIVERSE VIA PANOPTES API ###
    # Getting the EXPORT URL: generates talk export and retrieves it
    talk_export = Project(proj_id).get_export(export_type='talk_comments', generate=True,  wait=False)
    # Description includes the URL of a tarfile containing talk data
    talk_describe = Project(proj_id).describe_export('talk_comments')
    # Tarfile URL location in talk_describe dictionary object
    talk_url = talk_describe['data_requests'][0]['url']
    # Localizing the tarfile and extracting it to ./_data directory
    talk_req = urllib2.urlopen(talk_url).read()
    file = BytesIO(talk_req)
    with tarfile.open(fileobj=file, mode='r:gz') as tar:
        # Extracting talk data
        tar.extractall(path="./_data")
    ###

def talk_clean(date):
    # TO-DO: this function should
    # 0. Become more dynamic to handle convert CSVs from alt dates, just in case...
    # 1. Remove/backup older JSONs CSVs (Ask team/look into files to make decisions)
    #       a.  Based on if else statement based on some number of JSONs files in _datacurrent date?
    #       b.  Based on if else statement based on current date?
    #       c.  Tarfile/backup/remove data occasionally based on some parameter?      
    talk_dat = pd.read_json(f'./_data/project-1104-comments_{date}.json')
    talk_dat.to_csv(f'./_data/project-1104-comments_{date}.csv')

def main():

    # Create an if/else statement to decide if the download is necessary
    _ = load_dotenv(find_dotenv())
    slug = os.environ.get("PANOPTES_SLUG")
    talk_dat = get_talk_dat(slug)
    
    current_date = date.today()
    panoptes_date = current_date.strftime('%Y-%m-%d')
    # Clean up and format talk data
    clean = talk_clean(date=panoptes_date)

talk = main()
#####################################################################################################

