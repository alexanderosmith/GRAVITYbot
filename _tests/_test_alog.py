#####################################################################################################
# DOCUMENTATION NOTES : #############################################################################
# File Author: Alexander O. Smith, aosmith@syr.edu
# Current Maintainer: Alexander O. Smith, aosmith@syr.edu
# Last Update: May 1, 2024
# Program Goal:
# This script automates gathering aLOG posts from LIGO to be analyzed for Citizen Scientists
#####################################################################################################
# DEPENDENCIES ######################################################################################
import feedparser as fp                     # Parsing LIGO's aLOG RSSs
from bs4 import BeautifulSoup as bs         # Scraping static HTML urls
import requests, re
from datetime import datetime, timedelta    # Managing datetime objects
import lxml.html as lh                      # Translating HTML/XML/LXML to readable format
from lxml import etree
import pandas as pd                         # Dataframe stuff (Pandas and CSV)
import csv, ssl, os.path                    # SSL: dealing with RSS security certificate issues
#####################################################################################################
#####################################################################################################
# FUNCTIONS #########################################################################################
# 1. rss_reduce     : reduces all RSS feeds to necessary data and outputs them into a dataframe
# 2. url_reduce     : reduces the non-rss links to data to merge with rss_reduce's df        (To Do!)
# 3. csv_cleanup    : cleans up the saved data for use in __test_main__.py                   (To Do!)
# 4. warnings       : simple text that states the limitation of this script for now
# 5. main           : enables a call within __test_main__.py
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

    # Return completed dataframe
    return df

def url_reduce():
    # url_reduce TO DO: 
    # 1. clean uri data
    # 2. capture headers and subheaders in the loop (unsure what issue is here)
    # 3. capture user names
    # 4. add other URLs to the url list and check them with the same code
    # 5. figure out pagination
    # 6. For good metadata housekeeping, format url_reduce's df analogously to rss_reduce's 
    
    urls = [
        "https://logbook.virgo-gw.eu/virgo/",    # VIRGO
        #"https://klog.icrr.u-tokyo.ac.jp/osl/",  # KAGRA
        # If more url's exist, add them here
    ]
    for url in urls:
        #"Pagination" occurs under this XPath: /html/body/div[3]/div/select
        page = requests.get(url)
        parser = lh.HTMLParser(encoding='utf-8')
        tree = lh.fromstring(page.content)
        soup = bs(page.content, "html.parser")

        # Scraped Data 
        date = tree.xpath('//div/section[1]/text()')
        uri = tree.xpath(f'//div[4]/div/section[1]/a//@onclick')   

        # Data Cleaning
        # TO DO: uri needs cleaning
        dates = ([d for d in date if len(d) > 5])
        dates = [re.sub('^-\s', '', d.strip()) for d in dates]  
        
        # I have validated that this counts the actual number of posts on a page
        posts = len(tree.xpath('//div[4]/div/article/p[1]'))
        
        # We still need to figure this one out...
        user_name = tree.xpath('//div[4]/div/section[1]/a//text()') # 

        text_body = []
        header_1 = []
        header_2 = []
        subheader = []

        p = 1
        # NOTICE: The posts = the full number of posts.
        while len(text_body) <= posts:
            # Getting Post Text
            txt = f'//div[4]/div[{p}]/article[1]//text()'
            body = tree.xpath(txt)
            body = ' '.join(body)
            # TO DO: Check these in loop
            head_1 = tree.xpath(f'//div[4]/div{p}/header/b/a[1]/text()')
            head_2 = tree.xpath(f'//div[4]/div{p}/header/b/a[2]/text()')
            subhead = tree.xpath(f'//div[4]/div{p}/section[2]/b//text()')
            #print(f'{p} Returns: {head_1}, {head_2}, {subhead}')
            header_1.append(head_1)
            header_2.append(head_2)
            subheader.append(subhead)

            if len(body) >= 2:
                #print(f'{p} --- {body}')
                b = re.sub(r'\s{2,}', ' ', str(body))
                if len(b) > 1:
                    text_body.append(b)
            if p > 200:
                print(f'Limit {p} was reached________')
                break
            p+=1

        #pagination = soup.find("select", id="next_reports").text
        # TO-DO:
        # HTML Modify example:
        # The first "page" looks like the following element.
        # <option value="1" selected="selected">1-25</option>
        # The second "page" looks like this, and requires modifying it to look like the previous
        # <option value="26">26-50</option>
        # You may need to modify the first 
        # Python Example: https://stackoverflow.com/questions/40775930/using-beautifulsoup-to-modify-html

        #pagination.find_all("option")
        #print('Posts: '+pagination)
        #print('\n\n'+forum+'\n\n')
        
        #!!! NOTICE: Remove everything after this after debugging
        print(header_1)
        print(f'Posts:       {posts} (All the following should equal this #)')
        print(f'Dates:       {len(dates)}')
        print(f'Report URIs: {len(uri)}')
        print(f'Headers:     {len(header)}')
        print(f'User Names:  {len(user_name)}')
        print(f'Subheaders:  {len(subheader)}')
        print(f'Text Body:   {len(text_body)}')

    return text_body, report_uri, header_1, header_2, subheader

example = url_reduce()
example
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
    # Get data as far back as possible.
    df_rss = rss_reduce(3)
    df_url = url_reduce()
    
    # Append df to an existing CSV. Note set headers to True first run.
    df_rss.to_csv('./_data/test_aLOG_RSS.csv', mode='a', header=False)
    #df_url.to_csv('./_data/test_aLOG_URL.csv', mode='a', header=False)
    
    # Print some limitations and considerations someone using this script might come across.
    warn = warnings()

    return df_rss, df_url, warn

#####################################################################################################
test = main()
#####################################################################################################
# BACKLOG: ##########################################################################################
# 1. Make sure you're actually capturing the text in the HTML file during scraping/cleaning.
# 2. Build CSV Clean Function
# 3. Decide on RSS and Scrape Function. Regardless, make their data mergeable
# 4. Take a look at cleaned text data for prompt inspirations for prompts.py
#####################################################################################################
# Scratch work
# Reduce duplicate rows of function results
# Need to connect this to an output dataset

urls_ex = [
    "https://logbook.virgo-gw.eu/virgo/",    # VIRGO
    #"https://klog.icrr.u-tokyo.ac.jp/osl/",  # KAGRA
    # If more url's exist, add them here
    ]
for url in urls_ex:
    page = requests.get(url)
    tree = lh.fromstring(page.content)
    soup = bs(page.content, "html.parser")

    # Example:
    report_uri = tree.xpath('//div[4]/div/section[1]/a//@onclick') # 29

    # Needs to be done in a loop
    user_name = tree.xpath('//div[4]/div/section[1]/a//text()') 

    # These are all kinda similar because they all exist under the main post
    header_1 = tree.xpath('//div[4]/div/header/b/a[1]//text()') # 25
    header_2 = tree.xpath('//div[4]/div/header/b/a[2]//text()') # 25
    subheader = tree.xpath('//div/section[2]/b/text()')  # 25

    #/html/body/div[4]/div[29]/header
    
len(report_uri)
len(header_1)