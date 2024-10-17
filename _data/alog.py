#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Author: Alexander O. Smith, aosmith@syr.edu
# Current Maintainer: Alexander O. Smith, aosmith@syr.edu
# Last Update: Sept 5, 2024
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
import csv, ssl, re                         # SSL: dealing with RSS security certificate issues
#####################################################################################################
# Might need to scrape individually: Saved for later
VIRGO_url = "https://logbook.virgo-gw.eu/virgo/"
KAGRA_url = "https://klog.icrr.u-tokyo.ac.jp/osl/"
#####################################################################################################
# FUNCTIONS #########################################################################################
# 1. rss_reduce     : reduces all RSS feeds to necessary data and outputs them into a dataframe
# 2. csv_cleanup    : cleans up the saved data for use in __main__.py
# 2. warnings       : simple text that states the limitation of this script for now
# 3. main           : enables a call within __main__.py
#####################################################################################################
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
                #print(type(full_html))
                
                # From full_html there's at least three more useful variables: report_id, author, text
                att_html = bs(full_html, "html.parser")
                
                # Cleaning Report ID
                rep_id = att_html.find_all("p")[1].text
                rep_id = re.sub('Report ID: ', '', rep_id)        
                    
                # Cleaning Author Email
                auth = att_html.p.text
                auth = re.sub('Author: ', '', auth)
                80386
                # Cleaning Text
                txt = att_html.get_text(separator=' ')
                txt = re.sub('[\n\t]', '', txt)
                txt = re.sub('[,;]', '', txt)

                txt = re.sub(r'^.*Report ID: \d+ ', '', txt)
                txt = re.sub(' Images attached to this report ', '', txt)
                txt = re.sub(r'\s+', ' ', txt)

                # Build By Row As Dictionary
                row = {
                    'entry_title': entry_title,
                    'entry_url': entry_url,
                    'rss_url':rss_url,
                    'entry_date': entry_date,
                    'text': txt,
                    'tags': tags,
                    #'full_html': full_html,
                    'report_id': rep_id,
                    'author_email': auth,

                    }
            # Append Row to Dataframe
            df = pd.concat(
                [df, pd.DataFrame([row])], 
                ignore_index=True
                )

    # Return Dataframe
    return df

def csv_cleanup():
    # Relative CSV Path
    alog_path = './_data/aLOG_RSS.csv'
    
    # Import CSV
    alog_dat = pd.read_csv(alog_path).reset_index()
    print('Original dedup alog DF: ' + str(len(alog_dat['report_id'])))

    # Drop Duplicate Rows, Keep The Last of Duplicates    
    unique_df = alog_dat.drop_duplicates(subset = ['report_id'], keep = 'last')
    print('Deduped alog DF: ' + str(len(unique_df['report_id'])))

    # Return the Deduplicated Dataframe
    return unique_df

def main():
    # Get RSS data as far back as possible.
    df = rss_reduce()

    # Append df to an existing CSV. Note set headers to True first run.
    df.to_csv('./_data/aLOG_RSS.csv', mode='a', header=False, index=False)

    # Remove duplicates
    csv = csv_cleanup()

    # Append df to a Fresh Deduplicated CSV.
    csv.to_csv('./_data/aLOG_RSS_deduplicated.csv', index=False)

    # Return CSV for Debugging
    return csv

#####################################################################################################
test = main()

#####################################################################################################
# BACKLOG: ##########################################################################################
# 1. Begin prompting for alog
# 2. Clean up this file, and document, document, document
# 3. Where should I call the prompts?
#####################################################################################################


