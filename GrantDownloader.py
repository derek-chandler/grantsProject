"""
get the latest zip file from grants.gov
creates directories:
    ./cache/
    ./cache/extracted
FULL URL EXAMPLE
https://www.grants.gov/extract/GrantsDBExtract20220203v2.zip


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import sys
import traceback
import zipfile
from http.client import RemoteDisconnected
from time import sleep

import requests
import wget
from bs4 import BeautifulSoup as bs
from requests.exceptions import ConnectionError

"""

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
    except Exception:
        print("There was an exception while cleaning temp files in " + cwd)
        print(traceback.print_stack())


# cleans old zip and XML files in cache if there is a new one
# takes the input of the current grant file name. it should be formatted like this:
#   GrantsDBExtract20220203
# as is with the rest of the script.
def cleanOldCache(currentfilename):
    # cache directory
    cache_dir = os.path.join(cwd, "cache")
    # cache/extracted directory
    xml_dir = os.path.join(cache_dir, "extracted")
    # full filepath for the current cached .zip file
    current_zip = os.path.join(cache_dir, currentfilename + "v2.zip")
    # full filepath for the current cached .xml file
    current_xml = os.path.join(xml_dir, currentfilename + "v2.xml")
    try:
        for filename in os.listdir(cache_dir):
            f = os.path.join(cache_dir, filename)
            if os.path.isfile(f):
                # if the .zip is the latest one dont remove
                if f == current_zip:
                    continue
                # otherwise remove if .zip
                else:
                    os.remove(f)
        for filename in os.listdir(xml_dir):
            f = os.path.join(xml_dir, filename)
            if os.path.isfile(f):
                # if the .xml is the latest one dont remove
                if f == current_xml:
                    continue
                # otherwise remove
                else:
                    os.remove(f)
    except Exception as e:
        print("There was an exception while cleaning old cache files in " + cache_dir)
        print(traceback.print_stack())


# unzips the file into cache/extracted
# used in multiple places, so it's implemented as a function to save time
def unzip_xml(file_path):
    with zipfile.ZipFile(file_path, 'r') as data:
        data.extractall(os.path.join(cwd, "cache", "extracted"))


# driver function using beautifulsoup4 web scraping library
def get():
    #################################################
    ## Cache directory creation/existence checking ##
    #################################################
    # cache_dir
    cache_dir = os.path.join(cwd, "cache")
    extract_dir = os.path.join(cwd, "cache", "extracted")
    # extract_dir
    # if cache folder does not exist, make it
    if not os.path.isdir(cache_dir):
        print("creating cache directory")
        os.mkdir(cache_dir)
    # if extracted folder does not exist, make it
    if not os.path.isdir(extract_dir):
        print("creating extracted directory")
        os.mkdir(extract_dir)

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
            # 10 seconds is defined in https://www.grants.gov/robots.txt
            # but really, 15 seconds is more reliable
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
    xml_path = os.path.join(extract_dir, filename + "v2.xml")
    zip_path = os.path.join(cache_dir, filename + "v2.zip")
    if os.path.isfile(xml_path):
        print("XML file exists")
        return xml_path
    # test if zip file exists
    if os.path.isfile(zip_path):
        print("zip file exists, unzipping...", end="")
        unzip_xml(zip_path)
        print("done")
        return xml_path
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
            wget.download(grant_url, cache_dir)
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
            if os.path.isfile(zip_path):
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
    unzip_xml(zip_path)
    return xml_path
