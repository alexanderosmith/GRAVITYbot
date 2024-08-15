#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Author: Alexander O. Smith, aosmith@syr.edu
# Current Maintainer: Alexander O. Smith, aosmith@syr.edu
# Last Update: August 14, 2024
# Program Goal:
# This script automates gathering aLOG posts from LIGO to be analyzed for Citizen Scientists
#####################################################################################################
# DEPENDENCIES ######################################################################################
import feedparser as fp                     # Parsing LIGO's aLOG RSSs
from bs4 import BeautifulSoup as bs         # Scraping static HTML urls
import requests
from datetime import datetime, timedelta    # Managing datetime objects
import lxml.html as lh                      # Translating HTML/XML/LXML to readable format
import pandas as pd                         # Dataframe stuff (Pandas and CSV)
import csv, ssl                             # SSL: dealing with RSS security certificate issues
#####################################################################################################
# Might need to scrape individually: Saved for later
VIRGO_url = "https://logbook.virgo-gw.eu/virgo/"
KAGRA_url = "https://klog.icrr.u-tokyo.ac.jp/osl/"
#####################################################################################################
# FUNCTIONS #########################################################################################
# 0. alog_scrap     : (incomplete) a function to scrape the entire alog
# 1. rss_reduce     : reduces all RSS feeds to necessary data and outputs them into a dataframe
# 2. csv_cleanup    : cleans up the saved data for use in __main__.py
# 2. warnings       : simple text that states the limitation of this script for now
# 3. main           : enables a call within __main__.py
#####################################################################################################

# A function to scrape the full alog.
# (Incomplete)
def alog_scrape():

    # Empty dataframe for scrape to fill
    df = pd.DataFrame(
        # Try to match all the data from the RSS feed.
        columns=[
            'entry_title', 
            'entry_url', 
            'rss_url',
            'entry_date', 
            'text', 
            'tags', 
            'full_html'
            ])
    
    # Each of the alog pages URLs
    # Future To-Do: gather Kagra and Virgo?
    alog_pages = [
        'https://alog.ligo-wa.caltech.edu/aLOG/',
        'https://alog.ligo-la.caltech.edu/aLOG/',
    ]

    # Loop to process URLs using bs4 and requests modules
    for a in alog_pages:
        alog_page = request.get(a)
        soup = BeautifulSoup(alog_page.text, 'html.parser')







def rss_reduce(weeks=2):
    # Initiate Dataframe with Column Names
    df = pd.DataFrame(
        columns=[
            'entry_title', 
            'entry_url', 
            'rss_url',
            'entry_date', 
            'text', 
            'tags', 
            'full_html'
            ]
        )
    
    # Fixes a HTTP certificate issue with the RSS feeds
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    
    # Existing RSS Feeds (2 other aLOG URLs don't have these and may need to scrape)
    LIGO_RSSs = [
        "https://alog.ligo-wa.caltech.edu/aLOG/rss-feed.php", # LHO
        "https://alog.ligo-la.caltech.edu/aLOG/rss-feed.php", # LLO
        ]

    # Connect with the RSS feed (returns a dictionary item)
    for f in LIGO_RSSs:
        rss_feed = fp.parse(f)

        # Define the time range
        now = datetime.now()
        time_range = timedelta(weeks=weeks)

        # Iterate through entries and filter by the time range
        for entry in rss_feed.entries:
            entry_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)
            if now - entry_date <= time_range:
                # Get the relevant data from the RSS feed
                entry_title = entry.title
                entry_url = entry.link
                entry_date = entry.published 
                rss_url = entry.title_detail.base
                tags = entry.tags[0]
                full_html = entry.summary

                # Clean text (format HTML)
                soup = bs(full_html, 'html')
                text = soup.find_all("p")[2:] # After this is the entry

                # Build row as dictionary
                row = {
                    'entry_title': entry_title,
                    'entry_url': entry_url,
                    'rss_url':rss_url,
                    'entry_date': entry_date,
                    'text': text,
                    'tags': tags,
                    'full_html': full_html,
                    }
            # Append row to dataframe object
            df = pd.concat(
                [df, pd.DataFrame([row])], 
                ignore_index=True)
    
    #

    # Return completed dataframe
    return df

#def csv_cleanup():
# clean up duplicate entries in csv
# clean up text in a new column using regex?
# If we scrape other data, we need to figure out how to retrofit that data to the RSS feed

def warnings():
    print(
        """
        #####################################################################################################
        # WARNING: The functionality of aLOG Summary is severely limited at present. ########################
        #####################################################################################################
        POTENTIAL ISSUES:
        1. RSS Feed only looks back to what is visible in the RSS URL which may not be enough of a summary.
        2. The output CSV needs formatting. Check the CSV to see if the data is clean enough for use.
        3. Outside of LIGO aLOG data, this file may need extensive reformatting to be useful.
        #####################################################################################################
        """  
        )

def main():

    # A full scrape of LLO and LHO alog pages
    #scrape_df = alog_scrape()

    # Get RSS data as far back as possible.
    df = rss_reduce()
    # Append df to an existing CSV. Note set headers to True first run.
    df.to_csv('./_data/aLOG_RSS.csv', mode='a', header=False)

    #warn = warnings()

    return df, warn

#####################################################################################################
test = main()
#####################################################################################################
# BACKLOG: ##########################################################################################
# 1. Build CSV Clean Function
# 2. Take a look at cleaned text data for prompt inspirations for prompts.py
#####################################################################################################