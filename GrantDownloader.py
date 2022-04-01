# required libraries
import os
import sys
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

# "current working directory"
# aka where the python script is running in
cwd = os.getcwd()


# cleans temporary (*.tmp) files in case of program halt or error
def cleanTmp():
    try:
        for filename in os.listdir(cwd):
            f = os.path.join(cwd, filename)
            if os.path.isfile(f):
                if f.endswith(".tmp"):
                    os.remove(f)
    except Exception as e:
        print("There was an exception while cleaning temp files in " + cwd)
        print(e.with_traceback())


# cleans old zip and XML files in cache if there is a new one
# takes the input of the current grant file name. it should be formatted like this:
#   GrantsDBExtract20220203
# as is with the rest of the script.
def cleanOldCache(currentfilename):
    # cache directory
    cachedir = cwd + "/cache"
    # cache/extracted directory
    xmldir = cachedir + "/extracted"
    # full filepath for the current cached .zip file
    currentzip = cachedir + "/" + currentfilename + "v2.zip"
    # full filepath for the current cached .xml file
    currentxml = xmldir + "/" + currentfilename + "v2.xml"
    try:
        for filename in os.listdir(cachedir):
            f = os.path.join(cachedir, filename)
            if os.path.isfile(f):
                # if the .zip is the latest one dont remove
                if f == currentzip:
                    continue
                # otherwise remove if .zip
                else:
                    os.remove(f)
        for filename in os.listdir(xmldir):
            f = os.path.join(xmldir, filename)
            if os.path.isfile(f):
                # if the .xml is the latest one dont remove
                if f == currentxml:
                    continue
                # otherwise remove
                else:
                    os.remove(f)
    except Exception as e:
        print("There was an exception while cleaning old cache files in " + cachedir)
        print(e.with_traceback())


# unzips the file into cache/extracted
# used in multiple places, so it's implemented as a function to save time
def unzip_xml(filename):
    with zipfile.ZipFile(filename, 'r') as data:
        data.extractall("cache/extracted/")


# driver function using beautifulsoup4 web scraping library
def get(_time=False):
    if _time:
        initial_time = time()
    #################################################
    ## Cache directory creation/existence checking ##
    #################################################
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

    print("today's file grabbed ({0}), checking...".format(filename), end="")

    ######################################################
    ## Check if XML or zip files already exist in cache ##
    ######################################################
    # test if XML file exists first to avoid re-downloading zip if unnecessary
    if os.path.isfile(cwd + "/cache/extracted/" + filename + "v2.xml"):
        print("XML file exists")
        if _time:
            print("took {0}s".format(time() - initial_time))
        return cwd + "/cache/extracted/" + filename + "v2.xml"
    # test if zip file exists
    if os.path.isfile(cwd + "/cache/" + filename + "v2.zip"):
        print("zip file exists, unzipping", end="")
        unzip_xml(cwd + "/cache/" + filename + "v2.zip")
        print("done")
        if _time:
            print("took {0}s".format(time() - initial_time))
        return cwd + "/cache/extracted/" + filename + "v2.xml"
    print("does not exist\ndownloading...")

    ########################################################
    ## Download zip file, if necessary according to above ##
    ########################################################
    # download
    successful = False
    while not successful:
        try:
            # clean up old zip files
            cleanOldCache(filename)
            wget.download(grant_url, "cache/")
            successful = True
        # sometimes the site prevents connection due to crawl-delay
        except ConnectionError:
            print("connection aborted, waiting 15 seconds...")
            sleep(15)
        # ... and sometimes the site disconnects before wget wants it to...
        # the file should still be downloaded just fine
        # (manually checked sha1 checksum vs. normally downloaded file and it checked out)
        except RemoteDisconnected:
            print("remote disconnected, verifying if file exists...")
            # if the zip file exists, then wget downloaded it
            # otherwise it stays as a .tmp file
            if os.path.isfile(cwd + "/cache/" + filename + "v2.zip"):
                successful = True
                print("file exists, continuing")
            else:
                cleanTmp()
                print("file does not exist, attempting re-download")
        # clean up temporary files if the script is manually interrupted
        except KeyboardInterrupt:
            cleanTmp()
            sys.exit(0)

    ########################################
    ## Unzip and return the FULL filepath ##
    ########################################
    print("\nunzipping")
    unzip_xml(cwd + "/cache/" + filename + "v2.zip")
    if _time:
        print("took {0}s".format(time() - initial_time))
    return cwd + "/cache/extracted/" + filename + "v2.xml"
