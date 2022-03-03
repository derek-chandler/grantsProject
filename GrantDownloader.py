# required libraries
import os
import zipfile
import wget
import requests
from time import sleep, time
from bs4 import BeautifulSoup as bs
from http.client import RemoteDisconnected
from requests.exceptions import ConnectionError


"""
get the latest zip file from grants.gov

creates directories:
    ./cache/
    ./cache/extracted

FULL URL EXAMPLE
https://www.grants.gov/extract/GrantsDBExtract20220203v2.zip
"""


# unzips the file into cache/extracted
# used in multiple places, so it's implemented as a function to save time
def unzip_xml(filename):
    with zipfile.ZipFile(filename, 'r') as data:
        data.extractall("cache/extracted/")


# driver function using beautifulsoup4 web scraping library
def get(runtime=False):
    if runtime:
        initial_time = time()
    #################################################
    ## Cache directory creation/existence checking ##
    #################################################
    # "current working directory"
    # aka where the python script is running in
    cwd = os.getcwd()
    # if cache folder does not exist, make it
    if not os.path.isdir(cwd + "/cache"):
        print("creating cache directory")
        os.mkdir(cwd + "/cache")
    # if extracted folder does not exist, make it
    if not os.path.isdir(cwd + "/cache/extracted"):
        print("creating extracted directory")
        os.mkdir(cwd + "/cache/extracted")

    ######################################################################
    ## Use bs4 to grab the latest filename straight from the website :) ##
    ######################################################################
    print("getting latest XML dump")
    xml_dumps_url = "https://www.grants.gov/web/grants/xml-extract.html"
    # grab the XML dump page
    xml_dumps_page = requests.get(xml_dumps_url)
    # make sure it's successful
    successful = False
    while not successful:
        status = xml_dumps_page.status_code
        if status == 200:
            successful = True
        else:
            print(
                "status code is {0}, waiting 15 seconds to retry...".format(status))
            sleep(15)
            xml_dumps_page = requests.get(xml_dumps_url)
    # web page
    soup = bs(xml_dumps_page.content, 'html.parser')
    # table containing XML links
    xml_link_entries = soup.find_all('table', {"class": "grid"})[0]
    # find all <a> tags which has href="", since that's where the links are stored
    xml_hrefs = xml_link_entries.find_all('a', href=True)
    # get just the last href since that's the latest one
    grant_url = xml_hrefs[len(xml_hrefs)-1]['href']
    # split URL at "/"
    split_url = grant_url.split("/")
    # remove v2.zip from the end because i cba to change later code
    filename = split_url[len(split_url)-1].split("v2.zip")[0]

    print("today's file grabbed ({0}), downloading...".format(filename))

    ######################################################
    ## Check if XML or zip files already exist in cache ##
    ######################################################
    # test if XML file exists first to avoid re-downloading zip if unnecessary
    if os.path.isfile(cwd + "/cache/extracted/" + filename + "v2.xml"):
        print("XML file exists")
        return cwd + "/cache/extracted/" + filename + "v2.xml"
    # test if zip file exists
    if os.path.isfile(cwd + "/cache/" + filename + "v2.zip"):
        print("zip file exists, unzipping")
        unzip_xml(cwd + "/cache/" + filename + "v2.zip")
        return cwd + "/cache/extracted/" + filename + "v2.xml"
    print("does not exist, downloading")

    ########################################################
    ## Download zip file, if necessary according to above ##
    ########################################################
    # download
    successful = False
    while not successful:
        try:
            wget.download(grant_url, "cache/")
            successful = True
        # sometimes the site prevents connection due to crawl-delay
        except ConnectionError as e:
            print("connection aborted, waiting 15 seconds...")
            sleep(15)
        # ... and sometimes the site disconnects before wget wants it to...
        # the file should still be downloaded just fine
        # (manually checked sha1 checksum vs. normally downloaded file and it checked out)
        except RemoteDisconnected as e:
            print("remote disconnected, verifying if file exists...")
            if os.path.isfile(cwd + "/cache/" + filename + "v2.zip"):
                successful = True
                print("file exists, continuing")
            else:
                print("file does not exist, attempting re-download")

    ########################################
    ## Unzip and return the FULL filepath ##
    ########################################
    print("\nunzipping")
    unzip_xml(cwd + "/cache/" + filename + "v2.zip")
    if runtime:
        print("took {0}s".format(time() - initial_time))
    return cwd + "/cache/extracted/" + filename + "v2.xml"


# this is for debugging. remove this line and call get() function directly from
#   GrantsParserXML.py
# print(get())
