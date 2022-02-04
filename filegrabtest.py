import os
import zipfile
import wget
import requests
from requests.exceptions import ConnectionError
from http.client import RemoteDisconnected
from datetime import datetime, timedelta

from time import sleep

"""
get the latest zip file from grants.gov based on current date

if today's isn't available, grab yesterday's, or the one before, etc.

creates directories cache/ and cache/extracted in current directory

FULL URL EXAMPLE
https://www.grants.gov/extract/GrantsDBExtract20220203v2.zip
"""

# http headers just in case
# "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
http_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}


# generates properly formatted filename based on today's date
# i.e. parsing the CURRENT date into YYYYMMDD format
def gen_filename(today=True, delta=1):
    # if requesting today's date
    # the reason this exists is because of timedelta being subtracted from current date
    if today:
        current_date = datetime.now().strftime("%Y%m%d")
    else:
        yesterday = datetime.now() - timedelta(days=delta)
        current_date = yesterday.strftime("%Y%m%d")
    # concat to the proper format
    filename = "GrantsDBExtract" + current_date
    return filename


# sends HEAD request and returns the http status number
# e.g. 301, 200, 404
def get_request_status(grant_url, headers=http_headers):
    print("getting status of " + grant_url)
    successful = False
    while not successful:
        try:
            req = requests.head(grant_url, headers=http_headers)
            successful = True
        #
        except ConnectionError as e:
            print("connection aborted, waiting 15 seconds...")
            sleep(15)
    status = req.status_code
    print("status is {0}".format(status))
    return status
    ex


# creates a proper URL from filename
# filename excludes the v2 and extension
def gen_proper_url(filename):
    base_url = "https://www.grants.gov/extract/"
    return base_url + filename + "v2.zip"


# unzips the file into cache/extracted
# used in multiple places, so it's implemented as a function to save time
def unzip_xml(filename):
    with zipfile.ZipFile(filename, 'r') as data:
        data.extractall("cache/extracted/")


# returns a tuple of the most recent filename (Grantblabla) and the url to the zip file
# max_age is the maximum number of days old grantdata can be, in case they decide not to
#   upload one that day for like.... a week or something. never know
def get_latest_info(max_age=4):
    # range excludes last value so add 1
    max_age += 1
    for i in range(0, max_age):
        filename = gen_filename(today=False, delta=i)
        grant_url = gen_proper_url(filename)
        status = get_request_status(grant_url)
        if status == 200:
            return (filename, grant_url)
        elif status == 404 and i == 3:
            print("could not download the file.")
            exit(0)
    return (filename, grant_url)


def get():
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

    print("getting latest information")
    info = get_latest_info(max_age=4)
    filename = info[0]
    grant_url = info[1]
    print("today's filename generated ({0})".format(filename))
    print("checking if exists")

    # test if XML file exists first so it doesn't re-download
    if os.path.isfile(cwd + "/cache/extracted/" + filename + "v2.xml"):
        print("XML file exists")
        return cwd + "/cache/extracted/" + filename + "v2.xml"
    # test if zip file exists
    if os.path.isfile(cwd + "/cache/" + filename + "v2.zip"):
        print("zip file exists, unzipping")
        unzip_xml(cwd + "/cache/" + filename + "v2.zip")
        return cwd + "/cache/extracted/" + filename + "v2.xml"
    print("does not exist, downloading")

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

    print("\nunzipping")
    unzip_xml(cwd + "/cache/" + filename + "v2.zip")
    return cwd + "/cache/extracted/" + filename + "v2.xml"
