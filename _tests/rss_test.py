#####################################################################################################
# DEPENDENCIES ######################################################################################
import feedparser as fp                     # Parsing LIGO's aLOG RSSs
from bs4 import BeautifulSoup as bs         # Scraping static HTML urls
import requests
from datetime import datetime, timedelta    # Managing datetime objects
import lxml.html as lh                      # Translating HTML/XML/LXML to readable format
import pandas as pd                         # Dataframe stuff (Pandas and CSV)
import csv, ssl, re, pytz                   # SSL: dealing with RSS security certificate issues
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
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# Existing RSS Feeds (2 other aLOG URLs don't have these and may need to scrape)
LIGO_RSSs = [
    "https://alog.ligo-wa.caltech.edu/aLOG/rss-feed.php", # LHO
    "https://alog.ligo-la.caltech.edu/aLOG/rss-feed.php", # LLO
    ]

text = []
entry_titles = []
entry_urls = []
for f in LIGO_RSSs:
    rss_feed = fp.parse(f)

    # Define the time range
    now = datetime.now()
    time_range = timedelta(weeks=2)

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
            
            # From full_html there's at least three more useful variables: report_id, author, text
            att_html = bs(full_html, "html.parser")
            
            # Cleaning Report ID
            rep_id = att_html.find_all("p")[1].text
            rep_id = re.sub('Report ID: ', '', rep_id)        
                
            # Cleaning Author Email
            auth = att_html.p.text
            auth = re.sub('Author: ', '', auth)
            
            # Cleaning Text
            txt = att_html.get_text(separator=' ')
            txt = re.sub(r'[\n\t]', ' ', txt)
            txt = re.sub(',', '', txt)
            txt = re.sub(r'^.*Report ID: \d+ ', '', txt)
            txt = re.sub(' Images attached to this report ', '', txt)
            txt = re.sub(r'\s+', ' ', txt)
            text.append(txt)
            entry_titles.append(entry_title)
            entry_urls.append(entry_url)

text = []
entry_titles = []
entry_urls = []
for f in LIGO_RSSs:
    rss_feed = fp.parse(f)

    # Define the time range
    now = datetime.now()
    time_range = timedelta(weeks=2)

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
            
            # From full_html there's at least three more useful variables: report_id, author, text
            att_html = bs(full_html, "html.parser")
            
            # Cleaning Report ID
            rep_id = att_html.find_all("p")[1].text
            rep_id = re.sub('Report ID: ', '', rep_id)        
                
            # Cleaning Author Email
            auth = att_html.p.text
            auth = re.sub('Author: ', '', auth)
            
            # Cleaning Text
            txt = att_html.get_text(separator=' ')
            txt = re.sub('[\n\t]', ' ', txt)
            txt = re.sub('[,;]', '', txt)
            txt = re.sub(r'^.*Report ID: \d+ ', '', txt)
            txt = re.sub(' Images attached to this report ', '', txt)
            txt = re.sub(r'\s+', ' ', txt)
            text.append(txt)
            entry_titles.append(entry_title)
            entry_urls.append(entry_url)

len(entry_titles)
len(entry_urls)

print(text[40:60])

file_path = "_data/aLOG_RSS_deduplicated.csv"
with open(file_path, encoding='utf-8') as file:
    reader = csv.DictReader(file)

    # Define the Universal timezone
    utc = pytz.UTC

    # Set up lists for dataframe return
    txt         =   []
    times       =   []
    comment_urls=   []

    for row in reader:
        text = row['text']
        txt.append(text)

        # Define time formats with and without microseconds
        date_fmt = "%a, %d %b %Y %H:%M:%S %z"
        #fmt_dot_ms = '%Y-%m-%d %H:%M:%S.%f%z'
        #fmt_wo_ms = '%Y-%m-%d %H:%M:%S%z'

        # Timestamp Data Clean
        timestamp = row['entry_date']

        try:
        # Parse the timestamp
            time = datetime.strptime(timestamp, date_fmt).astimezone(utc)
            times.append(time)
            
        except:
            print(f'Datetime Conversion Warning')
            times.append('datetime_conversion_issue')
            

        url = row['entry_url']
        comment_urls.append(url)

    # Generate DataFrame of data necessary for GRAVITYbot interpretation
    text_dat = pd.DataFrame({
        'timestamp'     : times,
        'comment'       : txt,
        'comment_url'   : comment_urls,
    })

print(text_dat.timestamp)

import smtplib
from email.mime.text import MIMEText

# The smtp.example.com here should be replaced with the actual name of the SMTP server you are using.
smtp_server = smtp.example.com

# Log in to the SMTP server
smtp_user = your_email@example.com
smtp_password = your_password
smtp_connection = smtplib.SMTP(smtp_server)
smtp_connection.login(smtp_user, smtp_password)